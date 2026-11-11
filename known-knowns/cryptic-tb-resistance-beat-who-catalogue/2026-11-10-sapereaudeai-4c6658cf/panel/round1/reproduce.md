# REPRODUCE skeptic: p2 leakage claim (ETH, split v2 vs 400 random splits)

context: subagent (Agent tool, subagent_type reproduce)

Started 11:56:39Z (date -u). Read only CLAIM.md, REPRODUCE.md, EXTERNAL_INPUTS.md, PREREG.md (+ PREREG.v2.md, PREREG.v3.md),
null_test.md and the files they name. I wrote my own checker before opening code/; code/ was read afterwards only to
explain the mismatches below. Scratch: ../work/panel_reproduce/ (my_checker.py, my_checker2.py, my_exact.py and their
outputs run1_output.txt, run2_output.txt, exact_output.txt).

## Definitions my checker implements (quoted from PREREG.md)

Split rule ("Split v2 (frozen)"): "link two reuse isolates when their released SNP distance is <= 12 ... clusters are the
connected components (single linkage) with no hub removal, so no TRAIN isolate is within 12 SNPs of any TEST isolate.
Components larger than 614 isolates (5%) go to TRAIN whole ... The other components are ordered by
sha256('V3R1T4S-cryptic-split-v2|' + smallest UNIQUEID in the component) and go whole to TEST until TEST first holds
>= 3,072 isolates (25%)."

Phenotype filter: "Primary: <DRUG>_PHENOTYPE_QUALITY == HIGH and phenotype in {R, S} ('I' excluded)."

p2 model and metric ("p2 (leakage)"): "For a test isolate, take the k = 10 nearest training isolates among those with a
HIGH-filter R/S phenotype for the drug (stable sort by distance, ties by matrix index); score = sum(w_j * R_j) / sum(w_j),
w_j = 1 / (1 + d_j)." "Metric: sensitivity at >= 95% specificity on the test part: threshold t = the smallest score value
such that the fraction of test negatives with score >= t is <= 0.05; sensitivity = fraction of test positives with score >= t."
"Controls: 400 random isolate-level splits with the same TEST size (3,073 of 12,287), numpy seeds 1..400. Leakage is
demonstrated only if every one of the 400 random-split metrics is strictly greater than the split-v2 metric".

Implementation choices (mine): one pass over the 12,287 reuse rows of the distance matrix (np.load mmap_mode='r', 256-row
blocks); union of all edges d <= 12 by scipy connected_components; per ETH row a stable argsort of the ETH columns in
matrix-index order (top 1,000 kept, with a hard error if any test isolate had fewer than 10 training isolates among them;
it never fired); candidate thresholds = the distinct test scores; FP fraction computed as count/len. A second script
(my_exact.py) recomputes every score as an exact rational (fractions.Fraction) and applies the threshold rule in integers
(20 * count <= N) to settle floating-point ties.

## Recomputed (pasted from ../work/panel_reproduce/run2_output.txt unless noted)

Input hashes (sha256sum): split/split.csv 3b4ed122...0a56 (matches CLAIM.md), data/CRyPTIC_reuse_table_20240917.csv
f785ae87...1c1b (matches), data/tables/GPI_SNP_DISTANCES_LABELS.npy 611512d7...5e61 (matches), distance matrix in the
read-only cache 02d7cd46...f5dd (matches EXTERNAL_INPUTS.md, 463,784,096 bytes).

(1) Split
```
reuse rows 12287 unique ids 12287 split rows 12287
split.csv row order == reuse table order: True
reuse isolates found in matrix labels 12287
matrix (15228, 15228) int16
read pass done 6.5 s; negative entries 0; max distance 2550; directed edges <=12 86032
asymmetric <=12 edges 0
components 7420
singletons 6399 largest [2539, 72, 48, 38, 35]
min TRAIN-TEST distance over TEST rows 13 over TRAIN rows 13
TEST isolates with a TRAIN isolate within 12 SNPs 0
components spanning TRAIN and TEST 0
big components [('site.02.subj.0031.lab.2014234024.iso.1', 2539)]
regenerated TEST 3073 TRAIN 9214 TEST clusters 2282 TRAIN clusters 5138
regenerated SPLIT column == split.csv SPLIT: True
CLUSTER column == C + smallest UNIQUEID of my component: True
sha256 of my regenerated split csv 3b4ed12292c1804bdd5e226c72e233eacf1be780f8432656e292e1d225640a56
```
The minimum TRAIN-TEST distance is computed over the full 12,287 x 12,287 reuse block (every TEST row against every TRAIN
column and vice versa), not a sample. My own regeneration from the rule reproduces split/split.csv byte for byte.

