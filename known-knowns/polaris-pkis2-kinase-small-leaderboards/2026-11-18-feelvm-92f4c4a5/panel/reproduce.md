context: subagent

# REPRODUCE skeptic verdict — claim `polaris/pkis2-lok-slk-c-1` (CLASS_LOK / CLASS_SLK)

## 1. The definition I was given (quoted from CLAIM.md, "Success criterion (bank entry, verbatim)")

> "Success means a saved prediction file (one prediction per official test row in official order;
> probabilities for classification; manifest with slug, sha256 of the downloaded table.parquet and
> the exact test index array from the public API) such that (a) the test rows are exactly the
> indices in the 'split' field of https://polarishub.io/api/v1/benchmark/polaris/<slug> and the
> label column is that benchmark's targetCols entry, (b) the skeptic's own computation of the
> benchmark's mainMetric is strictly better in that metric's direction than EVERY value listed in
> the live leaderboard table, re-fetched immediately before claiming, (c) the margin is at least 5%
> relative for MSE/MAE or 0.020 absolute for PR-AUC/ROC-AUC/balanced-accuracy, AND a
> 10,000-resample bootstrap over the 74-144 test rows puts the attacker ahead in at least 95% of
> resamples, (d) fitting used only the official train indices, with any multi-task borrowing
> restricted to OTHER kinases' train indices (declared, and checked to contain no test row of the
> target benchmark), and (e) no external PKIS or ChEMBL kinase-profiling record for a test
> compound-kinase pair was used; the PKIS data are public, so this must be verified by InChIKey,
> not assumed. A first entry on an EMPTY leaderboard is NOT a record and does not count."

Operative numbers fixed by the claim package: best listed CLASS_LOK pr_auc
0.2553191489361702 (the-record-we-beat.md, PNAModel), margin bar 0.2753191489361702
(best + 0.020), bootstrap seed 20261118 with 10,000 resamples of the 132 test rows
(PREREG.v3.md win rule 4, degenerate all-one-class resamples redrawn and disclosed).

## 2. What I did

I wrote my own checker from the definition above BEFORE opening REPRODUCE.md or
pipeline_lokslk.py. The checker reads only claim-folder files: table_v1.parquet,
bench_pkis2-lok-slk-c-1.json, preds.csv, official_inputs.json, the-record-we-beat.md,
null_test.md (labels are taken from the parquet itself, which I verified against
official_inputs.json rather than trusting it). I ran it twice with the provided venv
python; both runs printed identical output (deterministic). Only after it passed did I
read the author's REPRODUCE.md and pipeline_lokslk.py to compare (they agree; see §4).

## 3. Exact numbers from my own checker's real output (40/40 checks, quoted)

Manifest / official inputs — my own computation, parquet as ground truth:

- "[PASS] sha256(table_v1.parquet) equals official_inputs.json pin  --
  653d2b6f3013c7c6b54b15ee8093fa2ac7380319bf6525c47dd182f4b75c4306"
- "[PASS] sha256(bench json) equals official_inputs.json pin  --
  b7a58de2d71d52669e2558a7648e01fefc7b920fc7c3d99f281f81ded9c60858"
- "[PASS] bench split sizes are 508 train / 132 test  -- train=508 test=132"
- "[PASS] official_inputs train_index_array == bench split[0] exactly (order incl.)"
- "[PASS] official_inputs test_index_array == bench split[1] exactly (order incl.)"
- "[PASS] train/test disjoint; union is all 640 parquet rows  -- parquet rows=640"
- "[PASS] official_inputs.json 'labels' keys are exactly the 132 test indices  -- n_keys=132"
- "[PASS] official_inputs.json test labels match parquet read at positional index (132 rows)  --
  0 mismatches"
- "[PASS] test CLASS_LOK positives = 24/132  -- 24/132" and
  "[PASS] test CLASS_SLK positives = 13/132  -- 13/132"
- bench targetCols == ['CLASS_LOK','CLASS_SLK'], mainMetric == pr_auc, slug == pkis2-lok-slk-c-1.

Prediction file (the claimed object, preds.csv):

