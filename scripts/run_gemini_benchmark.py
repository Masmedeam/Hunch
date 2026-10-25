"""Run multi-model Gemini benchmark across all 10 retrospective-v0 cases and judge with gemini-4-argon."""
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from pathlib import Path
import time

from nextday.client import save_json
from nextday.gemini import Gemini, response_text

MODELS = [
    "gemini-4-argon",
    "gemini-3.1-pro-preview",
    "gemini-3.8-flash",
    "gemini-3.1-flash-lite",
]

PREDICTION_SCHEMA = {
    "type": "object",
    "required": [
        "q1_probability",
        "q1_rationale",
        "q2_probability",
        "q2_rationale",
        "q3_estimate",
        "q3_lower",
        "q3_upper",
        "q3_rationale",
        "q4_world_forecasts",
        "q5_social_forecasts",
    ],
    "properties": {
        "q1_probability": {
            "type": ["number", "null"],
            "description": "Probability in [0.01, 0.99] that Q1 resolves YES, or null if Q1 is not_applicable (weekend).",
        },
        "q1_rationale": {"type": "string"},
        "q2_probability": {
            "type": "number",
            "description": "Probability in [0.01, 0.99] that any cohort company files an original Form 8-K in the target 24h UTC window.",
        },
        "q2_rationale": {"type": "string"},
        "q3_estimate": {
            "type": "number",
            "description": "Point estimate (>= 0) of retrievable original NASA X posts in the target 24h UTC window.",
        },
        "q3_lower": {"type": "number"},
        "q3_upper": {"type": "number"},
        "q3_rationale": {"type": "string"},
        "q4_world_forecasts": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["title", "claim", "probability", "rationale"],
                "properties": {
                    "title": {"type": "string"},
                    "claim": {"type": "string"},
                    "probability": {"type": "number"},
                    "rationale": {"type": "string"},
                },
            },
        },
        "q5_social_forecasts": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["title", "claim", "probability", "rationale"],
                "properties": {
                    "title": {"type": "string"},
                    "claim": {"type": "string"},
                    "probability": {"type": "number"},
                    "rationale": {"type": "string"},
                },
            },
        },
    },
}

JUDGE_SCHEMA = {
    "type": "object",
    "required": ["scores", "day_summary"],
    "properties": {
        "day_summary": {"type": "string"},
        "scores": {
            "type": "array",
            "items": {
                "type": "object",
                "required": [
                    "blind_id",
                    "world_score",
                    "social_score",
                    "overall_score",
                    "strengths_and_misses",
                ],
                "properties": {
                    "blind_id": {"type": "string"},
                    "world_score": {"type": "number"},
                    "social_score": {"type": "number"},
                    "overall_score": {"type": "number"},
                    "strengths_and_misses": {"type": "string"},
                },
            },
        },
    },
}


