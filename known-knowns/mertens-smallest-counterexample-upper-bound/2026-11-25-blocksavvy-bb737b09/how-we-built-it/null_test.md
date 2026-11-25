# Null test (PREREG lens lattice2; frozen design, seed 20261125)
controls: 400
best_control: 0.48328909749031995
real: 0.981446976007603
real_beats_all_controls: yes
command: cd attempts/lattice2 && python code/null_test.py 0 1 && python code/null_summary.py

Notes: "real" is the best certified |h_StR| below y_KN from the lattice2 search (E10, y = 3867117295887568249.133776574254,
jobs/E10_n160_tplus_r120.rescore.out). It beats every control (0 of 400 control hits) but is NOT a hit (< 1 + 6e-8),
so no p3 claim follows. The p4 K2 check is a deterministic certified sum and needs no null model.
Output files: attempts/lattice2/null_controls_0.jsonl, attempts/lattice2/null_summary.out.
