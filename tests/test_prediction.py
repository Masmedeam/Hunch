import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from nextday.gemini import response_text
from nextday.normalize import iso, write_jsonl
from nextday.prediction import prediction_run, select_evidence, validate_forecasts


def forecast(evidence_id="obs-1"):
    return {"overview": "Test", "limitations": ["Limited evidence"], "forecasts": [
        {"id": "F1", "title": "Test forecast", "claim": "A defined event happens", "forecast_type": "binary_event",
         "scope": "Test entity", "status": "forecast", "probability": 0.6, "estimate": None, "outcomes": [],
         "rationale": "Observed evidence", "evidence_ids": [evidence_id], "assumptions": [], "disconfirmation_signals": [],
         "resolution": {"mode": "measurable", "rule": "Check a defined source during the target window", "sources": ["https://example.com"]}}
    ]}


class FakeGemini:
    model = "gemini-4-argon"

    def __init__(self, invalid=False):
        self.generations = 0
        self.invalid = invalid

    def info(self):
        return {"name": "models/gemini-4-argon", "inputTokenLimit": 1048576, "outputTokenLimit": 32768,
                "supportedGenerationMethods": ["generateContent", "countTokens"]}

    def count_tokens(self, payload):
        return {"totalTokens": 1000}

    def generate(self, payload):
        self.generations += 1
        result = forecast("invented" if self.invalid else "obs-1")
        return {"modelVersion": self.model, "candidates": [{"finishReason": "STOP", "content": {"parts": [{"text": json.dumps(result)}]}}],
                "usageMetadata": {"promptTokenCount": 1000, "candidatesTokenCount": 200, "thoughtsTokenCount": 20}}


class PredictionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.item = {"observation_id": "obs-1", "entity_id": "web:1", "platform": "web", "kind": "article",
                     "topic": "technology", "requested_region": "US", "captured_at": iso(datetime.now(timezone.utc) - timedelta(minutes=2)),
                     "title": "Test", "text": "Evidence text", "metrics": {}, "extra": {}}
        write_jsonl(self.root / "exports/latest/context.jsonl", [self.item])
        self.schema = json.loads(Path("config/forecast-schema.json").read_text())

    def tearDown(self):
        self.temp.cleanup()

    def test_preview_and_completed_resume_do_not_generate_twice(self):
        client = FakeGemini()
        prediction_run("test", root=self.root, client=client)
        self.assertEqual(client.generations, 0)
        output = prediction_run("test", execute=True, root=self.root, client=client)
        self.assertTrue(output["metadata"]["prospective_submission"])
        prediction_run("test", execute=True, root=self.root, client=client)
        self.assertEqual(client.generations, 1)

    def test_budget_refusal_is_before_generation(self):
        client = FakeGemini()
        with self.assertRaises(ValueError):
            prediction_run("test", execute=True, root=self.root, budget="0.01", client=client)
        self.assertEqual(client.generations, 0)

    def test_unknown_references_preserve_raw_and_do_not_retry(self):
        client = FakeGemini(invalid=True)
        with self.assertRaises(ValueError):
            prediction_run("test", execute=True, root=self.root, client=client)
        self.assertTrue((self.root / "predictions/test/response.json").exists())
        with self.assertRaises(ValueError):
            prediction_run("test", execute=True, root=self.root, client=client)
        self.assertEqual(client.generations, 1)

    def test_sampling_and_truncation_are_explicit(self):
        items = [{**self.item, "entity_id": str(i), "observation_id": str(i), "platform": "x" if i % 2 else "web", "text": "A" * 500} for i in range(4)]
        evidence = select_evidence(items, [], limit=2, text_chars=100)
        self.assertEqual({x["platform"] for x in evidence}, {"x", "web"})
        self.assertTrue(all(x["text_truncated"] for x in evidence))

    def test_stale_curves_are_flagged_in_model_input(self):
        item = {**self.item, "extra": {"popularity_curve": [{"value": 1}], "curve_last_point_age_days": 10}}
        self.assertFalse(select_evidence([item], [])[0]["freshness"]["usable_current_week_curve"])

    def test_categorical_and_numeric_consistency(self):
        result = forecast()
        result["forecasts"][0]["outcomes"] = [{"label": "A", "probability": 0.7}, {"label": "B", "probability": 0.7}]
        with self.assertRaises(ValueError):
            validate_forecasts(result, self.schema, [{"evidence_id": "obs-1"}], 5)
        result["forecasts"][0]["outcomes"] = []
        result["forecasts"][0]["estimate"] = {"value": 5, "unit": "views", "lower": 6, "upper": 10, "interval_probability": 0.8}
        with self.assertRaises(ValueError):
            validate_forecasts(result, self.schema, [{"evidence_id": "obs-1"}], 5)

    def test_nonfinite_estimate_is_rejected(self):
        result = forecast()
        result["forecasts"][0]["estimate"] = {"value": float("inf"), "unit": "views", "lower": None, "upper": None, "interval_probability": None}
        with self.assertRaises(ValueError):
            validate_forecasts(result, self.schema, [{"evidence_id": "obs-1"}], 5)

    def test_thought_parts_not_interpreted_as_forecasts(self):
        response = {"candidates": [{"finishReason": "STOP", "content": {"parts": [{"text": "private", "thought": True}, {"text": "answer"}]}}]}
        self.assertEqual(response_text(response), "answer")

    def test_truncated_output_is_not_accepted(self):
        with self.assertRaises(ValueError):
            response_text({"candidates": [{"finishReason": "MAX_TOKENS", "content": {"parts": [{"text": "partial"}]}}]})


if __name__ == "__main__":
    unittest.main()
