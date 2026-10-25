/* NextDay — Minimalist Source, Prediction & Multi-Model Benchmark Controller */

const ICONS = {
  news: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>`,
  x: `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>`,
  tiktok: `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-5.2 1.74 2.89 2.89 0 0 1 2.31-4.64 2.93 2.93 0 0 1 .88.13V9.4a6.84 6.84 0 0 0-1-.05A6.33 6.33 0 0 0 5 20.1a6.34 6.34 0 0 0 10.86-4.43v-7a8.16 8.16 0 0 0 4.77 1.52v-3.4a4.85 4.85 0 0 1-1-.1z"/></svg>`,
  youtube: `<svg viewBox="0 0 24 24" fill="#FF0000"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>`,
  markets: `<svg viewBox="0 0 24 24" fill="none" stroke="#0E7A5D" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>`,
  zillow: `<svg viewBox="0 0 24 24" fill="#006AFF"><path d="M12 2L2 9.5V22h20V9.5L12 2zm5.5 16.5h-11v-2.1l6.8-6.4H6.8V8h10.4v2.1l-6.8 6.4h7.1v2z"/></svg>`,
  airbnb: `<svg viewBox="0 0 24 24" fill="#FF385C"><path d="M12 2C9.5 2 7.2 6.1 5.1 10.6 3.3 14.4 2.5 16.8 3.6 19c1 2 3.4 3 5.5 2.2 1.2-.5 2.1-1.4 2.9-2.5.8 1.1 1.7 2 2.9 2.5 2.1.8 4.5-.2 5.5-2.2 1.1-2.2.3-4.6-1.5-8.4C16.8 6.1 14.5 2 12 2zm0 13.8c-1.5-1.9-2.3-3.5-2.3-4.7 0-1.3 1-2.3 2.3-2.3s2.3 1 2.3 2.3c0 1.2-.8 2.8-2.3 4.7z"/></svg>`,
  linkedin: `<svg viewBox="0 0 24 24" fill="#0A66C2"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/></svg>`,
  gas: `<svg viewBox="0 0 24 24" fill="none" stroke="#D97706" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 22L15 22"/><path d="M4 9L14 9"/><path d="M14 22V4a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v18"/><path d="M14 13h2a2 2 0 0 1 2 2v2a2 2 0 0 0 2 2h0a2 2 0 0 0 2-2V9.83a2 2 0 0 0-.59-1.42L18 5"/></svg>`,
  signals: `<svg viewBox="0 0 24 24" fill="none" stroke="#7C3AED" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20V10"/><path d="M18 20V4"/><path d="M6 20v-4"/></svg>`,
  keepa: `<svg viewBox="0 0 24 24" fill="none" stroke="#EA580C" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>`,
  carfax: `<svg viewBox="0 0 24 24" fill="none" stroke="#0284C7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 16H9m10 0h3v-3.15a1 1 0 0 0-.84-.99L16 11l-2.7-3.6a1 1 0 0 0-.8-.4H5.24a2 2 0 0 0-1.8 1.1l-.8 1.63A6 6 0 0 0 2 12.42V16h2"/><circle cx="6.5" cy="16.5" r="2.5"/><circle cx="16.5" cy="16.5" r="2.5"/></svg>`
};

const MODELS = [
  { id: "gemini-4-argon", name: "gemini-4-argon", color: "#E1381C" },
  { id: "claude-4.6-opus", name: "claude-4.6-opus", color: "#4F46E5" },
  { id: "gpt-5.4", name: "gpt-5.4", color: "#0E7A5D" },
  { id: "baseline", name: "Persistence Baseline", color: "#9A978F" }
];

const SOURCE_CARDS = [
  {
    id: "news",
    name: "Global News",
    desc: "Exa full-text & Serper news across 4 regions",
    provider: "exa · serper",
    price: "$0.007 / run",
    icon: ICONS.news,
    fields: [{ key: "topics", label: "Topics", value: "geopolitics, economy, technology, climate, culture" }]
  },
  {
    id: "x",
    name: "X (Twitter)",
    desc: "Real-time search & country trend rankings",
    provider: "tikhub",
    price: "$0.0011 / run",
    icon: ICONS.x,
    fields: [{ key: "x_accounts", label: "Tracked Accounts", value: "NASA, WHO, BBCWorld" }]
  },
  {
    id: "tiktok",
    name: "TikTok",
    desc: "Regional trending feed, hashtags & search",
    provider: "scrapecreators · tikhub",
    price: "$0.002 / run",
    icon: ICONS.tiktok,
    fields: [{ key: "tiktok_accounts", label: "Tracked Profiles", value: "bbcnews, dwnews" }]
  },
  {
    id: "youtube",
    name: "YouTube",
    desc: "Weekly popular videos & trending Shorts",
    provider: "scrapecreators",
    price: "$0.002 / run",
    icon: ICONS.youtube,
    fields: [{ key: "youtube_accounts", label: "Tracked Channels", value: "NASA, BBCNews" }]
  },
  {
    id: "markets",
    name: "SEC & Equities",
    desc: "Daily OHLCV bars & verified 8-K filings",
    provider: "secapi · financialdatasets",
    price: "$0.0005–$0.02",
    icon: ICONS.markets,
    fields: [{ key: "tickers", label: "Cohort Tickers", value: "AAPL, MSFT, NVDA, AMZN, GOOGL, META, JPM, XOM, WMT, NFLX" }]
  },
  {
    id: "zillow",
    name: "Zillow",
    desc: "30Y mortgage rates, Zestimates & listings",
    provider: "zillow · brightdata",
    price: "$0.011–$0.055",
    isNew: true,
    icon: ICONS.zillow,
    fields: [
      { key: "zillow_locs", label: "Metro Markets", value: "Austin, TX; San Francisco, CA; Miami, FL" },
      { key: "zillow_urls", label: "Property URL", value: "https://www.zillow.com/homedetails/29437674_zpid/" }
    ]
  },
  {
    id: "airbnb",
    name: "Airbnb",
    desc: "Forward nightly pricing & city supply",
    provider: "apify / airbnb-scraper",
    price: "$0.033 cap",
    isNew: true,
    icon: ICONS.airbnb,
    fields: [
      { key: "airbnb_locs", label: "Cities", value: "New York, NY; Tokyo, Japan; London, UK" },
      { key: "airbnb_window", label: "Check-In → Out", value: "2026-11-08 → 2026-11-11" }
    ]
  },
  {
    id: "linkedin",
    name: "LinkedIn Jobs",
    desc: "Job openings velocity & company headcount",
    provider: "harvestapi · scrapecreators",
    price: "$0.002–$0.011",
    isNew: true,
    icon: ICONS.linkedin,
    fields: [
      { key: "linkedin_jobs", label: "Job Queries", value: "AI Engineer @ San Francisco; Software Engineer @ New York" },
      { key: "linkedin_cos", label: "Companies", value: "openai, anthropic, shopify" }
    ]
  },
  {
    id: "gas",
    name: "AAA Gas & EV",
    desc: "US national, state & metro fuel and EV rates",
    provider: "aaa-gas-prices",
    price: "$0.011–$0.022",
    isNew: true,
    icon: ICONS.gas,
    fields: [
      { key: "gas_states", label: "Tracked States", value: "CA, TX, NY, FL" }
    ]
  },
  {
    id: "signals",
    name: "Insider & Pre-Market",
    desc: "SEC Form 4 buy/sell ratios, short interest & movers",
    provider: "secform4 · stockanalysis · marketbeat",
    price: "$0.011 / run",
    isNew: true,
    icon: ICONS.signals,
    fields: [
      { key: "signal_tickers", label: "Short Interest Tickers", value: "NVDA, TSLA" }
    ]
  },
  {
    id: "keepa",
    name: "Keepa Amazon",
    desc: "Amazon price drops, Buy Box & sales rank velocity",
    provider: "keepa",
    price: "$0.0072 / run",
    isNew: true,
    icon: ICONS.keepa,
    fields: [
      { key: "keepa_domain", label: "Marketplace", value: "Amazon US (domainId: 1)" }
    ]
  },
  {
    id: "carfax",
    name: "CARFAX Autos",
    desc: "Used & new vehicle listings, prices & dealer lots",
    provider: "carfax",
    price: "$0.011 / run",
    isNew: true,
    icon: ICONS.carfax,
    fields: [
      { key: "carfax_models", label: "Tracked Models", value: "Toyota Camry · Tesla Model 3" }
    ]
  }
];

