# REPRODUCE (p4)

Environment used: Python 3.11.15, numpy 2.4.6, scipy 1.17.1, pandas 3.1.0, scikit-learn 1.9.1 (CPU). Run from inside
this claim folder; `<python>` is your interpreter; always isolated mode (-I) with the data path as an argument.
Nothing downloads, installs or unpickles anything.

1. `sha256sum data/sperm-whale-dialogues.csv` -> 1856c8bf915cc5ae6f928aaa2036cbbc6ad8840bb6e4f6a96aaeb96953215da2
2. Frozen pipeline (5 folds, inner CV, leakage self-test; about 20 s):

       <python> -I code/score_p4.py data/sperm-whale-dialogues.csv rerun

   Prints per-fold bits and `GATE p4: {...}`; writes rerun/p4_per_position.csv and rerun/p4_summary.json.
3. `sha256sum rerun/p4_per_position.csv result/p4_per_position.csv` (expect identical on the same library versions).
4. Independent recomputation: log-loss per row = -(y log2 p + (1-y) log2(1-p)) with y = y_same; gain = reference
   minus model; bootstrap over REC groups with replacement, statistic sum(gain)/count.
5. Null controls (optional, about 3-6 s each): `<python> -I null/nulls.py N4 data/sperm-whale-dialogues.csv 0 400 rerun/N4.csv`
   with code/ on the import path (copy null/nulls.py into code/ first, since it imports p4lib and swlib from its
   own folder).
