import json
import tempfile
import unittest
from pathlib import Path

from nextday.client import save_json
from nextday.collector import maximum_charge, run_batch, validate_input
from nextday.plans import build_plan, followup_plan


class FakeClient:
    def __init__(self, price="0.01"):
        self.posts = 0
        self.price = price

    def inspect(self, provider, endpoint):
        return {"endpoint_version": 1, "input_schema": {"type": "object", "required": ["q"]},
                "price": {"rule": {"type": "flat", "amount_usd": self.price},
                          "charges": {"NO_RESULT": "0.02", "PROVIDER_ERROR": "0.00"}}}

    def request(self, method, path, body=None, key=None, timeout=None):
        self.posts += method == "POST"
        assert key
        return {"id": "fake-run", "status": "COMPLETED", "charge_usd": "0.01",
                "run_url": "https://example.test/run", "provider_response": {"http_status": 200}, "output": {"items": []}}


class CollectorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = self.temp.name
        self.plan_path = Path(self.root) / "plan.json"
        self.plan = {"jobs": [{"provider": "test", "endpoint": "/test", "input": {"q": "news"}, "source": "news"}]}
        save_json(self.plan_path, self.plan)

    def tearDown(self):
        self.temp.cleanup()

    def test_empty_result_fee_in_reservation(self):
        self.assertEqual(str(maximum_charge(FakeClient().inspect("", ""))), "0.02")

    def test_schema_errors_do_not_dump_provider_tokens(self):
        token = "DO_NOT_LOG_PROVIDER_CURSOR" * 100
        with self.assertRaises(ValueError) as caught:
            validate_input({"cursor": token}, {"type": "object", "properties": {"cursor": {"type": "string", "maxLength": 10}}})
        self.assertNotIn(token, str(caught.exception))

    def test_over_budget_does_not_run(self):
        client = FakeClient()
        with self.assertRaises(ValueError):
            run_batch(self.plan_path, "test", "0.01", True, self.root, client)
        self.assertEqual(client.posts, 0)

    def test_total_approval_covers_multiple_batches(self):
        client = FakeClient()
        save_json(Path(self.root) / "approval.json", {"total_max_usd": "0.03"})
        run_batch(self.plan_path, "one", "0.02", False, self.root, client)
        with self.assertRaises(ValueError):
            run_batch(self.plan_path, "two", "0.02", True, self.root, client)
        self.assertEqual(client.posts, 0)

    def test_preview_is_free_and_resume_is_idempotent(self):
        client = FakeClient()
        run_batch(self.plan_path, "test", "0.02", False, self.root, client)
        self.assertEqual(client.posts, 0)
        run_batch(self.plan_path, "test", "0.02", True, self.root, client)
        run_batch(self.plan_path, "test", "0.02", True, self.root, client)
        self.assertEqual(client.posts, 1)

    def test_changed_input_is_rejected_on_resume(self):
        client = FakeClient()
        run_batch(self.plan_path, "test", "0.02", False, self.root, client)
        self.plan["jobs"][0]["input"]["q"] = "changed"
        save_json(self.plan_path, self.plan)
        with self.assertRaises(ValueError):
            run_batch(self.plan_path, "test", "0.02", True, self.root, client)

    def test_frozen_plan_deduplicates_unfiltered_x_search(self):
        plan = build_plan()
        identities = [(j["provider"], j["endpoint"], json.dumps(j["input"], sort_keys=True)) for j in plan["jobs"]]
        self.assertEqual(len(identities), len(set(identities)))
        self.assertTrue(all(j["region"] == "not_filtered" for j in plan["jobs"] if j["source"] == "x_search"))

    def test_refresh_preserves_unavailable_cohort_members(self):
        spec = {"source": "x_detail", "provider": "tikhub", "endpoint": "/tweet", "input": {"tweet_id": "deleted"}, "region": "unknown", "language": "en"}
        save_json(Path(self.root) / "batches/details/manifest.json", {"jobs": [{"spec": spec, "status": "FAILED"}]})
        plan = followup_plan(self.root, limit=1, refresh=True)
        self.assertEqual(plan["jobs"][0]["input"]["tweet_id"], "deleted")


    def test_vertical_sources_zillow_airbnb_linkedin_in_plan(self):
        plan = build_plan(verticals=["zillow", "airbnb", "linkedin"])
        sources = {j["source"] for j in plan["jobs"]}
        self.assertIn("zillow_mortgage_rates", sources)
        self.assertIn("zillow_property", sources)
        self.assertIn("airbnb_search", sources)
        self.assertIn("linkedin_jobs", sources)
        self.assertIn("linkedin_company", sources)
        self.assertIn("linkedin_posts", sources)


if __name__ == "__main__":
    unittest.main()