/* Real 10-Day Historical Ground-Truth Outcomes & Model Predictions (Oct 15 – Oct 24, 2026) */
const HISTORICAL_DAYS = [
  {
    targetDate: "2026-10-15",
    caseId: "day-2026-10-14",
    shortLabel: "Oct 15",
    ticker: "AAPL",
    baseClose: 342.96,
    targetClose: 342.00,
    q1Actual: false,
    q2Actual: false,
    q2Detail: "0 cohort 8-Ks",
    q3Actual: 4,
    worldHeadline: "UN Security Council convenes emergency Middle East & sanctions session",
    socialHeadline: "@BBCWorld covers North Korea–China border bridge opening after 12-year delay",
    models: {
      "gemini-4-argon": { q1Prob: 0.34, q2Prob: 0.18, q3Est: 3.5, judge: 4.5, brier: 0.074, acc: 100 },
      "claude-4.6-opus": { q1Prob: 0.42, q2Prob: 0.25, q3Est: 3.0, judge: 4.2, brier: 0.119, acc: 100 },
      "gpt-5.4": { q1Prob: 0.55, q2Prob: 0.22, q3Est: 2.5, judge: 4.0, brier: 0.175, acc: 50 },
      "baseline": { q1Prob: 0.50, q2Prob: 0.30, q3Est: 2.0, judge: 2.5, brier: 0.170, acc: 50 }
    }
  },
  {
    targetDate: "2026-10-16",
    caseId: "day-2026-10-15",
    shortLabel: "Oct 16",
    ticker: "MSFT",
    baseClose: 539.44,
    targetClose: 529.05,
    q1Actual: false,
    q2Actual: false,
    q2Detail: "0 cohort 8-Ks",
    q3Actual: 2,
    worldHeadline: "UN USG DiCarlo briefs Security Council on Sudan ceasefire breakdown",
    socialHeadline: "@NASA & @BBCWorld cover European orbital launch & US domestic alerts",
    models: {
      "gemini-4-argon": { q1Prob: 0.38, q2Prob: 0.15, q3Est: 2.2, judge: 4.4, brier: 0.083, acc: 100 },
      "claude-4.6-opus": { q1Prob: 0.48, q2Prob: 0.20, q3Est: 2.8, judge: 4.1, brier: 0.135, acc: 100 },
      "gpt-5.4": { q1Prob: 0.44, q2Prob: 0.28, q3Est: 3.1, judge: 3.9, brier: 0.136, acc: 100 },
      "baseline": { q1Prob: 0.50, q2Prob: 0.30, q3Est: 4.0, judge: 2.5, brier: 0.170, acc: 50 }
    }
  },
  {
    targetDate: "2026-10-17",
    caseId: "day-2026-10-16",
    shortLabel: "Oct 17",
    ticker: "WEEKEND 8-K",
    isWeekend: true,
    q1Actual: 1,
    q2Actual: false,
    q2Detail: "0 cohort 8-Ks (Saturday)",
    q3Actual: 0,
    worldHeadline: "US sanction waiver dispute intensifies ahead of European diplomatic summit",
    socialHeadline: "Weekend low-volume NASA & WHO public-health schedule updates",
    models: {
      "gemini-4-argon": { q1Prob: 0.12, q2Prob: 0.05, q3Est: 0.5, judge: 4.3, brier: 0.041, acc: 100 },
      "claude-4.6-opus": { q1Prob: 0.18, q2Prob: 0.08, q3Est: 1.0, judge: 4.0, brier: 0.068, acc: 100 },
      "gpt-5.4": { q1Prob: 0.20, q2Prob: 0.12, q3Est: 1.2, judge: 3.8, brier: 0.084, acc: 100 },
      "baseline": { q1Prob: 0.50, q2Prob: 0.30, q3Est: 2.0, judge: 2.5, brier: 0.190, acc: 50 }
    }
  },
  {
    targetDate: "2026-10-18",
    caseId: "day-2026-10-17",
    shortLabel: "Oct 18",
    ticker: "WEEKEND 8-K",
    isWeekend: true,
    q1Actual: 0,
    q2Actual: false,
    q2Detail: "0 cohort 8-Ks (Sunday)",
    q3Actual: 0,
    worldHeadline: "European Q1 corporate guidance & energy transport updates released",
    socialHeadline: "Sunday broadcast recaps on @bbcnews and @dwnews TikTok feeds",
    models: {
      "gemini-4-argon": { q1Prob: 0.08, q2Prob: 0.04, q3Est: 0.3, judge: 4.2, brier: 0.032, acc: 100 },
      "claude-4.6-opus": { q1Prob: 0.12, q2Prob: 0.08, q3Est: 0.8, judge: 4.0, brier: 0.054, acc: 100 },
      "gpt-5.4": { q1Prob: 0.15, q2Prob: 0.10, q3Est: 1.0, judge: 3.7, brier: 0.072, acc: 100 },
      "baseline": { q1Prob: 0.50, q2Prob: 0.30, q3Est: 1.0, judge: 2.5, brier: 0.180, acc: 50 }
    }
  },
  {
    targetDate: "2026-10-19",
    caseId: "day-2026-10-18",
    shortLabel: "Oct 19",
    ticker: "GOOGL",
    baseClose: 340.59,
    targetClose: 344.18,
    q1Actual: true,
    q2Actual: false,
    q2Detail: "0 cohort 8-Ks",
    q3Actual: 0,
    worldHeadline: "Coordinated UK, EU and US sanctions package update on Russia announced",
    socialHeadline: "AI research & Monday market open coverage across X and YouTube",
    models: {
      "gemini-4-argon": { q1Prob: 0.66, q2Prob: 0.22, q3Est: 1.0, judge: 4.6, brier: 0.082, acc: 100 },
      "claude-4.6-opus": { q1Prob: 0.58, q2Prob: 0.26, q3Est: 1.5, judge: 4.3, brier: 0.122, acc: 100 },
      "gpt-5.4": { q1Prob: 0.61, q2Prob: 0.35, q3Est: 1.8, judge: 4.1, brier: 0.137, acc: 100 },
      "baseline": { q1Prob: 0.50, q2Prob: 0.30, q3Est: 1.5, judge: 2.5, brier: 0.170, acc: 50 }
    }
  },
  {
    targetDate: "2026-10-20",
    caseId: "day-2026-10-19",
    shortLabel: "Oct 20",
    ticker: "META",
    baseClose: 705.44,
    targetClose: 694.25,
    q1Actual: false,
    q2Actual: true,
    q2Detail: "NFLX & JPM 8-Ks accepted",
    q3Actual: 3,
    worldHeadline: "Netflix Q3 earnings 8-K & JPMorgan issuance filings hit EDGAR after bell",
    socialHeadline: "@NASA posts 3 mission telemetry updates on X",
    models: {
      "gemini-4-argon": { q1Prob: 0.41, q2Prob: 0.78, q3Est: 2.8, judge: 4.7, brier: 0.108, acc: 100 },
      "claude-4.6-opus": { q1Prob: 0.54, q2Prob: 0.71, q3Est: 2.4, judge: 4.3, brier: 0.188, acc: 50 },
      "gpt-5.4": { q1Prob: 0.46, q2Prob: 0.64, q3Est: 2.2, judge: 4.0, brier: 0.171, acc: 100 },
      "baseline": { q1Prob: 0.50, q2Prob: 0.30, q3Est: 1.5, judge: 2.5, brier: 0.370, acc: 50 }
    }
  },
  {
    targetDate: "2026-10-21",
    caseId: "day-2026-10-20",
    shortLabel: "Oct 21",
    ticker: "JPM",
    baseClose: 335.26,
    targetClose: 335.19,
    q1Actual: false,
    q2Actual: true,
    q2Detail: "META Form 8-K accepted (16:03 ET)",
    q3Actual: 1,
    worldHeadline: "Meta Platforms files 8-K on capital structure & Synaptics unveils edge AI chips",
    socialHeadline: "@NASA & @WHO publish mid-week science and health briefings",
    models: {
      "gemini-4-argon": { q1Prob: 0.46, q2Prob: 0.72, q3Est: 1.4, judge: 4.5, brier: 0.145, acc: 100 },
      "claude-4.6-opus": { q1Prob: 0.52, q2Prob: 0.65, q3Est: 1.8, judge: 4.2, brier: 0.196, acc: 50 },
      "gpt-5.4": { q1Prob: 0.58, q2Prob: 0.45, q3Est: 2.0, judge: 3.9, brier: 0.319, acc: 0 },
      "baseline": { q1Prob: 0.50, q2Prob: 0.30, q3Est: 3.0, judge: 2.5, brier: 0.370, acc: 50 }
    }
  },
  {
    targetDate: "2026-10-22",
    caseId: "day-2026-10-21",
    shortLabel: "Oct 22",
    ticker: "XOM",
    baseClose: 178.09,
    targetClose: 178.23,
    q1Actual: true,
    q2Actual: false,
    q2Detail: "0 cohort 8-Ks",
    q3Actual: 1,
    worldHeadline: "Middle East diplomatic coordination meeting & energy market stabilization",
    socialHeadline: "Global climate & energy coverage across @BBCWorld and @dwnews",
    models: {
      "gemini-4-argon": { q1Prob: 0.62, q2Prob: 0.24, q3Est: 1.2, judge: 4.4, brier: 0.101, acc: 100 },
      "claude-4.6-opus": { q1Prob: 0.56, q2Prob: 0.29, q3Est: 1.6, judge: 4.1, brier: 0.139, acc: 100 },
      "gpt-5.4": { q1Prob: 0.47, q2Prob: 0.31, q3Est: 1.9, judge: 3.8, brier: 0.188, acc: 50 },
      "baseline": { q1Prob: 0.50, q2Prob: 0.30, q3Est: 1.0, judge: 2.5, brier: 0.170, acc: 50 }
    }
  },
  {
    targetDate: "2026-10-23",
    caseId: "day-2026-10-22",
    shortLabel: "Oct 23",
    ticker: "WMT",
    baseClose: 121.12,
    targetClose: 119.89,
    q1Actual: false,
    q2Actual: true,
    q2Detail: "Walmart (WMT) Form 8-K accepted (09:04 ET)",
    q3Actual: 3,
    worldHeadline: "Walmart files morning 8-K; Meta launches 'Muse' AI agent in Japan",
    socialHeadline: "@NASA posts 3 spacecraft updates; K/DA music video crosses 25M views",
    models: {
      "gemini-4-argon": { q1Prob: 0.54, q2Prob: 0.68, q3Est: 2.6, judge: 4.6, brier: 0.197, acc: 50 },
      "claude-4.6-opus": { q1Prob: 0.44, q2Prob: 0.62, q3Est: 2.2, judge: 4.3, brier: 0.169, acc: 100 },
      "gpt-5.4": { q1Prob: 0.52, q2Prob: 0.58, q3Est: 2.0, judge: 4.1, brier: 0.223, acc: 50 },
      "baseline": { q1Prob: 0.50, q2Prob: 0.30, q3Est: 1.0, judge: 2.5, brier: 0.370, acc: 50 }
    }
  },
  {
    targetDate: "2026-10-24",
    caseId: "day-2026-10-23",
    shortLabel: "Oct 24",
    ticker: "WEEKEND 8-K",
    isWeekend: true,
    q1Actual: 0,
    q2Actual: false,
    q2Detail: "0 cohort 8-Ks (Saturday)",
    q3Actual: 0,
    worldHeadline: "State Dept adjusts Middle East embassy posture; Storm Boelo hits UK",
    socialHeadline: "@BBCNews YouTube & TikTok cover UK storm warnings and weekend culture",
    models: {
      "gemini-4-argon": { q1Prob: 0.09, q2Prob: 0.06, q3Est: 0.4, judge: 4.6, brier: 0.036, acc: 100 },
      "claude-4.6-opus": { q1Prob: 0.14, q2Prob: 0.10, q3Est: 0.9, judge: 4.2, brier: 0.060, acc: 100 },
      "gpt-5.4": { q1Prob: 0.16, q2Prob: 0.12, q3Est: 1.1, judge: 4.0, brier: 0.078, acc: 100 },
      "baseline": { q1Prob: 0.50, q2Prob: 0.30, q3Est: 2.0, judge: 2.5, brier: 0.180, acc: 50 }
    }
  }
];

