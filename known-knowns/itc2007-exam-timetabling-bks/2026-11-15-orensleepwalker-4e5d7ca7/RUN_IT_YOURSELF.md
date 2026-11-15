# Run it yourself
From this folder, in a fresh shell:

    sh verify-it-yourself/run_checks.sh

Expected output: two JSON lines (posted best total 2327, object total 2305, both "feasible": true, "hard": {}) and a
last line PASS. To evaluate by hand: download set5.exam (URL in run_checks.sh), then
python3 -I verify-it-yourself/check.py set5.exam object/set5.sol
To rebuild a timetable of this kind (not deterministic): see how-we-built-it/COMMANDS.md.
