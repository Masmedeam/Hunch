/* NEXTDAY — Ultra-Minimalistic Source & Forecast Controller */

const ICONS = {
  news: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>`,
  x: `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>`,
  tiktok: `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-5.2 1.74 2.89 2.89 0 0 1 2.31-4.64 2.93 2.93 0 0 1 .88.13V9.4a6.84 6.84 0 0 0-1-.05A6.33 6.33 0 0 0 5 20.1a6.34 6.34 0 0 0 10.86-4.43v-7a8.16 8.16 0 0 0 4.77 1.52v-3.4a4.85 4.85 0 0 1-1-.1z"/></svg>`,
  youtube: `<svg viewBox="0 0 24 24" fill="#FF0000"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>`,
  markets: `<svg viewBox="0 0 24 24" fill="none" stroke="#0E7A5D" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>`,
  zillow: `<svg viewBox="0 0 24 24" fill="#006AFF"><path d="M12 2L2 9.5V22h20V9.5L12 2zm5.5 16.5h-11v-2.1l6.8-6.4H6.8V8h10.4v2.1l-6.8 6.4h7.1v2z"/></svg>`,
  airbnb: `<svg viewBox="0 0 24 24" fill="#FF385C"><path d="M12 2C9.5 2 7.2 6.1 5.1 10.6 3.3 14.4 2.5 16.8 3.6 19c1 2 3.4 3 5.5 2.2 1.2-.5 2.1-1.4 2.9-2.5.8 1.1 1.7 2 2.9 2.5 2.1.8 4.5-.2 5.5-2.2 1.1-2.2.3-4.6-1.5-8.4C16.8 6.1 14.5 2 12 2zm0 13.8c-1.5-1.9-2.3-3.5-2.3-4.7 0-1.3 1-2.3 2.3-2.3s2.3 1 2.3 2.3c0 1.2-.8 2.8-2.3 4.7z"/></svg>`,
  linkedin: `<svg viewBox="0 0 24 24" fill="#0A66C2"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/></svg>`
};

const SOURCE_CARDS = [
  {
    id: "news",
    name: "Global News",
    desc: "Exa full-text & Serper news across 4 regions",
    provider: "exa · serper",
    price: "$0.007 / run",
    icon: ICONS.news,
    fields: [
      { key: "topics", label: "Topics", value: "geopolitics, economy, technology, climate, culture" }
    ]
  },
  {
    id: "x",
    name: "X (Twitter)",
    desc: "Real-time search & country trend rankings",
    provider: "tikhub",
    price: "$0.0011 / run",
    icon: ICONS.x,
    fields: [
      { key: "x_accounts", label: "Tracked Accounts", value: "NASA, WHO, BBCWorld" }
    ]
  },
  {
    id: "tiktok",
    name: "TikTok",
    desc: "Regional trending feed, hashtags & search",
    provider: "scrapecreators · tikhub",
    price: "$0.002 / run",
    icon: ICONS.tiktok,
    fields: [
      { key: "tiktok_accounts", label: "Tracked Profiles", value: "bbcnews, dwnews" }
    ]
  },
  {
    id: "youtube",
    name: "YouTube",
    desc: "Weekly popular videos & trending Shorts",
    provider: "scrapecreators",
    price: "$0.002 / run",
    icon: ICONS.youtube,
    fields: [
      { key: "youtube_accounts", label: "Tracked Channels", value: "NASA, BBCNews" }
    ]
  },
  {
    id: "markets",
    name: "SEC & Equities",
    desc: "Daily OHLCV bars & verified 8-K filings",
    provider: "secapi · financialdatasets",
    price: "$0.0005–$0.02",
    icon: ICONS.markets,
    fields: [
      { key: "tickers", label: "Cohort Tickers", value: "AAPL, MSFT, NVDA, AMZN, GOOGL, META, JPM, XOM, WMT, NFLX" }
    ]
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
  }
];

