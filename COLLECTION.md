# Initial collection — 25 October 2026

**178 Glasser Runs, $0.40332 charged, within the approved $1 one-off allowance.**

- 1,838 normalized observations covering 1,521 distinct scoped entities.
- Compact context: 234 recent articles, 274 YouTube videos, 667 social posts, 282 trend terms, and 60 regional hashtag records.
- 240 article-body observations, including repeated discoveries; 31 bodies may be truncated at the requested character limit.
- Views appear in 1,312 observations; comment counts in 830. These are observation counts, not distinct-item counts.
- 526 comparable counter-change intervals, including repeated discoveries and one refresh of a fixed 30-post/video cohort. These are short observed intervals, **not seven-day gains**.
- Requested sampling regions: US, GB, India, Japan. English/Japanese queries. No claim of exhaustive worldwide coverage or verified audience geography.

## Important findings

1. **TikTok hashtag curves are stale:** all 462 returned points precede the last seven days; the latest points were about 10.7 days old when captured. Preserve them for audit, but do not interpret `time_range=7` as current-week freshness.
2. **Cheap news discovery was weak:** 16 empty queries and four returned articles without a usable recent date. Date-bounded Exa retrieval supplied the recent article context.
3. **YouTube trending was unavailable:** all four tested TikHub country requests returned a charged 404. Weekly video searches and a separate Shorts feed produced data; these are not equivalent to that endpoint.
4. **Some YouTube counters are rounded:** 42 metric observations have rounded display precision and are excluded from exact-counter growth calculations.
5. Missing/uncertain fields remain explicit. Raw responses, Run URLs, schemas, prices, inputs and capture times are retained.

## Start here

- `data/exports/latest/context.jsonl` — latest structured context, with observation references.
- `data/exports/latest/quality_report.json` — machine-readable audit.
- `data/exports/latest/engagement_growth.jsonl` — actual measured intervals.
- `data/exports/latest/trend_points.jsonl` — curve dates, native values and age flags.
- `data/observations.sqlite` — queryable store.
- `README.md` — collection, resume, fixed-cohort refresh and frozen-export commands.

No recurring scheduler is enabled. True observed weekly engagement requires retaining and refreshing the cohort over a week, with a separately approved ongoing budget.
