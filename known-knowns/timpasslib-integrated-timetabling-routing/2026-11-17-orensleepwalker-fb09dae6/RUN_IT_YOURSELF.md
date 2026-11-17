# Verify
From this folder: `sh verify-it-yourself/run_checks.sh` (last line PASS). Needs python3 (standard library), curl and sha256sum. verify-it-yourself/RECEIPTS.md holds a real run.
By hand: unpack the instance zip and the posted best zip from https://timpasslib.aalto.fi/data/ (links in run_checks.sh), then `python3 -I verify-it-yourself/evaluate.py <instance folder> <timetable.csv>` prints one JSON line with feasibility and the total.
To rebuild timetables of this kind (not deterministic; multi-threaded CP-SAT): how-we-built-it/code/ (joint_lns.py takes `<instance dir> <start.csv> <out dir> <seconds> <seed>`; paths in the saved code were cleaned and need adjusting).
