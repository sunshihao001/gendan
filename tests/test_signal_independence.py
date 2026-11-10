"""Independent comparator tests plus a real Gendan engine integration contract."""
import copy
import json
from pathlib import Path
import unittest

from tools.signal_independence import as_of_case, compare_report, evaluate

CASE = json.loads((Path(__file__).parents[1] / "data" / "signal_independence_demo.json").read_text(encoding="utf-8"))
AT = "2026-11-09T01:03:00Z"


class SignalIndependenceTests(unittest.TestCase):
    def test_as_of_excludes_future_receiver_sale(self):
        snap = as_of_case(CASE, AT)
        self.assertEqual(len(snap["events"]), 5)
        self.assertEqual(set(e["type"] for e in snap["events"]), {"sol_transfer", "swap_buy"})

    def test_analyze_integration_three_buys_two_candidate_groups(self):
        r = evaluate(CASE, AT)
        self.assertEqual(r["baseline_distinct_buy_addresses"], 3)
        self.assertEqual(r["counterfactual_if_shared_funder_meant_common_operator"]["number_of_groups"], 2)
        self.assertEqual(r["counterfactual_if_shared_funder_meant_common_operator"]["groups"], [["W_A", "W_C"], ["W_D"]])
        self.assertEqual(r["verified_distinct_economic_actors"], "UNKNOWN")
        self.assertEqual(r["same_slot_candidate_pairs"][0]["wallets"], ["W_A", "W_C"])
        self.assertEqual(r["shared_funder_candidate_pairs"][0]["wallets"], ["W_A", "W_C"])

    def test_same_slot_alone_does_not_reduce_scenario_count(self):
        altered = copy.deepcopy(CASE)
        altered["events"] = [e for e in altered["events"] if e["type"] != "sol_transfer"]
        r = evaluate(altered, AT)
        self.assertEqual(r["baseline_distinct_buy_addresses"], 3)
        self.assertEqual(r["counterfactual_if_shared_funder_meant_common_operator"]["number_of_groups"], 3)
        self.assertEqual(len(r["same_slot_candidate_pairs"]), 1)

    def test_late_observation_not_in_past_cutoff(self):
        altered = copy.deepcopy(CASE)
        for ev in altered["events"]:
            if ev["id"] == "s05":
                ev["observed_time"] = "2026-11-09T01:04:00Z"
        r = evaluate(altered, AT)
        self.assertEqual(r["baseline_distinct_buy_addresses"], 2)
        self.assertEqual(r["counterfactual_if_shared_funder_meant_common_operator"]["number_of_groups"], 1)

    def test_copying_same_instruction_does_not_increase_address_count(self):
        altered = copy.deepcopy(CASE)
        duplicate = copy.deepcopy(altered["events"][2])
        duplicate["id"] = "s03_duplicate"
        altered["events"].append(duplicate)
        r = evaluate(altered, AT)
        self.assertEqual(r["baseline_distinct_buy_addresses"], 3)
        self.assertEqual(r["raw_buy_events"], 3)

    def test_no_verified_independence_just_because_no_funder_edge(self):
        altered = copy.deepcopy(CASE)
        altered["events"] = [e for e in altered["events"] if e["type"] != "sol_transfer"]
        r = evaluate(altered, AT)
        self.assertEqual(r["verified_distinct_economic_actors"], "UNKNOWN")

    def test_window_validation(self):
        with self.assertRaises(ValueError):
            compare_report({"events": []}, AT, 0)


if __name__ == "__main__":
    unittest.main()
