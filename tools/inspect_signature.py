"""Read-only Solana transaction inspection: source RPC JSON or GET-only-equivalent HTTPS JSON-RPC.

No keys, signers, orders or transaction submission. Observes token-account balances,
not end-user economic ownership or trading profit. Every transaction needs evidence.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from decimal import Decimal
import json
from pathlib import Path
from urllib.request import Request, urlopen


def pubkey(item: object) -> str:
    if isinstance(item, str):
        return item
    if isinstance(item, dict):
        return str(item.get("pubkey", ""))
    return ""


def request_transaction(signature: str, rpc_url: str) -> dict:
    if not rpc_url.startswith("https://"):
        raise ValueError("RPC URL must use https://")
    if not signature or any(c.isspace() for c in signature):
        raise ValueError("a nonempty no-whitespace signature is required")
    payload = {"jsonrpc": "2.0", "id": 1, "method": "getTransaction",
               "params": [signature, {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0,
                                      "commitment": "finalized"}]}
    req = Request(rpc_url, data=json.dumps(payload).encode("utf-8"),
                  headers={"Content-Type": "application/json", "User-Agent": "Gendan-ReadOnly/0.1"},
                  method="POST")
    with urlopen(req, timeout=20) as response:
        data = json.load(response)
    if "error" in data:
        raise ValueError(f"RPC returned error: {data['error']}")
    if data.get("result") is None:
        raise ValueError("RPC returned null result: pruned, not indexed or unavailable")
    return data


def inspect(payload: dict, mint: str | None = None) -> dict:
    tx = payload.get("result", payload)
    if not isinstance(tx, dict):
        raise ValueError("transaction must be an object")
    message = (tx.get("transaction") or {}).get("message") or {}
    meta = tx.get("meta") or {}
    if "preTokenBalances" not in meta or "postTokenBalances" not in meta:
        raise ValueError("required RPC pre/post token balances missing; cannot interpret ownership")
    addresses = [pubkey(k) for k in message.get("accountKeys", [])]
    pre, post = {}, {}
    def parse(rows, target):
        for b in rows:
            bmint = b.get("mint")
            if mint and bmint != mint:
                continue
            idx = b.get("accountIndex")
            if not isinstance(idx, int) or idx < 0 or idx >= len(addresses):
                raise ValueError("token balance account index unresolved")
            amount = (b.get("uiTokenAmount") or {}).get("amount")
            if amount is None or b.get("owner") is None:
                raise ValueError("token balance amount/owner missing; report UNKNOWN")
            key = (idx, bmint)
            if key in target:
                raise ValueError("same token account index duplicated in one balance side")
            target[key] = {"raw": Decimal(str(amount)), "owner": b["owner"],
                           "decimals": b["uiTokenAmount"].get("decimals")}
    parse(meta["preTokenBalances"], pre)
    parse(meta["postTokenBalances"], post)
    changes = []
    for idx, bmint in sorted(set(pre) | set(post)):
        before, after = pre.get((idx, bmint)), post.get((idx, bmint))
        if before and after and before["owner"] != after["owner"]:
            raise ValueError("token account owner changed: require separate evidence")
        representative = after or before
        if before and after and before["decimals"] != after["decimals"]:
            raise ValueError("token decimals conflict")
        delta = (after["raw"] if after else Decimal(0)) - (before["raw"] if before else Decimal(0))
        changes.append({"token_account": addresses[idx], "owner": representative["owner"], "mint": bmint,
                        "decimals": representative["decimals"], "pre_raw": str(before["raw"] if before else 0),
                        "post_raw": str(after["raw"] if after else 0), "net_change_raw": str(delta)})
    parsed_transfers = []
    instr = [("outer", ix, inst) for ix, inst in enumerate(message.get("instructions", []))]
    for group in meta.get("innerInstructions") or []:
        for index, inst in enumerate(group.get("instructions", [])):
            instr.append((f"inner:{group.get('index','?')}", index, inst))
    for level, ix, inst in instr:
        parsed = inst.get("parsed") if isinstance(inst, dict) else None
        if not isinstance(parsed, dict) or parsed.get("type") not in {"transfer", "transferChecked"}:
            continue
        prog = inst.get("program")
        info = parsed.get("info") or {}
        if prog in {"spl-token", "spl-token-2022"} and info.get("source") and info.get("destination"):
            if mint and info.get("mint") and info["mint"] != mint:
                continue
            parsed_transfers.append({"level": level, "index": ix, "source_token_account": info["source"],
                                     "destination_token_account": info["destination"], "mint": info.get("mint", "UNKNOWN"),
                                     "raw_amount": info.get("amount", (info.get("tokenAmount") or {}).get("amount", "UNKNOWN")),
                                     "authority": info.get("authority", "UNKNOWN"),
                                     "status": "PARSED_INSTRUCTION_NOT_CONTROLLER_PROOF"})
    signatures = (tx.get("transaction") or {}).get("signatures") or []
    return {"signature": signatures[0] if signatures else "UNKNOWN", "slot": tx.get("slot"), "block_time": tx.get("blockTime"),
            "transaction_failed": bool(meta.get("err")), "token_account_changes": changes,
            "parsed_token_transfers": parsed_transfers, "unknowns": [
                "Net token-account change is not sufficient to infer a swap, price or realized profit",
                "Token transfer between accounts does not prove common control or subsequent liquidation",
                "Only addresses exposed by this RPC transaction are covered; history is not complete",
            ], "status": "RAW_RPC_INSPECTED_NOT_WALLET_LIFECYCLE_COMPLETE"}


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect raw Solana RPC transaction without signing/trading")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--input-rpc", type=Path, help="saved getTransaction jsonParsed JSON")
    source.add_argument("--signature", help="fetch transaction from public Solana RPC (HTTPS POST read method)")
    parser.add_argument("--mint", help="optional token mint filter")
    parser.add_argument("--rpc-url", default="https://api.mainnet-beta.solana.com")
    parser.add_argument("--out", type=Path, default=Path("output/tx_inspection.json"))
    args = parser.parse_args()
    payload = json.loads(args.input_rpc.read_text(encoding="utf-8")) if args.input_rpc else request_transaction(args.signature, args.rpc_url)
    result = inspect(payload, mint=args.mint)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"signature={result['signature']} accounts={len(result['token_account_changes'])} parsed_transfers={len(result['parsed_token_transfers'])} output={args.out.resolve()}")


if __name__ == "__main__":
    main()
