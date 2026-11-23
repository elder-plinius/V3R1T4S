# Null test for the p3 claim (PREREG.md, lens paper-rf)

controls: 1000
best_control: 0.2448512585812357
real: 0.26954233409610984
real_beats_all_controls: yes
command: WORKERS=4 python3 code/null_rf.py; python3 code/summarize.py (key null_rf)

Each control reruns the frozen random forest on the folds of real draw (j mod 100) after permuting receiver labels among each caller's calls (keeps every caller's receiver frequencies). Control mean 0.2107, sd 0.0119, 99.9th percentile 0.2426. The real statistic is the mean over 100 draws; each control is one draw, which is the conservative direction. The full-win pipeline's own null (output/null_pa: 99.9th percentile 0.5172 vs real 0.4902) is reported in attempts/prior-acoustic/report.md and is not part of this claim.
