# Null test (PREREG.md, null design N-SF): paired label-swap null on the p1 subset (2,038 cases), 400 controls
controls: 400
best_control: 0.013722
real: 0.033707
real_beats_all_controls: yes
command: python -I attempts/p1-eval/code/p1_eval.py ../2026-11-11-1222/attempts/full-eval/output/h2h/h2h_percase.tsv ../2026-11-11-0916/work/C_percase.tsv attempts/p1-eval/output
Values copied from attempts/p1-eval/output/p1_eval.out (statistic: mean of RR_method - RR_LIRICAL; control k swaps
the two tools' RR per case with probability 1/2, random.Random(20261111 + k)). Controls >= real: 0.
