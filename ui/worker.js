/**
 * Cloudflare Worker for NextDay
 * - POST /api/plan-simulator : Calculates Glasser calls & costs for selected sources
 * - POST /api/run-prediction : Runs a next-day forecast across the selected sources
 * - POST /api/validate-forecast : Validates forecast JSON
 */

const ENDPOINT_PRICING = {
  "exa:/search": { display: 0.007, max: 0.022 },
  "serper:/news": { display: 0.001, max: 0.001 },
  "tikhub:/api/v1/twitter/web/fetch_trending": { display: 0.0011, max: 0.0011 },
  "tikhub:/api/v1/twitter/web/fetch_search_timeline": { display: 0.0011, max: 0.0011 },
  "tikhub:/api/v1/tiktok/ads/get_trends_hashtag_list": { display: 0.0011, max: 0.0011 },
  "tikhub:/api/v1/tiktok/web/fetch_trending_searchwords": { display: 0.0011, max: 0.0011 },
  "scrapecreators:/v1/tiktok/get-trending-feed": { display: 0.002, max: 0.002 },
  "scrapecreators:/v1/tiktok/search/keyword": { display: 0.002, max: 0.002 },
  "scrapecreators:/v1/youtube/search": { display: 0.002, max: 0.002 },
  "financialdatasets:/prices": { display: 0.02, max: 0.02 },
  "secapi:/filings/search": { display: 0.0005, max: 0.0005 },
  "zillow:/get_mortgage_rates": { display: 0.055, max: 0.055 },
  "zillow:/search_agents": { display: 0.011, max: 0.011 },
  "brightdata:/datasets/v3/zillow-properties": { display: 0.00165, max: 0.03 },
  "apify:/tri_angle/airbnb-scraper": { display: 0.00165, max: 0.033 },
  "apify:/harvestapi/linkedin-job-search": { display: 0.001, max: 0.011 },
  "scrapecreators:/v1/linkedin/company": { display: 0.00188, max: 0.00188 },
  "wellfound:/get_trending_jobs": { display: 0.011, max: 0.011 },
  "aaa-gas-prices:/get_national_average": { display: 0.022, max: 0.022 },
  "aaa-gas-prices:/get_state_gas_prices": { display: 0.011, max: 0.011 },
  "aaa-gas-prices:/get_price_change_by_state": { display: 0.022, max: 0.022 },
  "aaa-gas-prices:/get_ev_charging_prices": { display: 0.011, max: 0.011 },
  "stockanalysis:/get_market_movers_premarket": { display: 0.011, max: 0.011 },
  "secform4:/get_insider_buy_sell_ratios": { display: 0.011, max: 0.011 },
  "marketbeat:/get_short_interest": { display: 0.011, max: 0.011 },
  "keepa:/deal": { display: 0.0072, max: 0.0072 },
  "carfax:/search_used_car_listings": { display: 0.011, max: 0.011 }
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
  const budget = Number(body.budget_usd || 1.0);
  const regions = Array.isArray(body.regions) ? body.regions : [{ code: "US", x_country: "UnitedStates", language: "en" }];
  const topics = Array.isArray(body.topics) ? body.topics : [{ name: "economy", en: "economy" }];
  const sources = body.enabled_sources || {};
  const verticals = body.verticals || {};
  const nowIso = new Date().toISOString().replace(/\.\d+Z$/, "Z");
  const startIso = new Date(Date.now() - 7 * 86400000).toISOString().replace(/\.\d+Z$/, "Z");

  const jobs = [];
  const seen = new Set();

  function addJob(source, provider, endpoint, input, region) {
    const key = `${provider}:${endpoint}:${JSON.stringify(input)}`;
    if (seen.has(key)) return;
    seen.add(key);
    const p = ENDPOINT_PRICING[`${provider}:${endpoint}`] || { display: 0.002, max: 0.005 };
    jobs.push({ source, provider, endpoint, input, region, display: p.display, max: p.max });
  }

  for (const r of regions) {
    const code = r.code;
    const lang = r.language || "en";
    const country = r.x_country || code;
    if (sources.x_trends) addJob("x_trends", "tikhub", "/api/v1/twitter/web/fetch_trending", { country }, code);
    if (sources.tiktok_trends) addJob("tiktok_trends", "scrapecreators", "/v1/tiktok/get-trending-feed", { region: code }, code);
    if (sources.tiktok_hashtags) addJob("tiktok_hashtags", "tikhub", "/api/v1/tiktok/ads/get_trends_hashtag_list", { country_code: code, time_range: 7 }, code);
    if (sources.exa_regional_news) addJob("news_text", "exa", "/search", { query: `Major news in ${country}`, category: "news", numResults: 10 }, code);

    for (const t of topics) {
      const q = t.en || t.name;
      if (sources.serper_news) addJob("news", "serper", "/news", { q: `${q} when:7d`, gl: code.toLowerCase() }, code);
      if (sources.x_search) addJob("x_search", "tikhub", "/api/v1/twitter/web/fetch_search_timeline", { keyword: `${q} lang:${lang}` }, "global");
      if (sources.youtube_search) addJob("youtube_search", "scrapecreators", "/v1/youtube/search", { query: q, region: code }, code);
      if (sources.tiktok_search) addJob("tiktok_search", "scrapecreators", "/v1/tiktok/search/keyword", { query: q, region: code }, code);
    }
  }

  if (sources.markets) {
    for (const ticker of (body.tickers || ["AAPL", "MSFT", "NVDA", "META"])) {
      addJob("prices", "financialdatasets", "/prices", { ticker, interval: "day" }, "US");
    }
    addJob("filings", "secapi", "/filings/search", { query: "formType:\"8-K\"" }, "US");
  }

  if (verticals.zillow?.enabled) {
    addJob("zillow_mortgage_rates", "zillow", "/get_mortgage_rates", {}, "US");
    for (const loc of (verticals.zillow.locations || ["Austin, TX"])) {
      addJob("zillow_agents", "zillow", "/search_agents", { location: loc }, "US");
    }
    for (const url of (verticals.zillow.property_urls || [])) {
      addJob("zillow_property", "brightdata", "/datasets/v3/zillow-properties", { url }, "US");
    }
  }

  if (verticals.airbnb?.enabled) {
    for (const loc of (verticals.airbnb.locations || ["New York, NY"])) {
      addJob("airbnb_search", "apify", "/tri_angle/airbnb-scraper", { locationQueries: [loc] }, loc);
    }
  }

  if (verticals.linkedin?.enabled) {
    for (const js of (verticals.linkedin.job_searches || [])) {
      addJob("linkedin_jobs", "apify", "/harvestapi/linkedin-job-search", { jobTitles: [js.title], locations: [js.location] }, js.location);
    }
    for (const url of (verticals.linkedin.company_urls || [])) {
      addJob("linkedin_company", "scrapecreators", "/v1/linkedin/company", { url }, "global");
    }
    addJob("wellfound_jobs", "wellfound", "/get_trending_jobs", {}, "global");
  }

  if (verticals.gas?.enabled) {
    addJob("aaa_gas_national", "aaa-gas-prices", "/get_national_average", {}, "US");
    addJob("aaa_gas_states", "aaa-gas-prices", "/get_state_gas_prices", {}, "US");
    addJob("aaa_ev_charging", "aaa-gas-prices", "/get_ev_charging_prices", {}, "US");
    for (const st of (verticals.gas.states || ["CA", "TX"])) {
      addJob("aaa_gas_state_change", "aaa-gas-prices", "/get_price_change_by_state", { state_code: st }, st);
    }
  }

  if (verticals.signals?.enabled) {
    addJob("premarket_movers", "stockanalysis", "/get_market_movers_premarket", {}, "US");
    addJob("insider_ratios", "secform4", "/get_insider_buy_sell_ratios", {}, "US");
    for (const tk of (verticals.signals.tickers || ["NVDA", "TSLA"])) {
      addJob("short_interest", "marketbeat", "/get_short_interest", { ticker: tk, exchange: "NASDAQ" }, "US");
    }
  }

  if (verticals.keepa?.enabled) {
    addJob("keepa_deals", "keepa", "/deal", { selection: { domainId: 1, dateRange: 1, priceTypes: [0] } }, "US");
  }

  if (verticals.carfax?.enabled) {
    for (const s of (verticals.carfax.searches || [{ zip: "94103", make: "Toyota", model: "Camry" }])) {
      addJob("carfax_used", "carfax", "/search_used_car_listings", { zip: s.zip, make: s.make, model: s.model, rows: 5 }, "US");
    }
  }

  const expectedUsd = jobs.reduce((a, j) => a + j.display, 0);
  const reservedUsd = jobs.reduce((a, j) => a + j.max, 0);

  return {
    schema_version: 1,
    created_at: nowIso,
    window_start: startIso,
    window_end: nowIso,
    job_count: jobs.length,
    expected_display_usd: expectedUsd.toFixed(4),
    reserved_max_usd: reservedUsd.toFixed(4),
    budget_usd: budget.toFixed(2),
    within_budget: reservedUsd <= budget,
    jobs: jobs.map(({ display, max, ...rest }) => rest)
  };
}

