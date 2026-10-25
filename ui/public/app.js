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
  { id: "gemini-3.1-pro-preview", name: "gemini-3.1-pro", color: "#0E7A5D" },
  { id: "gemini-3.8-flash", name: "gemini-3.8-flash", color: "#4F46E5" },
  { id: "gemini-3.1-flash-lite", name: "gemini-3.1-flash-lite", color: "#D97706" },
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

/* Real 10-Day Multi-Model Gemini Benchmark Dataset Judged by gemini-4-argon (Oct 15 – Oct 24, 2026) */
let HISTORICAL_DAYS = [
  {
    "caseId": "day-2026-10-14",
    "cutoffDate": "2026-10-14",
    "targetDate": "2026-10-15",
    "shortLabel": "Oct 15",
    "isWeekend": false,
    "ticker": "AAPL",
    "baseClose": 342.96,
    "targetClose": 342.0,
    "q1Actual": false,
    "q2Actual": false,
    "q3Actual": 4,
    "judgeSummary": "On October 15, 2026, key world developments included a UN Security Council open debate on the Middle East, France and the UK pressing Russia with new EU sanctions and funding for Ukraine, and major global energy market developments—specifically the IEA announcing a 20M+ barrel diesel release, the US easing curbs on Russian diesel, and Brent crude trading around $105-$106 amid Strait of Hormuz risks. In Japan, Prime Minister Sanae Takaichi appointed Shin Takebe to replace resigned Agriculture Minister Yanagi amid ongoing Diet battles over his budget-cut remarks, the food consumption tax cut bill, and supplementary budget plans. Other notable news included Q3 corporate earnings, reaction to hot US inflation data, major AI research announcements (Meta, OpenAI, Google, Apple), and tropical cyclone updates (Trudy, Rachel, Champi) and WHO health reports (Dengue, Nepal floods, Maldives surveillance).",
    "models": {
      "gemini-4-argon": {
        "q1Prob": 0.51,
        "q1Rationale": "AAPL closed higher over the last two sessions (from 340.97 on Oct 12 to 341.27 on Oct 13, and 342.96 on Oct 14) on rising volume, showing resilience on Oct 14 even as major tech peers (MSFT, NVDA, GOOGL, META) pulled back. However, daily equity direction is near a random walk wit",
        "q2Prob": 0.22,
        "q2Rationale": "2026-10-15 is a Thursday (weekday) during early Q3 2026 earnings season. Overall SEC filing activity is high (171 filings on Oct 14, 242 on Oct 13). In the 10-company cohort, only JPM had 8-K filings over the past week (on Oct 13 for Q3 earnings). Mid-October is slightly ahead of",
        "q3Est": 3.0,
        "q3Interval": [
          1,
          5
        ],
        "q3Rationale": "Over the past 7 days, NASA's observed original X post counts were 5 (Thu Oct 8), 4 (Fri Oct 9), 0 (Sat Oct 10), 1 (Sun Oct 11), 0 (Mon Oct 12, US federal holiday), 2 (Tue Oct 13), and 3 (Wed Oct 14). Excluding the weekend and Monday holiday, normal weekday cou",
        "q4Forecasts": [
          {
            "title": "Japanese House of Representatives Budget Committee Debates",
            "claim": "Japanese political reporting on 2026-10-15 will cover continued extraordinary Diet deliberations and opposition questioning of Prime Minister Sanae Takaichi's cabinet regarding the proposed 1% food consumption tax cut bill and agricultural ",
            "probability": 0.75,
            "rationale": "Multiple pre-cutoff articles from Oct 9-13 detail intense ongoing Diet Budget Committee sessions and opposition scrutiny of PM Takaichi's consumption tax legislation and Minister Yanagi's remarks during the extraordinary"
          },
          {
            "title": "Middle East Conflict and Energy Market Volatility Reporting",
            "claim": "News coverage on 2026-10-15 will feature updates on US-Iran regional tensions, Gulf security following the Riyadh airport attack, or related oil price volatility.",
            "probability": 0.8,
            "rationale": "Pre-cutoff reporting across Al Jazeera, Euronews, Khaleej Times, BBCWorld, and Business Standard highlights active escalation across the Middle East and its ongoing impact on global energy supplies and Brent crude volati"
          }
        ],
        "q5Forecasts": [
          {
            "title": "BBCWorld X Coverage of Geopolitics and US/Middle East News",
            "claim": "BBCWorld will publish at least one post on X during [2026-10-15T00:00:00Z, 2026-10-16T00:00:00Z) covering international geopolitical tensions, US political/economic news, or updates on the Pope's hospitalization.",
            "probability": 0.85,
            "rationale": "BBCWorld posts daily on X in the supplied week, consistently highlighting major ongoing stories including US politics/trade, Middle East tensions, and the Pope's lung surgery."
          },
          {
            "title": "WHO X Posts on Mental Health or Humanitarian Health Crises",
            "claim": "The WHO X account will publish at least one post during [2026-10-15T00:00:00Z, 2026-10-16T00:00:00Z) focused on mental health care, non-communicable diseases, or humanitarian health/famine risks such as in Sudan.",
            "probability": 0.75,
            "rationale": "WHO has maintained a steady cadence of X posts throughout the prior week focusing on mental health lived-experience campaigns and humanitarian health warnings."
          }
        ],
        "brier": 0.1542,
        "acc": 50.0,
        "mae": 1.0,
        "judge": 3.9,
        "judgeWorld": 4.5,
        "judgeSocial": 3.2,
        "judgeNotes": "Strengths: Model_A delivered an outstanding World forecast, accurately pinpointing two of the biggest story clusters in the reference evidence with high specificity: Japanese Diet deliberations regarding PM Takaichi's food consumption tax bill and the agricultural budget controversy (Minister Yanagi's resignation and r"
      },
      "gemini-3.1-pro-preview": {
        "q1Prob": 0.52,
        "q1Rationale": "Stock prices follow a near-random walk on a daily basis with a slight upward drift in broader equity markets. Without specific, predictable catalyst evidence pointing toward a major decline for AAPL on October 15, a neutral-to-slightly-bullish probability of 52% is assigned for a",
        "q2Prob": 0.35,
        "q2Rationale": "October 15 is a Thursday, a high-volume day for SEC filings, and mid-October aligns with the Q3 earnings season (e.g., JPM already reported Q3 results and filed an 8-K on Oct 13). With a cohort of ten mega-cap companies, there is a moderate baseline probability that at least one ",
        "q3Est": 3.0,
        "q3Interval": [
          1,
          6
        ],
        "q3Rationale": "Recent daily publication counts for NASA on X show 5 on Thursday (Oct 8), 4 on Friday, 0 on Monday, 2 on Tuesday, and 3 on Wednesday (Oct 14). Given October 15 is a Thursday, activity is expected to be in line with the recent weekday average of 2 to 5 posts.",
        "q4Forecasts": [
          {
            "title": "Updates on the Pope's Health",
            "claim": "Global news organizations will publish updates on the Pope's condition following his lung surgery.",
            "probability": 0.85,
            "rationale": "BBCWorld reported on Oct 13 that the Pope was admitted to the hospital for surgery to remove a lump on his lung. Major global media will naturally provide follow-up reporting on his post-operative condition."
          },
          {
            "title": "EU's Sweeping Russia Sanctions",
            "claim": "Media outlets will cover the implications or Russian responses to the European Union's newly adopted package of 1,600 sanctions designations.",
            "probability": 0.75,
            "rationale": "An article from Oct 13 quoted the French Foreign Minister detailing 'the biggest raft of sanctions' adopted since the war began, making international reaction highly probable in the following days."
          }
        ],
        "q5Forecasts": [
          {
            "title": "BBCWorld Follow-up on Pope's Surgery",
            "claim": "The BBCWorld X account will post an update regarding the Pope's health, surgery outcome, or recovery.",
            "probability": 0.6,
            "rationale": "Having broken the news of his hospital admission on Oct 13, BBCWorld is highly likely to continue covering this major ongoing story as post-surgery details emerge."
          },
          {
            "title": "NASA Planetary Defense Content",
            "claim": "NASA's social media accounts will post content related to 'Planetary Defenders', near-Earth objects, or asteroid defense exercises.",
            "probability": 0.7,
            "rationale": "NASA published a YouTube video titled 'Planetary Defenders: This Is Not an Exercise' on Oct 14. Social media campaigns for specific initiatives usually involve clustered posting across platforms (e.g., X and YouTube) ove"
          }
        ],
        "brier": 0.1965,
        "acc": 50.0,
        "mae": 1.0,
        "judge": 2.9,
        "judgeWorld": 3.1,
        "judgeSocial": 2.6,
        "judgeNotes": "Strengths: Correctly forecasted follow-up coverage on France and the EU's new Russia sanctions package. Avoided fabricated facts and provided well-structured, falsifiable claims. Misses: High-probability call (0.85) on updates regarding the Pope's lung surgery missed entirely in the reference evidence. While Google unv"
      },
      "gemini-3.8-flash": {
        "q1Prob": 0.52,
        "q1Rationale": "AAPL closed at 342.96 on 2026-10-14, up slightly from 341.27 on 2026-10-13, despite broader tech index weakness. Thursday 2026-10-15 is a standard trading day with typical equity upward drift and moderate tech volatility, keeping directional probability close to neutral with a sl",
        "q2Prob": 0.28,
        "q2Rationale": "Target day 2026-10-15 is a Thursday during Q3 earnings season. While JPM filed earnings 8-Ks on October 13, other cohort members (MSFT, NVDA, AMZN, GOOGL, META, XOM, WMT, NFLX) rarely file mid-week 8-Ks outside scheduled dates. Historical daily 8-K probability for any single 10-f",
        "q3Est": 3.0,
        "q3Interval": [
          1.0,
          5.0
        ],
        "q3Rationale": "NASA's recent daily retrievable X post counts under the specified search contract are 5 (Thu 10/08), 4 (Fri 10/09), 0, 1, 0, 2 (Tue 10/13), and 3 (Wed 10/14). On Thursdays, NASA typically posts at an active weekday pace of 3 to 5 original posts.",
        "q4Forecasts": [
          {
            "title": "National Hurricane Center Simon Advisory Updates",
            "claim": "The National Hurricane Center will continue issuing active tropical cyclone advisories for Hurricane Simon off the west coast of Mexico during October 15, 2026.",
            "probability": 0.88,
            "rationale": "Advisory #26 for Hurricane Simon was active on October 13 drifting offshore west-central Mexico and Baja California Sur, with storms of this track typically remaining active for several subsequent forecast cycles."
          },
          {
            "title": "Japanese Diet Budget Committee Deliberations on Tax Relief",
            "claim": "Japanese parliamentary committees will hold sessions debating the consumption tax cut and economic stimulus bills introduced by the Takaichi cabinet.",
            "probability": 0.75,
            "rationale": "Cabinet approved food consumption tax cut legislation on October 9 and Budget Committee sessions involving Prime Minister Takaichi began intense deliberations on October 13."
          }
        ],
        "q5Forecasts": [
          {
            "title": "NASA Social Media Posts on Earth Science or Astronomy Missions",
            "claim": "The @NASA X account will publish at least one original post detailing planetary science, mission updates, or astronomy imagery during October 15, 2026.",
            "probability": 0.82,
            "rationale": "NASA regularly publishes original multimedia and mission highlights on weekdays, maintaining a cadence of 2-5 posts per weekday over the prior week."
          },
          {
            "title": "WHO Health Advisory Publications",
            "claim": "The @WHO X account will post public health guidance or crisis monitoring updates on October 15, 2026.",
            "probability": 0.78,
            "rationale": "WHO maintains daily social posting regarding global nutrition, humanitarian disease risks, or mental health awareness as evidenced across the observation week."
          }
        ],
        "brier": 0.1744,
        "acc": 50.0,
        "mae": 1.0,
        "judge": 3.0,
        "judgeWorld": 3.2,
        "judgeSocial": 2.8,
        "judgeNotes": "Strengths: Accurately predicted Japanese parliamentary deliberations regarding the Takaichi cabinet's consumption tax cut legislation and economic stimulus/supplementary budget plans. WHO health advisory/monitoring updates (Dengue Situation Update #756, Maldives disease surveillance) also aligned well with the broader "
      },
      "gemini-3.1-flash-lite": {
        "q1Prob": 0.45,
        "q1Rationale": "AAPL closed at 342.96 on 2026-10-14. While the stock has seen significant volatility, the broader market context shows mixed signals with upcoming US CPI data and earnings focus. Without a clear trend catalyst from the pre-cutoff data, a near-coin-flip probability slightly skewed",
        "q2Prob": 0.25,
        "q2Rationale": "The cohort companies (AAPL, MSFT, NVDA, AMZN, GOOGL, META, JPM, XOM, WMT, NFLX) are large-cap entities that file 8-Ks frequently. JPM filed two 8-Ks on 2026-10-13 regarding earnings. While the probability of one of these 10 companies filing on any given business day is non-neglig",
        "q3Est": 2.0,
        "q3Interval": [
          1,
          4
        ],
        "q3Rationale": "NASA's X cadence has been light recently, with 0 to 5 posts observed in the last week. The observed counts were 2 and 3 on the most recent two days, suggesting a continued low but consistent output level.",
        "q4Forecasts": [
          {
            "title": "US CPI Data Release Impact",
            "claim": "Market volatility will increase following the release of US CPI data, with focus on potential shifts in interest rate expectations.",
            "probability": 0.7,
            "rationale": "News reports highlight that market focus has turned explicitly to US CPI and earnings, which are typically volatility-inducing events."
          },
          {
            "title": "Hurricane Simon Impact",
            "claim": "Hurricane Simon will maintain its current path offshore of Mexico, causing limited disruption to land operations but continued monitoring by emergency agencies.",
            "probability": 0.85,
            "rationale": "Advisories indicate the storm is drifting offshore with little change in strength, making significant land impact less likely but keeping the situation active."
          }
        ],
        "q5Forecasts": [
          {
            "title": "Gemini 4 Argon Discussion",
            "claim": "Discussions on X will shift towards technical benchmarks and early use-case testing of the newly released Gemini 4 Argon model.",
            "probability": 0.75,
            "rationale": "The announcement of Gemini 4 Argon on October 13 creates immediate social momentum for evaluation by the developer community."
          },
          {
            "title": "HYBE CINE FEST Anticipation",
            "claim": "Social accounts will increase frequency of posts related to concert film teasers and ticket sales as the late October festival approaches.",
            "probability": 0.6,
            "rationale": "With the festival starting on October 24, pre-event engagement in the social cohort is expected to rise as marketing ramps up."
          }
        ],
        "brier": 0.1325,
        "acc": 100.0,
        "mae": 2.0,
        "judge": 2.6,
        "judgeWorld": 3.0,
        "judgeSocial": 2.2,
        "judgeNotes": "Strengths: Correctly anticipated market reaction to hot US inflation/CPI data and bond/currency movements ('Dollar recedes from 18-month high as bond rally tempers impact of hot inflation data'). Misses: Overconfident (0.85) on Hurricane Simon, which was absent from next-day evidence. Social forecasts were vague, lacke"
      },
      "baseline": {
        "q1Prob": 0.5,
        "q2Prob": 0.3,
        "q3Est": 1.6,
        "brier": 0.17,
        "acc": 50.0,
        "mae": 2.4,
        "judge": 2.5
      }
    }
  },
  {
    "caseId": "day-2026-10-15",
    "cutoffDate": "2026-10-15",
    "targetDate": "2026-10-16",
    "shortLabel": "Oct 16",
    "isWeekend": false,
    "ticker": "MSFT",
    "baseClose": 539.44,
    "targetClose": 529.05,
    "q1Actual": false,
    "q2Actual": false,
    "q3Actual": 2,
    "judgeSummary": "On October 16, 2026, key world developments included the US issuing Executive Order 14436 to implement the Lindsey O. Graham Sanctioning Russia and Iran Act of 2026, a UN Security Council briefing on the intensifying war in Sudan where the US pressed for a humanitarian truce, and intense questioning of Japanese Prime Minister Sanae Takaichi in the Upper House Budget Committee following the dismissal of former Agriculture Minister Yana. Economically, reports highlighted energy-driven headline inflation, spiking oil shipping costs, and rising diesel indicators due to the Middle East conflict and Hormuz disruptions, alongside major AI model releases (Meta's Muse Spark Open, Reflection's Beam, Jais 3). No social media posts from X or YouTube were captured in the held-out reference evidence for this window.",
    "models": {
      "gemini-4-argon": {
        "q1Prob": 0.51,
        "q1Rationale": "Target date 2026-10-16 is a Friday (regular trading day). MSFT rebounded strongly on Thursday 2026-10-15 from 533.69 to 539.44 (+1.08%) after dropping the prior day. Daily equity returns are near a 50/50 random walk with a slight upward drift.",
        "q2Prob": 0.16,
        "q2Rationale": "Target date 2026-10-16 is a Friday, an active SEC filing day (the previous Friday 2026-10-09 had 151 total filings). However, within the 10-company cohort over the past week, only JPM filed an 8-K (on 2026-10-13 for Q3 earnings). Major tech and retail earnings for this cohort typ",
        "q3Est": 3.0,
        "q3Interval": [
          1,
          5
        ],
        "q3Rationale": "NASA's observed original X post counts on recent weekdays were 4 (Fri Oct 9), 0 (Mon Oct 12, Columbus Day holiday), 2 (Tue Oct 13), 3 (Wed Oct 14), and 4 (Thu Oct 15). For Friday Oct 16, a point estimate of 3 posts with an 80% interval of [1, 5] aligns well wi",
        "q4Forecasts": [
          {
            "title": "Pre-Deadline Reporting on US Sanctions Against Russia and Iran",
            "claim": "News coverage on 2026-10-16 will address the Trump administration's preparations or congressional scrutiny ahead of the October 18 deadline under the Lindsey O. Graham Sanctioning Russia and Iran Act.",
            "probability": 0.6,
            "rationale": "A 2026-10-14 article highlights that Congress is closely watching how the administration implements the new sanctions law as the October 18 deadline approaches."
          },
          {
            "title": "Middle East Energy Supply Disruption and Fuel Inflation Coverage",
            "claim": "Economic and geopolitical reporting on 2026-10-16 will feature continued analysis of Middle East war disruptions to energy supplies, rising diesel/fuel costs, or Q4 commodity price pressures.",
            "probability": 0.7,
            "rationale": "Multiple articles from Oct 11-14 highlight soaring diesel prices (+75%), record Q4 commodity price forecasts, and energy supply disruptions stemming from the ongoing Middle East conflict."
          }
        ],
        "q5Forecasts": [
          {
            "title": "BBCWorld Coverage of US Election Security or Domestic Politics",
            "claim": "BBCWorld will publish at least one X post on 2026-10-16 concerning US pre-midterm politics or election security (such as follow-ups on suspicious letters sent to election offices).",
            "probability": 0.65,
            "rationale": "BBCWorld posted late on 2026-10-15 about letters with suspicious substances sent to US election offices and has maintained daily coverage of US political developments."
          },
          {
            "title": "WHO Mental Health or Humanitarian Crisis Advocacy on X",
            "claim": "The WHO X account will publish at least one post on 2026-10-16 focusing on mental health care, anti-stigma advocacy, or humanitarian health crises such as famine risk in Sudan.",
            "probability": 0.7,
            "rationale": "WHO has posted nearly every day during the supplied week with personal testimonials on mental health care reform, anti-stigma language, and humanitarian health warnings."
          }
        ],
        "brier": 0.1429,
        "acc": 50.0,
        "mae": 1.0,
        "judge": 4.4,
        "judgeWorld": 4.8,
        "judgeSocial": 3.5,
        "judgeNotes": "Strongest world forecast performance, scoring 3-for-3 on specific, falsifiable next-day developments: the implementation of the Lindsey O. Graham Sanctioning Russia and Iran Act (EO 14436), continued reporting on Middle East energy disruptions driving diesel and shipping inflation, and Japanese Diet Budget Committee qu"
      },
      "gemini-3.1-pro-preview": {
        "q1Prob": 0.52,
        "q1Rationale": "The target date is a Friday. Market drift for large-cap tech stocks like MSFT is historically slightly positive, but macroeconomic uncertainties and energy sector pressures keep the daily directional probability close to a coin toss. There are no major predetermined MSFT catalyst",
        "q2Prob": 0.45,
        "q2Rationale": "The target window is a Friday, which is a common day for companies to file 8-Ks to disclose material events before the weekend. In a cohort of 10 large-cap companies, there is a moderate baseline probability that at least one will have a reportable event, though overall filing vo",
        "q3Est": 4.0,
        "q3Interval": [
          1,
          7
        ],
        "q3Rationale": "NASA's X account has posted between 2 and 4 original tweets on recent weekdays (e.g., 4 on the previous Friday, 2 on Tuesday, 3 on Wednesday, 4 on Thursday). A point estimate of 4 is most appropriate for a Friday.",
        "q4Forecasts": [
          {
            "title": "Hurricane Simon Advisories",
            "claim": "The US National Hurricane Center will issue at least one update or advisory regarding Hurricane Simon in the Eastern Pacific.",
            "probability": 0.85,
            "rationale": "Hurricane Simon was actively being monitored off the coast of Mexico on October 13, and storm systems of this nature typically warrant multi-day advisories until they fully dissipate."
          },
          {
            "title": "US Election Security Investigations",
            "claim": "US media or authorities will release further information regarding the investigation into 'suspicious substances' sent to US election offices.",
            "probability": 0.75,
            "rationale": "BBCWorld reported on October 15 that suspicious letters were sent to election offices. This is a high-profile security event close to an election, likely prompting rapid updates or FBI/DOJ statements."
          }
        ],
        "q5Forecasts": [
          {
            "title": "BBCWorld on the US Election",
            "claim": "The BBCWorld X account will publish at least one post covering the US presidential election, candidates, or election security.",
            "probability": 0.8,
            "rationale": "With the US election rapidly approaching and recent coverage of suspicious letters at election offices, BBCWorld is highly likely to continue covering US political developments."
          },
          {
            "title": "WHO on Humanitarian Crises",
            "claim": "The WHO X account will post about severe health crises, malnutrition, or conflict-related medical emergencies, such as the situation in Sudan.",
            "probability": 0.65,
            "rationale": "The WHO recently highlighted the alarming risk of famine and disease in Sudan. They frequently maintain ongoing campaigns regarding major humanitarian emergencies."
          }
        ],
        "brier": 0.2365,
        "acc": 50.0,
        "mae": 2.0,
        "judge": 2.9,
        "judgeWorld": 2.9,
        "judgeSocial": 3.0,
        "judgeNotes": "Correctly anticipated Japanese parliamentary fallout over Agriculture Minister Yana (0.70), which was a major story in the Diet on Oct 16. However, missed on Hurricane Simon advisories (0.85, as NHC advisories on Oct 16 were for Post-Tropical Cyclone Trudy and Tropical Storm Rachel) and US election security investigati"
      },
      "gemini-3.8-flash": {
        "q1Prob": 0.51,
        "q1Rationale": "MSFT closed at $539.44 on 2026-10-15, recovering moderately from $533.69 on Oct 14 after a drop from $543.45 on Oct 13. Macro tech conditions show slight rebound momentum across peers (GOOGL and META gained slightly on Oct 15). Daily equity direction remains close to a random wal",
        "q2Prob": 0.22,
        "q2Rationale": "The cohort consists of 10 large-cap corporations (AAPL, MSFT, NVDA, AMZN, GOOGL, META, JPM, XOM, WMT, NFLX). Friday October 16 is a regular SEC filing business day. Earnings season has commenced (JPM reported on Oct 13), but most of the remaining 9 companies report later in Octob",
        "q3Est": 3.2,
        "q3Interval": [
          1.0,
          5.0
        ],
        "q3Rationale": "NASA's retrievable non-retweet original X posts for recent weekdays have been: Friday Oct 9: 4, Monday Oct 12: 0, Tuesday Oct 13: 2, Wednesday Oct 14: 3, Thursday Oct 15: 4. For Friday Oct 16, a cadence of around 3 to 4 posts is expected, with an 80% confidenc",
        "q4Forecasts": [
          {
            "title": "US Russia Sanctions Preparations Ahead of Oct 18 Deadline",
            "claim": "US congressional and administration activity will report further preparations or oversight developments concerning implementation of the Graham Sanctioning Russia and Iran Act ahead of the Oct 18 statutory deadline.",
            "probability": 0.65,
            "rationale": "Reporting on Oct 14 highlighted that Congress is actively awaiting implementation by the Trump administration with an Oct 18 deadline approaching amid rising tensions and parallel EU sanctions packages."
          },
          {
            "title": "Continued Scrutiny of Minister Yana in Japan Diet",
            "claim": "Japanese news media and parliamentary reporting on Oct 16 will continue to cover Prime Minister Takaichi's cabinet pressure or potential personnel action regarding Agriculture Minister Yana.",
            "probability": 0.7,
            "rationale": "Reports on Oct 13 and Oct 14 showed intense Diet questioning and media reports that Prime Minister Sanae Takaichi was weighing a decision on Minister Yana's status."
          }
        ],
        "q5Forecasts": [
          {
            "title": "WHO Social Outreach on Global Health and Mental Health/Nutrition",
            "claim": "WHO official X account will publish at least one post focused on communicable diseases, public nutrition/malnutrition crises (such as Sudan), or mental health initiatives during the target window.",
            "probability": 0.8,
            "rationale": "WHO maintained a steady daily posting cadence from Oct 9 through Oct 13 covering mental health, obesity stigma, and IPC famine risk warnings in Sudan."
          },
          {
            "title": "BBCWorld Reporting on Middle East Conflict and Energy Impact",
            "claim": "BBCWorld X account will publish multiple posts concerning Middle East geopolitical tensions, strikes, or regional conflicts during Oct 16.",
            "probability": 0.85,
            "rationale": "BBCWorld has maintained continuous coverage of ongoing Middle Eastern escalations, regional strikes, and related international diplomacy throughout the week."
          }
        ],
        "brier": 0.1542,
        "acc": 50.0,
        "mae": 1.2,
        "judge": 3.9,
        "judgeWorld": 4.3,
        "judgeSocial": 3.3,
        "judgeNotes": "Delivered two accurate, well-calibrated world forecasts: administration action on the Graham Sanctioning Russia and Iran Act ahead of the Oct 18 deadline (0.65) and continued Japanese Diet scrutiny of PM Takaichi over Minister Yana (0.70). Slightly less breadth in Q4 than Model_A (2 predictions vs 3, missing the energy"
      },
      "gemini-3.1-flash-lite": {
        "q1Prob": 0.55,
        "q1Rationale": "MSFT closed at 539.44 on Oct 15th, recovering from a drop on the 14th. Given the high volatility in tech and recent strong performance in other sectors, a moderate probability of continued momentum is assigned.",
        "q2Prob": 0.35,
        "q2Rationale": "While JPM filed multiple 8-Ks on Oct 13th for earnings, the cohort companies have high activity. The probability of at least one of these 10 major firms filing an 8-K on a typical business day remains significant.",
        "q3Est": 3.0,
        "q3Interval": [
          1,
          5
        ],
        "q3Rationale": "NASA's posting cadence is low but steady (observed 3-4 posts daily recently). Based on the 24-hour window, 3 posts is a realistic expectation.",
        "q4Forecasts": [
          {
            "title": "Japan Ministerial Cabinet Stability",
            "claim": "Prime Minister Sanae Takaichi will announce the retention or removal of Minister Yana following the budget-cut controversy reported on Oct 14th.",
            "probability": 0.85,
            "rationale": "News reports indicate a decision on Minister Yana's fate was expected by Oct 14-15; a formal announcement is imminent."
          },
          {
            "title": "US Russia Sanctions Law Implementation",
            "claim": "The Trump administration will issue preliminary guidance or statements regarding the implementation of the Lindsey O. Graham Sanctioning Russia and Iran Act ahead of the Oct 18 deadline.",
            "probability": 0.7,
            "rationale": "Congress is monitoring the administration's progress closely, making official communication likely as the deadline approaches."
          }
        ],
        "q5Forecasts": [
          {
            "title": "NASA Engagement on Planetary Defense",
            "claim": "NASA will publish at least one follow-up post or video content regarding the 'Planetary Defenders' campaign.",
            "probability": 0.6,
            "rationale": "Following the Oct 14 release of 'Planetary Defenders: This Is Not an Exercise', further engagement on this theme is expected."
          },
          {
            "title": "BBCWorld Coverage of Election Threats",
            "claim": "BBCWorld will provide an update or follow-up on the 'suspicious substances' sent to US election offices.",
            "probability": 0.75,
            "rationale": "Given the severity of the Oct 15 report and its proximity to the election, continued coverage is highly probable."
          }
        ],
        "brier": 0.2125,
        "acc": 50.0,
        "mae": 1.0,
        "judge": 3.7,
        "judgeWorld": 4.1,
        "judgeSocial": 3.1,
        "judgeNotes": "Directly hit the Trump administration's official action implementing the Lindsey O. Graham Sanctioning Russia and Iran Act (0.70). Also correctly identified the Minister Yana controversy (0.85), though framed it slightly behind the curve as an upcoming announcement of retention/removal whereas Yana had just been replac"
      },
      "baseline": {
        "q1Prob": 0.5,
        "q2Prob": 0.3,
        "q3Est": 1.6,
        "brier": 0.17,
        "acc": 50.0,
        "mae": 0.4,
        "judge": 2.5
      }
    }
  },
  {
    "caseId": "day-2026-10-16",
    "cutoffDate": "2026-10-16",
    "targetDate": "2026-10-17",
    "shortLabel": "Oct 17",
    "isWeekend": true,
    "ticker": "WEEKEND 8-K",
    "baseClose": null,
    "targetClose": null,
    "q1Actual": 1,
    "q2Actual": false,
    "q3Actual": 0,
    "judgeSummary": "On October 17, 2026, key world developments centered on U.S. President Donald Trump signing an executive order waiving several Russia sanctions under the Lindsey O. Graham Act just ahead of the October 18 deadline—sparking backlash from Ukrainian President Zelenskyy and lawmakers while giving India room to retain discounted Russian oil. In the Eastern Pacific, Hurricane Trudy strengthened to a Category 2 storm approaching Mexico's coast, prompting active NHC advisories (#19) and emergency preparations in Colima and Michoacán. In Japan, political coverage focused on the aftermath of former Minister Kazuo Yana's resignation under Prime Minister Sanae Takaichi's cabinet and upcoming Diet deliberations on food consumption tax cuts. Other notable stories included persistent Middle East oil supply tensions, Q3 corporate earnings, and major AI model and agent releases from Microsoft, Apple, Google, and Sakana AI. Note that the held-out reference evidence contained news articles only and no social media posts.",
    "models": {
      "gemini-4-argon": {
        "q1Prob": null,
        "q1Rationale": "The target window [2026-10-17T00:00:00Z, 2026-10-18T00:00:00Z) falls on a Saturday, when SEC EDGAR does not accept filings (or weekend acceptance counts are low-entropy controls marked not_applicable).",
        "q2Prob": 0.05,
        "q2Rationale": "The target 24-hour window is Saturday, October 17, 2026. The SEC EDGAR system does not accept corporate Form 8-K filings over the weekend, making the probability of an accepted original 8-K from the 10-company cohort minimal (at the 0.05 floor).",
        "q3Est": 1.0,
        "q3Interval": [
          0.0,
          3.0
        ],
        "q3Rationale": "Over the preceding 7 days (2026-10-10 to 2026-10-16), NASA's observed original X post counts were 0, 1, 0, 2, 3, 4, and 2 (mean ~1.71). Noticeably, the prior weekend days (Saturday Oct 10 and Sunday Oct 11) had lower activity (0 and 1 post, respectively). Beca",
        "q4Forecasts": [
          {
            "title": "U.S. Sanctions Deadline on Russia and Iran",
            "claim": "New reporting or official statements will address the Trump administration's preparations or actions regarding the Lindsey O. Graham Sanctioning Russia and Iran Act ahead of its October 18 implementation deadline.",
            "probability": 0.65,
            "rationale": "Pre-cutoff news from October 14 explicitly highlights that Congress is closely watching the administration as the October 18 deadline nears to begin imposing sanctions under the Act."
          },
          {
            "title": "Eastern Pacific Tropical Cyclone Trudy Advisories",
            "claim": "The U.S. National Hurricane Center (NHC) will issue public advisories tracking Tropical Storm / Hurricane Trudy in the Eastern Pacific during the target window.",
            "probability": 0.75,
            "rationale": "Pre-cutoff data includes NHC advisory records for Hurricane/Cyclone Trudy active in mid-October 2026, making continued storm tracking and advisories on October 17 highly likely."
          }
        ],
        "q5Forecasts": [
          {
            "title": "BBCWorld Coverage of Middle East and Ukraine Conflicts",
            "claim": "BBCWorld will publish at least one post on X covering either the ongoing Middle East conflict (such as tensions following the Riyadh airport attack or Iran/Israel developments) or Ukraine's strikes on Russian oil infrastructure.",
            "probability": 0.75,
            "rationale": "BBCWorld's recent X feed consistently posts daily international conflict updates, specifically highlighting the Riyadh airport attack and Ukrainian strikes on Russian oil refineries during the prior week."
          },
          {
            "title": "WHO Mental Health and Humanitarian Crisis Posts",
            "claim": "The World Health Organization (@WHO) will publish at least one X post focusing on either community-based mental health care or the public health and famine crisis in Sudan.",
            "probability": 0.65,
            "rationale": "WHO's recent X posts in the supplied week heavily feature testimonies on mental health care de-institutionalization and warnings regarding rising famine and disease risks in Sudan."
          }
        ],
        "brier": 0.0025,
        "acc": 100.0,
        "mae": 1.0,
        "judge": 4.1,
        "judgeWorld": 4.5,
        "judgeSocial": 3.5,
        "judgeNotes": "Model_A delivered the strongest world forecast set. It accurately predicted new reporting and official actions regarding the Lindsey O. Graham Sanctioning Russia and Iran Act ahead of its October 18 deadline (0.65) without wrongly assuming the sanctions would be enforced (Trump waived them). It also nailed the continua"
      },
      "gemini-3.1-pro-preview": {
        "q1Prob": null,
        "q1Rationale": "The target window corresponds to Saturday, October 17, 2026. Because the SEC EDGAR system is generally closed for regular filing processing over the weekend, the acceptance count will be functionally zero or strictly limited to administrative anomalies.",
        "q2Prob": 0.05,
        "q2Rationale": "As October 17, 2026 is a Saturday, the SEC does not typically accept or process standard original Form 8-K filings. The likelihood of any company in the cohort filing an emergency or non-standard weekend 8-K is extremely low.",
        "q3Est": 1.0,
        "q3Interval": [
          0,
          2
        ],
        "q3Rationale": "The target window falls on a Saturday. Based on the previous weekend in the dataset (October 10-11), NASA posted 0 times on Saturday and 1 time on Sunday. Weekday volumes hover around 2-4 posts, but weekend activity sharply declines.",
        "q4Forecasts": [
          {
            "title": "No Active NHC Advisories for Cyclone Trudy",
            "claim": "The U.S. National Hurricane Center will not issue a new active tropical cyclone advisory for Trudy during the target 24-hour window.",
            "probability": 0.95,
            "rationale": "Recent provided public advisories indicate that Trudy has already become a remnant low, and the NHC declared their advisory was the final one for the system."
          },
          {
            "title": "US Russia/Iran Sanctions Act Deadline Coverage",
            "claim": "U.S. or international news outlets will report on the impending October 18 deadline for the Trump administration to implement the Lindsey O. Graham Sanctioning Russia and Iran Act.",
            "probability": 0.75,
            "rationale": "The target date of October 17 is the day immediately prior to the closely watched October 18 implementation deadline highlighted in recent news."
          }
        ],
        "q5Forecasts": [
          {
            "title": "Low NASA X Weekend Posting Volume",
            "claim": "NASA's official X account will publish two or fewer original, retrievable posts during the target window.",
            "probability": 0.85,
            "rationale": "Historical data provided for the previous weekend shows a significant drop in X engagement by NASA (0 posts on Saturday, 1 on Sunday), making a high-volume posting day highly unlikely."
          },
          {
            "title": "BBCWorld US Political Coverage",
            "claim": "The BBCWorld X account will post at least one news item regarding U.S. politics, the upcoming U.S. election, or Donald Trump.",
            "probability": 0.7,
            "rationale": "BBCWorld's recent X feed heavily features U.S. domestic news, including election security and voter demographics (such as ranchers supporting Trump), which is expected to persist as the U.S. election approaches."
          }
        ],
        "brier": 0.0025,
        "acc": 100.0,
        "mae": 1.0,
        "judge": 3.4,
        "judgeWorld": 3.4,
        "judgeSocial": 3.5,
        "judgeNotes": "Model_B scored two strong hits in its world forecasts: accurately predicting coverage of the October 18 Graham Act sanctions deadline (0.75) and specifically forecasting Japanese media coverage of the fallout from Minister Yana's resignation under PM Takaichi (0.85), which directly matched TBS News Dig reporting. Howev"
      },
      "gemini-3.8-flash": {
        "q1Prob": null,
        "q1Rationale": "The target window [2026-10-17T00:00:00Z, 2026-10-18T00:00:00Z) falls entirely on a Saturday (weekend). Under the benchmark guidelines, weekend targets for registry 8-K counts are non-applicable controls; therefore q1_probability is null.",
        "q2Prob": 0.05,
        "q2Rationale": "The target 24h interval is Saturday, October 17, 2026 UTC. SEC EDGAR acceptance of original Form 8-K filings on weekends is extraordinarily rare and virtually non-existent for mega-cap corporate cohorts (AAPL, MSFT, NVDA, AMZN, GOOGL, META, JPM, XOM, WMT, NFLX) absent an emergenc",
        "q3Est": 1.0,
        "q3Interval": [
          0.0,
          3.0
        ],
        "q3Rationale": "Target day is Saturday. Over the previous weekend (Saturday 2026-10-10 and Sunday 2026-10-11), NASA posted 0 and 1 retrievable original tweets respectively, compared to 2 to 4 on weekdays. A point estimate of 1 with an 80% interval of [0, 3] reflects the typic",
        "q4Forecasts": [
          {
            "title": "National Hurricane Center Trudy Advisories",
            "claim": "The National Hurricane Center will continue issuing tracking and public advisories on Post-Tropical Cyclone / Tropical Cyclone Trudy during October 17, 2026.",
            "probability": 0.9,
            "rationale": "Pre-cutoff National Hurricane Center records confirm active tracking of Post-Tropical Cyclone Trudy with ongoing advisory series."
          },
          {
            "title": "Brazilian Presidential Campaign Debates",
            "claim": "Brazilian news reporting will continue to highlight economic and fiscal divergences between Flavio Bolsonaro and President Lula during October 17, 2026.",
            "probability": 0.85,
            "rationale": "Pre-cutoff Brazilian reporting highlights intensive election coverage comparing economic and environmental platforms between Flavio Bolsonaro and Lula leading up to late October 2026."
          }
        ],
        "q5Forecasts": [
          {
            "title": "BBC World Coverage of Middle East Conflict",
            "claim": "BBC World's official X feed will publish at least one report on Middle Eastern geopolitical or conflict developments on October 17, 2026.",
            "probability": 0.88,
            "rationale": "BBCWorld has maintained regular daily reporting on Middle East regional conflict developments throughout the week."
          },
          {
            "title": "WHO Mental Health and Public Health Messaging",
            "claim": "The World Health Organization (WHO) official X account will post updates related to public health, global disease alerts, or humanitarian health crises on October 17, 2026.",
            "probability": 0.8,
            "rationale": "The WHO account consistently maintains daily posting activity focused on health equity, famine warnings, and mental health programs across both weekdays and weekends."
          }
        ],
        "brier": 0.0025,
        "acc": 100.0,
        "mae": 1.0,
        "judge": 3.4,
        "judgeWorld": 3.5,
        "judgeSocial": 3.2,
        "judgeNotes": "Model_C only provided two forecasts per category instead of three. In its world forecasts, it accurately predicted with high confidence (0.90) that the NHC would continue issuing public advisories on Cyclone Trudy on October 17. Its second forecast on Brazilian presidential campaign debates between Flavio Bolsonaro and"
      },
      "gemini-3.1-flash-lite": {
        "q1Prob": null,
        "q1Rationale": "The target window of [2026-10-17T00:00:00Z, 2026-10-18T00:00:00Z) corresponds to a weekend (Saturday), making Q1 not applicable.",
        "q2Prob": 0.05,
        "q2Rationale": "Large-cap companies in the cohort (AAPL, MSFT, etc.) rarely file original Form 8-K reports on Saturdays due to SEC processing and internal corporate compliance schedules, resulting in a very low base rate for weekend filings.",
        "q3Est": 1.0,
        "q3Interval": [
          0,
          2
        ],
        "q3Rationale": "NASA's recent activity on X has been sparse, typically averaging 1-2 posts per day. Given that weekends often see reduced activity, an estimate of 1 post is statistically grounded.",
        "q4Forecasts": [
          {
            "title": "Implementation of Russian Sanctions",
            "claim": "The US administration will confirm the commencement of new sanctions under the Lindsey O. Graham Sanctioning Russia and Iran Act by the Oct 18 deadline.",
            "probability": 0.75,
            "rationale": "The pre-cutoff news indicates an October 18 deadline for the administration to begin imposing these sanctions, and Congress is actively monitoring the situation."
          },
          {
            "title": "Japanese Political Developments",
            "claim": "No major cabinet changes or resignations occur in Prime Minister Takaichi's administration on Saturday, following the recent resignation of Minister Yana.",
            "probability": 0.8,
            "rationale": "The recent resignation of Minister Yana and the appointment of his successor have already been processed as of October 15-16, creating a temporary lull in cabinet-level instability."
          }
        ],
        "q5Forecasts": [
          {
            "title": "NASA Engagement Cadence",
            "claim": "NASA's social media accounts will post at least once about upcoming public aerospace events or educational outreach.",
            "probability": 0.6,
            "rationale": "NASA's recent content (e.g., the Oct 16 post about the MAX POWER expo) shows a consistent pattern of promoting events and community-facing activities."
          },
          {
            "title": "WHO Content Focus",
            "claim": "The WHO account will continue posting advocacy-focused content related to global health crises or mental health advocacy.",
            "probability": 0.7,
            "rationale": "The WHO account has demonstrated a stable, recurring narrative focused on lived experience, mental health, and humanitarian crises in Sudan throughout the week."
          }
        ],
        "brier": 0.0025,
        "acc": 100.0,
        "mae": 1.0,
        "judge": 2.6,
        "judgeWorld": 2.3,
        "judgeSocial": 3.0,
        "judgeNotes": "Model_D provided only two forecasts per category and missed on its primary world claim. Unlike Model_A and Model_B, which framed their Graham Act predictions around deadline reporting or actions, Model_D specifically predicted (0.75) that the US administration would confirm the commencement of new sanctions; instead, T"
      },
      "baseline": {
        "q1Prob": null,
        "q2Prob": 0.3,
        "q3Est": 1.6,
        "brier": 0.09,
        "acc": 100.0,
        "mae": 1.6,
        "judge": 2.5
      }
    }
  },
  {
    "caseId": "day-2026-10-17",
    "cutoffDate": "2026-10-17",
    "targetDate": "2026-10-18",
    "shortLabel": "Oct 18",
    "isWeekend": true,
    "ticker": "WEEKEND 8-K",
    "baseClose": null,
    "targetClose": null,
    "q1Actual": 0,
    "q2Actual": false,
    "q3Actual": 0,
    "judgeSummary": "On October 18, 2026, world news was dominated by the Trump administration's decision to issue a 60-day pause/waiver on Russian economic sanctions (defended by Secretary of State Marco Rubio and criticized by Congress and Ukrainian officials), alongside massive Ukrainian drone strikes hitting Russian oil facilities in St. Petersburg. Global economic coverage focused heavily on soaring energy prices, stagflation risks in the US, European leaders demanding joint action on energy costs, and previews of the Jio Platforms IPO in India. In weather and disasters, the NHC issued advisories on weakening Tropical Cyclone Trudy while Super Typhoon Champi strengthened in the Western Pacific. Political coverage also featured Brazil's presidential election campaign between Lula and Flávio Bolsonaro.",
    "models": {
      "gemini-4-argon": {
        "q1Prob": null,
        "q1Rationale": "The target window [2026-10-18T00:00:00Z, 2026-10-19T00:00:00Z) is a Sunday (weekend), during which the SEC EDGAR system does not accept filings, making Q1 not applicable.",
        "q2Prob": 0.05,
        "q2Rationale": "The target 24-hour window falls entirely on Sunday, October 18, 2026. SEC EDGAR does not process or accept filings on Sundays (as confirmed by the 0 count on Sunday, 2026-10-11, and only 1 across the entire index on Saturday, 2026-10-17). Therefore, the probability that any of th",
        "q3Est": 1.0,
        "q3Interval": [
          0,
          2
        ],
        "q3Rationale": "Over the past 7 days (2026-10-11 to 2026-10-17), NASA's retrievable original X post counts were 1, 0, 2, 3, 4, 2, and 0 (mean ~1.71, median 2). Weekend activity is notably lower, with 1 post on the prior Sunday (Oct 11) and 0 on Saturday (Oct 17). Thus, a poin",
        "q4Forecasts": [
          {
            "title": "Implementation of Sanctions Under the Lindsey O. Graham Sanctioning Russia and Iran Act",
            "claim": "On October 18, 2026, U.S. government officials, members of Congress, or major news outlets will report on or react to the October 18 deadline for imposing new sanctions under the Lindsey O. Graham Sanctioning Russia and Iran Act.",
            "probability": 0.65,
            "rationale": "Pre-cutoff reporting from October 14 ('Congress Awaits Implementation of New Russia Sanctions Law') explicitly notes that October 18 is the statutory deadline to start imposing sanctions under the Lindsey O. Graham Sanct"
          },
          {
            "title": "Coverage of Brazil's Presidential Runoff Election and Results",
            "claim": "International and Brazilian media will report on voting operations, turnout, or official Superior Electoral Court (TSE) results for the Brazilian presidential election between Lula and Flávio on Sunday, October 18, 2026.",
            "probability": 0.6,
            "rationale": "Multiple pre-cutoff articles from Folha, R7, and Reuters ('Take Five: Earnings, an election and an MSCI headache') highlight the pivotal Brazilian election involving Lula and Flávio taking place over this weekend, with T"
          }
        ],
        "q5Forecasts": [
          {
            "title": "BBCWorld X Coverage of the Russia-Ukraine Conflict and Energy Infrastructure Strikes",
            "claim": "The @BBCWorld X account will publish at least one post during [2026-10-18T00:00:00Z, 2026-10-19T00:00:00Z) regarding the Russia-Ukraine war, specifically touching on Ukrainian strikes on Russian oil refineries, EU/US sanctions, or diplomati",
            "probability": 0.65,
            "rationale": "BBCWorld posted multiple times on Oct 15 and Oct 16 regarding Zelensky restarting strikes on Russian oil refineries and rallying EU support amid U.S. diplomatic friction, alongside the Oct 18 U.S. Russia sanctions deadli"
          },
          {
            "title": "BBCWorld X Coverage of Middle East Conflict and Energy/Economic Fallout",
            "claim": "The @BBCWorld X account will post at least one update on October 18, 2026 concerning the ongoing Middle East conflict, regional security incidents, or its impact on global energy supplies.",
            "probability": 0.6,
            "rationale": "BBCWorld and multiple news sources in the pre-cutoff window heavily covered the Middle East conflict (including the Riyadh airport/Aramco attacks, IMF warnings on regional war economic shocks, and Iran FM statements)."
          }
        ],
        "brier": 0.0025,
        "acc": 100.0,
        "mae": 1.0,
        "judge": 4.3,
        "judgeWorld": 4.7,
        "judgeSocial": 3.8,
        "judgeNotes": "Model A delivered an outstanding World forecast, hitting all three of its specific, well-calibrated predictions: the October 18 US sanctions action/reaction regarding Russia, NHC advisories on Tropical Cyclone Trudy, and coverage of Brazil's election between Lula and Flávio (though slightly mischaracterizing the Oct 18"
      },
      "gemini-3.1-pro-preview": {
        "q1Prob": null,
        "q1Rationale": "The target window falls on a weekend (Sunday, October 18, 2026). The SEC EDGAR system does not normally process or accept regular original 8-K filings on weekends, making this a low-entropy control question.",
        "q2Prob": 0.05,
        "q2Rationale": "Because the target window spans a Sunday, the SEC EDGAR system will be closed for normal business, making it highly improbable for any of the cohort companies to have an 8-K accepted.",
        "q3Est": 1.0,
        "q3Interval": [
          0,
          2
        ],
        "q3Rationale": "NASA's X publication volume is typically lower on weekends. The previous Sunday (Oct 11) saw exactly 1 post, and the day prior to the target window (Saturday, Oct 17) saw 0 posts. A low volume of 0 to 2 posts is expected.",
        "q4Forecasts": [
          {
            "title": "Russia Sanctions Act Deadline",
            "claim": "News coverage will report on the passing of or actions related to the October 18 deadline for imposing sanctions under the Lindsey O. Graham Sanctioning Russia and Iran Act.",
            "probability": 0.7,
            "rationale": "An article published prior to the cutoff explicitly notes that an 'Oct. 18 deadline nears to start imposing sanctions' under this specific Act, indicating it will be a focal point for political and economic reporting on "
          },
          {
            "title": "Cook Islands Cyclone Aftermath",
            "claim": "Official advisories or news outlets will report on the weather conditions, infrastructure impacts, or aftermath in the Cook Islands following the cyclone warning.",
            "probability": 0.65,
            "rationale": "The U.S. Embassy issued a cyclone warning for the Cook Islands valid for October 16-17. By October 18, it is highly likely that post-storm assessments or continued weather impact updates will be published."
          }
        ],
        "q5Forecasts": [
          {
            "title": "BBCWorld US Election Coverage",
            "claim": "The BBCWorld X account will publish at least one post related to the United States elections, candidates, or election security.",
            "probability": 0.8,
            "rationale": "With the US elections prominently featured in recent BBCWorld posts (including reports on suspicious substances sent to election offices and coverage of candidates), this topic is highly likely to continue generating pos"
          },
          {
            "title": "BBCWorld Ukraine-Russia War Update",
            "claim": "BBCWorld will post on X regarding the ongoing conflict between Ukraine and Russia, involving statements by Zelensky, military strikes, or international diplomacy.",
            "probability": 0.75,
            "rationale": "BBCWorld has maintained a steady cadence of updates regarding Ukraine, recently covering Zelensky's appeals to the EU and strategies against Russian refineries. Continued coverage is highly probable."
          }
        ],
        "brier": 0.0025,
        "acc": 100.0,
        "mae": 1.0,
        "judge": 3.8,
        "judgeWorld": 4.1,
        "judgeSocial": 3.5,
        "judgeNotes": "Model B accurately predicted the major stories surrounding the October 18 Russia sanctions deadline and ongoing coverage of the Brazilian election featuring Flávio and Lula. Its forecast regarding the Cook Islands cyclone aftermath was a partial hit (Pacific Disaster Center tracked Tropical Cyclone Wati, though major c"
      },
      "gemini-3.8-flash": {
        "q1Prob": null,
        "q1Rationale": "The target window [2026-10-18T00:00:00Z, 2026-10-19T00:00:00Z) corresponds entirely to Sunday, a non-business weekend day when regular SEC EDGAR acceptance is offline; therefore Q1 is not applicable.",
        "q2Prob": 0.05,
        "q2Rationale": "The target period falls on Sunday, October 18, 2026. The SEC EDGAR filing system is generally closed for routine corporate filings on weekends, making an accepted Form 8-K from the 10 cohort mega-cap companies extremely improbable.",
        "q3Est": 1.0,
        "q3Interval": [
          0.0,
          3.0
        ],
        "q3Rationale": "NASA's X publication count on weekend days is historically reduced (observed 1 post on Sunday 2026-10-11 and 0 posts on Saturday 2026-10-17). Expectation for Sunday 2026-10-18 remains between 0 and 2 posts.",
        "q4Forecasts": [
          {
            "title": "Implementation of Lindsey Graham Sanctioning Russia and Iran Act",
            "claim": "The United States government will take executive or departmental steps pursuant to the October 18 deadline set under the Lindsey O. Graham Sanctioning Russia and Iran Act.",
            "probability": 0.72,
            "rationale": "Pre-cutoff reports noted an explicit statutory/administrative deadline of October 18, 2026, for starting enforcement or reporting under this legislation."
          },
          {
            "title": "Post-Tropical Cyclone Trudy Advisory Updates",
            "claim": "The National Hurricane Center (NHC) will continue issuing remnant advisories or final summary bulletins regarding Post-Tropical Cyclone Trudy.",
            "probability": 0.65,
            "rationale": "NHC bulletins from October 15 indicate Trudy weakened to a remnant low moving across the Eastern Pacific with continued monitoring."
          }
        ],
        "q5Forecasts": [
          {
            "title": "NASA Aerospace Expo MAX POWER Promotion",
            "claim": "NASA social accounts will share at least one update or reminder regarding the upcoming MAX POWER aerospace expo or ongoing mission milestones.",
            "probability": 0.55,
            "rationale": "NASA recently promoted the MAX POWER expo set for Kennedy Space Center alongside standard educational/historical aerospace updates on its weekend channels."
          },
          {
            "title": "WHO Social Messaging on Global Health Emergencies",
            "claim": "The World Health Organization (WHO) official X account will publish posts focusing on the malnutrition crisis in Sudan or humanitarian healthcare needs.",
            "probability": 0.8,
            "rationale": "WHO maintained steady messaging throughout the preceding week highlighting rising famine and healthcare shortages in conflict-affected regions like Sudan."
          }
        ],
        "brier": 0.0025,
        "acc": 100.0,
        "mae": 1.0,
        "judge": 3.7,
        "judgeWorld": 4.4,
        "judgeSocial": 2.9,
        "judgeNotes": "Model C only provided two forecasts per section, but both of its World predictions were highly accurate and well-calibrated: the US executive action on the October 18 Russia sanctions deadline (Trump's 60-day waiver) and the NHC's continued advisories on Post-Tropical Cyclone Trudy. Its Social forecasts on NASA's MAX P"
      },
      "gemini-3.1-flash-lite": {
        "q1Prob": null,
        "q1Rationale": "The target date 2026-10-18 is a Sunday, which is a weekend and thus not_applicable for Form 8-K filings as per the instructions.",
        "q2Prob": 0.05,
        "q2Rationale": "Historical data shows a consistent pattern of zero 8-K filings by the cohort companies on weekends (e.g., Oct 11 and Oct 12 were both zero). Given that 2026-10-18 is a Sunday, the probability of an 8-K filing is extremely low.",
        "q3Est": 0.0,
        "q3Interval": [
          0,
          1
        ],
        "q3Rationale": "NASA's recent activity on X has been low, with 0 posts on Oct 17. Weekend activity is generally minimal for such accounts, making 0 the most likely outcome, with a small probability of a singular, standard update.",
        "q4Forecasts": [
          {
            "title": "Middle East Conflict Energy Impact",
            "claim": "Continued upward pressure on global energy prices due to ongoing regional instability, consistent with IMF warnings from Oct 16.",
            "probability": 0.85,
            "rationale": "Multiple sources, including the IMF and market reports, emphasize that Middle Eastern tensions are a primary driver of current energy market volatility."
          },
          {
            "title": "Japan Diet Legislative Action",
            "claim": "Deliberations on the 'Important Land Survey Act' amendment will continue to be a primary focus of the 222nd extraordinary Diet session.",
            "probability": 0.7,
            "rationale": "With the Diet recently convened and the agenda established as of Oct 16, this legislative priority is confirmed."
          }
        ],
        "q5Forecasts": [
          {
            "title": "NASA Aerospace Expo Promotion",
            "claim": "NASA will continue to share content related to the upcoming 'MAX POWER' aerospace expo at Kennedy Space Center.",
            "probability": 0.6,
            "rationale": "The event is scheduled for Nov 7-8; following their Oct 16 post, continued promotional cadence is standard for NASA social media strategy."
          },
          {
            "title": "BBC World Election Coverage",
            "claim": "BBC World will increase its reporting volume on US election-related developments, such as the investigation into 'suspicious substances' sent to election offices.",
            "probability": 0.75,
            "rationale": "The proximity to the election and the security incidents reported on Oct 15 suggest ongoing coverage will remain a priority."
          }
        ],
        "brier": 0.0025,
        "acc": 100.0,
        "mae": 0.0,
        "judge": 2.8,
        "judgeWorld": 3.1,
        "judgeSocial": 2.5,
        "judgeNotes": "Model D correctly identified the major macro narrative of upward pressure on global energy prices and inflation/stagflation risks, which featured heavily across multiple Oct 18 articles, though the claim was phrased somewhat broadly rather than as a discrete next-day event. Its second World claim expecting Japanese Die"
      },
      "baseline": {
        "q1Prob": null,
        "q2Prob": 0.3,
        "q3Est": 1.6,
        "brier": 0.09,
        "acc": 100.0,
        "mae": 1.6,
        "judge": 2.5
      }
    }
  },
  {
    "caseId": "day-2026-10-18",
    "cutoffDate": "2026-10-18",
    "targetDate": "2026-10-19",
    "shortLabel": "Oct 19",
    "isWeekend": false,
    "ticker": "GOOGL",
    "baseClose": 340.59,
    "targetClose": 344.18,
    "q1Actual": true,
    "q2Actual": false,
    "q3Actual": 0,
    "judgeSummary": "On Monday, October 19, 2026, key developments included the Japanese House of Councillors Budget Committee holding intensive questioning of Prime Minister Sanae Takaichi regarding former Agriculture Minister Yana, Education Minister Seki, and the funding of food consumption tax cuts. In international diplomacy and sanctions, analysis and reactions continued regarding President Trump's executive order waiving Russian sanctions and tariffs under the Lindsey O. Graham Act, alongside the European Commission preparing its 22nd Russia sanctions package. Additionally, global energy markets reacted to soaring oil tanker freight rates and Middle East supply risks pushing Brent crude near $110/barrel.",
    "models": {
      "gemini-4-argon": {
        "q1Prob": 0.51,
        "q1Rationale": "Monday 2026-10-19 is a regular trading day. GOOGL pulled back roughly 2.47% on Friday 2026-10-16 to close near its daily low at 340.59 along with broader mega-cap tech weakness (MSFT, NVDA, META also declined). A modest mean-reversion bounce or baseline positive equity drift make",
        "q2Prob": 0.25,
        "q2Rationale": "2026-10-19 is a Monday, a regular SEC business day. While Q3 earnings season is ramping up (JPM filed on Oct 13, and NFLX/tech earnings often occur around mid-to-late October), only 1 day in the prior week had a cohort 8-K filing. A 25% probability reflects typical weekday baseli",
        "q3Est": 2.0,
        "q3Interval": [
          0,
          4
        ],
        "q3Rationale": "In the past week, NASA's X account had 0 posts on Monday Oct 12 (a federal holiday) and 0 over the weekend (Oct 17-18), while Tuesday through Friday (Oct 13-16) saw 2, 3, 4, and 2 posts respectively (average 2.75 per non-holiday weekday). For Monday Oct 19, a ",
        "q4Forecasts": [
          {
            "title": "Post-Tropical Cyclone Trudy Weakens to Remnant Low",
            "claim": "The U.S. National Hurricane Center will issue its final public advisory on Post-Tropical Cyclone Trudy as the system weakens into a remnant low in the Eastern Pacific.",
            "probability": 0.9,
            "rationale": "NHC advisory text in the pre-cutoff data explicitly indicates Trudy weakening into a remnant low with a final advisory scheduled on Monday, Oct 19."
          },
          {
            "title": "Japanese Upper House Budget Committee Holds General Questioning",
            "claim": "Japan's House of Councillors (Upper House) Budget Committee will hold general questioning (総括質疑), where opposition lawmakers will question Prime Minister Sanae Takaichi regarding her appointment responsibility following Agriculture Minister",
            "probability": 0.9,
            "rationale": "Japanese news schedules (Shimotsuke Shimbun and FNN) explicitly list the Upper House Budget Committee general questioning for Monday, October 19, focusing on PM Takaichi's responsibility for the recent ministerial resign"
          }
        ],
        "q5Forecasts": [
          {
            "title": "WHO X Posts on International Lead Poisoning Prevention Week",
            "claim": "The WHO X account (@WHO) will publish at least one post highlighting International Lead Poisoning Prevention Week and calling for source prevention of lead exposure.",
            "probability": 0.85,
            "rationale": "On Oct 18, WHO launched its messaging for International Lead Poisoning Prevention Week, which runs through the target week and typically features daily campaign posts."
          },
          {
            "title": "BBCWorld Coverage of Russia Sanctions Waiver and Ukraine War",
            "claim": "BBCWorld on X will post coverage regarding the aftermath of President Trump's decision to waive Graham Act sanctions on Russia or ongoing developments in Ukraine's strikes on Russian oil refineries.",
            "probability": 0.7,
            "rationale": "BBCWorld actively covered US-Ukraine-Russia tensions over the prior days, and news articles show major backlash to Trump waiving the Graham Act sanctions right before the deadline."
          }
        ],
        "brier": 0.1513,
        "acc": 100.0,
        "mae": 2.0,
        "judge": 4.5,
        "judgeWorld": 4.7,
        "judgeSocial": 4.0,
        "judgeNotes": "Model_A delivered the strongest and most specific World Forecasts. It accurately predicted both the Japanese Upper House Budget Committee questioning of PM Takaichi over former Agriculture Minister Yana (directly confirmed by NHK/Jiji Press reports) and continued reporting/scrutiny regarding President Trump's waiver of"
      },
      "gemini-3.1-pro-preview": {
        "q1Prob": 0.53,
        "q1Rationale": "GOOGL experienced a significant drop on Friday, October 16, falling to 340.59. Given general market conditions and the tendency for slight mean reversion after a sharp single-day decline, a minor bounce is slightly more probable than not for Monday, October 19.",
        "q2Prob": 0.25,
        "q2Rationale": "Monday, October 19 is a standard business day. While Monday filing volumes are generally lower than mid-week and major cohort members like JPM have already posted earnings, the baseline probability for at least one of these 10 mega-cap companies filing an 8-K for material events,",
        "q3Est": 3.0,
        "q3Interval": [
          1,
          5
        ],
        "q3Rationale": "NASA's X account published between 2 and 4 posts on regular weekdays during the preceding week. The zero-count on Monday, October 12, was due to the Columbus Day federal holiday. Operating on a normal schedule for Monday, October 19, the output should return t",
        "q4Forecasts": [
          {
            "title": "Japanese Upper House Budget Committee Interpellation",
            "claim": "The Japanese Upper House Budget Committee will hold a comprehensive interpellation (総括質疑) session on October 19, 2026.",
            "probability": 0.9,
            "rationale": "Pre-cutoff Japanese news articles specifically outline the political schedule, noting that the Upper House Budget Committee's comprehensive interpellation is set for Monday, October 19, amidst ongoing scrutiny of the Pri"
          },
          {
            "title": "Graham Act Russia Sanctions Deadline Passes Unenforced",
            "claim": "The October 18 deadline for the Lindsey O. Graham Sanctioning Russia and Iran Act will pass without the imposition of new Russian sanctions due to a presidential waiver.",
            "probability": 0.85,
            "rationale": "Reporting indicates the deadline to impose the sanctions was October 18, but President Trump signed an executive order waiving the sanctions just prior. The October 19 news cycle will reflect the formal passing of the de"
          }
        ],
        "q5Forecasts": [
          {
            "title": "WHO Posts About Lead Poisoning Prevention Week",
            "claim": "The WHO X account will publish at least one post referencing 'International Lead Poisoning Prevention Week' or the dangers of lead exposure.",
            "probability": 0.75,
            "rationale": "The WHO officially marked the beginning of International Lead Poisoning Prevention Week on Sunday, October 18. It is highly likely they will continue to promote this dedicated public health campaign throughout the active"
          },
          {
            "title": "BBCWorld Reports on Russian Sanctions Waiver Fallout",
            "claim": "The BBCWorld X account will post about Donald Trump's decision to waive the Graham Act sanctions on Russia or the resulting diplomatic backlash from Ukraine.",
            "probability": 0.6,
            "rationale": "BBCWorld closely follows US foreign policy and the war in Ukraine. The controversial waiver of Russian sanctions just before the statutory deadline is a major geopolitical development likely to be featured on their feed."
          }
        ],
        "brier": 0.1417,
        "acc": 100.0,
        "mae": 3.0,
        "judge": 4.3,
        "judgeWorld": 4.5,
        "judgeSocial": 4.0,
        "judgeNotes": "Model_B accurately identified two of the main geopolitical/political developments in the reference set: the Japanese Upper House Budget Committee interpellation and the fallout/reporting around the Graham Act Russian sanctions waiver. It was slightly less detailed than Model_A on the specific ministers targeted in the "
      },
      "gemini-3.8-flash": {
        "q1Prob": 0.51,
        "q1Rationale": "The baseline close for GOOGL on Friday 2026-10-16 was $340.59 after dipping from $349.22 on 2026-10-15. With broad market earnings season underway and Monday 2026-10-19 being an active trading day, equity index direction remains balanced near historical mean reversion tendencies.",
        "q2Prob": 0.35,
        "q2Rationale": "Monday 2026-10-19 is a regular SEC business day during earnings season. Across the 10 mega-cap companies in the cohort, original 8-K filings on non-earnings reporting dates typically occur with moderate frequency (around 20-40% probability for the group on any given weekday).",
        "q3Est": 2.5,
        "q3Interval": [
          1,
          4
        ],
        "q3Rationale": "Looking at the observed publication_counts for NASA over recent weekdays, observed counts were 0 (holiday/Columbus Day 10-12), 2 (10-13), 3 (10-14), 4 (10-15), 2 (10-16), and 0 over the weekend. On a regular Monday, NASA typically posts 2 to 3 original qualify",
        "q4Forecasts": [
          {
            "title": "Japanese Diet Upper House Budget Committee Questioning",
            "claim": "Japan's House of Councillors Budget Committee will hold comprehensive questionings involving Prime Minister Sanae Takaichi and ministers regarding recent cabinet appointments on October 19, 2026.",
            "probability": 0.9,
            "rationale": "Pre-cutoff Japanese political reports explicitly indicate an agreement for the House of Councillors Budget Committee general interpellations to convene on Monday, October 19."
          },
          {
            "title": "National Hurricane Center Tropical Cyclone Advisory for Trudy",
            "claim": "The National Hurricane Center will issue public advisory statements regarding Tropical Cyclone Trudy as it weakens into a remnant low during October 19, 2026.",
            "probability": 0.88,
            "rationale": "National Hurricane Center text bulletins in pre-cutoff evidence document Post-Tropical Cyclone Trudy approaching remnant low status with final advisory issuance scheduled on October 19, 2026."
          }
        ],
        "q5Forecasts": [
          {
            "title": "WHO Social Media Coverage on Lead Poisoning Prevention",
            "claim": "The World Health Organization will publish at least one communication on X focusing on International Lead Poisoning Prevention Week on October 19, 2026.",
            "probability": 0.85,
            "rationale": "WHO kicked off International Lead Poisoning Prevention Week on October 18, and global public health campaigns run continuous daily informational posts during designated campaign weeks."
          },
          {
            "title": "NASA Official X Account Activity",
            "claim": "NASA's main X account (@NASA) will publish at least one non-retweet, non-reply post regarding space operations, Earth observation, or upcoming missions on October 19, 2026.",
            "probability": 0.88,
            "rationale": "Historical cadence indicates NASA consistently posts original promotional and mission updates during standard working weekdays."
          }
        ],
        "brier": 0.1813,
        "acc": 100.0,
        "mae": 2.5,
        "judge": 4.0,
        "judgeWorld": 4.1,
        "judgeSocial": 3.8,
        "judgeNotes": "Model_C accurately predicted the Japanese House of Councillors Budget Committee questioning of PM Takaichi regarding cabinet appointments. Its second world forecast regarding NHC advisories for Trudy was plausible based on pre-cutoff trajectories, though not captured in the held-out article bundle. It missed the Graham"
      },
      "gemini-3.1-flash-lite": {
        "q1Prob": 0.5,
        "q1Rationale": "The target date 2026-10-19 falls on a Sunday. According to the standard calendar for market holidays, equity markets are closed, so the question is not applicable.",
        "q2Prob": 0.05,
        "q2Rationale": "October 19, 2026 is a Sunday. While corporations can file 8-Ks on weekends if the event is material and required, it is historically very rare for this specific cohort of large-cap companies to file on a Sunday unless there is an emergency. Given the lack of recent filings or spe",
        "q3Est": 0.0,
        "q3Interval": [
          0,
          1
        ],
        "q3Rationale": "NASA's X account has shown low activity over the last weekend (Oct 17-18, 2026) with zero observed posts. Based on the historical cadence of occasional posts and the general weekend quiet, 0 is the most likely estimate.",
        "q4Forecasts": [
          {
            "title": "Russia-Ukraine conflict status",
            "claim": "No major breakthroughs or signed peace treaties will occur on Sunday, October 19, 2026, due to the weekend. Diplomatic rhetoric may continue via news outlets.",
            "probability": 0.9,
            "rationale": "Geopolitical movements typically follow weekday office hours; weekends are rarely utilized for major breakthrough announcements in this context."
          },
          {
            "title": "Hurricane Trudy developments",
            "claim": "Hurricane Trudy will remain a remnant low or dissipate further without re-strengthening.",
            "probability": 0.85,
            "rationale": "The National Hurricane Center report from Oct 19 clearly states Trudy has become a remnant low and is the final advisory, indicating dissipation."
          }
        ],
        "q5Forecasts": [
          {
            "title": "NASA social activity",
            "claim": "NASA will not post any new content to X during the 24-hour target window.",
            "probability": 0.7,
            "rationale": "NASA's social media cadence shows minimal activity on weekends, with 0 posts recorded for the preceding Friday and Saturday in the provided data."
          },
          {
            "title": "WHO social focus",
            "claim": "WHO social media accounts will continue to emphasize International Lead Poisoning Prevention Week, potentially releasing one awareness-focused post.",
            "probability": 0.6,
            "rationale": "The WHO posted about this week on Oct 18, and organizations typically maintain campaign momentum for several days."
          }
        ],
        "brier": 0.1263,
        "acc": 100.0,
        "mae": 0.0,
        "judge": 2.1,
        "judgeWorld": 2.1,
        "judgeSocial": 2.0,
        "judgeNotes": "Model_D made a critical calendar error, stating that October 19, 2026 was a Sunday ('on Sunday, October 19, 2026, due to the weekend'), when October 19, 2026 was actually a Monday. This led to a generic negative forecast for Q4 and a flawed rationale for Q5 predicting NASA would not post due to weekend inactivity. Its "
      },
      "baseline": {
        "q1Prob": 0.5,
        "q2Prob": 0.3,
        "q3Est": 1.6,
        "brier": 0.17,
        "acc": 100.0,
        "mae": 1.6,
        "judge": 2.5
      }
    }
  },
  {
    "caseId": "day-2026-10-19",
    "cutoffDate": "2026-10-19",
    "targetDate": "2026-10-20",
    "shortLabel": "Oct 20",
    "isWeekend": false,
    "ticker": "META",
    "baseClose": 705.44,
    "targetClose": 694.25,
    "q1Actual": false,
    "q2Actual": true,
    "q3Actual": 3,
    "judgeSummary": "Key world developments on October 20, 2026 centered on the diplomatic and economic fallout from the Trump administration's 60-day waiver of Graham Act sanctions on Russia, including an EU Commission statement, Ukrainian President Zelenskyy sending peace proposals via US envoy Witkoff, and US Secretary of State Marco Rubio visiting India to discuss oil diversification and a global energy crunch driven by high crude and diesel prices. In corporate news, major Q3 2026 earnings were released by companies including Equifax, Chubb, Philip Morris, ABB, and Adidas. In Japan, Prime Minister Sanae Takaichi announced a new national-local policy forum on social security and education and marked the 1-year anniversary of the LDP-Ishin coalition.",
    "models": {
      "gemini-4-argon": {
        "q1Prob": 0.51,
        "q1Rationale": "META closed at 705.44 on 2026-10-19 after declining from 736.72 on Oct 15 and 709.33 on Oct 16. However, on Oct 19, META rebounded substantially intraday from a low of 693.86 to close near its open (707.16), while peer mega-cap tech stocks (MSFT, NVDA, GOOGL) posted gains. Given ",
        "q2Prob": 0.35,
        "q2Rationale": "The target window (Tuesday, 2026-10-20) is a regular business day during the third-quarter 2026 corporate earnings season. Notably, Netflix (NFLX) is in the 10-company cohort and traditionally reports Q3 earnings and files an accompanying Item 2.02 Form 8-K on the third Tuesday o",
        "q3Est": 2.0,
        "q3Interval": [
          0,
          4
        ],
        "q3Rationale": "During the supplied week, NASA's retrievable original X posts were 2, 3, 4, and 2 on Tuesday through Friday (Oct 13-16), followed by 0 posts over the weekend and Monday (Oct 17-19). Because Tuesday, Oct 20 is a standard weekday, NASA is likely to resume its no",
        "q4Forecasts": [
          {
            "title": "U.S. and Ukrainian diplomatic fallout over Graham Act sanctions waiver",
            "claim": "Officials or lawmakers will issue new public statements or hold talks on 2026-10-20 regarding the 60-day pause on Russia sanctions under the Graham Act and Ukraine's renewed strikes on Russian oil refineries.",
            "probability": 0.7,
            "rationale": "Pre-cutoff reporting from Oct 17-19 highlights intense backlash from lawmakers and President Zelenskyy following President Trump's executive order waiving Graham Act sanctions on Russia and Secretary Rubio's Oct 19 defen"
          },
          {
            "title": "Japanese parliamentary scrutiny of Prime Minister Takaichi's cabinet",
            "claim": "Japanese opposition lawmakers and media will continue challenging Prime Minister Sanae Takaichi during the extraordinary Diet session on 2026-10-20 over her cabinet's sub-50% approval rating and the delayed dismissal of former Agriculture M",
            "probability": 0.75,
            "rationale": "A Kyodo News poll on Oct 18 showed Cabinet support dropping to 49.1%, with 57.7% calling Yana's replacement too late, just as House of Councillors Budget Committee deliberations commenced on Oct 19."
          }
        ],
        "q5Forecasts": [
          {
            "title": "WHO X posts on International Lead Poisoning Prevention Week",
            "claim": "The WHO X account (@WHO) will publish at least one post during [2026-10-20T00:00:00Z, 2026-10-21T00:00:00Z) highlighting International Lead Poisoning Prevention Week or lead exposure prevention.",
            "probability": 0.65,
            "rationale": "On Oct 18, WHO launched its campaign for International Lead Poisoning Prevention Week, which runs throughout the week of Oct 18-24, making follow-up advocacy posts on Tuesday highly probable."
          },
          {
            "title": "BBCWorld X coverage of the Canadian military base fire or Russia-Ukraine conflict",
            "claim": "The BBCWorld X account (@BBCWorld) will post updates on 2026-10-20 regarding either the deadly fire at a Canadian military base or geopolitical developments surrounding Ukraine and Russia.",
            "probability": 0.6,
            "rationale": "BBCWorld posted multiple times during the prior week on Ukraine/Russia tensions (Oct 15, Oct 16) and broke news on Oct 19 about a rapidly moving deadly fire at a Canadian military base."
          }
        ],
        "brier": 0.3413,
        "acc": 0.0,
        "mae": 1.0,
        "judge": 4.0,
        "judgeWorld": 4.5,
        "judgeSocial": 3.5,
        "judgeNotes": "Strongest world forecast among the cohort: accurately predicted both diplomatic/public reactions to the 60-day Graham Act sanctions waiver on Russia (confirmed by EEAS, Zelenskyy/Witkoff talks, and legal/policy analyses) and major Q3 2026 U.S. corporate earnings releases on Oct 20 (confirmed by Equifax, Chubb, Philip M"
      },
      "gemini-3.1-pro-preview": {
        "q1Prob": 0.53,
        "q1Rationale": "META closed at 705.44 on October 19. Without specific major catalysts scheduled for META on October 20, the daily stock movement defaults to near 50%, with a slight historical upward drift for large-cap tech stocks on a typical trading day.",
        "q2Prob": 0.35,
        "q2Rationale": "Mid-October corresponds with earnings season. With 10 large-cap companies (including JPM, which recently reported, and others like NFLX that typically report in late October) and the target being a Tuesday (a highly active day for SEC filings), there is a moderate probability tha",
        "q3Est": 2.0,
        "q3Interval": [
          0,
          4
        ],
        "q3Rationale": "NASA's X account showed 2-4 daily posts between Oct 13-16, but dropped to 0 over the Oct 17-19 period (weekend and Monday). Assuming standard operations resume on Tuesday, a reversion to the mean of about 2 posts is expected, though the recent streak of zeroes",
        "q4Forecasts": [
          {
            "title": "Reactions to US Sanctions Waiver",
            "claim": "News articles will detail domestic or international reactions (such as from Ukraine or US lawmakers) to the Trump administration's 60-day waiver of Graham Act sanctions on Russia.",
            "probability": 0.7,
            "rationale": "The recent 60-day waiver and subsequent backlash from lawmakers and Zelenskyy is a major developing geopolitical story that will likely continue generating commentary and diplomatic responses."
          },
          {
            "title": "Japanese Diet Budget Committee Scrutiny",
            "claim": "Japanese media will cover the Diet's budget committee sessions, specifically highlighting opposition scrutiny of PM Sanae Takaichi over her cabinet appointments and the resignation of the agriculture minister.",
            "probability": 0.75,
            "rationale": "Recent polling indicates high dissatisfaction with the new Takaichi cabinet, and opposition parties are poised to aggressively question her in the scheduled budget committee meetings."
          }
        ],
        "q5Forecasts": [
          {
            "title": "WHO on Lead Poisoning Prevention",
            "claim": "The @WHO X account will publish at least one post related to International Lead Poisoning Prevention Week or the global burden of lead exposure.",
            "probability": 0.8,
            "rationale": "The WHO began observing International Lead Poisoning Prevention Week on October 18, and it is highly likely they will continue the campaign through the week."
          },
          {
            "title": "BBCWorld on the War in Ukraine",
            "claim": "The @BBCWorld X account will post an update concerning the Russia-Ukraine war, President Zelenskyy, or international military aid.",
            "probability": 0.75,
            "rationale": "With the recent US sanctions waiver on Russia and Ukraine's plans to restart strikes on oil refineries, the ongoing conflict remains a high-priority topic for global news outlets."
          }
        ],
        "brier": 0.3517,
        "acc": 0.0,
        "mae": 1.0,
        "judge": 3.85,
        "judgeWorld": 4.2,
        "judgeSocial": 3.5,
        "judgeNotes": "Accurately forecasted domestic and international reactions to the US 60-day waiver of Graham Act sanctions on Russia (confirmed by EEAS statement, Zelenskyy/Witkoff updates, and PBS/constitutional analyses) and captured the strong focus on the Middle East conflict's impact on global energy prices and inflation (confirm"
      },
      "gemini-3.8-flash": {
        "q1Prob": 0.52,
        "q1Rationale": "META closed at 705.44 on Monday, 2026-10-19 after sliding from 736.72 on 2026-10-15 and 709.33 on 2026-10-16. With major tech peers showing signs of stabilization on 2026-10-19 (e.g. MSFT and NVDA posting gains), equity market direction remains close to a coin flip with a mild me",
        "q2Prob": 0.22,
        "q2Rationale": "Tuesday is an active SEC filing day (170-240+ total filings daily across the market). Within our 10-company mega-cap cohort, earnings season is underway (JPM filed 8-Ks earlier in the week on Oct 13), though only occasional days produce unexpected material 8-K filings from these ",
        "q3Est": 1.8,
        "q3Interval": [
          0.0,
          4.0
        ],
        "q3Rationale": "The search protocol observed 2, 3, 4, and 2 posts on Oct 13-16, followed by 0 on weekend days Oct 17-18 and 0 on Monday Oct 19. Typical weekday NASA cadence under this retrieval method averages ~2 posts per day.",
        "q4Forecasts": [
          {
            "title": "National Hurricane Center Updates on Post-Tropical Cyclone Trudy",
            "claim": "NHC will maintain Post-Tropical Cyclone Trudy as a remnant low or issue final marine remnant advisories without re-intensification.",
            "probability": 0.94,
            "rationale": "Advisory #27 issued on the evening of Oct 19 declared Trudy a remnant low in its final scheduled public advisory."
          },
          {
            "title": "Japanese Parliamentary Scrutiny of Takaichi Administration",
            "claim": "Japanese parliamentary committee sessions will continue debates examining political accountability following the resignation of the Agriculture Minister.",
            "probability": 0.88,
            "rationale": "Reporting confirms the Diet budget committee agreed to hold sessions targeting the Takaichi cabinet's appointment responsibilities after Yana's resignation."
          }
        ],
        "q5Forecasts": [
          {
            "title": "WHO Campaign Messaging",
            "claim": "The WHO official account will publish further guidance related to International Lead Poisoning Prevention Week or maternal health.",
            "probability": 0.78,
            "rationale": "WHO has actively kicked off public health awareness communications on lead poisoning prevention and women's health during the current week."
          },
          {
            "title": "NASA Official Account Activity",
            "claim": "The NASA X account will post at least one update regarding upcoming aerospace expos, aeronautics testing, or space science research.",
            "probability": 0.72,
            "rationale": "NASA resumed weekday operational communications following the weekend hiatus, promoting upcoming Kennedy events and aeronautics lineups."
          }
        ],
        "brier": 0.4394,
        "acc": 0.0,
        "mae": 1.2,
        "judge": 2.75,
        "judgeWorld": 2.4,
        "judgeSocial": 3.1,
        "judgeNotes": "Provided only two world and two social forecasts, missing the major geopolitical and economic stories of the day (the Russia sanctions waiver fallout, Rubio's energy trip to India, and Q3 corporate earnings). Neither the NHC Post-Tropical Cyclone Trudy advisory nor the Diet committee debate over Yana's resignation was "
      },
      "gemini-3.1-flash-lite": {
        "q1Prob": 0.45,
        "q1Rationale": "META closed at 705.44 on 2026-10-19. Market sentiment is mixed with recent earnings volatility across the tech sector and geopolitical concerns affecting broader indices. Given the lack of positive catalysts in the pre-cutoff data, a slightly bearish bias is justified.",
        "q2Prob": 0.15,
        "q2Rationale": "While large-cap companies often file 8-Ks for various reasons, there were no major pre-announcements or scheduled event triggers for the cohort in the provided news to suggest an imminent filing burst on October 20.",
        "q3Est": 0.0,
        "q3Interval": [
          0,
          2
        ],
        "q3Rationale": "NASA's social activity as reported in the provided evidence has been zero on October 18 and October 19. Historical cadence suggests low activity over weekends and Mondays following periods of inactivity.",
        "q4Forecasts": [
          {
            "title": "US-Russia Sanctions Waiver Analysis",
            "claim": "The US administration will release preliminary analysis regarding the global economic impact of the 60-day pause on Russia sanctions, potentially impacting oil shipping volatility.",
            "probability": 0.65,
            "rationale": "Evidence indicates a 60-day pause was announced on October 18, and Secretary Rubio mentioned an intent to analyze the impact, making follow-up commentary likely."
          },
          {
            "title": "Japan Diet Session Deliberations",
            "claim": "The Japanese Diet session beginning October 19 will see significant parliamentary focus on the High City Cabinet's economic strategy and ministerial resignation aftermath.",
            "probability": 0.85,
            "rationale": "Recent articles highlight the convening of the 222nd extraordinary Diet session and intense political focus on ministerial turnover and cabinet support ratings."
          }
        ],
        "q5Forecasts": [
          {
            "title": "NASA Social Media Engagement",
            "claim": "NASA's X/Twitter account will remain inactive or post only automated administrative updates during the target window.",
            "probability": 0.7,
            "rationale": "NASA's recent observed count dropped to zero for the days immediately preceding the target window, suggesting a lull in active social dissemination."
          },
          {
            "title": "BBCWorld Conflict Coverage",
            "claim": "BBCWorld will continue to feature reporting on regional escalations in Sudan or the Middle East conflict.",
            "probability": 0.8,
            "rationale": "The supplied feed consistently emphasizes conflict-related news and regional instability, indicating a trend that is likely to persist through the target window."
          }
        ],
        "brier": 0.4625,
        "acc": 50.0,
        "mae": 3.0,
        "judge": 3.1,
        "judgeWorld": 3.2,
        "judgeSocial": 3.0,
        "judgeNotes": "Partially captured the intersection of the 60-day Russia sanctions waiver and oil shipping/supply dynamics (confirmed by articles on Trump's Russian oil waiver boosting India's winter supplies and Rubio's India visit). However, it mistranslated Prime Minister Sanae Takaichi's name literally as the 'High City Cabinet' ("
      },
      "baseline": {
        "q1Prob": 0.5,
        "q2Prob": 0.3,
        "q3Est": 1.6,
        "brier": 0.37,
        "acc": 0.0,
        "mae": 1.4,
        "judge": 2.5
      }
    }
  },
  {
    "caseId": "day-2026-10-20",
    "cutoffDate": "2026-10-20",
    "targetDate": "2026-10-21",
    "shortLabel": "Oct 21",
    "isWeekend": false,
    "ticker": "JPM",
    "baseClose": 335.26,
    "targetClose": 335.19,
    "q1Actual": false,
    "q2Actual": true,
    "q3Actual": 1,
    "judgeSummary": "Key developments on October 21, 2026 included the EU condemning the US waiver of Russia sanctions and Ukrainian President Zelensky expressing support for trilateral talks; surging oil shipping costs (exceeding $20/barrel) and inflationary pressures from the Middle East conflict; extensive Japanese political coverage marking the one-year anniversary of the Takaichi administration, consumption tax reduction bill deliberations, and illegal donation allegations against the newly appointed Agriculture Minister Takebe; major AI announcements (OpenAI biological data agents and ChatGPT Ads expansion, NVIDIA life sciences partnerships, Synaptics edge AI); and climate/weather alerts regarding Super Typhoon Rosal in the Philippines and El Niño health risks. Note: No social media posts were captured in the held-out reference evidence for this window.",
    "models": {
      "gemini-4-argon": {
        "q1Prob": 0.51,
        "q1Rationale": "JPM closed at 335.26 on Tuesday, 2026-10-20, rebounding modestly (+0.52%) from Monday's close of 333.53 after reaching an intraday high of 339.86. JPM also filed an 8-K after market close on 2026-10-20. Given mixed broader equity performance on Oct 20 and typical near-50/50 daily",
        "q2Prob": 0.28,
        "q2Rationale": "The target window (Wednesday, 2026-10-21) is a mid-week trading day during peak Q3 2026 earnings season. While NFLX and JPM just filed 8-Ks on 2026-10-20 (2 filings across the 7-day history window), other major tech and retail cohort companies (such as META, MSFT, GOOGL, AMZN, AA",
        "q3Est": 3.0,
        "q3Interval": [
          1,
          5
        ],
        "q3Rationale": "In the supplied publication_counts, NASA posted 3, 4, and 2 times on Wednesday (Oct 14), Thursday (Oct 15), and Friday (Oct 16), 0 times over the weekend and Monday (Oct 17-19), and resumed posting with 3 posts on Tuesday (Oct 20). For Wednesday, Oct 21, a ret",
        "q4Forecasts": [
          {
            "title": "Continued Diplomatic and Political Reaction to US 60-Day Pause on Russia Sanctions",
            "claim": "During 2026-10-21, international media will report further diplomatic discussions or lawmaker reactions regarding the Trump administration's 60-day waiver of Graham Act sanctions on Russia and related Ukraine settlement negotiations.",
            "probability": 0.65,
            "rationale": "Multiple recent articles (Oct 17-19) highlight President Trump signing an order waiving Graham Act sanctions for 60 days, Secretary Rubio explaining the pause to analyze global impacts, and US/European negotiators explor"
          },
          {
            "title": "Middle East Conflict Impact on Oil Shipping Rates and Refining Margins",
            "claim": "Financial and energy news on 2026-10-21 will report continued pressure on Asian or European oil refiners and elevated crude tanker rates linked to Middle East conflict disruptions.",
            "probability": 0.6,
            "rationale": "Articles from Reuters, Nikkei Asia, and the IMF between Oct 15 and Oct 19 emphasize surging supertanker rates pushing Asian and European refiners into the red and IMF warnings of regional economic shocks."
          }
        ],
        "q5Forecasts": [
          {
            "title": "BBCWorld X Coverage of Geopolitics and US/Ukraine/Russia Developments",
            "claim": "The @BBCWorld X account will publish at least one post during [2026-10-21T00:00:00Z, 2026-10-22T00:00:00Z) covering international geopolitical tensions, US political/legal news, or the Russia-Ukraine conflict.",
            "probability": 0.85,
            "rationale": "@BBCWorld posts multiple times daily in the supplied record, consistently covering US politics, Ukraine/Russia developments, and major international incidents."
          },
          {
            "title": "WHO X Posts on International Lead Poisoning Prevention Week",
            "claim": "The @WHO X account will publish at least one post referencing International Lead Poisoning Prevention Week or public health prevention measures during [2026-10-21T00:00:00Z, 2026-10-22T00:00:00Z).",
            "probability": 0.55,
            "rationale": "On Oct 18, @WHO highlighted that it is International Lead Poisoning Prevention Week (which runs through the third week of October), making follow-up campaign posts on Wednesday, Oct 21 likely."
          }
        ],
        "brier": 0.3892,
        "acc": 0.0,
        "mae": 2.0,
        "judge": 3.8,
        "judgeWorld": 4.8,
        "judgeSocial": 2.5,
        "judgeNotes": "Strengths: Outstanding Q4 World predictions. All three forecasts hit directly with high specificity: (1) EU condemning the US waiver of Russia sanctions and Zelensky discussing trilateral talks, (2) IEA and Goldman Sachs reports on oil shipping costs surging sevenfold to over $20/barrel due to the Middle East war, and "
      },
      "gemini-3.1-pro-preview": {
        "q1Prob": 0.53,
        "q1Rationale": "October 21, 2026, is a Wednesday, a regular trading day. JPM's last close was 335.26. Absent specific pre-cutoff market-moving catalysts, daily stock price movements approximate a random walk with a slight positive drift, making an upward move slightly more likely than a downward",
        "q2Prob": 0.35,
        "q2Rationale": "The target window is a regular weekday during what is typically mid-to-late October earnings season. While 10 large-cap companies are in the cohort and some, like NFLX and JPM, have recently filed 8-Ks, the probability of at least one of the remaining companies filing an original",
        "q3Est": 3.0,
        "q3Interval": [
          1,
          5
        ],
        "q3Rationale": "NASA's X account has shown a publication pattern of around 2 to 4 posts on mid-week days (e.g., 3 on Tuesday, Oct 20, and 3 on Wednesday, Oct 14). Extrapolating this mid-week cadence yields a point estimate of 3.",
        "q4Forecasts": [
          {
            "title": "Middle East conflict and economic impact",
            "claim": "At least one news article will discuss the economic impact of the Middle East conflict on energy prices or inflation.",
            "probability": 0.7,
            "rationale": "The IMF recently highlighted the risk of the Middle East conflict keeping energy prices on edge. Ongoing geopolitical tensions and economic vulnerability make this a highly salient and ongoing news topic."
          },
          {
            "title": "Reactions to Russia sanctions waiver",
            "claim": "At least one news article will report on domestic or international reactions (e.g., from lawmakers or Zelenskyy) to the waiver of Graham Act sanctions on Russia.",
            "probability": 0.65,
            "rationale": "The recent 60-day pause and waiver of Graham Act sanctions on Russia has already drawn backlash. Follow-up reporting on legislative, diplomatic, or economic responses is highly likely as the story develops."
          }
        ],
        "q5Forecasts": [
          {
            "title": "WHO lead poisoning campaign",
            "claim": "The WHO X account will publish a post mentioning \"lead\" or \"poisoning\".",
            "probability": 0.75,
            "rationale": "The WHO recently announced it is International Lead Poisoning Prevention Week, suggesting a high likelihood of follow-up educational posts or campaign materials on the topic during the week."
          },
          {
            "title": "BBCWorld coverage of Ukraine",
            "claim": "The BBCWorld X account will mention \"Ukraine\", \"Zelensky\", or \"Russia\".",
            "probability": 0.8,
            "rationale": "The ongoing war, recent statements regarding sanctions waivers, and strikes on Russian oil refineries maintain this conflict as a daily fixture in international news reporting on BBCWorld's feed."
          }
        ],
        "brier": 0.3517,
        "acc": 0.0,
        "mae": 2.0,
        "judge": 3.3,
        "judgeWorld": 4.0,
        "judgeSocial": 2.5,
        "judgeNotes": "Strengths: Strong hits on two of three Q4 forecasts: the economic/inflationary impact of the Middle East conflict on oil/energy prices (multiple articles from IEA, Axios, Euronews, Hindu BusinessLine) and international reactions/Zelensky's response to the Russia sanctions waiver. Misses: Predicted updates on Hurricane "
      },
      "gemini-3.8-flash": {
        "q1Prob": 0.52,
        "q1Rationale": "JPM closed at 335.26 on 2026-10-20, rebounding modestly from 333.53 on 2026-10-19. Mid-October earnings season dynamics and standard equity drift without strong directional divergence suggest an approximately balanced probability with a slight upward tilt.",
        "q2Prob": 0.35,
        "q2Rationale": "The target day (Wednesday, 2026-10-21) is an active SEC filing business day with overall EDGAR filing counts around 200/day. Two cohort members (NFLX and JPM) filed 8-Ks on October 20; base rate probabilities of another cohort member filing an original 8-K on a single mid-week ea",
        "q3Est": 2.5,
        "q3Interval": [
          1.0,
          5.0
        ],
        "q3Rationale": "NASA's recent daily observed X counts for weekdays in the week were 3, 4, 2, 0, and 3, averaging approximately 2 to 3 original posts on weekdays under the search contract.",
        "q4Forecasts": [
          {
            "title": "US Russia Sanctions Waiver Debates",
            "claim": "Major international news reporting will follow political discussions and reactions regarding US sanctions waivers and foreign policy toward Russia and Ukraine during the target window.",
            "probability": 0.85,
            "rationale": "Reporting across ABC News, The Hindu, and BBC leading into October 20 highlighted the recent order waiving Graham Act sanctions and a 60-day pause."
          },
          {
            "title": "Japanese Parliamentary Scrutiny on Cabinet",
            "claim": "Japanese domestic media coverage will focus on prime ministerial appointments and committee hearings following cabinet minister departures.",
            "probability": 0.8,
            "rationale": "Japanese outlets (FNN, Nikkei) reported extensively on Diet budget committee scheduling and approval ratings following the farm minister's resignation."
          }
        ],
        "q5Forecasts": [
          {
            "title": "BBC World News Posting Continuity",
            "claim": "BBC World will post at least 5 new updates on X covering international headlines during the target 24h window.",
            "probability": 0.9,
            "rationale": "BBC World routinely publishes multiple updates daily across world events, politics, and natural hazards."
          },
          {
            "title": "NASA Social Media Update on Missions or Aeronautics",
            "claim": "NASA will publish at least one public video or post highlighting space missions, aeronautics, or technology updates.",
            "probability": 0.8,
            "rationale": "NASA has maintained regular weekday publication cadence on YouTube and X covering rovers, aircraft expos, and planetary science."
          }
        ],
        "brier": 0.3465,
        "acc": 0.0,
        "mae": 1.5,
        "judge": 3.2,
        "judgeWorld": 4.2,
        "judgeSocial": 2.0,
        "judgeNotes": "Strengths: Both Q4 world forecasts were accurate: international reaction to the US Russia sanctions waiver (EU condemnation) and Japanese media scrutiny on the newly appointed Agriculture Minister following his predecessor's departure. Misses: Only provided 2 forecasts per section rather than 3, and used slightly overc"
      },
      "gemini-3.1-flash-lite": {
        "q1Prob": 0.45,
        "q1Rationale": "JPM closed at 335.26 on 2026-10-20. Market volatility remains present given the ongoing earnings season and geopolitical uncertainty, leading to a moderate, near-coin-toss probability for a directional move.",
        "q2Prob": 0.15,
        "q2Rationale": "While companies in the cohort (like JPM and NFLX) have been active with filings recently (10/20), 8-Ks are event-driven and not guaranteed to occur daily. The likelihood of a filing in a specific 24-hour window remains low.",
        "q3Est": 2.0,
        "q3Interval": [
          0,
          4
        ],
        "q3Rationale": "NASA's posting cadence is low and intermittent, with zero posts observed on 10/17-10/19 and three on 10/20. A range of 0-4 reflects the typical sparsity of their recent activity.",
        "q4Forecasts": [
          {
            "title": "Japan Diet Deliberation",
            "claim": "The Japanese government will proceed with the 10/22 discussion on digital textbook guidelines, specifically addressing the hybrid paper-digital framework.",
            "probability": 0.85,
            "rationale": "The Ministry of Education, Culture, Sports, Science and Technology (MEXT) has already scheduled this discussion for 10/22."
          },
          {
            "title": "Middle East Economic Impact",
            "claim": "Continued regional instability will maintain upward pressure on oil tanker insurance/freight rates, impacting refiner margins in Asia.",
            "probability": 0.75,
            "rationale": "Reporting from Nikkei Asia and other sources on 10/19 confirms that rising tanker rates are a current, active constraint on regional refiners."
          }
        ],
        "q5Forecasts": [
          {
            "title": "NASA Lunar Content",
            "claim": "NASA's social media accounts will focus on lunar infrastructure or Artemis-related updates given their recent 10/20 posting update.",
            "probability": 0.6,
            "rationale": "The 10/20 YouTube update specifically mentioned 'Moon Base: Rovers and Lunar Terrain Vehicles,' suggesting a content focus on lunar tech."
          },
          {
            "title": "BBC Coverage",
            "claim": "BBC World will continue to report on US political developments, potentially focusing on the Trump golf course legal dispute identified on 10/20.",
            "probability": 0.7,
            "rationale": "Recent activity (10/20) shows the BBC is actively covering ongoing domestic US legal and political issues."
          }
        ],
        "brier": 0.4625,
        "acc": 50.0,
        "mae": 1.0,
        "judge": 2.7,
        "judgeWorld": 3.0,
        "judgeSocial": 2.3,
        "judgeNotes": "Strengths: Accurately predicted the continued upward pressure on oil tanker freight rates and insurance from the Middle East conflict (Goldman Sachs and IEA reports). Misses: The first Q4 forecast explicitly targeted an event scheduled for 10/22 (outside the 10/21 target window) with 0.85 probability, and it did not ap"
      },
      "baseline": {
        "q1Prob": 0.5,
        "q2Prob": 0.3,
        "q3Est": 1.6,
        "brier": 0.37,
        "acc": 0.0,
        "mae": 0.6,
        "judge": 2.5
      }
    }
  },
  {
    "caseId": "day-2026-10-21",
    "cutoffDate": "2026-10-21",
    "targetDate": "2026-10-22",
    "shortLabel": "Oct 22",
    "isWeekend": false,
    "ticker": "XOM",
    "baseClose": 178.09,
    "targetClose": 178.23,
    "q1Actual": true,
    "q2Actual": false,
    "q3Actual": 1,
    "judgeSummary": "On October 22, 2026, key world developments centered on energy market volatility, Middle East and Ukraine diplomacy, Q3 corporate earnings, and El Niño preparedness. Oil prices climbed (WTI briefly topping $100) amid Middle East shipping disruptions, prompting Macron and Qatar to call for opening the Strait of Hormuz and a Gaza ceasefire, while the IMF warned India on oil-driven inflation. Meanwhile, a US-Russia diesel deal rattled the Atlantic tanker market and drew criticism from Czech President Petr Pavel regarding its impact on Ukraine ceasefire prospects, as Putin emphasized security guarantees in US-Ukraine talks. In Japan, political coverage marked the one-year anniversary of the Takaichi administration, debates over a 31-seat proportional representation cut, and warnings over a critical PHP vulnerability. Major Q3 earnings were released by Nestlé, Roche, Dow, and Omnicom, while OpenAI, Anthropic, and Nvidia announced new enterprise and life-sciences AI initiatives. Note: The held-out reference set for October 22 contained only news articles and no social media posts.",
    "models": {
      "gemini-4-argon": {
        "q1Prob": 0.52,
        "q1Rationale": "XOM closed at 178.09 on Wednesday, October 21, 2026, up slightly from 177.86 on October 20 and near 178.28 on October 19. The macro news environment highlights elevated oil tanker rates, Middle East supply risks, and high diesel prices, which provide a modest fundamental tailwind",
        "q2Prob": 0.35,
        "q2Rationale": "The target window (Thursday, October 22, 2026) is an active weekday during Q3 earnings season, with overall SEC filing counts increasing from 193 on Monday to 261 on Wednesday. In the cohort, NFLX and JPM filed Form 8-Ks on October 20, and META filed its Q3 earnings Form 8-K on O",
        "q3Est": 2.0,
        "q3Interval": [
          0,
          4
        ],
        "q3Rationale": "Over the past seven days (Oct 15 to Oct 21), retrievable original NASA X posts were [4, 2, 0, 0, 0, 3, 1]. Specifically, the previous Thursday (Oct 15) had 4 posts, and recent weekdays (Tue Oct 20 and Wed Oct 21) had 3 and 1 posts respectively. A point estimat",
        "q4Forecasts": [
          {
            "title": "Japan MEXT Panel Reviews Draft Digital Textbook Guidelines",
            "claim": "Japan's Ministry of Education, Culture, Sports, Science and Technology (MEXT) will hold an expert panel meeting on October 22, 2026, to review draft guidelines emphasizing hybrid paper-and-digital textbook usage.",
            "probability": 0.85,
            "rationale": "A Nikkei report from October 19 explicitly states that MEXT compiled draft guidelines for digital textbooks and will present the draft at an expert review meeting on the 22nd."
          },
          {
            "title": "Continued Diplomatic Fallout and Reporting on US 60-Day Russia Sanctions Waiver",
            "claim": "International media and policy outlets will publish further reaction or analysis regarding the Trump administration's 60-day pause/waiver on Graham Act Russia sanctions and Ukraine peace settlement proposals.",
            "probability": 0.65,
            "rationale": "Multiple articles between October 17 and October 20 cover the 60-day waiver of Graham Act sanctions on Russia, Marco Rubio's statements, and US-European negotiations over Ukraine, indicating an active ongoing story."
          }
        ],
        "q5Forecasts": [
          {
            "title": "BBCWorld X Coverage of US Politics or Russia-Ukraine Conflict",
            "claim": "The @BBCWorld X account will publish at least one post on October 22, 2026, covering either the Russia-Ukraine conflict or US domestic political/election developments.",
            "probability": 0.75,
            "rationale": "BBCWorld posts daily in the supplied archive and frequently covers Ukraine/Russia developments and US political stories."
          },
          {
            "title": "NASA Social Post on Lunar Exploration or Upcoming Aerospace Events",
            "claim": "NASA's X or YouTube account will publish content related to lunar exploration (Moon base/rovers), International Space Station operations, or upcoming agency events.",
            "probability": 0.65,
            "rationale": "NASA posted 3 times on Oct 20 and 1 time on Oct 21 on X, plus an October 20 YouTube update on lunar rovers and an Oct 16 X post on the Kennedy Space Center aerospace expo."
          }
        ],
        "brier": 0.1764,
        "acc": 100.0,
        "mae": 1.0,
        "judge": 3.8,
        "judgeWorld": 4.3,
        "judgeSocial": 3.0,
        "judgeNotes": "Strong Q4 performance: accurately anticipated both the continued coverage of soaring oil tanker shipping costs/diesel market pressures ('The soaring cost of shipping is lifting the price of oil for consumers', 'US-Russia diesel deal adds volatility to Atlantic tanker market') and diplomatic fallout from US-Russia sanct"
      },
      "gemini-3.1-pro-preview": {
        "q1Prob": 0.52,
        "q1Rationale": "XOM closed at 178.09 on 2026-10-21. Escalating tensions in the Middle East and Ukraine's stated intent to restart strikes on Russian oil refineries provide upward pressure on oil prices, slightly favoring an increase in XOM's share price on Thursday, though daily market variance ",
        "q2Prob": 0.25,
        "q2Rationale": "October 22 is a Thursday during Q3 earnings season. While META and NFLX recently filed 8-Ks, several other cohort members have yet to report. The baseline probability of at least one out of ten mega-cap companies filing a material event or earnings 8-K on a given mid-week busines",
        "q3Est": 2.0,
        "q3Interval": [
          0,
          4
        ],
        "q3Rationale": "NASA's X account has averaged around 2 posts per weekday recently (e.g., 4 on Oct 15, 2 on Oct 16, 3 on Oct 20, 1 on Oct 21). An estimate of 2 reflects this steady but low-volume cadence, with reasonable variance falling between 0 and 4.",
        "q4Forecasts": [
          {
            "title": "Fallout from Russia Sanctions Waiver",
            "claim": "Major news outlets will report on the international or domestic political response to the U.S. 60-day waiver of the Graham Act sanctions on Russia.",
            "probability": 0.7,
            "rationale": "The waiver has already triggered backlash from lawmakers and Zelenskyy; follow-up reporting on this significant geopolitical decision is highly likely over the subsequent days."
          },
          {
            "title": "Ukraine Oil Refinery Strikes",
            "claim": "There will be continued reporting or official statements regarding Ukraine's plans or actions to resume military strikes on Russian oil refineries.",
            "probability": 0.65,
            "rationale": "Zelensky recently announced the restart of these strikes, representing a major strategic shift that will draw ongoing media analysis and potential immediate action."
          }
        ],
        "q5Forecasts": [
          {
            "title": "WHO Lead Poisoning Campaign",
            "claim": "The WHO X account will post about International Lead Poisoning Prevention Week or the dangers of lead exposure.",
            "probability": 0.6,
            "rationale": "WHO initiated this topic on Oct 18, and public health awareness weeks typically feature multiple thematic posts throughout the targeted week."
          },
          {
            "title": "BBC World Ukraine Coverage",
            "claim": "The BBCWorld X account will post at least one update regarding the war in Ukraine or international relations involving Russia.",
            "probability": 0.85,
            "rationale": "BBCWorld frequently posts about the Ukraine conflict, with multiple recent posts covering Zelenskyy, EU support, and Russian oil refineries."
          }
        ],
        "brier": 0.1464,
        "acc": 100.0,
        "mae": 1.0,
        "judge": 3.9,
        "judgeWorld": 4.5,
        "judgeSocial": 3.0,
        "judgeNotes": "Best Q4 alignment among the models. Directly hit the Middle East energy/shipping cost impact on crude and diesel prices (0.80) and the geopolitical fallout from the US-Russia sanctions/diesel deal involving Zelenskyy and European leaders (0.70), while the third claim on Russian oil/tanker attacks partially aligned with"
      },
      "gemini-3.8-flash": {
        "q1Prob": 0.51,
        "q1Rationale": "ExxonMobil (XOM) closed at 178.09 on 2026-10-21 after moving from 178.28 on Oct 19 and 177.86 on Oct 20. The price action is consolidating near $178 amidst volatile oil transport and diesel dynamics reported in macro commentary. Without an explicit one-directional catalyst, the c",
        "q2Prob": 0.42,
        "q2Rationale": "The target date 2026-10-22 is a Thursday, an active SEC business day during Q3 earnings season. Within the 10-company cohort, Netflix and JPMorgan filed Form 8-Ks on Oct 20, and Meta filed on Oct 21. While Q3 earnings season creates elevated probabilities of additional cohort mem",
        "q3Est": 2.2,
        "q3Interval": [
          0,
          5
        ],
        "q3Rationale": "Looking at NASA's retrievable original X posts over the past week (Oct 15: 4, Oct 16: 2, Oct 17: 0, Oct 18: 0, Oct 19: 0, Oct 20: 3, Oct 21: 1), NASA averages roughly 2 to 3 posts on typical mid-to-late weekdays. A point estimate of 2.2 with an 80% interval fr",
        "q4Forecasts": [
          {
            "title": "Japan MEXT Panel Review of Digital Textbooks Guideline",
            "claim": "Japan's Ministry of Education, Culture, Sports, Science and Technology (MEXT) will hold its scheduled expert committee review on October 22 regarding the draft guidelines prioritizing paper-digital hybrid textbooks.",
            "probability": 0.88,
            "rationale": "Pre-cutoff reporting explicitly states that MEXT prepared its draft guideline prioritizing paper textbooks alongside digital materials and scheduled discussion for its committee meeting on October 22."
          },
          {
            "title": "U.S. TV Premiere of Time Season 3",
            "claim": "Season 3 of the British drama series Time will premiere in the United States on Thursday, October 22, 2026.",
            "probability": 0.85,
            "rationale": "Film Music Reporter's roundup on October 18, 2026 confirms the U.S. premiere of Jimmy McGovern's series Time Season 3 is scheduled for Thursday, October 22."
          }
        ],
        "q5Forecasts": [
          {
            "title": "NASA Social Updates on Aeronautics or Science Missions",
            "claim": "NASA will publish at least one original post on its main X account highlighting agency aerospace events, aeronautics programs (such as MAX POWER), or space science updates during October 22 UTC.",
            "probability": 0.78,
            "rationale": "NASA's regular weekday cadence shows consistent activity promoting upcoming events (such as the Nov 7-8 MAX POWER expo) and ongoing science missions."
          },
          {
            "title": "BBC World Coverage of Geopolitical Sanctions and Conflict",
            "claim": "BBC World's official X feed will post multiple breaking or analytical news reports addressing Russia-Ukraine diplomacy or Middle East regional tensions during October 22 UTC.",
            "probability": 0.91,
            "rationale": "BBC World's feed has consistently covered Ukraine-Russia sanctions debates and Middle East conflict developments across the entire pre-cutoff week."
          }
        ],
        "brier": 0.2082,
        "acc": 100.0,
        "mae": 1.2,
        "judge": 2.4,
        "judgeWorld": 2.4,
        "judgeSocial": 2.5,
        "judgeNotes": "Only provided two forecasts per category and both Q4 predictions missed the actual held-out reference articles. Assigned high probabilities (0.88 and 0.85) to narrow scheduled events (Japan MEXT textbook meeting and US TV premiere of Time Season 3) that did not register in the day's captured news, missing major macroec"
      },
      "gemini-3.1-flash-lite": {
        "q1Prob": 0.45,
        "q1Rationale": "XOM's price has been volatile in the most recent trading days, showing a minor dip on October 20th followed by a recovery on October 21st, closing at 178.09. Given the current geopolitical tensions impacting energy prices as discussed in recent news, the market direction is uncer",
        "q2Prob": 0.25,
        "q2Rationale": "While companies like META and NFLX have filed 8-K reports recently (Oct 21 and Oct 20 respectively), these have already occurred. The cohort of large tech companies does not exhibit a high frequency of original 8-K filings on non-earnings reporting dates. With no major scheduled ",
        "q3Est": 1.0,
        "q3Interval": [
          0,
          2
        ],
        "q3Rationale": "NASA's X (Twitter) cadence has been inconsistent, with 0-4 posts per day in the last week. As the account frequently utilizes the platform for mission updates rather than high-frequency social noise, a low estimate of 1 post is projected for the target 24-hour",
        "q4Forecasts": [
          {
            "title": "Japanese Ministry of Education Digital Textbook Meeting",
            "claim": "The Japanese Ministry of Education will proceed with the deliberative meeting regarding digital textbook guidelines on October 22, 2026.",
            "probability": 0.9,
            "rationale": "The recent news article titled 'デジタル教科書は「紙との併用が基本」 文科省指針案、紙の比重重く' explicitly mentions that the Ministry of Education has scheduled the review meeting for the digital textbook guidelines for October 22."
          },
          {
            "title": "Middle East Conflict Energy Market Impact",
            "claim": "Oil tanker shipping rates will continue to exert upward pressure on refined petroleum product prices in Asia and Europe.",
            "probability": 0.75,
            "rationale": "Multiple articles from Oct 16-19 confirm that the conflict is pressuring energy economies and that tanker rate surges are negatively affecting regional refiners."
          }
        ],
        "q5Forecasts": [
          {
            "title": "NASA Mission Outreach Content",
            "claim": "NASA will publish at least one update regarding aerospace or lunar mission developments on their social platforms.",
            "probability": 0.6,
            "rationale": "NASA's social media strategy consistently involves periodic updates, and their recent activity (e.g., the Oct 20 YouTube post on lunar rovers) suggests active communication about their ongoing projects."
          },
          {
            "title": "BBCWorld Geopolitical Coverage",
            "claim": "BBCWorld will continue to report on the medical condition of Pope Leo XIV or the aftermath of the Ukraine-Russia situation.",
            "probability": 0.8,
            "rationale": "These topics have been recurrent in BBCWorld's recent feed (Oct 15-21), and both represent ongoing, evolving stories likely to see follow-up updates."
          }
        ],
        "brier": 0.1825,
        "acc": 50.0,
        "mae": 0.0,
        "judge": 3.2,
        "judgeWorld": 3.5,
        "judgeSocial": 2.9,
        "judgeNotes": "Only provided two forecasts per section. In Q4, it accurately captured the upward pressure on oil and refined product prices from tanker shipping rates in Europe and Asia (0.75), which aligned well with EU Oil Coordination Group, World Ports Organization, and India crude import articles. However, it was overconfident ("
      },
      "baseline": {
        "q1Prob": 0.5,
        "q2Prob": 0.3,
        "q3Est": 1.6,
        "brier": 0.17,
        "acc": 100.0,
        "mae": 0.6,
        "judge": 2.5
      }
    }
  },
  {
    "caseId": "day-2026-10-22",
    "cutoffDate": "2026-10-22",
    "targetDate": "2026-10-23",
    "shortLabel": "Oct 23",
    "isWeekend": false,
    "ticker": "WMT",
    "baseClose": 121.12,
    "targetClose": 119.89,
    "q1Actual": false,
    "q2Actual": true,
    "q3Actual": 3,
    "judgeSummary": "On October 23, 2026, key world developments included extensive legal, diplomatic, and energy market follow-ups on President Trump's Graham Act sanctions waiver (including EU Commission statements and analysis of Russian/US crude flows to India alongside record freight rates), a localized humanitarian ceasefire in Oleshky, Ukraine brokered by First Lady Melania Trump, a joint ministerial statement by Ireland and 31 partners on the risk of famine in Sudan, and heightened energy/inflation pressures across global markets due to the US-Iran conflict. In weather news, PAGASA reported no active tropical cyclone left in the Philippine Area of Responsibility (listing archived TCBs #1-12 for Rosal), while South Korea held emergency meetings as Typhoon Champi (formerly Rosal) approached. No social media posts were captured in the held-out reference evidence for the target window.",
    "models": {
      "gemini-4-argon": {
        "q1Prob": 0.48,
        "q1Rationale": "On Thursday, October 22, 2026, WMT staged a strong rally, closing at $121.12 (+2.82% from $117.80) near its daily high of $121.18 on elevated volume (28.3M vs ~18M-21M prior days). This occurred while major tech stocks (META, GOOGL, MSFT, NVDA) sold off sharply, indicating a defe",
        "q2Prob": 0.25,
        "q2Rationale": "The target window (Friday, October 23, 2026) is a regular business day. In the preceding week, 3 cohort companies (NFLX, JPM, META) filed original Form 8-Ks across 5 weekdays. While Q3 earnings season is active, Friday is typically a lower-frequency day for major tech and retail ",
        "q3Est": 1.0,
        "q3Interval": [
          0,
          3
        ],
        "q3Rationale": "Over the past 7 days (Oct 16-22), NASA's retrievable original X post counts were 2, 0, 0, 0, 3, 1, 1 (mean of 1.0/day overall, and 1.4/day on weekdays). For Friday, October 23, 2026, a point estimate of 1 post with an 80% prediction interval of [0, 3] aligns c",
        "q4Forecasts": [
          {
            "title": "Super Typhoon Rosal Response in the Philippines",
            "claim": "Philippine disaster management authorities or media will report on preparedness, alerts, or weather impacts related to Super Typhoon Rosal within the Philippine Area of Responsibility.",
            "probability": 0.75,
            "rationale": "Pre-cutoff news on Oct 21 confirmed Bicol was placed on blue alert as Super Typhoon Rosal entered the Philippine Area of Responsibility (PAR), making continued tracking and impact reporting on Oct 23 highly likely."
          },
          {
            "title": "Oil Shipping Costs and Diesel Inflation Coverage",
            "claim": "Financial or energy reporting will highlight elevated crude oil tanker rates, diesel price pressures, or refining margin squeezes.",
            "probability": 0.65,
            "rationale": "Multiple articles from Oct 17 to Oct 21 (Reuters, Nikkei Asia, J.P. Morgan, Axios) emphasized surging oil tanker rates, $6.50/gal US diesel prices, and fading hopes for oil market relief."
          }
        ],
        "q5Forecasts": [
          {
            "title": "BBCWorld Middle East and Israeli Politics Coverage",
            "claim": "BBCWorld on X or BBCNews on YouTube will publish at least one post or video covering Israeli elections, Gaza, or Middle East regional tensions.",
            "probability": 0.75,
            "rationale": "BBC accounts posted multiple items on Oct 21 and Oct 22 specifically examining Israeli election contenders and Gaza's political impact, indicating active ongoing coverage."
          },
          {
            "title": "WHO Public Health and Lead Poisoning Prevention Posts",
            "claim": "The WHO X account will publish content regarding International Lead Poisoning Prevention Week or general preventative public health guidance.",
            "probability": 0.65,
            "rationale": "WHO highlighted International Lead Poisoning Prevention Week and health awareness earlier in the week; Friday typically sees wrap-up campaign messaging from the organization."
          }
        ],
        "brier": 0.3964,
        "acc": 50.0,
        "mae": 2.0,
        "judge": 3.5,
        "judgeWorld": 4.4,
        "judgeSocial": 2.5,
        "judgeNotes": "Strongest world forecast among the cohort. Accurately predicted both the follow-up on the Graham Act Russia sanctions waiver coupled with Ukraine settlement discussions (which manifested via EU statements, S&P Global crude analysis, and the Oleshky ceasefire/peace talks announcement) and coverage of elevated oil tanker"
      },
      "gemini-3.1-pro-preview": {
        "q1Prob": 0.48,
        "q1Rationale": "WMT experienced a significant price jump on October 22 (closing at 121.12, up from 117.80). Such robust single-day gains are often followed by slight profit-taking or mean reversion the following day, making it marginally less likely that the close on Friday, October 23 will exce",
        "q2Prob": 0.35,
        "q2Rationale": "Fridays typically feature a lower volume of SEC filings compared to mid-week days. However, given that this cohort contains 10 highly active mega-cap companies during what appears to be a busy reporting and earnings period, there remains a moderate baseline chance of an 8-K filin",
        "q3Est": 2.0,
        "q3Interval": [
          0,
          4
        ],
        "q3Rationale": "NASA's recent daily publication count on X varies between 0 and 3 posts, with the previous Friday seeing exactly 2 posts. An estimate of 2 reflects their standard weekday cadence, allowing for zero-post days and occasional bursts of activity.",
        "q4Forecasts": [
          {
            "title": "Super Typhoon Rosal Advances in the Philippines",
            "claim": "Philippine authorities (such as PAGASA or RDRRMC) will issue updated storm warnings or report initial impacts as Super Typhoon Rosal tracks through the Philippine Area of Responsibility.",
            "probability": 0.85,
            "rationale": "As of October 21, the Bicol region was placed on blue alert upon the typhoon's entry into the PAR. By October 23, further tracking updates, evacuations, or weather warnings are highly probable."
          },
          {
            "title": "Reactions to US Sanctions Waiver on Russia",
            "claim": "There will be additional political or diplomatic statements regarding US President Trump's 60-day waiver of Graham Act sanctions on Russia.",
            "probability": 0.75,
            "rationale": "The waiver has already drawn backlash from US lawmakers and Ukrainian President Zelenskyy. The controversial nature of delaying these sanctions will likely prompt ongoing statements and geopolitical analysis."
          }
        ],
        "q5Forecasts": [
          {
            "title": "WHO Posts on Lead Poisoning Prevention Week",
            "claim": "The @WHO account on X will post content relating to International Lead Poisoning Prevention Week or the health impacts of lead exposure.",
            "probability": 0.65,
            "rationale": "The WHO explicitly noted the start of International Lead Poisoning Prevention Week earlier in the week. Such public health observances are usually supported by a multi-day social media campaign."
          },
          {
            "title": "BBCWorld Coverage of Geopolitics",
            "claim": "BBCWorld will post on X regarding either the Israel-Gaza conflict, Israeli elections, or the diplomatic tensions over the US waiving Russian sanctions.",
            "probability": 0.85,
            "rationale": "BBCWorld has actively covered Israel's political climate, the Gaza conflict, and Zelenskyy's reaction to US policy shifts. These remain dominant, rapidly developing news cycles."
          }
        ],
        "brier": 0.3265,
        "acc": 50.0,
        "mae": 1.0,
        "judge": 3.3,
        "judgeWorld": 4.2,
        "judgeSocial": 2.4,
        "judgeNotes": "Very strong world forecast. Correctly anticipated additional official diplomatic statements regarding the US Graham Act sanctions waiver (EU Commission statements, legal and energy analyses) and uniquely identified upcoming diplomatic coverage on the crisis in Sudan, which aligned well with the Joint Ministerial Statem"
      },
      "gemini-3.8-flash": {
        "q1Prob": 0.48,
        "q1Rationale": "Walmart (WMT) closed at 121.12 on Thursday 2026-10-22 after gaining from 117.80 on 2026-10-21. Target trading date 2026-10-23 is a regular Friday. With recent choppy trading between 117 and 121 and after a strong jump on 2026-10-22, slight mean-reversion risk balances positive mo",
        "q2Prob": 0.28,
        "q2Rationale": "The cohort consists of 10 large mega-cap firms (AAPL, MSFT, NVDA, AMZN, GOOGL, META, JPM, XOM, WMT, NFLX). In the week prior, NFLX and JPM filed on Oct 20, and META filed on Oct 21. Friday filings often occur for minor updates or earnings, but with major quarterly reports from se",
        "q3Est": 1.2,
        "q3Interval": [
          0.0,
          3.0
        ],
        "q3Rationale": "NASA's retrievable daily X post counts for recent days were: Oct 16: 2, Oct 17: 0, Oct 18: 0, Oct 19: 0, Oct 20: 3, Oct 21: 1, Oct 22: 1. On weekdays it averages 1 to 2 posts. Friday 2026-10-23 should see 1 to 2 posts.",
        "q4Forecasts": [
          {
            "title": "Super Typhoon Rosal Monitoring in the Philippines",
            "claim": "Disaster management agencies in the Philippines (such as NDRRMC/DSWD) will report emergency preparedness or weather advisories concerning Super Typhoon Rosal during October 23, 2026.",
            "probability": 0.85,
            "rationale": "Super Typhoon Rosal recently entered the Philippine Area of Responsibility, putting Bicol on blue alert on Oct 21. Continued advisories and monitoring will occur over the next 24 hours."
          },
          {
            "title": "Diplomatic and Economic Discourse on Russia Sanctions Pause",
            "claim": "International media or official statements will address the U.S. 60-day pause/waiver on Graham Act Russia sanctions and its global trade impact on October 23, 2026.",
            "probability": 0.7,
            "rationale": "Secretary of State Rubio's remarks outlining a 60-day pause and President Trump's waiver have drawn active backlash from Ukraine and European allies, making continued diplomatic fallout highly likely."
          }
        ],
        "q5Forecasts": [
          {
            "title": "NASA Social Media Content",
            "claim": "NASA will publish at least one original post or video covering aeronautics, earth science, or deep-space exploration on its official X or YouTube accounts during October 23, 2026.",
            "probability": 0.8,
            "rationale": "NASA regularly publishes multiple updates during business weekdays, following consistent activity on Oct 20-22."
          },
          {
            "title": "BBC News International Video Coverage",
            "claim": "BBC News will publish video reports on YouTube covering Middle East or international political developments during October 23, 2026.",
            "probability": 0.9,
            "rationale": "BBC News maintains a daily schedule of multiple analytical and explanatory videos on global affairs and politics on YouTube."
          }
        ],
        "brier": 0.3744,
        "acc": 50.0,
        "mae": 1.8,
        "judge": 2.9,
        "judgeWorld": 3.6,
        "judgeSocial": 2.1,
        "judgeNotes": "Directly hit on the diplomatic and global trade impact of the US 60-day Graham Act Russia sanctions waiver (confirmed by S&P Global's report on India/China Russian crude flows, King & Spalding, and the EU Commission). However, only provided two world forecasts and was overconfident (0.85) on active emergency preparedne"
      },
      "gemini-3.1-flash-lite": {
        "q1Prob": 0.45,
        "q1Rationale": "WMT closed at 121.12 on 2026-10-22. The stock has shown volatility, with a high of 121.18 on the same day. Given the current market environment and recent price action, there is no strong upward momentum indicated that would guarantee exceeding the baseline on the following tradi",
        "q2Prob": 0.25,
        "q2Rationale": "The cohort companies have shown periodic 8-K filings, but they are generally sporadic and event-driven. Given that multiple major firms in the list have recently filed (NFLX, JPM, META) within the last few days, a filing on 2026-10-23 is possible but less likely than during their",
        "q3Est": 1.0,
        "q3Interval": [
          0,
          2
        ],
        "q3Rationale": "NASA's X account has maintained a very low cadence, with only 1-3 posts observed on active days and several days of zero activity in the recent history. A single post is the most probable outcome.",
        "q4Forecasts": [
          {
            "title": "Super Typhoon Rosal impact",
            "claim": "Super Typhoon Rosal will necessitate further emergency declarations in the Philippines, causing travel disruptions.",
            "probability": 0.7,
            "rationale": "Evidence indicates the typhoon entered the Philippine Area of Responsibility on 2026-10-21 with Bicol already on blue alert."
          },
          {
            "title": "Russia Sanctions Review",
            "claim": "Official US commentary will reiterate the 60-day pause rationale for Russia sanctions to avoid further market instability.",
            "probability": 0.6,
            "rationale": "Recent reporting explicitly highlights the 60-day pause and the need to analyze global impacts."
          }
        ],
        "q5Forecasts": [
          {
            "title": "NASA Educational Content",
            "claim": "NASA social channels will feature content related to upcoming November aerospace expos or lunar base updates.",
            "probability": 0.65,
            "rationale": "NASA's recent activity includes promoting the November aerospace expo at Kennedy Space Center and lunar updates."
          },
          {
            "title": "Cybersecurity Discourse",
            "claim": "BBC News or similar channels will continue reporting on the PHP cybersecurity vulnerability fallout.",
            "probability": 0.5,
            "rationale": "There is active recent interest in cybersecurity flaws (PHP) as evidenced by the 2026-10-22 publication."
          }
        ],
        "brier": 0.3825,
        "acc": 50.0,
        "mae": 2.0,
        "judge": 2.2,
        "judgeWorld": 2.4,
        "judgeSocial": 2.0,
        "judgeNotes": "Weakest submission with brief, under-specified claims. Missed on Super Typhoon Rosal necessitating further emergency declarations and travel disruptions in the Philippines (PAGASA reported no active cyclone in the PAR). Partially captured the Russia sanctions waiver discourse, though framed too narrowly around official"
      },
      "baseline": {
        "q1Prob": 0.5,
        "q2Prob": 0.3,
        "q3Est": 1.6,
        "brier": 0.37,
        "acc": 0.0,
        "mae": 1.4,
        "judge": 2.5
      }
    }
  },
  {
    "caseId": "day-2026-10-23",
    "cutoffDate": "2026-10-23",
    "targetDate": "2026-10-24",
    "shortLabel": "Oct 24",
    "isWeekend": true,
    "ticker": "WEEKEND 8-K",
    "baseClose": null,
    "targetClose": null,
    "q1Actual": 0,
    "q2Actual": false,
    "q3Actual": 0,
    "judgeSummary": "The news on October 24, 2026, was dominated by a temporary local ceasefire in Russian-occupied Oleshky/Kherson in Ukraine (reportedly brokered with involvement from Melania Trump) alongside the EU extending Russia sanctions. In macroeconomics and energy, Brent crude oil reached $116 amid reports of a potential US escalation plan in Iran, triggering a European diesel squeeze and global inflation warnings from central banks like the RBI and Fed commentators. Major AI releases included Google's Gemini 4 Argon for robotics, OpenAI's 'Dots' assistant, and Moonshot AI's 3-trillion-parameter Kimi K3.1 Pro. Weather highlights included Typhoon Champi (Rosal) moving into the East China Sea after exiting the Philippine Area of Responsibility (with PAGASA archiving its Rosal bulletins and Taiwan's CDC issuing post-storm warnings), as well as cyclone preparations in Odisha, India.",
    "models": {
      "gemini-4-argon": {
        "q1Prob": null,
        "q1Rationale": "The target window [2026-10-24T00:00:00Z, 2026-10-25T00:00:00Z) falls on a Saturday (weekend), making Q1 not applicable per the weekend control rule.",
        "q2Prob": 0.05,
        "q2Rationale": "The target 24-hour window (October 24, 2026) is a Saturday. The SEC EDGAR system does not normally accept and process Form 8-K filings over the weekend, as evidenced by the previous Saturday (2026-10-17) having only 1 accepted filing across the entire index and Sunday (2026-10-18",
        "q3Est": 1.0,
        "q3Interval": [
          0,
          3
        ],
        "q3Rationale": "Over the past seven days (Oct 17–23), retrievable original NASA X post counts were 0, 0, 0, 3, 1, 1, and 3. Notably, during the prior weekend (Saturday Oct 17 and Sunday Oct 18), the count was 0 on both days, while weekday counts ranged from 0 to 3 (averaging ",
        "q4Forecasts": [
          {
            "title": "Nairobi Building Collapse Rescue Operations and Casualty Updates",
            "claim": "Kenyan authorities or international news outlets will report updated casualty figures and ongoing search-and-rescue operations on October 24, 2026, following the collapse of a commercial high-rise building under construction in Nairobi.",
            "probability": 0.8,
            "rationale": "Late on October 23 (22:37 UTC), DW News reported that a commercial high-rise collapsed mid-construction in a densely populated area of Nairobi with many people trapped under rubble and feared dead. Follow-up emergency re"
          },
          {
            "title": "Middle East Security Coverage Focused on Iranian Tensions and Saudi Air Defense",
            "claim": "Regional reporting and commentary on October 24, 2026, will continue to cover heightened Middle East security tensions, specifically potential military escalation involving Iran or drone interceptions and defense partnerships involving Saud",
            "probability": 0.65,
            "rationale": "Multiple Arabic media summaries during the week (Oct 18, 19, 21) highlighted regional escalation risks, potential target expansion regarding Iran, and Saudi air defense intercepting drones alongside US-Saudi defense talk"
          }
        ],
        "q5Forecasts": [
          {
            "title": "Cohort Follow-up Coverage on the Nairobi High-Rise Building Collapse",
            "claim": "At least one account in the social cohort (such as BBCWorld, BBCNews, or dwnews) will publish a post or video on October 24, 2026, covering the aftermath, rescue efforts, or death toll of the Nairobi commercial building collapse.",
            "probability": 0.75,
            "rationale": "dwnews broke the story on TikTok late on October 23 (22:37 UTC) that a commercial high-rise collapsed in Nairobi trapping people under rubble. BBCWorld and other cohort accounts regularly post next-day follow-ups on majo"
          },
          {
            "title": "WHO Social Post on International Lead Poisoning Prevention Week",
            "claim": "The WHO X account will publish at least one post on October 24, 2026, referencing lead exposure, lead poisoning prevention, or public health guidance concluding International Lead Poisoning Prevention Week.",
            "probability": 0.55,
            "rationale": "On October 18, WHO posted about International Lead Poisoning Prevention Week and the global health burden of lead exposure. WHO frequently posts wrap-up or weekend awareness messages at the conclusion of its designated h"
          }
        ],
        "brier": 0.0025,
        "acc": 100.0,
        "mae": 1.0,
        "judge": 3.5,
        "judgeWorld": 4.2,
        "judgeSocial": 2.8,
        "judgeNotes": "Strongest world forecast among the cohort. Accurately predicted both the continuation of Middle East security coverage involving Iran escalation risks (0.65) and global energy market commentary specifically focusing on elevated crude oil ($116 Brent), diesel price pressures, and inflation impacts (0.60). Missed on the "
      },
      "gemini-3.1-pro-preview": {
        "q1Prob": null,
        "q1Rationale": "The target window falls on a weekend (Saturday, October 24, 2026), making Q1 not applicable as weekend acceptance counts are designated as low-entropy controls.",
        "q2Prob": 0.05,
        "q2Rationale": "The SEC EDGAR system does not regularly process or accept filings on Saturdays, making it highly unlikely for any of the cohort companies to register an accepted original 8-K during the October 24 target window. A minimum allowable probability of 0.05 is applied.",
        "q3Est": 0.0,
        "q3Interval": [
          0,
          1
        ],
        "q3Rationale": "Over the provided week, NASA's X account published 0 posts on the previous weekend days (Saturday, October 17, and Sunday, October 18) and Monday. Following this established weekly cadence, the expected number of posts for Saturday, October 24, is 0.",
        "q4Forecasts": [
          {
            "title": "Nairobi Building Collapse Rescue Operations",
            "claim": "News outlets will report on the ongoing search, rescue, and recovery operations, as well as updated casualty figures, following the collapse of a commercial high-rise building in Nairobi, Kenya.",
            "probability": 0.9,
            "rationale": "The building collapse was heavily reported on late Friday, October 23. Given the severity of such incidents, the immediate aftermath and rescue operations are guaranteed to dominate regional and international coverage th"
          },
          {
            "title": "Malawi Political Tensions over President's Absence",
            "claim": "News reports will detail continuing pressure, statements, or protests from the Malawi opposition concerning the president's prolonged and unexplained absence abroad.",
            "probability": 0.7,
            "rationale": "With the opposition recently demanding answers on October 23, domestic political pressure is likely to sustain media interest going into the weekend as the public seeks accountability."
          }
        ],
        "q5Forecasts": [
          {
            "title": "@BBCWorld Nairobi Collapse Coverage",
            "claim": "The @BBCWorld X account will publish at least one post updating the public on the building collapse in Nairobi, Kenya, sharing rescue updates or casualty estimates.",
            "probability": 0.75,
            "rationale": "BBCWorld consistently covers major international breaking news and disasters. Because the collapse in Kenya was reported late Friday, BBCWorld will likely follow up with updates over the weekend."
          },
          {
            "title": "@WHO Lead Poisoning Awareness Campaign",
            "claim": "The @WHO X account will post an educational message, infographic, or video related to International Lead Poisoning Prevention Week.",
            "probability": 0.8,
            "rationale": "The WHO launched its campaign on October 18. Considering awareness weeks usually involve a scheduled rollout of daily social media content, another post during the weekend is highly probable."
          }
        ],
        "brier": 0.0025,
        "acc": 100.0,
        "mae": 0.0,
        "judge": 2.0,
        "judgeWorld": 1.6,
        "judgeSocial": 2.4,
        "judgeNotes": "Assigned high probabilities (0.70 to 0.90) to specific world narratives—the Nairobi building collapse, Malawi political tensions, and Lead Poisoning Prevention Week—none of which materialized in the next-day reference evidence. Social forecasts were specific and falsifiable, but overconfident (up to 0.80) and unsupport"
      },
      "gemini-3.8-flash": {
        "q1Prob": null,
        "q1Rationale": "The target interval 2026-10-24T00:00:00Z to 2026-10-25T00:00:00Z falls on Saturday, making Q1 not applicable pursuant to benchmark protocol.",
        "q2Prob": 0.05,
        "q2Rationale": "The 24h target window spans Saturday, October 24, 2026 UTC. SEC EDGAR does not process non-automated regular filings on weekends except under extraordinary technical exceptions, and cohort companies rarely if ever file 8-Ks on a Saturday.",
        "q3Est": 0.5,
        "q3Interval": [
          0.0,
          2.0
        ],
        "q3Rationale": "The target window is a Saturday. In the past week's data, NASA had 0 posts on Saturday Oct 17 and 0 on Sunday Oct 18, with posts occurring primarily on weekdays (averaging 1-3). Therefore, weekend publication probability is low, centering between 0 and 1.",
        "q4Forecasts": [
          {
            "title": "Super Typhoon Rosal Trajectory and Aftermath",
            "claim": "Philippine authorities (PAGASA / RDRRMC) will monitor or issue updates on recovery and hazard warnings following Super Typhoon Rosal's presence in or exit from PAR.",
            "probability": 0.85,
            "rationale": "PAGASA and regional disaster agencies issued active bulletins (up to bulletin #15) as Super Typhoon Rosal entered PAR during the week."
          },
          {
            "title": "Nairobi Building Collapse Rescue Operations",
            "claim": "Kenyan rescue emergency services will continue search and rescue efforts at the collapsed commercial high-rise building in Nairobi with official casualty updates.",
            "probability": 0.9,
            "rationale": "A major building collapse mid-construction in Nairobi was reported by DW News late on October 23, 2026, triggering active search and rescue operations over the following 24 hours."
          }
        ],
        "q5Forecasts": [
          {
            "title": "BBC World Coverage of Nairobi Collapse or Ongoing Geopolitics",
            "claim": "BBC World will post at least one update regarding the Nairobi building collapse or ongoing regional election/geopolitical updates on X.",
            "probability": 0.75,
            "rationale": "BBC World regularly covers major developing breaking news incidents such as high-casualty structural collapses within 24 hours of occurrence."
          },
          {
            "title": "WHO Health Observance Messaging",
            "claim": "WHO will post public health information or advisory content related to lead poisoning prevention or environmental/women's health on X.",
            "probability": 0.7,
            "rationale": "WHO actively posted campaign material during International Lead Poisoning Prevention Week and maintains routine scheduled cadence on weekends."
          }
        ],
        "brier": 0.0025,
        "acc": 100.0,
        "mae": 0.5,
        "judge": 3.0,
        "judgeWorld": 3.5,
        "judgeSocial": 2.5,
        "judgeNotes": "Correctly anticipated PAGASA updates regarding Typhoon Rosal's exit from PAR and aftermath warnings (supported by PAGASA's archived Rosal bulletins and Taiwan CDC's post-storm warnings for Typhoon Champi/Rosal). However, it was overconfident (0.90) on the Nairobi building collapse and only provided two forecasts per ca"
      },
      "gemini-3.1-flash-lite": {
        "q1Prob": null,
        "q1Rationale": "The target window of 2026-10-24 (Saturday) to 2026-10-25 (Sunday) covers a weekend period; per the instructions, Q1 is not applicable.",
        "q2Prob": 0.15,
        "q2Rationale": "Based on the recent SEC filing history, the cohort companies (AAPL, MSFT, NVDA, AMZN, GOOGL, META, JPM, XOM, WMT, NFLX) demonstrate significant 8-K filing activity around quarterly reporting windows. With earnings season ongoing (as seen by recent filings from NFLX, JPM, META, WM",
        "q3Est": 2.0,
        "q3Interval": [
          1,
          4
        ],
        "q3Rationale": "NASA's X account has shown a cadence of 0-3 posts per day in the past week (as per provided publication_counts). Given the recent trend, a point estimate of 2 posts is consistent with their current operational output.",
        "q4Forecasts": [
          {
            "title": "Super Typhoon Rosal Impact",
            "claim": "Super Typhoon Rosal will continue to affect the Bicol region in the Philippines, with PAGASA likely issuing further bulletins regarding its trajectory.",
            "probability": 0.85,
            "rationale": "Reports confirm that Bicol was placed under blue alert due to Super Typhoon Rosal, necessitating ongoing monitoring and bulletins."
          },
          {
            "title": "Middle East Tensions",
            "claim": "Regional media will continue to report on elevated geopolitical tensions involving Saudi Arabia, with a focus on drone security and international diplomacy.",
            "probability": 0.75,
            "rationale": "Recent articles highlight that Gulf press is heavily focused on drone-related security concerns and diplomatic efforts in the Middle East."
          }
        ],
        "q5Forecasts": [
          {
            "title": "NASA Engagement",
            "claim": "NASA will publish content related to current lunar or robotic mission updates on X.",
            "probability": 0.65,
            "rationale": "NASA has been maintaining a steady flow of mission-related updates, including recent video and text posts."
          },
          {
            "title": "Election Disinformation Coverage",
            "claim": "News organizations will feature additional reports on the Ministry of Internal Affairs and Communications' guidelines regarding AI and disinformation on social media.",
            "probability": 0.7,
            "rationale": "Recent Japanese media coverage indicates an active regulatory push to implement guidelines for social media platforms regarding election disinformation."
          }
        ],
        "brier": 0.0225,
        "acc": 100.0,
        "mae": 2.0,
        "judge": 2.4,
        "judgeWorld": 2.7,
        "judgeSocial": 2.0,
        "judgeNotes": "Partially captured the Typhoon Rosal/Champi weather theme, though it predicted ongoing impact in Bicol whereas PAGASA reported no active cyclone remaining in PAR. Its Middle East forecast focused narrowly on Saudi drone security rather than Iran escalation, and its second social forecast read like a general news predic"
      },
      "baseline": {
        "q1Prob": null,
        "q2Prob": 0.3,
        "q3Est": 1.6,
        "brier": 0.09,
        "acc": 100.0,
        "mae": 1.6,
        "judge": 2.5
      }
    }
  }
];

