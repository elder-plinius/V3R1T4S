# Criterion skeptic: massbalancemachine-norway-test-glaciers-rmse, partial win p3

context: subagent (Claude Code Agent tool, fresh context)

## Binding text and my literal reading

Bank partial win p3 (checked against bank/targets.json, id massbalancemachine-norway-test-glaciers-rmse; CLAIM.md
quotes it exactly): "Reproduce MBM's three test RMSEs within 0.01 m w.e. from the shipped CSVs with an independent
re-implementation (validates the split and scorer)."

Read literally, it asks for all of these:
1. "MBM's three test RMSEs": Ba, Bw and Bs, all three, as MBM computed them. The only published source the bank names
   is the notebook 3.1.1 output (data/3.1.1_ML_model_performance_test.ipynb, cell 36): Ba 1.00 (Count 1065), Bw 0.59
   (Count 999), Bs 0.70 (Count 1028). The per-season record counts belong to the definition: an RMSE over a different
   set of records is a different quantity.
2. "within 0.01 m w.e.": |reproduced - published| <= 0.01 for each of the three. The published values are rounded to
   2 decimals, so I check two readings. (i) Against the printed numbers. (ii) Against every unrounded value the print
   allows: [0.995, 1.005), [0.585, 0.595), [0.695, 0.705). A pass has to hold under both.
3. "from the shipped CSVs": the inputs are the repository's feature-joined CSVs. No other data, and no observation from
   a test glacier in training.
4. "independent re-implementation": the pipeline that turns the CSVs into the three RMSEs is the claimant's own code,
   not the repository's scripts, notebooks or pickled objects. What it must cover is set by the parenthetical:
   "validates the split and scorer". So the split (14 test glaciers against the 18 training glaciers) and the scorer
   (monthly predictions summed per record, RMSE per season) must be the claimant's own. Retraining with MBM's
   published hyperparameters is within the text. Re-deriving those hyperparameters by cross-validation is not required,
   and so it is not validated either.

## What I checked (numbers copied from command output)

All Python ran as `python -I -B`, with at most 2 threads and one fit at a time. I unpickled nothing. The only booster I
loaded was the JSON file.

- Inputs: `sha256sum -c SHA256SUMS.txt` reported no mismatch. The three data hashes equal the constants in
  code/reimpl_p3.py and the hashes in baseline/README.md.
- Primary rerun (`code/reimpl_p3.py data <new dir> --nthread 2`): "train records {'annual': 2845, 'summer': 2901,
  'winter': 2752} | test records {'annual': 1065, 'summer': 1028, 'winter': 999} | test monthly rows 24913";
  "OUR MODEL on OUR test records: annual 0.9962 (n=1065) / winter 0.5881 (n=999) / summer 0.7001 (n=1028)";
  "P3_PASS: yes". The new test_record_predictions_primary.csv and model_primary.json are byte-identical (cmp) to the
  files in result/.
- Unrounded (result/result_primary.json): Ba 0.9962432769999511, Bw 0.5881431288741465, Bs 0.7000514608796857.
  - Reading (i), against the print: |diff| is 0.0038 / 0.0019 / 0.0001.
  - Reading (ii), worst case over the rounding intervals: at most 0.0088 / 0.0069 / 0.0051. Both readings pass.
- My own script, written separately and importing nothing from claim/code:
  - It builds records with a melt and string record keys, and its training input is the wide CSV with every row of
    the 14 test BREIDs removed (3064 of 4171 rows, 18 glaciers, 0 test RGIIDs left).
  - It has its own aggregated objective and trains with seed 23 and nthread 2.
  - It got 67909 training monthly rows (notebook 2.1.1 cell 9 prints 67909 for MBM) and the same test records,
    1065 / 999 / 1028.
  - Its predictions equal the claim's model exactly ("max |mine - claim| 0.0") and differ from the shipped MBM booster
    (data/custom_loss_best_model.json, xgboost 2.0.3, 300 trees, 11 features) by at most 3.58e-07 per monthly row.
  - Scored my own way on the shipped test CSV (grouped by its id), my retrain, the claim's model and the shipped
    booster each give:

    | season | n | RMSE | MSE | MAE | bias | R2 |
    |---|---|---|---|---|---|---|
    | Ba | 1065 | 0.9962 | 0.9925 | 0.7705 | -0.0123 | 0.6351 |
    | Bw | 999 | 0.5881 | 0.3459 | 0.4635 | -0.0122 | 0.6633 |
    | Bs | 1028 | 0.7001 | 0.4901 | 0.5384 | +0.0361 | 0.7193 |

    Rounded to 2 decimals, all 15 statistics equal cell 36's line: RMSE 1.00/0.59/0.70, MSE 0.99/0.35/0.49, MAE
    0.77/0.46/0.54, bias -0.01/-0.01/0.04, R2 0.64/0.66/0.72. The shipped booster scored on the claim's records
    differs from the claim's retrain by 4.0e-08 / 7.1e-09 / 1.1e-08 in RMSE.
  - A plain scorer on result/test_record_predictions_primary.csv gives 0.996243 / 0.588143 / 0.700051 over
    1065 / 999 / 1028 rows.