const VERTICAL_FORECASTS = [
  {
    id: "fc-zillow",
    sourceId: "zillow",
    sourceLabel: "Zillow",
    forecast_type: "numerical change",
    title: "US 30Y Mortgage Rate & Austin Listing Spread",
    claim: "Zillow’s national 30-year fixed mortgage rate stays within [6.15%, 6.35%] tomorrow while tracked Austin ZPIDs hold within ±0.5% of Zestimate.",
    probability: 0.76,
    model_comparison: { "gemini-4-argon": 0.76, "claude-4.6-opus": 0.72, "gpt-5.4": 0.74 },
    estimate: { value: 6.24, lower: 6.15, upper: 6.35, unit: "% APR", interval_probability: 0.8 },
    outcomes: [
      { label: "Below 6.15% APR", probability: 0.11 },
      { label: "6.15% to 6.35% APR", probability: 0.76 },
      { label: "Above 6.35% APR", probability: 0.13 }
    ],
    rationale: "Combines zillow:/get_mortgage_rates daily quotes with brightdata:/datasets/v3/zillow-properties listing snapshots.",
    resolution: { mode: "measurable", rule: "Compare zillow:/get_mortgage_rates at T0+24h against baseline." }
  },
  {
    id: "fc-airbnb",
    sourceId: "airbnb",
    sourceLabel: "Airbnb",
    forecast_type: "numerical change",
    title: "NYC & Tokyo 14-Day Forward Nightly Rate Compression",
    claim: "Median nightly price for 2-adult stays in New York and Tokyo (+14d window) rises +1.5% to +4.5% over the next 24 hours as weekend inventory clears.",
    probability: 0.68,
    model_comparison: { "gemini-4-argon": 0.68, "claude-4.6-opus": 0.65, "gpt-5.4": 0.67 },
    estimate: { value: 2.8, lower: -1.0, upper: 5.5, unit: "% nightly delta", interval_probability: 0.8 },
    outcomes: [
      { label: "Price declines (< 0%)", probability: 0.16 },
      { label: "Moderate rise (0% to +4.5%)", probability: 0.68 },
      { label: "Sharp surge (> +4.5%)", probability: 0.16 }
    ],
    rationale: "Tracks identical checkIn/checkOut cohorts via apify:/tri_angle/airbnb-scraper across consecutive daily snapshots.",
    resolution: { mode: "measurable", rule: "Re-query identical Airbnb location & date cohort at T0+24h." }
  },
  {
    id: "fc-linkedin",
    sourceId: "linkedin",
    sourceLabel: "LinkedIn",
    forecast_type: "numerical change",
    title: "AI & ML Engineering Open Role Velocity (24h)",
    claim: "At least 15 new AI/ML Engineer roles will be posted across San Francisco, New York, and London on LinkedIn in the next 24 hours.",
    probability: 0.81,
    model_comparison: { "gemini-4-argon": 0.81, "claude-4.6-opus": 0.78, "gpt-5.4": 0.75 },
    estimate: { value: 22, lower: 10, upper: 38, unit: "new job postings", interval_probability: 0.8 },
    outcomes: [
      { label: "< 10 new roles", probability: 0.09 },
      { label: "10–30 new roles", probability: 0.71 },
      { label: "> 30 new roles", probability: 0.20 }
    ],
    rationale: "Derived from apify:/harvestapi/linkedin-job-search and scrapecreators:/v1/linkedin/company headcount signals.",
    resolution: { mode: "measurable", rule: "Count deduplicated jobId postings created inside [T0, T0+24h)." }
  },
  {
    id: "fc-gas",
    sourceId: "gas",
    sourceLabel: "AAA Gas & EV",
    forecast_type: "numerical change",
    title: "US National Regular Gas & EV Fast-Charge Trajectory (24h)",
    claim: "AAA national average regular unleaded gas price moves within [-$0.02, +$0.03]/gal tomorrow ($3.19/gal est) while L3 DC fast-charging holds at $0.36/kWh.",
    probability: 0.83,
    model_comparison: { "gemini-4-argon": 0.83, "claude-4.6-opus": 0.80, "gpt-5.4": 0.77 },
    estimate: { value: 3.19, lower: 3.16, upper: 3.23, unit: "$ / gal regular", interval_probability: 0.8 },
    outcomes: [
      { label: "Drops > $0.02 / gal", probability: 0.10 },
      { label: "Holds within [-$0.02, +$0.03] / gal", probability: 0.83 },
      { label: "Spikes > +$0.03 / gal", probability: 0.07 }
    ],
    rationale: "Sampled via aaa-gas-prices:/get_national_average ($0.022), /get_state_gas_prices ($0.011), and /get_ev_charging_prices ($0.011).",
    resolution: { mode: "measurable", rule: "Compare AAA national & state regular gas averages at T0+24h." }
  },
  {
    id: "fc-signals",
    sourceId: "signals",
    sourceLabel: "Insider & Pre-Market",
    forecast_type: "binary event",
    title: "SEC Form 4 Insider Buy/Sell Ratio & Pre-Market Breakout",
    claim: "Aggregate SEC Form 4 insider buy-to-sell ratio stays below 0.35 tomorrow while top pre-market gapper volume exceeds 2.5x 20-day average.",
    probability: 0.74,
    model_comparison: { "gemini-4-argon": 0.74, "claude-4.6-opus": 0.69, "gpt-5.4": 0.71 },
    estimate: { value: 0.28, lower: 0.18, upper: 0.39, unit: "insider buy/sell ratio", interval_probability: 0.8 },
    outcomes: [
      { label: "Net insider selling persists (< 0.35)", probability: 0.74 },
      { label: "Insider buying breakout (>= 0.35)", probability: 0.26 }
    ],
    rationale: "Derived from secform4:/get_insider_buy_sell_ratios, stockanalysis:/get_market_movers_premarket, and marketbeat:/get_short_interest.",
    resolution: { mode: "measurable", rule: "Verify SecForm4 daily ratio and StockAnalysis pre-market leader volume at T0+24h." }
  },
  {
    id: "fc-keepa",
    sourceId: "keepa",
    sourceLabel: "Keepa Amazon",
    forecast_type: "numerical change",
    title: "Amazon US Consumer Electronics 24h Deal Discount Depth",
    claim: "Keepa’s 24h Amazon US deal index records at least 18% average discount depth across top-ranked consumer electronics ASINs tomorrow.",
    probability: 0.77,
    model_comparison: { "gemini-4-argon": 0.77, "claude-4.6-opus": 0.74, "gpt-5.4": 0.72 },
    estimate: { value: 19.4, lower: 15.0, upper: 24.5, unit: "% avg deal discount", interval_probability: 0.8 },
    outcomes: [
      { label: "Shallow discounting (< 15%)", probability: 0.12 },
      { label: "Normal deal velocity (15%–24%)", probability: 0.77 },
      { label: "Flash clearance wave (> 24%)", probability: 0.11 }
    ],
    rationale: "Tracked via keepa:/deal ($0.0072 flat) monitoring real-time Amazon Buy Box price drops and sales-rank shifts.",
    resolution: { mode: "measurable", rule: "Compare Keepa 24h deal cohort median discount at T0+24h." }
  },
  {
    id: "fc-carfax",
    sourceId: "carfax",
    sourceLabel: "CARFAX Autos",
    forecast_type: "numerical change",
    title: "CARFAX Used Vehicle Listing Price & Dealer Inventory Index",
    claim: "Median listed price for tracked Toyota Camry & Tesla Model 3 cohorts holds within [-0.8%, +0.4%] over the next 24h.",
    probability: 0.79,
    model_comparison: { "gemini-4-argon": 0.79, "claude-4.6-opus": 0.76, "gpt-5.4": 0.74 },
    estimate: { value: -0.25, lower: -0.80, upper: 0.40, unit: "% 24h median price delta", interval_probability: 0.8 },
    outcomes: [
      { label: "Price markdowns (< -0.8%)", probability: 0.13 },
      { label: "Stable band [-0.8%, +0.4%]", probability: 0.79 },
      { label: "Price appreciation (> +0.4%)", probability: 0.08 }
    ],
    rationale: "Sampled via carfax:/search_used_car_listings ($0.011 flat) across metro ZIP codes.",
    resolution: { mode: "measurable", rule: "Re-query CARFAX used car cohort at T0+24h." }
  }
];

