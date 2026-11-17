# Null test (PREREG.md N-SF, primary)

Statistic: dMRR = MRR(C) - MRR(PRE), paired, gene level, LIRICAL 2.4.1, over the 500 sampled cases complete in both
conditions. Control k swaps each case's C and PRE reciprocal ranks with probability 1/2 (random.Random(20261111 + k))
and recomputes dMRR. Values copied from attempts/lirical-temporal/result/summary.json (null_NSF).

controls: 400
best_control: 0.10625759104180113
real: 0.4768890962028496
real_beats_all_controls: yes
command: python -I attempts/lirical-temporal/code/score_lirical.py score attempts/lirical-temporal/output work ../2026-11-11-0916/work ../2026-11-11-0916/data/hgnc_protein-coding_gene.txt <hgnc_complete_set_2026-06-05.txt> <mim2gene_medgen> attempts/lirical-temporal/result   (run from this run folder; the panel copy is claim/REPRODUCE.md step 1)

Not run (declared in PREREG.md): run 1's N2 date-permutation placebo, which needs every case scored under all 12 releases.
