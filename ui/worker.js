/**
 * Cloudflare Worker for NEXTDAY // Temporal Evidence & Forecasting Observatory
 * Serves the static observatory assets + interactive Edge APIs for:
 *  - Ingestion plan generation & Glasser reservation simulation (/api/plan-simulator)
 *  - Forecast contract & mathematical consistency validation (/api/validate-forecast)
 *  - Multi-model objective Brier/MAE scoring & blinded judge prompt builder (/api/score-submission)
 */

const ENDPOINT_PRICING = {
  "exa:/search": { display: 0.007, max: 0.022, provider: "exa", endpoint: "/search" },
  "serper:/news": { display: 0.001, max: 0.001, provider: "serper", endpoint: "/news" },
  "tikhub:/api/v1/twitter/web/fetch_trending": { display: 0.0011, max: 0.0011, provider: "tikhub", endpoint: "/api/v1/twitter/web/fetch_trending" },
  "tikhub:/api/v1/twitter/web/fetch_search_timeline": { display: 0.0011, max: 0.0011, provider: "tikhub", endpoint: "/api/v1/twitter/web/fetch_search_timeline" },
  "tikhub:/api/v1/twitter/web/fetch_tweet_detail": { display: 0.0011, max: 0.0011, provider: "tikhub", endpoint: "/api/v1/twitter/web/fetch_tweet_detail" },
  "tikhub:/api/v1/youtube/web/get_trending_videos": { display: 0.0011, max: 0.0011, provider: "tikhub", endpoint: "/api/v1/youtube/web/get_trending_videos" },
  "tikhub:/api/v1/tiktok/ads/get_trends_hashtag_list": { display: 0.0011, max: 0.0011, provider: "tikhub", endpoint: "/api/v1/tiktok/ads/get_trends_hashtag_list" },
  "tikhub:/api/v1/tiktok/ads/get_trends_hashtag_detail": { display: 0.0011, max: 0.0011, provider: "tikhub", endpoint: "/api/v1/tiktok/ads/get_trends_hashtag_detail" },
  "tikhub:/api/v1/tiktok/web/fetch_trending_searchwords": { display: 0.0011, max: 0.0011, provider: "tikhub", endpoint: "/api/v1/tiktok/web/fetch_trending_searchwords" },
  "scrapecreators:/v1/tiktok/get-trending-feed": { display: 0.002, max: 0.002, provider: "scrapecreators", endpoint: "/v1/tiktok/get-trending-feed" },
  "scrapecreators:/v1/tiktok/search/keyword": { display: 0.002, max: 0.002, provider: "scrapecreators", endpoint: "/v1/tiktok/search/keyword" },
  "scrapecreators:/v2/tiktok/video": { display: 0.002, max: 0.002, provider: "scrapecreators", endpoint: "/v2/tiktok/video" },
  "scrapecreators:/v3/tiktok/profile/videos": { display: 0.002, max: 0.002, provider: "scrapecreators", endpoint: "/v3/tiktok/profile/videos" },
  "scrapecreators:/v1/youtube/search": { display: 0.002, max: 0.002, provider: "scrapecreators", endpoint: "/v1/youtube/search" },
  "scrapecreators:/v1/youtube/video": { display: 0.002, max: 0.002, provider: "scrapecreators", endpoint: "/v1/youtube/video" },
  "scrapecreators:/v1/youtube/shorts/trending": { display: 0.002, max: 0.002, provider: "scrapecreators", endpoint: "/v1/youtube/shorts/trending" },
  "scrapecreators:/v1/youtube/channel-videos": { display: 0.002, max: 0.002, provider: "scrapecreators", endpoint: "/v1/youtube/channel-videos" },
  "financialdatasets:/prices": { display: 0.02, max: 0.02, provider: "financialdatasets", endpoint: "/prices" },
  "financialdatasets:/company/facts": { display: 0.02, max: 0.02, provider: "financialdatasets", endpoint: "/company/facts" },
  "secapi:/edgar-index/ingestion-log/{date}": { display: 0.0005, max: 0.0005, provider: "secapi", endpoint: "/edgar-index/ingestion-log/{date}" },
  "secapi:/filings/search": { display: 0.0005, max: 0.0005, provider: "secapi", endpoint: "/filings/search" },
  "secapi:/filing-document": { display: 0.0005, max: 0.0005, provider: "secapi", endpoint: "/filing-document" },
  "nasdaq:/get_earnings_calendar": { display: 0.011, max: 0.011, provider: "nasdaq", endpoint: "/get_earnings_calendar" },
  "zillow:/get_mortgage_rates": { display: 0.055, max: 0.055, provider: "zillow", endpoint: "/get_mortgage_rates" },
  "zillow:/search_agents": { display: 0.011, max: 0.011, provider: "zillow", endpoint: "/search_agents" },
  "zillow:/get_open_houses": { display: 0.033, max: 0.033, provider: "zillow", endpoint: "/get_open_houses" },
  "brightdata:/datasets/v3/zillow-properties": { display: 0.00165, max: 0.03, provider: "brightdata", endpoint: "/datasets/v3/zillow-properties" },
  "apify:/tri_angle/airbnb-scraper": { display: 0.00165, max: 0.033, provider: "apify", endpoint: "/tri_angle/airbnb-scraper" },
  "apify:/harvestapi/linkedin-job-search": { display: 0.001, max: 0.011, provider: "apify", endpoint: "/harvestapi/linkedin-job-search" },
  "apify:/harvestapi/linkedin-post-search": { display: 0.018, max: 0.18, provider: "apify", endpoint: "/harvestapi/linkedin-post-search" },
  "scrapecreators:/v1/linkedin/company": { display: 0.00188, max: 0.00188, provider: "scrapecreators", endpoint: "/v1/linkedin/company" },
  "scrapecreators:/v1/linkedin/search/posts": { display: 0.00188, max: 0.00188, provider: "scrapecreators", endpoint: "/v1/linkedin/search/posts" },
  "theirstack:/v1/jobs/search": { display: 0.035934, max: 1.25, provider: "theirstack", endpoint: "/v1/jobs/search" },
  "wellfound:/get_trending_jobs": { display: 0.011, max: 0.011, provider: "wellfound", endpoint: "/get_trending_jobs" }
};

