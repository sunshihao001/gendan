"""All tests run offline. No network, credentials, trade or RPC calls."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).parents[1]))
from tools.snapshot_case import inspect, render

SOURCE = Path(__file__).parents[1] / "data/blix_archived_mint_vendor_summary.json"


class SnapshotCaseTests(unittest.TestCase):
    def setUp(self):
        self.case = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_archived_real_provider_transcription_pool_exclusion(self):
        r = inspect(self.case)
        self.assertEqual(r["metrics"]["pool_matched_holders"], 2)
        self.assertEqual(r["holder_candidates"][0]["candidate_role"], "POOL_INFRASTRUCTURE_CANDIDATE")
        self.assertEqual(r["holder_candidates"][0]["copytrading_decision"], "SKIP_AS_INDEPENDENT_WALLET")
        self.assertEqual(r["copyability"], "NOT_TESTABLE_WITH_SNAPSHOT_ONLY")
        self.assertEqual(r["data_status"], "ARCHIVED_VENDOR_EVIDENCE_NOT_ONCHAIN_REPLAY")

    def test_actual_provider_price_and_inventory_changes(self):
        changes = inspect(self.case)["pool_results"][0]["changes"]
        self.assertEqual(changes[0]["token_reserve_change"], "1443150")
        self.assertEqual(changes[0]["sol_reserve_change"], "-8.0596")
        self.assertEqual(changes[1]["token_reserve_change"], "-400272")
        self.assertEqual(changes[1]["sol_reserve_change"], "3.66125")
        self.assertTrue(changes[0]["price_change_pct"].startswith("-6.07"))

    def test_unverified_owner_does_not_get_positive_label(self):
        c = deepcopy(self.case)
        c["holder_observations"][0]["owner"] = "OTHER_WALLET"
        h = inspect(c)["holder_candidates"][0]
        self.assertEqual(h["copytrading_decision"], "UNKNOWN")
        self.assertEqual(h["candidate_role"], "OWNER_ROLE_UNVERIFIED")

    def test_invalid_supply_and_mint_fail_closed(self):
        c = deepcopy(self.case)
        c["holder_observations"][0]["reported_supply_pct"] = 101
        with self.assertRaisesRegex(ValueError, "exceeds"):
            inspect(c)
        c = deepcopy(self.case)
        c["holder_observations"][0]["mint"] = "OTHER_MINT"
        with self.assertRaisesRegex(ValueError, "mint mismatch"):
            inspect(c)

    def test_bad_time_duplicate_or_negative_values_fail_closed(self):
        c = deepcopy(self.case)
        c["pools"][0]["observations"][1]["observed_at_utc"] = "2026-11-01T02:44:23.396Z"
        with self.assertRaisesRegex(ValueError, "duplicate observation"):
            inspect(c)
        c = deepcopy(self.case)
        c["pools"][0]["observations"][1]["reserve_sol"] = "-1"
        with self.assertRaisesRegex(ValueError, "nonnegative"):
            inspect(c)

    def test_html_is_escaped(self):
        c = deepcopy(self.case)
        c["holder_observations"][0]["source_label"] = '<script>alert("hi")</script>'
        s = render(inspect(c))
        self.assertNotIn("<script>", s)
        self.assertIn("SKIP_AS_INDEPENDENT_WALLET", s)


if __name__ == "__main__":
    unittest.main()
