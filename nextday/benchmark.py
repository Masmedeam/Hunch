"""Historical case acquisition and isolated evidence/answer packs.

Raw backfills are private. Publication times are never relabeled as capture times.
No forecasting or model-judge requests are made by this module.
"""
import hashlib
import json
import math
import re
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from html.parser import HTMLParser
from pathlib import Path
from zoneinfo import ZoneInfo

from .client import save_json
from .collector import utcnow
from .normalize import as_datetime, canonical_url, iso, timestamp, write_jsonl

DEFAULT_ROOT = "data/benchmarks/retrospective-v0"
CIKS = {"AAPL": "320193", "MSFT": "789019", "NVDA": "1045810", "AMZN": "1018724",
        "GOOGL": "1652044", "META": "1326801", "JPM": "19617", "XOM": "34088", "WMT": "104169", "NFLX": "1065280"}
NEWS_QUERIES = [
    ("diplomacy", "International diplomacy government sanctions ceasefire public policy announcements"),
    ("business", "Company earnings business regulatory announcements United States Europe Asia"),
    ("economy", "Economy inflation energy oil transport developments United States India Europe"),
    ("technology", "Artificial intelligence technology product research announcements"),
    ("climate_health", "Severe weather climate cyclone public health official updates"),
    ("culture", "Entertainment music film cultural announcements releases")
]
QUESTION_TEMPLATES = [
    {"slot": "q1", "track": "numeric_anchor", "rule": "If the target is a US regular trading weekday: next-day return of predetermined rotating ticker. Otherwise: next-day total EDGAR 8-K filing count."},
    {"slot": "q2", "track": "corporate_event", "rule": "At least one original 8-K acceptance in the fixed verified company cohort during the target UTC day."},
    {"slot": "q3", "track": "social_publication", "rule": "Next-day number of retrievable original NASA X posts under the frozen search protocol, not historical views/comments."},
    {"slot": "q4", "track": "world_narrative", "rule": "Up to three specific next-day world developments from history; judge against held-out reporting, acknowledging incomplete world coverage."},
    {"slot": "q5", "track": "social_narrative", "rule": "Up to three next-day topics/publication developments on the fixed social cohort; no claims of historical engagement velocity."}
]


class FilingText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style"}:
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in {"script", "style"}:
            self.skip = max(0, self.skip - 1)

    def handle_data(self, data):
        if not self.skip and data.strip():
            self.parts.append(data.strip())


def filing_text(output):
    value = output if isinstance(output, str) else None
    if isinstance(output, dict):
        value = next((output.get(k) for k in ["content", "text", "html", "document"] if isinstance(output.get(k), str)), None)
    if not value:
        return None
    if re.search(r"request originates from an undeclared|request rate threshold exceeded|access denied", value, re.I):
        return None
    parser = FilingText()
    parser.feed(value)
    return "\n".join(parser.parts) if "<" in value else value


def dates_between(start, end):
    current = date.fromisoformat(start)
    last = date.fromisoformat(end)
    while current <= last:
        yield current.isoformat()
        current += timedelta(days=1)


def job(source, provider, endpoint, inputs, **metadata):
    return {"source": source, "provider": provider, "endpoint": endpoint, "input": inputs, **metadata}


def freeze_protocol(root=DEFAULT_ROOT, plan_file="config/benchmark-plan.json"):
    root = Path(root)
    path = root / "protocol.json"
    if path.exists():
        return json.loads(path.read_text())
    plan = json.loads(Path(plan_file).read_text())
    cutoffs = plan["proposed_cutoff_dates_utc"]
    first = date.fromisoformat(min(cutoffs)) - timedelta(days=6)
    last = date.fromisoformat(max(cutoffs)) + timedelta(days=1)
    protocol = {"schema_version": 1, "frozen_at": utcnow(), "evaluation_mode": "retrospective_reconstructed",
                "cutoff_dates": cutoffs, "history_start": first.isoformat(), "collection_end": last.isoformat(),
                "lookback_days": 7, "horizon_hours": 24, "tickers": plan["numeric_anchor_tickers"], "expected_ciks": CIKS,
                "x_accounts": ["NASA", "WHO", "BBCWorld"], "tiktok_accounts": ["bbcnews", "dwnews"],
                "youtube_accounts": ["NASA", "BBCNews"], "news_queries": NEWS_QUERIES,
                "question_templates": QUESTION_TEMPLATES, "max_x_pages_per_account_day": 5,
                "max_profile_pages": 12, "youtube_details_per_estimated_day_per_channel": 3,
                "price_policy": "Frozen provider bars; adjustment/revision semantics unknown. No current financial metrics in inputs.",
                "social_policy": "Publication content only; all current engagement counters omitted. Search/profile survivorship and edit history remain unknown.",
                "selection_policy": "Dates, cohorts and templates frozen before target retrieval. No outcome-based question/case selection.",
                "source_plan": plan}
    save_json(path, protocol)
    save_json(root / "private_raw/approval.json", {"total_max_usd": "10.00", "scope": "User-approved historical benchmark scraping only; independent of previous collection and inference."})
    return protocol