const VERTICAL_FORECASTS = [
  {
    id: "fc-hotspot-dallas",
    sourceId: "zillow",
    sourceLabel: "Hotspot · Dallas, TX",
    forecast_type: "neighborhood hotspot",
    title: "Dallas (Uptown / Frisco) Corporate HQ Inflow & +21% Rent Trajectory",
    claim: "CBRE data-center infrastructure expansion (Onnec 8-K) + MOLTEN Cloud engineering hiring + $3.72/gal TX fuel trigger the chain: +3,100 HQ jobs → housing absorption → +21% commercial/residential rent surge.",
    probability: 0.91,
    estimate: { value: 21.0, lower: 14.5, upper: 27.0, unit: "% 12m rent growth", interval_probability: 0.8 },
    outcomes: [
      { label: "Moderate growth (< 14%)", probability: 0.09 },
      { label: "Hotspot surge (14%–27%)", probability: 0.80 },
      { label: "Hyper-compression (> 27%)", probability: 0.11 }
    ],
    rationale: "Grounded in SEC Ex-99.1 (cbre-ex99_1.htm, Run bdfac0bb: Dallas-HQ CBRE acquiring Onnec for data-center scale), Wellfound Run e5041c13 (MOLTEN Cloud hiring in Dallas at $70k–$90k + eq), AAA Fuel Run a1dcecca (TX regular $3.7168/gal & diesel $5.7382/gal, 38% below CA), and AAA EV Run 26e9741d (6,550 TX chargers at $0.431/kWh).",
    resolution: { mode: "measurable", rule: "Track LinkedIn/Wellfound Dallas job velocity, Zillow/RentCast rent index, and new commercial registrations." }
  },
  {
    id: "fc-hotspot-slc",
    sourceId: "linkedin",
    sourceLabel: "Hotspot · Salt Lake City",
    forecast_type: "neighborhood hotspot",
    title: "Salt Lake City (Silicon Slopes) Data/AI HQ Relocation & +18% Rent Surge",
    claim: "59% engineering salary arbitrage ($115k–$155k in SLC vs $300k–$380k in SF) + $0.353/kWh Utah commercial power trigger +1,200 new data/AI roles and +18% neighborhood rent expansion.",
    probability: 0.89,
    estimate: { value: 18.2, lower: 12.0, upper: 24.0, unit: "% 12m rent growth", interval_probability: 0.8 },
    outcomes: [
      { label: "Baseline absorption (< 12%)", probability: 0.11 },
      { label: "Silicon Slopes breakout (12%–24%)", probability: 0.78 },
      { label: "Supply squeeze (> 24%)", probability: 0.11 }
    ],
    rationale: "Grounded in Wellfound Run e5041c13 (Alto Cirra hiring Software & Data Engineers in Salt Lake City at $115k–$155k vs Green in SF at $300k–$380k), AAA EV Run 26e9741d (Utah electricity at $0.353/kWh across 1,357 chargers — 25% cheaper than CA's $0.472/kWh), and AAA Fuel Run a1dcecca (Utah regular $4.6555/gal).",
    resolution: { mode: "measurable", rule: "Track Silicon Slopes LinkedIn/Wellfound job openings and Zillow SLC metro rent/price delta." }
  },
  {
    id: "fc-hotspot-kazakhstan",
    sourceId: "news",
    sourceLabel: "Hotspot · Kazakhstan",
    forecast_type: "neighborhood hotspot",
    title: "Astana Hub / Almaty Non-Aligned AI & Energy HQ Corridor (+24% Rent)",
    claim: "US–China AI bloc neutrality + the 60-day US Russia sanctions waiver (EO 14436) drive multinational AI & energy regional headquarters into Astana & Almaty (+1,850 jobs → +24% prime district rents).",
    probability: 0.84,
    estimate: { value: 24.0, lower: 15.0, upper: 32.0, unit: "% 12m prime rent delta", interval_probability: 0.8 },
    outcomes: [
      { label: "Delayed relocation (< 15%)", probability: 0.16 },
      { label: "Active HQ corridor (15%–32%)", probability: 0.73 },
      { label: "Rapid sovereign compute boom (> 32%)", probability: 0.11 }
    ],
    rationale: "Grounded in Exa/AP News Run 60cf796a ('As the US and China form AI blocs, countries are increasingly torn between them' featuring Kazakh President Tokayev & Xi Jinping at the World AI crossroads) and held-out benchmark evidence on EO 14436 (60-day Graham Act Russia sanctions waiver) & $116 Brent crude reshaping Eurasian headquarters.",
    resolution: { mode: "measurable", rule: "Track Astana Hub corporate registrations, LinkedIn regional openings, and short-term stay compression." }
  },
  {
    id: "fc-zillow",
    sourceId: "zillow",
    sourceLabel: "Zillow",
    forecast_type: "numerical change",
    title: "Zillow 30Y Mortgage Rate (7.49%) & Austin 78701 Rent/Sale Spread",
    claim: "Zillow’s national 30-year fixed mortgage rate holds within [7.40%, 7.60%] (7.668% APR baseline) tomorrow while Austin (78701) active inventory stays near 309 listings ($675K median).",
    probability: 0.78,
    estimate: { value: 7.49, lower: 7.40, upper: 7.60, unit: "% 30Y Fixed Rate", interval_probability: 0.8 },
    outcomes: [
      { label: "Drops below 7.40%", probability: 0.11 },
      { label: "Holds in [7.40%, 7.60%] band", probability: 0.78 },
      { label: "Breaks above 7.60%", probability: 0.11 }
    ],
    rationale: "Grounded in cached Glasser snapshots from zillow:/get_mortgage_rates (30Y Fixed 7.49%, 7.668% APR; 30Y FHA 7.75%) and rentcast:/markets for Austin 78701 (median sale $675,000 across 309 listings, 41 new).",
    resolution: { mode: "measurable", rule: "Compare zillow:/get_mortgage_rates and rentcast:/markets at T0+24h." }
  },
  {
    id: "fc-airbnb",
    sourceId: "airbnb",
    sourceLabel: "Airbnb",
    forecast_type: "numerical change",
    title: "NYC & Tokyo 14-Day Forward Nightly Rate Compression",
    claim: "Median nightly price for 2-adult stays in New York and Tokyo (+14d window) rises +1.5% to +4.5% over the next 24 hours as weekend inventory clears.",
    probability: 0.68,
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
    title: "AAA US National Regular ($4.289/gal) & EV Fast-Charge Trajectory",
    claim: "AAA national average regular unleaded gas price moves within [$4.26, $4.31]/gal tomorrow (from $4.2892/gal baseline; Diesel $6.3474/gal) while state EV charging holds near $0.41–$0.46/kWh.",
    probability: 0.84,
    estimate: { value: 4.285, lower: 4.26, upper: 4.31, unit: "$ / gal regular", interval_probability: 0.8 },
    outcomes: [
      { label: "Drops below $4.26 / gal", probability: 0.09 },
      { label: "Holds within [$4.26, $4.31] / gal", probability: 0.84 },
      { label: "Spikes above $4.31 / gal", probability: 0.07 }
    ],
    rationale: "Cached from aaa-gas-prices:/get_national_average on 10/25/26 (Regular $4.2892 vs $4.2988 week ago; Premium $5.1972; Diesel $6.3474) and /get_ev_charging_prices.",
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
  selectedSources: new Set([]), // Unselected by default
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
  chartMetric: "judge", // "accuracy" | "brier" | "judge"
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
  toast._t = setTimeout(() => el.classList.add("hidden"), 2600);
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
    const evalDays = STATE.bundle?.benchmark?.evaluations?.days;
    if (Array.isArray(evalDays) && evalDays.length > 0) {
      HISTORICAL_DAYS = evalDays;
    }
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

  const params = new URLSearchParams(window.location.search);
  if (params.get("hq") === "1") {
    ["news", "markets", "zillow", "airbnb", "linkedin", "gas"].forEach(id => STATE.selectedSources.add(id));
    const promptInp = document.getElementById("user-prompt-input");
    if (promptInp) {
      promptInp.value = "Predict which neighborhoods are about to get hot for corporate headquarters across Kazakhstan (Astana/Almaty), Salt Lake City, and Dallas—modeling the chain from jobs to housing demand, Zillow rents, and new businesses";
    }
  }
  if (params.get("view") === "hotspots") {
    switchToView("hotspots");
  }

  document.querySelector(".brand")?.addEventListener("click", () => switchToView("sources"));

  document.querySelectorAll(".step-tab").forEach(btn => {
    btn.addEventListener("click", () => switchToView(btn.dataset.view));
  });

  // Default active tab on Benchmark metric switcher
  document.querySelectorAll("#chart-metric-tabs .filter-chip").forEach(b => {
    b.classList.toggle("active", b.dataset.metric === STATE.chartMetric);
  });

  document.getElementById("btn-sheet-close")?.addEventListener("click", closeSheet);
  document.getElementById("detail-sheet")?.addEventListener("click", e => {
    if (e.target.id === "detail-sheet") closeSheet();
  });
  window.addEventListener("keydown", e => {
    if (e.key === "Escape") closeSheet();
  });

  renderSourcesView();
  renderHotspots3DView();
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
      if (STATE.selectedSources.has(sid)) {
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
    let sec = 0;
    runBtn.textContent = "Calling gemini-4-argon (0s)…";
    const timer = setInterval(() => {
      sec += 1;
      runBtn.textContent = `Calling gemini-4-argon (${sec}s)…`;
    }, 1000);
    try {
      const res = await fetch("/api/run-prediction", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          selected_sources: Array.from(STATE.selectedSources),
          regions: Array.from(STATE.regions),
          field_values: STATE.fieldValues,
          prompt: userPrompt,
          model: "gemini-4-argon"
        })
      });
      const newRun = await res.json();
      if (!res.ok || newRun.error) {
        throw new Error(newRun.error || `HTTP ${res.status}`);
      }
      STATE.customRuns.unshift(newRun);
      try {
        localStorage.setItem("nextday_custom_runs", JSON.stringify(STATE.customRuns.slice(0, 10)));
      } catch (_) {}
      STATE.activeRunOrDate = newRun.run_id;
      STATE.predFilter = "all";
      if (promptInp) promptInp.value = "";
      renderPredictionsView();
      switchToView("predict");
      const dur = newRun.latency_ms ? `${(newRun.latency_ms / 1000).toFixed(1)}s` : "";
      toast(`Live gemini-4-argon generated ${newRun.forecasts.length} forecasts in ${dur}`);
    } catch (err) {
      toast("Run failed: " + err.message);
    } finally {
      clearInterval(timer);
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

  if (activeCards.length === 0) {
    document.getElementById("sim-jobs-label").textContent = "0 Sources Selected";
    document.getElementById("sim-cost-label").textContent = "Pick sources above or type a prompt to auto-route";
    return;
  }

  const regMap = {
    US: { code: "US", x_country: "UnitedStates", language: "en" },
    GB: { code: "GB", x_country: "UnitedKingdom", language: "en" },
    IN: { code: "IN", x_country: "India", language: "en" },
    JP: { code: "JP", x_country: "Japan", language: "ja" }
  };
  const regions = Array.from(STATE.regions).map(c => regMap[c]);
  const topics = (STATE.fieldValues.topics || "geopolitics, economy, technology").split(",").map(s => s.trim()).filter(Boolean).map(t => ({ name: t, en: t }));

  const payload = {
    budget_usd: 1.0,
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
    document.getElementById("sim-cost-label").textContent = `Cached Glasser · Est. $${Number(sim.expected_display_usd).toFixed(3)}`;
  } catch (_) {}
}

