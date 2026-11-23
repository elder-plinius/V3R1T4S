# Baseline record (p4)

No published baseline exists for this exact task (same-or-switch of the whale label at the bank's scored positions
of sperm-whale-dialogues.csv). The partial win defines the reference itself: "a smoothed first-order model of that
same-or-switch sequence". It is computed here from that definition (code/swlib.py: switch_counts, switch_probs,
switch_ref_fit): counts of (y_{t-1}, y_t) over positions >= 2 of the training-fold streams, additive smoothing alpha
from {0.01, 0.03, 0.1, 0.3, 1} by inner leave-one-training-fold-out CV. Same data, folds, scored set and metric
(bits per coda, pooled over the 5 held-out folds) as the model. Held-out reference bits per fold 0.8664, 0.8494,
0.8835, 0.7903, 0.8945; pooled 0.8503 (result/p4_summary.json).
