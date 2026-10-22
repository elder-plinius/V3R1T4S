# Null test, cell C20 (proportion 0.20), PREREG rule 13 (run 2026-10-18-0202)

Paired permutation null between the cell's candidate (COMB-NEW, runs/2026-10-18-0202/out/comb_new/test/0.20) and the bar
holder, Mockingbird-I1's official per-item predictions at 0.20: in control c, for every cognate set of every family, the two systems' predictions for all rows of
that set are swapped with probability 1/2 (random.Random(20261018 + c)); d_c = NED(bar side) - NED(candidate side),
official per-item NED and aggregation, left-to-right summation. Run by the main session at 2026-10-18T04:49Z, after
selection.md (sha256 2d0d43d4901280c8c26b1ae2d3b02e0c8c770873de4e9ee67cbf3dffedd1063c) and tools/score_test.py.
Output: runs/2026-10-18-0202/out/null_0.20.out and out/null_0.20.json.

values: candidate NED 0.20345235544710852, bar NED 0.2648052468982754, d = 0.061352891451166874
fast path bit-identical in every check: yes
controls: 400
best_control: 0.01732600288224881
real: 0.061352891451166874
real_beats_all_controls: yes
control mean 0.00030137828913791466 sd 0.00576800935470761; controls >= real: 0
command: STUB_MPL=1 WORKDIR/runs/2026-10-16-2026/attempts/calibrator/venv/bin/python -I runs/2026-10-18-0202/tools/null_test.py --prop 0.20 --bar mockingbird --cand-dir runs/2026-10-18-0202/out/comb_new/test/0.20 --out out/null_0.20.json
