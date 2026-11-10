#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
python3 -m unittest discover -s tests -q
python3 -m tools.snapshot_case data/blix_archived_mint_vendor_summary.json --out output
printf '%s\n' "Report generated at: $PWD/output/case_report.html"
if command -v open >/dev/null 2>&1; then open output/case_report.html
elif command -v xdg-open >/dev/null 2>&1; then xdg-open output/case_report.html
fi
