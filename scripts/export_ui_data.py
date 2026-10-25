"""Export a credential-free, provenance-rich JSON bundle for the Cloudflare UI."""
import json
from collections import Counter
from decimal import Decimal
from pathlib import Path


def load_json(path, default=None):
    p = Path(path)
    if not p.exists():
        return default
    return json.loads(p.read_text())


def summarize_batches(batches_dir):
    rows = []
    total_charged = Decimal("0")
    total_reserved = Decimal("0")
    total_calls = 0
    for path in sorted(Path(batches_dir).glob("*/manifest.json")):
        m = json.loads(path.read_text())
        statuses = Counter(j.get("status", "UNKNOWN") for j in m.get("jobs", []))
        sources = Counter(j.get("spec", {}).get("source", "unknown") for j in m.get("jobs", []))
        charged = sum((Decimal(j.get("charge_usd") or "0") for j in m.get("jobs", [])), Decimal("0"))
        reserved = Decimal(m.get("reserved_usd") or "0")
        total_charged += charged
        total_reserved += reserved
        total_calls += len(m.get("jobs", []))
        rows.append({
            "batch": m.get("batch"),
            "created_at": m.get("created_at"),
            "finished_at": m.get("finished_at"),
            "planned_calls": len(m.get("jobs", [])),
            "statuses": dict(statuses),
            "sources": dict(sources),
            "budget_usd": m.get("budget_usd"),
            "reserved_usd": str(reserved),
            "charged_usd": str(charged),
        })
    return {
        "batches": rows,
        "total_calls": total_calls,
        "total_reserved_usd": str(total_reserved),
        "total_charged_usd": str(total_charged),
    }


def export_contracts(contracts_dir="data/contracts"):
    items = []
    for path in sorted(Path(contracts_dir).glob("*.json")):
        c = json.loads(path.read_text())
        schema = c.get("input_schema") or {}
        items.append({
            "id": path.stem,
            "provider": c.get("provider"),
            "provider_label": c.get("provider_label"),
            "endpoint": c.get("endpoint"),
            "endpoint_version": c.get("endpoint_version"),
            "name": c.get("name"),
            "description": c.get("description"),
            "tags": c.get("tags") or [],
            "price": c.get("price"),
            "run_mode": c.get("run_mode"),
            "timeout_ms": c.get("timeout_ms"),
            "required_inputs": schema.get("required") or [],
            "properties": {
                k: {
                    "type": v.get("type"),
                    "enum": v.get("enum"),
                    "maximum": v.get("maximum"),
                    "minimum": v.get("minimum"),
                    "maxLength": v.get("maxLength"),
                }
                for k, v in (schema.get("properties") or {}).items()
            },
            "sample_input": c.get("sample_input"),
        })
    return items


def trim_record(rec, max_chars=520):
    out = dict(rec)
    if out.get("text") and len(out["text"]) > max_chars:
        out["text_preview"] = out["text"][:max_chars] + "…"
        out["text_full_length"] = len(out["text"])
        out["text"] = out["text"][:max_chars]
    return out


