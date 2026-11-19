context: subagent

# CRITERION verdict — polaris/pkis2-lok-slk-c-1

Success criterion (CLAIM.md, verbatim): "Pick one named Polaris PKIS benchmark whose live leaderboard has at least one entry. Success means a saved prediction file (one prediction per official test row in official order; probabilities for classification; manifest with slug, sha256 of the downloaded table.parquet and the exact test index array from the public API) such that (a) the test rows are exactly the indices in the 'split' field of https://polarishub.io/api/v1/benchmark/polaris/<slug> and the label column is that benchmark's targetCols entry, (b) the skeptic's own computation of the benchmark's mainMetric is strictly better in that metric's direction than EVERY value listed in the live leaderboard table, re-fetched immediately before claiming, (c) the margin is at least 5% relative for MSE/MAE or 0.020 absolute for PR-AUC/ROC-AUC/balanced-accuracy, AND a 10,000-resample bootstrap over the 74-144 test rows puts the attacker ahead in at least 95% of resamples, (d) fitting used only the official train indices, with any multi-task borrowing restricted to OTHER kinases' train indices (declared, and checked to contain no test row of the target benchmark), and (e) no external PKIS or ChEMBL kinase-profiling record for a test compound-kinase pair was used; the PKIS data are public, so this must be verified by InChIKey, not assumed. A first entry on an EMPTY leaderboard is NOT a record and does not count."

## (a) Prediction file and manifest — MET

- preds.csv: 132 rows, columns exactly `row_index, CLASS_LOK, CLASS_SLK` = targetCols of the benchmark JSON; `row_index` equals the API `split[1]` array element-for-element in official order (my check: True); all values in [0,1] (True), no NaN (True).
- Manifest (official_inputs.json): slug `pkis2-lok-slk-c-1` matches the benchmark JSON slug; `test_index_array` == `split[1]` exactly and `train_index_array` == `split[0]` exactly (both True); pins the parquet sha256.
- I re-hashed the in-folder files myself: table_v1.parquet sha256 = 653d2b6f3013c7c6b54b15ee8093fa2ac7380319bf6525c47dd182f4b75c4306 (matches manifest and CLAIM.md bit-exact); benchmark JSON sha256 = b7a58de2d71d52669e2558a7648e01fefc7b920fc7c3d99f281f81ded9c60858 (matches its pin, so the split arrays in the package are the pinned API response).
- Split is a proper partition of the v1 table: 508 train + 132 test, disjoint (0 overlap), union = all 640 rows. Test positives: CLASS_LOK 24/132, CLASS_SLK 13/132; parquet labels equal the manifest label dict for all 132 test rows (both targets True).

## (b) Beats EVERY listed leaderboard value — MET

