# PREREG.v5: matched-pair check of the species signal beyond the strongest covariate (p3 sensitivity S7)

frozen_utc: 2026-11-12T19:16:23Z

Seen before writing: W1/W2 covariate-only numbers, W1 and P2 permutation summaries. Not yet computed: anything below.
Nothing in earlier PREREG files changes. Reported as a sensitivity check; no primary number is replaced.

null_test: required (unchanged for the run)

S7. Using the saved species-RF out-of-fold scores of PREREG.md (20 repeats):
  - W1 (Qin 2012): AUC of the species score over (case, control) pairs whose ages differ by <= 3 years
    ("age-matched pairs"), mean over repeats with the 2.5-97.5 percentile range; next to it the same pair-restricted
    AUC of the age-only LR out-of-fold score is not available (not saved), so instead the AUC of raw age itself over
    the same pairs is reported (it should be near 0.5 by construction).
  - W2 (WT2D): the same with BMI-matched pairs (|BMI difference| <= 1.0 kg/m2).
  - Also: Spearman correlation of the species score with age (W1) / BMI (W2), separately within controls and within
    cases (repeat-0 scores).