let CACHED_BUNDLE = null;

async function getBundle(env, requestUrl) {
  if (CACHED_BUNDLE) return CACHED_BUNDLE;
  if (!env.ASSETS) return null;
  try {
    const res = await env.ASSETS.fetch(new URL("/data/bundle.json", requestUrl));
    if (res.ok) {
      CACHED_BUNDLE = await res.json();
      return CACHED_BUNDLE;
    }
  } catch (_) {}
  return null;
}

const LIVE_FORECAST_SCHEMA = {
  type: "object",
  required: ["overview", "forecasts"],
  properties: {
    overview: { type: "string" },
    forecasts: {
      type: "array",
      items: {
        type: "object",
        required: [
          "id",
          "sourceId",
          "sourceLabel",
          "forecast_type",
          "title",
          "claim",
          "probability",
          "outcomes",
          "rationale",
          "resolution"
        ],
        properties: {
          id: { type: "string" },
          sourceId: {
            type: "string",
            enum: ["news", "x", "tiktok", "youtube", "markets", "zillow", "airbnb", "linkedin", "gas", "signals", "keepa", "carfax"]
          },
          sourceLabel: { type: "string" },
          forecast_type: { type: "string" },
          title: { type: "string" },
          claim: { type: "string" },
          probability: { type: "number" },
          estimate: {
            anyOf: [
              { type: "null" },
              {
                type: "object",
                required: ["value", "lower", "upper", "unit"],
                properties: {
                  value: { type: "number" },
                  lower: { type: "number" },
                  upper: { type: "number" },
                  unit: { type: "string" },
                  interval_probability: { type: "number" }
                }
              }
            ]
          },
          outcomes: {
            type: "array",
            items: {
              type: "object",
              required: ["label", "probability"],
              properties: {
                label: { type: "string" },
                probability: { type: "number" }
              }
            }
          },
          rationale: { type: "string" },
          resolution: {
            type: "object",
            required: ["mode", "rule"],
            properties: {
              mode: { type: "string" },
              rule: { type: "string" }
            }
          }
        }
      }
    }
  }
};