(3) Phenotype filter
```
ETH quality values {'HIGH': 8820, 'LOW': 1956, 'MEDIUM': 1354, nan: 157}
ETH binary values {'S': 9431, 'R': 1727, 'I': 972, nan: 157}
ETH filtered isolates 8251 R 1189 S 7062
```
Matches the log (8,251 phenotyped, R 1,189). The per-split n_test and R_test of all 400 random rows of output/p2_knn_ETH.csv
equal mine ("n_test equal True R equal True"); code/p2_knn.py applies the same filter (read after my run).

(2) kNN metric, real split and controls
```
REAL split v2: {'sens95': 0.34962406015037595, 'spec': 0.9502732240437158, 'thr': 0.4835751364256107, 'sens95_negcand': 0.3458646616541353, 'ap': 0.4169851972238189, 'n': 2096, 'R': 266}
prediction file rows 2096 merge {'both': 2096, 'left_only': 0, 'right_only': 0}
max |score diff| 2.220446049250313e-16 nearest dist equal True phenotype equal True
CALL column consistent with my threshold True calls R 184
npz seeds 1..400: True
npz test_rows == sorted default_rng(seed).choice(12287,3073,replace=False) for all 400 seeds: True
RANDOM n 400 min 0.5135 mean 0.6003 max 0.6678; all > real: True (count above 400); margin mean-real 0.2507, min-real 0.1639
random AP min 0.5965 mean 0.6699 max 0.7395
neg-only threshold candidates variant: real 0.3459 random min 0.5135 mean 0.5994 max 0.6678
per-seed max |sens95 diff| vs output/p2_knn_ETH.csv 0.0031250000000000444 |ap diff| 2.932870090244233e-05 n_test equal True R equal True
seeds with sens95 != published: {333: {'sens95': 0.5875, 'sens95_pub': 0.584375, 'thr': 0.3728139107347729, 'threshold_pub': 0.37514008675272226, 'spec': 0.95, 'spec_at_t_pub': 0.9505681818181818}}
seeds with threshold != published: [6, 21, 22, 35, 72, 116, 153, 199, 200, 210, 293, 333, 356, 357, 371] my spec there [0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.950624, 0.95] published spec [0.950581, 0.950562, 0.950575, 0.950568, 0.950556, 0.950556, 0.950575, 0.950568, 0.950568, 0.950575, 0.950575, 0.950568, 0.950556, 0.950057, 0.950562]
seeds with |AP diff| > 1e-12: 108
exact random mean: mine 0.60031782 published 0.60031001
real vs published: sens95 0.3496240602 vs 0.3496240602, ap 0.4169851972 vs 0.4169851972, thr 0.4835751364 vs 0.4835751364
ALT n 100 min 0.1799 mean 0.3259 max 0.4662
alt vs published (row order) max |diff| 0.0
```
Exact rational check (../work/panel_reproduce/exact_output.txt):
```
EXACT real sens95 93/266 = 0.3496240602 spec 0.9502732240 thr 51955930316/107441277275
EXACT random min 0.513514 mean 0.60031782 max 0.667774; all > real True
seeds where exact != published [333] [(0.5875, 0.584375)]
seeds where exact != my float checker []
```
Every headline number of CLAIM.md is confirmed by the definition, in floating point and in exact arithmetic: real 0.3496
(93/266), controls min 0.5135, mean 0.6003, max 0.6678, all 400 strictly above the real value, margin mean - real 0.2507,
min - real 0.1639. The secondary 100 alternative cluster-aware splits reproduce exactly (0.1799 / 0.3259 / 0.4662). The
prediction file result/predictions_ETH_knn10_split_v2_test.csv matches my per-isolate scores (max difference 2.2e-16),
nearest-TRAIN distances, phenotypes and calls (184 R calls at t = 0.48358). The control-split file
result/random_control_splits_test_rows.npz equals sorted default_rng(seed).choice(12287, 3073, replace=False) for every
seed 1..400.

