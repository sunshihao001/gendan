import copy
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from gendan.engine import analyze, render_html, write_outputs

CASE = json.loads((Path(__file__).parents[1] / "data" / "demo_case.json").read_text(encoding="utf-8"))


class GendanOfflineContractTests(unittest.TestCase):
    def test_end_to_end_receiver_seller_is_candidate_only(self):
        result = analyze(CASE)
        r = [x for x in result["roles"] if x["wallet"] == "W_B" and x["code"] == "receiver_seller_candidate"]
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0]["status"], "INFERRED")
        self.assertEqual(set(r[0]["evidence_ids"]), {"e05", "e06"})
        self.assertIn("不能证明", r[0]["caveat"])

    def test_transfer_only_does_not_imply_sale(self):
        result = analyze(CASE)
        self.assertNotIn(("W_Z", "receiver_seller_candidate"), {(r["wallet"], r["code"]) for r in result["roles"]})

    def test_same_slot_not_jito_bundle(self):
        r = analyze(CASE)
        pairs = [e for e in r["relations"] if e["type"] == "SAME_SLOT_CANDIDATE"]
        self.assertEqual(len(pairs), 1)
        self.assertIn("不代表真实 Jito Bundle", pairs[0]["caveat"])
        self.assertFalse(any("JITO_CONFIRMED" in x["type"] for x in r["relations"]))

    def test_shared_funder_not_common_owner(self):
        r = analyze(CASE)
        shared = [x for x in r["relations"] if x["type"] == "SHARED_FUNDER_CANDIDATE"]
        self.assertEqual(len(shared), 1)
        self.assertIn("不证明共同控制", shared[0]["caveat"])

    def test_duplicate_same_instruction_skipped(self):
        case = copy.deepcopy(CASE)
        repeated = copy.deepcopy(case["events"][0])
        repeated["id"] = "e01_repeat"
        case["events"].append(repeated)
        result = analyze(case)
        self.assertEqual(len(result["events"]), len(CASE["events"]))
        self.assertIn("DUPLICATE_NORMALIZED_EVENT_SKIPPED: e01_repeat", result["warnings"])

    def test_same_signature_different_instructions_preserved(self):
        case = copy.deepcopy(CASE)
        repeated = copy.deepcopy(case["events"][0])
        repeated["id"] = "e01_other_instruction"
        repeated["instruction_index"] = 1
        case["events"].append(repeated)
        result = analyze(case)
        self.assertEqual(len(result["events"]), len(CASE["events"]) + 1)

    def test_other_mint_rejected(self):
        case = copy.deepcopy(CASE)
        case["events"][0]["mint"] = "WRONG_MINT"
        with self.assertRaisesRegex(ValueError, "mint"):
            analyze(case)

    def test_preexisting_sell_not_linked(self):
        case = copy.deepcopy(CASE)
        for e in case["events"]:
            if e["id"] == "e06":
                e["event_time"] = "2026-11-09T01:03:00Z"
                e["observed_time"] = "2026-11-09T01:03:09Z"
        r = analyze(case)
        self.assertFalse(any(x["code"] == "receiver_seller_candidate" for x in r["roles"]))

    def test_copyability_unknown_and_missing_coverage(self):
        r = analyze(CASE)
        self.assertEqual(r["copyability"]["verdict"], "COPYABILITY_UNKNOWN")
        self.assertFalse(r["copyability"]["verified_positive_edge"])
        self.assertTrue(any("quotes_and_fees_complete" in x for x in r["warnings"]))

    def test_negative_amount_rejected(self):
        case = copy.deepcopy(CASE)
        case["events"][0]["amount"] = "-1"
        with self.assertRaisesRegex(ValueError, "nonnegative"):
            analyze(case)

    def test_render_outputs(self):
        report = analyze(CASE)
        html = render_html(report)
        self.assertIn("DEMO-001-SYNTHETIC", html)
        self.assertIn("钱包关系调查图谱", html)
        self.assertIn("COPYABILITY_UNKNOWN", html)
        with TemporaryDirectory() as td:
            j, h = write_outputs(report, td)
            self.assertTrue(j.is_file() and h.is_file())
            self.assertEqual(json.loads(j.read_text(encoding="utf-8"))["case_id"], CASE["case_id"])

    def test_no_network_or_order_api(self):
        # Behavior test: engine succeeds with only a local dict, no keys/network configuration.
        self.assertEqual(analyze(CASE)["data_status"], "SYNTHETIC_FIXTURE_ONLY")


if __name__ == "__main__":
    unittest.main()