const VERTICAL_FORECASTS = [
  {
    id: "fc-zillow",
    sourceId: "zillow",
    sourceLabel: "Zillow",
    title: "US 30Y Mortgage Rate & Austin Listing Spread",
    claim: "Zillow’s national 30-year fixed mortgage rate stays within [6.15%, 6.35%] tomorrow while tracked Austin ZPIDs hold within ±0.5% of Zestimate.",
    probability: 0.76,
    estimate: { value: 6.24, lower: 6.15, upper: 6.35, unit: "% APR", interval_probability: 0.8 },
    outcomes: [
      { label: "Below 6.15% APR", probability: 0.11 },
      { label: "6.15% to 6.35% APR", probability: 0.76 },
      { label: "Above 6.35% APR", probability: 0.13 }
    ],
    rationale: "Combines zillow:/get_mortgage_rates daily quotes with brightdata:/datasets/v3/zillow-properties listing snapshots.",
    resolution: { mode: "measurable", rule: "Compare zillow:/get_mortgage_rates at T0+24h against baseline.", sources: ["zillow:/get_mortgage_rates"] }
  },
  {
    id: "fc-airbnb",
    sourceId: "airbnb",
    sourceLabel: "Airbnb",
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
    resolution: { mode: "measurable", rule: "Re-query identical Airbnb location & date cohort at T0+24h.", sources: ["apify:/tri_angle/airbnb-scraper"] }
  },
  {
    id: "fc-linkedin",
    sourceId: "linkedin",
    sourceLabel: "LinkedIn",
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
    resolution: { mode: "measurable", rule: "Count deduplicated jobId postings created inside [T0, T0+24h).", sources: ["apify:/harvestapi/linkedin-job-search"] }
  }
];

const STATE = {
  bundle: null,
  casesCache: {},
  view: "sources",
  selectedSources: new Set(["news", "x", "tiktok", "youtube", "markets", "zillow", "airbnb", "linkedin"]),
  regions: new Set(["US", "GB", "IN", "JP"]),
  editingSourceId: null,
  fieldValues: {},
  lastSim: null,

  predFilter: "all",
  predLayout: "cards",

  activeCaseId: "day-2026-10-14",
  unsealed: false,
  feedKind: "all",
  feedSearch: ""
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
  toast._t = setTimeout(() => el.classList.add("hidden"), 2200);
}

function openSheet(badgeHtml, contentHtml) {
  document.getElementById("sheet-badge").innerHTML = badgeHtml;
  document.getElementById("sheet-content").innerHTML = contentHtml;
  document.getElementById("detail-sheet").classList.remove("hidden");
}

function closeSheet() {
  document.getElementById("detail-sheet").classList.add("hidden");
}

