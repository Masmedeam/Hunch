"""Explicit region/topic sampling plus unprompted trends; no claim of exhaustiveness."""
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path


def build_plan(coverage="config/coverage.json", now=None, news_only=False, verticals=None):
    config = json.loads(Path(coverage).read_text())
    now = now or datetime.now(timezone.utc)
    start = now - timedelta(days=7)
    iso = lambda dt: dt.isoformat(timespec="seconds").replace("+00:00", "Z")
    jobs = []
    seen = set()

    def add(source, provider, endpoint, inputs, region, language, topic, window):
        identity = (provider, endpoint, json.dumps(inputs, sort_keys=True))
        if identity in seen:
            return
        seen.add(identity)
        jobs.append({"source": source, "provider": provider, "endpoint": endpoint, "input": inputs,
                     "region": region, "language": language, "topic": topic, "window_semantics": window})

    for region in config["regions"]:
        code, lang = region["code"], region["language"]
        if news_only:
            for topic in config["topics"]:
                query = topic.get(lang, topic["en"])
                add("news_text", "exa", "/search", {"query": f'Recent reporting about {query} in {region["x_country"]}', "category": "news", "numResults": 10, "startPublishedDate": iso(start), "endPublishedDate": iso(now), "contents": {"text": {"maxCharacters": 8000}}}, code, lang, topic["name"], "publication_date_filter_current_text")
            continue
        add("x_trends", "tikhub", "/api/v1/twitter/web/fetch_trending", {"country": region["x_country"]}, code, lang, "unprompted", "current_ranking")
        add("youtube_trends", "tikhub", "/api/v1/youtube/web/get_trending_videos", {"country_code": code.lower(), "language_code": lang}, code, lang, "unprompted", "current_ranking")
        add("tiktok_trends", "scrapecreators", "/v1/tiktok/get-trending-feed", {"region": code}, code, lang, "unprompted", "current_feed")
        add("tiktok_hashtags", "tikhub", "/api/v1/tiktok/ads/get_trends_hashtag_list", {"country_code": code, "time_range": 7, "limit": 20, "page": 1}, code, lang, "unprompted", "provider_7_day_aggregate")
        for topic in config["topics"]:
            query = topic.get(lang, topic["en"])
            name = topic["name"]
            add("news", "serper", "/news", {"q": query + " when:7d", "gl": code.lower(), "hl": lang}, code, lang, name, "query_hint_7_days_unverified")
            add("x_search", "tikhub", "/api/v1/twitter/web/fetch_search_timeline", {"keyword": f'{query} lang:{lang} since:{start:%Y-%m-%d} until:{now + timedelta(days=1):%Y-%m-%d}', "search_type": "Top"}, "not_filtered", lang, name, "date_filtered_posts_current_engagement")
            add("youtube_search", "scrapecreators", "/v1/youtube/search", {"query": query, "region": code, "sortBy": "popular", "uploadDate": "this_week", "type": "videos"}, code, lang, name, "week_upload_filter_current_engagement")
            add("tiktok_search", "scrapecreators", "/v1/tiktok/search/keyword", {"query": query, "region": code, "sort_by": "most-liked", "date_posted": "this-week"}, code, lang, name, "week_post_filter_current_engagement")
        add("news_text", "exa", "/search", {"query": f'Major news developments in {region["x_country"]} during the past week', "category": "news", "numResults": 10, "startPublishedDate": iso(start), "endPublishedDate": iso(now), "contents": {"text": {"maxCharacters": 8000}}}, code, lang, "general", "publication_date_filter_current_text")
    if not news_only:
        add("tiktok_search_trends", "tikhub", "/api/v1/tiktok/web/fetch_trending_searchwords", {}, "unknown", "unknown", "unprompted", "provider_daily_search_trends")
        vconf = config.get("verticals") or {}
        active_verticals = set(verticals or [k for k, v in vconf.items() if isinstance(v, dict) and v.get("enabled")])
        if "zillow" in active_verticals and "zillow" in vconf:
            zc = vconf["zillow"]
            if zc.get("include_mortgage_rates", True):
                add("zillow_mortgage_rates", "zillow", "/get_mortgage_rates", {}, "US", "en", "real_estate", "current_rate_snapshot")
            for loc in zc.get("locations") or []:
                add("zillow_agents", "zillow", "/search_agents", {"location": loc}, "US", "en", "real_estate", "current_directory_snapshot")
            for url in zc.get("property_urls") or []:
                add("zillow_property", "brightdata", "/datasets/v3/zillow-properties", {"url": url}, "US", "en", "real_estate", "current_listing_snapshot")
            for zpid in zc.get("open_house_zpids") or []:
                add("zillow_open_houses", "zillow", "/get_open_houses", {"zpid": str(zpid)}, "US", "en", "real_estate", "current_listing_snapshot")
        if "airbnb" in active_verticals and "airbnb" in vconf:
            ac = vconf["airbnb"]
            check_in = (now + timedelta(days=int(ac.get("check_in_offset_days", 14)))).strftime("%Y-%m-%d")
            check_out = (now + timedelta(days=int(ac.get("check_in_offset_days", 14)) + int(ac.get("stay_nights", 3)))).strftime("%Y-%m-%d")
            for loc in ac.get("locations") or []:
                add("airbnb_search", "apify", "/tri_angle/airbnb-scraper", {
                    "locationQueries": [loc], "checkIn": check_in, "checkOut": check_out,
                    "adults": int(ac.get("adults", 2)), "currency": ac.get("currency", "USD")
                }, loc, "en", "hospitality", "forward_booking_window_snapshot")
        if "linkedin" in active_verticals and "linkedin" in vconf:
            lc = vconf["linkedin"]
            for js in lc.get("job_searches") or []:
                add("linkedin_jobs", "apify", "/harvestapi/linkedin-job-search", {
                    "jobTitles": [js["title"]], "locations": [js.get("location", "United States")]
                }, js.get("location", "US"), "en", "job_market", "current_open_roles_snapshot")
            for url in lc.get("company_urls") or []:
                add("linkedin_company", "scrapecreators", "/v1/linkedin/company", {"url": url}, "global", "en", "job_market", "current_company_headcount_snapshot")
            for q in lc.get("post_queries") or []:
                add("linkedin_posts", "scrapecreators", "/v1/linkedin/search/posts", {"query": q, "date_posted": "last-week"}, "global", "en", "job_market", "week_post_filter_current_engagement")
            if lc.get("include_wellfound_trending"):
                add("wellfound_jobs", "wellfound", "/get_trending_jobs", {}, "global", "en", "job_market", "current_trending_jobs_snapshot")
        if "gas" in active_verticals and "gas" in vconf:
            gc = vconf["gas"]
            if gc.get("include_national_average", True):
                add("aaa_gas_national", "aaa-gas-prices", "/get_national_average", {}, "US", "en", "energy", "current_fuel_price_snapshot")
            if gc.get("include_all_states", True):
                add("aaa_gas_states", "aaa-gas-prices", "/get_state_gas_prices", {}, "US", "en", "energy", "current_fuel_price_snapshot")
            if gc.get("include_ev_charging", True):
                add("aaa_ev_charging", "aaa-gas-prices", "/get_ev_charging_prices", {}, "US", "en", "energy", "current_ev_price_snapshot")
            for st in gc.get("states") or []:
                add("aaa_gas_state_change", "aaa-gas-prices", "/get_price_change_by_state", {"state_code": st}, st, "en", "energy", "state_fuel_delta_snapshot")
        if "signals" in active_verticals and "signals" in vconf:
            sc = vconf["signals"]
            if sc.get("include_premarket_movers", True):
                add("premarket_movers", "stockanalysis", "/get_market_movers_premarket", {}, "US", "en", "markets", "premarket_session_snapshot")
            if sc.get("include_insider_ratios", True):
                add("insider_ratios", "secform4", "/get_insider_buy_sell_ratios", {}, "US", "en", "markets", "form4_insider_ratio_snapshot")
            for item in sc.get("short_interest_tickers") or []:
                add("short_interest", "marketbeat", "/get_short_interest", {"ticker": item["ticker"], "exchange": item.get("exchange", "NASDAQ")}, "US", "en", "markets", "short_interest_snapshot")
        if "keepa" in active_verticals and "keepa" in vconf:
            kc = vconf["keepa"]
            add("keepa_deals", "keepa", "/deal", {"selection": {"domainId": int(kc.get("domain_id", 1)), "dateRange": int(kc.get("date_range", 1)), "priceTypes": [0]}}, "US", "en", "ecommerce", "daily_price_drops_snapshot")
        if "carfax" in active_verticals and "carfax" in vconf:
            cc = vconf["carfax"]
            for s in cc.get("searches") or []:
                add("carfax_used", "carfax", "/search_used_car_listings", {"zip": s["zip"], "make": s["make"], "model": s["model"], "rows": int(s.get("rows", 5))}, "US", "en", "automotive", "used_vehicle_inventory_snapshot")
    return {"schema_version": 1, "created_at": iso(now), "window_start": iso(start), "window_end": iso(now), "coverage": config, "jobs": jobs}


