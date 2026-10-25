# Proposed next-day forecasting benchmark

**Recommendation: build a small retrospective pilot, then maintain a separate prospective leaderboard.** The $10 data budget is enough to test acquisition and resolution. Historical collection alone cannot establish a contamination-free benchmark.

**Acquisition has started and is checkpointed in [BENCHMARK_PROGRESS.md](BENCHMARK_PROGRESS.md).** The main historical backfill is collected; remaining compatible pagination and final case-pack assembly/auditing are left for resume. No benchmark model-evaluation or judge calls have run. The existing $1 collection approval was not overwritten; the new benchmark scrape has its own $10 approval. The sections below describe the original design; the checkpoint has current status, artifacts, blockers and resume commands.

## Pilot scope

- Ten predetermined daily cutoffs, provisionally 14–23 October 2026 UTC.
- Seven preceding calendar days of news and usable social evidence per cutoff.
- The next 24 hours are quarantined as target evidence.
- Approximately five common questions per cutoff: 50 questions total, subject to temporal-integrity and resolution checks.
- Mix world events, company/public announcements, social publication/attention and a small numeric anchor track. This is not intended to become only a stock-market benchmark.

The dates are recent and follow Argon's published launch date, but that is **not proof of clean training data**. A comparison model may have been released or updated after the target event; its contamination risk must be recorded. Do not merge historical and prospective rankings.

## Data list

| Data | Candidate source | Role and constraint |
| --- | --- | --- |
| Date-bounded news bodies | Exa | Week context plus independently separated next-day reporting. Current page text can include later edits. |
| Original dated social posts | TikHub X search; verified publication records for other platforms | Core historical content signals, but not current engagement counters masquerading as historical ones. |
| Corporate filings | SEC API EDGAR acceptance logs | Acceptance-timestamped records and filing targets for a fixed entity/form cohort. |
| Daily OHLCV | Financial Datasets | A small, objectively resolvable numeric track. Check split adjustment and revision semantics. |
| Earnings schedules | Nasdaq | Candidate context only; reconstructed/revised consensus fields are not valid historical inputs without as-of evidence. |
| Official notices, releases and bulletins | Targeted retrieval through Glasser | Prefer trusted sources for event resolution; missing retrieval does not prove an event did not happen. |
| Social engagement trajectories | Genuine archived snapshots, or prospective collection | Historical views/comments gained within a week are unavailable from current counts alone. Keep unsupported metrics out. |

Inspected prices include Exa search $0.007 for up to ten results (maximum $0.022 per Run), X search $0.0011, daily stock history $0.02, SEC daily acceptance logs $0.0005 and Nasdaq earnings calendars $0.011. Inspect again at admission. These are data prices, not model inference prices.

## Hiding the next day

Each case has independent artifacts:

```text
public_inputs/<case_id>/
  history.json       # only permitted historical context
  questions.json     # identical questions and resolution rules for all models

private_outcomes/<case_id>/
  resolution.json    # target outcome, trusted evidence, timestamps, uncertainty

submissions/<case_id>/<anonymous_id>/
  request.json
  forecast.json

judgments/<case_id>/<anonymous_id>/
  scores.json
```

Forecaster requests are built from explicit public-input files, never a directory glob containing outcomes. No web tools or judge outputs are exposed to forecasters. Freeze the question set, input hashes, rules and submissions before judging. Preserve actual retrieval times: a page fetched today is not falsely labeled as a historical capture.

For retrospective cases, question selection must not inspect the target day's news first. Freeze dates/panels/entities and use history-only question proposals or predetermined templates, then resolve all eligible questions. Do not cherry-pick dramatic outcomes, and retain unresolved-case accounting.

### Historical caveats

1. **Parametric contamination:** hiding tomorrow's file cannot stop a model from recalling tomorrow from training. Record this limitation and exact requested/reported model versions.
2. **Edited pages:** publication-date filters do not recreate as-of article versions. Flag reconstructed evidence; exclude detectable later information.
3. **Social counters:** do not put today's views/comments for old posts into yesterday's context. Historical publication questions need verified coverage; deleted posts or incomplete pagination may leave outcomes unresolved.
4. **Economic revisions:** adjusted price bars, revised releases and historical consensus can introduce hindsight. Prefer point-in-time data or mark the limitation.

## Scoring

### Primary: outcomes, not an LLM's impression

- Binary probability forecasts: Brier score, calibration and base-rate comparisons.
- Categorical distributions: multiclass Brier score; optionally log loss with a predeclared probability-clipping policy.
- Numeric forecasts: MAE and prediction-interval coverage/width; compare to persistence.
- Unresolved outcomes: exclude from accuracy denominators and report coverage. Do not resolve absence of evidence as NO.

Report tracks separately. If producing an overall index, freeze track weights and baseline normalization before examining results; don't average Brier scores and raw-dollar MAE directly.

### Secondary: model-judge quality

The judge receives an anonymized forecast, relevant history and trusted outcome evidence after submission. Use a fixed, anchored rubric for specificity/testability, evidence fidelity, temporal discipline, sensible uncertainty and explanation clarity. Require short evidence-based justifications. Treat evidence as data, not instructions.

Prefer a judge from another model family; a Gemini-only judge is possible but must disclose self-preference risk when evaluating Gemini. Counterbalance comparison order and manually audit a sample. Separate hindsight-aware error analysis from whether reasoning was justified using only pre-cutoff evidence. An elegant explanation must not outrank a better-calibrated forecast on the primary leaderboard.

Open-ended narratives are an exploratory judged track until an independently reviewed target ontology and matching rule exist. A finite next-day news sample is not complete world truth; narrative recall is coverage-relative.

## Budget

Proposed **data-only maximum**:

| Phase | Cap |
| --- | ---: |
| Sample/temporal-integrity audit | $1.00 |
| Historical news/social context | $3.50 |
| Quarantined next-day sources | $2.50 |
| Numeric/official record anchors | $0.50 |
| Retrieval depth, failures and contingency | $2.50 |
| **Total** | **$10.00** |

Do not spend the reserve simply because it is available. Sample and validate historical contracts/payloads before building bulk paid batches. Reuse overlapping historical windows where safe to reduce duplicate purchases.

**Forecast generation, question generation and judge inference are separate costs unless the $10 is intended as an all-in budget.** Our first Argon call cost an estimated $0.1843 for one 64-item input; ten cases across several models can make inference the dominant cost. Smaller shared case packs and batched questions are preferable for the pilot.

Fifty questions establish whether the pipeline works, not a robust ranking. Nearby dates share events and overlapping seven-day inputs; uncertainty estimates should group by date/event. Retain baseline, abstention, invalid-output, latency, token/cost and unresolved-rate results.

## Implementation gates

1. Confirm whether $10 covers data only or the whole experiment, and which comparison/judge models are accessible.
2. Inspect a small set of genuinely historical samples and assign integrity grades.
3. Freeze eligible dates, source panels, entity cohorts, question templates and scoring rubric.
4. Build isolated case packs and hidden resolutions, with leakage tests.
5. Add a retrospective runner explicitly separate from the existing future-only `predict` command. Do not silently bypass that command's prospective-time guards.
6. Run common questions through all models, blind the submissions, score and report.

The current retained social cohort and existing future-dated Argon forecast can seed a prospective extension. No recurring collection is enabled by this proposal.