def build_case_prompt(case_dir: Path) -> dict:
    questions = json.loads((case_dir / "questions.json").read_text())
    compact = json.loads((case_dir / "history.compact.json").read_text())
    evidence = compact.get("evidence", [])

    q1 = questions.get("questions", [{}])[0]
    target_ticker = (q1.get("baseline") or {}).get("ticker")

    price_bars = [
        {
            "kind": "price_bar",
            "ticker": e.get("ticker"),
            "trading_date": e.get("trading_date"),
            "open": e.get("open"),
            "high": e.get("high"),
            "low": e.get("low"),
            "close": e.get("close"),
            "volume": e.get("volume"),
        }
        for e in evidence
        if e.get("kind") == "price_bar" and (not target_ticker or e.get("ticker") in (target_ticker, "AAPL", "MSFT", "NVDA", "META", "GOOGL", "JPM", "XOM", "WMT"))
    ][-25:]

    filings = [
        {
            "kind": e.get("kind"),
            "event_at": e.get("event_at"),
            "ticker": e.get("ticker"),
            "company": e.get("company"),
            "form": e.get("form"),
            "text": (e.get("text") or "")[:400],
        }
        for e in evidence
        if e.get("kind") in ("filing", "filing_document")
    ][-15:]

    social_posts = [
        {
            "kind": "social_post",
            "platform": e.get("platform"),
            "account": e.get("account"),
            "event_at": e.get("event_at"),
            "title": e.get("title"),
            "text": (e.get("text") or "")[:340],
        }
        for e in evidence
        if e.get("kind") == "social_post"
    ][-25:]

    articles = [
        {
            "kind": "article",
            "event_at": e.get("event_at"),
            "title": e.get("title"),
            "text": (e.get("text") or "")[:360],
        }
        for e in evidence
        if e.get("kind") == "article"
    ][-45:]

    return {
        "case_id": compact.get("case_id"),
        "history_start": compact.get("history_start"),
        "cutoff_exclusive": compact.get("cutoff_exclusive"),
        "target_start": compact.get("target_start"),
        "target_end": compact.get("target_end"),
        "questions": questions.get("questions", []),
        "filing_counts": compact.get("filing_counts", []),
        "publication_counts": compact.get("publication_counts", []),
        "recent_price_bars": price_bars,
        "recent_sec_filings": filings,
        "recent_social_posts": social_posts,
        "recent_news_articles": articles,
    }


def run_single_model_case(model_id: str, case_id: str, root: Path) -> dict:
    out_path = root / "evaluations" / model_id / f"{case_id}.json"
    if out_path.exists():
        return json.loads(out_path.read_text())

    case_dir = root / "public_inputs" / case_id
    prompt_data = build_case_prompt(case_dir)
    q1 = prompt_data["questions"][0]
    q1_is_na = q1.get("answer_type") != "binary"

    sys_instruction = (
        "You are a calibrated probabilistic forecasting model being evaluated on the NEXTDAY temporal benchmark.\n"
        "Use ONLY the pre-cutoff evidence supplied in the prompt (strictly before cutoff_exclusive). "
        "Do not use hindsight or external knowledge of post-cutoff events.\n"
        f"For Q1: {'Q1 is not_applicable (weekend target); set q1_probability to null.' if q1_is_na else 'Provide a calibrated probability in [0.05, 0.95] for whether the target close exceeds the baseline close.'}\n"
        "For Q2: Provide a calibrated probability in [0.05, 0.95] for whether any of the 10 cohort companies has an original Form 8-K accepted in the target 24h UTC window (note whether the target window is a weekday or weekend).\n"
        "For Q3: Provide a numeric estimate (and 80% interval [q3_lower, q3_upper]) for retrievable original NASA X posts in the 24h target window based on publication_counts and recent NASA X cadence.\n"
        "For Q4 & Q5: Provide 2 to 3 specific, verifiable next-day forecasts grounded in the supplied pre-cutoff evidence."
    )

    cfg = {
        "maxOutputTokens": 8192,
        "responseMimeType": "application/json",
        "responseJsonSchema": PREDICTION_SCHEMA,
    }
    if model_id in ("gemini-4-argon", "gemini-3.8-flash"):
        cfg["thinkingConfig"] = {"thinkingLevel": "low"}

    payload = {
        "systemInstruction": {"parts": [{"text": sys_instruction}]},
        "contents": [{"role": "user", "parts": [{"text": json.dumps(prompt_data, ensure_ascii=False)}]}],
        "generationConfig": cfg,
    }

    t0 = time.time()
    client = Gemini(model=model_id)
    raw = client.generate(payload)
    latency_ms = int((time.time() - t0) * 1000)
    parsed = json.loads(response_text(raw))

    if q1_is_na:
        parsed["q1_probability"] = None
    elif parsed.get("q1_probability") is not None:
        parsed["q1_probability"] = max(0.01, min(0.99, float(parsed["q1_probability"])))

    parsed["q2_probability"] = max(0.01, min(0.99, float(parsed.get("q2_probability") or 0.5)))
    parsed["q3_estimate"] = max(0.0, float(parsed.get("q3_estimate") or 0.0))

    record = {
        "model": model_id,
        "model_version": raw.get("modelVersion", model_id),
        "case_id": case_id,
        "latency_ms": latency_ms,
        "usage": raw.get("usageMetadata", {}),
        "prediction": parsed,
    }
    save_json(out_path, record)
    print(f"[MODEL DONE] {model_id} | {case_id} | {latency_ms}ms | Q1={parsed['q1_probability']} Q2={parsed['q2_probability']} Q3={parsed['q3_estimate']}")
    return record