(4) Determinism
- My checker run twice (two different memory-handling variants): ../work/panel_reproduce/my_random_controls.csv and
  my_random_controls_b.csv have the same sha256 (2a1f6fcb...0192); both regenerated split files hash 3b4ed122...0a56; all
  shared output lines identical.
- Author code: the 6 rows of output/smoke_p2_knn_ETH.csv (an earlier run of the same script) are identical, as strings,
  to the same rows of output/p2_knn_ETH.csv. The author's kNN uses argpartition on unique integer keys
  (distance * n + index), which is deterministic and equals the stable-sort tie rule.
- Not run: code/p2_knn.py (stated peak about 400 MB, above my 350 MB cap), code/make_split_v2.py and code/export_p2_artifacts.py
  (they would touch the whole memory map). My independent regeneration of split/split.csv and of both result/ files stands
  in for REPRODUCE.md steps 1 and 4; code/audit_split_v2.py needs run-1 files outside claim/ and was replaced by my own
  full-block TRAIN-TEST distance check.

## Mismatches

1. output/p2_knn_ETH.csv, random seed 333: sens95 is 0.584375 (threshold 0.37514, specificity 0.950568); the frozen
   definition gives 0.5875 (threshold 0.37281, specificity exactly 0.95, i.e. exactly 5% of test negatives at or above t,
   which "<= 0.05" admits). Confirmed in exact rational arithmetic. Cause (code/p2_knn.py, the same expression in
   code/export_p2_artifacts.py): `frac = 1.0 - np.searchsorted(neg, cand, side='left') / len(neg)` evaluates to
   0.05000000000000004 when the true fraction is exactly 0.05 (1 - 0.95 in binary floating point), so the rule acts as
   "< 0.05" at the boundary. It moves the threshold in 14 seeds (6, 21, 22, 35, 72, 116, 153, 199, 200, 210, 293, 333,
   356, 371) and changes sens95 in seed 333 only. In seed 357 the threshold also differs (0.40000 vs my 0.40040) through
   floating-point ties between equal scores; sens95 is unchanged there and my value agrees with the exact computation.
   The split-v2 value is not at the boundary (specificity 0.95027) and is unaffected. Effect on the claim: the random
   mean moves from 0.60031001 to 0.60031782; min, max, the 4-decimal mean, the margins and "all 400 above" are unchanged.
2. Average precision differs from mine by at most 2.9e-5 in 108 of 400 random seeds (floating-point ties between scores
   that are equal in exact arithmetic are broken differently by different summation orders). AP is reported alongside
   only; the real AP 0.4170 and the random AP range 0.5965-0.7395 match at the stated precision.
3. None in split/split.csv, the phenotype filter, the npz, the prediction file or the alternative splits.

## Process note (my own run, not the claim)

My first checker run peaked at 528 MB working set (mostly mapped file pages, map held open across blocks) and the exact
rational run at 719 MB working set (a 600,789-entry Fraction cache). Both broke the 350 MB cap. The second checker run,
which reopens the map per block, peaked at 204 MB working set. All three finished normally; I started no other process.

## Verdict

Every claimed number reproduces from the definition with independent code, the split is cluster-aware and regenerates
byte for byte, and the runs are deterministic. But output/p2_knn_ETH.csv, a file the claim releases, holds one per-split
metric (seed 333) that does not follow the frozen threshold rule, because of a floating-point boundary error in the released
code. Under "fail on any mismatch" this fails. The fix is to compute the fraction as count / len (or test 20 * count <= N
in integers) in code/p2_knn.py and code/export_p2_artifacts.py and regenerate output/p2_knn_ETH.csv. Seed 333 would then
read 0.5875, the random mean 0.60031782, and no headline figure changes.

pass: false