def make_plan(phase, root=DEFAULT_ROOT):
    protocol = freeze_protocol(root)
    start, end = protocol["history_start"], protocol["collection_end"]
    jobs = []
    if phase == "audit":
        day = protocol["cutoff_dates"][0]
        jobs = [job("benchmark_prices", "financialdatasets", "/prices", {"ticker": "AAPL", "interval": "day", "start_date": start, "end_date": day}),
                job("benchmark_company", "financialdatasets", "/company/facts", {"ticker": "AAPL"}),
                job("benchmark_filings", "secapi", "/edgar-index/ingestion-log/{date}", {"date": day}, day=day),
                job("benchmark_x", "tikhub", "/api/v1/twitter/web/fetch_search_timeline", {"keyword": f"from:NASA -is:retweet -is:reply since:{day} until:{(date.fromisoformat(day)+timedelta(days=1)).isoformat()}", "search_type": "Latest"}, day=day, account="NASA", page=1),
                job("benchmark_tiktok", "scrapecreators", "/v3/tiktok/profile/videos", {"handle": "bbcnews", "sort_by": "latest"}, account="bbcnews", page=1),
                job("benchmark_youtube", "scrapecreators", "/v1/youtube/channel-videos", {"handle": "NASA", "sort": "latest"}, account="NASA", page=1)]
        for topic, query in NEWS_QUERIES[:2]:
            jobs.append(job("benchmark_news", "exa", "/search", {"query": query, "category": "news", "numResults": 10,
                            "startPublishedDate": day+"T00:00:00Z", "endPublishedDate": day+"T23:59:59Z", "contents": {"text": {"maxCharacters": 8000}}}, day=day, topic=topic))
    elif phase == "core":
        # The audit's short AAPL history is not reused as a full-range price query.
        for ticker in protocol["tickers"]:
            jobs.append(job("benchmark_prices", "financialdatasets", "/prices", {"ticker": ticker, "interval": "day", "start_date": start, "end_date": end}))
            if ticker != "AAPL":
                jobs.append(job("benchmark_company", "financialdatasets", "/company/facts", {"ticker": ticker}))
        for day in dates_between((date.fromisoformat(start)-timedelta(days=1)).isoformat(), end):
            if day != protocol["cutoff_dates"][0]:
                jobs.append(job("benchmark_filings", "secapi", "/edgar-index/ingestion-log/{date}", {"date": day}, day=day))
        for day in dates_between(start, end):
            for account in protocol["x_accounts"]:
                lo = (date.fromisoformat(day)-timedelta(days=1)).isoformat()
                hi = (date.fromisoformat(day)+timedelta(days=2)).isoformat()
                jobs.append(job("benchmark_x", "tikhub", "/api/v1/twitter/web/fetch_search_timeline", {"keyword": f"from:{account} -is:retweet -is:reply since:{lo} until:{hi}", "search_type": "Latest"}, day=day, account=account, page=1, boundary_buffer_days=1))
        ciks = " OR ".join(protocol["expected_ciks"].values())
        query = f'cik:({ciks}) AND formType:"8-K" AND filedAt:[{start} TO {(date.fromisoformat(end)+timedelta(days=1)).isoformat()}]'
        jobs.append(job("benchmark_company_filings", "secapi", "/filings/search", {"query": query, "size": 50, "from": 0, "sortOrder": "asc"}, page=1))
        jobs += [job("benchmark_tiktok", "scrapecreators", "/v3/tiktok/profile/videos", {"handle": account, "sort_by": "latest"}, account=account, page=1) for account in protocol["tiktok_accounts"] if account != "bbcnews"]
        jobs += [job("benchmark_youtube", "scrapecreators", "/v1/youtube/channel-videos", {"handle": account, "sort": "latest"}, account=account, page=1) for account in protocol["youtube_accounts"] if account != "NASA"]
    elif phase == "news":
        for day in dates_between(start, end):
            for topic, query in NEWS_QUERIES:
                if day == protocol["cutoff_dates"][0] and topic in {"diplomacy", "business"}:
                    continue
                jobs.append(job("benchmark_news", "exa", "/search", {"query": query, "category": "news", "numResults": 10,
                                "startPublishedDate": day+"T00:00:00Z", "endPublishedDate": day+"T23:59:59Z",
                                "contents": {"text": {"maxCharacters": 8000}}}, day=day, topic=topic))
    else:
        raise ValueError("Unknown benchmark acquisition phase.")
    return {"schema_version": 1, "phase": phase, "protocol_sha256": hashlib.sha256(json.dumps(protocol, sort_keys=True).encode()).hexdigest(), "jobs": jobs}


def raw_snapshots(root=DEFAULT_ROOT):
    """Read the persisted latest terminal response once per intended Run."""
    snapshots = []
    for path in sorted((Path(root) / "private_raw/batches").glob("*/manifest.json")):
        manifest = json.loads(path.read_text())
        for entry in manifest["jobs"]:
            if entry.get("status") in {"COMPLETED", "FAILED", "STOPPED"} and entry.get("raw_file"):
                snapshots.append(json.loads(Path(entry["raw_file"]).read_text()))
    return snapshots


def usable(envelope):
    run = envelope["run"]
    http = (run.get("provider_response") or {}).get("http_status", 0)
    output = run.get("output")
    return run["status"] == "COMPLETED" and 200 <= http < 300 and output is not None and not (isinstance(output, dict) and output.get("success") is False)


def timeline(output):
    data = output.get("data") or {}
    return data.get("timeline") or []


def profile_items(output, source):
    if source == "benchmark_tiktok":
        return output.get("aweme_list") or []
    return output.get("videos") or []


def item_time(item, source, captured):
    if source == "benchmark_tiktok":
        return timestamp(item.get("create_time_utc") or item.get("create_time"), captured)
    if source == "benchmark_youtube":
        # publishDate is the machine publication timestamp; publishedTime may
        # have been reconstructed by the provider from a rounded relative label.
        if item.get("publishDate"):
            return timestamp(item["publishDate"], captured)
        return None, "needs_exact_publication_detail"
    return timestamp(item.get("created_at"), captured)


def filings_rows(output):
    if not isinstance(output, dict):
        return None
    if isinstance(output.get("filings"), list):
        return output["filings"]
    if isinstance(output.get("data"), list):
        return output["data"]
    return None


def exact_total(output):
    total = output.get("total") if isinstance(output, dict) else None
    if isinstance(total, dict) and total.get("relation") == "eq":
        return int(total["value"])
    if isinstance(total, int):
        return total
    return None


