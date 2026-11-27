# Run it yourself
1. `sh verify-it-yourself/run_checks.sh` (expect PASS).
2. One bound by hand: download the instance (URL pattern in run_checks.sh), then `python3 verify-it-yourself/break_floor_stdlib.py <instance.xml>` or `python3 object/<instance>/certificate.py <instance.xml>`.
3. Solver replay (OR-Tools 9.15): `python3 verify-it-yourself/replay.py <file with lines: name path seed>`.
