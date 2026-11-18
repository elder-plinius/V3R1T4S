# Null test — polaris/pkis2-lok-slk-c-1 (400 label-permutation controls)

The frozen E2 pipeline (same features, seeds and test rows; the final Platt map is monotone and
therefore PR-AUC-invariant, asserted for the real fit at the top of the runner's output) was
retrained 400 times on the 508 official train rows with the training labels permuted per control id
(the continuous LOK/SLK labels and the CLASS_LOK/CLASS_SLK labels each independently permuted). Each
control was scored on the official 132 test rows.

controls: 400
best_control: 0.607118
real: 0.634334
real_beats_all_controls: yes
command: python3 runs/2026-11-18-1010/code/null_test_lokslk.py  (writes null_test_lokslk/null_results.csv; then code/summarize_null_lokslk.py)

control CLASS_LOK pr_auc: min 0.117245, mean 0.251396, max 0.607118
control CLASS_SLK pr_auc: min 0.066369, mean 0.143578, max 0.377647
control mean pr_auc:     min 0.115582, mean 0.197487, max 0.369311
real CLASS_SLK pr_auc: 0.377856659137; real mean pr_auc: 0.506095215029
real_beats_all_controls_mean: yes
real_beats_all_controls_slk: yes
Disclosure: the CLASS_SLK target beats its best control only narrowly (0.377857 vs 0.377647,
+0.00021); the claimed metric (CLASS_LOK, the value the live leaderboard lists) clears its best
control by +0.027 and the two-target mean by +0.137. The thin SLK margin is recorded, not hidden.