def series_key(spec):
    source = spec["source"]
    if source == "benchmark_x":
        return source, spec.get("account"), spec.get("day"), spec.get("boundary_buffer_days", 0)
    if source in {"benchmark_tiktok", "benchmark_youtube"}:
        return source, spec["account"]
    if source == "benchmark_company_filings":
        return source, spec["input"]["query"]
    return source, json.dumps(spec["input"], sort_keys=True)


def continuation_plan(root=DEFAULT_ROOT):
    protocol = freeze_protocol(root)
    groups = defaultdict(list)
    for envelope in raw_snapshots(root):
        if envelope["spec"]["source"] in {"benchmark_x", "benchmark_tiktok", "benchmark_youtube", "benchmark_company_filings"}:
            groups[series_key(envelope["spec"])].append(envelope)
    jobs = []
    for key, samples in sorted(groups.items(), key=lambda x: str(x[0])):
        samples.sort(key=lambda x: x["spec"].get("page", 1))
        latest = samples[-1]
        spec = latest["spec"]
        source = spec["source"]
        if not usable(latest) or (source == "benchmark_x" and not spec.get("boundary_buffer_days")):
            continue
        output = latest["run"]["output"]
        inputs = dict(spec["input"])
        page = spec.get("page", 1)
        token = None
        field = None
        if source == "benchmark_x":
            rows = timeline(output)
            previous_ids = {r.get("tweet_id") for sample in samples[:-1] if usable(sample) for r in timeline(sample["run"]["output"])}
            if not rows or not {r.get("tweet_id") for r in rows} - previous_ids or page >= protocol["max_x_pages_per_account_day"]:
                continue
            token = (output.get("data") or {}).get("next_cursor")
            field = "cursor"
        elif source in {"benchmark_tiktok", "benchmark_youtube"}:
            rows = profile_items(output, source)
            id_field = "aweme_id" if source == "benchmark_tiktok" else "id"
            previous_ids = {r.get(id_field) for sample in samples[:-1] if usable(sample) for r in profile_items(sample["run"]["output"], source)}
            if not rows or not {r.get(id_field) for r in rows} - previous_ids or page >= protocol["max_profile_pages"]:
                continue
            known_times = [at for item in rows if not item.get("is_top") and (at := item_time(item, source, latest["captured_at"])[0])]
            # Stop only when the unpinned response is monotonically newest-first
            # and crosses the collection start; old pinned posts can't stop it.
            if len(known_times) >= 2 and known_times == sorted(known_times, key=as_datetime, reverse=True) and as_datetime(known_times[-1]) < as_datetime(protocol["history_start"]+"T00:00:00Z"):
                continue
            if source == "benchmark_tiktok":
                if not output.get("has_more"):
                    continue
                token = output.get("max_cursor")
                field = "max_cursor"
            else:
                token = output.get("continuationToken")
                field = "continuationToken"
        else:
            rows = filings_rows(output)
            total = exact_total(output)
            if rows is None or not rows or (total is not None and inputs.get("from", 0) + len(rows) >= total) or page >= 20:
                continue
            token = inputs.get("from", 0) + inputs.get("size", 50)
            field = "from"
        if token is None or token == "" or any(sample["spec"]["input"].get(field) == (int(token) if field == "from" else str(token)) for sample in samples):
            continue
        inputs[field] = int(token) if field == "from" else str(token)
        jobs.append(dict(spec, input=inputs, page=page+1))
    return compatible_continuations({"schema_version": 1, "phase": "continuation", "jobs": jobs})


def compatible_continuations(plan):
    """Do not truncate opaque tokens or send values beyond inspected contracts."""
    safe, blocked = [], list(plan.get("blocked_continuations", []))
    for spec in plan["jobs"]:
        invalid = next(((field, len(str(spec["input"][field]))) for field in ["cursor", "continuationToken", "max_cursor"]
                        if spec["input"].get(field) is not None and len(str(spec["input"][field])) > 2048), None)
        if invalid:
            blocked.append({"source": spec["source"], "account": spec.get("account"), "page": spec.get("page"),
                            "reason": "provider_returned_token_exceeds_inspected_input_contract", "field": invalid[0],
                            "characters": invalid[1], "maximum_characters": 2048, "action": "quarantined_not_truncated_or_run"})
        else:
            safe.append(spec)
    return {**plan, "jobs": safe, "blocked_continuations": blocked}


def youtube_detail_plan(root=DEFAULT_ROOT):
    protocol = freeze_protocol(root)
    buckets = defaultdict(dict)
    already = {e["spec"]["input"].get("url") for e in raw_snapshots(root) if e["spec"]["source"] == "benchmark_youtube_detail"}
    for envelope in raw_snapshots(root):
        if envelope["spec"]["source"] != "benchmark_youtube" or not usable(envelope):
            continue
        for item in profile_items(envelope["run"]["output"], "benchmark_youtube"):
            if item.get("publishDate") or not item.get("id"):
                continue
            estimated, _ = timestamp(item.get("publishedTime"), envelope["captured_at"])
            if not estimated or not protocol["history_start"] <= estimated[:10] <= protocol["collection_end"]:
                continue
            key = envelope["spec"]["account"], estimated[:10]
            buckets[key][item["id"]] = item
    jobs = []
    for (account, day), items in sorted(buckets.items()):
        for ident in sorted(items)[:protocol["youtube_details_per_estimated_day_per_channel"]]:
            url = "https://www.youtube.com/watch?v=" + ident
            if url not in already:
                jobs.append(job("benchmark_youtube_detail", "scrapecreators", "/v1/youtube/video", {"url": url}, account=account, estimated_day=day))
    return {"schema_version": 1, "phase": "youtube_publication_details", "jobs": jobs}