- My own recomputation (sklearn average_precision_score on the official test rows): CLASS_LOK pr_auc = 0.634333770922 (matches claim to 12 decimals), ROC = 0.880208333333, CLASS_SLK pr_auc = 0.377856659137, two-target mean = 0.506095215029.
- Six listed values (the-record-we-beat.md, consistent with the manifest's `listed_pr_auc_values`): 0.2553191489361702, 0.18181818181818182 (x4), 0.17394416607015034. My value beats every one strictly in the metric's direction (higher): gaps +0.379014621986 / +0.452515589 / +0.460389605; min gap +0.379014621986 > 0.
- Comparison-metric convention: the evidence table in the-record-we-beat.md shows all six result pages' listed pr_auc equal to their CLASS_LOK row exactly, so CLASS_LOK pr_auc is the listed metric; and the mean-interpretation robustness also clears (mean 0.506095215029 > 0.2553191489361702, gap +0.250776066093), so the win survives either reading of the multi-task board.
- Re-fetch before claiming is recorded (2026-11-18T16:04:25Z, HTTP 200, page sha256 5671da...58bc, same six entries as the earlier fetch). I judge this record within the package only; it is internally consistent.

## (c) Margin AND 10,000-resample bootstrap — MET

- Margin: 0.634333770922 − 0.2553191489361702 = +0.379014621986 absolute, far above the required +0.020 (also ~148% relative).
- Bootstrap recomputed by me with the frozen procedure (numpy default_rng(20261118), 10,000 resamples of the 132 test rows, degenerate all-one-class resamples redrawn): fraction of resamples with CLASS_LOK pr_auc > 0.2553191489361702 = 1.000000, with 0 degenerate redraws — matches the claim exactly and is >= 0.95.
- Mean-interpretation bootstrap (same procedure): 0.999600 >= 0.95, matching the claim's reported alternative; 132 test rows lies inside the criterion's 74-144 range.

## (d) Train-only fitting — MET (verified in the in-folder pipeline code)

- pipeline_lokslk.py: every fit uses only the 508 official train indices — ExtraTreesRegressor on X[train] with `cont_all[tr]`, LGBMClassifier on X[train] with `cls_all[tr]`, Platt/logistic on the train-row OOF blend scores vs `cls_all[tr]`; the test rows enter only as prediction inputs (X[te]) and the blend rank-normalizes test predictions only. No test-row label of any column (binary or continuous) is read anywhere on the fitting path.
- The declared auxiliary is the continuous LOK/SLK percent-inhibition columns of the same 508 train rows — no other-kinase borrowing exists, so the "OTHER kinases' train indices" restriction is not even triggered; the same-table auxiliary is sliced at train indices (`cont_all[tr]`) in the code.
- My own InChIKey recomputation from the pinned parquet: all 640 SMILES parse; 640 unique keys; 508 unique train keys / 132 unique test keys; train/test key overlap 0; even first-block (skeleton) overlap 0. The declared auxiliary is therefore physically incapable of containing a test-row label.
- Minor finding, no effect: PREREG.v3 paraphrases the label rule as "> 80% inhibition", but the official CLASS columns are exactly (continuous >= 80) — the 3 edge rows with value exactly 80.0 (2 LOK, 1 SLK) are labeled positive and all are train rows. Scoring used the official CLASS targetCols directly, so no computation is affected.

## (e) No external PKIS/ChEMBL test-pair record — MET (declared provenance cannot contain test labels)

- Declared provenance is only: the official pinned parquet (train-row labels; SMILES-derived features for all rows), the same table's continuous columns at train indices, and the benchmark's own API split. No external profiling record is declared or referenced by the pipeline.
- InChIKey audit recomputed by me: 640/640 unique keys, 0 train/test overlap, 0 skeleton-block overlap — a PKIS/ChEMBL lookup keyed on train compounds cannot return a test compound-kinase pair of this benchmark, and no such lookup exists in the declared pipeline. Features enter only as X (ECFP4 counts + RDKit descriptors, label-free by construction per the prereg); the feature matrices and the OOF npz live outside the claim folder so I could not byte-audit them, but the Platt map is monotone with the disclosed positive coefficients (a=9.000716, a=5.744524), so it cannot affect PR-AUC — the ranking that sets every claimed metric comes solely from components fitted on train-row labels.

## Trap clauses — RESPECTED

- Board NOT empty: six entries recorded (two fetch timestamps, page sha256, entry names), best listed 0.2553191489361702; this is not a first-entry-on-empty-board claim.
- v1/v2 confusion: the claim pins the v1 table sha256, applies the API split positionally to the v1 table, and the harness calibration validates that exact alignment — my own rerun of the constant all-positive predictor on the v1 table with the API split gives CLASS_LOK pr_auc 0.18181818181818182 (= 24/132), CLASS_SLK pr_auc 0.09848484848484848 (= 13/132), accuracy 0.18181818181818182 — bit-exact matches to the listed values of the four constant "baseline null model" entries (and to their CLASS_SLK result-page rows). A v1/v2 row-order mixup could not reproduce these numbers.

## Baseline / harness calibration and null_test.md controls — CHECKED

- Calibration is on the same data, split and metric as the claim (same pinned v1 parquet, same 508/132 API arrays, same sklearn pr_auc): BASELINE CALIBRATION reproduces PASS under my recomputation (three exact value matches above).
- Null test: 400 label-permutation controls recorded; real CLASS_LOK 0.634334 > best control 0.607118, i.e. beats all 400 by +0.027216, and the recorded real value equals my recomputed 0.634333770922 to 6 decimals. I could not rerun the 400 pipeline retrains (runner and feature matrices sit outside the claim package); the recorded summary is internally consistent (control mean 0.251396 sits at the prevalence scale of 24/132; the fat right tail is disclosed, not hidden) and the required condition "real beats all 400 controls" is met on those numbers. Two-target mean likewise beats its controls (0.506095 vs best 0.369311, +0.136784).
- CLASS_SLK beats its best control only narrowly (0.377857 vs 0.377647, +0.00021) — disclosed in null_test.md. This weakens any standalone SLK claim, but the claim as scoped rests on CLASS_LOK, the metric the live board lists, which clears its controls by +0.027216; the SLK thin margin therefore does not undermine the claim as scoped, and I do not treat it as one.

## Hidden quantifiers / stretched definitions — HUNTED

- "Pick one named Polaris PKIS benchmark ... at least one entry": satisfied by exactly this one cell (pkis2-lok-slk-c-1, six entries); the claim asserts nothing about other cells (prior reads on other cells appear only as disclosures).
- "EVERY value listed": all six checked individually, min gap +0.379014621986.
- The multi-task board's single-metric listing is handled under both readings (CLASS_LOK 0.634333770922 and mean 0.506095215029 both clear bar, margin and bootstrap: 1.000000 and 0.999600).
- CLASS_SLK and ROC appear in the claim only as reported numbers, which I reproduced exactly (0.377856659137; 0.880208333333); no wider record is asserted for them.
- Every number in the one-sentence claim reproduced to 12 decimals under my independent recomputation; nothing in the claim is wider than the evidence in the folder.

## Non-subsumption

The win is not subsumed: the board is non-empty (6 entries), the best real entry is beaten strictly by +0.379014621986 with bootstrap ahead-fraction 1.000000, the constant null-model entries sit at 0.18181818181818182, and the real value beats all 400 recorded permutation controls (best 0.607118). The bit-exact harness calibration rules out scorer/split/data misalignment on this exact cell.

confirmed_scope: On the official 132-row test split of the named benchmark polaris/pkis2-lok-slk-c-1, the saved prediction file (probabilities for CLASS_LOK/CLASS_SLK in official split order, manifest with slug, pinned parquet sha256 and exact test index array) achieves skeptic-recomputed CLASS_LOK pr_auc 0.634333770922 — strictly above all six listed leaderboard values (best 0.2553191489361702; margin +0.379014621986; ahead in 1.000000 of 10,000 bootstrap resamples) — fitted per the in-folder pipeline only on the 508 official train rows with the declared continuous LOK/SLK train-row auxiliary (recomputed InChIKey audit: 640 unique keys, 0 train/test overlap), with the harness calibration reproducing the listed null-model values bit-exactly and, per the recorded 400-control null test, the real value above every control (best 0.607118) — a genuine, non-subsumed win for this one cell only.

pass: true
