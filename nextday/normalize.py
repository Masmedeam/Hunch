"""Explicit adapters for inspected provider payloads; unknown fields stay in raw files."""
import hashlib
import json
import re
import sqlite3
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from .client import save_json


def digest(value):
    return hashlib.sha256(value.encode()).hexdigest()


def canonical_url(url):
    if not isinstance(url, str) or not url.startswith(("https://", "http://")):
        return None
    parts = urlsplit(url)
    query = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True)
             if not k.lower().startswith("utm_") and k.lower() not in {"fbclid", "gclid", "ref"}]
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path, urlencode(query), ""))


def iso(dt):
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def as_datetime(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def timestamp(value, captured_at):
    if value is None or value == "":
        return None, "unknown"
    try:
        if isinstance(value, str) and re.fullmatch(r"\d{10}|\d{13}", value):
            value = int(value)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            seconds = value / 1000 if value > 10**11 else value
            return iso(datetime.fromtimestamp(seconds, timezone.utc)), "machine_timestamp"
        text = str(value)
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
            return text + "T00:00:00Z", "day"
        dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
        if dt.tzinfo is not None:
            return iso(dt), "machine_timestamp"
    except (ValueError, TypeError, OverflowError, OSError):
        pass
    try:
        dt = parsedate_to_datetime(str(value))
        if dt.tzinfo is not None:
            return iso(dt), "machine_timestamp"
    except (ValueError, TypeError):
        pass
    for fmt in ("%b %d, %Y", "%B %d, %Y"):
        try:
            return iso(datetime.strptime(str(value), fmt).replace(tzinfo=timezone.utc)), "day"
        except ValueError:
            pass
    match = re.search(r"(\d+)\s+(minute|hour|day|week)s?\s+ago", str(value), re.I)
    if match:
        seconds = int(match[1]) * {"minute": 60, "hour": 3600, "day": 86400, "week": 604800}[match[2].lower()]
        return iso(datetime.fromisoformat(captured_at.replace("Z", "+00:00")) - timedelta(seconds=seconds)), "relative_estimate"
    return None, "unparsed"


def metric(value, path, semantics="cumulative_snapshot"):
    """Don't convert rounded labels (1.2M) into exact counts, or missing into zero."""
    if isinstance(value, bool) or value is None:
        return None
    try:
        count = Decimal(str(value).replace(",", ""))
        if not count.is_finite() or count < 0 or count != count.to_integral_value():
            return None
        return {"value": int(count), "native_field": path, "semantics": semantics, "precision": "reported_integer"}
    except InvalidOperation:
        return None


def metrics_from(item, mapping, prefix="", semantics="cumulative_snapshot"):
    result = {}
    for name, field in mapping.items():
        parsed = metric(item.get(field), prefix + field, semantics)
        if parsed is not None:
            result[name] = parsed
    return result


def youtube_metrics(item):
    result = metrics_from(item, {"views": "viewCountInt", "likes": "likeCountInt", "comments": "commentCountInt"})
    for name, display_field in {"views": "viewCountText", "likes": "likeCountText", "comments": "commentCountText"}.items():
        display = item.get(display_field)
        if name in result and display and re.search(r"\d\s*[KMB万億]", str(display), re.I):
            result[name]["precision"] = "rounded_display"
            result[name]["display_raw"] = display
    return result


def normalize_envelope(envelope, raw_file=""):
    run, spec = envelope["run"], envelope["spec"]
    output = run.get("output")
    if not isinstance(output, dict) or run["status"] != "COMPLETED":
        return []
    if output.get("success") is False:
        return []
    data = output.get("data") or {}
    source = spec["source"]
    captured = envelope["captured_at"]
    records = []

    def add(item, path, platform, kind, native_id, title=None, text=None, url=None, published=None,
            date_text=None, author=None, metrics=None, rank=None, extra=None):
        entity = str(native_id) if native_id is not None else canonical_url(url)
        if not entity:
            return
        published_at, precision = timestamp(published if published is not None else date_text, captured)
        if date_text and precision == "machine_timestamp" and re.search(r"\bago\b", str(date_text), re.I):
            precision = "provider_derived_relative"
        recency = "unknown"
        if published_at:
            dt = as_datetime(published_at)
            end = as_datetime(captured)
            recency = "future_timestamp" if dt > end else ("older_than_7_days" if dt < end - timedelta(days=7) else "within_7_days")
        scope = ":" + spec.get("region", "unknown") if kind in {"trend", "hashtag"} else ""
        record = {"schema_version": 1, "observation_id": digest(run["id"] + ":" + path),
                  "entity_id": platform + ":" + kind + ":" + entity + scope, "native_id": native_id,
                  "platform": platform, "kind": kind, "title": title, "text": text, "url": canonical_url(url),
                  "published_at": published_at, "publication_precision": precision,
                  "publication_recency_at_capture": recency,
                  "publication_raw": published, "publication_date_text": date_text,
                  "captured_at": captured, "provider_completed_at": run.get("completed_at"),
                  "author": author, "metrics": metrics or {}, "rank": rank,
                  "hashtags": list(dict.fromkeys(re.findall(r"#[\w]+", text or title or "", re.UNICODE))),
                  "source": source, "provider": run["provider"], "endpoint": run["endpoint"],
                  "endpoint_version": run["endpoint_version"], "requested_region": spec.get("region", "unknown"),
                  "requested_language": spec.get("language", "unknown"), "topic": spec.get("topic"),
                  "window_semantics": spec.get("window_semantics"), "run_id": run["id"], "run_url": run.get("run_url"),
                  "raw_file": str(raw_file), "native_path": path, "extra": extra or {}}
        records.append(record)

    if source in {"news", "news_text"}:
        key = "news" if source == "news" else "results"
        for i, item in enumerate(output.get(key) or []):
            url = item.get("link") or item.get("url")
            add(item, f"/{key}/{i}", "web", "article", None, item.get("title"),
                item.get("text") or item.get("snippet"), url, item.get("publishedDate"), item.get("date"),
                {"name": item.get("source") or item.get("author")},
                extra={"text_kind": "captured_body" if item.get("text") else "snippet", "possible_truncation": bool(item.get("text") and len(item["text"]) >= 8000)})
    elif source == "x_trends":
        for i, item in enumerate(data.get("trends") or []):
            add(item, f"/data/trends/{i}", "x", "trend", item.get("name"), item.get("name"),
                text=item.get("description"), rank=i + 1,
                extra={"context": item.get("context"), "rank_semantics": "response_position"})
    elif source in {"x_search", "x_detail"}:
        items = [(f"/data/timeline/{i}", x) for i, x in enumerate(data.get("timeline") or [])] if source == "x_search" else [("/data", data)]
        for i, (path, item) in enumerate(items):
            native = item.get("tweet_id") if source == "x_search" else item.get("id")
            if native is None:
                continue
            ident = str(native)
            user = item.get("user_info") or item.get("author") or {}
            add(item, path, "x", "post", ident, text=item.get("text"),
                url=f'https://x.com/{item.get("screen_name") or user.get("screen_name") or "i"}/status/{ident}',
                published=item.get("created_at"),
                author={"id": user.get("rest_id"), "handle": user.get("screen_name"), "name": user.get("name"), "followers": user.get("followers_count"), "sub_count_raw": user.get("sub_count")},
                metrics=metrics_from(item, {"views": "views", "likes": "likes" if source == "x_detail" else "favorites", "comments": "replies", "shares": "retweets", "quotes": "quotes", "bookmarks": "bookmarks"}), rank=i + 1 if source == "x_search" else None,
                extra={"language": item.get("lang"), "rank_semantics": "search_result_position" if source == "x_search" else None})
    elif source in {"tiktok_search", "tiktok_trends", "tiktok_detail"}:
        items = [(f"/aweme_list/{i}", x) for i, x in enumerate(output.get("aweme_list") or [])]
        items += [(f"/search_item_list/{i}/aweme_info", x["aweme_info"]) for i, x in enumerate(output.get("search_item_list") or []) if isinstance(x.get("aweme_info"), dict)]
        if isinstance(output.get("aweme_detail"), dict):
            items.append(("/aweme_detail", output["aweme_detail"]))
        if isinstance(output.get("aweme_id"), (str, int)):
            items.append(("", output))
        for i, (path, item) in enumerate(items):
            ident = item.get("aweme_id")
            user, stats, music = item.get("author") or {}, item.get("statistics") or {}, item.get("music") or {}
            url = item.get("url") or (item.get("share_info") or {}).get("share_url")
            add(item, path, "tiktok", "post", str(ident) if ident else None,
                title=(item.get("image_post_info") or {}).get("title"), text=item.get("desc") or item.get("search_desc"),
                url=url, published=item.get("create_time_utc") or item.get("create_time"),
                author={"id": user.get("uid"), "handle": user.get("unique_id"), "name": user.get("nickname"), "followers": user.get("follower_count")},
                metrics=metrics_from(stats, {"views": "play_count", "likes": "digg_count", "comments": "comment_count", "shares": "share_count", "bookmarks": "collect_count"}, "statistics."), rank=i + 1,
                extra={"reported_post_region": item.get("region"), "reported_language": item.get("desc_language"), "is_ad": item.get("is_ad"), "music_id": music.get("id_str") or music.get("id"), "music_title": music.get("title")})
    elif source in {"youtube_search", "youtube_shorts", "youtube_detail"}:
        items = [(f"/{key}/{i}", item) for key in ["videos", "shorts", "lives"] for i, item in enumerate(output.get(key) or [])]
        if output.get("id") and output.get("title"):
            items.append(("", output))
        for path, item in items:
            ident = item.get("id")
            user = item.get("channel") or {}
            add(item, path, "youtube", "video", ident, title=item.get("title"), text=item.get("description"),
                url=item.get("url") or (f"https://www.youtube.com/watch?v={ident}" if ident else None),
                published=item.get("publishedTime") or item.get("publishDate"), date_text=item.get("publishedTimeText"),
                author={"id": user.get("id"), "handle": user.get("handle"), "name": user.get("title")},
                metrics=youtube_metrics(item),
                extra={"video_type": item.get("type"), "duration_seconds": item.get("lengthSeconds") or (item["durationMs"] / 1000 if item.get("durationMs") else None), "views_display": item.get("viewCountText"), "comments_display": item.get("commentCountText")})
    elif source in {"tiktok_hashtags", "tiktok_hashtag_detail"}:
        items = [(f"/data/items/{i}", x) for i, x in enumerate(data.get("items") or [])] if source == "tiktok_hashtags" else [("/data", data)]
        for path, item in items:
            add(item, path, "tiktok", "hashtag", item.get("hashtagID"), title=item.get("hashtagName"),
                metrics=metrics_from(item, {"views": "vv", "posts": "publishCnt"}, semantics="provider_window_aggregate_definition_unverified"),
                rank=item.get("rankIndex"), extra={"popularity_curve": item.get("popularityCurve"), "industry_ids": item.get("industryIDs"), "range_days": spec["input"].get("time_range"), "reported_range_days": item.get("timeRange"), "reported_country": item.get("countryCode"), "age_profile": item.get("ageProfile"), "country_profile": item.get("representativeCountryProfile"), "curve_units": "provider_native_unverified"})
    elif source == "tiktok_search_trends":
        for i, item in enumerate(data.get("trending_search_words") or []):
            word = item.get("trendingSearchWord")
            add(item, f"/data/trending_search_words/{i}", "tiktok", "trend", word, title=word, rank=i + 1,
                extra={"provider_type": item.get("trendingSearchWordType"), "rank_semantics": "response_position"})
    elif source in {"zillow_mortgage_rates", "zillow_property", "zillow_agents", "zillow_open_houses"}:
        rows = output.get("results") or output.get("items") or output.get("agents") or ([output] if isinstance(output, dict) else [])
        for i, item in enumerate(rows if isinstance(rows, list) else [rows]):
            if not isinstance(item, dict):
                continue
            ident = item.get("zpid") or item.get("id") or item.get("screenName") or spec["input"].get("zpid") or spec["input"].get("url") or f"{source}-{i}"
            kind = "rate" if source == "zillow_mortgage_rates" else "listing"
            add(item, f"/{i}", "zillow", kind, str(ident),
                title=item.get("address") or item.get("streetAddress") or item.get("name") or "Zillow Snapshot",
                text=item.get("description") or json.dumps({k: v for k, v in item.items() if k in {"rate", "apr", "price", "zestimate", "homeStatus", "daysOnZillow"}}, ensure_ascii=False),
                url=item.get("url") or spec["input"].get("url"),
                metrics=metrics_from(item, {"price": "price", "zestimate": "zestimate", "days_on_zillow": "daysOnZillow"}),
                extra={"vertical": "real_estate", "location": spec["input"].get("location")})
    elif source == "airbnb_search":
        rows = output.get("results") or output.get("items") or output.get("listings") or []
        for i, item in enumerate(rows if isinstance(rows, list) else []):
            if not isinstance(item, dict):
                continue
            ident = item.get("id") or item.get("listingId") or item.get("url")
            add(item, f"/results/{i}", "airbnb", "listing", str(ident) if ident else None,
                title=item.get("name") or item.get("title"),
                text=item.get("description") or item.get("roomType"),
                url=item.get("url"),
                metrics=metrics_from(item, {"nightly_price": "price", "reviews": "reviewsCount"}),
                rank=i + 1,
                extra={"vertical": "hospitality", "check_in": spec["input"].get("checkIn"), "check_out": spec["input"].get("checkOut"), "rating": item.get("rating")})
    elif source in {"linkedin_jobs", "linkedin_company", "linkedin_posts", "wellfound_jobs"}:
        rows = output.get("jobs") or output.get("results") or output.get("posts") or output.get("items") or ([output] if isinstance(output, dict) else [])
        for i, item in enumerate(rows if isinstance(rows, list) else [rows]):
            if not isinstance(item, dict):
                continue
            ident = item.get("id") or item.get("jobId") or item.get("urn") or item.get("url") or spec["input"].get("url")
            kind = "job" if source in {"linkedin_jobs", "wellfound_jobs"} else ("company" if source == "linkedin_company" else "post")
            add(item, f"/{i}", "linkedin", kind, str(ident) if ident else f"{source}-{i}",
                title=item.get("title") or item.get("jobTitle") or item.get("name"),
                text=item.get("description") or item.get("text") or item.get("tagline"),
                url=item.get("url") or item.get("jobUrl") or spec["input"].get("url"),
                published=item.get("postedAt") or item.get("publishedAt") or item.get("created_at"),
                author={"name": item.get("companyName") or item.get("company") or item.get("authorName")},
                metrics=metrics_from(item, {"applicants": "applicantsCount", "employees": "employeeCount", "followers": "followerCount", "likes": "likeCount", "comments": "commentCount"}),
                rank=i + 1,
                extra={"vertical": "job_market", "location": item.get("location") or spec.get("region")})
    for row in records:
        curve = row["extra"].get("popularity_curve") or []
        dates = [at for point in curve if (at := timestamp(point.get("timestamp"), captured)[0])]
        if dates:
            row["extra"]["curve_start_at"] = min(dates, key=as_datetime)
            row["extra"]["curve_end_at"] = max(dates, key=as_datetime)
            row["extra"]["curve_last_point_age_days"] = (as_datetime(captured) - as_datetime(row["extra"]["curve_end_at"])).total_seconds() / 86400
            row["extra"]["curve_freshness"] = "older_than_requested_week" if row["extra"]["curve_last_point_age_days"] > 7 else "recent_points"
    return records


def trend_points(observations):
    points = []
    for obs in observations:
        for i, point in enumerate(obs["extra"].get("popularity_curve") or []):
            at, precision = timestamp(point.get("timestamp"), obs["captured_at"])
            age = (as_datetime(obs["captured_at"]) - as_datetime(at)).total_seconds() / 86400 if at else None
            points.append({"entity_id": obs["entity_id"], "observation_id": obs["observation_id"],
                           "captured_at": obs["captured_at"], "point_at": at, "timestamp_precision": precision,
                           "point_age_days_at_capture": age, "value_raw": point.get("value"),
                           "unit": "provider_popularity_index_unverified", "requested_range_days": obs["extra"].get("range_days"),
                           "native_path": obs["native_path"] + f"/popularityCurve/{i}", "run_url": obs["run_url"]})
    return points


def growth(observations):
    """Only comparable exact cumulative counters; preserve decreases as warnings."""
    groups = defaultdict(list)
    for obs in observations:
        for name, entry in obs["metrics"].items():
            if entry["semantics"] == "cumulative_snapshot" and entry.get("precision", "reported_integer") == "reported_integer":
                groups[(obs["entity_id"], obs["provider"], obs["endpoint"], name)].append((obs, entry))
    changes = []
    for (entity, provider, endpoint, name), samples in groups.items():
        samples.sort(key=lambda x: as_datetime(x[0]["captured_at"]))
        for (a, av), (b, bv) in zip(samples, samples[1:]):
            elapsed = (datetime.fromisoformat(b["captured_at"].replace("Z", "+00:00")) - datetime.fromisoformat(a["captured_at"].replace("Z", "+00:00"))).total_seconds()
            if elapsed < 60:
                continue
            delta = bv["value"] - av["value"]
            changes.append({"entity_id": entity, "provider": provider, "endpoint": endpoint, "metric": name,
                            "start": a["captured_at"], "end": b["captured_at"], "elapsed_seconds": elapsed,
                            "delta": delta, "per_hour": delta * 3600 / elapsed,
                            "counter_decreased": delta < 0, "observation_ids": [a["observation_id"], b["observation_id"]]})
    return changes


def write_jsonl(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False) + "\n")