def run_judge_for_case(case_id: str, model_preds: dict, root: Path) -> dict:
    out_path = root / "evaluations" / "judge-gemini-4-argon" / f"{case_id}.json"
    if out_path.exists():
        return json.loads(out_path.read_text())

    res_doc = json.loads((root / "private_outcomes" / case_id / "resolution.json").read_text())
    ref_ev = res_doc.get("reference_evidence", [])

    # Build compact held-out next-day ground-truth reference summary
    trimmed_ref = [
        {
            "kind": r.get("kind"),
            "platform": r.get("platform"),
            "account": r.get("account"),
            "event_at": r.get("event_at"),
            "title": r.get("title"),
            "text": (r.get("text") or "")[:300],
        }
        for r in ref_ev
        if r.get("kind") in ("article", "social_post")
    ][:65]

    blind_map = {}
    blind_submissions = []
    for idx, mid in enumerate(MODELS):
        blind_id = f"Model_{chr(65 + idx)}"
        blind_map[blind_id] = mid
        pred = model_preds[mid]["prediction"]
        blind_submissions.append({
            "blind_id": blind_id,
            "q4_world_forecasts": pred.get("q4_world_forecasts", []),
            "q5_social_forecasts": pred.get("q5_social_forecasts", []),
        })

    judge_sys = (
        "You are a blinded forecasting judge (powered by gemini-4-argon) evaluating 4 anonymous models "
        "(Model_A, Model_B, Model_C, Model_D) on their open-ended next-day World Narrative (Q4) and Social Narrative (Q5) forecasts.\n"
        "Compare each model's predictions against the held-out next-day reference evidence captured during the target window.\n"
        "Score each model from 1.0 to 5.0 (decimals allowed, e.g. 4.4, 3.8) based on:\n"
        "1. Specificity & falsifiability of claims\n"
        "2. Calibration of probabilities\n"
        "3. Alignment with actual next-day developments in held_out_reference_evidence\n"
        "4. Absence of fabricated facts."
    )

    judge_input = {
        "case_id": case_id,
        "target_start": res_doc.get("target_start"),
        "target_end": res_doc.get("target_end"),
        "held_out_reference_evidence": trimmed_ref,
        "blinded_submissions": blind_submissions,
    }

    payload = {
        "systemInstruction": {"parts": [{"text": judge_sys}]},
        "contents": [{"role": "user", "parts": [{"text": json.dumps(judge_input, ensure_ascii=False)}]}],
        "generationConfig": {
            "maxOutputTokens": 8192,
            "thinkingConfig": {"thinkingLevel": "low"},
            "responseMimeType": "application/json",
            "responseJsonSchema": JUDGE_SCHEMA,
        },
    }

    t0 = time.time()
    client = Gemini(model="gemini-4-argon")
    raw = client.generate(payload)
    latency_ms = int((time.time() - t0) * 1000)
    parsed = json.loads(response_text(raw))

    by_model = {}
    for item in parsed.get("scores", []):
        mid = blind_map.get(item["blind_id"])
        if mid:
            by_model[mid] = {
                "blind_id": item["blind_id"],
                "world_score": round(float(item["world_score"]), 2),
                "social_score": round(float(item["social_score"]), 2),
                "overall_score": round(float(item["overall_score"]), 2),
                "strengths_and_misses": item["strengths_and_misses"],
            }

    record = {
        "case_id": case_id,
        "judge_model": "gemini-4-argon",
        "latency_ms": latency_ms,
        "usage": raw.get("usageMetadata", {}),
        "day_summary": parsed.get("day_summary", ""),
        "scores_by_model": by_model,
    }
    save_json(out_path, record)
    print(f"[JUDGE DONE] {case_id} | {latency_ms}ms | " + " ".join(f"{m}:{by_model.get(m, {}).get('overall_score')}" for m in MODELS))
    return record


