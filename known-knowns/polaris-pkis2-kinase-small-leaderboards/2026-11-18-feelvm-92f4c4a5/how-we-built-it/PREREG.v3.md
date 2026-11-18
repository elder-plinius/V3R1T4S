# PREREG.v3 — new cell polaris/pkis2-lok-slk-c-1, frozen 2026-11-18T15:10Z (before any test scoring on this cell)

A new frozen rule for a new cell of the same bank target. It does not alter `PREREG.md` or `PREREG.v2.md`.

## Cell

`polaris/pkis2-lok-slk-c-1`, multi-task classification, targetCols `["CLASS_LOK", "CLASS_SLK"]`
(threshold > 80% inhibition per the benchmark README), mainMetric `pr_auc`, official train 508 / test
132 rows from the benchmark API `split` field, dataset `polaris/kinase-pkis2-1` (v1 table,
sha256 653d2b6f3013c7c6b54b15ee8093fa2ac7380319bf6525c47dd182f4b75c4306, same 640 compounds as the v2
table, different row order; rows mapped by canonical SMILES, all 640 unique).

**Live leaderboard convention (verified from all six result pages, 2026-11-18T15:0xZ):** the listed
`pr_auc` value of every entry equals its CLASS_LOK row exactly (0.2553191489361702, 0.18181818181818182
x4, 0.17394416607015034). The comparison metric is therefore CLASS_LOK pr_auc; the two-target mean is
reported as a robustness check against the mean-interpretation.

## Bars (live page fetched 2026-11-18T13:5xZ, one honest GET)

Best listed CLASS_LOK pr_auc = **0.2553191489361702** (DGLGraphTransformer_PNAModel); others 0.18181818181818182
(MPNN/GCN/GAT/pharm2D_FC) and 0.17394416607015034 (AttentiveFP). Best listed ROC (CLASS_LOK) = 0.6759259259259259.

## Win rule (all must hold)

1. The prediction file has 132 rows aligned to the official `split[1]` order with probabilities in [0,1]
   for both targets; manifest records slug, parquet sha256 and the exact test index array.
2. Our CLASS_LOK pr_auc is strictly above every listed pr_auc value, re-fetched immediately before the claim.
3. Margin: our CLASS_LOK pr_auc >= 0.2553191489361702 + 0.020 = 0.2753191489361702.
4. Bootstrap: 10,000 resamples (`numpy.random.default_rng(20261118)`) of the 132 test rows; the fraction
   with CLASS_LOK pr_auc > 0.2553191489361702 must be >= 0.95. Degenerate resamples (all-one-class for a
   target) are redrawn and the count disclosed.
5. Robustness clause (mean-interpretation): the two-target mean pr_auc must also be >= 0.2753191489361702
   and its bootstrap fraction above 0.2553191489361702 must be >= 0.95. This is reported alongside the
   primary; a failure of only this clause is disclosed and the claim is scoped to the listed convention.

## Frozen recipe (E2, per target T in {LOK, SLK}; deterministic seeds)

- Features X: ECFP4 counts (2048) + 18 RDKit physchem descriptors from SMILES (no labels involved).
- Component A: ExtraTreesRegressor(n_estimators=800, max_features=0.1, min_samples_leaf=1,
  random_state=0, n_jobs=8) trained on the continuous percent-inhibition label of T over the 508
  official train rows. (Declared auxiliary use of the same table's continuous column, train rows only.)
- Component B: LGBMClassifier(n_estimators=400, learning_rate=0.05, num_leaves=15, min_child_samples=10,
  random_state=0) trained on CLASS_T over the 508 official train rows.
- Blend: rank-normalise each component's 132 test predictions to [0,1] and average.
- Probability output: Platt scaling (logistic regression) fitted on the 10-partition out-of-fold blend
  scores of the 508 train rows vs CLASS_T; the map is monotone, so PR-AUC/ROC are invariant to it.
- Train-only CV of this recipe (10 scaffold-grouped partitions): CLASS_LOK PR-AUC 0.6744 +- 0.0298,
  CLASS_SLK 0.3519 +- 0.0393, LOK ROC 0.87. Selection used only these train-only numbers.

## Fitting rules

- Only the 508 official train indices. No test-row label of any column (continuous or binary) enters any
  fit, the Platt map, the blend, or feature building.
- The only auxiliary data are the continuous LOK/SLK columns of the same official train rows (declared).
  No external PKIS/ChEMBL record is used; features come from SMILES only.
- Test-read budget on this cell: **one** read of the frozen prediction file. Baseline and null reads are
  counted and disclosed separately below.

## Baseline (step 3c)

No entry on this cell publishes code or predictions: the six listed entries are Polaris "baseline null
model" submissions with "No references provided" and no links (checked on the benchmark page and every
result page, 2026-11-18). Four of the six listed entries are constant all-positive predictors, whose
published values are therefore reproducible exactly from the definition: a constant probability 1.0
prediction must give CLASS_LOK pr_auc = 24/132 = 0.18181818181818182, CLASS_SLK pr_auc = 13/132 =
0.09848484848484848, accuracy = 24/132 = 0.18181818181818182. Reproducing those listed values bit-for-bit
with the official split and our scorer calibrates the harness on this exact cell (same data, split,
metric). The non-trivial best entry (PNA, 0.2553191489361702) has no released predictions and is compared
by its listed value only.

## Null test

400 controls: the same frozen E2 pipeline retrained with the training labels permuted (per control id:
one RNG seed; the continuous LOK/SLK labels and the CLASS_LOK/CLASS_SLK labels are each independently
permuted over the 508 train rows). Each control is scored on the official 132 test rows; the real
CLASS_LOK pr_auc must exceed all 400 control CLASS_LOK pr_aucs (and the real mean likewise). `null_test: required`

## Disclosure

- Prior test reads on OTHER cells of this target (KIT v2 regression and KIT v2 classification, one frozen
  candidate each) are reported in `attempts/final-frozen/report.md` and `attempts/p3-kit-cls/report.md`;
  no value from those reads entered this cell's model or selection.
- Model selection for this cell used train-only scaffold-grouped CV over 10 stable partitions.