async function generatePredictionRun(body, env, requestUrl) {
  const t0 = Date.now();
  const rawSources = Array.isArray(body.selected_sources) && body.selected_sources.length > 0
    ? body.selected_sources
    : ["news", "markets", "zillow", "gas"];
  const selected = new Set(rawSources);
  const fields = body.field_values || {};
  const userPrompt = (body.prompt || "").trim();
  const model = "gemini-4-argon";
  const now = new Date();
  const runId = `run-${now.toISOString().slice(11, 19).replace(/:/g, "")}`;

  if (!env.GEMINI_API_KEY) {
    throw new Error("GEMINI_API_KEY secret is not configured on the Worker backend.");
  }

  const bundle = await getBundle(env, requestUrl);
  const vc = bundle?.prospective?.vertical_cache || {};
  const pilotEvidence = bundle?.prospective?.argon_pilot?.evidence || [];

  // Build compact cached Glasser evidence payload for selected sources
  const cachedEvidence = {};
  if (selected.has("news")) {
    cachedEvidence.news = pilotEvidence
      .filter(e => e.platform === "web" || e.kind === "news_article")
      .slice(0, 10)
      .map(e => ({ title: e.title, region: e.requested_region, topic: e.topic, published_at: e.published_at, snippet: (e.text || "").slice(0, 260) }));
  }
  if (selected.has("x") || selected.has("tiktok") || selected.has("youtube")) {
    cachedEvidence.social = pilotEvidence
      .filter(e => ["x", "tiktok", "youtube"].includes(e.platform))
      .slice(0, 12)
      .map(e => ({ platform: e.platform, title: e.title || (e.text || "").slice(0, 140), metrics: e.metrics, changes: e.engagement_changes }));
  }
  if (selected.has("markets")) {
    const latestCase = (bundle?.benchmark?.cases || []).slice(-1)[0] || {};
    cachedEvidence.markets = {
      tracked_tickers: fields.tickers || "AAPL, MSFT, NVDA, AMZN, GOOGL, META, TSLA, XOM",
      recent_filing_counts: latestCase.filing_counts || [],
      sample_market_evidence: (latestCase.sample_evidence || []).filter(e => e.kind === "equity_price" || e.kind === "sec_filing").slice(0, 8)
    };
  }
  if (selected.has("gas") || userPrompt.toLowerCase().includes("gas") || userPrompt.toLowerCase().includes("fuel") || userPrompt.toLowerCase().includes("ev")) {
    cachedEvidence.aaa_gas_and_ev = {
      national_average: vc.aaa_gas_national,
      state_averages_sample: (vc.aaa_gas_states || []).slice(0, 12),
      ev_charging_sample: (vc.aaa_ev_charging || []).slice(0, 10),
      requested_states: fields.gas_states || "CA, TX, NY, FL"
    };
  }
  if (selected.has("zillow") || selected.has("airbnb") || /rent|zillow|house|housing|mortgage|real estate|airbnb|hotel/.test(userPrompt.toLowerCase())) {
    cachedEvidence.real_estate_and_rentals = {
      zillow_mortgage_rates: vc.zillow_mortgage,
      rentcast_us_market_stats: vc.rentcast_market,
      requested_zillow_cities: fields.zillow_locs || "Austin, TX; Miami, FL",
      requested_airbnb_cities: fields.airbnb_locs || "New York, NY; San Francisco, CA"
    };
  }
  if (selected.has("linkedin") || /job|hiring|linkedin|layoff|salary|engineer/.test(userPrompt.toLowerCase())) {
    cachedEvidence.job_market = {
      wellfound_trending_startup_jobs: vc.wellfound_jobs,
      requested_linkedin_queries: fields.linkedin_jobs || "AI Engineer @ San Francisco; Software Engineer @ New York",
      requested_companies: fields.linkedin_cos || "openai, anthropic, shopify"
    };
  }
  if (selected.has("signals") || /insider|form 4|premarket|pre-market|short/.test(userPrompt.toLowerCase())) {
    cachedEvidence.market_signals = {
      secform4_insider_buy_sell: vc.insider_ratios,
      stockanalysis_premarket_movers: vc.premarket_movers,
      requested_tickers: fields.signal_tickers || "NVDA, TSLA"
    };
  }
  if (selected.has("keepa") || /amazon|keepa|deal|ecommerce|price drop/.test(userPrompt.toLowerCase())) {
    cachedEvidence.keepa_amazon_deals = vc.keepa_deals;
  }
  if (selected.has("carfax") || /car|auto|used car|camry|tesla|vehicle/.test(userPrompt.toLowerCase())) {
    cachedEvidence.carfax_used_autos = {
      sample_listings: vc.carfax_used,
      requested_models: fields.carfax_models || "Toyota Camry · Tesla Model 3"
    };
  }

  const systemText = [
    "You are Hunch, a rigorous probabilistic next-day forecasting engine powered by gemini-4-argon.",
    "You are given cached Glasser multi-source evidence snapshots captured on 2026-10-25 UTC and user configuration.",
    "Generate between 4 and 6 concrete, quantitatively resolvable next-day (24-hour horizon: 2026-10-26 UTC) forecasts.",
    userPrompt
      ? `CRITICAL USER GUIDANCE PROMPT: "${userPrompt}". Your FIRST forecast in the array MUST directly and deeply address this user prompt (set its sourceLabel to "Guided Focus · " + the relevant source name, and ground its numbers in the supplied Glasser data and domain baselines). Then generate 3 to 5 additional forecasts covering the user's selected sources.`
      : "Generate 5 diverse, specific next-day forecasts across the user's selected data sources.",
    "For each forecast:",
    "- Cite specific numbers, prices, rates, tickers, or counts from the supplied cached Glasser evidence in `rationale`.",
    "- `probability` must be a calibrated float between 0.05 and 0.95.",
    "- `outcomes` must contain 2 or 3 mutually exclusive, exhaustive scenarios whose probabilities sum to 1.0.",
    "- Provide a numeric `estimate` (value, lower, upper, unit, interval_probability: 0.8) whenever a quantitative metric is forecast."
  ].join("\n");

  const userPayload = {
    current_cutoff_utc: "2026-10-25T20:00:00Z",
    target_window_utc: "2026-10-26T00:00:00Z to 2026-10-27T00:00:00Z",
    user_guidance_prompt: userPrompt || null,
    selected_sources: Array.from(selected),
    regions: body.regions || ["US", "GB", "IN", "JP"],
    field_values: fields,
    cached_glasser_evidence: cachedEvidence
  };

  const geminiPayload = {
    systemInstruction: { parts: [{ text: systemText }] },
    contents: [{ role: "user", parts: [{ text: JSON.stringify(userPayload) }] }],
    generationConfig: {
      maxOutputTokens: 4096,
      thinkingConfig: { thinkingLevel: "low" },
      responseMimeType: "application/json",
      responseJsonSchema: LIVE_FORECAST_SCHEMA
    }
  };

  const geminiRes = await fetch(
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-4-argon:generateContent",
    {
      method: "POST",
      headers: {
        "x-goog-api-key": env.GEMINI_API_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json"
      },
      body: JSON.stringify(geminiPayload)
    }
  );

  if (!geminiRes.ok) {
    let errCode = `HTTP ${geminiRes.status}`;
    try {
      const errJson = await geminiRes.json();
      errCode = errJson?.error?.status || errJson?.error?.message || errCode;
    } catch (_) {}
    throw new Error(`gemini-4-argon API error (${errCode})`);
  }

  const rawResp = await geminiRes.json();
  const candidate = (rawResp.candidates || [])[0];
  if (!candidate) {
    throw new Error("gemini-4-argon returned no candidate.");
  }
  const rawText = (candidate.content?.parts || [])
    .filter(p => !p.thought)
    .map(p => p.text || "")
    .join("");

  const parsed = JSON.parse(rawText);
  const latencyMs = Date.now() - t0;

  const forecasts = (parsed.forecasts || []).map((f, idx) => {
    const p = Math.max(0.01, Math.min(0.99, Number(f.probability) || 0.7));
    return {
      ...f,
      id: `${runId}-${idx + 1}`,
      probability: p
    };
  });

  return {
    run_id: runId,
    label: `Run ${now.toISOString().slice(11, 16)} UTC`,
    prompt: userPrompt || null,
    overview: parsed.overview || null,
    created_at: now.toISOString(),
    target_date: "2026-10-26",
    is_live: true,
    live_llm: true,
    model: rawResp.modelVersion || model,
    latency_ms: latencyMs,
    usage: rawResp.usageMetadata || null,
    selected_sources: Array.from(selected),
    forecasts
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
        service: "nextday-prediction",
        model: "gemini-4-argon",
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

    if (url.pathname === "/api/run-prediction" && request.method === "POST") {
      try {
        const body = await request.json();
        const result = await generatePredictionRun(body, env, request.url);
        return jsonResponse(result);
      } catch (err) {
        return jsonResponse({ error: String(err.message || err) }, 400);
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
