# Hunch — Neighborhood Weather Forecast & 3D HQ Simulator (Pitch Deck)
> **Gemini 4 Argon SF Hackathon (Cerebral Valley · Shack15)** — *Track 1: Million Token Engineering*  
> **Interactive Web Deck:** `/pitch` (`ui/public/pitch/index.html` & `pitch/index.html`)

---

## Slide 01 // The Problem
**"We have a weather forecast for rain—but no prediction for which neighborhoods are about to get hot."**

- A big company headquarters announcement sets off a predictable chain reaction:
  1. **Early Public Signals** (Geopolitics, energy spreads, SEC 8-K leases, stealth job postings)
  2. **Jobs** (High-salary engineering & operations roles flood into the district)
  3. **Demand** (Short-term corporate stays & active listing inventory tighten)
  4. **Rents & Zillow Prices** (Residential & commercial price/sqft reprices 60–90 days later)
  5. **New Businesses** (Cafes, suppliers, schools, and new office towers transform the block)
- Today's real-estate portals only report **today's prices** (`T − 0`). World models (`gemini-4-argon` with 1M context) can fuse 32,490+ public records to **simulate how a neighborhood evolves** before the press release drops.

---

## Slide 02 // The Solution
**Hunch fuses LinkedIn, Zillow & geopolitics into `gemini-4-argon` to forecast corporate HQ moves and simulate neighborhood evolution.**

- **Stage 1 — Public Signal Ingestion (`545 Glasser Runs · $2.41 Total Spend`):** Contract-validated collector across LinkedIn/Wellfound jobs, Zillow/RentCast, Airbnb 14-day stays, AAA Fuel & EV Grid, SEC EDGAR 8-K/Form 4, and multilingual Geopolitical News (`Exa`, `X`, `TikTok`, `YouTube`).
- **Stage 2 — Temporal Quarantine (`32,490 Records · Zero Leakage`):** Enforces point-in-time cutoffs (`T₀`), strips post-cutoff article edits (`28 mutated articles quarantined`), and computes 526 exact counter growth deltas.
- **Stage 3 — `gemini-4-argon` World Model + 3D Office Placement:** Pinpoints which neighborhoods corporations will move into next—**Kazakhstan**, **Salt Lake City**, and **Dallas**—and drives interactive 3D office and neighborhood evolution models (`0.1759` Brier #1, `3.98/5.0` Blinded Judge #1).

---

## Slide 03 // Actual Fetched Research Data (Oct 25, 2026 UTC)
**Why our captured Glasser & SQLite data points to Kazakhstan, Salt Lake City & Dallas:**

| Predicted Hotspot | Glasser Run IDs | Actual Captured Research Signal (`observations.sqlite` & `verticals-cache-01`) |
| :--- | :--- | :--- |
| **1. Kazakhstan (`Astana Hub / Almaty`)** | `60cf796a` · `EO 14436` | **AP News (`run 60cf796a`)** captures Kazakh President Tokayev & Xi Jinping at the World AI crossroads as non-aligned nations bridge US and China AI blocs; combined with the **60-day US Russia sanctions waiver (`EO 14436`)** and `$116` Brent crude, multinational tech & energy firms route Eurasian HQs into Astana & Almaty. |
| **2. Salt Lake City, UT (`Silicon Slopes`)** | `e5041c13` · `26e9741d` | **Wellfound/LinkedIn (`run e5041c13`)** shows **Alto Cirra** hiring Software & Data Engineers in Salt Lake City at **`$115k–$155k`** (59% comp savings vs SF's `$300k–$380k` Staff Data Eng at *Green*), paired with Utah commercial EV/grid power at **`$0.353/kWh`** (`1,357` chargers, **25% cheaper than CA's `$0.472/kWh`**). |
| **3. Dallas, TX (`Uptown / Frisco`)** | `bdfac0bb` · `e5041c13` · `a1dcecca` | **SEC Exhibit 99.1 (`cbre-ex99_1.htm`, `run bdfac0bb`)** captures Dallas-HQ **CBRE** acquiring *Onnec* to scale data-center & commercial infrastructure; **MOLTEN Cloud** (`run e5041c13`) expands engineering in Dallas (`$70k–$90k + eq`); Texas regular fuel sits at **`$3.72/gal`** & diesel at **`$5.74/gal`** (**38% below CA**). |

---

## Slide 04 // Predicted Hotspots & Interactive 3D Office Models
**Where big corporations move next—and interactive 3D models of the offices built there:**

1. **Astana / Almaty, Kazakhstan (`84% Probability`):** *Eurasian AI & Sovereign Compute Twin Towers* (`42,000 m² · 1,850 Desks · +24% Predicted 12m Rent Delta`).
2. **Salt Lake City, Utah (`89% Probability`):** *Wasatch Mass-Timber & Solar AI Campus* (`28,500 m² · 1,200 Desks · +18% Predicted 12m Rent Delta`).
3. **Dallas, Texas (`91% Probability`):** *Uptown Skybridge Hyperscale HQ* (`64,000 m² · 3,100 Desks · +21% Predicted 12m Rent Delta`).
- Includes an interactive **4-Stage Causal Chain Scrubber** (`01 Signals → 02 HQ & Jobs → 03 Demand & Rents → 04 New Businesses`) that dynamically builds the 3D office campus and surrounding residential & retail blocks in real time.

---

## Slide 05 // Why the Live App Demo Matters
- **Working Live Demo (50% of Judging):** Explore the interactive 3D office models in the main app (`/?view=hotspots`), toggle any of the 12 Glasser sources, inspect the USD budget preflight, and watch `gemini-4-argon` generate live neighborhood & HQ predictions (`/?hq=1`).
- **Closed Verification Loop (25% + 15%):** Benchmarked across 10 historical daily cutoffs (50 questions, 32,490 records). `gemini-4-argon` achieves **#1 Brier calibration (0.1759)** and **#1 Blinded Judge score (3.98/5)**.
