# Null test, cell C10 (proportion 0.10), PREREG rule 13 (run 2026-10-18-0202)

Paired permutation null between the cell's candidate (COMB-ALL10, runs/2026-10-18-0202/out/comb_all10/test/0.10) and the bar
holder, run 2026-10-17-1806's confirmed combiner (frozen test-0.10 predictions): in control c, for every cognate set of every family, the two systems' predictions for all rows of
that set are swapped with probability 1/2 (random.Random(20261018 + c)); d_c = NED(bar side) - NED(candidate side),
official per-item NED and aggregation, left-to-right summation. Run by the main session at 2026-10-18T04:49Z, after
selection.md (sha256 2d0d43d4901280c8c26b1ae2d3b02e0c8c770873de4e9ee67cbf3dffedd1063c) and tools/score_test.py.
Output: runs/2026-10-18-0202/out/null_0.10.out and out/null_0.10.json.

values: candidate NED 0.18916240713560675, bar NED 0.19710919181751296, d = 0.00794678468190621
fast path bit-identical in every check: yes
controls: 400
best_control: 0.005948936672339172
real: 0.00794678468190621
real_beats_all_controls: yes
control mean -2.234311498897454e-05 sd 0.0023103494062423784; controls >= real: 0
command: STUB_MPL=1 WORKDIR/runs/2026-10-16-2026/attempts/calibrator/venv/bin/python -I runs/2026-10-18-0202/tools/null_test.py --prop 0.10 --bar ours --cand-dir runs/2026-10-18-0202/out/comb_all10/test/0.10 --out out/null_0.10.json
