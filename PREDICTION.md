# Gemini 4 Argon — verified live test

**Access confirmed for `gemini-4-argon` using the local Gemini API key.** The metadata request, tiny generation test and mixed-evidence prediction all succeeded. The generation responses report `modelVersion: gemini-4-argon`; no model substitution was used.

## First prediction

- 64 deterministically sampled news/social evidence items out of 1,517 context entities.
- Evidence cutoff: **25 October 2026, 17:38:48 UTC**.
- Target window: **26 October 2026, 00:00–24:00 UTC**.
- Submitted and completed before the target window.
- Low thinking level; 8,192-token output/thinking cap.
- API usage: **72,786 input + 3,876 output tokens**.
- Estimated standard-price cost: **$0.184332**, without cache discounts; not an invoice. The separate tiny connectivity test adds approximately $0.000190.
- Five forecasts passed JSON-schema, supplied-reference, interval and distribution consistency checks.

The returned output spans cyclone classification, UK power restoration, META daily returns, US diplomatic/military developments, and YouTube video views. It demonstrates binary, categorical and numerical predictions in one common envelope. These are **model predictions, not verified facts or measured forecasting performance**.

## Files

- `data/predictions/argon-pilot/forecast.json` — validated output and local run metadata.
- `data/predictions/argon-pilot/response.json` — unchanged provider response.
- `data/predictions/argon-pilot/request.json` / `prompt.txt` — frozen model input.
- `data/predictions/argon-pilot/evidence.json` — exact supplied evidence and provenance.
- `data/predictions/argon-pilot/audit.json` — offline review annotations.
- `config/forecast-schema.json` — general, model-neutral forecast contract.

## Review before scoring

1. **Temporal precision:** the cyclone claim says “before the end” but its resolution rule specifies bulletins inside the target window. Align the claim with the rule and distinguish new intensification from continued classification.
2. **Atomic claims:** the US geopolitical forecast combines embassy departure/closure decisions with military strikes. Splitting these would make interpretation and scoring cleaner.
3. **Measurable claims:** the META forecast contains vague “investor scrutiny” and “elevated trading volume” language in addition to numerical return bins. Score only an agreed measurable target, not an undefined composite.
4. **Resolution availability:** missing utility reports must mean unresolved, not automatically NO. The YouTube counter needs a predeclared collection tolerance/cache policy around the target endpoint.
5. **Probability quality:** numeric probabilities are not calibrated merely because they parse. Baselines, repeated prospective runs and independent outcome resolution are needed.

The original output is preserved. Do not silently rewrite its rules after observing outcomes; any revised question set must be frozen and re-forecast before the relevant window starts. No outcome resolution or recurring prediction calls have run.
