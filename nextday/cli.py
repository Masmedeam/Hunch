import argparse
import json
import sys
from pathlib import Path

from .client import APIError, Glasser, save_json
from .collector import run_batch
from .plans import build_plan


def main():
    parser = argparse.ArgumentParser(description="Glasser news and social data collector")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("catalog", help="Free catalog download and authentication check")
    p = sub.add_parser("plan", help="Generate a frozen week-discovery plan (offline)")
    p.add_argument("--coverage", default="config/coverage.json")
    p.add_argument("--output", default="data/plan.json")
    p.add_argument("--news-only", action="store_true", help="Date-bounded Exa article text by topic/region")
    p.add_argument("--verticals", nargs="*", choices=["zillow", "airbnb", "linkedin", "gas", "signals", "keepa", "carfax"], help="Include Zillow, Airbnb, LinkedIn, AAA Gas, Market Signals, Keepa or Carfax verticals")
    p = sub.add_parser("collect", help="Inspect/validate; paid calls ONLY with --execute")
    p.add_argument("--plan", default="data/plan.json")
    p.add_argument("--batch", required=True)
    p.add_argument("--budget", default="1.00")
    p.add_argument("--execute", action="store_true")
    p.add_argument("--root", default="data")
    p = sub.add_parser("benchmark-plan", help="Freeze benchmark protocol and prepare historical collection plans")
    p.add_argument("--root", default="data/benchmarks/retrospective-v0")
    p.add_argument("--phase", choices=["audit", "core", "news", "continuation", "youtube-dates"], required=True)
    p.add_argument("--output", required=True)
    p = sub.add_parser("benchmark-build", help="Offline: build isolated public histories/questions and hidden resolutions")
    p.add_argument("--root", default="data/benchmarks/retrospective-v0")
    p = sub.add_parser("normalize", help="Rebuild normalized observations and exports offline")
    p.add_argument("--root", default="data")
    p.add_argument("--cutoff", help="Optional UTC ISO timestamp for frozen export")
    p.add_argument("--since", help="Optional lower bound on evidence capture time for a weekly package")
    p = sub.add_parser("followup", help="Offline plan for hashtag details and tracked video metrics")
    p.add_argument("--root", default="data")
    p.add_argument("--output", default="data/followup-plan.json")
    p.add_argument("--limit", type=int, default=10, help="Maximum retained videos per platform")
    p.add_argument("--refresh", action="store_true", help="Re-fetch already tracked detail IDs instead of discovery enrichment")
    sub.add_parser("gemini-check", help="Free metadata/access listing check for Gemini 4 Argon")
    p = sub.add_parser("predict", help="Prepare/count tokens; generate forecasts ONLY with --execute")
    p.add_argument("--name", required=True)
    p.add_argument("--root", default="data")
    p.add_argument("--evidence-dir")
    p.add_argument("--limit", type=int, default=64)
    p.add_argument("--text-chars", type=int, default=3500)
    p.add_argument("--forecasts", type=int, default=5)
    p.add_argument("--thinking", choices=["low", "medium", "high"], default="low")
    p.add_argument("--max-output-tokens", type=int, default=8192)
    p.add_argument("--budget", default="0.30")
    p.add_argument("--target-start", help="Future timezone-aware ISO timestamp; default next UTC midnight")
    p.add_argument("--horizon-hours", type=int, default=24)
    p.add_argument("--instructions", help="Optional domain/task instructions; base safety/time rules still apply")
    p.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    try:
        if args.command == "catalog":
            c = Glasser()
            b = c.request("GET", "/v1/balance")
            catalog = c.catalog()
            save_json("data/catalog.json", catalog)
            print(f"Authenticated; available USD {b.get('available_usd')}; {len(catalog['entries'])} endpoints.")
        elif args.command == "plan":
            if Path(args.output).exists():
                raise ValueError("Plan file already exists; choose a new output to preserve resumability.")
            plan = build_plan(args.coverage, news_only=args.news_only, verticals=args.verticals)
            save_json(args.output, plan)
            print(f"Saved {len(plan['jobs'])} jobs to {args.output}. No API calls made.")
        elif args.command == "collect":
            run_batch(args.plan, args.batch, args.budget, args.execute, args.root)
        elif args.command == "normalize":
            from .normalize import rebuild
            print(json.dumps(rebuild(args.root, args.cutoff, args.since), indent=2))
        elif args.command == "followup":
            from .plans import followup_plan
            if Path(args.output).exists():
                raise ValueError("Plan file already exists; choose a new output.")
            plan = followup_plan(args.root, args.limit, args.refresh)
            save_json(args.output, plan)
            print(f"Saved {len(plan['jobs'])} detail calls to {args.output}. No API calls made.")
        elif args.command == "gemini-check":
            from .gemini import Gemini
            client = Gemini()
            info = client.info()
            save_json("data/gemini/argon-model.json", info)
            print(json.dumps(info, indent=2))
        elif args.command == "predict":
            from .prediction import prediction_run
            result = prediction_run(args.name, args.execute, args.root, args.evidence_dir, args.limit,
                                    args.text_chars, args.forecasts, args.thinking, args.max_output_tokens,
                                    args.budget, args.target_start, args.horizon_hours, args.instructions)
            if args.execute:
                print(f"Saved forecast to {args.root}/predictions/{args.name}/forecast.json")
                print("Model-reported usage:", json.dumps(result["metadata"]["usage"]))
        elif args.command == "benchmark-plan":
            from .benchmark import make_plan, continuation_plan, youtube_detail_plan
            if Path(args.output).exists():
                raise ValueError("Benchmark plan already exists; use another output path to preserve resumability.")
            plan = continuation_plan(args.root) if args.phase == "continuation" else (youtube_detail_plan(args.root) if args.phase == "youtube-dates" else make_plan(args.phase, args.root))
            save_json(args.output, plan)
            print(f"Saved {len(plan['jobs'])} historical acquisition jobs. No paid calls made.")
        else:
            from .benchmark import build_dataset
            print(json.dumps(build_dataset(args.root), indent=2))
    except (APIError, ValueError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