async function init() {
  try {
    const res = await fetch("/data/bundle.json");
    STATE.bundle = res.ok ? await res.json() : {};
  } catch (_) {
    STATE.bundle = {};
  }

  for (const s of SOURCE_CARDS) {
    for (const f of s.fields) STATE.fieldValues[f.key] = f.value;
  }

  // Step Tabs
  document.querySelectorAll(".step-tab").forEach(btn => {
    btn.addEventListener("click", () => {
      STATE.view = btn.dataset.view;
      document.querySelectorAll(".step-tab").forEach(b => b.classList.toggle("active", b === btn));
      document.querySelectorAll(".view").forEach(v => v.classList.toggle("active", v.id === `view-${STATE.view}`));
    });
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
  await renderBenchmarkView();
}

/* ===================================================================
   STEP 1: SOURCES VIEW
   =================================================================== */
function renderSourcesView() {
  // Region pills
  const regEl = document.getElementById("region-pills");
  const allRegs = [
    { code: "US", country: "UnitedStates", lang: "en" },
    { code: "GB", country: "UnitedKingdom", lang: "en" },
    { code: "IN", country: "India", lang: "en" },
    { code: "JP", country: "Japan", lang: "ja" }
  ];
  regEl.innerHTML = allRegs.map(r => `
    <button class="region-pill ${STATE.regions.has(r.code) ? "active" : ""}" data-reg="${r.code}">
      ${r.code}
    </button>
  `).join("");

  regEl.querySelectorAll(".region-pill").forEach(btn => {
    btn.addEventListener("click", () => {
      const code = btn.dataset.reg;
      if (STATE.regions.has(code) && STATE.regions.size > 1) STATE.regions.delete(code);
      else STATE.regions.add(code);
      renderSourcesView();
    });
  });

  // 8 Icon Cards
  const grid = document.getElementById("sources-grid");
  grid.innerHTML = SOURCE_CARDS.map(s => {
    const selected = STATE.selectedSources.has(s.id);
    return `
      <div class="source-card ${selected ? "selected" : ""}" data-sid="${s.id}">
        <div>
          <div class="source-card-top">
            <div class="brand-icon-box">${s.icon}</div>
            <div class="source-card-actions">
              <button class="gear-btn" data-gear="${s.id}" title="Configure ${esc(s.name)}" type="button">⚙</button>
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
      renderPredictionsView();
    });
  });

  renderSourceConfigSheet();
  updateSimulation();

  document.getElementById("budget-input").onchange = () => updateSimulation();
  document.getElementById("btn-download-plan").onclick = () => {
    if (!STATE.lastSim) return;
    const blob = new Blob([JSON.stringify(STATE.lastSim, null, 2)], { type: "application/json" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "nextday-plan.json";
    a.click();
    toast("Downloaded nextday-plan.json");
  };
  document.getElementById("btn-show-cli").onclick = () => {
    const verts = ["zillow", "airbnb", "linkedin"].filter(v => STATE.selectedSources.has(v));
    const vFlag = verts.length ? ` --verticals ${verts.join(" ")}` : "";
    const budget = document.getElementById("budget-input")?.value || "1.00";
    const cmd = `# 1. Build plan\n.venv/bin/nextday plan${vFlag} --output data/custom-plan.json\n\n# 2. Free contract & budget check\n.venv/bin/nextday collect --plan data/custom-plan.json --batch custom --budget ${budget}\n\n# 3. Execute & forecast\n.venv/bin/nextday collect --plan data/custom-plan.json --batch custom --budget ${budget} --execute\n.venv/bin/nextday normalize\n.venv/bin/nextday predict --name nextday-run --execute`;
    openSheet(
      `<span class="fc-source-pill">CLI PIPELINE</span>`,
      `
        <h2 style="font-family:var(--serif);font-size:28px;font-weight:400;margin-bottom:8px;">Ready-to-Run Commands</h2>
        <p style="color:var(--ink-secondary);font-size:13px;">Copy and run in your terminal, or proceed to Step 2 to inspect forecasts.</p>
        <pre class="code-box">${esc(cmd)}</pre>
        <div style="margin-top:16px;display:flex;gap:10px;">
          <button class="btn-primary" id="sheet-copy-cli" type="button">Copy Commands</button>
        </div>
      `
    );
    document.getElementById("sheet-copy-cli")?.addEventListener("click", () => {
      navigator.clipboard.writeText(cmd).then(() => toast("Copied commands"));
    });
  };
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
    mode: "prospective",
    budget_usd: Number(document.getElementById("budget-input")?.value || 1.0),
    regions,
    topics,
    enabled_sources: {
      exa_regional_news: STATE.selectedSources.has("news"),
      serper_news: STATE.selectedSources.has("news"),
      x_trends: STATE.selectedSources.has("x"),
      x_search: STATE.selectedSources.has("x"),
      tiktok_trends: STATE.selectedSources.has("tiktok"),
      tiktok_search: STATE.selectedSources.has("tiktok"),
      tiktok_hashtags: STATE.selectedSources.has("tiktok"),
      tiktok_search_trends: STATE.selectedSources.has("tiktok"),
      youtube_search: STATE.selectedSources.has("youtube"),
      youtube_trends: false
    },
    verticals: {
      zillow: {
        enabled: STATE.selectedSources.has("zillow"),
        include_mortgage_rates: true,
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
        company_urls: (STATE.fieldValues.linkedin_cos || "openai, anthropic").split(",").map(c => `https://linkedin.com/company/${c.trim()}`),
        include_wellfound_trending: true
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
    document.getElementById("sim-jobs-label").textContent = `${sim.job_count} Glasser Calls (${activeCards.length} sources)`;
    document.getElementById("sim-cost-label").textContent = `Est. $${Number(sim.expected_display_usd).toFixed(3)} · Reserved $${Number(sim.reserved_max_usd).toFixed(3)}`;
  } catch (_) {}
}

/* ===================================================================
   STEP 2: PREDICTIONS VIEW (CLEAN VISUAL CARDS)
   =================================================================== */
function getForecastIcon(fc) {
  if (fc.sourceId && ICONS[fc.sourceId]) return { icon: ICONS[fc.sourceId], label: fc.sourceLabel };
  if (fc.id === "fc-3") return { icon: ICONS.markets, label: "Stocks · META" };
  if (fc.id === "fc-5") return { icon: ICONS.youtube, label: "YouTube" };
  return { icon: ICONS.news, label: "News & Social" };
}

function renderPredictionsView() {
  const filterBar = document.getElementById("pred-source-filters");
  const filterDefs = [
    { id: "all", label: "All", icon: "" },
    { id: "news", label: "News & Social", icon: ICONS.news },
    { id: "markets", label: "SEC & Stocks", icon: ICONS.markets },
    { id: "zillow", label: "Zillow", icon: ICONS.zillow },
    { id: "airbnb", label: "Airbnb", icon: ICONS.airbnb },
    { id: "linkedin", label: "LinkedIn", icon: ICONS.linkedin }
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

  document.querySelectorAll(".layout-toggle .icon-btn").forEach(btn => {
    btn.onclick = () => {
      STATE.predLayout = btn.dataset.layout;
      document.querySelectorAll(".layout-toggle .icon-btn").forEach(b => b.classList.toggle("active", b === btn));
      renderPredictionsView();
    };
  });

  const pilot = STATE.bundle?.prospective?.argon_pilot || {};
  const liveForecasts = (pilot.forecast?.result?.forecasts || []).map(fc => ({
    ...fc,
    sourceId: fc.id === "fc-3" ? "markets" : "news"
  }));
  const allForecasts = [...liveForecasts, ...VERTICAL_FORECASTS].filter(fc => {
    if (STATE.predFilter === "all") return true;
    return fc.sourceId === STATE.predFilter;
  });

  const container = document.getElementById("predictions-container");
  if (STATE.predLayout === "compact") {
    container.innerHTML = `
      <div class="feed-section">
        ${allForecasts.map((fc, idx) => {
          const meta = getForecastIcon(fc);
          const p = fc.probability !== null && fc.probability !== undefined
            ? `${(fc.probability * 100).toFixed(0)}%`
            : `${(Math.max(...(fc.outcomes || []).map(o => o.probability)) * 100).toFixed(0)}% top bin`;
          return `
            <div class="feed-row" data-fc-idx="${idx}">
              <div class="feed-row-left">
                <div class="row-icon">${meta.icon}</div>
                <div>
                  <div class="row-title">${esc(fc.title)}</div>
                  <div style="font-size:12px;color:var(--ink-secondary);">${esc(fc.claim)}</div>
                </div>
              </div>
              <div class="row-meta" style="font-weight:700;color:var(--ink);font-size:14px;">${esc(p)}</div>
            </div>
          `;
        }).join("")}
      </div>
    `;
  } else {
    container.innerHTML = `
      <div class="forecast-grid">
        ${allForecasts.map((fc, idx) => {
          const meta = getForecastIcon(fc);
          const est = fc.estimate;
          const topOutcome = (fc.outcomes || []).slice().sort((a, b) => b.probability - a.probability)[0];
          const probDisplay = fc.probability !== null && fc.probability !== undefined
            ? `${(fc.probability * 100).toFixed(0)}%`
            : (topOutcome ? `${(topOutcome.probability * 100).toFixed(0)}%` : "—");
          const probSub = fc.probability !== null && fc.probability !== undefined ? "Probability" : "Modal Scenario";

          return `
            <article class="forecast-card" data-fc-idx="${idx}">
              <div>
                <div class="fc-top">
                  <div>
                    <div class="fc-badges">
                      <span class="fc-source-pill">${meta.icon} <span>${esc(meta.label)}</span></span>
                      <span class="fc-source-pill">${esc(fc.forecast_type)}</span>
                    </div>
                    <h2 class="fc-headline">${esc(fc.title)}</h2>
                  </div>
                  <div class="prob-badge">
                    <div class="prob-number">${esc(probDisplay)}</div>
                    <div class="prob-caption">${esc(probSub)}</div>
                  </div>
                </div>
                <p class="fc-claim-short" style="margin-top:12px;">${esc(fc.claim)}</p>
              </div>

              <div>
                ${est ? `
                  <div class="range-bar-box" style="margin-bottom:14px;">
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
                  <span>Resolution: ${esc(fc.resolution?.mode || "measurable")}</span>
                  <span>Inspect Details →</span>
                </div>
              </div>
            </article>
          `;
        }).join("")}
      </div>
    `;
  }

  container.querySelectorAll("[data-fc-idx]").forEach(el => {
    el.addEventListener("click", () => {
      const fc = allForecasts[Number(el.dataset.fcIdx)];
      if (fc) openForecastDrawer(fc);
    });
  });
}

function openForecastDrawer(fc) {
  const meta = getForecastIcon(fc);
  const outcomes = fc.outcomes || [];
  openSheet(
    `<span class="fc-source-pill">${meta.icon} <span>${esc(meta.label)} · ${esc(fc.id)}</span></span>`,
    `
      <h2 style="font-family:var(--serif);font-size:30px;font-weight:400;line-height:1.15;margin-bottom:12px;">${esc(fc.title)}</h2>
      <p style="font-size:14px;font-weight:500;background:var(--surface-subtle);padding:14px;border-radius:10px;margin-bottom:18px;">
        ${esc(fc.claim)}
      </p>

      ${outcomes.length ? `
        <div style="margin-bottom:18px;">
          <div class="kicker">SCENARIO DISTRIBUTION</div>
          ${outcomes.map(o => `
            <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid var(--border);font-size:13px;">
              <span>${esc(o.label)}</span>
              <strong style="font-family:var(--mono);">${(o.probability * 100).toFixed(1)}%</strong>
            </div>
          `).join("")}
        </div>
      ` : ""}

      <div style="margin-bottom:18px;">
        <div class="kicker">EVIDENCE RATIONALE</div>
        <p style="font-size:13.5px;color:var(--ink-secondary);line-height:1.6;">${esc(fc.rationale)}</p>
      </div>

      ${(fc.assumptions || []).length ? `
        <div style="margin-bottom:18px;">
          <div class="kicker">KEY ASSUMPTIONS</div>
          <ul style="padding-left:18px;font-size:13px;color:var(--ink-secondary);">
            ${fc.assumptions.map(a => `<li>${esc(a)}</li>`).join("")}
          </ul>
        </div>
      ` : ""}

      ${fc.resolution ? `
        <div style="background:var(--surface-subtle);padding:14px;border-radius:10px;font-size:12.5px;">
          <div class="kicker">RESOLUTION RULE (${esc(fc.resolution.mode.toUpperCase())})</div>
          <p>${esc(fc.resolution.rule)}</p>
        </div>
      ` : ""}
    `
  );
}

/* ===================================================================
   STEP 3: BENCHMARK VIEW (10-DAY STRIP, 5 TRACKS, CLEAN FEED)
   =================================================================== */
async function loadCase(caseId) {
  if (STATE.casesCache[caseId]) return STATE.casesCache[caseId];
  try {
    const r = await fetch(`/data/cases/${caseId}.json`);
    if (r.ok) {
      const d = await r.json();
      STATE.casesCache[caseId] = d;
      return d;
    }
  } catch (_) {}
  return (STATE.bundle?.benchmark?.cases || []).find(c => c.case_id === caseId);
}

async function renderBenchmarkView() {
  const cases = STATE.bundle?.benchmark?.cases || [];
  const daysStrip = document.getElementById("days-strip");
  daysStrip.innerHTML = cases.map((c, idx) => {
    const d = c.case_id.replace("day-2026-", "");
    return `
      <div class="day-pill ${c.case_id === STATE.activeCaseId ? "active" : ""}" data-cid="${c.case_id}">
        <small>CASE ${idx + 1}</small>
        <span>${esc(d)}</span>
      </div>
    `;
  }).join("");

  daysStrip.querySelectorAll(".day-pill").forEach(pill => {
    pill.addEventListener("click", async () => {
      STATE.activeCaseId = pill.dataset.cid;
      await renderBenchmarkView();
    });
  });

  const sealBtn = document.getElementById("btn-seal-toggle");
  const sealLbl = document.getElementById("seal-label");
  sealBtn.classList.toggle("unsealed", STATE.unsealed);
  sealLbl.textContent = STATE.unsealed ? "Next 24h Unsealed" : "Next 24h Sealed";
  sealBtn.onclick = () => {
    STATE.unsealed = !STATE.unsealed;
    renderBenchmarkView();
  };

  const c = await loadCase(STATE.activeCaseId);
  if (!c) return;

  // 5 Track Cards
  const trackIcons = [ICONS.markets, ICONS.markets, ICONS.x, ICONS.news, ICONS.tiktok];
  const qs = c.questions || [];
  const rs = c.resolutions || [];
  const tracksRow = document.getElementById("case-questions-row");
  tracksRow.innerHTML = qs.map((q, i) => {
    const res = rs[i] || {};
    let outText = "🔒 Sealed";
    if (STATE.unsealed) {
      outText = res.value !== null && res.value !== undefined
        ? `Outcome: ${JSON.stringify(res.value)}`
        : `${(res.source_ids || []).length} held-out refs`;
    }
    return `
      <div class="track-card" data-q-idx="${i}">
        <div class="track-card-top">
          <div class="row-icon" style="width:28px;height:28px;">${trackIcons[i] || ICONS.news}</div>
          <span style="font-family:var(--mono);font-size:10px;color:var(--ink-muted);">Q${i + 1} · ${esc(q.track)}</span>
        </div>
        <div class="track-q">${esc(q.question)}</div>
        <div class="track-outcome ${STATE.unsealed ? "revealed" : ""}">${esc(outText)}</div>
      </div>
    `;
  }).join("");

  tracksRow.querySelectorAll(".track-card").forEach(card => {
    card.addEventListener("click", () => {
      const i = Number(card.dataset.qIdx);
      const q = qs[i];
      const res = rs[i] || {};
      openSheet(
        `<span class="fc-source-pill">${esc(q.id)} · ${esc(q.track)}</span>`,
        `
          <h2 style="font-family:var(--serif);font-size:26px;font-weight:400;margin-bottom:12px;">${esc(q.question)}</h2>
          <p style="font-size:13px;color:var(--ink-secondary);margin-bottom:16px;"><strong>Resolution Rule:</strong> ${esc(q.resolution_rule)}</p>
          <div class="code-box">${esc(JSON.stringify(STATE.unsealed ? res : { status: "SEALED_BEHIND_CUTOFF_WALL" }, null, 2))}</div>
        `
      );
    });
  });

  renderCaseFeed(c);
}

function getRecordIcon(r) {
  if (r.kind === "article") return ICONS.news;
  if (r.kind === "price_bar" || r.kind === "filing" || r.kind === "filing_document") return ICONS.markets;
  if (r.platform === "x") return ICONS.x;
  if (r.platform === "tiktok") return ICONS.tiktok;
  if (r.platform === "youtube") return ICONS.youtube;
  return ICONS.news;
}

function renderCaseFeed(c) {
  const tabsEl = document.getElementById("feed-kind-tabs");
  const kinds = [
    { id: "all", label: "All Evidence" },
    { id: "article", label: "News" },
    { id: "social_post", label: "Social" },
    { id: "filing", label: "SEC 8-K" },
    { id: "price_bar", label: "Stocks" }
  ];
  tabsEl.innerHTML = kinds.map(k => `
    <button class="filter-chip ${STATE.feedKind === k.id ? "active" : ""}" data-fk="${k.id}">${esc(k.label)}</button>
  `).join("");

  tabsEl.querySelectorAll(".filter-chip").forEach(btn => {
    btn.addEventListener("click", () => {
      STATE.feedKind = btn.dataset.fk;
      renderCaseFeed(c);
    });
  });

  const searchInp = document.getElementById("feed-search");
  searchInp.oninput = () => {
    STATE.feedSearch = searchInp.value.trim().toLowerCase();
    renderCaseFeed(c);
  };

  const evidence = c.evidence || c.sample_evidence || [];
  const filtered = evidence.filter(r => {
    if (STATE.feedKind !== "all" && r.kind !== STATE.feedKind) return false;
    if (STATE.feedSearch) {
      const hay = `${r.title || ""} ${r.text || ""} ${r.ticker || ""} ${r.account || ""}`.toLowerCase();
      if (!hay.includes(STATE.feedSearch)) return false;
    }
    return true;
  });

  const listEl = document.getElementById("feed-list");
  listEl.innerHTML = filtered.slice(0, 50).map((r, idx) => {
    let title = r.title || r.text || "";
    if (r.kind === "price_bar") title = `${r.ticker} Daily Close $${r.close} (${r.trading_date})`;
    else if (r.kind === "filing") title = `${r.company || r.ticker} — SEC Form ${r.form} (${r.accession})`;
    else if (r.kind === "social_post") title = `@${r.account}: ${(r.text || r.title || "").slice(0, 90)}`;

    return `
      <div class="feed-row" data-r-idx="${idx}">
        <div class="feed-row-left">
          <div class="row-icon">${getRecordIcon(r)}</div>
          <div class="row-title">${esc(title)}</div>
        </div>
        <div class="row-meta">${esc((r.event_at || "").slice(5, 16).replace("T", " "))}</div>
      </div>
    `;
  }).join("");

  listEl.querySelectorAll(".feed-row").forEach(row => {
    row.addEventListener("click", () => {
      const r = filtered[Number(row.dataset.rIdx)];
      if (!r) return;
      openSheet(
        `<span class="fc-source-pill">${esc(r.kind)} · ${esc(r.event_at)}</span>`,
        `
          <h2 style="font-family:var(--serif);font-size:26px;font-weight:400;margin-bottom:12px;">
            ${esc(r.title || r.ticker || `@${r.account || "Evidence Record"}`)}
          </h2>
          ${r.text ? `<p style="font-size:13.5px;color:var(--ink-secondary);line-height:1.65;white-space:pre-wrap;margin-bottom:16px;">${esc(r.text)}</p>` : ""}
          <pre class="code-box">${esc(JSON.stringify(r, null, 2))}</pre>
        `
      );
    });
  });
}

document.addEventListener("DOMContentLoaded", init);