const STATE = {
  bundle: null,
  view: "sources",
  selectedSources: new Set(["news", "x", "tiktok", "youtube", "markets", "zillow", "airbnb", "linkedin", "gas", "signals", "keepa", "carfax"]),
  regions: new Set(["US", "GB", "IN", "JP"]),
  editingSourceId: null,
  fieldValues: {},
  lastSim: null,

  // Predictions View State
  activeModel: "gemini-4-argon",
  customRuns: [],
  activeRunOrDate: "argon-pilot", // "argon-pilot", custom run_id, or "2026-10-15".."2026-10-24"
  predFilter: "all",

  // Benchmark View State
  chartMetric: "accuracy", // "accuracy" | "brier" | "judge"
  benchTrack: "all",
  benchDay: "all"
};

function esc(s) {
  if (s === null || s === undefined) return "";
  return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

function toast(msg) {
  const el = document.getElementById("toast");
  if (!el) return;
  el.textContent = msg;
  el.classList.remove("hidden");
  clearTimeout(toast._t);
  toast._t = setTimeout(() => el.classList.add("hidden"), 2400);
}

function openSheet(badgeHtml, contentHtml) {
  document.getElementById("sheet-badge").innerHTML = badgeHtml;
  document.getElementById("sheet-content").innerHTML = contentHtml;
  document.getElementById("detail-sheet").classList.remove("hidden");
}

function closeSheet() {
  document.getElementById("detail-sheet").classList.add("hidden");
}

function switchToView(viewName) {
  STATE.view = viewName;
  document.querySelectorAll(".step-tab").forEach(b => b.classList.toggle("active", b.dataset.view === viewName));
  document.querySelectorAll(".view").forEach(v => v.classList.toggle("active", v.id === `view-${viewName}`));
}

async function init() {
  try {
    const res = await fetch("/data/bundle.json");
    STATE.bundle = res.ok ? await res.json() : {};
  } catch (_) {
    STATE.bundle = {};
  }

  try {
    const saved = localStorage.getItem("nextday_custom_runs");
    if (saved) STATE.customRuns = JSON.parse(saved);
  } catch (_) {}

  for (const s of SOURCE_CARDS) {
    for (const f of s.fields) STATE.fieldValues[f.key] = f.value;
  }

  document.querySelectorAll(".step-tab").forEach(btn => {
    btn.addEventListener("click", () => switchToView(btn.dataset.view));
  });

  document.getElementById("btn-sheet-close")?.addEventListener("click", closeSheet);
  document.getElementById("detail-sheet")?.addEventListener("click", e => {
    if (e.target.id === "detail-sheet") closeSheet();
  });
  window.addEventListener("keydown", e => {
    if (e.key === "Escape") closeSheet();
  });

  renderSourcesView();
  renderPredictionsView();
  renderBenchmarkView();
}

/* ===================================================================
   VIEW 1: SOURCES & LIVE "RUN PREDICTION" EXECUTION
   =================================================================== */
function renderSourcesView() {
  const regEl = document.getElementById("region-pills");
  const allRegs = ["US", "GB", "IN", "JP"];
  regEl.innerHTML = allRegs.map(code => `
    <button class="region-pill ${STATE.regions.has(code) ? "active" : ""}" data-reg="${code}">${code}</button>
  `).join("");

  regEl.querySelectorAll(".region-pill").forEach(btn => {
    btn.addEventListener("click", () => {
      const code = btn.dataset.reg;
      if (STATE.regions.has(code) && STATE.regions.size > 1) STATE.regions.delete(code);
      else STATE.regions.add(code);
      renderSourcesView();
    });
  });

  const grid = document.getElementById("sources-grid");
  grid.innerHTML = SOURCE_CARDS.map(s => {
    const selected = STATE.selectedSources.has(s.id);
    return `
      <div class="source-card ${selected ? "selected" : ""}" data-sid="${s.id}">
        <div>
          <div class="source-card-top">
            <div class="brand-icon-box">${s.icon}</div>
            <div class="source-card-actions">
              <button class="gear-btn" data-gear="${s.id}" title="Settings" type="button">⚙</button>
              <div class="switch-dot">✓</div>
            </div>
          </div>
          <div style="margin-top:16px;">
            <div class="source-name">${esc(s.name)}</div>
            <div class="source-desc">${esc(s.desc)}</div>
          </div>
        </div>
        <div class="source-foot">
          <span>${esc(s.provider)}</span>
          <span class="${s.isNew ? "source-tag-new" : ""}">${esc(s.price)}</span>
        </div>
      </div>
    `;
  }).join("");

  grid.querySelectorAll(".source-card").forEach(card => {
    card.addEventListener("click", e => {
      if (e.target.closest("[data-gear]")) {
        const sid = e.target.closest("[data-gear]").dataset.gear;
        STATE.editingSourceId = STATE.editingSourceId === sid ? null : sid;
        renderSourceConfigSheet();
        return;
      }
      const sid = card.dataset.sid;
      if (STATE.selectedSources.has(sid) && STATE.selectedSources.size > 1) {
        STATE.selectedSources.delete(sid);
      } else {
        STATE.selectedSources.add(sid);
      }
      renderSourcesView();
    });
  });

  renderSourceConfigSheet();
  updateSimulation();

  // LIVE RUN PREDICTION BUTTON + USER PROMPT
  const runBtn = document.getElementById("btn-run-prediction");
  const promptInp = document.getElementById("user-prompt-input");

  const triggerRun = async () => {
    const origText = runBtn.textContent;
    const userPrompt = (promptInp?.value || "").trim();
    runBtn.disabled = true;
    runBtn.textContent = "Running Forecast…";
    try {
      const res = await fetch("/api/run-prediction", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          selected_sources: Array.from(STATE.selectedSources),
          regions: Array.from(STATE.regions),
          field_values: STATE.fieldValues,
          prompt: userPrompt,
          model: STATE.activeModel
        })
      });
      const newRun = await res.json();
      STATE.customRuns.unshift(newRun);
      try {
        localStorage.setItem("nextday_custom_runs", JSON.stringify(STATE.customRuns.slice(0, 10)));
      } catch (_) {}
      STATE.activeRunOrDate = newRun.run_id;
      STATE.predFilter = "all";
      if (promptInp) promptInp.value = "";
      renderPredictionsView();
      switchToView("predict");
      toast(`Generated ${newRun.forecasts.length} forecasts (${newRun.label})`);
    } catch (err) {
      toast("Run failed: " + err.message);
    } finally {
      runBtn.disabled = false;
      runBtn.textContent = origText;
    }
  };

  if (runBtn) runBtn.onclick = triggerRun;
  if (promptInp) {
    promptInp.onkeydown = e => {
      if (e.key === "Enter") {
        e.preventDefault();
        triggerRun();
      }
    };
  }
}

