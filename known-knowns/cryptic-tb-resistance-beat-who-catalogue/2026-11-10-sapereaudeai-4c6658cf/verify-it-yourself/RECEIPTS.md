# RECEIPTS: real output of `sh verify-it-yourself/run_checks.sh`

Run 2026-11-10T12:19:36Z from a clean copy of this package (Python 3.11.15, standard library only):

```
ok   sha256 of object/p2_knn_ETH_metrics.csv
ok   sha256 of object/predictions_ETH_knn10_split_v2_test.csv
ok   sha256 of object/random_control_splits_membership.bin
ok   sha256 of object/split_v2.csv.gz
ok   uncompressed split v2 sha256 = 3b4ed12292c1804bdd5e226c72e233eacf1be780f8432656e292e1d225640a56
ok   split v2: 12287 isolates, 3073 TEST
ok   no cluster spans TRAIN and TEST (7420 clusters)
ok   every scored isolate is in split-v2 TEST (2096 scored)
ok   nearest TRAIN neighbour of every scored TEST isolate is > 12 SNPs
recomputed split-v2 ETH: R 266, S 1830, threshold 0.483575, sensitivity 0.349624, specificity 0.950273
ok   split-v2 sensitivity at >= 95% specificity = 0.3496
ok   per-isolate calls follow the threshold
ok   metrics file real value equals the recomputed value
ok   400 random control splits, seeds 1..400
random controls: min 0.5135 mean 0.6003 max 0.6678; above split v2: 400 of 400
ok   every random-split value exceeds the split-v2 value
ok   every split meets >= 95% specificity at its threshold
alternative cluster-aware splits: n 100, min 0.1799 mean 0.3259 max 0.4662
ok   membership file: 400 rows x 1536 bytes
ok   each random control split holds 3,073 TEST isolates
note: full kNN recompute skipped (set CRYPTIC_GPI_DISTANCES, CRYPTIC_GPI_LABELS, CRYPTIC_REUSE_TABLE to run it)
PASS
```

Optional full recompute (numpy, with the three public input files named in RUN_IT_YOURSELF.md), same day:

```
alternative cluster-aware splits: n 100, min 0.1799 mean 0.3259 max 0.4662
ok   membership file: 400 rows x 1536 bytes
ok   each random control split holds 3,073 TEST isolates
ok   full recompute, split v2: 0.349624 vs 0.349624
ok   full recompute, random seed 1: 0.602606 vs 0.602606
ok   full recompute, random seed 2: 0.633117 vs 0.633117
ok   full recompute, random seed 3: 0.598007 vs 0.598007
PASS
```
