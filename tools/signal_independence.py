"""Read-only counterfactual comparison for observed copy-trading buy signals.

Uses Gendan's existing normalized events and relation labels. A shared funder
is an *ambiguous candidate relation*, not proof of common ownership.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
from typing import Any


def utc(text: str) -> datetime:
    t = datetime.fromisoformat(text.replace("Z", "+00:00"))
    if t.tzinfo is None:
        raise ValueError("time must contain a timezone")
    return t.astimezone(timezone.utc)


def as_of_case(case: dict[str, Any], cutoff: str) -> dict[str, Any]:
    """Exclude events not yet observed; never reason about future transfers."""
    t = utc(cutoff)
    snap = deepcopy(case)
    snap["events"] = [e for e in case.get("events", [])
                      if utc(e["event_time"]) <= t and utc(e["observed_time"]) <= t]
    return snap


def compare_report(report: dict[str, Any], cutoff: str, window_minutes: int = 10) -> dict[str, Any]:
    """Compare one-address-one-vote against an explicitly hypothetical merger.

    `report` is Gendan engine.analyze(as_of_case(...)) output. The hypothetical
    source merger is *not* an estimate or lower bound of distinct human owners.
    """
    if window_minutes <= 0:
        raise ValueError("window_minutes must be > 0")
    end = utc(cutoff)
    start = end - timedelta(minutes=window_minutes)
    buys = [e for e in report["events"]
            if e["type"] == "swap_buy" and start <= utc(e["event_time"]) <= end
            and utc(e["observed_time"]) <= end]
    buyers = sorted({e["wallet"] for e in buys})
    buyer_set = set(buyers)

    def pairs(kind: str) -> list[dict[str, Any]]:
        seen = set()
        result = []
        for rel in report.get("relations", []):
            if rel["type"] != kind:
                continue
            a, b = rel["from"], rel["to"]
            if a not in buyer_set or b not in buyer_set or a == b:
                continue
            pair = tuple(sorted((a, b)))
            if pair in seen:
                continue
            seen.add(pair)
            result.append({"wallets": list(pair), "evidence_ids": rel.get("evidence_ids", []),
                           "status": rel.get("status", "UNKNOWN")})
        return sorted(result, key=lambda r: r["wallets"])

    funding = pairs("SHARED_FUNDER_CANDIDATE")
    same_slot = pairs("SAME_SLOT_CANDIDATE")
    parent = {w: w for w in buyers}

    def root(w: str) -> str:
        while parent[w] != w:
            w = parent[w]
        return w

    for rel in funding:
        a, b = rel["wallets"]
        parent[root(a)] = root(b)
    groups: dict[str, list[str]] = {}
    for w in buyers:
        groups.setdefault(root(w), []).append(w)
    proposed = sorted((sorted(g) for g in groups.values()), key=lambda g: g[0])
    return {
        "case_id": report.get("case_id"),
        "data_status": report.get("data_status", "UNKNOWN"),
        "evaluation_cutoff_utc": end.isoformat(),
        "buy_window_start_utc": start.isoformat(),
        "window_minutes": window_minutes,
        "raw_buy_events": len(buys),
        "baseline_distinct_buy_addresses": len(buyers),
        "buy_addresses": buyers,
        "shared_funder_candidate_pairs": funding,
        "same_slot_candidate_pairs": same_slot,
        "counterfactual_if_shared_funder_meant_common_operator": {
            "number_of_groups": len(proposed), "groups": proposed,
            "is_real_owner_estimate": False,
        },
        "verified_distinct_economic_actors": "UNKNOWN",
        "decision": "WATCH_OR_INVESTIGATE; NOT_VERIFIED_INDEPENDENT_CONSENSUS",
        "limits": [
            "A transfer from a common funder may come from a service, exchange or bot.",
            "Same slot is neither proven Jito Bundle nor common-control evidence.",
            "Unlinked addresses are not thereby proven independent.",
            "As-of filtering prevents look-ahead but does not prove historical coverage.",
            "This comparison contains no executable quotes, fee-adjusted PnL, or live trading.",
        ],
    }


def evaluate(case: dict[str, Any], cutoff: str, window_minutes: int = 10) -> dict[str, Any]:
    # Reuse the existing relation engine instead of writing another graph parser.
    from gendan.engine import analyze
    return compare_report(analyze(as_of_case(case, cutoff)), cutoff, window_minutes)


def main() -> None:
    p = argparse.ArgumentParser(description="Read-only copy-signal independence sensitivity check")
    p.add_argument("case", type=Path, help="existing Gendan JSON input (no keys, no transactions)")
    p.add_argument("--at", required=True, help="ISO-8601 cutoff with timezone")
    p.add_argument("--window-minutes", type=int, default=10)
    p.add_argument("--out", type=Path)
    args = p.parse_args()
    value = evaluate(json.loads(args.case.read_text(encoding="utf-8")), args.at, args.window_minutes)
    rendered = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