def regional_plan(root=DEFAULT_ROOT):
    """Uniform date/region supplement; not selected using target outcomes."""
    protocol = freeze_protocol(root)
    panels = [("regional_japan", "日本の政治 経済 社会 ニュース", "ja"),
              ("regional_india", "India government economy weather technology news", "en"),
              ("regional_brazil", "Brasil notícias política economia clima", "pt"),
              ("regional_middle_east", "أخبار الشرق الأوسط السياسة الاقتصاد", "ar")]
    jobs = []
    for day in dates_between(protocol["history_start"], protocol["collection_end"]):
        for topic, query, language in panels:
            jobs.append(job("benchmark_news", "exa", "/search", {"query": query, "category": "news", "numResults": 10,
                            "startPublishedDate": day+"T00:00:00Z", "endPublishedDate": day+"T23:59:59Z",
                            "contents": {"text": {"maxCharacters": 8000}}}, day=day, topic=topic, query_language=language))
    return {"phase": "uniform_regional_supplement", "selection_policy": "All collection dates, all declared regions; no outcome-dependent selection or question changes.", "jobs": jobs}


def clean_post_text(value):
    # Never dereference embedded links to today's edited article content.
    return re.sub(r"https?://\S+", "[link withheld]", value or "")


def news_leakage_flags(item, cutoff):
    flags = []
    if re.search(r"\blive\s+(?:updates|blog|coverage)\b", item.get("title") or "", re.I):
        flags.append("mutable_live_coverage")
    for key in ("modifiedDate", "dateModified", "updatedAt", "lastUpdated"):
        if item.get(key):
            at, _ = timestamp(item[key], cutoff)
            if at and as_datetime(at) >= as_datetime(cutoff):
                flags.append("explicit_post_cutoff_update")
    text = item.get("text") or ""
    for match in re.finditer(r"(?:last\s+updated|updated\s+(?:on|at)?\s*)[:\s]*(\w+\s+\d{1,2},\s*2026|2026-\d{2}-\d{2})", text, re.I):
        at, _ = timestamp(match[1], cutoff)
        if at and as_datetime(at) >= as_datetime(cutoff):
            flags.append("explicit_post_cutoff_update")
    return sorted(set(flags))


def parse_snapshots(snapshots):
    """Allowlisted fields only: never copy native social statistics into history."""
    records, source_audit, quarantined = [], {}, []
    for envelope in snapshots:
        run, spec = envelope["run"], envelope["spec"]
        source = spec["source"]
        if not usable(envelope):
            continue
        output = run["output"]
        def add(item, path, at, kind, fields, integrity):
            if not at:
                quarantined.append({"run_id": run["id"], "path": path, "reason": "missing_exact_event_or_publication_timestamp"})
                return
            sid = hashlib.sha256((run["id"]+path).encode()).hexdigest()
            record = {"source_id": sid, "kind": kind, "event_at": at, "retrieved_at": envelope["captured_at"],
                      "integrity": integrity, **fields}
            records.append(record)
            source_audit[sid] = {"run_id": run["id"], "run_url": run.get("run_url"), "native_path": path,
                                 "provider": run["provider"], "endpoint": run["endpoint"], "spec": spec}
        if source == "benchmark_filing_document":
            body = filing_text(output)
            at, precision = timestamp(spec.get("filed_at"), envelope["captured_at"])
            if not body or precision != "machine_timestamp":
                quarantined.append({"run_id": run["id"], "reason": "unusable_original_filing_document"})
                continue
            add(output, "", at, "filing_document", {"accession": spec["accession"], "cik": str(spec.get("cik", "")).lstrip("0"),
                "ticker": spec.get("ticker"), "url": spec["input"]["url"], "text": body[:15000], "original_text_characters": len(body),
                "text_truncated": len(body) > 15000}, "original_sec_archive_filing")
        elif source == "benchmark_prices":
            for i, item in enumerate(output.get("prices") or []):
                trading_day = str(item.get("time", ""))[:10]
                try:
                    date.fromisoformat(trading_day)
                    values = {key: str(Decimal(str(item[key]))) for key in ["open", "high", "low", "close", "volume"]}
                    if any(not Decimal(value).is_finite() for value in values.values()):
                        raise ValueError("nonfinite price")
                except (ValueError, KeyError, ArithmeticError):
                    quarantined.append({"run_id": run["id"], "path": f"/prices/{i}", "reason": "invalid_price_bar"})
                    continue
                # Daily-bar availability is explicit and conservative: after the
                # nominal US regular-session close, not at midnight on trade date.
                at = iso(datetime.combine(date.fromisoformat(trading_day), datetime.min.time(), ZoneInfo("America/New_York")).replace(hour=16))
                add(item, f"/prices/{i}", at, "price_bar", {"ticker": spec["input"]["ticker"], "trading_date": trading_day, **values}, "reconstructed_price_bar_revision_semantics_unknown")
        elif source in {"benchmark_filings", "benchmark_company_filings"}:
            rows = filings_rows(output)
            if rows is None:
                quarantined.append({"run_id": run["id"], "reason": "unrecognized_filings_payload"})
                continue
            for i, item in enumerate(rows):
                at, precision = timestamp(item.get("filedAt"), envelope["captured_at"])
                if precision != "machine_timestamp":
                    at = None
                add(item, ("/filings/" if "filings" in output else "/data/")+str(i), at, "filing", {
                    "accession": item.get("accessionNo"), "form": item.get("formType"), "cik": str(item.get("cik", "")).lstrip("0") or None,
                    "ticker": item.get("ticker"), "company": item.get("companyName"), "url": item.get("linkToFilingDetails"),
                    "cohort_search": source == "benchmark_company_filings"}, "timestamped_registry_record")
        elif source == "benchmark_news":
            for i, item in enumerate(output.get("results") or []):
                at, precision = timestamp(item.get("publishedDate"), envelope["captured_at"])
                add(item, f"/results/{i}", at, "article", {"title": item.get("title"), "text": item.get("text") or "",
                "url": canonical_url(item.get("url")), "topic": spec.get("topic"), "publication_precision": precision,
                    "requested_day": spec["day"], "machine_publication_date_not_as_of_capture": True,
                    "text_possible_truncation": len(item.get("text") or "") >= 8000,
                    "explicit_modified_at": {k:item[k] for k in ["modifiedDate", "dateModified", "updatedAt", "lastUpdated"] if item.get(k)}}, "reconstructed_publication_filtered_current_text")
        elif source == "benchmark_x":
            for i, item in enumerate(timeline(output)):
                account = item.get("screen_name") or (item.get("user_info") or {}).get("screen_name")
                if str(account).lower() != spec["account"].lower() or not item.get("tweet_id"):
                    quarantined.append({"run_id": run["id"], "path": f"/data/timeline/{i}", "reason": "unexpected_account_or_missing_post_id"})
                    continue
                at, precision = item_time(item, source, envelope["captured_at"])
                if precision != "machine_timestamp":
                    at = None
                add(item, f"/data/timeline/{i}", at, "social_post", {"platform": "x", "native_id": str(item["tweet_id"]),
                    "account": spec["account"], "text": clean_post_text(item.get("text")), "title": None,
                    "url": f"https://x.com/{account}/status/{item['tweet_id']}", "known_reply": bool(item.get("in_reply_to_status_id_str")),
                    "metrics_policy": "current engagement omitted", "source_query_day": spec["day"]}, "reconstructed_post_content_edit_and_survivorship_unknown")
        elif source in {"benchmark_tiktok", "benchmark_youtube", "benchmark_youtube_detail"}:
            rows = [output] if source == "benchmark_youtube_detail" else profile_items(output, source)
            time_source = "benchmark_youtube" if source == "benchmark_youtube_detail" else source
            for i, item in enumerate(rows):
                at, precision = item_time(item, time_source, envelope["captured_at"])
                if precision != "machine_timestamp":
                    at = None
                platform = "tiktok" if source == "benchmark_tiktok" else "youtube"
                native_id = item.get("aweme_id") if platform == "tiktok" else item.get("id")
                if native_id is None:
                    quarantined.append({"run_id": run["id"], "reason": "missing_social_publication_id"})
                    continue
                add(item, f"/{'aweme_list' if platform == 'tiktok' else 'videos'}/{i}", at, "social_post", {"platform": platform,
                    "native_id": str(native_id), "account": spec["account"], "title": item.get("title"),
                    "text": clean_post_text(item.get("desc")) if platform == "tiktok" else None,
                    "url": canonical_url(item.get("url")), "metrics_policy": "current engagement omitted"}, "reconstructed_post_content_edit_and_survivorship_unknown")
    return records, source_audit, quarantined