- Split: the 14 BREIDs in code/reimpl_p3.py match notebook 2.1.1 cell 4 ("test_glaciers = [54, 703, ...]"). They map
  one-to-one to the bank's 14 RGIIDs ("test RGIIDs from BREID list == bank list: True"). The shipped test CSV has
  exactly those BREIDs and RGIIDs. Training rows hold 0 test RGIIDs, and 0 stake (utm_east, utm_north) positions are
  shared between test and training rows. The features are only climate and topographic columns, with no mass-balance
  or geodetic input. I found no path by which a test-glacier observation enters training.
- Test cleaning rule: it is the repository's own rule, from notebook 2.1.1 cell 5 ("# Remove strange value /
  df_test_winter = df_test_winter[df_test_winter['balance_winter'] != 9.99]"). In code/reimpl_p3.py it applies only
  where BREID is a test BREID.
  - It drops exactly 1 record (notebook 2.1.1 cell 4 printed 1000 test winter records; cell 36 counts 999).
  - The wide CSV has 9.99 winter values: test 1, train 0. Applying the rule to test only therefore changes nothing in
    training.
  - The rule is needed for n 999: supporting/lens2_output.txt shows that keeping the record gives Bw 0.6529 (n=1000),
    which fails.
- Records built from the CSVs: check (a) shows the record targets equal the shipped test CSV per season. Spot rows
  match what notebook 3.1.1 printed, for example id 0 BREID 54 2013 -6.24 (summer), id 1028 1.32 (winter),
  id 2027 -4.92 and id 3091 -3.29 (annual).
- Null models and discrimination:
  - A zero prediction gives 1.8804 / 2.3378 / 3.3397 and record-shuffled predictions give 2.2177 / 1.4065 / 1.7934.
    Both fail the tolerance (rerun output).
  - supporting/lens2_output.txt: 0 of 24 configurations of MBM's notebook-2.1.1 grid land within 0.01 of all three
    values, and tree_method exact misses (1.0476 / 0.6075 / 0.7021).
  - So the 0.01 tolerance on 2-decimal numbers is not loose enough to be met by chance.
  - The claimant saw the numbers in an earlier run (PREREG.md says so). That does not matter here: there is no free
    choice left to tune, since the configuration is MBM's published one and my independent rerun with a different
    seed and thread count is bit-identical.
- Baseline record (baseline/README.md):
  - It uses the same data (the same three sha256 values), the same split (the 14 BREIDs) and the same metric (RMSE
    over point records per season, with monthly predictions summed per record).
  - Its expected values are the published 1.00 / 0.59 / 0.70 with n 1065 / 999 / 1028, the same as the claim.
  - Its "shipped booster, our scorer" column (0.9962 / 0.5881 / 0.7001) matches my own scoring of that booster.
- Independence, from reading code/reimpl_p3.py:
  - Its imports are argparse, csv, hashlib, json, math, os, sys, numpy, pandas and xgboost. Nothing comes from the
    repository, and no .pkl file is read.
  - Its own code covers record building, the split, the objective, the training call and the scorer.
  - Shared with MBM: the xgboost library; MBM's selected hyperparameters (notebook 2.1.1 cell 52: max_depth=5,
    learning_rate=0.05, n_estimators=300, gamma=0, min_child_weight=0); base_score 0.5, read from the shipped booster
    JSON (lens2 shows leaving it unset changes nothing at 4 decimals); the 11 feature names; and MBM's record
    conventions, which define the target quantities.
  - That is independent enough to validate the split and the scorer, which is what the parenthetical names.
    - The split: a model trained only on the 18 training glaciers' rows reproduces MBM's shipped booster to 3.6e-07
      per monthly row. This also supports, indirectly, that MBM's training input excluded the test glaciers. The
      package does not include MBM's scripts/, so I could not read MBM's own training code directly.
    - The scorer: monthly predictions summed per record and RMSE per season reproduce all 15 printed statistics.
  - What it does not validate is MBM's cross-validated hyperparameter selection.

## Hidden quantifiers and wording

- "within 0.01": holds under both the rounded and the unrounded reading, for all three seasons, over the exact counts.
- "three test RMSEs": all three are reproduced. None is dropped or substituted.
- "from the shipped CSVs": holds for both the wide CSV used to build records and train, and the monthly test CSV used
  to score.
- The one-sentence claim says "shared only the xgboost 3.2.0 library and MBM's selected hyperparameters". That leaves
  out base_score 0.5 (taken from the shipped booster), the 11 feature names and MBM's record conventions, although the
  body of CLAIM.md lists them. This is a looseness of wording that does not change the result. The confirmed_scope
  below states the sharing exactly.
- The claim limits itself to p3 ("nothing wider") and claims nothing on p1, p2 or the full criterion. It does not
  subsume, and is not subsumed by, any other win named in the entry.

confirmed_scope: Code of the claimant's own (record building from the shipped ML_MB_Norway CSVs at commit 32d8175, the 14-BREID test split, the repository's test-only 9.99 winter-record rule, the summed-monthly aggregated-MSE objective and the per-season record scorer), retrained only on the 18 training glaciers with xgboost 3.2.0, MBM's published hyperparameters and base_score 0.5, gives test RMSEs Ba 0.9962 (n 1065), Bw 0.5881 (n 999) and Bs 0.7001 (n 1028) m w.e., within 0.01 of notebook 3.1.1's printed 1.00 / 0.59 / 0.70 and within 1e-7 of the shipped MBM booster scored the same way, which meets bank partial win p3 and nothing wider (not p1, p2, the full criterion or MBM's hyperparameter selection).

pass: true
