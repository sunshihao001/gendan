"""Offline, read-only Solana wallet-event research.

Input is a normalized illustrative event list, NOT a Solana RPC parser.
The word OBSERVED refers only to observations within the supplied dataset.
No network calls, wallet keys, transaction creation, signing, or financial scoring.
"""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from html import escape
from itertools import combinations
import json
import math
from pathlib import Path
from typing import Any

EVENT_TYPES = {"sol_transfer", "token_transfer", "swap_buy", "swap_sell", "promotion_claim"}
DISPLAY = {
    "shared_funder_candidate": "共享资金源候选（非同控证明）",
    "same_slot_candidate": "同槽买入候选（非 Jito Bundle 证明）",
    "receiver_seller_candidate": "接收 Token 后发生卖出事件",
    "new_receiver_candidate": "新接收钱包（观察样本内）",
    "active_trader_candidate": "高频交易者候选（非刷量证明）",
    "funder_observed": "观察到多地址出资",
    "launch_buyer_candidate": "创建槽早期买入候选",
    "promoter_link_claim": "KOL 营销关联声明（未证实）",
}
STATUS = ("OBSERVED", "INFERRED", "HYPOTHESIS", "UNKNOWN")


def _date(value: str) -> datetime:
    if not isinstance(value, str):
        raise ValueError("Event time must be an ISO-8601 string")
    v = value.strip()
    if v.endswith("Z"):
        v = v[:-1] + "+00:00"
    dt = datetime.fromisoformat(v)
    if dt.tzinfo is None:
        raise ValueError("Event time must include a UTC offset")
    return dt.astimezone(timezone.utc)


def _amount(value: Any) -> str:
    try:
        n = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        raise ValueError(f"Invalid amount: {value!r}") from None
    if not n.is_finite() or n < 0:
        raise ValueError("Amount must be a finite nonnegative number")
    return format(n, "f")


def _validate_event(ev: dict, mint: str) -> dict:
    e = dict(ev)
    if not e.get("id") or not e.get("signature"):
        raise ValueError("Every event needs id and signature")
    if e.get("type") not in EVENT_TYPES:
        raise ValueError(f"Unknown event type {e.get('type')}")
    if not isinstance(e.get("instruction_index"), int) or e["instruction_index"] < 0:
        raise ValueError("instruction_index must be a nonnegative integer")
    e["event_time"] = _date(e["event_time"]).isoformat()
    e["observed_time"] = _date(e["observed_time"]).isoformat()
    if _date(e["observed_time"]) < _date(e["event_time"]):
        raise ValueError("observed_time must not be earlier than event_time")
    if e.get("mint") and e["mint"] != mint:
        # The V0.1 single-mint adapter must never silently mix data for another Mint.
        raise ValueError("Event mint differs from this case Mint")
    if e["type"] in ("sol_transfer", "token_transfer"):
        if not e.get("from") or not e.get("to"):
            raise ValueError("Transfers require from and to")
        e["asset"] = e.get("asset") or ("SOL" if e["type"] == "sol_transfer" else mint)
        e["amount"] = _amount(e["amount"])
    elif e["type"] in ("swap_buy", "swap_sell"):
        if not e.get("wallet"):
            raise ValueError("Swaps require wallet")
        e["amount"] = _amount(e["amount"])
        e["asset"] = e.get("asset", mint)
        e["venue"] = e.get("venue") or "DEX_UNKNOWN"
    else:
        if not e.get("source_name") or not e.get("promoter"):
            raise ValueError("Marketing claims require source_name and promoter")
    e["mint"] = mint
    e["source"] = e.get("source", "UNSPECIFIED")
    return e