- "[PASS] preds.csv columns == ['row_index','CLASS_LOK','CLASS_SLK']"
- "[PASS] preds.csv has exactly 132 data rows  -- rows=132"
- "[PASS] preds row_index equals bench split[1] in exact order"
- "[PASS] all CLASS_LOK/CLASS_SLK probabilities in [0,1]"
- raw file carries full float precision (e.g. `4,0.01527530841048556,0.01428526194755736`),
  so the metric recomputation is not rounded-input-degraded.

Skeptic's own computation of the claimed metrics (sklearn average_precision_score /
roc_auc_score on the parquet labels at the official test positions):

- "  CLASS_LOK pr_auc        = 0.63433377092228493   claimed 0.634333770922"
- "  CLASS_LOK roc_auc      = 0.88020833333333326   claimed 0.880208333333"
- "  CLASS_SLK pr_auc       = 0.37785665913664424   claimed 0.377856659137"
- "  two-target mean        = 0.50609521502946464   claimed 0.506095215029"
- "[PASS] CLASS_LOK pr_auc == 0.634333770922  -- diff=2.849e-13"
- "[PASS] CLASS_LOK roc_auc == 0.880208333333  -- diff=3.333e-13"
- "[PASS] CLASS_SLK pr_auc == 0.377856659137  -- diff=3.558e-13"
- "[PASS] two-target mean == 0.506095215029  -- diff=4.646e-13"

Every claimed value is exactly my computed value rounded to its 12th decimal; the
residual diffs (< 5e-13) are pure rounding of the printed claims, not mismatches.
Rank-space recomputation (the Platt map in REPRODUCE.md has a=9.000716 and a=5.744524,
both > 0, so it is monotone and cannot change a ranking metric) gives identical values:
"rank-space CLASS_LOK pr_auc 0.634333770922285 roc_auc 0.880208333333333",
"rank-space CLASS_SLK pr_auc 0.377856659136644".

Margin and beat-every-listed-value rules:

- "[PASS] official_inputs listed_pr_auc_values equals the-record-we-beat.md six values"
- "[PASS] official_inputs bar == best listed 0.2553191489361702"
- "[PASS] CLASS_LOK pr_auc >= best+0.020 = 0.2753191489361702  --
  0.634333770922285 >= 0.275319148936170"
- "[PASS] CLASS_LOK pr_auc strictly above EVERY listed value  --
  min gap = 0.379015 over 6 entries"
- "[PASS] two-target mean pr_auc >= best+0.020 (robustness clause)  --
  0.506095215029465"

Bootstrap rule (10,000 resamples, numpy.random.default_rng(20261118), fraction with
CLASS_LOK pr_auc > 0.2553191489361702; required >= 0.95, claimed 1.000000). I ran it
under two independent draw methods to guard against stream-convention dependence:

- "  draw=rng.integers: CLASS_LOK ahead-fraction = 1.000000 (claimed 1.000000);
  mean-interpretation fraction = 0.999600 (claimed 0.999600); degenerate redraws = 0"
- "  draw=rng.choice: CLASS_LOK ahead-fraction = 1.000000 (claimed 1.000000);
  mean-interpretation fraction = 0.999600 (claimed 0.999600); degenerate redraws = 0"
- "[PASS] bootstrap (integers): claimed 1.000000 reproduces exactly  -- fraction=1.000000"
- "[PASS] bootstrap (choice): claimed 1.000000 reproduces exactly  -- fraction=1.000000"

Both the primary 1.000000 and the secondary 0.999600 claimed fractions reproduce
exactly, deterministically, with zero degenerate redraws.

Harness calibration (the required baseline/ run):

- My independent form: "constant-1 CLASS_LOK pr_auc = 0.18181818181818182
  (= 24/132 = 0.18181818181818182)", "constant-1 CLASS_SLK pr_auc =
  0.09848484848484848 (= 13/132 = 0.09848484848484848)", "constant-1 CLASS_LOK
  accuracy = 0.18181818181818182" — each matches a listed leaderboard null-model
  value bit-for-bit (the four constant all-positive entries in the-record-we-beat.md).