def source_completeness(snapshots, protocol):
    logs, x_days, companies = {}, {}, {}
    groups = defaultdict(list)
    for envelope in snapshots:
        spec = envelope["spec"]
        if spec["source"] == "benchmark_filings":
            rows = filings_rows(envelope["run"].get("output")) if usable(envelope) else None
            total = exact_total(envelope["run"].get("output"))
            valid_rows = rows is not None and all(row.get("accessionNo") and row.get("formType") and timestamp(row.get("filedAt"), envelope["captured_at"])[1] == "machine_timestamp" for row in rows)
            logs[spec["day"]] = {"complete": bool(valid_rows and total == len(rows)), "run_id": envelope["run"]["id"]}
        elif spec["source"] == "benchmark_company" and usable(envelope):
            facts = envelope["run"]["output"].get("company_facts") or {}
            ticker = spec["input"]["ticker"]
            companies[ticker] = companies.get(ticker, False) or str(facts.get("cik", "")).lstrip("0") == protocol["expected_ciks"].get(ticker)
        elif spec["source"] == "benchmark_company_cik" and usable(envelope):
            for row in filings_rows(envelope["run"].get("output")) or []:
                ticker = row.get("ticker")
                if ticker in protocol["expected_ciks"] and str(row.get("cik", "")).lstrip("0") == protocol["expected_ciks"].get(ticker):
                    companies[ticker] = True
        elif spec["source"] in {"benchmark_x", "benchmark_company_filings"}:
            groups[series_key(spec)].append(envelope)
    cohort_complete = False
    for key, samples in groups.items():
        samples.sort(key=lambda x: x["spec"].get("page", 1))
        last = samples[-1]
        if key[0] == "benchmark_x":
            if not last["spec"].get("boundary_buffer_days"):
                continue
            ids = {row.get("tweet_id") for e in samples if usable(e) for row in timeline(e["run"]["output"])}
            latest_rows = timeline(last["run"]["output"]) if usable(last) else None
            complete = latest_rows is not None and (not latest_rows or not (last["run"]["output"].get("data") or {}).get("next_cursor"))
            x_days[(key[1], key[2])] = {"complete_under_search_contract": complete, "pages": len(samples), "returned_unique_posts": len(ids),
                                       "warning": "Retrospective search has unknown censorship/deletion/survivorship and boundary behavior; not complete historical platform truth."}
        else:
            rows = [row for e in samples if usable(e) for row in (filings_rows(e["run"]["output"]) or [])]
            total = exact_total(last["run"].get("output"))
            cohort_complete = all(usable(e) for e in samples) and total is not None and len({x.get("accessionNo") for x in rows}) == total
    return {"filing_logs": logs, "x_days": x_days, "verified_company_ciks": companies, "company_search_complete": cohort_complete}


def between(record, start, end):
    return as_datetime(start) <= as_datetime(record["event_at"]) < as_datetime(end)


