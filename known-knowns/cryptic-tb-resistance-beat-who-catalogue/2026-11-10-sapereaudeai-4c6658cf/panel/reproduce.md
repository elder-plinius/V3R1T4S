# REPRODUCE skeptic, panel round 2: p2 leakage claim (ETH, 10-NN on SNP distances)

context: subagent (Agent tool, subagent_type reproduce, round 2)

Started 12:11:13 UTC (date -u). Read only: CLAIM.md, REPAIR.md, REPRODUCE.md, EXTERNAL_INPUTS.md, PREREG.md (+ PREREG.v2.md,
PREREG.v3.md), null_test.md and the data/result/output/split files they name. I did not read the author's code
(code/*.py) and did not run code/p2_knn.py. My checker is ../work/panel2_reproduce/check.py (relative to claim/;
sha256 e573daffd804bc0e6743d73f7852f5a117a3214d7cc0f54890bb3981b6e3d4b4), written from the definitions below. Logs:
../work/panel2_reproduce/run1.log and run2.log.

## Definitions my checker implements (quoted from PREREG.md)

Split v2: "link two reuse isolates when their released SNP distance is <= 12 ...; clusters are the connected components
(single linkage) with no hub removal, so no TRAIN isolate is within 12 SNPs of any TEST isolate. Components larger than
614 isolates (5%) go to TRAIN whole ... The other components are ordered by sha256('V3R1T4S-cryptic-split-v2|' +
smallest UNIQUEID in the component) and go whole to TEST until TEST first holds >= 3,072 isolates (25%)."

Phenotype filter: "Primary: <DRUG>_PHENOTYPE_QUALITY == HIGH and phenotype in {R, S} ('I' excluded)."

p2: "Model (fixed, no tuning): genome-wide k-nearest-neighbour on the released SNP distances. For a test isolate, take
the k = 10 nearest training isolates among those with a HIGH-filter R/S phenotype for the drug (stable sort by
distance, ties by matrix index); score = sum(w_j * R_j) / sum(w_j), w_j = 1 / (1 + d_j).
- Metric: sensitivity at >= 95% specificity on the test part: threshold t = the smallest score value such that the
fraction of test negatives with score >= t is <= 0.05; sensitivity = fraction of test positives with score >= t."
"Controls: 400 random isolate-level splits with the same TEST size (3,073 of 12,287), numpy seeds 1..400. Leakage is
demonstrated only if every one of the 400 random-split metrics is strictly greater than the split-v2 metric".

Implementation notes (mine): the threshold test is done in integers (20 * #neg(score >= t) <= #neg); candidate t =
every distinct score value on the test part (primary reading), and separately negative scores only (alternative reading,
reported below). Neighbours: exact top-10 by the integer key distance * n_train + position (train columns kept in matrix
index order), so ties go to the lower matrix index; weights summed in neighbour order in float64. Components by my own
union-find over all reuse-pair entries <= 12 read in 256-row memory-mapped blocks. Random splits regenerated as
np.sort(np.random.default_rng(seed).choice(12287, 3073, replace=False)). AP computed with tied scores grouped.

## What I recomputed and what my code printed (run 2, pasted)

Distance matrix sha256 (sha256sum): 02d7cd4602a0bc900448f0fb290cf958a3b2c834f0bd878ca880af91eedef5dd (= EXTERNAL_INPUTS.md).
split/split.csv sha256 (sha256sum): 3b4ed12292c1804bdd5e226c72e233eacf1be780f8432656e292e1d225640a56 (= CLAIM.md).

```
[   0.0s] labels 15228 unique 15228
[   0.0s] split rows 12287 unique 12287
[   0.0s] split v2 TEST 3073 TRAIN 9214 values ['test', 'train']
[   0.1s] reuse rows 12287 same order as split.csv: True
[   0.1s] ETH quality counts {'HIGH': 8820, 'MEDIUM': 1354, 'LOW': 1956, 'NA': 157}
[   0.1s] ETH phenotype counts {'S': 9431, 'I': 972, 'R': 1727, 'NA': 157}
[   0.1s] ETH HIGH x phenotype {('HIGH', 'S'): 7062, ('HIGH', 'I'): 569, ('HIGH', 'R'): 1189}
[   0.1s] ETH phenotyped (HIGH, R/S) 8251 R 1189 S 7062
[   1.7s] scan done: negative entries 0 nonzero diagonal 0 edges<=12 (upper) 43016 ok 1 ws 38.6 MB peak_ws 59.2 MB
[   1.7s] min distance TRAIN row->TEST col 13 TEST row->TRAIN col 13
[   1.7s] components 7420 singletons 6399 largest [2539, 72, 48, 38, 35]
[   1.8s] components > 5% to TRAIN [2539] threshold 0.05*N = 614.35 TEST target 0.25*N = 3071.75
[   1.8s] my TEST 3073 equal to split.csv SPLIT column: True
[   1.8s] CLUSTER column equals 'C'+smallest UNIQUEID of my component: True
[   1.8s] regenerated split csv (newline '\n') sha256 3b4ed12292c1804bdd5e226c72e233eacf1be780f8432656e292e1d225640a56
[   2.4s] submatrix (8251, 8251) int16 min 0 symmetric True ok 1 ws 175.0 MB peak_ws 204.1 MB
[   2.4s] author rows Counter({'random': 400, 'alt_cluster_aware': 100, 'real_split_v2': 1})
[   2.7s] REAL split v2: {'sens_all': 0.34962406015037595, 'sens_neg': 0.3458646616541353, 'spec': 0.9502732240437158, 't': 0.48357513642561073, 'ap': 0.4169851972238189, 'n': 2096, 'R': 266} mismatches [] AP diff 0
[   2.7s] predictions file rows 2096 same isolate set: True
[   2.7s] pred score max abs diff 2.220446049250313e-16 nearest-dist equal True phenotype equal True calls equal (score>=t ->R) True calls values {'notR': 1912, 'R': 184} min nearest 13
[   2.8s] npz {'test_rows': (400, 3073), 'seeds': (400,)} seeds 1 400 sorted rows True
[ 104.3s] npz splits equal to default_rng(seed).choice sorted: 400 / 400
[ 104.4s] RANDOM: n 400 min 0.5135 mean 0.6003 max 0.6678 all > real: True count above 400 margin mean-real 0.2507 min-real 0.1639
[ 104.4s] per-split sens95 mismatches vs author 0 ; splits where neg-only candidate set differs 65
[ 104.4s] AP diff vs author: max abs 2.93e-05
[ 104.4s] seed 333: 0.5875
[ 104.4s] neg-only candidate reading: real 0.3459; random min 0.5135 mean 0.5994 max 0.6678; all above real True
[ 104.4s] done ok 1 ws 181.8 MB peak_ws 230.8 MB
```

Per-split comparison with output/p2_knn_ETH.csv: for the real row and all 400 random rows, my sens95 and spec_at_t equal
the author's values exactly (float equality), the threshold agrees within 1e-12, and n_test / R_test agree; 0
mismatches in 401 rows. A follow-up comparison printed:
`AP differing seeds 71 max 2.932870090244233e-05` and `round1 vs current sens95 differing seeds ['333']`.

## Results by check

1. Split: sha256 matches; the rule regenerates split/split.csv byte for byte from the distances alone (my file has the
   same sha256 and `cmp` reports it identical); 7,420 components, 6,399 singletons, one 2,539-isolate component sent to
   TRAIN, TEST 3,073 / TRAIN 9,214, as stated. Cluster-aware: the minimum distance between any TRAIN and any TEST isolate
   is 13 in both directions (no TRAIN isolate within 12 SNPs of a TEST isolate); 0 negative entries, zero diagonal.
2. kNN / metric: real split v2 sens95 = 0.34962406015037595 (= 93/266 R isolates; 2,096 phenotyped TEST isolates),
   specificity at t 0.9503, t = 0.48357513642561073. The 400 saved control splits equal default_rng(seed).choice
   sorted for seeds 1..400 (400/400). Controls: min 0.5135, mean 0.6003, max 0.6678, all 400 strictly above 0.3496;
   margin mean - real 0.2507, min - real 0.1639. All equal the claim and every per-split value in output/p2_knn_ETH.csv.
   Seed 333 is 0.5875, the repaired value; the only seed that differs from the superseded round-1 file.
   result/predictions_ETH_knn10_split_v2_test.csv: same 2,096 isolates, scores within 2.2e-16 of mine, identical nearest
   TRAIN distances (minimum 13) and phenotypes, and CALL = R exactly when score >= t (184 R calls).
3. Phenotype filter: ETH_PHENOTYPE_QUALITY == HIGH and ETH_BINARY_PHENOTYPE in {R, S} gives 8,251 isolates (1,189 R,
   7,062 S; 569 HIGH 'I' excluded), matching the log's "phenotyped isolates 8251 R 1189". The reuse table row order
   equals split/split.csv row order, so the control row indices address the right isolates.
4. Determinism: two complete runs of my checker produced byte-identical per-seed results (my_random.csv), real-split
   scores (my_real_scores.npy) and regenerated split file. The author's file agrees exactly with my independent code on
   all 401 sens95 values, which also shows their run is deterministic for these numbers.

Not checked: the 100 alternative cluster-aware splits (secondary, not part of the claim); the author's code was not run.

## Observations (not mismatches of the claim)

- Threshold candidate set: PREREG.md says "the smallest score value"; the author (and my primary reading) take any
  test score value. If only negative-score values are candidates, the real value is 0.3459 instead of 0.3496 and 65
  of 400 controls change (min 0.5135, mean 0.5994, max 0.6678); all 400 controls are still above the real value, so
  the conclusion does not depend on this reading, but the headline number 0.3496 does.
- Average precision: equal on the real split (0.4169851972238189); on 71 of 400 random splits my AP (tied scores
  grouped) differs from the author's by at most 2.93e-05, consistent with tie handling or 1-ulp score differences
  between mathematically equal scores. AP is reported alongside only and is not part of the claim.

## Measured peak memory

Peak working set 230.8 MB (K32GetProcessMemoryInfo PeakWorkingSetSize of my process, run 2), under the 300 MB cap.
4 threads (OMP/OPENBLAS/MKL_NUM_THREADS=4), one process at a time. (Run 1's memory line read 0.0 MB because of a ctypes
bug in my probe; fixed for run 2.)

## Mismatches

None. Every checked property and every claimed number reproduced exactly with independently written code.

pass: true
