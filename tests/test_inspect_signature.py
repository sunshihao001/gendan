"""Synthetic getTransaction JSON fixture; no RPC requests are made."""
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).parents[1]))
from tools.inspect_signature import inspect, request_transaction


def tx():
    return {"result": {"slot": 10, "blockTime": 1750000000,
        "transaction": {"signatures": ["SYNTHETIC_SIG"],
            "message": {"accountKeys": [{"pubkey": "TokenAccountA"}, {"pubkey": "TokenAccountB"}],
                        "instructions": []}},
        "meta": {"err": None,
                 "preTokenBalances": [{"accountIndex": 0, "mint": "MINT", "owner": "WALLET_A", "uiTokenAmount": {"amount": "1000000", "decimals": 6}}],
                 "postTokenBalances": [{"accountIndex": 0, "mint": "MINT", "owner": "WALLET_A", "uiTokenAmount": {"amount": "500000", "decimals": 6}},
                                       {"accountIndex": 1, "mint": "MINT", "owner": "WALLET_B", "uiTokenAmount": {"amount": "500000", "decimals": 6}}],
                 "innerInstructions": [{"index": 0, "instructions": [{"program": "spl-token", "parsed": {"type": "transferChecked", "info": {"source": "TokenAccountA", "destination": "TokenAccountB", "mint": "MINT", "tokenAmount": {"amount": "500000"}, "authority": "WALLET_A"}}}]}]}}}


class RpcInspectTests(unittest.TestCase):
    def test_transfer_and_net_asset_changes(self):
        r = inspect(tx(), mint="MINT")
        self.assertEqual(len(r["parsed_token_transfers"]), 1)
        self.assertEqual(r["token_account_changes"][0]["net_change_raw"], "-500000")
        self.assertEqual(r["token_account_changes"][1]["owner"], "WALLET_B")
        self.assertIn("NOT_WALLET_LIFECYCLE_COMPLETE", r["status"])

    def test_missing_owner_does_not_guess(self):
        c = tx()
        del c["result"]["meta"]["preTokenBalances"][0]["owner"]
        with self.assertRaisesRegex(ValueError, "owner missing"):
            inspect(c)

    def test_missing_balances_rejected(self):
        c = tx()
        del c["result"]["meta"]["preTokenBalances"]
        with self.assertRaisesRegex(ValueError, "balances missing"):
            inspect(c)

    def test_http_rpc_blocked(self):
        with self.assertRaisesRegex(ValueError, "https"):
            request_transaction("SIGNATURE", "http://localhost:8899")


if __name__ == "__main__":
    unittest.main()
