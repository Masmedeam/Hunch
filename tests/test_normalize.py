import unittest
import tempfile
from pathlib import Path
from nextday.client import save_json
from nextday.normalize import canonical_url, growth, metric, normalize_envelope, rebuild, timestamp, youtube_metrics


def envelope(source, output):
    return {"captured_at": "2026-10-25T12:00:00Z", "spec": {"source": source, "region": "US", "language": "en", "input": {}},
            "run": {"id": "test", "status": "COMPLETED", "provider": "test", "endpoint": "/test", "endpoint_version": 1, "output": output}}


class NormalizeTests(unittest.TestCase):
    def test_missing_counts_are_not_zero(self):
        self.assertIsNone(metric(None, "views"))
        self.assertIsNone(metric("1.2M", "views"))
        self.assertEqual(metric(0, "views")["value"], 0)
        self.assertIsNone(metric(-1, "views"))

    def test_youtube_rounded_integer_is_not_exact_growth(self):
        counts = youtube_metrics({"commentCountInt": 31000, "commentCountText": "31K"})
        self.assertEqual(counts["comments"]["precision"], "rounded_display")

    def test_jsonl_unicode_separator_does_not_split_captions(self):
        from nextday.plans import followup_plan
        with tempfile.TemporaryDirectory() as root:
            e = envelope("tiktok_trends", {"aweme_list": [{"aweme_id": "1", "url": "https://www.tiktok.com/@u/video/1", "desc": "first\u2028second"}]})
            save_json(Path(root) / "batches/test/raw/one.json", e)
            rebuild(root)
            plan = followup_plan(root, limit=1)
            self.assertTrue(any(x["source"] == "tiktok_detail" for x in plan["jobs"]))

    def test_relative_and_day_precision(self):
        parsed, precision = timestamp("2 hours ago", "2026-10-25T12:00:00Z")
        self.assertEqual(parsed, "2026-10-25T10:00:00Z")
        self.assertEqual(precision, "relative_estimate")
        self.assertEqual(timestamp("2026-10-25", "")[1], "day")
        self.assertEqual(timestamp("Sep 4, 2025", "")[1], "day")
        self.assertEqual(timestamp("1792929600", "")[1], "machine_timestamp")

    def test_canonical_url_preserves_meaningful_query(self):
        self.assertEqual(canonical_url("https://example.com/article?id=1&utm_source=x#fragment"), "https://example.com/article?id=1")

    def test_tiktok_current_counter_and_raw_provenance(self):
        e = envelope("tiktok_trends", {"aweme_list": [{"aweme_id": "123", "desc": "#news", "statistics": {"play_count": 100, "comment_count": 0}, "create_time": 1792929600}]})
        rows = normalize_envelope(e, "raw.json")
        self.assertEqual(rows[0]["metrics"]["views"]["semantics"], "cumulative_snapshot")
        self.assertEqual(rows[0]["metrics"]["comments"]["value"], 0)
        self.assertEqual(rows[0]["native_path"], "/aweme_list/0")
        self.assertEqual(rows[0]["raw_file"], "raw.json")

    def test_x_no_volume_is_not_fabricated(self):
        row = normalize_envelope(envelope("x_trends", {"data": {"trends": [{"name": "News", "context": "Trending"}]}}))[0]
        self.assertEqual(row["metrics"], {})
        self.assertEqual(row["rank"], 1)

    def test_x_detail_normalizes_distinct_like_field(self):
        row = normalize_envelope(envelope("x_detail", {"data": {"id": "1", "text": "news", "likes": 5, "replies": 2, "author": {"screen_name": "author"}}}))[0]
        self.assertEqual(row["metrics"]["likes"]["value"], 5)
        self.assertEqual(row["metrics"]["comments"]["value"], 2)
        self.assertEqual(row["author"]["handle"], "author")

    def test_hashtag_detail_preserves_stale_curve_dates(self):
        e = envelope("tiktok_hashtag_detail", {"data": {"hashtagID": "1", "hashtagName": "news", "popularityCurve": [{"timestamp": "1791504000", "value": 100}]}})
        row = normalize_envelope(e)[0]
        self.assertGreater(row["extra"]["curve_last_point_age_days"], 7)

    def test_country_rankings_have_separate_entity_scope(self):
        e = envelope("x_trends", {"data": {"trends": [{"name": "News"}]}})
        a = normalize_envelope(e)[0]
        e["spec"]["region"] = "JP"
        b = normalize_envelope(e)[0]
        self.assertNotEqual(a["entity_id"], b["entity_id"])

    def test_growth_preserves_decreases(self):
        common = {"entity_id": "x:1", "provider": "p", "endpoint": "/a", "observation_id": "1"}
        a = {**common, "captured_at": "2026-10-25T10:00:00Z", "metrics": {"views": metric(100, "views")}}
        b = {**common, "captured_at": "2026-10-25T12:00:00Z", "metrics": {"views": metric(90, "views")}}
        change = growth([a, b])[0]
        self.assertEqual(change["delta"], -10)
        self.assertTrue(change["counter_decreased"])
        self.assertEqual(growth([a]), [])

    def test_hashtag_aggregate_not_used_as_cumulative_growth(self):
        e = envelope("tiktok_hashtags", {"data": {"items": [{"hashtagID": "1", "hashtagName": "news", "vv": 50, "publishCnt": 3}]}})
        rows = normalize_envelope(e)
        self.assertEqual(growth(rows), [])

    def test_cutoff_excludes_later_fractional_seconds_and_old_news(self):
        with tempfile.TemporaryDirectory() as root:
            e = envelope("news", {"news": [{"title": "Old", "link": "https://example.com/old", "date": "Sep 4, 2025"}]})
            e["captured_at"] = "2026-10-25T12:00:00.100000Z"
            save_json(Path(root) / "batches/test/raw/one.json", e)
            report = rebuild(root, "2026-10-25T12:00:00Z")
            self.assertEqual(report["observations"], 0)
            report = rebuild(root)
            self.assertEqual(report["observations"], 1)
            self.assertEqual(report["context_entities"], 0)
            report = rebuild(root, since="2026-10-25T12:00:01Z")
            self.assertEqual(report["observations"], 0)


    def test_zillow_airbnb_linkedin_normalization(self):
        z = normalize_envelope(envelope("zillow_property", {"results": [{"zpid": "29437674", "address": "100 Main St", "price": 750000, "zestimate": 765000, "url": "https://www.zillow.com/homedetails/29437674_zpid/"}]}))[0]
        self.assertEqual(z["platform"], "zillow")
        self.assertEqual(z["metrics"]["price"]["value"], 750000)
        a = normalize_envelope(envelope("airbnb_search", {"results": [{"id": "ab-1", "name": "Downtown Loft", "price": 240, "reviewsCount": 48, "url": "https://www.airbnb.com/rooms/1"}]}))[0]
        self.assertEqual(a["platform"], "airbnb")
        self.assertEqual(a["metrics"]["nightly_price"]["value"], 240)
        l = normalize_envelope(envelope("linkedin_jobs", {"jobs": [{"jobId": "li-99", "title": "AI Engineer", "companyName": "Acme AI", "applicantsCount": 84, "url": "https://www.linkedin.com/jobs/view/99"}]}))[0]
        self.assertEqual(l["platform"], "linkedin")
        self.assertEqual(l["kind"], "job")
        self.assertEqual(l["metrics"]["applicants"]["value"], 84)


if __name__ == "__main__":
    unittest.main()
