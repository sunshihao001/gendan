"""CLI: python -m gendan.cli data/demo_case.json --out output"""
import argparse
import json
from pathlib import Path
from .engine import analyze, write_outputs


def main() -> None:
    parser = argparse.ArgumentParser(description="Gendan offline evidence graph (no network, no trading)")
    parser.add_argument("input", type=Path, help="normalized JSON event case")
    parser.add_argument("--out", default="output", type=Path)
    args = parser.parse_args()
    case = json.loads(args.input.read_text(encoding="utf-8"))
    report = analyze(case)
    js, html = write_outputs(report, args.out)
    print(f"Case: {report['case_id']} | {len(report['events'])} events | {len(report['roles'])} roles | {len(report['relations'])} edges")
    print(f"Copyability: {report['copyability']['verdict']} | status: {report['data_status']}")
    print(f"JSON: {js}\nHTML: {html}")


if __name__ == "__main__":
    main()
