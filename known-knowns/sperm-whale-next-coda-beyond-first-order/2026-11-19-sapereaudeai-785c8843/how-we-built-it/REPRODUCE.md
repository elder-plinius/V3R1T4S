# REPRODUCE (p3)

Environment used: Python 3.11.15, numpy 2.4.6, scipy 1.17.1, pandas 3.1.0 (CPU). Run from inside this claim folder;
`<python>` is your interpreter; always isolated mode (-I), data path as an argument. Nothing downloads, installs or
unpickles anything.

1. `sha256sum data/DominicaCodas.csv` -> 53dd44fbfb0040da93656aa44883954f3abe18dd6539e90c625af86a96db6b45
2. Frozen pipeline (5 date folds, inner CV, leakage self-test; about 2 minutes):

       <python> -I code/score_p3.py data/DominicaCodas.csv rerun

   Prints per-fold bits and `GATE p3: {...}`; writes rerun/p3_probs_bigram.csv, rerun/p3_probs_full.csv,
   rerun/p3_summary.json, rerun/p3_folds.csv, rerun/p3_vocab.csv.
3. `sha256sum rerun/p3_probs_full.csv result/p3_probs_full.csv rerun/p3_probs_bigram.csv result/p3_probs_bigram.csv`
   (expect identical on the same library versions).
4. Independent recomputation: per row, -log2 p[y_token]; gain = bigram minus full; bootstrap over rewritten-Date
   groups (the part of `stream` before '|') with replacement, statistic sum(gain)/count.