- I then ran baseline/lokslk_null_model.py itself. Its only hardcoded data-directory
  paths point outside the claim folder, which I may not open, so I ran a copy in which
  only those paths are repointed at the claim folder's own bench_pkis2-lok-slk-c-1.json
  and table_v1.parquet (files I had already sha256-verified against the
  official_inputs.json pins); no logic was changed. Its rerun output is line-for-line
  identical to baseline/lokslk_null_model_output.txt ("IDENTICAL: rerun output equals
  saved baseline/lokslk_null_model_output.txt line-for-line"), final line
  "BASELINE CALIBRATION: PASS".

Null-test controls (null_test.md):

- "[PASS] real CLASS_LOK pr_auc > best of 400 controls (0.607118)  -- 0.634334 > 0.607118"
- "[PASS] real CLASS_SLK pr_auc > best control (0.377647)  -- 0.377857 > 0.377647"
- "[PASS] real two-target mean > best control mean (0.369311)  -- 0.506095 > 0.369311"
- The raw 400-control values are not inside the claim folder; the binding comparison is
  against the recorded maxima, and the real fit beats the CLASS_LOK max by +0.027 and the
  mean max by +0.137 (the thin CLASS_SLK margin +0.00021 is disclosed in null_test.md
  itself, not hidden).

Final tally, quoted: "TOTAL: 40/40 checks passed" / "OVERALL: PASS" — identical on
both full runs of the checker.

## 4. Author artifacts, compared only after my checker passed

- REPRODUCE.md: its step-1 script reads the same files, makes the same structural
  assertions (132 rows, row_index == split[1] in order, probabilities in [0,1]), uses the
  same sklearn metrics, and the same bootstrap stream (default_rng(20261118),
  rng.integers, 10,000 resamples, redraw on all-one-class). Its expected outputs are
  exactly my numbers (0.634333770922 / 0.880208333333 / 0.377856659137 / 0.506095215029,
  margin True, bootstrap fraction 1.000000 with 0 redraws). It agrees with my checker;
  it did not replace it.
- baseline/lokslk_null_model.py: run as required (see §3) — PASS, output identical to
  baseline/lokslk_null_model_output.txt.
- pipeline_lokslk.py: fitting slices are `components(tr, te, cont_all[tr], cls_all[tr])`
  with tr = bench split[0] (the 508 official train rows); the Platt map is fitted on
  train-row OOF scores vs train labels; features come from SMILES only. This is
  consistent with the claim's fitting disclosure (train rows only; auxiliary use
  limited to the same train rows' continuous LOK/SLK columns). I did not execute it: it
  reads feature/auxiliary files outside the claim folder, which are outside what I may
  open, and retraining is unnecessary — the definition requires the saved prediction
  file to win, and it does. (Fitting-provenance and InChIKey-audit clauses (d)/(e) are
  other panelists' scope; nothing in the saved files contradicts them.)

## 5. Disclosure of one data-encoding detail

The official table encodes the class labels with a non-strict threshold: CLASS == (pct
>= 80) holds over all 640 rows for both targets (2 LOK rows and 1 SLK row sit exactly at
80 and are CLASS=1), while the README-style strict rule (> 80) does not. This is the
dataset's own encoding, applies identically to train and test, and cannot affect any
metric here: I score on the parquet's CLASS_LOK/CLASS_SLK columns (the benchmark's
targetCols) directly. The row-by-row threshold consistency over all 640 rows also rules
out any row misalignment between the parquet and the split indices.

## 6. Conclusion

Every property and every claimed number reproduces from the saved claim-folder files
with my own from-definition checker: the object is well-formed (one row per official
test index in exact split[1] order, probabilities in [0,1]), the four claimed metrics
match my recomputation to the claimed 12th decimal, the margin rule holds
(0.634333770922285 >= 0.2753191489361702), every listed leaderboard value is strictly
beaten (min gap 0.379015 over 6 entries), the seeded bootstrap gives ahead-fraction
1.000000 (and mean-interpretation 0.999600) under two independent draw methods with
zero degenerate redraws, the harness calibration reproduces the listed null-model
values exactly, and the real fit beats all 400 recorded label-permutation controls.
No mismatch, no missing object, no non-determinism found.

pass: true