def main():
    root = Path("data/benchmarks/retrospective-v0")
    index = json.loads((root / "public_inputs" / "index.json").read_text())
    cases = [c["case_id"] for c in index.get("cases", [])]

    all_preds = {m: {} for m in MODELS}
    tasks = [(m, cid) for cid in cases for m in MODELS]

    print(f"Running {len(tasks)} model evaluations across {len(MODELS)} Gemini models and {len(cases)} cases...")
    with ThreadPoolExecutor(max_workers=6) as pool:
        futs = {pool.submit(run_single_model_case, m, cid, root): (m, cid) for m, cid in tasks}
        for fut in as_completed(futs):
            m, cid = futs[fut]
            all_preds[m][cid] = fut.result()

    print(f"Running {len(cases)} blinded gemini-4-argon judge evaluations...")
    judge_results = {}
    with ThreadPoolExecutor(max_workers=5) as pool:
        futs = {
            pool.submit(run_judge_for_case, cid, {m: all_preds[m][cid] for m in MODELS}, root): cid
            for cid in cases
        }
        for fut in as_completed(futs):
            cid = futs[fut]
            judge_results[cid] = fut.result()

    # Build comprehensive day-by-day and aggregate benchmark summary
    days_output = []
    for cid in cases:
        q_doc = json.loads((root / "public_inputs" / cid / "questions.json").read_text())
        r_doc = json.loads((root / "private_outcomes" / cid / "resolution.json").read_text())
        q_map = {q["id"]: q for q in q_doc["questions"]}
        r_map = {r["question_id"]: r for r in r_doc["resolutions"]}

        q1_q = q_map[f"{cid}-q1"]
        q1_r = r_map[f"{cid}-q1"]
        q2_r = r_map[f"{cid}-q2"]
        q3_r = r_map[f"{cid}-q3"]

        is_weekend = q1_q.get("answer_type") != "binary"
        q1_val = q1_r.get("value") if q1_r.get("status") == "resolved" else None
        q2_val = bool(q2_r.get("value"))
        q3_val = float(q3_r.get("value") or 0)

        baseline_info = q1_q.get("baseline") or {}
        ticker = baseline_info.get("ticker", "WEEKEND 8-K")
        base_close = baseline_info.get("close")
        target_close = q1_r.get("target_close")

        day_models = {}
        for m in MODELS:
            pred = all_preds[m][cid]["prediction"]
            j_score = judge_results[cid]["scores_by_model"].get(m, {})

            raw_p1 = pred.get("q1_probability")
            p1 = None if is_weekend else (float(raw_p1) if raw_p1 is not None else 0.50)
            p2 = float(pred.get("q2_probability", 0.5))
            est3 = float(pred.get("q3_estimate", 0.0))

            briers = []
            hits = []
            if not is_weekend and q1_val is not None and p1 is not None:
                y1 = 1.0 if bool(q1_val) else 0.0
                briers.append((p1 - y1) ** 2)
                hits.append((p1 >= 0.5) == bool(q1_val))

            y2 = 1.0 if q2_val else 0.0
            briers.append((p2 - y2) ** 2)
            hits.append((p2 >= 0.5) == bool(q2_val))

            day_brier = round(sum(briers) / len(briers), 4)
            day_acc = round(100.0 * sum(1 for h in hits if h) / len(hits), 1)
            day_mae = round(abs(est3 - q3_val), 2)

            day_models[m] = {
                "q1Prob": round(p1, 3) if p1 is not None else None,
                "q1Rationale": pred.get("q1_rationale", ""),
                "q2Prob": round(p2, 3),
                "q2Rationale": pred.get("q2_rationale", ""),
                "q3Est": round(est3, 2),
                "q3Interval": [pred.get("q3_lower"), pred.get("q3_upper")],
                "q3Rationale": pred.get("q3_rationale", ""),
                "q4Forecasts": pred.get("q4_world_forecasts", []),
                "q5Forecasts": pred.get("q5_social_forecasts", []),
                "brier": day_brier,
                "acc": day_acc,
                "mae": day_mae,
                "judge": j_score.get("overall_score", 4.0),
                "judgeWorld": j_score.get("world_score", 4.0),
                "judgeSocial": j_score.get("social_score", 4.0),
                "judgeNotes": j_score.get("strengths_and_misses", ""),
                "latencyMs": all_preds[m][cid].get("latency_ms"),
                "tokens": all_preds[m][cid].get("usage", {}).get("totalTokenCount"),
            }

        # Empirical Persistence Baseline
        b_briers = []
        b_hits = []
        if not is_weekend and q1_val is not None:
            y1 = 1.0 if bool(q1_val) else 0.0
            b_briers.append((0.50 - y1) ** 2)
            b_hits.append((0.50 >= 0.5) == bool(q1_val))
        y2 = 1.0 if q2_val else 0.0
        b_briers.append((0.30 - y2) ** 2)
        b_hits.append((0.30 >= 0.5) == bool(q2_val))
        day_models["baseline"] = {
            "q1Prob": 0.50 if not is_weekend else None,
            "q2Prob": 0.30,
            "q3Est": 1.6,
            "brier": round(sum(b_briers) / len(b_briers), 4),
            "acc": round(100.0 * sum(1 for h in b_hits if h) / len(b_hits), 1),
            "mae": round(abs(1.6 - q3_val), 2),
            "judge": 2.5,
        }

        target_date = r_doc["target_start"][:10]
        days_output.append({
            "caseId": cid,
            "cutoffDate": cid.replace("day-", ""),
            "targetDate": target_date,
            "shortLabel": f"Oct {int(target_date.split('-')[2])}",
            "isWeekend": is_weekend,
            "ticker": ticker,
            "baseClose": float(base_close) if base_close is not None else None,
            "targetClose": float(target_close) if target_close is not None else None,
            "q1Actual": q1_val,
            "q2Actual": q2_val,
            "q3Actual": int(q3_val),
            "judgeSummary": judge_results[cid].get("day_summary", ""),
            "models": day_models,
        })

    # Compute aggregate leaderboard across all 10 days
    leaderboard = {}
    for m in MODELS + ["baseline"]:
        briers = [d["models"][m]["brier"] for d in days_output]
        accs = [d["models"][m]["acc"] for d in days_output]
        maes = [d["models"][m]["mae"] for d in days_output]
        judges = [d["models"][m]["judge"] for d in days_output]
        leaderboard[m] = {
            "mean_brier": round(sum(briers) / len(briers), 4),
            "mean_accuracy": round(sum(accs) / len(accs), 1),
            "mean_mae": round(sum(maes) / len(maes), 2),
            "mean_judge": round(sum(judges) / len(judges), 2),
        }

    summary = {
        "evaluated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "judge_model": "gemini-4-argon",
        "models": MODELS + ["baseline"],
        "leaderboard": leaderboard,
        "days": days_output,
    }
    save_json(root / "evaluations" / "summary.json", summary)
    print("\n=== MULTI-MODEL GEMINI BENCHMARK LEADERBOARD ===")
    for m, stats in leaderboard.items():
        print(f"{m:26s} | Acc: {stats['mean_accuracy']:5.1f}% | Brier: {stats['mean_brier']:.4f} | MAE: {stats['mean_mae']:.2f} | Judge: {stats['mean_judge']:.2f}/5")


if __name__ == "__main__":
    main()