def rebuild(root="data", cutoff=None, since=None):
    root = Path(root)
    if cutoff:
        parsed = datetime.fromisoformat(cutoff.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            raise ValueError("Export cutoff must include a UTC offset.")
        cutoff = iso(parsed)
    if since:
        parsed = datetime.fromisoformat(since.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            raise ValueError("Export start must include a UTC offset.")
        since = iso(parsed)
        if cutoff and as_datetime(since) > as_datetime(cutoff):
            raise ValueError("Export start is after its cutoff.")
    observations, runs, audits = {}, {}, []
    for path in sorted((root / "batches").glob("*/raw/*.json")):
        envelope = json.loads(path.read_text())
        if cutoff and as_datetime(envelope["captured_at"]) > as_datetime(cutoff):
            continue
        if since and as_datetime(envelope["captured_at"]) < as_datetime(since):
            continue
        run = envelope["run"]
        if run["status"] not in {"COMPLETED", "FAILED", "STOPPED"}:
            continue
        rows = normalize_envelope(envelope, path)
        for row in rows:
            observations[row["observation_id"]] = row
        runs[run["id"]] = run
        audits.append({"run_id": run["id"], "run_url": run.get("run_url"), "source": envelope["spec"]["source"],
                       "status": run["status"], "provider_http_status": (run.get("provider_response") or {}).get("http_status"),
                       "charge_usd": run.get("charge_usd"), "normalized_records": len(rows), "raw_file": str(path)})
    rows = sorted(observations.values(), key=lambda x: (as_datetime(x["captured_at"]), x["observation_id"]))
    by_entity = defaultdict(list)
    for row in rows:
        by_entity[row["entity_id"]].append(row)
    context = []
    for entity, samples in by_entity.items():
        record = dict(samples[-1])
        record["discovery_contexts"] = [dict(zip(("source", "topic", "requested_region", "requested_language"), values)) for values in sorted(set((x["source"], x.get("topic") or "unknown", x["requested_region"], x["requested_language"]) for x in samples))]
        record["observation_ids"] = [x["observation_id"] for x in samples]
        # A currently trending old post is a current attention signal. An old
        # news article is not recent news; keep it in observations, not context.
        if record["kind"] != "article" or record["publication_recency_at_capture"] == "within_7_days":
            context.append(record)
    export_name = cutoff.replace(":", "-") if cutoff else "latest"
    if since:
        export_name += "__from_" + since.replace(":", "-")
    export = root / "exports" / export_name
    write_jsonl(export / "observations.jsonl", rows)
    write_jsonl(export / "context.jsonl", context)
    changes = growth(rows)
    write_jsonl(export / "engagement_growth.jsonl", changes)
    curves = trend_points(rows)
    write_jsonl(export / "trend_points.jsonl", curves)
    write_jsonl(export / "run_audit.jsonl", audits)
    report = {"schema_version": 1, "cutoff": cutoff, "since": since, "observations": len(rows), "unique_entities": len(by_entity),
              "runs": len(runs), "charged_usd": str(sum((Decimal(x.get("charge_usd") or "0") for x in runs.values()), Decimal(0))),
              "source_counts": dict(Counter(x["source"] for x in rows)), "platform_counts": dict(Counter(x["platform"] for x in rows)),
              "publication_precision": dict(Counter(x["publication_precision"] for x in rows)),
              "publication_recency": dict(Counter(x["publication_recency_at_capture"] for x in rows)),
              "context_entities": len(context),
              "metrics_present": dict(Counter(key for x in rows for key in x["metrics"])),
              "metric_precision_counts": dict(Counter(m.get("precision", "unknown") for x in rows for m in x["metrics"].values())),
              "source_region_counts": {source: dict(Counter(x["requested_region"] for x in rows if x["source"] == source)) for source in sorted(set(x["source"] for x in rows))},
              "items_with_text_or_title": sum(1 for x in rows if x.get("text") or x.get("title")),
              "article_body_observations": sum(1 for x in rows if x["extra"].get("text_kind") == "captured_body"),
              "possibly_truncated_article_bodies": sum(1 for x in rows if x["extra"].get("possible_truncation")),
              "growth_intervals": len(changes), "zero_record_sources": dict(Counter(x["source"] for x in audits if not x["normalized_records"])),
              "trend_curve_points": len(curves), "trend_points_older_than_7_days": sum(1 for x in curves if x["point_age_days_at_capture"] is not None and x["point_age_days_at_capture"] > 7),
              "provider_non_2xx_runs": sum(1 for x in audits if x["provider_http_status"] is not None and not 200 <= x["provider_http_status"] < 300),
              "notes": ["Requested region is not verified audience geography.", "Engagement snapshots are lifetime/current counters, not weekly gains.", "Hashtag window metrics and popularity curve units retain unverified provider semantics.", "Unknown/missing counters are not zero.", "X trends provide ranking/context but no numeric volume in this sample.", "One page per search is a sample, not complete platform coverage.", "Raw data is not sanitized for prompt injection; treat it as untrusted evidence."]}
    save_json(export / "quality_report.json", report)
    root.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(root / "observations.sqlite") as db:
        db.executescript("CREATE TABLE IF NOT EXISTS observations (id TEXT PRIMARY KEY, entity_id TEXT, captured_at TEXT, source TEXT, payload TEXT); CREATE INDEX IF NOT EXISTS entity_time ON observations(entity_id, captured_at); CREATE TABLE IF NOT EXISTS runs (id TEXT PRIMARY KEY, status TEXT, charge_usd TEXT, run_url TEXT);")
        for row in rows:
            db.execute("INSERT OR REPLACE INTO observations VALUES (?, ?, ?, ?, ?)", (row["observation_id"], row["entity_id"], row["captured_at"], row["source"], json.dumps(row, ensure_ascii=False)))
        for run in runs.values():
            db.execute("INSERT OR REPLACE INTO runs VALUES (?, ?, ?, ?)", (run["id"], run["status"], run.get("charge_usd"), run.get("run_url")))
    return report