def export_ui_bundle(out_dir="ui/public/data"):
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    cases_dir = out_path / "cases"
    cases_dir.mkdir(parents=True, exist_ok=True)

    bench_root = Path("data/benchmarks/retrospective-v0")
    protocol = load_json(bench_root / "protocol.json", {})
    integrity = load_json(bench_root / "integrity_report.json", {})
    amendments = load_json(bench_root / "acquisition-amendments.json", {})
    regional_amendment = load_json(bench_root / "regional-acquisition-amendment.json", {})
    resume_status = load_json(bench_root / "private_raw/resume-status.json", {})
    index = load_json(bench_root / "public_inputs/index.json", {"cases": []})

    bench_batches = summarize_batches(bench_root / "private_raw/batches")
    prospective_batches = summarize_batches("data/batches")

    cases_summary = []
    for entry in index.get("cases", []):
        cid = entry["case_id"]
        pub_dir = bench_root / "public_inputs" / cid
        priv_dir = bench_root / "private_outcomes" / cid
        compact = load_json(pub_dir / "history.compact.json", {})
        full_hist = load_json(pub_dir / "history.json", {})
        questions = load_json(pub_dir / "questions.json", {"questions": []})
        resolution = load_json(priv_dir / "resolution.json", {"resolutions": [], "reference_evidence": []})

        full_evidence = full_hist.get("evidence", [])
        kind_counts = Counter(r.get("kind") for r in full_evidence)
        topic_counts = Counter(r.get("topic") for r in full_evidence if r.get("kind") == "article")
        platform_counts = Counter(r.get("platform") for r in full_evidence if r.get("kind") == "social_post")

        ref_evidence = resolution.get("reference_evidence", [])
        ref_kind_counts = Counter(r.get("kind") for r in ref_evidence)

        case_detail = {
            "case_id": cid,
            "cutoff_exclusive": compact.get("cutoff_exclusive"),
            "history_start": compact.get("history_start"),
            "target_start": compact.get("target_start"),
            "target_end": compact.get("target_end"),
            "input_profile": compact.get("input_profile"),
            "limitations": compact.get("limitations", []),
            "filing_counts": compact.get("filing_counts", []),
            "publication_counts": compact.get("publication_counts", []),
            "questions": questions.get("questions", []),
            "resolutions": resolution.get("resolutions", []),
            "excluded_reference_records": resolution.get("excluded_reference_records", {}),
            "stats": {
                "full_history_records": len(full_evidence),
                "compact_history_records": len(compact.get("evidence", [])),
                "kind_counts": dict(kind_counts),
                "topic_counts": dict(topic_counts),
                "platform_counts": dict(platform_counts),
                "reference_evidence_count": len(ref_evidence),
                "reference_kind_counts": dict(ref_kind_counts),
                "history_sha256": entry.get("history_sha256"),
                "compact_history_sha256": entry.get("compact_history_sha256"),
                "questions_sha256": entry.get("questions_sha256"),
            },
            "evidence": [trim_record(r, 900) for r in compact.get("evidence", [])],
            "reference_evidence": [trim_record(r, 700) for r in ref_evidence[:80]],
        }
        (cases_dir / f"{cid}.json").write_text(json.dumps(case_detail, ensure_ascii=False) + "\n")

        cases_summary.append({
            "case_id": cid,
            "cutoff_exclusive": compact.get("cutoff_exclusive"),
            "history_start": compact.get("history_start"),
            "target_start": compact.get("target_start"),
            "target_end": compact.get("target_end"),
            "stats": case_detail["stats"],
            "filing_counts": compact.get("filing_counts", []),
            "publication_counts": compact.get("publication_counts", []),
            "questions": questions.get("questions", []),
            "resolutions": resolution.get("resolutions", []),
            "sample_evidence": [trim_record(r, 380) for r in compact.get("evidence", [])[:36]],
            "sample_reference": [trim_record(r, 380) for r in ref_evidence[:24]],
        })

    # Prospective live prediction & evidence
    argon_forecast = load_json("data/predictions/argon-pilot/forecast.json", {})
    argon_audit = load_json("data/predictions/argon-pilot/audit.json", {})
    argon_evidence = load_json("data/predictions/argon-pilot/evidence.json", [])
    prospective_quality = load_json("data/exports/latest/quality_report.json", {})

    # Compute empirical baseline stats across the 10 cases
    q1_weekday_up = [
        res["value"]
        for c in cases_summary
        for q, res in zip(c["questions"], c["resolutions"])
        if q["id"].endswith("-q1") and q["answer_type"] == "binary" and isinstance(res.get("value"), bool)
    ]
    q2_events = [
        res["value"]
        for c in cases_summary
        for q, res in zip(c["questions"], c["resolutions"])
        if q["id"].endswith("-q2") and isinstance(res.get("value"), bool)
    ]
    q3_counts = [
        res["value"]
        for c in cases_summary
        for q, res in zip(c["questions"], c["resolutions"])
        if q["id"].endswith("-q3") and isinstance(res.get("value"), (int, float))
    ]

    bundle = {
        "generated_at": integrity.get("created_at"),
        "project": {
            "name": "NEXTDAY // Temporal Evidence & Forecasting Observatory",
            "version": "0.2.0",
            "model": "gemini-4-argon",
        },
        "configs": {
            "coverage": load_json("config/coverage.json", {}),
            "benchmark_plan": load_json("config/benchmark-plan.json", {}),
            "forecast_schema": load_json("config/forecast-schema.json", {}),
        },
        "contracts": export_contracts("data/contracts"),
        "benchmark": {
            "protocol": protocol,
            "integrity": integrity,
            "amendments": amendments,
            "regional_amendment": regional_amendment,
            "resume_status": resume_status,
            "batches_summary": bench_batches,
            "cases": cases_summary,
            "empirical_baselines": {
                "q1_weekday_cases": len(q1_weekday_up),
                "q1_up_rate": round(sum(1 for x in q1_weekday_up if x) / len(q1_weekday_up), 4) if q1_weekday_up else None,
                "q2_resolved_cases": len(q2_events),
                "q2_event_rate": round(sum(1 for x in q2_events if x) / len(q2_events), 4) if q2_events else None,
                "q3_resolved_cases": len(q3_counts),
                "q3_mean_posts": round(sum(q3_counts) / len(q3_counts), 2) if q3_counts else None,
                "q3_min_posts": min(q3_counts) if q3_counts else None,
                "q3_max_posts": max(q3_counts) if q3_counts else None,
            },
        },
        "prospective": {
            "quality_report": prospective_quality,
            "batches_summary": prospective_batches,
            "argon_pilot": {
                "forecast": argon_forecast,
                "audit": argon_audit,
                "evidence": [trim_record(e, 700) for e in argon_evidence],
            },
        },
    }

    (out_path / "bundle.json").write_text(json.dumps(bundle, ensure_ascii=False) + "\n")
    return {
        "bundle_bytes": (out_path / "bundle.json").stat().st_size,
        "cases_exported": len(cases_summary),
        "contracts_exported": len(bundle["contracts"]),
    }


if __name__ == "__main__":
    print(json.dumps(export_ui_bundle(), indent=2))