def analyze(case: dict) -> dict:
    """Derive narrowly stated wallet *candidates* from normalized demo/owned data."""
    mint = case.get("mint")
    if not mint or not case.get("case_id"):
        raise ValueError("Input requires case_id and mint")
    warnings: list[str] = []
    ids: set[str] = set()
    seen: set[tuple] = set()
    events: list[dict] = []
    for raw in case.get("events", []):
        e = _validate_event(raw, mint)
        if e["id"] in ids:
            raise ValueError("Event id duplicated: " + e["id"])
        ids.add(e["id"])
        # Deduplicate same normalized instruction, but keep distinct instructions in one signature.
        key = (e["signature"], e["instruction_index"], e["type"], e.get("from"),
               e.get("to"), e.get("wallet"), e.get("asset"), e.get("amount"))
        if key in seen:
            warnings.append(f"DUPLICATE_NORMALIZED_EVENT_SKIPPED: {e['id']}")
            continue
        seen.add(key)
        events.append(e)
    events.sort(key=lambda e: (e["event_time"], e["signature"], e["instruction_index"], e["id"]))

    nodes: dict[str, dict] = {}
    for w in case.get("wallets", []):
        nodes[w["id"]] = {"id": w["id"], "kind": "wallet", "name": w.get("name", w["id"])}
    roles: list[dict] = []
    relations: list[dict] = []
    signatures_by_wallet: dict[str, set[str]] = defaultdict(set)

    def ensure_node(key: str, kind: str = "wallet"):
        nodes.setdefault(key, {"id": key, "kind": kind, "name": key})

    def role(wallet: str, code: str, evidence: list[str], status: str = "INFERRED", note: str = ""):
        if not evidence:
            return
        roles.append({"wallet": wallet, "code": code, "label": DISPLAY[code],
                      "status": status, "evidence_ids": sorted(set(evidence)), "caveat": note})

    def link(source: str, target: str, kind: str, evidence: list[str],
             status: str, label: str, caveat: str = ""):
        relations.append({"from": source, "to": target, "type": kind,
                          "status": status, "label": label,
                          "evidence_ids": sorted(set(evidence)), "caveat": caveat})

    token_transfers: list[dict] = []
    sellers: dict[str, list[dict]] = defaultdict(list)
    fundees: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    buys_by_slot: dict[int, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    trade_events: dict[str, list[str]] = defaultdict(list)
    launch_slot = case.get("launch_slot")
    for e in events:
        typ = e["type"]
        if typ in ("sol_transfer", "token_transfer"):
            a, b = e["from"], e["to"]
            ensure_node(a)
            ensure_node(b)
            signatures_by_wallet[a].add(e["signature"])
            signatures_by_wallet[b].add(e["signature"])
            tag = "SOL_TRANSFER" if typ == "sol_transfer" else "TOKEN_TRANSFER"
            label = f"{e['amount']} {e['asset']}"
            link(a, b, tag, [e["id"]], "OBSERVED", label,
                 "在输入数据中观察到的转账事件，不证明两地址同控，也非卖出")
            if typ == "token_transfer":
                token_transfers.append(e)
            if typ == "sol_transfer":
                fundees[a][b].append(e["id"])
        elif typ in ("swap_buy", "swap_sell"):
            wallet, venue = e["wallet"], e["venue"]
            ensure_node(wallet)
            venue_key = "venue:" + venue
            ensure_node(venue_key, "venue")
            # Edges indicate a recorded event at a venue, NOT direct token counterparties.
            trade_events[wallet].append(e["id"])
            signatures_by_wallet[wallet].add(e["signature"])
            if typ == "swap_buy":
                buys_by_slot[e.get("slot", -1)][wallet].append(e["id"])
                link(venue_key, wallet, "SWAP_BUY_EVENT", [e["id"]], "OBSERVED", "买入事件",
                     "箭头用于表示该钱包发生买入，不代表该池对钱包做了直接资产转账")
            else:
                sellers[wallet].append(e)
                link(wallet, venue_key, "SWAP_SELL_EVENT", [e["id"]], "OBSERVED", "卖出事件",
                     "箭头用于表示该钱包发生卖出，不是 Token 去向或净收益证明")
        else:
            src = "promoter:" + e["promoter"]
            ensure_node(src, "promoter")
            mintnode = "mint:" + mint
            ensure_node(mintnode, "mint")
            link(src, mintnode, "PROMOTION_CLAIM", [e["id"]], "HYPOTHESIS", "营销声明",
                 "仅为提供的材料声明；未核宣传合作、付款或钱包控制")
            if e.get("wallet"):
                ensure_node(e["wallet"])
                role(e["wallet"], "promoter_link_claim", [e["id"]], "HYPOTHESIS",
                     "营销内容未独立核实，不能断言与钱包有付费合作")

    for sender, targets in sorted(fundees.items()):
        if len(targets) >= 2:
            role(sender, "funder_observed", [eid for v in targets.values() for eid in v], "OBSERVED",
                 "仅能观察 SOL 转出，最终经济出资者未知")
            for a, b in combinations(sorted(targets), 2):
                link(a, b, "SHARED_FUNDER_CANDIDATE", targets[a] + targets[b],
                     "INFERRED", "共同 SOL 来源",
                     "交易所/机器人/公用分发 Hub 亦会导致这种模式，不证明共同控制人")

    if isinstance(launch_slot, int):
        slot_buys = buys_by_slot.get(launch_slot, {})
        for wallet, eids in sorted(slot_buys.items()):
            role(wallet, "launch_buyer_candidate", eids, "INFERRED",
                 "创建槽买入通常无法以相同执行顺序跟单")
        for a, b in combinations(sorted(slot_buys), 2):
            link(a, b, "SAME_SLOT_CANDIDATE", slot_buys[a] + slot_buys[b],
                 "INFERRED", "同 Slot 买入",
                 "不代表真实 Jito Bundle，更不代表共同控制")

    for wallet, eids in sorted(trade_events.items()):
        if len(eids) >= 5:
            role(wallet, "active_trader_candidate", eids, "INFERRED",
                 "仅表示本样本活跃，不证明刷量、洗盘或操纵")

    for tr in token_transfers:
        recv = tr["to"]
        # Case records observed first-seen, not actual wallet creation time.
        role(recv, "new_receiver_candidate", [tr["id"]], "INFERRED",
             "仅指本数据中的 Token 接收者；是否新钱包/新控制人未知")
        later = [e for e in sellers.get(recv, []) if e["event_time"] > tr["event_time"]]
        if later:
            role(recv, "receiver_seller_candidate", [tr["id"]] + [x["id"] for x in later],
                 "INFERRED", "先收再卖的时序成立；不能证明卖出的正是这笔转入 Token，亦非同控证据")

    coverage = dict(case.get("coverage", {}))
    if not coverage:
        warnings.append("DATA_COVERAGE_UNKNOWN: no coverage declaration")
    for field in ("raw_rpc_complete", "historical_signatures_complete", "quotes_and_fees_complete"):
        if coverage.get(field) is not True:
            warnings.append(f"INCOMPLETE_OR_UNKNOWN: {field}")
    warnings.append("ECONOMIC_CONTROL_UNKNOWN: transfers and timing do not prove common owner")
    warnings.append("COPYABILITY_UNKNOWN: no independent real-time signal-to-execution net return evidence")

    return {
        "version": "0.1.0", "case_id": case["case_id"], "mint": mint,
        "data_status": case.get("data_status", "UNKNOWN"),
        "coverage": coverage, "events": events,
        "nodes": sorted(nodes.values(), key=lambda n: n["id"]),
        "relations": relations, "roles": roles,
        "warnings": sorted(set(warnings)),
        "copyability": {"verdict": "COPYABILITY_UNKNOWN", "verified_positive_edge": False,
                        "reason": "未取得可冻结的真实观察时间、历史报价/费用/滑点、完整失败样本及样本外净 PnL"},
        "interpretation_notice": "关系与角色均为有限输入的观察或推断，不证明操盘手身份，也不是交易建议",
    }


def _node_color(kind: str) -> str:
    return {"wallet": "#6a91ed", "venue": "#64b4a4", "mint": "#d7a35f", "promoter": "#af86d0"}.get(kind, "#8491a7")


def _graph_svg(report: dict) -> str:
    nodes = report["nodes"]
    n = max(len(nodes), 1)
    width, height = 1120, 690
    cx, cy, radius = width / 2, height / 2, min(width, height) * .35
    coords = {}
    for i, node in enumerate(nodes):
        a = -math.pi/2 + i*2*math.pi/n
        coords[node["id"]] = (cx + radius*math.cos(a), cy + radius*math.sin(a))
    parts = [f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="模拟钱包有向关系图" xmlns="http://www.w3.org/2000/svg">',
             '<defs><marker id="arr" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0 0 L10 4 L0 8 Z" fill="#8d97ad"/></marker></defs>']
    for index, rel in enumerate(report["relations"]):
        a, b = coords[rel["from"]], coords[rel["to"]]
        dx, dy = b[0]-a[0], b[1]-a[1]
        dist = math.hypot(dx, dy) or 1
        ux, uy = dx/dist, dy/dist
        ax, ay = a[0] + ux*42, a[1] + uy*42
        bx, by = b[0] - ux*48, b[1] - uy*48
        dotted = rel["status"] != "OBSERVED"
        stroke = "#f6a86a" if dotted else "#8d97ad"
        dash = 'stroke-dasharray="6 7"' if dotted else ""
        # Small offset of crossing lines to reduce perfect overlap.
        offset = (index % 3 - 1) * 8
        perp = (-uy*offset, ux*offset)
        title = f'{rel["type"]} | {rel["label"]} | {rel["status"]} | {", ".join(rel["evidence_ids"])} | {rel["caveat"]}'
        parts.append(f'<path d="M {ax:.1f},{ay:.1f} Q {(ax+bx)/2+perp[0]:.1f},{(ay+by)/2+perp[1]:.1f} {bx:.1f},{by:.1f}" fill="none" stroke="{stroke}" stroke-width="1.9" {dash} marker-end="url(#arr)"><title>{escape(title)}</title></path>')
    for node in nodes:
        x, y = coords[node["id"]]
        color = _node_color(node["kind"])
        label = node["name"]
        short = label if len(label) < 17 else label[:14] + "…"
        parts.append(f'<g><circle cx="{x:.1f}" cy="{y:.1f}" r="36" fill="{color}" stroke="#d2d9e9" stroke-width="2"><title>{escape(label)} | {node["kind"]}</title></circle><text x="{x:.1f}" y="{y+56:.1f}" text-anchor="middle" fill="#dfe6f5" font-size="14">{escape(short)}</text></g>')
    parts.append("</svg>")
    return "".join(parts)


def render_html(report: dict) -> str:
    def h(v: Any) -> str:
        return escape(str(v))
    role_rows = "".join(f'<tr><td>{h(r["wallet"])}</td><td>{h(r["label"])}</td><td><span class="status">{h(r["status"])}</span></td><td>{h(", ".join(r["evidence_ids"]))}</td><td>{h(r["caveat"])}</td></tr>' for r in report["roles"])
    relation_rows = "".join(f'<tr><td>{h(r["from"])} → {h(r["to"])}</td><td>{h(r["type"])}</td><td>{h(r["label"])}</td><td>{h(r["status"])}</td><td>{h(", ".join(r["evidence_ids"]))}</td><td>{h(r["caveat"])}</td></tr>' for r in report["relations"])
    coverage_rows = "".join(f'<li><code>{h(k)}</code>：{h(v)}</li>' for k,v in sorted(report["coverage"].items()))
    warning_rows = "".join(f'<li>{h(w)}</li>' for w in report["warnings"])
    return f'''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>跟单｜{h(report["case_id"])}</title>
<style> :root{{color-scheme:dark}}*{{box-sizing:border-box}}body{{margin:0;background:#0f172a;color:#d9e4f5;font:15px/1.6 system-ui,-apple-system,Segoe UI,sans-serif}}main{{max-width:1320px;margin:auto;padding:24px}}h1{{font-size:30px;margin-bottom:5px}}h2{{font-size:20px;margin-top:32px}}p,.muted{{color:#a6b2c8}}.tag{{display:inline-block;background:#263951;border-radius:7px;padding:3px 9px;margin-right:8px}}.panel{{background:#192438;border:1px solid #354256;border-radius:16px;padding:18px;overflow:hidden}}svg{{display:block;width:100%;height:auto;min-height:360px}}.legend{{display:flex;flex-wrap:wrap;gap:12px;color:#b0bbcf;font-size:13px}}.dot{{display:inline-block;width:12px;height:12px;border-radius:50%;vertical-align:middle;margin-right:5px}}table{{width:100%;border-collapse:collapse;font-size:13px;min-width:850px}}th,td{{padding:9px 11px;border-bottom:1px solid #314057;text-align:left;vertical-align:top}}th{{color:#f1f5fd;background:#253449}}.scroller{{overflow-x:auto}}.status{{color:#f2b676}}code{{font-size:12px;overflow-wrap:anywhere}}.notice{{border-left:3px solid #efb366;padding-left:14px}}@media(max-width:640px){{h1{{font-size:24px}}main{{padding:12px}}}}</style></head>
<body><main><h1>跟单 · 钱包关系调查图谱</h1><p>案例 {h(report["case_id"])} · Mint <code>{h(report["mint"])}</code> · 数据：{h(report["data_status"])} · 版本 {h(report["version"])}</p>
<p class="notice"><strong>非真实交易 / 非投资建议：</strong>{h(report["interpretation_notice"])}。当前跟单结论：<strong>{h(report["copyability"]["verdict"])}</strong>。</p>
<div class="panel">{_graph_svg(report)}<div class="legend"><span><i class="dot" style="background:#6a91ed"></i>钱包</span><span><i class="dot" style="background:#64b4a4"></i>交易场所（事件，不是交易对手）</span><span><i class="dot" style="background:#d7a35f"></i>Mint</span><span><i class="dot" style="background:#af86d0"></i>宣传来源</span><span>实线：样本观察</span><span>虚线橙色：关系推断/假设</span><span>悬停边/节点显示证据</span></div></div>
<h2>钱包角色候选</h2><div class="panel scroller"><table><thead><tr><th>钱包</th><th>候选角色</th><th>级别</th><th>证据事件</th><th>不能证明什么</th></tr></thead><tbody>{role_rows}</tbody></table></div>
<h2>关系证据链</h2><div class="panel scroller"><table><thead><tr><th>来源 → 去向</th><th>事件/关系</th><th>摘要</th><th>级别</th><th>证据</th><th>替代解释/边界</th></tr></thead><tbody>{relation_rows}</tbody></table></div>
<h2>覆盖与缺口</h2><div class="panel"><ul>{coverage_rows}</ul><h3>警告与未知</h3><ul>{warning_rows}</ul></div>
<p>离线原型：由输入 JSON 生成；真实链上适配、全量历史、签名归档和可复制净收益尚未验证。</p></main></body></html>'''


def write_outputs(report: dict, directory: str | Path) -> tuple[Path, Path]:
    target = Path(directory)
    target.mkdir(parents=True, exist_ok=True)
    js, page = target / "demo_report.json", target / "demo_report.html"
    js.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    page.write_text(render_html(report), encoding="utf-8")
    return js, page