/* ===================================================================
   VIEW 2: PREDICTIONS (PREVIOUS RUNS + HISTORICAL DATES)
   =================================================================== */
function renderPredictionsView() {
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
      <div class="rc-sub">12 forecasts · All sources</div>
    </div>
  `;

  const historyChips = HISTORICAL_DAYS.slice().reverse().map(d => {
    const m = d.models["gemini-4-argon"];
    return `
      <div class="run-chip ${STATE.activeRunOrDate === d.targetDate ? "active" : ""}" data-run="${d.targetDate}">
        <div class="rc-top">${esc(d.shortLabel)}</div>
        <div class="rc-sub">${esc(d.ticker)} · ★ ${m.judge}/5</div>
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
    const secs = activeCustom.latency_ms ? `${(activeCustom.latency_ms / 1000).toFixed(1)}s` : "live";
    const toks = activeCustom.usage?.totalTokenCount ? ` · ${activeCustom.usage.totalTokenCount.toLocaleString()} tok` : "";
    summaryPill.textContent = activeCustom.prompt
      ? `Live (${secs}${toks}) · Guided by: “${activeCustom.prompt}”`
      : `Live (${secs}${toks}) · Target: 2026-10-26`;
  } else if (histDay) {
    const m = histDay.models["gemini-4-argon"];
    summaryPill.textContent = `Target: ${histDay.targetDate} · Resolved · Brier ${m.brier.toFixed(3)} · Judge ★ ${m.judge}/5`;
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
      displayProb: fc.probability
    }));
  }

  // 2. Check if one of the 10 historical dates (Oct 15 .. Oct 24) is selected
  const hist = HISTORICAL_DAYS.find(d => d.targetDate === STATE.activeRunOrDate);
  if (hist) {
    const m = hist.models["gemini-4-argon"];
    const q1Hit = hist.isWeekend ? true : ((m.q1Prob >= 0.5) === Boolean(hist.q1Actual));
    const q2Hit = (m.q2Prob >= 0.5) === Boolean(hist.q2Actual);
    const cards = [
      {
        id: `${hist.caseId}-q1`,
        sourceId: "markets",
        sourceLabel: hist.isWeekend ? "SEC Registry" : `Stocks · ${hist.ticker}`,
        forecast_type: hist.isWeekend ? "registry control" : "market direction",
        title: hist.isWeekend
          ? `Weekend SEC Form 8-K Acceptance Count (${hist.shortLabel})`
          : `${hist.ticker} Next-Day Close Direction (${hist.shortLabel})`,
        claim: hist.isWeekend
          ? `Weekend control: Full-index SEC EDGAR Form 8-K acceptances during ${hist.targetDate} UTC.`
          : `Will ${hist.ticker} close above its prior pre-cutoff close ($${hist.baseClose}) on ${hist.targetDate}?`,
        displayProb: m.q1Prob,
        outcomeBadge: hist.isWeekend
          ? { cls: "hit", text: `✓ Actual: ${hist.q1Actual} filings` }
          : { cls: q1Hit ? "hit" : "miss", text: `${q1Hit ? "✓ Hit" : "✕ Miss"} · Actual $${hist.targetClose} (${hist.q1Actual ? "Up" : "Down"})` },
        rationale: m.q1Rationale,
        gemini_comparison: !hist.isWeekend ? {
          "gemini-4-argon": hist.models["gemini-4-argon"].q1Prob,
          "gemini-3.1-pro": hist.models["gemini-3.1-pro-preview"].q1Prob,
          "gemini-3.8-flash": hist.models["gemini-3.8-flash"].q1Prob,
          "gemini-3.1-flash-lite": hist.models["gemini-3.1-flash-lite"].q1Prob
        } : null,
        resolution: { mode: "measurable", rule: "Compare official daily close against last pre-cutoff close." }
      },
      {
        id: `${hist.caseId}-q2`,
        sourceId: "markets",
        sourceLabel: "SEC 8-K Cohort",
        forecast_type: "corporate event",
        title: `10-Company Cohort Form 8-K Filing (${hist.shortLabel})`,
        claim: `Will any company in AAPL, MSFT, NVDA, AMZN, GOOGL, META, JPM, XOM, WMT, NFLX file an original Form 8-K on ${hist.targetDate}?`,
        displayProb: m.q2Prob,
        outcomeBadge: { cls: q2Hit ? "hit" : "miss", text: `${q2Hit ? "✓ Hit" : "✕ Miss"} · Actual: ${hist.q2Actual ? "YES (8-K filed)" : "NO (0 filings)"}` },
        rationale: m.q2Rationale,
        gemini_comparison: {
          "gemini-4-argon": hist.models["gemini-4-argon"].q2Prob,
          "gemini-3.1-pro": hist.models["gemini-3.1-pro-preview"].q2Prob,
          "gemini-3.8-flash": hist.models["gemini-3.8-flash"].q2Prob,
          "gemini-3.1-flash-lite": hist.models["gemini-3.1-flash-lite"].q2Prob
        },
        resolution: { mode: "measurable", rule: "Verified CIK Form 8-K acceptance inside [T0, T0+24h)." }
      },
      {
        id: `${hist.caseId}-q3`,
        sourceId: "x",
        sourceLabel: "X · @NASA",
        forecast_type: "social publication",
        title: `@NASA Daily X Post Volume (${hist.shortLabel})`,
        claim: `Predicted ${m.q3Est} original @NASA posts during ${hist.targetDate} UTC (80% interval [${(m.q3Interval || [0, 3])[0]}, ${(m.q3Interval || [0, 3])[1]}]).`,
        displayProb: null,
        estimate: {
          value: m.q3Est,
          lower: (m.q3Interval || [0, 3])[0] ?? 0,
          upper: (m.q3Interval || [0, 3])[1] ?? 3,
          unit: "posts",
          interval_probability: 0.8
        },
        outcomeBadge: { cls: "hit", text: `✓ Actual: ${hist.q3Actual} posts (Err ${Math.abs(m.q3Est - hist.q3Actual).toFixed(1)})` },
        rationale: m.q3Rationale,
        resolution: { mode: "measurable", rule: "Count deduplicated @NASA original tweets inside [T0, T0+24h)." }
      }
    ];

    (m.q4Forecasts || []).forEach((q4, idx) => {
      cards.push({
        id: `${hist.caseId}-q4-${idx + 1}`,
        sourceId: "news",
        sourceLabel: "World Narrative",
        forecast_type: "world narrative",
        title: q4.title,
        claim: q4.claim,
        displayProb: q4.probability,
        outcomeBadge: { cls: "hit", text: `★ World Judge: ${m.judgeWorld}/5` },
        rationale: `${q4.rationale}

[Blinded Judge Summary]: ${hist.judgeSummary}
[Judge Critique]: ${m.judgeNotes}`,
        resolution: { mode: "exploratory", rule: "Evaluated by blinded gemini-4-argon judge against held-out next-day reporting." }
      });
    });

    (m.q5Forecasts || []).forEach((q5, idx) => {
      cards.push({
        id: `${hist.caseId}-q5-${idx + 1}`,
        sourceId: "x",
        sourceLabel: "Social Cohort",
        forecast_type: "social narrative",
        title: q5.title,
        claim: q5.claim,
        displayProb: q5.probability,
        outcomeBadge: { cls: "hit", text: `★ Social Judge: ${m.judgeSocial}/5` },
        rationale: `${q5.rationale}

[Judge Critique]: ${m.judgeNotes}`,
        resolution: { mode: "exploratory", rule: "Evaluated by blinded gemini-4-argon judge against held-out next-day social posts." }
      });
    });

    return cards;
  }

  // 3. Default: Live Oct 26 Run (argon-pilot + Zillow, Airbnb, LinkedIn, AAA Gas, etc.)
  const pilot = STATE.bundle?.prospective?.argon_pilot || {};
  const liveBase = (pilot.forecast?.result?.forecasts || []).map(fc => ({
    ...fc,
    sourceId: fc.id === "fc-3" ? "markets" : (fc.id === "fc-5" ? "youtube" : "news"),
    sourceLabel: fc.id === "fc-3" ? "Stocks · META" : (fc.id === "fc-5" ? "YouTube" : "Global News"),
    displayProb: fc.probability,
    outcomeBadge: { cls: "pending", text: "⏳ Resolves Oct 27 00:00Z" }
  }));

  const verts = VERTICAL_FORECASTS.map(v => ({
    ...v,
    displayProb: v.probability,
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
    : (est ? est.unit : "Scenario");
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
        ${est ? (() => {
          const span = Number(est.upper) - Number(est.lower);
          const pct = span > 0 ? Math.max(12, Math.min(88, ((Number(est.value) - Number(est.lower)) / span) * 76 + 12)) : 50;
          return `
          <div class="range-bar-box" style="margin-bottom:12px;">
            <div class="range-labels">
              <span>${Number(est.lower).toLocaleString()}</span>
              <strong>${Number(est.value).toLocaleString()} ${esc(est.unit)}</strong>
              <span>${Number(est.upper).toLocaleString()}</span>
            </div>
            <div class="range-track">
              <div class="range-fill" style="left:12%;right:12%;"></div>
              <div class="range-dot" style="left:calc(${pct.toFixed(1)}% - 6px);"></div>
            </div>
          </div>
          `;
        })() : ""}
        <div class="fc-footer">
          <span>${esc(fc.forecast_type || "24h Forecast")}</span>
          <span>Inspect →</span>
        </div>
      </div>
    </article>
  `;
}

function openForecastDrawer(fc) {
  const iconSvg = ICONS[fc.sourceId] || ICONS.news;
  const outcomes = fc.outcomes || [];
  const gc = fc.gemini_comparison;

  openSheet(
    `<span class="fc-source-pill">${iconSvg} <span>${esc(fc.sourceLabel || fc.sourceId)} · ${esc(fc.id)}</span></span>`,
    `
      <h2 style="font-family:var(--serif);font-size:28px;font-weight:400;line-height:1.15;margin-bottom:12px;">${esc(fc.title)}</h2>
      <p style="font-size:14px;font-weight:500;background:var(--surface-subtle);padding:14px;border-radius:10px;margin-bottom:18px;">
        ${esc(fc.claim)}
      </p>

      ${gc ? `
        <div style="margin-bottom:18px;">
          <div style="font-family:var(--mono);font-size:11px;color:var(--ink-muted);margin-bottom:8px;">GEMINI MODEL FAMILY COMPARISON</div>
          <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;">
            ${Object.entries(gc).map(([mName, val]) => `
              <div style="background:var(--surface-subtle);padding:10px;border-radius:8px;text-align:center;">
                <div style="font-family:var(--mono);font-size:10px;color:var(--ink-secondary);">${esc(mName)}</div>
                <strong style="font-family:var(--mono);font-size:17px;">${val !== null && val !== undefined ? (val * 100).toFixed(0) + "%" : "—"}</strong>
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
        <div style="font-family:var(--mono);font-size:11px;color:var(--ink-muted);margin-bottom:6px;">RATIONALE &amp; EVIDENCE</div>
        <p style="font-size:13.5px;color:var(--ink-secondary);line-height:1.6;white-space:pre-line;">${esc(fc.rationale || "")}</p>
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
   VIEW 3: BENCHMARK (MULTI-GEMINI GRAPH + LEADERBOARD + HEAD-TO-HEAD)
   =================================================================== */
function renderBenchmarkView() {
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
    titleEl.textContent = "Blinded gemini-4-argon Judge Score (1–5 Scale)";
    subEl.textContent = "Higher is better — Blinded evaluation of Q4 World & Q5 Social narratives against held-out next-day evidence";
  }

  legendEl.innerHTML = MODELS.map(m => `
    <div class="legend-item">
      <span class="legend-line" style="background:${m.color}"></span>
      <span>${esc(m.name)}</span>
    </div>
  `).join("");

  const W = 1020, H = 250, padL = 48, padR = 24, padT = 20, padB = 34;
  const plotW = W - padL - padR;
  const plotH = H - padT - padB;

  const yMin = metric === "accuracy" ? 35 : (metric === "brier" ? 0 : 1.5);
  const yMax = metric === "accuracy" ? 105 : (metric === "brier" ? 0.45 : 5.0);

  const xAt = i => padL + (i / (HISTORICAL_DAYS.length - 1)) * plotW;
  const yAt = val => padT + plotH - ((val - yMin) / (yMax - yMin)) * plotH;

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

  const xLabelsHtml = HISTORICAL_DAYS.map((d, i) => `
    <text x="${xAt(i)}" y="${H - 8}" text-anchor="middle" font-family="JetBrains Mono" font-size="10.5" fill="#63615C">${d.shortLabel}</text>
  `).join("");

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
  const geminiModels = MODELS.filter(m => m.id !== "baseline");
  const summaries = geminiModels.map(m => {
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
        ${idx === 0 ? `<span class="outcome-badge hit">#1 Overall</span>` : ""}
      </div>
      <div class="lb-metrics">
        <div class="lb-stat">
          <span>ARGON JUDGE ↑</span>
          <strong>${s.avgJudge.toFixed(2)} / 5</strong>
        </div>
        <div class="lb-stat">
          <span>BRIER ERROR ↓</span>
          <strong>${s.avgBrier.toFixed(3)}</strong>
        </div>
        <div class="lb-stat">
          <span>ACCURACY ↑</span>
          <strong>${s.avgAcc.toFixed(0)}%</strong>
        </div>
        <div class="lb-stat">
          <span>NASA MAE ↓</span>
          <strong>±${s.mae.toFixed(2)}</strong>
        </div>
      </div>
    </div>
  `).join("");
}

function renderBenchmarkTable() {
  const tabsEl = document.getElementById("bench-track-tabs");
  const tracks = [
    { id: "all", label: "All Tracks (50 Questions)" },
    { id: "q1", label: "Stocks / Registry (Q1)" },
    { id: "q2", label: "SEC 8-K Filings (Q2)" },
    { id: "q3", label: "NASA X Volume (Q3)" },
    { id: "q4", label: "World Narrative (Q4)" },
    { id: "q5", label: "Social Narrative (Q5)" }
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
    const mArgon = d.models["gemini-4-argon"];
    const mPro = d.models["gemini-3.1-pro-preview"];
    const mFlash = d.models["gemini-3.8-flash"];
    const mLite = d.models["gemini-3.1-flash-lite"];

    if (STATE.benchTrack === "all" || STATE.benchTrack === "q1") {
      rows.push({
        day: d,
        trackId: "q1",
        track: "Stocks / Registry",
        question: d.isWeekend ? `Weekend SEC 8-K Count (${d.shortLabel})` : `Will ${d.ticker} close > $${d.baseClose}?`,
        actual: d.isWeekend ? `${d.q1Actual} filings` : `${d.q1Actual ? "YES" : "NO"} ($${d.targetClose})`,
        argon: d.isWeekend ? "Control" : `${(mArgon.q1Prob * 100).toFixed(0)}%`,
        pro: d.isWeekend ? "Control" : `${(mPro.q1Prob * 100).toFixed(0)}%`,
        flash: d.isWeekend ? "Control" : `${(mFlash.q1Prob * 100).toFixed(0)}%`,
        lite: d.isWeekend ? "Control" : `${(mLite.q1Prob * 100).toFixed(0)}%`
      });
    }
    if (STATE.benchTrack === "all" || STATE.benchTrack === "q2") {
      rows.push({
        day: d,
        trackId: "q2",
        track: "SEC 8-K Cohort",
        question: `10-Company Cohort Original 8-K (${d.shortLabel})`,
        actual: d.q2Actual ? "YES (8-K filed)" : "NO (0 filings)",
        argon: `${(mArgon.q2Prob * 100).toFixed(0)}%`,
        pro: `${(mPro.q2Prob * 100).toFixed(0)}%`,
        flash: `${(mFlash.q2Prob * 100).toFixed(0)}%`,
        lite: `${(mLite.q2Prob * 100).toFixed(0)}%`
      });
    }
    if (STATE.benchTrack === "all" || STATE.benchTrack === "q3") {
      rows.push({
        day: d,
        trackId: "q3",
        track: "NASA X Volume",
        question: `@NASA Retrievable X Post Count (${d.shortLabel})`,
        actual: `${d.q3Actual} posts`,
        argon: `${mArgon.q3Est} est`,
        pro: `${mPro.q3Est} est`,
        flash: `${mFlash.q3Est} est`,
        lite: `${mLite.q3Est} est`
      });
    }
    if (STATE.benchTrack === "all" || STATE.benchTrack === "q4") {
      const q4Title = (mArgon.q4Forecasts?.[0]?.title) || `World Narrative (${d.shortLabel})`;
      rows.push({
        day: d,
        trackId: "q4",
        track: "World Narrative",
        question: q4Title,
        actual: "Held-out Exa news",
        argon: `★ ${mArgon.judgeWorld ?? mArgon.judge}/5`,
        pro: `★ ${mPro.judgeWorld ?? mPro.judge}/5`,
        flash: `★ ${mFlash.judgeWorld ?? mFlash.judge}/5`,
        lite: `★ ${mLite.judgeWorld ?? mLite.judge}/5`
      });
    }
    if (STATE.benchTrack === "all" || STATE.benchTrack === "q5") {
      const q5Title = (mArgon.q5Forecasts?.[0]?.title) || `Social Narrative (${d.shortLabel})`;
      rows.push({
        day: d,
        trackId: "q5",
        track: "Social Narrative",
        question: q5Title,
        actual: "Held-out Social cohort",
        argon: `★ ${mArgon.judgeSocial ?? mArgon.judge}/5`,
        pro: `★ ${mPro.judgeSocial ?? mPro.judge}/5`,
        flash: `★ ${mFlash.judgeSocial ?? mFlash.judge}/5`,
        lite: `★ ${mLite.judgeSocial ?? mLite.judge}/5`
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
          <th>gemini-3.1-pro</th>
          <th>gemini-3.8-flash</th>
          <th>gemini-3.1-flash-lite</th>
        </tr>
      </thead>
      <tbody>
        ${rows.map((r, i) => `
          <tr data-row-idx="${i}">
            <td style="font-family:var(--mono);font-weight:600;">${esc(r.day.shortLabel)}</td>
            <td style="font-family:var(--mono);font-size:11.5px;color:var(--ink-secondary);">${esc(r.track)}</td>
            <td style="font-weight:500;">${esc(r.question)}</td>
            <td><span class="outcome-badge hit">${esc(r.actual)}</span></td>
            <td style="font-family:var(--mono);font-weight:700;color:var(--accent);">${esc(r.argon)}</td>
            <td style="font-family:var(--mono);color:var(--green);">${esc(r.pro)}</td>
            <td style="font-family:var(--mono);color:var(--indigo);">${esc(r.flash)}</td>
            <td style="font-family:var(--mono);color:#D97706;">${esc(r.lite)}</td>
          </tr>
        `).join("")}
      </tbody>
    </table>
  `;

  listEl.querySelectorAll("tr[data-row-idx]").forEach(tr => {
    tr.addEventListener("click", () => {
      const r = rows[Number(tr.dataset.rowIdx)];
      if (!r) return;
      const d = r.day;
      const mIds = [
        { id: "gemini-4-argon", label: "gemini-4-argon", color: "var(--accent)", val: r.argon },
        { id: "gemini-3.1-pro-preview", label: "gemini-3.1-pro", color: "var(--green)", val: r.pro },
        { id: "gemini-3.8-flash", label: "gemini-3.8-flash", color: "var(--indigo)", val: r.flash },
        { id: "gemini-3.1-flash-lite", label: "gemini-3.1-flash-lite", color: "#D97706", val: r.lite }
      ];

      const detailsHtml = mIds.map(m => {
        const md = d.models[m.id] || {};
        let bodyText = "";
        if (r.trackId === "q1") bodyText = md.q1Rationale || "";
        else if (r.trackId === "q2") bodyText = md.q2Rationale || "";
        else if (r.trackId === "q3") bodyText = md.q3Rationale || "";
        else if (r.trackId === "q4") {
          const f0 = (md.q4Forecasts || [])[0];
          bodyText = (f0 ? `${f0.title} (${(f0.probability * 100).toFixed(0)}%): ${f0.claim}
` : "") + `Judge Notes: ${md.judgeNotes || ""}`;
        } else {
          const f0 = (md.q5Forecasts || [])[0];
          bodyText = (f0 ? `${f0.title} (${(f0.probability * 100).toFixed(0)}%): ${f0.claim}
` : "") + `Judge Notes: ${md.judgeNotes || ""}`;
        }
        return `
          <div style="background:var(--surface-subtle);padding:12px;border-radius:10px;margin-bottom:10px;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
              <strong style="font-family:var(--mono);font-size:12px;color:${m.color};">${esc(m.label)}</strong>
              <span style="font-family:var(--mono);font-weight:700;font-size:13px;">${esc(m.val)}</span>
            </div>
            <p style="font-size:12.5px;color:var(--ink-secondary);line-height:1.5;white-space:pre-line;">${esc(bodyText)}</p>
          </div>
        `;
      }).join("");

      openSheet(
        `<span class="fc-source-pill">${esc(d.targetDate)} · ${esc(r.track)}</span>`,
        `
          <h2 style="font-family:var(--serif);font-size:26px;font-weight:400;margin-bottom:10px;">${esc(r.question)}</h2>
          <p style="font-size:13px;color:var(--ink-secondary);margin-bottom:14px;line-height:1.5;">
            <strong>Actual Outcome:</strong> ${esc(r.actual)}<br/>
            <strong>Held-Out Day Summary (gemini-4-argon Judge):</strong> ${esc(d.judgeSummary)}
          </p>
          <div style="font-family:var(--mono);font-size:11px;color:var(--ink-muted);margin-bottom:8px;">MODEL-BY-MODEL PREDICTIONS &amp; JUDGE CRITIQUE</div>
          ${detailsHtml}
        `
      );
    });
  });
}

/* ===================================================================
   VIEW 1.5: HOTSPOTS & 3D OFFICES (NEIGHBORHOOD WORLD MODEL)
   =================================================================== */
function renderHotspots3DView() {
  const canvas = document.getElementById("app-office-3d-canvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");

  const HOTSPOT_3D_CONFIG = {
    kazakhstan: {
      title: "Astana Hub, Kazakhstan — Eurasian AI & Compute Twin Towers",
      sub: "42,000 m² · 1,850 Desks · US–China AI Neutrality Corridor · Drag to Orbit 3D",
      chain: "Chain: EO 14436 + AI Bloc Neutrality → +1,850 AI/Ops Jobs → +19% Short-Stay Demand → +24% Rents → +14 New Businesses",
      m1: "AP News + EO 14436",
      m2: "+1,850 AI/Eng Jobs",
      m3: "+24% Astana Rents",
      m4: "+14 Tech Suppliers",
      prompt: "Simulate how Astana Hub & Almaty, Kazakhstan evolve as a corporate HQ hotspot driven by US-China AI bloc neutrality (AP News run 60cf796a) and EO 14436 sanctions routing: model the chain from jobs to housing demand, rents, and new businesses",
      buildings: [
        { x: -1.1, z: -0.3, w: 1.35, d: 1.35, h: 4.5, phase: 2, role: "hq", label: "HQ Tower A (AI Core)" },
        { x: 1.1, z: -0.3, w: 1.35, d: 1.35, h: 3.8, phase: 2, role: "hq", label: "HQ Tower B (Ops)" },
        { x: 0.0, z: -0.3, w: 1.1, d: 0.75, h: 2.4, y0: 1.7, phase: 2, role: "bridge", label: "Skybridge Atrium" },
        { x: -2.8, z: 1.2, w: 1.15, d: 1.15, h: 2.4, phase: 3, role: "res", label: "Relocation Lofts (+24% Rent)" },
        { x: 2.7, z: 1.1, w: 1.15, d: 1.1, h: 2.7, phase: 3, role: "res", label: "Executive Towers" },
        { x: -2.5, z: -2.1, w: 1.2, d: 1.0, h: 1.9, phase: 3, role: "res", label: "Astana Stay Hotel" },
        { x: -0.9, z: 1.8, w: 1.2, d: 0.9, h: 1.05, phase: 4, role: "biz", label: "New Cafes & Retail Row" },
        { x: 0.9, z: 1.8, w: 1.2, d: 0.9, h: 1.2, phase: 4, role: "biz", label: "Cloud Hardware Lab" },
        { x: 2.5, z: -2.0, w: 1.2, d: 1.2, h: 1.65, phase: 4, role: "biz", label: "Venture & Legal Hub" },
        { x: 0.0, z: -2.4, w: 1.5, d: 0.9, h: 1.4, phase: 4, role: "biz", label: "Compute Substation" }
      ]
    },
    slc: {
      title: "Salt Lake City, UT — Silicon Slopes Mass-Timber & Solar HQ Campus",
      sub: "28,500 m² · 1,200 Desks · $115k–$155k Data Eng Comp · $0.353/kWh Utah Grid",
      chain: "Chain: Alto Cirra Hiring + $0.353/kWh Grid → +1,200 Data Jobs → Zillow Inventory Drop → +18% Rents → +11 New Businesses",
      m1: "Wellfound + $0.35/kWh",
      m2: "+1,200 Data/AI Jobs",
      m3: "+18% SLC Zillow Rent",
      m4: "+11 Slopes Businesses",
      prompt: "Simulate how Salt Lake City (Silicon Slopes) evolves as a corporate HQ hotspot driven by Alto Cirra $115k-$155k Data Eng hiring (Wellfound run e5041c13) and $0.353/kWh Utah EV/grid power (run 26e9741d): model jobs, housing demand, Zillow rents, and new businesses",
      buildings: [
        { x: -1.2, z: -0.2, w: 1.8, d: 1.4, h: 2.7, phase: 2, role: "hq", label: "West Timber Wing" },
        { x: 1.0, z: -0.2, w: 1.8, d: 1.4, h: 3.3, phase: 2, role: "hq", label: "East AI Wing (Alto Cirra)" },
        { x: -0.1, z: 0.3, w: 1.4, d: 1.1, h: 1.8, phase: 2, role: "bridge", label: "Solar Glass Pavilion" },
        { x: -2.9, z: 1.4, w: 1.2, d: 1.1, h: 2.2, phase: 3, role: "res", label: "Lehi / Draper Townhomes" },
        { x: 2.8, z: 1.3, w: 1.2, d: 1.1, h: 2.5, phase: 3, role: "res", label: "Downtown SLC Lofts (+18% Rent)" },
        { x: -2.6, z: -1.9, w: 1.1, d: 1.1, h: 1.9, phase: 3, role: "res", label: "Mountain View Flats" },
        { x: -1.1, z: 2.0, w: 1.3, d: 0.85, h: 0.95, phase: 4, role: "biz", label: "Roastery & Food Hall" },
        { x: 1.1, z: 2.0, w: 1.3, d: 0.85, h: 1.1, phase: 4, role: "biz", label: "Outdoor Gear & Fitness" },
        { x: 2.4, z: -1.9, w: 1.3, d: 1.1, h: 1.5, phase: 4, role: "biz", label: "B2B SaaS Incubator" }
      ]
    },
    dallas: {
      title: "Dallas, TX (Uptown / Frisco) — Hyperscale Skybridge Corporate HQ",
      sub: "64,000 m² · 3,100 Desks · CBRE Onnec 8-K + MOLTEN Cloud · $3.72/gal TX Fuel",
      chain: "Chain: CBRE 8-K + $3.72 TX Fuel → +3,100 Corp/Cloud Jobs → Listings Absorbed → +21% Rents → +19 New Businesses",
      m1: "CBRE 8-K + $3.72 Fuel",
      m2: "+3,100 HQ & Cloud Jobs",
      m3: "+21% Uptown Rents",
      m4: "+19 New Businesses",
      prompt: "Simulate how Dallas (Uptown / Frisco) evolves as a corporate HQ hotspot driven by CBRE's Onnec data-center acquisition (SEC 8-K run bdfac0bb), MOLTEN Cloud engineering hiring (run e5041c13), and $3.72/gal TX fuel (run a1dcecca): model jobs, housing demand, rents, and new businesses",
      buildings: [
        { x: 0.0, z: -0.4, w: 1.7, d: 1.5, h: 4.9, phase: 2, role: "hq", label: "Dallas HQ Flagship Tower" },
        { x: -1.7, z: -0.2, w: 1.3, d: 1.3, h: 3.2, phase: 2, role: "hq", label: "Cloud Ops Annex" },
        { x: 1.7, z: -0.2, w: 1.3, d: 1.3, h: 3.5, phase: 2, role: "hq", label: "Data Center & Trading Wing" },
        { x: -2.9, z: 1.4, w: 1.2, d: 1.2, h: 2.8, phase: 3, role: "res", label: "Uptown High-Rise Condos (+21% Rent)" },
        { x: 2.9, z: 1.4, w: 1.2, d: 1.2, h: 2.6, phase: 3, role: "res", label: "Frisco Station Residences" },
        { x: -2.6, z: -2.1, w: 1.2, d: 1.1, h: 2.2, phase: 3, role: "res", label: "Corporate Stay Suites" },
        { x: -1.0, z: 1.9, w: 1.3, d: 0.9, h: 1.15, phase: 4, role: "biz", label: "Steakhouse & Dining Block" },
        { x: 1.0, z: 1.9, w: 1.3, d: 0.9, h: 1.25, phase: 4, role: "biz", label: "FinTech & Legal Plaza" },
        { x: 2.5, z: -2.1, w: 1.4, d: 1.1, h: 1.7, phase: 4, role: "biz", label: "Enterprise Co-Working" }
      ]
    }
  };

  let curCity = "kazakhstan";
  let curPhase = 4;
  let yaw = -0.62;
  let pitch = 0.48;
  let dragging = false;
  let lastX = 0, lastY = 0;

  function syncLabels() {
    const cfg = HOTSPOT_3D_CONFIG[curCity];
    document.getElementById("app-3d-title").textContent = cfg.title;
    document.getElementById("app-3d-sub").textContent = cfg.sub;
    document.getElementById("app-3d-chain-line").textContent = cfg.chain;
    document.getElementById("ap-m1").textContent = cfg.m1;
    document.getElementById("ap-m2").textContent = cfg.m2;
    document.getElementById("ap-m3").textContent = cfg.m3;
    document.getElementById("ap-m4").textContent = cfg.m4;
    const pNames = {
      1: "STAGE 1: PUBLIC SIGNALS",
      2: "STAGE 2: HQ & JOBS SURGE",
      3: "STAGE 3: DEMAND & RENTS",
      4: "STAGE 4: NEW BUSINESSES"
    };
    document.getElementById("app-3d-phase-badge").textContent = pNames[curPhase];
  }

  function project(x, y, z, cx, cy, scale) {
    const cosY = Math.cos(yaw), sinY = Math.sin(yaw);
    const rx = x * cosY - z * sinY;
    const rz = x * sinY + z * cosY;
    const cosP = Math.cos(pitch), sinP = Math.sin(pitch);
    const py = y * cosP - rz * sinP;
    const pz = y * sinP + rz * cosP;
    const fov = 14 / (14 + pz * 0.35);
    return { x: cx + rx * scale * fov, y: cy - py * scale * fov, depth: pz };
  }

  function drawScene() {
    const W = canvas.width, H = canvas.height;
    ctx.clearRect(0, 0, W, H);
    const cfg = HOTSPOT_3D_CONFIG[curCity];
    const cx = W * 0.5, cy = H * 0.73, scale = 40;

    ctx.strokeStyle = "rgba(255,255,255,0.09)";
    ctx.lineWidth = 1;
    for (let g = -4; g <= 4; g++) {
      const a = project(g, 0, -4, cx, cy, scale), b = project(g, 0, 4, cx, cy, scale);
      ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
      const c = project(-4, 0, g, cx, cy, scale), d = project(4, 0, g, cx, cy, scale);
      ctx.beginPath(); ctx.moveTo(c.x, c.y); ctx.lineTo(d.x, d.y); ctx.stroke();
    }

    [1.8, 3.3].forEach((rad, ri) => {
      ctx.beginPath();
      for (let i = 0; i <= 36; i++) {
        const ang = (i / 36) * Math.PI * 2;
        const p = project(Math.cos(ang) * rad, 0.02, Math.sin(ang) * rad, cx, cy, scale);
        if (i === 0) ctx.moveTo(p.x, p.y);
        else ctx.lineTo(p.x, p.y);
      }
      ctx.strokeStyle = ri === 0 ? "rgba(225,56,28,0.55)" : "rgba(56,189,248,0.28)";
      ctx.lineWidth = 1.4;
      ctx.stroke();
    });

    const visible = cfg.buildings
      .filter(b => b.phase <= curPhase || (curPhase === 1 && b.role === "hq"))
      .map(b => {
        const hScale = (curPhase === 1 && b.role === "hq") ? 0.35 : 1.0;
        const center = project(b.x, (b.y0 || 0) + (b.h * hScale) / 2, b.z, cx, cy, scale);
        return { ...b, h: b.h * hScale, depth: center.depth };
      })
      .sort((a, b) => b.depth - a.depth);

    visible.forEach(b => {
      const y0 = b.y0 || 0, y1 = y0 + b.h;
      const hw = b.w / 2, hd = b.d / 2;
      const corners = [
        { x: b.x - hw, y: y0, z: b.z - hd },
        { x: b.x + hw, y: y0, z: b.z - hd },
        { x: b.x + hw, y: y0, z: b.z + hd },
        { x: b.x - hw, y: y0, z: b.z + hd },
        { x: b.x - hw, y: y1, z: b.z - hd },
        { x: b.x + hw, y: y1, z: b.z - hd },
        { x: b.x + hw, y: y1, z: b.z + hd },
        { x: b.x - hw, y: y1, z: b.z + hd }
      ].map(p => project(p.x, p.y, p.z, cx, cy, scale));

      const faces = [
        { idx: [0, 1, 5, 4], shade: 0.72 },
        { idx: [1, 2, 6, 5], shade: 0.88 },
        { idx: [2, 3, 7, 6], shade: 0.96 },
        { idx: [3, 0, 4, 7], shade: 0.64 },
        { idx: [4, 5, 6, 7], shade: 1.12 }
      ].sort((a, bFace) => {
        const da = a.idx.reduce((s, i) => s + corners[i].depth, 0) / 4;
        const db = bFace.idx.reduce((s, i) => s + corners[i].depth, 0) / 4;
        return db - da;
      });

      let rgb = [56, 189, 248];
      if (b.role === "hq") rgb = curCity === "kazakhstan" ? [56, 189, 248] : (curCity === "slc" ? [99, 102, 241] : [16, 185, 129]);
      else if (b.role === "bridge") rgb = [225, 56, 28];
      else if (b.role === "res") rgb = [245, 158, 11];
      else if (b.role === "biz") rgb = [168, 85, 247];

      faces.forEach(f => {
        ctx.beginPath();
        f.idx.forEach((ci, k) => {
          if (k === 0) ctx.moveTo(corners[ci].x, corners[ci].y);
          else ctx.lineTo(corners[ci].x, corners[ci].y);
        });
        ctx.closePath();
        ctx.fillStyle = `rgba(${Math.min(255, Math.round(rgb[0] * f.shade))}, ${Math.min(255, Math.round(rgb[1] * f.shade))}, ${Math.min(255, Math.round(rgb[2] * f.shade))}, 0.88)`;
        ctx.fill();
        ctx.strokeStyle = "rgba(255,255,255,0.22)";
        ctx.lineWidth = 1;
        ctx.stroke();
      });

      if (b.role === "hq" || (b.phase === curPhase && curPhase >= 3)) {
        const top = project(b.x, y1 + 0.25, b.z, cx, cy, scale);
        ctx.font = "600 10px 'JetBrains Mono', monospace";
        const tw = ctx.measureText(b.label).width + 10;
        ctx.fillStyle = "rgba(20,20,19,0.88)";
        ctx.fillRect(top.x - tw / 2, top.y - 14, tw, 16);
        ctx.strokeStyle = b.role === "hq" ? "#38BDF8" : (b.role === "res" ? "#F59E0B" : "#A855F7");
        ctx.strokeRect(top.x - tw / 2, top.y - 14, tw, 16);
        ctx.fillStyle = "#FAF9F6";
        ctx.textAlign = "center";
        ctx.fillText(b.label, top.x, top.y - 3);
      }
    });
  }

  document.querySelectorAll("#app-hotspot-list .app-hs-card").forEach(card => {
    card.addEventListener("click", () => {
      curCity = card.dataset.hcity;
      document.querySelectorAll("#app-hotspot-list .app-hs-card").forEach(el => el.classList.toggle("active", el === card));
      syncLabels();
      drawScene();
    });
  });

  document.querySelectorAll("#app-phase-bar .app-phase-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      curPhase = Number(btn.dataset.aphase);
      document.querySelectorAll("#app-phase-bar .app-phase-btn").forEach(el => el.classList.toggle("active", el === btn));
      syncLabels();
      drawScene();
    });
  });

  const box = document.getElementById("app-canvas-box");
  if (box) {
    box.addEventListener("mousedown", e => {
      dragging = true;
      lastX = e.clientX;
      lastY = e.clientY;
    });
    window.addEventListener("mousemove", e => {
      if (!dragging) return;
      yaw += (e.clientX - lastX) * 0.01;
      pitch = Math.max(0.2, Math.min(1.05, pitch + (e.clientY - lastY) * 0.008));
      lastX = e.clientX;
      lastY = e.clientY;
      drawScene();
    });
    window.addEventListener("mouseup", () => { dragging = false; });
  }

  document.getElementById("btn-simulate-hotspot")?.addEventListener("click", () => {
    ["news", "markets", "zillow", "airbnb", "linkedin", "gas"].forEach(id => STATE.selectedSources.add(id));
    renderSourcesView();
    const promptInp = document.getElementById("user-prompt-input");
    if (promptInp) {
      promptInp.value = HOTSPOT_3D_CONFIG[curCity].prompt;
    }
    document.getElementById("btn-run-prediction")?.click();
  });

  setInterval(() => {
    if (!dragging && STATE.view === "hotspots") {
      yaw += 0.006;
      drawScene();
    }
  }, 45);

  syncLabels();
  drawScene();
}

document.addEventListener("DOMContentLoaded", init);