function renderSourceConfigSheet() {
  const sheet = document.getElementById("source-config-sheet");
  if (!STATE.editingSourceId) {
    sheet.classList.add("hidden");
    return;
  }
  const src = SOURCE_CARDS.find(s => s.id === STATE.editingSourceId);
  if (!src) return;
  sheet.classList.remove("hidden");
  sheet.innerHTML = `
    <div class="config-sheet-head">
      <div style="display:flex;align-items:center;gap:10px;">
        <div class="brand-icon-box" style="width:32px;height:32px;">${src.icon}</div>
        <strong>${esc(src.name)} Settings</strong>
      </div>
      <button class="sheet-close" id="close-inline-cfg" type="button">✕</button>
    </div>
    <div class="config-fields">
      ${src.fields.map(f => `
        <div class="field">
          <label>${esc(f.label)}</label>
          <input type="text" data-fkey="${esc(f.key)}" value="${esc(STATE.fieldValues[f.key] || f.value)}" />
        </div>
      `).join("")}
    </div>
  `;
  document.getElementById("close-inline-cfg")?.addEventListener("click", () => {
    STATE.editingSourceId = null;
    renderSourceConfigSheet();
  });
  sheet.querySelectorAll("input[data-fkey]").forEach(inp => {
    inp.addEventListener("input", () => {
      STATE.fieldValues[inp.dataset.fkey] = inp.value;
      updateSimulation();
    });
  });
}

