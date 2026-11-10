#!/usr/bin/env python3
"""Study-003 method counterexample; synthetic intervals, no market data or trading."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Interval:
    label: str
    mint: str
    start: int
    end: int


def previous_row_filter(positions):
    """Source-equivalent logic: start > previous raw row's end (not max active end)."""
    ordered = sorted(positions, key=lambda p: (p.mint, p.start))
    accepted, previous_by_mint = [], {}
    for p in ordered:
        previous = previous_by_mint.get(p.mint)
        if previous is None or p.start > previous.end:
            accepted.append(p)
        previous_by_mint[p.mint] = p
    return accepted


def no_overlapping_positions(positions):
    """A conservative comparison policy: retain only non-overlapping positions per mint."""
    ordered = sorted(positions, key=lambda p: (p.mint, p.start))
    accepted, last_end_by_mint = [], {}
    for p in ordered:
        end = last_end_by_mint.get(p.mint)
        if end is None or p.start > end:
            accepted.append(p)
            last_end_by_mint[p.mint] = p.end
    return accepted


def follower_return(source_entry, source_exit, follower_entry, follower_exit, fee_pct_each_side):
    """Synthetic unit-price-only return. Ignores market depth and order failures."""
    source = source_exit / source_entry - 1
    follower = follower_exit * (1 - fee_pct_each_side) / (follower_entry * (1 + fee_pct_each_side)) - 1
    return source, follower


def test():
    intervals = [
        Interval("A-long", "Mint-X", 0, 100),
        Interval("B-ignored", "Mint-X", 10, 20),
        Interval("C-wrongly-admitted", "Mint-X", 30, 40),
        Interval("D-independent", "Mint-Y", 30, 40),
    ]
    naive = [p.label for p in previous_row_filter(intervals)]
    strict = [p.label for p in no_overlapping_positions(intervals)]
    assert naive == ["A-long", "C-wrongly-admitted", "D-independent"], naive
    assert strict == ["A-long", "D-independent"], strict
    src, copier = follower_return(1.0, 1.5, 1.4, 1.35, 0.01)
    assert round(src * 100, 2) == 50.0
    assert round(copier * 100, 2) == -5.48
    print("SYNTHETIC_OVERLAP_PREVIOUS_ROW", naive)
    print("SYNTHETIC_OVERLAP_CONSERVATIVE", strict)
    print("SYNTHETIC_SOURCE_RETURN_PCT", round(src * 100, 2))
    print("SYNTHETIC_FOLLOWER_RETURN_PCT", round(copier * 100, 2))
    print("ALL_SYNTHETIC_ASSERTIONS_PASSED")


if __name__ == "__main__":
    test()
