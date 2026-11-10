@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
  set "PYCMD=py -3"
) else (
  set "PYCMD=python"
)
%PYCMD% -m unittest discover -s tests -q
if errorlevel 1 (
  echo Tests failed. Report not opened.
  pause
  exit /b 1
)
%PYCMD% -m tools.snapshot_case data/blix_archived_mint_vendor_summary.json --out output
if errorlevel 1 (
  echo Failed to generate report.
  pause
  exit /b 1
)
start "" "%CD%\output\case_report.html"
echo Report opened. This is an archived historical case, NOT live trading data.
pause