def followup_plan(root="data", limit=10, refresh=False):
    if not 1 <= limit <= 100:
        raise ValueError("Detail limit must be between 1 and 100 per platform.")
    now = datetime.now(timezone.utc)
    jobs, seen = [], set()

    def add(source, provider, endpoint, inputs, obs, semantics="current_engagement"):
        identity = (provider, endpoint, json.dumps(inputs, sort_keys=True))
        if identity not in seen:
            seen.add(identity)
            jobs.append({"source": source, "provider": provider, "endpoint": endpoint, "input": inputs,
                         "region": obs.get("requested_region", "unknown"), "language": obs.get("requested_language", "unknown"),
                         "topic": obs.get("topic", "unprompted"), "window_semantics": semantics})

    if refresh:
        counts = {"youtube_detail": 0, "tiktok_detail": 0, "x_detail": 0}
        # Cohort membership comes from persisted plans, not only successful
        # responses: unavailable posts must not silently leave the cohort.
        for path in sorted((Path(root) / "batches").glob("*/manifest.json")):
            manifest = json.loads(path.read_text())
            for entry in manifest["jobs"]:
                spec = entry["spec"]
                source = spec["source"]
                if source not in counts or counts[source] >= limit:
                    continue
                before = len(jobs)
                add(source, spec["provider"], spec["endpoint"], spec["input"],
                    {"requested_region": spec.get("region"), "requested_language": spec.get("language"), "topic": spec.get("topic")})
                if len(jobs) > before:
                    counts[source] += 1
        return {"schema_version": 1, "created_at": now.isoformat().replace("+00:00", "Z"), "jobs": jobs}

    # JSONL uses LF separators. str.splitlines() also splits valid Unicode
    # characters such as U+2028 inside social captions, corrupting records.
    with (Path(root) / "exports/latest/observations.jsonl").open() as stream:
        observations = [json.loads(line) for line in stream if line.strip()]
    for platform in ["youtube", "tiktok", "x"]:
        candidates = [x for x in observations if x["platform"] == platform and x["kind"] in {"post", "video"} and x.get("native_id")]
        # Highest current views; deduplicate by stable native ID before limiting.
        candidates.sort(key=lambda x: x["metrics"].get("views", {}).get("value", 0), reverse=True)
        count = 0
        ids = set()
        for obs in candidates:
            ident = str(obs["native_id"])
            if ident in ids:
                continue
            ids.add(ident)
            if platform == "youtube":
                add("youtube_detail", "scrapecreators", "/v1/youtube/video", {"url": f"https://www.youtube.com/watch?v={ident}"}, obs)
            elif platform == "tiktok":
                if not obs.get("url"):
                    continue
                add("tiktok_detail", "scrapecreators", "/v2/tiktok/video", {"url": obs["url"]}, obs)
            else:
                add("x_detail", "tikhub", "/api/v1/twitter/web/fetch_tweet_detail", {"tweet_id": ident}, obs)
            count += 1
            if count >= limit:
                break
    if not refresh:
        for region in sorted(set(x["requested_region"] for x in observations if x["source"] == "tiktok_hashtags")):
            candidates = [x for x in observations if x["source"] == "tiktok_hashtags" and x["requested_region"] == region]
            candidates.sort(key=lambda x: x.get("rank") or 1000)
            for obs in candidates[:2]:
                add("tiktok_hashtag_detail", "tikhub", "/api/v1/tiktok/ads/get_trends_hashtag_detail", {"hashtag_id": str(obs["native_id"]), "country_code": region, "time_range": 7}, obs, "provider_7_day_detail")
        add("youtube_shorts", "scrapecreators", "/v1/youtube/shorts/trending", {}, {}, "current_ranking_geography_unspecified")
    return {"schema_version": 1, "created_at": now.isoformat().replace("+00:00", "Z"), "jobs": jobs}
