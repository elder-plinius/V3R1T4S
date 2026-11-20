# REPRODUCE

Environment used: Python 3.11.15, numpy 2.4.6, scipy 1.17.1, pandas 3.1.0 (CPU). No other package. Run every
command from inside this claim folder, with the data path passed as an argument and Python in isolated mode (-I).
Replace `<python>` with your interpreter. Nothing here downloads, installs or unpickles anything.

1. Data checksum:

       sha256sum data/sperm-whale-dialogues.csv
       # expect 1856c8bf915cc5ae6f928aaa2036cbbc6ad8840bb6e4f6a96aaeb96953215da2 (500,380 bytes)

   To fetch it yourself (one plain request):
   https://raw.githubusercontent.com/pratyushasharma/sw-combinatoriality/7228c8eed2cc27ddd23b74c51aeccec9d762389e/data/sperm-whale-dialogues.csv

2. Rerun the frozen pipeline end to end (all 5 folds, all inner CV, leakage self-test; about 7 minutes single-core):

       <python> -I code/score_content.py data/sperm-whale-dialogues.csv rerun

   It prints per-fold bits, the leakage results and the line `GATES: {...}`, and writes rerun/folds.csv,
   rerun/probs_R1.csv, rerun/probs_twin.csv, rerun/probs_full.csv, rerun/probs_all.npz (plain arrays, no pickle)
   and rerun/content_summary.json.

3. Compare with the saved results (expect identical files on the same library versions):

       sha256sum rerun/probs_full.csv result/probs_full.csv rerun/probs_twin.csv result/probs_twin.csv rerun/probs_R1.csv result/probs_R1.csv rerun/folds.csv result/folds.csv

4. Independent recomputation from the saved per-position probabilities: each row of result/probs_*.csv is
   REC, pos (0-based position in the TsTo-ordered stream), fold, y_token (true token id (c-1)*5+b), p0..p49.
   Check every row sums to 1 with no zero entry; cross-entropy = mean of -log2 p[y_token]; gains = R1 minus full
   and twin minus full; bootstrap = resample the REC groups with replacement, statistic sum(gain)/count.

Expected pooled values: R1 2.7802, twin 2.6549, full 2.1238 bits per coda; full vs R1 +0.6563; full vs twin +0.5311
with 95% interval [0.4571, 0.6325] at seed 20261119.
