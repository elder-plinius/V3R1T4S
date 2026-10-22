# Null test, cell C30 (proportion 0.30), PREREG rule 13 (run 2026-10-18-0202)

Paired permutation null between the cell's candidate (COMB-NEW, runs/2026-10-18-0202/out/comb_new/test/0.30) and the bar
holder, FeVeT's published per-item predictions at 0.30: in control c, for every cognate set of every family, the two systems' predictions for all rows of
that set are swapped with probability 1/2 (random.Random(20261018 + c)); d_c = NED(bar side) - NED(candidate side),
official per-item NED and aggregation, left-to-right summation. Run by the main session at 2026-10-18T04:49Z, after
selection.md (sha256 2d0d43d4901280c8c26b1ae2d3b02e0c8c770873de4e9ee67cbf3dffedd1063c) and tools/score_test.py.
Output: runs/2026-10-18-0202/out/null_0.30.out and out/null_0.30.json.

values: candidate NED 0.22327922550091464, bar NED 0.2632988364952282, d = 0.04001961099431353
fast path bit-identical in every check: yes
controls: 400
best_control: 0.01038051165515197
real: 0.04001961099431353
real_beats_all_controls: yes
control mean 9.711894693928851e-05 sd 0.0035018285383694057; controls >= real: 0
command: STUB_MPL=1 WORKDIR/runs/2026-10-16-2026/attempts/calibrator/venv/bin/python -I runs/2026-10-18-0202/tools/null_test.py --prop 0.30 --bar fevet --cand-dir runs/2026-10-18-0202/out/comb_new/test/0.30 --out out/null_0.30.json
