# Null test (PREREG rule 13), cell N50 (proportion 0.50, mean NED), run 2026-10-18-0839

Paired permutation null against FeVeT's published per-item 0.50 predictions (the bar holder), 400 controls: in control c every cognate set's rows are swapped between the candidate (COMB-8, runs/2026-10-18-0839/out/comb8/test/0.50) and FeVeT with probability 1/2 (random.Random(20261018 + c)); d = candidate's advantage on the cell metric, left-to-right summation. Run by the main session at 2026-10-18T11:27Z after selection.md existed; tool runs/2026-10-18-0839/tools/null_test.py (working directory runs/2026-10-18-0839); full output runs/2026-10-18-0839/out/null_N50.out and .json. Lines below copied from the tool's output.

controls: 400
best_control: 0.011032244018352122
real: 0.05967853202112411
real_beats_all_controls: yes
command: STUB_MPL=1 WORKDIR/runs/2026-10-16-2026/attempts/calibrator/venv/bin/python -I tools/null_test.py --prop 0.50 --bar fevet --cand-dir out/comb8/test/0.50 --out out/null_N50.json

detail: candidate NED 0.24912258145405175, bar NED 0.30880111347517586, d = 0.05967853202112411