function jsonResponse(data, status = 200) {
  return new Response(JSON.stringify(data, null, 2), {
    status,
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type"
    }
  });
}

function simulatePlan(body) {
  const mode = body.mode || "prospective";
  const budget = Number(body.budget_usd || (mode === "prospective" ? 1.0 : 10.0));
  const regions = Array.isArray(body.regions) ? body.regions : [];
  const topics = Array.isArray(body.topics) ? body.topics : [];
  const sources = body.enabled_sources || {};
  const nowIso = body.window_end || new Date().toISOString().replace(/\.\d+Z$/, "Z");
  const startDt = new Date(new Date(nowIso).getTime() - (Number(body.lookback_days || 7) * 86400000));
  const startIso = startDt.toISOString().replace(/\.\d+Z$/, "Z");

  const jobs = [];
  const seen = new Set();

  function addJob(source, provider, endpoint, input, region, language, topic, windowSemantics) {
    const key = `${provider}:${endpoint}:${JSON.stringify(input)}`;
    if (seen.has(key)) return;
    seen.add(key);
    const priceInfo = ENDPOINT_PRICING[`${provider}:${endpoint}`] || { display: 0.002, max: 0.005 };
    jobs.push({
      source,
      provider,
      endpoint,
      input,
      region,
      language,
      topic,
      window_semantics: windowSemantics,
      estimated_display_usd: priceInfo.display,
      reserved_max_usd: priceInfo.max
    });
  }

  if (mode === "prospective") {
    for (const r of regions) {
      const code = r.code;
      const lang = r.language || "en";
      const country = r.x_country || code;

      if (sources.x_trends !== false) {
        addJob("x_trends", "tikhub", "/api/v1/twitter/web/fetch_trending", { country }, code, lang, "unprompted", "current_ranking");
      }
      if (sources.youtube_trends) {
        addJob("youtube_trends", "tikhub", "/api/v1/youtube/web/get_trending_videos", { country_code: code.toLowerCase(), language_code: lang }, code, lang, "unprompted", "current_ranking");
      }
      if (sources.tiktok_trends !== false) {
        addJob("tiktok_trends", "scrapecreators", "/v1/tiktok/get-trending-feed", { region: code }, code, lang, "unprompted", "current_feed");
      }
      if (sources.tiktok_hashtags !== false) {
        addJob("tiktok_hashtags", "tikhub", "/api/v1/tiktok/ads/get_trends_hashtag_list", { country_code: code, time_range: 7, limit: 20, page: 1 }, code, lang, "unprompted", "provider_7_day_aggregate");
      }
      for (const t of topics) {
        const query = t[lang] || t.en || t.name;
        if (sources.serper_news !== false) {
          addJob("news", "serper", "/news", { q: `${query} when:7d`, gl: code.toLowerCase(), hl: lang }, code, lang, t.name, "query_hint_7_days_unverified");
        }
        if (sources.x_search !== false) {
          addJob("x_search", "tikhub", "/api/v1/twitter/web/fetch_search_timeline", {
            keyword: `${query} lang:${lang} since:${startIso.slice(0, 10)} until:${nowIso.slice(0, 10)}`,
            search_type: "Top"
          }, "not_filtered", lang, t.name, "date_filtered_posts_current_engagement");
        }
        if (sources.youtube_search !== false) {
          addJob("youtube_search", "scrapecreators", "/v1/youtube/search", { query, region: code, sortBy: "popular", uploadDate: "this_week", type: "videos" }, code, lang, t.name, "week_upload_filter_current_engagement");
        }
        if (sources.tiktok_search !== false) {
          addJob("tiktok_search", "scrapecreators", "/v1/tiktok/search/keyword", { query, region: code, sort_by: "most-liked", date_posted: "this-week" }, code, lang, t.name, "week_post_filter_current_engagement");
        }
        if (sources.exa_topic_news) {
          addJob("news_text", "exa", "/search", {
            query: `Recent reporting about ${query} in ${country}`,
            category: "news",
            numResults: 10,
            startPublishedDate: startIso,
            endPublishedDate: nowIso,
            contents: { text: { maxCharacters: 8000 } }
          }, code, lang, t.name, "publication_date_filter_current_text");
        }
      }
      if (sources.exa_regional_news !== false) {
        addJob("news_text", "exa", "/search", {
          query: `Major news developments in ${country} during the past week`,
          category: "news",
          numResults: 10,
          startPublishedDate: startIso,
          endPublishedDate: nowIso,
          contents: { text: { maxCharacters: 8000 } }
        }, code, lang, "general", "publication_date_filter_current_text");
      }
    }
    if (sources.tiktok_search_trends !== false) {
      addJob("tiktok_search_trends", "tikhub", "/api/v1/tiktok/web/fetch_trending_searchwords", {}, "unknown", "unknown", "unprompted", "provider_daily_search_trends");
    }
    const verticals = body.verticals || {};
    if (verticals.zillow && verticals.zillow.enabled) {
      if (verticals.zillow.include_mortgage_rates !== false) {
        addJob("zillow_mortgage_rates", "zillow", "/get_mortgage_rates", {}, "US", "en", "real_estate", "current_rate_snapshot");
      }
      for (const loc of (verticals.zillow.locations || [])) {
        addJob("zillow_agents", "zillow", "/search_agents", { location: loc }, "US", "en", "real_estate", "current_directory_snapshot");
      }
      for (const url of (verticals.zillow.property_urls || [])) {
        addJob("zillow_property", "brightdata", "/datasets/v3/zillow-properties", { url }, "US", "en", "real_estate", "current_listing_snapshot");
      }
      for (const zpid of (verticals.zillow.open_house_zpids || [])) {
        addJob("zillow_open_houses", "zillow", "/get_open_houses", { zpid: String(zpid) }, "US", "en", "real_estate", "current_listing_snapshot");
      }
    }
    if (verticals.airbnb && verticals.airbnb.enabled) {
      const checkIn = verticals.airbnb.check_in || "2026-11-08";
      const checkOut = verticals.airbnb.check_out || "2026-11-11";
      for (const loc of (verticals.airbnb.locations || [])) {
        addJob("airbnb_search", "apify", "/tri_angle/airbnb-scraper", {
          locationQueries: [loc],
          checkIn,
          checkOut,
          adults: Number(verticals.airbnb.adults || 2),
          currency: verticals.airbnb.currency || "USD"
        }, loc, "en", "hospitality", "forward_booking_window_snapshot");
      }
    }
    if (verticals.linkedin && verticals.linkedin.enabled) {
      for (const js of (verticals.linkedin.job_searches || [])) {
        addJob("linkedin_jobs", "apify", "/harvestapi/linkedin-job-search", {
          jobTitles: [js.title],
          locations: [js.location || "United States"]
        }, js.location || "US", "en", "job_market", "current_open_roles_snapshot");
      }
      for (const url of (verticals.linkedin.company_urls || [])) {
        addJob("linkedin_company", "scrapecreators", "/v1/linkedin/company", { url }, "global", "en", "job_market", "current_company_headcount_snapshot");
      }
      for (const q of (verticals.linkedin.post_queries || [])) {
        addJob("linkedin_posts", "scrapecreators", "/v1/linkedin/search/posts", { query: q, date_posted: "last-week" }, "global", "en", "job_market", "week_post_filter_current_engagement");
      }
      if (verticals.linkedin.include_wellfound_trending) {
        addJob("wellfound_jobs", "wellfound", "/get_trending_jobs", {}, "global", "en", "job_market", "current_trending_jobs_snapshot");
      }
    }
  } else {
    const days = Number(body.collection_days || 17);
    const tickers = Array.isArray(body.tickers) ? body.tickers : ["AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "JPM", "XOM", "WMT", "NFLX"];
    const xAccounts = Array.isArray(body.x_accounts) ? body.x_accounts : ["NASA", "WHO", "BBCWorld"];
    const tiktokAccounts = Array.isArray(body.tiktok_accounts) ? body.tiktok_accounts : ["bbcnews", "dwnews"];
    const youtubeAccounts = Array.isArray(body.youtube_accounts) ? body.youtube_accounts : ["NASA", "BBCNews"];
    for (const ticker of tickers) {
      addJob("benchmark_prices", "financialdatasets", "/prices", { ticker, interval: "day", start_date: "2026-10-08", end_date: "2026-10-24" }, "US", "en", ticker, "historical_ohlcv");
      addJob("benchmark_company", "financialdatasets", "/company/facts", { ticker }, "US", "en", ticker, "cik_mapping");
    }
    for (let d = 0; d < days; d++) {
      const dayLabel = `day-${d + 1}`;
      addJob("benchmark_filings", "secapi", "/edgar-index/ingestion-log/{date}", { date: dayLabel }, "US", "en", "edgar", "registry_log");
      for (const acc of xAccounts) {
        addJob("benchmark_x", "tikhub", "/api/v1/twitter/web/fetch_search_timeline", { keyword: `from:${acc} -is:retweet -is:reply`, day: dayLabel }, "global", "en", acc, "buffered_utc_search");
      }
      for (const t of topics) {
        addJob("benchmark_news", "exa", "/search", { query: t.en || t.name, day: dayLabel, category: "news", numResults: 10 }, "global", "en", t.name, "publication_date_filter_current_text");
      }
    }
    for (const acc of tiktokAccounts) {
      addJob("benchmark_tiktok", "scrapecreators", "/v3/tiktok/profile/videos", { handle: acc, sort_by: "latest" }, "global", "en", acc, "profile_publication_record");
    }
    for (const acc of youtubeAccounts) {
      addJob("benchmark_youtube", "scrapecreators", "/v1/youtube/channel-videos", { handle: acc, sort: "latest" }, "global", "en", acc, "channel_publication_record");
    }
  }

  const expectedUsd = jobs.reduce((acc, j) => acc + j.estimated_display_usd, 0);
  const reservedUsd = jobs.reduce((acc, j) => acc + j.reserved_max_usd, 0);

  return {
    schema_version: 1,
    mode,
    created_at: nowIso,
    window_start: startIso,
    window_end: nowIso,
    job_count: jobs.length,
    expected_display_usd: expectedUsd.toFixed(5),
    reserved_max_usd: reservedUsd.toFixed(5),
    budget_usd: budget.toFixed(2),
    within_budget: reservedUsd <= budget,
    jobs: jobs.map(({ estimated_display_usd, reserved_max_usd, ...rest }) => rest)
  };
}

function validateForecastPayload(payload) {
  const errors = [];
  const warnings = [];
  if (!payload || typeof payload !== "object") {
    return { valid: false, errors: ["Payload must be a JSON object."], warnings: [] };
  }
  const result = payload.result || payload;
  if (typeof result.overview !== "string" || !result.overview.trim()) {
    errors.push("Missing top-level 'overview' string.");
  }
  if (!Array.isArray(result.limitations)) {
    errors.push("Missing top-level 'limitations' array.");
  }
  if (!Array.isArray(result.forecasts) || result.forecasts.length === 0) {
    errors.push("'forecasts' must be a non-empty array.");
    return { valid: false, errors, warnings };
  }

  const ids = new Set();
  for (const [idx, fc] of result.forecasts.entries()) {
    const label = fc.id || `forecasts[${idx}]`;
    if (ids.has(fc.id)) errors.push(`Duplicate forecast id '${fc.id}'.`);
    ids.add(fc.id);

    if (!["forecast", "abstain"].includes(fc.status)) {
      errors.push(`${label}: status must be 'forecast' or 'abstain'.`);
    }
    if (fc.status === "forecast" && (!Array.isArray(fc.evidence_ids) || fc.evidence_ids.length === 0)) {
      errors.push(`${label}: non-abstaining forecast requires at least one evidence_id.`);
    }
    if (fc.status === "abstain" && (fc.probability !== null || fc.estimate !== null || (fc.outcomes && fc.outcomes.length > 0))) {
      errors.push(`${label}: abstaining forecast must have null probability/estimate and empty outcomes.`);
    }
    if (fc.probability !== null && fc.probability !== undefined) {
      if (typeof fc.probability !== "number" || !Number.isFinite(fc.probability) || fc.probability < 0 || fc.probability > 1) {
        errors.push(`${label}: probability must be a finite number in [0, 1] or null.`);
      }
    }
    if (Array.isArray(fc.outcomes) && fc.outcomes.length > 0) {
      const sum = fc.outcomes.reduce((acc, o) => acc + Number(o.probability || 0), 0);
      if (Math.abs(sum - 1) > 0.001) {
        errors.push(`${label}: categorical outcomes probabilities sum to ${sum.toFixed(4)} (must sum to 1.0 ± 0.001).`);
      }
      const outcomeLabels = fc.outcomes.map(o => o.label);
      if (new Set(outcomeLabels).size !== outcomeLabels.length) {
        errors.push(`${label}: duplicate categorical outcome labels.`);
      }
    }
    if (fc.estimate !== null && fc.estimate !== undefined) {
      const { value, lower, upper, interval_probability } = fc.estimate;
      if ((lower === null) !== (upper === null)) {
        errors.push(`${label}: prediction interval requires both lower and upper endpoints.`);
      }
      if (lower !== null && (value < lower || value > upper)) {
        errors.push(`${label}: point estimate (${value}) lies outside interval [${lower}, ${upper}].`);
      }
      if (lower !== null && (interval_probability === null || interval_probability === undefined)) {
        errors.push(`${label}: prediction interval requires interval_probability.`);
      }
    }
    if (!fc.resolution || !["measurable", "exploratory", "unresolvable"].includes(fc.resolution.mode)) {
      errors.push(`${label}: resolution.mode must be measurable, exploratory, or unresolvable.`);
    }
    if (fc.claim && /\b(and|or|nor)\b/i.test(fc.claim) && fc.claim.length > 180) {
      warnings.push(`${label}: long claim contains conjunctions; verify atomic claim decomposition before scoring.`);
    }
  }

  return {
    valid: errors.length === 0,
    forecast_count: result.forecasts.length,
    errors,
    warnings
  };
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (request.method === "OPTIONS") {
      return jsonResponse({ ok: true });
    }

    if (url.pathname === "/api/health") {
      return jsonResponse({
        status: "ok",
        service: "nextday-prediction-observatory",
        model: "gemini-4-argon",
        edge_colo: request.cf ? request.cf.colo : "local",
        timestamp: new Date().toISOString()
      });
    }

    if (url.pathname === "/api/plan-simulator" && request.method === "POST") {
      try {
        const body = await request.json();
        return jsonResponse(simulatePlan(body));
      } catch (err) {
        return jsonResponse({ error: String(err.message || err) }, 400);
      }
    }

    if (url.pathname === "/api/validate-forecast" && request.method === "POST") {
      try {
        const body = await request.json();
        return jsonResponse(validateForecastPayload(body));
      } catch (err) {
        return jsonResponse({ valid: false, errors: [String(err.message || err)], warnings: [] }, 400);
      }
    }

    if (env.ASSETS) {
      const res = await env.ASSETS.fetch(request);
      if (res.status !== 404) return res;
      return env.ASSETS.fetch(new URL("/index.html", request.url));
    }

    return new Response("Not Found", { status: 404 });
  }
};