def clean_case_records(records, start, end):
    selected = []
    excluded = Counter()
    seen = set()
    for record in sorted(records, key=lambda x: (as_datetime(x["event_at"]), x["retrieved_at"])):
        if not between(record, start, end):
            continue
        if record["kind"] == "filing" and not record.get("cohort_search"):
            continue  # Full-market records remain private; history gets daily counts.
        if record["kind"] == "article":
            flags = news_leakage_flags({**record, **record.get("explicit_modified_at", {})}, end)
            if flags:
                excluded.update(flags)
                continue
            identity = "article", record.get("url") or record["source_id"]
        elif record["kind"] == "social_post":
            if record.get("known_reply"):
                excluded["known_reply_not_original_publication"] += 1
                continue
            identity = record["platform"], record["native_id"]
        elif record["kind"] == "price_bar":
            identity = "price", record["ticker"], record["trading_date"]
        elif record["kind"] == "filing_document":
            identity = "document", record.get("url")
        else:
            identity = "filing", record.get("accession")
        if identity in seen:
            continue
        seen.add(identity)
        safe = {key:value for key,value in record.items() if key not in {"explicit_modified_at", "source_query_day", "cohort_search", "known_reply"}}
        selected.append(safe)
    return selected, dict(excluded)


def compact_history(history, max_records=200, text_chars=1500):
    """Uniform, outcome-independent common input profile; full evidence retained."""
    from collections import deque
    core = [r for r in history["evidence"] if r["kind"] in {"price_bar", "filing", "filing_document"}]
    core.sort(key=lambda r: r["event_at"])
    groups = defaultdict(list)
    for record in history["evidence"]:
        if record["kind"] not in {"price_bar", "filing", "filing_document"}:
            groups[(record["event_at"][:10], record["kind"], record.get("topic") or record.get("platform"))].append(record)
    selected = list(core[:max_records])
    queues = [deque(sorted(group, key=lambda r:r["source_id"])) for _,group in sorted(groups.items(), key=lambda x:str(x[0]))]
    while queues and len(selected) < max_records:
        next_queues = []
        for queue in queues:
            if len(selected) < max_records:
                selected.append(queue.popleft())
            if queue:
                next_queues.append(queue)
        queues = next_queues
    compact = []
    for record in selected:
        row = dict(record)
        if row.get("text") and len(row["text"]) > text_chars:
            row["original_text_characters_before_compaction"] = len(row["text"])
            row["text"] = row["text"][:text_chars]
            row["input_text_truncated"] = True
        compact.append(row)
    return {**history, "input_profile": {"name": "compact-200x1500-v1", "maximum_records": max_records,
            "text_character_limit": text_chars, "full_history_records": len(history["evidence"]),
            "selection": "Keep structured anchors, then deterministic round-robin day/type/topic/platform strata; no outcome/current-engagement selection."},
            "evidence": compact}


def filing_day_count(records, completeness, day):
    start = day + "T00:00:00Z"
    end = (date.fromisoformat(day)+timedelta(days=1)).isoformat()+"T00:00:00Z"
    neighboring_days = [(date.fromisoformat(day)-timedelta(days=1)).isoformat(), day]
    complete = all(completeness["filing_logs"].get(d, {}).get("complete") for d in neighboring_days)
    matching = {r.get("accession"):r for r in records if r["kind"] == "filing" and not r.get("cohort_search") and r.get("form") == "8-K" and between(r, start, end)}
    return {"date": day, "value": len(matching) if complete else None, "complete": complete,
            "source_ids": [r["source_id"] for r in matching.values()],
            "source_run_ids": [completeness["filing_logs"].get(d, {}).get("run_id") for d in neighboring_days]}


def publication_day_count(records, completeness, account, day):
    start = day+"T00:00:00Z"
    end = (date.fromisoformat(day)+timedelta(days=1)).isoformat()+"T00:00:00Z"
    matching = {r["native_id"]:r for r in records if r["kind"] == "social_post" and r["platform"] == "x" and r["account"].lower() == account.lower() and between(r, start, end)}
    complete = completeness["x_days"].get((account, day), {}).get("complete_under_search_contract", False)
    return {"date": day, "account": account, "observed_count": len(matching), "complete_under_search_contract": complete,
            "value": len(matching) if complete else None, "source_ids": [r["source_id"] for r in matching.values()]}


