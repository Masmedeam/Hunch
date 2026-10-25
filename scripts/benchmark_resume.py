"""Resume the approved historical scrape; dry-run/status-only unless --execute.

Run from the project root. Wait for existing collection workers to finish before
using --execute. Existing batch names/idempotency keys are deliberately reused.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nextday.benchmark import DEFAULT_ROOT, build_dataset, compatible_continuations, continuation_plan, youtube_detail_plan
from nextday.client import save_json
from nextday.collector import run_batch
from nextday.checkpoint import write_checkpoint


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true", help="Resume paid scraping within the existing $10 approval, then build data")
    parser.add_argument("--root", default=DEFAULT_ROOT)
    args = parser.parse_args()
    root = Path(args.root) / "private_raw"
    if not args.execute:
        write_checkpoint(args.root)
        print("Updated BENCHMARK_PROGRESS.md. No API calls made. Add --execute only after existing workers finish.")
        return
    for name, budget in [("audit", "1.00"), ("core", "1.00"), ("news", "3.00"), ("filing-documents", "0.01"), ("regional", "2.00")]:
        path = root / "plans" / (name + ".json")
        if not path.exists():
            raise ValueError(f"Missing frozen plan: {path}. Do not invent replacement batch inputs.")
        run_batch(path, name, budget, True, root)
        write_checkpoint(args.root)
    for number in range(1, 3):
        name = f"pagination-{number:02d}"
        path = root / "plans" / (name + ".json")
        compatible_path = root / "plans" / (name + "-compatible.json")
        if compatible_path.exists():
            path = compatible_path
        if path.exists():
            plan = json.loads(path.read_text())
        else:
            plan = continuation_plan(args.root)
            save_json(path, plan)
        compatible = compatible_continuations(plan)
        if compatible["jobs"] != plan["jobs"]:
            if (root / "batches" / name / "manifest.json").exists():
                raise ValueError("Cannot change an already admitted pagination batch; inspect its manifest manually.")
            # Original invalid plan remains untouched; no Run was admitted for it.
            path = root / "plans" / (name + "-compatible.json")
            plan = compatible
            save_json(path, plan)
        if not plan["jobs"]:
            break
        run_batch(path, name, "0.50", True, root)
        write_checkpoint(args.root)
    cik_path = root / "plans/cik-verify.json"
    if not cik_path.exists():
        save_json(cik_path, {"schema_version": 1, "phase": "cik_verify", "jobs": [
            {"source": "benchmark_company_cik", "provider": "secapi", "endpoint": "/filings/search",
             "input": {"query": "ticker:XOM AND cik:34088", "size": 1, "from": 0, "sortOrder": "desc"}}
        ]})
    run_batch(cik_path, "cik-verify", "0.01", True, root)
    path = root / "plans/youtube-dates.json"
    if path.exists():
        plan = json.loads(path.read_text())
    else:
        plan = youtube_detail_plan(args.root)
        save_json(path, plan)
    if plan["jobs"]:
        run_batch(path, "youtube-dates", "0.50", True, root)
    report = build_dataset(args.root)
    write_checkpoint(args.root)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