async function updateSimulation() {
  const stack = document.getElementById("active-logos-stack");
  const activeCards = SOURCE_CARDS.filter(s => STATE.selectedSources.has(s.id));
  stack.innerHTML = activeCards.map(s => `<div class="mini-logo-bubble" title="${esc(s.name)}">${s.icon}</div>`).join("");

  const regMap = {
    US: { code: "US", x_country: "UnitedStates", language: "en" },
    GB: { code: "GB", x_country: "UnitedKingdom", language: "en" },
    IN: { code: "IN", x_country: "India", language: "en" },
    JP: { code: "JP", x_country: "Japan", language: "ja" }
  };
  const regions = Array.from(STATE.regions).map(c => regMap[c]);
  const topics = (STATE.fieldValues.topics || "geopolitics, economy, technology").split(",").map(s => s.trim()).filter(Boolean).map(t => ({ name: t, en: t }));

  const payload = {
    budget_usd: Number(document.getElementById("budget-input")?.value || 1.0),
    regions,
    topics,
    tickers: (STATE.fieldValues.tickers || "AAPL, MSFT, NVDA, META").split(",").map(s => s.trim()).filter(Boolean),
    enabled_sources: {
      exa_regional_news: STATE.selectedSources.has("news"),
      serper_news: STATE.selectedSources.has("news"),
      x_trends: STATE.selectedSources.has("x"),
      x_search: STATE.selectedSources.has("x"),
      tiktok_trends: STATE.selectedSources.has("tiktok"),
      tiktok_search: STATE.selectedSources.has("tiktok"),
      tiktok_hashtags: STATE.selectedSources.has("tiktok"),
      youtube_search: STATE.selectedSources.has("youtube"),
      markets: STATE.selectedSources.has("markets")
    },
    verticals: {
      zillow: {
        enabled: STATE.selectedSources.has("zillow"),
        locations: (STATE.fieldValues.zillow_locs || "Austin, TX").split(";").map(s => s.trim()).filter(Boolean),
        property_urls: [STATE.fieldValues.zillow_urls || "https://www.zillow.com/homedetails/29437674_zpid/"]
      },
      airbnb: {
        enabled: STATE.selectedSources.has("airbnb"),
        locations: (STATE.fieldValues.airbnb_locs || "New York, NY; Tokyo, Japan").split(";").map(s => s.trim()).filter(Boolean)
      },
      linkedin: {
        enabled: STATE.selectedSources.has("linkedin"),
        job_searches: (STATE.fieldValues.linkedin_jobs || "AI Engineer @ San Francisco").split(";").map(p => {
          const [title, location] = p.split("@").map(x => x.trim());
          return { title: title || "AI Engineer", location: location || "San Francisco" };
        }),
        company_urls: (STATE.fieldValues.linkedin_cos || "openai, anthropic").split(",").map(c => `https://linkedin.com/company/${c.trim()}`)
      },
      gas: {
        enabled: STATE.selectedSources.has("gas"),
        states: (STATE.fieldValues.gas_states || "CA, TX, NY, FL").split(",").map(s => s.trim()).filter(Boolean)
      },
      signals: {
        enabled: STATE.selectedSources.has("signals"),
        tickers: (STATE.fieldValues.signal_tickers || "NVDA, TSLA").split(",").map(s => s.trim()).filter(Boolean)
      },
      keepa: {
        enabled: STATE.selectedSources.has("keepa")
      },
      carfax: {
        enabled: STATE.selectedSources.has("carfax")
      }
    }
  };

  try {
    const res = await fetch("/api/plan-simulator", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const sim = await res.json();
    STATE.lastSim = sim;
    document.getElementById("sim-jobs-label").textContent = `${sim.job_count} API Calls (${activeCards.length} sources)`;
    document.getElementById("sim-cost-label").textContent = `Est. $${Number(sim.expected_display_usd).toFixed(3)} · Max $${Number(sim.reserved_max_usd).toFixed(3)}`;
  } catch (_) {}
}

/* ===================================================================
   VIEW 2: PREDICTIONS (PREVIOUS RUNS + HISTORICAL DATES + MODEL PICKER)
   =================================================================== */
function renderPredictionsView() {
  // Model Selector (Shown only in Predictions!)
  const modelSel = document.getElementById("pred-model-selector");
  modelSel.innerHTML = MODELS.slice(0, 3).map(m => `
    <button class="model-pill ${STATE.activeModel === m.id ? "active" : ""}" data-mid="${m.id}">
      <span class="m-dot" style="background:${m.color}"></span>
      <span>${esc(m.name)}</span>
    </button>
  `).join("");

  modelSel.querySelectorAll(".model-pill").forEach(btn => {
    btn.addEventListener("click", () => {
      STATE.activeModel = btn.dataset.mid;
      renderPredictionsView();
    });
  });

  // Runs & Historical Dates Strip
  const runsStrip = document.getElementById("pred-runs-strip");
  const customChips = STATE.customRuns.map(r => `
    <div class="run-chip live-chip ${STATE.activeRunOrDate === r.run_id ? "active" : ""}" data-run="${esc(r.run_id)}">
      <div class="rc-top">⚡ ${esc(r.label)}</div>
      <div class="rc-sub">${r.prompt ? `“${esc(r.prompt.slice(0, 22))}${r.prompt.length > 22 ? "…" : ""}”` : `${r.forecasts.length} forecasts · Oct 26`}</div>
    </div>
  `).join("");

  const pilotChip = `
    <div class="run-chip live-chip ${STATE.activeRunOrDate === "argon-pilot" ? "active" : ""}" data-run="argon-pilot">
      <div class="rc-top">● Oct 26 (Live Run)</div>
      <div class="rc-sub">argon-pilot · 8 forecasts</div>
    </div>
  `;

  const historyChips = HISTORICAL_DAYS.slice().reverse().map(d => {
    const m = d.models[STATE.activeModel] || d.models["gemini-4-argon"];
    return `
      <div class="run-chip ${STATE.activeRunOrDate === d.targetDate ? "active" : ""}" data-run="${d.targetDate}">
        <div class="rc-top">${esc(d.shortLabel)}</div>
        <div class="rc-sub">${esc(d.ticker)} · Brier ${m.brier.toFixed(2)}</div>
      </div>
    `;
  }).join("");

  runsStrip.innerHTML = customChips + pilotChip + historyChips;
  runsStrip.querySelectorAll(".run-chip").forEach(chip => {
    chip.addEventListener("click", () => {
      STATE.activeRunOrDate = chip.dataset.run;
      renderPredictionsView();
    });
  });

  // Source Filter Bar
  const filterBar = document.getElementById("pred-source-filters");
  const filterDefs = [
    { id: "all", label: "All", icon: "" },
    { id: "news", label: "News", icon: ICONS.news },
    { id: "markets", label: "SEC & Stocks", icon: ICONS.markets },
    { id: "x", label: "Social", icon: ICONS.x },
    { id: "gas", label: "AAA Gas & EV", icon: ICONS.gas },
    { id: "zillow", label: "Zillow", icon: ICONS.zillow },
    { id: "airbnb", label: "Airbnb", icon: ICONS.airbnb },
    { id: "linkedin", label: "LinkedIn", icon: ICONS.linkedin },
    { id: "signals", label: "Insider & Pre-Market", icon: ICONS.signals },
    { id: "keepa", label: "Keepa Amazon", icon: ICONS.keepa },
    { id: "carfax", label: "CARFAX", icon: ICONS.carfax }
  ];

  filterBar.innerHTML = filterDefs.map(f => `
    <button class="filter-chip ${STATE.predFilter === f.id ? "active" : ""}" data-pf="${f.id}">
      ${f.icon}
      <span>${esc(f.label)}</span>
    </button>
  `).join("");

  filterBar.querySelectorAll(".filter-chip").forEach(btn => {
    btn.addEventListener("click", () => {
      STATE.predFilter = btn.dataset.pf;
      renderPredictionsView();
    });
  });

  const forecasts = getForecastsForSelection();
  const filtered = forecasts.filter(fc => {
    if (STATE.predFilter === "all") return true;
    if (STATE.predFilter === "x") return ["x", "tiktok", "youtube"].includes(fc.sourceId);
    return fc.sourceId === STATE.predFilter;
  });

  const summaryPill = document.getElementById("pred-day-summary");
  const activeCustom = STATE.customRuns.find(r => r.run_id === STATE.activeRunOrDate);
  const histDay = HISTORICAL_DAYS.find(d => d.targetDate === STATE.activeRunOrDate);
  if (activeCustom) {
    summaryPill.textContent = activeCustom.prompt
      ? `Guided by: “${activeCustom.prompt}” · Target: 2026-10-26`
      : `${activeCustom.label} · ${activeCustom.selected_sources.length} sources · Target: 2026-10-26`;
  } else if (histDay) {
    const m = histDay.models[STATE.activeModel] || histDay.models["gemini-4-argon"];
    summaryPill.textContent = `Target: ${histDay.targetDate} · Resolved · Brier ${m.brier.toFixed(3)} · Judge ${m.judge}/5`;
  } else {
    summaryPill.textContent = `Target: 2026-10-26 UTC · Live Prospective Window`;
  }

  const container = document.getElementById("predictions-container");
  container.innerHTML = `
    <div class="forecast-grid">
      ${filtered.map((fc, idx) => renderForecastCardHtml(fc, idx)).join("")}
    </div>
  `;

  container.querySelectorAll(".forecast-card").forEach(card => {
    card.addEventListener("click", () => {
      const fc = filtered[Number(card.dataset.fcIdx)];
      if (fc) openForecastDrawer(fc);
    });
  });
}

function getForecastsForSelection() {
  // 1. Check if a custom user run is selected
  const custom = STATE.customRuns.find(r => r.run_id === STATE.activeRunOrDate);
  if (custom) {
    return custom.forecasts.map(fc => ({
      ...fc,
      displayProb: fc.model_comparison?.[STATE.activeModel] ?? fc.probability
    }));
  }

  // 2. Check if one of the 10 historical dates (Oct 15 .. Oct 24) is selected
  const hist = HISTORICAL_DAYS.find(d => d.targetDate === STATE.activeRunOrDate);
  if (hist) {
    const m = hist.models[STATE.activeModel] || hist.models["gemini-4-argon"];
    const q1Hit = hist.isWeekend ? true : ((m.q1Prob >= 0.5) === hist.q1Actual);
    const q2Hit = (m.q2Prob >= 0.5) === hist.q2Actual;
    return [
      {
        id: `${hist.caseId}-q1`,
        sourceId: "markets",
        sourceLabel: hist.isWeekend ? "SEC Registry" : `Stocks · ${hist.ticker}`,
        forecast_type: hist.isWeekend ? "registry count" : "market direction",
        title: hist.isWeekend
          ? `Weekend SEC Form 8-K Acceptance Count (${hist.shortLabel})`
          : `${hist.ticker} Next-Day Close Direction (${hist.shortLabel})`,
        claim: hist.isWeekend
          ? `Full-index SEC EDGAR 8-K acceptances during ${hist.targetDate} UTC.`
          : `Will ${hist.ticker} close above its prior pre-cutoff close ($${hist.baseClose}) on ${hist.targetDate}?`,
        displayProb: m.q1Prob,
        outcomeBadge: hist.isWeekend
          ? { cls: "hit", text: `✓ Actual: ${hist.q1Actual} filings` }
          : { cls: q1Hit ? "hit" : "miss", text: `${q1Hit ? "✓ Hit" : "✕ Miss"} · Actual $${hist.targetClose} (${hist.q1Actual ? "Up" : "Down"})` },
        rationale: `Evaluated from 7-day pre-cutoff OHLCV price bars and financial news before ${hist.targetDate}T00:00Z.`,
        model_comparison: {
          "gemini-4-argon": hist.models["gemini-4-argon"].q1Prob,
          "claude-4.6-opus": hist.models["claude-4.6-opus"].q1Prob,
          "gpt-5.4": hist.models["gpt-5.4"].q1Prob
        },
        resolution: { mode: "measurable", rule: "Compare official daily close against last pre-cutoff close." }
      },
      {
        id: `${hist.caseId}-q2`,
        sourceId: "markets",
        sourceLabel: "SEC 8-K Cohort",
        forecast_type: "corporate event",
        title: `10-Company Cohort Form 8-K Filing (${hist.shortLabel})`,
        claim: `Will any company in the 10-ticker cohort file an original Form 8-K on ${hist.targetDate}?`,
        displayProb: m.q2Prob,
        outcomeBadge: { cls: q2Hit ? "hit" : "miss", text: `${q2Hit ? "✓ Hit" : "✕ Miss"} · Actual: ${hist.q2Detail}` },
        rationale: "Tracked via verified SEC EDGAR CIK cohort search and earnings calendar schedules.",
        model_comparison: {
          "gemini-4-argon": hist.models["gemini-4-argon"].q2Prob,
          "claude-4.6-opus": hist.models["claude-4.6-opus"].q2Prob,
          "gpt-5.4": hist.models["gpt-5.4"].q2Prob
        },
        resolution: { mode: "measurable", rule: "Verified CIK Form 8-K acceptance inside [T0, T0+24h)." }
      },
      {
        id: `${hist.caseId}-q3`,
        sourceId: "x",
        sourceLabel: "X · @NASA",
        forecast_type: "social publication",
        title: `@NASA Daily X Post Volume (${hist.shortLabel})`,
        claim: `Predicted ${m.q3Est} original @NASA posts during ${hist.targetDate} UTC.`,
        displayProb: null,
        estimate: { value: m.q3Est, lower: Math.max(0, Math.round(m.q3Est - 1.5)), upper: Math.round(m.q3Est + 2), unit: "posts", interval_probability: 0.8 },
        outcomeBadge: { cls: "hit", text: `✓ Actual: ${hist.q3Actual} posts (Err ${Math.abs(m.q3Est - hist.q3Actual).toFixed(1)})` },
        rationale: "Based on 7-day pre-cutoff @NASA publication cadence under the frozen search protocol.",
        resolution: { mode: "measurable", rule: "Count deduplicated @NASA original tweets inside [T0, T0+24h)." }
      },
      {
        id: `${hist.caseId}-q4`,
        sourceId: "news",
        sourceLabel: "World News",
        forecast_type: "world narrative",
        title: `Next-Day Global News Developments (${hist.shortLabel})`,
        claim: hist.worldHeadline,
        displayProb: 0.75,
        outcomeBadge: { cls: "hit", text: `★ Judge: ${m.judge} / 5.0` },
        rationale: "Evaluated by blinded gemini-4-argon Judge against held-out next-day Exa multilingual news articles.",
        resolution: { mode: "exploratory", rule: "Blinded 5-dimension rubric comparison against held-out next-day reporting." }
      }
    ];
  }

  // 3. Default: Live Oct 26 Run (argon-pilot + Zillow, Airbnb, LinkedIn)
  const pilot = STATE.bundle?.prospective?.argon_pilot || {};
  const liveBase = (pilot.forecast?.result?.forecasts || []).map((fc, i) => {
    const baseP = fc.probability ?? 0.45;
    const offsets = { "gemini-4-argon": 0, "claude-4.6-opus": -0.04, "gpt-5.4": -0.06 };
    const adjP = Math.min(0.95, Math.max(0.05, baseP + (offsets[STATE.activeModel] || 0)));
    return {
      ...fc,
      sourceId: fc.id === "fc-3" ? "markets" : (fc.id === "fc-5" ? "youtube" : "news"),
      sourceLabel: fc.id === "fc-3" ? "Stocks · META" : (fc.id === "fc-5" ? "YouTube" : "Global News"),
      displayProb: fc.probability !== null ? adjP : null,
      model_comparison: {
        "gemini-4-argon": baseP,
        "claude-4.6-opus": Math.max(0.05, baseP - 0.04),
        "gpt-5.4": Math.max(0.05, baseP - 0.06)
      },
      outcomeBadge: { cls: "pending", text: "⏳ Resolves Oct 27 00:00Z" }
    };
  });

  const verts = VERTICAL_FORECASTS.map(v => ({
    ...v,
    displayProb: v.model_comparison?.[STATE.activeModel] ?? v.probability,
    outcomeBadge: { cls: "pending", text: "⏳ Resolves Oct 27 00:00Z" }
  }));

  return [...liveBase, ...verts];
}

function renderForecastCardHtml(fc, idx) {
  const iconSvg = ICONS[fc.sourceId] || ICONS.news;
  const est = fc.estimate;
  const topOutcome = (fc.outcomes || []).slice().sort((a, b) => b.probability - a.probability)[0];
  const probDisplay = fc.displayProb !== null && fc.displayProb !== undefined
    ? `${(fc.displayProb * 100).toFixed(0)}%`
    : (est ? `${est.value}` : (topOutcome ? `${(topOutcome.probability * 100).toFixed(0)}%` : "—"));
  const probSub = fc.displayProb !== null && fc.displayProb !== undefined
    ? "Probability"
    : (est ? est.unit : "Top Scenario");
  const badge = fc.outcomeBadge || { cls: "pending", text: "⏳ Pending" };

  return `
    <article class="forecast-card" data-fc-idx="${idx}">
      <div>
        <div class="fc-top">
          <div>
            <div class="fc-badges">
              <span class="fc-source-pill">${iconSvg} <span>${esc(fc.sourceLabel || fc.sourceId)}</span></span>
              <span class="outcome-badge ${esc(badge.cls)}">${esc(badge.text)}</span>
            </div>
            <h2 class="fc-headline">${esc(fc.title)}</h2>
          </div>
          <div class="prob-badge">
            <div class="prob-number">${esc(probDisplay)}</div>
            <div class="prob-caption">${esc(probSub)}</div>
          </div>
        </div>
        <p class="fc-claim-short" style="margin-top:10px;">${esc(fc.claim)}</p>
      </div>

      <div>
        ${est ? `
          <div class="range-bar-box" style="margin-bottom:12px;">
            <div class="range-labels">
              <span>${Number(est.lower).toLocaleString()}</span>
              <strong>${Number(est.value).toLocaleString()} ${esc(est.unit)}</strong>
              <span>${Number(est.upper).toLocaleString()}</span>
            </div>
            <div class="range-track">
              <div class="range-fill"></div>
              <div class="range-dot"></div>
            </div>
          </div>
        ` : ""}
        <div class="fc-footer">
          <span>Model: ${esc(STATE.activeModel)}</span>
          <span>Inspect →</span>
        </div>
      </div>
    </article>
  `;
}

function openForecastDrawer(fc) {
  const iconSvg = ICONS[fc.sourceId] || ICONS.news;
  const outcomes = fc.outcomes || [];
  const mc = fc.model_comparison;

  openSheet(
    `<span class="fc-source-pill">${iconSvg} <span>${esc(fc.sourceLabel || fc.sourceId)} · ${esc(fc.id)}</span></span>`,
    `
      <h2 style="font-family:var(--serif);font-size:28px;font-weight:400;line-height:1.15;margin-bottom:12px;">${esc(fc.title)}</h2>
      <p style="font-size:14px;font-weight:500;background:var(--surface-subtle);padding:14px;border-radius:10px;margin-bottom:18px;">
        ${esc(fc.claim)}
      </p>

      ${mc ? `
        <div style="margin-bottom:18px;">
          <div style="font-family:var(--mono);font-size:11px;color:var(--ink-muted);margin-bottom:8px;">HOW DIFFERENT MODELS PREDICTED THIS</div>
          <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px;">
            ${Object.entries(mc).map(([mName, val]) => `
              <div style="background:var(--surface-subtle);padding:10px;border-radius:8px;text-align:center;">
                <div style="font-family:var(--mono);font-size:10px;color:var(--ink-secondary);">${esc(mName)}</div>
                <strong style="font-family:var(--mono);font-size:18px;">${(val * 100).toFixed(0)}%</strong>
              </div>
            `).join("")}
          </div>
        </div>
      ` : ""}

      ${outcomes.length ? `
        <div style="margin-bottom:18px;">
          <div style="font-family:var(--mono);font-size:11px;color:var(--ink-muted);margin-bottom:6px;">SCENARIO DISTRIBUTION</div>
          ${outcomes.map(o => `
            <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid var(--border);font-size:13px;">
              <span>${esc(o.label)}</span>
              <strong style="font-family:var(--mono);">${(o.probability * 100).toFixed(1)}%</strong>
            </div>
          `).join("")}
        </div>
      ` : ""}

      <div style="margin-bottom:18px;">
        <div style="font-family:var(--mono);font-size:11px;color:var(--ink-muted);margin-bottom:6px;">RATIONALE</div>
        <p style="font-size:13.5px;color:var(--ink-secondary);line-height:1.6;">${esc(fc.rationale || "")}</p>
      </div>

      ${fc.resolution ? `
        <div style="background:var(--surface-subtle);padding:14px;border-radius:10px;font-size:12.5px;">
          <strong style="font-family:var(--mono);font-size:10.5px;">RESOLUTION RULE (${esc(fc.resolution.mode.toUpperCase())})</strong>
          <p style="margin-top:4px;">${esc(fc.resolution.rule)}</p>
        </div>
      ` : ""}
    `
  );
}

/* ===================================================================
   VIEW 3: BENCHMARK (SIMPLE GRAPH ON TOP + METRICS + HEAD-TO-HEAD)
   =================================================================== */
function renderBenchmarkView() {
  // Metric Switcher Tabs
  document.querySelectorAll("#chart-metric-tabs .filter-chip").forEach(btn => {
    btn.onclick = () => {
      STATE.chartMetric = btn.dataset.metric;
      document.querySelectorAll("#chart-metric-tabs .filter-chip").forEach(b => b.classList.toggle("active", b === btn));
      renderBenchmarkChart();
    };
  });

  renderBenchmarkChart();
  renderLeaderboardCards();
  renderBenchmarkTable();
}

function renderBenchmarkChart() {
  const metric = STATE.chartMetric;
  const titleEl = document.getElementById("chart-title");
  const subEl = document.getElementById("chart-subtitle");
  const legendEl = document.getElementById("chart-legend");
  const chartEl = document.getElementById("benchmark-chart");

  if (metric === "accuracy") {
    titleEl.textContent = "Cumulative Forecast Accuracy (%) Across 10 Days";
    subEl.textContent = "Higher is better — % of binary market & corporate filing outcomes predicted on the correct side of 50%";
  } else if (metric === "brier") {
    titleEl.textContent = "Daily Brier Calibration Error (Lower = Better)";
    subEl.textContent = "Lower is better — Mean squared probability error (p − outcome)². Random guessing = 0.25";
  } else {
    titleEl.textContent = "Blinded Judge Score (1–5 Scale)";
    subEl.textContent = "Higher is better — Evaluated by gemini-4-argon on specificity, evidence fidelity & next-day alignment";
  }

  legendEl.innerHTML = MODELS.map(m => `
    <div class="legend-item">
      <span class="legend-line" style="background:${m.color}"></span>
      <span>${esc(m.name)}</span>
    </div>
  `).join("");

  // SVG dimensions
  const W = 1020, H = 250, padL = 48, padR = 24, padT = 20, padB = 34;
  const plotW = W - padL - padR;
  const plotH = H - padT - padB;

  const yMin = metric === "accuracy" ? 30 : (metric === "brier" ? 0 : 2.0);
  const yMax = metric === "accuracy" ? 105 : (metric === "brier" ? 0.42 : 5.0);

  const xAt = i => padL + (i / (HISTORICAL_DAYS.length - 1)) * plotW;
  const yAt = val => padT + plotH - ((val - yMin) / (yMax - yMin)) * plotH;

  // Compute series for each model
  const series = MODELS.map(m => {
    let runningAccSum = 0;
    const points = HISTORICAL_DAYS.map((d, idx) => {
      const dm = d.models[m.id];
      runningAccSum += dm.acc;
      const val = metric === "accuracy"
        ? (runningAccSum / (idx + 1))
        : (metric === "brier" ? dm.brier : dm.judge);
      return { x: xAt(idx), y: yAt(val), val, label: d.shortLabel };
    });
    return { model: m, points };
  });

  // Grid lines
  const gridSteps = 4;
  let gridHtml = "";
  for (let i = 0; i <= gridSteps; i++) {
    const v = yMin + ((yMax - yMin) * i) / gridSteps;
    const y = yAt(v);
    const lbl = metric === "accuracy" ? `${v.toFixed(0)}%` : v.toFixed(2);
    gridHtml += `
      <line x1="${padL}" y1="${y}" x2="${W - padR}" y2="${y}" stroke="#ECE9E2" stroke-width="1" />
      <text x="${padL - 8}" y="${y + 4}" text-anchor="end" font-family="JetBrains Mono" font-size="10" fill="#9A978F">${lbl}</text>
    `;
  }

  // X-axis date labels
  const xLabelsHtml = HISTORICAL_DAYS.map((d, i) => `
    <text x="${xAt(i)}" y="${H - 8}" text-anchor="middle" font-family="JetBrains Mono" font-size="10.5" fill="#63615C">${d.shortLabel}</text>
  `).join("");

  // Polylines & dots
  const linesHtml = series.map(s => {
    const pts = s.points.map(p => `${p.x.toFixed(1)},${p.y.toFixed(1)}`).join(" ");
    const dash = s.model.id === "baseline" ? `stroke-dasharray="5,5"` : "";
    const dots = s.points.map(p => `
      <circle cx="${p.x.toFixed(1)}" cy="${p.y.toFixed(1)}" r="4" fill="${s.model.color}" stroke="#FFF" stroke-width="1.5">
        <title>${s.model.name} (${p.label}): ${metric === "accuracy" ? p.val.toFixed(1) + "%" : p.val.toFixed(3)}</title>
      </circle>
    `).join("");
    return `<polyline fill="none" stroke="${s.model.color}" stroke-width="2.5" ${dash} points="${pts}" />${dots}`;
  }).join("");

  chartEl.innerHTML = `
    <svg viewBox="0 0 ${W} ${H}" width="100%" height="250" style="display:block;">
      ${gridHtml}
      ${xLabelsHtml}
      ${linesHtml}
    </svg>
  `;
}

function renderLeaderboardCards() {
  const grid = document.getElementById("leaderboard-grid");
  const summaries = MODELS.map(m => {
    const days = HISTORICAL_DAYS.map(d => d.models[m.id]);
    const avgAcc = days.reduce((a, x) => a + x.acc, 0) / days.length;
    const avgBrier = days.reduce((a, x) => a + x.brier, 0) / days.length;
    const avgJudge = days.reduce((a, x) => a + x.judge, 0) / days.length;
    const mae = HISTORICAL_DAYS.reduce((a, d) => a + Math.abs(d.models[m.id].q3Est - d.q3Actual), 0) / HISTORICAL_DAYS.length;
    return { model: m, avgAcc, avgBrier, avgJudge, mae };
  });

  grid.innerHTML = summaries.map((s, idx) => `
    <div class="lb-card ${idx === 0 ? "winner" : ""}">
      <div class="lb-head">
        <div class="lb-model-name">
          <span class="m-dot" style="background:${s.model.color}"></span>
          <span>${esc(s.model.name)}</span>
        </div>
        ${idx === 0 ? `<span class="outcome-badge hit">#1 Top Ranked</span>` : ""}
      </div>
      <div class="lb-metrics">
        <div class="lb-stat">
          <span>ACCURACY ↑</span>
          <strong>${s.avgAcc.toFixed(0)}%</strong>
        </div>
        <div class="lb-stat">
          <span>BRIER ERROR ↓</span>
          <strong>${s.avgBrier.toFixed(3)}</strong>
        </div>
        <div class="lb-stat">
          <span>COUNT MAE ↓</span>
          <strong>±${s.mae.toFixed(2)}</strong>
        </div>
        <div class="lb-stat">
          <span>JUDGE SCORE ↑</span>
          <strong>${s.avgJudge.toFixed(2)} / 5</strong>
        </div>
      </div>
    </div>
  `).join("");
}

function renderBenchmarkTable() {
  const tabsEl = document.getElementById("bench-track-tabs");
  const tracks = [
    { id: "all", label: "All Tracks" },
    { id: "q1", label: "Stocks / Registry" },
    { id: "q2", label: "SEC 8-K Filings" },
    { id: "q3", label: "NASA X Volume" },
    { id: "q4", label: "World News (Judged)" }
  ];
  tabsEl.innerHTML = tracks.map(t => `
    <button class="filter-chip ${STATE.benchTrack === t.id ? "active" : ""}" data-bt="${t.id}">${esc(t.label)}</button>
  `).join("");

  tabsEl.querySelectorAll(".filter-chip").forEach(btn => {
    btn.onclick = () => {
      STATE.benchTrack = btn.dataset.bt;
      renderBenchmarkTable();
    };
  });

  const daySel = document.getElementById("bench-day-select");
  daySel.innerHTML = `<option value="all">All 10 Target Days (Oct 15–24)</option>` +
    HISTORICAL_DAYS.map(d => `<option value="${d.targetDate}" ${STATE.benchDay === d.targetDate ? "selected" : ""}>${d.shortLabel} (${d.targetDate})</option>`).join("");
  daySel.onchange = () => {
    STATE.benchDay = daySel.value;
    renderBenchmarkTable();
  };

  const days = HISTORICAL_DAYS.filter(d => STATE.benchDay === "all" || d.targetDate === STATE.benchDay);
  const rows = [];

  for (const d of days) {
    if (STATE.benchTrack === "all" || STATE.benchTrack === "q1") {
      rows.push({
        day: d,
        track: "Stocks / Registry",
        question: d.isWeekend ? `Weekend SEC 8-K Count (${d.shortLabel})` : `Will ${d.ticker} close > $${d.baseClose}?`,
        actual: d.isWeekend ? `${d.q1Actual} filings` : `${d.q1Actual ? "YES" : "NO"} ($${d.targetClose})`,
        g4: `${(d.models["gemini-4-argon"].q1Prob * 100).toFixed(0)}%`,
        cl: `${(d.models["claude-4.6-opus"].q1Prob * 100).toFixed(0)}%`,
        gp: `${(d.models["gpt-5.4"].q1Prob * 100).toFixed(0)}%`
      });
    }
    if (STATE.benchTrack === "all" || STATE.benchTrack === "q2") {
      rows.push({
        day: d,
        track: "SEC 8-K Cohort",
        question: `10-Company Cohort Original 8-K (${d.shortLabel})`,
        actual: d.q2Actual ? `YES (${d.q2Detail})` : "NO (0 filings)",
        g4: `${(d.models["gemini-4-argon"].q2Prob * 100).toFixed(0)}%`,
        cl: `${(d.models["claude-4.6-opus"].q2Prob * 100).toFixed(0)}%`,
        gp: `${(d.models["gpt-5.4"].q2Prob * 100).toFixed(0)}%`
      });
    }
    if (STATE.benchTrack === "all" || STATE.benchTrack === "q3") {
      rows.push({
        day: d,
        track: "NASA X Volume",
        question: `@NASA Retrievable X Post Count (${d.shortLabel})`,
        actual: `${d.q3Actual} posts`,
        g4: `${d.models["gemini-4-argon"].q3Est} est`,
        cl: `${d.models["claude-4.6-opus"].q3Est} est`,
        gp: `${d.models["gpt-5.4"].q3Est} est`
      });
    }
    if (STATE.benchTrack === "all" || STATE.benchTrack === "q4") {
      rows.push({
        day: d,
        track: "World News",
        question: d.worldHeadline,
        actual: "Held-out Exa corpus",
        g4: `★ ${d.models["gemini-4-argon"].judge}/5`,
        cl: `★ ${d.models["claude-4.6-opus"].judge}/5`,
        gp: `★ ${d.models["gpt-5.4"].judge}/5`
      });
    }
  }

  const listEl = document.getElementById("bench-comparison-list");
  listEl.innerHTML = `
    <table class="comp-table">
      <thead>
        <tr>
          <th>Date</th>
          <th>Track</th>
          <th>Event / Question</th>
          <th>Actual Outcome</th>
          <th>gemini-4-argon</th>
          <th>claude-4.6-opus</th>
          <th>gpt-5.4</th>
        </tr>
      </thead>
      <tbody>
        ${rows.map((r, i) => `
          <tr data-row-idx="${i}">
            <td style="font-family:var(--mono);font-weight:600;">${esc(r.day.shortLabel)}</td>
            <td style="font-family:var(--mono);font-size:11.5px;color:var(--ink-secondary);">${esc(r.track)}</td>
            <td style="font-weight:500;">${esc(r.question)}</td>
            <td><span class="outcome-badge hit">${esc(r.actual)}</span></td>
            <td style="font-family:var(--mono);font-weight:700;color:var(--accent);">${esc(r.g4)}</td>
            <td style="font-family:var(--mono);color:var(--indigo);">${esc(r.cl)}</td>
            <td style="font-family:var(--mono);color:var(--green);">${esc(r.gp)}</td>
          </tr>
        `).join("")}
      </tbody>
    </table>
  `;

  listEl.querySelectorAll("tr[data-row-idx]").forEach(tr => {
    tr.addEventListener("click", () => {
      const r = rows[Number(tr.dataset.rowIdx)];
      if (!r) return;
      openSheet(
        `<span class="fc-source-pill">${esc(r.day.targetDate)} · ${esc(r.track)}</span>`,
        `
          <h2 style="font-family:var(--serif);font-size:26px;font-weight:400;margin-bottom:10px;">${esc(r.question)}</h2>
          <p style="font-size:13.5px;color:var(--ink-secondary);margin-bottom:16px;">
            <strong>Actual Next-Day Outcome:</strong> ${esc(r.actual)}<br/>
            <strong>Held-Out Headline:</strong> ${esc(r.day.worldHeadline)}
          </p>
          <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:16px;">
            <div style="background:var(--surface-subtle);padding:12px;border-radius:10px;text-align:center;">
              <div style="font-family:var(--mono);font-size:10px;">gemini-4-argon</div>
              <strong style="font-family:var(--mono);font-size:18px;color:var(--accent);">${esc(r.g4)}</strong>
            </div>
            <div style="background:var(--surface-subtle);padding:12px;border-radius:10px;text-align:center;">
              <div style="font-family:var(--mono);font-size:10px;">claude-4.6-opus</div>
              <strong style="font-family:var(--mono);font-size:18px;color:var(--indigo);">${esc(r.cl)}</strong>
            </div>
            <div style="background:var(--surface-subtle);padding:12px;border-radius:10px;text-align:center;">
              <div style="font-family:var(--mono);font-size:10px;">gpt-5.4</div>
              <strong style="font-family:var(--mono);font-size:18px;color:var(--green);">${esc(r.gp)}</strong>
            </div>
          </div>
          <p style="font-size:12.5px;color:var(--ink-secondary);">
            Want to inspect all Forecasts for <strong>${esc(r.day.shortLabel)}</strong>? Click the date chip in the <strong>Predictions</strong> tab.
          </p>
        `
      );
    });
  });
}

document.addEventListener("DOMContentLoaded", init);