def generate_case(protocol, records, completeness, cutoff_day, index):
    """Question wording/cohorts depend on protocol/calendar/history, never targets."""
    target_day = date.fromisoformat(cutoff_day)+timedelta(days=1)
    start = (date.fromisoformat(cutoff_day)-timedelta(days=6)).isoformat()+"T00:00:00Z"
    cutoff = target_day.isoformat()+"T00:00:00Z"
    end = (target_day+timedelta(days=1)).isoformat()+"T00:00:00Z"
    case_id = "day-"+cutoff_day
    history, excluded = clean_case_records(records, start, cutoff)
    daily_filings = [filing_day_count(records, completeness, day) for day in dates_between(start[:10], cutoff_day)]
    daily_publications = [publication_day_count(records, completeness, "NASA", day) for day in dates_between(start[:10], cutoff_day)]
    # Histories contain aggregates from known pre-cutoff days only, with no
    # source links into a multi-day raw response containing held-out data.
    public = {"schema_version": 1, "case_id": case_id, "evaluation_mode": "retrospective_reconstructed",
              "history_start": start, "cutoff_exclusive": cutoff, "target_start": cutoff, "target_end": end,
              "evidence": history, "filing_counts": [{k:v for k,v in x.items() if k not in {"source_ids", "source_run_ids"}} for x in daily_filings],
              "publication_counts": [{k:v for k,v in x.items() if k != "source_ids"} for x in daily_publications],
              "limitations": ["Articles/post titles and captions are current versions backfilled by publication time, not archived as-of snapshots.",
                              "Social views, likes, comments and follower counts are intentionally absent.",
                              "Historical source discovery may omit deleted posts and edited content. Search is not complete platform truth.",
                              "Evaluate this case in a fresh stateless call. Other cases' histories may contain this case's held-out next day; never combine cases in one forecaster prompt.",
                              "Price bars may be revised/adjusted. Daily close availability uses a nominal 16:00 America/New_York assumption.",
                              "The model may know historical outcomes from training; this is not a contamination-free benchmark."]}
    ticker = protocol["tickers"][index % len(protocol["tickers"])]
    previous = sorted([x for x in history if x["kind"] == "price_bar" and x["ticker"] == ticker], key=lambda x:x["trading_date"])
    questions = []
    if target_day.weekday() < 5:
        questions.append({"id": case_id+"-q1", "track": "market_direction", "answer_type": "binary", "primary_eligible": True,
                          "question": f"Will {ticker}'s Financial Datasets daily close for {target_day.isoformat()} exceed its most recent daily close available before {cutoff}?",
                          "resolution_rule": "Compare the frozen provider daily close for the target trade date to the last pre-cutoff bar. Missing bars are unresolved, not negative.",
                          "baseline": {"ticker": ticker, "trading_date": previous[-1]["trading_date"] if previous else None, "close": previous[-1]["close"] if previous else None}})
    else:
        questions.append({"id": case_id+"-q1", "track": "registry_count", "answer_type": "numeric", "unit": "accepted original 8-K filings", "primary_eligible": True,
                          "question": f"How many original Form 8-K filings have SEC acceptance timestamps in [{cutoff}, {end}) across the full filing index?",
                          "resolution_rule": "Count unique 8-K accession numbers in the complete frozen SEC daily logs by actual offset-aware filedAt timestamps; require both neighboring Eastern-date logs.",
                          "warning": "Weekend acceptance counts are low-entropy controls, not evidence of difficult forecasting."})
    questions += [
        {"id": case_id+"-q2", "track": "corporate_event", "answer_type": "binary", "primary_eligible": True,
         "question": f"Will any company in {', '.join(protocol['tickers'])} have an original 8-K accepted by the SEC during [{cutoff}, {end})?",
         "resolution_rule": "A matching verified CIK, formType exactly 8-K and acceptance timestamp inside the UTC target interval resolves YES. NO requires complete fixed-cohort filing search and verified mappings; otherwise unresolved."},
        {"id": case_id+"-q3", "track": "social_publication", "answer_type": "numeric", "primary_eligible": False,
         "question": f"How many NASA X posts created during [{cutoff}, {end}) are retrievable through the fixed Latest search protocol with from:NASA -is:retweet -is:reply?",
         "resolution_rule": "Deduplicate tweet IDs, enforce exact UTC created_at times and require observed pagination termination. This is a frozen retrievable-archive count, not complete historical platform activity.",
         "warning": "Experimental search-relative social track. Missing/capped/erroring retrieval is unresolved; no historical engagement target."},
        {"id": case_id+"-q4", "track": "world_narrative", "answer_type": "open_forecasts", "primary_eligible": False,
         "question": f"Using only the supplied week, forecast up to three specific new geopolitical, economic, technology, weather or public-health developments during [{cutoff}, {end}). Provide probabilities when meaningful and abstain when unsupported.",
         "resolution_rule": "Judge against separately held-out reporting and verify claims independently where possible. Unmentioned events are unsupported by this reference corpus, not automatically false; world coverage is incomplete."},
        {"id": case_id+"-q5", "track": "social_narrative", "answer_type": "open_forecasts", "primary_eligible": False,
         "question": f"Predict up to three specific topics or publication developments on the fixed X, TikTok and YouTube account cohort during [{cutoff}, {end}), grounded in the supplied week. Do not infer historical view/comment growth from current counters.",
         "resolution_rule": "Compare to held-out dated publication records from the declared account/format cohort; judge specificity and support. No claim of complete platform trends or historical popularity."}
    ]
    # Hidden target access starts here, after the common questions are fixed.
    target_records, target_excluded = clean_case_records(records, cutoff, end)
    resolutions = []
    q1 = questions[0]
    if q1["answer_type"] == "binary":
        candidates = [x for x in target_records if x["kind"] == "price_bar" and x["ticker"] == ticker and x["trading_date"] == target_day.isoformat()]
        baseline = q1["baseline"]["close"]
        value = Decimal(candidates[-1]["close"]) > Decimal(baseline) if candidates and baseline is not None else None
        resolutions.append({"question_id": q1["id"], "status": "resolved" if value is not None else "unresolved", "value": value,
                            "target_close": candidates[-1]["close"] if candidates else None, "source_ids": [x["source_id"] for x in candidates], "reason": "frozen_provider_daily_bars"})
    else:
        count = filing_day_count(records, completeness, target_day.isoformat())
        resolutions.append({"question_id": q1["id"], "status": "resolved" if count["complete"] else "unresolved", "value": count["value"], "source_ids": count["source_ids"], "reason": "complete_timestamped_registry_logs"})
    cohort = set(protocol["expected_ciks"].values())
    hits = [x for x in target_records if x["kind"] == "filing" and x.get("cik") in cohort and x.get("form") == "8-K"]
    mapped = all(completeness["verified_company_ciks"].get(ticker) for ticker in protocol["tickers"])
    value = True if hits and mapped else (False if mapped and completeness["company_search_complete"] else None)
    resolutions.append({"question_id": case_id+"-q2", "status": "resolved" if value is not None else "unresolved", "value": value,
                        "source_ids": [x["source_id"] for x in hits], "reason": "verified_issuer_timestamped_registry_search"})
    count = publication_day_count(records, completeness, "NASA", target_day.isoformat())
    resolutions.append({"question_id": case_id+"-q3", "status": "resolved_search_relative" if count["complete_under_search_contract"] else "unresolved", "value": count["value"],
                        "observed_lower_bound": count["observed_count"], "source_ids": count["source_ids"], "reason": "not_complete_historical_platform_truth"})
    for suffix, kinds in [("q4", {"article"}), ("q5", {"social_post"})]:
        refs = [x for x in target_records if x["kind"] in kinds]
        resolutions.append({"question_id": case_id+"-"+suffix, "status": "reference_ready" if refs else "unresolved", "value": None,
                            "source_ids": [x["source_id"] for x in refs], "reason": "incomplete_reference_corpus_requires_judge_and_semantic_review"})
    hidden = {"schema_version": 1, "case_id": case_id, "target_start": cutoff, "target_end": end,
              "resolutions": resolutions, "reference_evidence": target_records, "excluded_reference_records": target_excluded,
              "warning": "Reference reporting is not complete world truth. Do not feed this file to forecasters."}
    return public, {"schema_version": 1, "case_id": case_id, "questions": questions}, hidden, excluded


