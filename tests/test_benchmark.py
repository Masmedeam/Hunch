import json
import tempfile
import unittest
from pathlib import Path

from nextday.benchmark import (CIKS, audit_public_history, between, build_dataset, clean_case_records, compatible_continuations,
    freeze_protocol, generate_case, load_public_case, make_plan, parse_snapshots, source_completeness)
from nextday.client import save_json


def envelope(source, output, ident="run", **metadata):
    return {"captured_at": "2026-10-25T18:00:00Z", "spec": {"source": source, "input": {}, **metadata},
            "run": {"id": ident, "status": "COMPLETED", "provider": "test", "endpoint": "/test", "output": output,
                    "provider_response": {"http_status": 200}, "charge_usd": "0.001", "run_url": "https://example.test/private-run"}}


class BenchmarkTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.protocol = freeze_protocol(self.root)

    def tearDown(self):
        self.temp.cleanup()

    def records(self):
        prices = envelope("benchmark_prices", {"prices": [
            {"time": "2026-10-14", "open": 9, "high": 11, "low": 8, "close": 10, "volume": 100},
            {"time": "2026-10-15", "open": 10, "high": 13, "low": 9, "close": 12, "volume": 200}]}, "prices", input={"ticker": "AAPL"})
        posts = envelope("benchmark_x", {"data": {"timeline": [
            {"tweet_id": "1", "screen_name": "NASA", "text": "Historical launch plan", "created_at": "Wed Oct 14 15:00:00 +0000 2026", "views": 777777777},
            {"tweet_id": "2", "screen_name": "NASA", "text": "FUTURE_SECRET_EVENT_MARKER", "created_at": "Thu Oct 15 15:00:00 +0000 2026", "views": 777777777}]}}, "posts", account="NASA", day="2026-10-14", page=1, boundary_buffer_days=1)
        return parse_snapshots([prices, posts])[0], [prices, posts]

    def test_next_day_and_current_engagement_are_hidden(self):
        records, snapshots = self.records()
        complete = source_completeness(snapshots, self.protocol)
        history, questions, hidden, _ = generate_case(self.protocol, records, complete, "2026-10-14", 0)
        audit_public_history(history, hidden)
        text = json.dumps(history)
        self.assertNotIn("FUTURE_SECRET_EVENT_MARKER", text)
        self.assertNotIn("777777777", text)
        self.assertNotIn('"close": "12"', text)
        self.assertIn("FUTURE_SECRET_EVENT_MARKER", json.dumps(hidden))
        self.assertTrue(hidden["resolutions"][0]["value"])
        self.assertEqual(len(questions["questions"]), 5)

    def test_utc_bounds_not_query_dates_control_history(self):
        record = {"event_at": "2026-10-15T01:00:00Z"}
        self.assertFalse(between(record, "2026-10-14T00:00:00Z", "2026-10-15T00:00:00Z"))

    def test_question_selection_does_not_depend_on_hidden_outcome(self):
        records, snapshots = self.records()
        complete = source_completeness(snapshots, self.protocol)
        original = generate_case(self.protocol, records, complete, "2026-10-14", 0)[1]
        changed = [dict(r, close="1") if r["kind"] == "price_bar" and r["trading_date"] == "2026-10-15" else r for r in records]
        alternate = generate_case(self.protocol, changed, complete, "2026-10-14", 0)[1]
        self.assertEqual(original, alternate)

    def test_article_future_update_is_excluded_but_schedule_is_retained(self):
        base = {"kind": "article", "event_at": "2026-10-14T12:00:00Z", "retrieved_at": "2026-10-25T12:00:00Z", "title": "Report", "integrity": "reconstructed"}
        records = [{**base, "source_id": "bad", "url": "https://example.com/bad", "text": "Result", "explicit_modified_at": {"modifiedDate": "2026-10-15T12:00:00Z"}},
                   {**base, "source_id": "good", "url": "https://example.com/good", "text": "An event is planned for October 15, 2026."}]
        selected, excluded = clean_case_records(records, "2026-10-08T00:00:00Z", "2026-10-15T00:00:00Z")
        self.assertEqual([x["source_id"] for x in selected], ["good"])
        self.assertEqual(excluded["explicit_post_cutoff_update"], 1)

    def test_incomplete_registry_is_not_zero(self):
        e = envelope("benchmark_filings", {"data": [], "total": {"value": 100, "relation": "eq"}}, day="2026-10-14")
        complete = source_completeness([e], self.protocol)
        self.assertFalse(complete["filing_logs"]["2026-10-14"]["complete"])

    def test_original_company_event_uses_verified_cik_not_accession_prefix(self):
        rows = [{"filedAt": "2026-10-15T08:00:00-04:00", "formType": "8-K", "cik": "320193", "accessionNo": "0001628280-26-123456"}]
        search = envelope("benchmark_company_filings", {"filings": rows, "total": {"value": 1, "relation": "eq"}}, "search", input={"query": "cohort", "from": 0, "size": 50}, page=1)
        mappings = [envelope("benchmark_company", {"company_facts": {"cik": cik}}, ticker, input={"ticker": ticker}) for ticker, cik in CIKS.items()]
        snapshots = [search]+mappings
        records = parse_snapshots(snapshots)[0]
        history, questions, hidden, _ = generate_case(self.protocol, records, source_completeness(snapshots, self.protocol), "2026-10-14", 0)
        self.assertTrue(hidden["resolutions"][1]["value"])
        self.assertEqual(records[0]["cik"], "320193")

    def test_public_loader_never_reads_hidden_answers(self):
        folder = self.root / "public_inputs/day-2026-10-14"
        save_json(folder / "history.json", {"case_id": "day-2026-10-14"})
        save_json(folder / "questions.json", {"questions": []})
        private = self.root / "private_outcomes/day-2026-10-14/resolution.json"
        private.parent.mkdir(parents=True)
        private.write_text("NOT VALID JSON; loader must never read this")
        result = load_public_case("day-2026-10-14", self.root)
        self.assertEqual(result["history"]["case_id"], "day-2026-10-14")
        with self.assertRaises(ValueError):
            load_public_case("../../private_outcomes", self.root)

    def test_protocol_dates_and_templates_are_frozen(self):
        original = self.protocol["frozen_at"]
        self.assertEqual(freeze_protocol(self.root)["frozen_at"], original)
        self.assertEqual(len(make_plan("news", self.root)["jobs"]), 100)
        self.assertEqual(json.loads((self.root / "private_raw/approval.json").read_text())["total_max_usd"], "10.00")

    def test_oversized_provider_cursor_is_quarantined_not_truncated(self):
        token = "opaque" * 1000
        original = {"jobs": [{"source": "benchmark_youtube", "account": "BBCNews", "input": {"continuationToken": token}},
                             {"source": "benchmark_tiktok", "account": "bbcnews", "input": {"max_cursor": "123"}}]}
        safe = compatible_continuations(original)
        self.assertEqual(len(safe["jobs"]), 1)
        self.assertEqual(len(safe["blocked_continuations"]), 1)
        self.assertEqual(original["jobs"][0]["input"]["continuationToken"], token)
        self.assertNotIn(token, json.dumps(safe))

    def test_audit_rejects_leaked_fields_and_boundary_record(self):
        history = {"history_start": "2026-10-08T00:00:00Z", "cutoff_exclusive": "2026-10-15T00:00:00Z", "evidence": [
            {"event_at": "2026-10-14T12:00:00Z", "source_id": "a", "views": 100}], "filing_counts": [], "publication_counts": []}
        with self.assertRaises(ValueError):
            audit_public_history(history, {"reference_evidence": []})
        history["evidence"][0].pop("views")
        history["evidence"][0]["event_at"] = history["cutoff_exclusive"]
        with self.assertRaises(ValueError):
            audit_public_history(history, {"reference_evidence": []})


if __name__ == "__main__":
    unittest.main()
