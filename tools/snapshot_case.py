"""Read-only Gendan pool/holder evidence checker.

Reads a local JSON file only. Does not connect to Solana, sign, trade, or infer
private owners. Values in an archived case can be transcribed, not raw RPC.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from html import escape
import json
from pathlib import Path


def num(value: object, name: str) -> Decimal:
    try:
        val = Decimal(str(value))
    except (TypeError, InvalidOperation):
        raise ValueError(f"{name}: invalid numeric value") from None
    if not val.is_finite() or val < 0:
        raise ValueError(f"{name}: must be finite and nonnegative")
    return val


def utc(value: object) -> datetime:
    if not isinstance(value, str):
        raise ValueError("observed_at_utc must be a string")
    try:
        t = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as err:
        raise ValueError(f"invalid observation time: {value}") from err
    if t.tzinfo is None:
        raise ValueError("observation time must have explicit UTC offset")
    return t.astimezone(timezone.utc)


def pct_change(a: Decimal, b: Decimal) -> str | None:
    if a == 0:
        return None
    return str((b - a) / a * 100).split("E")[0]


def inspect(snapshot: dict) -> dict:
    """Analyze source-transcribed market snapshots without inventing swaps."""
    case_id = snapshot.get("case_id")
    mint = snapshot.get("mint")
    source_url = snapshot.get("source_url")
    if not all(isinstance(x, str) and x for x in (case_id, mint, source_url)):
        raise ValueError("case_id, mint, source_url required")
    if not source_url.startswith("https://github.com/"):
        raise ValueError("source_url must be an explicit GitHub provenance link")
    kind = snapshot.get("evidence_kind")
    if kind not in {"TRANSCRIBED_VENDOR_REPORT", "RAW_VENDOR_SNAPSHOT"}:
        raise ValueError("evidence_kind must declare raw or transcribed vendor evidence")
    pools = snapshot.get("pools", [])
    holders = snapshot.get("holder_observations", [])
    if not pools or not isinstance(pools, list) or not isinstance(holders, list):
        raise ValueError("pools list required; holder_observations must be a list")
    indexed = {}
    pool_results = []
    warnings = []
    for pool in pools:
        address = pool.get("address")
        if not isinstance(address, str) or not address or address in indexed:
            raise ValueError("pool address missing or duplicated")
        indexed[address] = pool
        observations = pool.get("observations", [])
        if not observations:
            raise ValueError(f"pool {address}: no observations")
        times = set()
        parsed = []
        for observation in observations:
            tm = utc(observation.get("observed_at_utc"))
            if tm in times:
                raise ValueError(f"pool {address}: duplicate observation time")
            times.add(tm)
            row = {"observed_at_utc": tm.isoformat(), "price_usd": str(num(observation.get("price_usd"), "price_usd")),
                   "liquidity_usd": str(num(observation.get("liquidity_usd"), "liquidity_usd")),
                   "reserve_token": str(num(observation.get("reserve_token"), "reserve_token")),
                   "reserve_sol": str(num(observation.get("reserve_sol"), "reserve_sol"))}
            parsed.append((tm, row))
        parsed.sort(key=lambda x: x[0])
        changes = []
        for (_, before), (_, after) in zip(parsed, parsed[1:]):
            changes.append({"from": before["observed_at_utc"], "to": after["observed_at_utc"],
                            "price_change_pct": pct_change(Decimal(before["price_usd"]), Decimal(after["price_usd"])),
                            "token_reserve_change": str(Decimal(after["reserve_token"]) - Decimal(before["reserve_token"])),
                            "sol_reserve_change": str(Decimal(after["reserve_sol"]) - Decimal(before["reserve_sol"])),
                            "liquidity_change_pct": pct_change(Decimal(before["liquidity_usd"]), Decimal(after["liquidity_usd"]))})
        pool_results.append({"address": address, "venue": pool.get("venue", "UNKNOWN"),
                             "observations": [row for _, row in parsed], "changes": changes,
                             "decision": "WATCH_POOL_ONLY", "economic_direction": "UNKNOWN_SWAP_VS_LP_VS_FEES"})
    candidates = []
    for h in holders:
        owner = h.get("owner")
        account = h.get("token_account")
        tm = utc(h.get("observed_at_utc"))
        if not isinstance(owner, str) or not owner or not isinstance(account, str) or not account:
            raise ValueError("holder must provide owner and token_account")
        if h.get("mint") and h["mint"] != mint:
            raise ValueError("holder mint mismatch")
        supply_pct = num(h.get("reported_supply_pct"), "reported_supply_pct")
        if supply_pct > 100:
            raise ValueError("reported_supply_pct exceeds 100")
        pool_match = owner in indexed
        candidates.append({"observed_at_utc": tm.isoformat(), "token_account": account, "owner": owner,
                           "reported_supply_pct": str(supply_pct),
                           "owner_matches_pool": pool_match,
                           "source_label": h.get("source_label", ""),
                           "candidate_role": "POOL_INFRASTRUCTURE_CANDIDATE" if pool_match else "OWNER_ROLE_UNVERIFIED",
                           "copytrading_decision": "SKIP_AS_INDEPENDENT_WALLET" if pool_match else "UNKNOWN",
                           "evidence_level": "VENDOR_CROSS_FIELD_MATCH" if pool_match else "VENDOR_ONLY"})
    warnings.append("Provider snapshots cannot establish swap-vs-LP cause or an executable trade price")
    warnings.append("Source transcription, when used, is not a fresh raw provider response")
    warnings.append("No wallet swap signatures or observer-first-seen signal; paper PnL cannot be computed")
    return {"case_id": case_id, "mint": mint, "source_url": source_url,
            "evidence_kind": kind, "data_status": "ARCHIVED_VENDOR_EVIDENCE_NOT_ONCHAIN_REPLAY",
            "pool_results": pool_results, "holder_candidates": candidates,
            "copyability": "NOT_TESTABLE_WITH_SNAPSHOT_ONLY", "warnings": warnings,
            "metrics": {"pools": len(pool_results), "holder_observations": len(candidates),
                        "pool_matched_holders": sum(int(x["owner_matches_pool"]) for x in candidates)}}


def render(report: dict) -> str:
    e = lambda x: escape(str(x), quote=True)
    pool_rows = "".join(f'<tr><td><code>{e(p["address"])}</code></td><td>{e(p["venue"])}</td><td>{len(p["observations"])}</td><td>{e(p["decision"])}</td></tr>' for p in report["pool_results"])
    holder_rows = "".join(f'<tr><td><code>{e(h["token_account"])}</code></td><td><code>{e(h["owner"])}</code></td><td>{e(h["reported_supply_pct"])}%</td><td>{e(h["candidate_role"])}</td><td><strong>{e(h["copytrading_decision"])}</strong></td></tr>' for h in report["holder_candidates"])
    change_rows = "".join(f'<tr><td><code>{e(p["address"][:12])}</code></td><td>{e(c["from"])}</td><td>{e(c["to"])}</td><td>{e(c["price_change_pct"])}%</td><td>{e(c["token_reserve_change"])}</td><td>{e(c["sol_reserve_change"])}</td></tr>' for p in report["pool_results"] for c in p["changes"])
    warning_rows = "".join(f'<li>{e(w)}</li>' for w in report["warnings"])
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Gendan | {e(report["case_id"])}</title><style>body{{font:15px/1.6 system-ui;background:#0e1728;color:#e6edf7;margin:0}}main{{max-width:1150px;margin:auto;padding:30px}}table{{width:100%;border-collapse:collapse;display:block;overflow:auto}}th,td{{padding:10px;border-bottom:1px solid #3b4b66;text-align:left}}th{{color:#c5d5ee;background:#1f304b}}section{{margin:22px 0;background:#17233b;padding:18px;border-radius:12px}}code{{font-size:12px;overflow-wrap:anywhere}}a{{color:#98c3ff}}.sub{{color:#acbad4}}</style></head><body><main><h1>Gendan｜真实来源池与Holder筛查</h1><p class="sub">案例 {e(report["case_id"])} · Mint: <code>{e(report["mint"])}</code></p><p><strong>数据等级：</strong>{e(report["data_status"])} · <strong>跟随可验收：</strong>{e(report["copyability"])}</p><p><a href="{e(report["source_url"])}">核对原始研究来源</a></p><section><h2>池与观察</h2><table><tr><th>池地址</th><th>市场</th><th>快照数</th><th>操作判断</th></tr>{pool_rows}</table></section><section><h2>可疑私人鲸鱼：基础设施剔除</h2><table><tr><th>Token Account</th><th>Owner</th><th>占比</th><th>角色候选</th><th>跟单筛选结果</th></tr>{holder_rows}</table></section><section><h2>真实供应商跨时点变化（不等于买卖方向）</h2><table><tr><th>池</th><th>从</th><th>到</th><th>价格变化</th><th>Token储备变化</th><th>SOL储备变化</th></tr>{change_rows}</table></section><section><h2>证据边界与后续核查</h2><ul>{warning_rows}</ul></section></main></body></html>'''


def main() -> None:
    parser = argparse.ArgumentParser(description="Gendan vendor snapshot + holder read-only checker")
    parser.add_argument("input", type=Path, help="source-provenanced local JSON file")
    parser.add_argument("--out", type=Path, default=Path("output"))
    args = parser.parse_args()
    report = inspect(json.loads(args.input.read_text(encoding="utf-8")))
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "case_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.out / "case_report.html").write_text(render(report), encoding="utf-8")
    print(f"Case={report['case_id']} pools={report['metrics']['pools']} holder_obs={report['metrics']['holder_observations']} pool_matches={report['metrics']['pool_matched_holders']}")
    print(f"Copyability={report['copyability']}; output={args.out.resolve()}")


if __name__ == "__main__":
    main()