FORBIDDEN_HISTORY_KEYS = {"views", "likes", "comments", "followers", "statistics", "play_count", "digg_count", "viewCountInt", "commentCountInt", "charge_usd", "run_url", "target_close", "resolutions", "reference_evidence"}


def audit_public_history(history, hidden):
    cutoff = history["cutoff_exclusive"]
    for record in history["evidence"]:
        if not as_datetime(history["history_start"]) <= as_datetime(record["event_at"]) < as_datetime(cutoff):
            raise ValueError("Out-of-window record in public history.")
    history_ids = {r["source_id"] for r in history["evidence"]}
    if history_ids & {r["source_id"] for r in hidden["reference_evidence"]}:
        raise ValueError("Target evidence source IDs leaked into public history.")
    def walk(value):
        if isinstance(value, dict):
            if set(value) & FORBIDDEN_HISTORY_KEYS:
                raise ValueError("Forbidden outcome/current-engagement/private-provenance field in public history.")
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)
    walk(history)
    for row in history["filing_counts"] + history["publication_counts"]:
        if row["date"] >= cutoff[:10]:
            raise ValueError("Next-day aggregate leaked into history.")


def load_public_case(case_id, root=DEFAULT_ROOT, compact=False):
    """Forecaster-safe loader: explicit allowlist; never reads private outcomes/raw."""
    if not re.fullmatch(r"day-\d{4}-\d{2}-\d{2}", case_id):
        raise ValueError("Invalid benchmark case ID.")
    folder = Path(root) / "public_inputs" / case_id
    return {"history": json.loads((folder / ("history.compact.json" if compact else "history.json")).read_text()), "questions": json.loads((folder / "questions.json").read_text())}


def build_dataset(root=DEFAULT_ROOT):
    root = Path(root)
    protocol = freeze_protocol(root)
    snapshots = raw_snapshots(root)
    records, source_audit, quarantined = parse_snapshots(snapshots)
    completeness = source_completeness(snapshots, protocol)
    save_json(root / "private_outcomes/source_audit.json", source_audit)
    save_json(root / "private_outcomes/quarantined.json", quarantined)
    cases, status_counts, excluded_counts = [], Counter(), Counter()
    for index, cutoff_day in enumerate(protocol["cutoff_dates"]):
        history, questions, hidden, excluded = generate_case(protocol, records, completeness, cutoff_day, index)
        audit_public_history(history, hidden)
        case_id = history["case_id"]
        folder = root / "public_inputs" / case_id
        question_path = folder / "questions.json"
        if question_path.exists() and json.loads(question_path.read_text()) != questions:
            raise ValueError("Previously materialized benchmark questions changed. Keep them frozen and use a new dataset version.")
        save_json(folder / "history.json", history)
        compact = compact_history(history)
        audit_public_history(compact, hidden)
        save_json(folder / "history.compact.json", compact)
        save_json(question_path, questions)
        save_json(root / "private_outcomes" / case_id / "resolution.json", hidden)
        status_counts.update(x["status"] for x in hidden["resolutions"])
        excluded_counts.update(excluded)
        cases.append({"case_id": case_id, "cutoff": history["cutoff_exclusive"], "questions": len(questions["questions"]),
                      "history_records": len(history["evidence"]), "history_sha256": hashlib.sha256((folder / "history.json").read_bytes()).hexdigest(),
                      "compact_history_records": len(compact["evidence"]), "compact_history_sha256": hashlib.sha256((folder / "history.compact.json").read_bytes()).hexdigest(),
                      "questions_sha256": hashlib.sha256(question_path.read_bytes()).hexdigest()})
    save_json(root / "public_inputs/index.json", {"schema_version": 1, "evaluation_mode": "retrospective_reconstructed", "cases": cases})
    runs = {e["run"]["id"]:e["run"] for e in snapshots}
    charged = sum((Decimal(run.get("charge_usd") or "0") for run in runs.values()), Decimal(0))
    report = {"schema_version": 1, "created_at": utcnow(), "cases": len(cases), "questions": sum(x["questions"] for x in cases),
              "raw_runs": len(runs), "charged_usd": str(charged), "scraping_cap_usd": "10.00", "model_calls": 0,
              "parsed_records": len(records), "record_kinds": dict(Counter(r["kind"] for r in records)),
              "social_platform_records": dict(Counter(r["platform"] for r in records if r["kind"] == "social_post")),
              "quarantined_records": len(quarantined), "excluded_history_reasons_across_cases": dict(excluded_counts),
              "resolution_status_counts": dict(status_counts), "verified_company_ciks": completeness["verified_company_ciks"],
              "company_search_complete": completeness["company_search_complete"], "public_history_leakage_checks": "passed_structured_timestamp_and_field_checks",
              "limitations": ["Historical model-training contamination remains possible.", "Current versions of publication-filtered articles/captions are not guaranteed historical snapshots.",
                              "Narrative cases have held-out reference evidence, not automatically resolved truth.", "Social publication counts are experimental search-relative counts; no historical engagement scores.",
                              "Primary scores must be separate from search-relative/narrative scores. Missing outcomes remain unresolved.", "EDGAR weekends and small cohorts yield low-entropy controls; report track baselines."]}
    save_json(root / "integrity_report.json", report)
    return report
