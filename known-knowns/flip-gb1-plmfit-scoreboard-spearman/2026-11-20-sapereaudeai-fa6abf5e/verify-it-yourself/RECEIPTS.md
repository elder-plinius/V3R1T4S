# Receipts: the checker's real output

Two runs, both from the package folder, on 2026-11-20. Python 3.11 on Windows (Git Bash), standard library only,
no network. Both end in `PASS`. The second adds check group 9 by pointing `GB1_CSV` at the released file.

## What this checker cannot do

- **It cannot refit the models.** Group 9 only proves the shipped predictions expand to exactly the files the
  run's REPRODUCE panellist verified. `RUN_IT_YOURSELF.md` section 3 refits them.
- **It cannot re-run the leakage test.** It only confirms that the package records byte-identical prediction
  files from a refit with every test score replaced by `nan`. Re-running it needs the released file and is step 4
  of `RUN_IT_YOURSELF.md`.
- **It cannot check novelty, and it does not fetch the scoreboard.** `the-record-we-beat/record.md` holds the
  snapshot with its fetch time, HTTP status and page sha256.
- **It cannot quantify configuration-selection noise.** The configuration was chosen in an earlier run; the only
  interval here is over test-sequence sampling.
- **It cannot verify the ProtEGNN comparator.** Those figures were read at source by a human, not fetched by a
  program; `../how-we-built-it/baseline/published-values-RESOLVED-by-operator.md` says so and says what a future
  run should re-verify.

## The corrupted-copy test

The repository's own `check_run.py --package` copies this package, flips a digit in a text file of `object/`, and
requires `run_checks.sh` to exit non-zero with a last line of exactly `FAIL`. Check group 1 is what makes that
happen: the sha256 of the changed file stops matching, the checker prints its failure and ends with `FAIL` and
nothing after it.

## Run 1: offline, no arguments

```
Checker for partial win p2, bank target flip-gb1-plmfit-scoreboard-spearman.
Python standard library only; no network; object/ is the only input.

1. object/ integrity
  ok   predictions_A.csv sha256 matches
  ok   predictions_B.csv sha256 matches
  ok   run_output.txt present (3743 bytes, sha256 ae2a6e25f1312a1cdf42503e148a553fe137bba90260cd4625ed29703aac7c1e)
  ok   scored_pairs.csv sha256 matches
  ok   summary.json sha256 matches
  ok   no unexpected files in object/

2. the scored set
  ok   all three tables carry the same 5743 keys in the same order
  ok   5743 distinct keys, no duplicates, none missing
  ok   every key is four letters of ACDEFGHIKLMNPQRSTVWY (sites 39, 40, 41, 54)
  ok   every prediction and every score is finite
  ok   the score column takes 4683 distinct values

3. the claimed Spearman of each configuration, recomputed from object/ alone
  ok   configuration A: recomputed Spearman 0.902852, matches summary.json
  ok   configuration B: recomputed Spearman 0.897451, matches summary.json

4. the Spearman implementation, on a known positive and a known negative
  ok   known positive (predictions = scores):  +1.000000
  ok   known negative (predictions = -scores): -1.000000

5. the three seeds, the mean and the standard deviation
  ok   configuration A: seeds [1, 2, 3], mean 0.902852, sd(ddof=0) 0.000000
  ok   configuration A: standard deviation is exactly 0, as summary.json states; summary.json also records 1 distinct prediction-file sha256 per configuration, which is the reason - the configuration is an input, so nothing in the fit is random
  ok   configuration B: seeds [1, 2, 3], mean 0.897451, sd(ddof=0) 0.000000
  ok   configuration B: standard deviation is exactly 0, as summary.json states; summary.json also records 1 distinct prediction-file sha256 per configuration, which is the reason - the configuration is an input, so nothing in the fit is random
  ok   the determinism statement is present and machine-readable

6. this checker's own bootstrap of the mean, 2000 resamples, seed 20261120
  ok   configuration A, mean's 95% interval here: [0.898260, 0.907084]
       the claim's own interval, 10,000 resamples under seed 0: [0.898044, 0.907247]
  ok   the two intervals agree to better than 0.002 at both endpoints

7. partial win p2, its two conditions
  ok   three-seed mean 0.902852 strictly above the scoreboard value 0.879100: True (margin +0.023752)
  ok   the mean's bootstrap 95% interval excludes 0.879100 (lower bound 0.898260): True
  ok   p2 MET: True

8. the full success criterion - reported, NOT claimed by this package
       mean >= scoreboard + 0.02 = 0.8991 : True
       mean >  highest published value 0.8995 +- 0.0058 : True (margin +0.003352)
       the mean's interval [0.898260, 0.907084] excludes 0.8995 : False
       -> the margin over the published value is smaller than that value's own
          uncertainty and the interval does not exclude it, which is why this
          package claims p2 and not the full criterion.  See README.md, Not claimed.

9. optional: rebuild the keys, the scores and the full-sequence prediction files
       SKIPPED: set GB1_CSV to the released gb1_data_full.csv to run this group.

10. what this checker cannot do
    - It cannot refit the models; group 9 only proves the shipped predictions are the
      ones the panel verified. RUN_IT_YOURSELF.md refits them.
    - It cannot check the leakage test, only that the package records byte-identical
      prediction files from a refit with every test score replaced by nan; re-running
      that test needs the released file and is step 4 of RUN_IT_YOURSELF.md.
    - It cannot check novelty, and it does not fetch the scoreboard. the-record-we-beat/
      holds the snapshot with its fetch time and HTTP status.
    - It cannot quantify configuration-selection noise: the configuration was chosen in
      an earlier run and the only interval here is over test-sequence sampling.

0 check(s) failed.
PASS
```

## Run 2: with the released file supplied, so check group 9 runs

```
Checker for partial win p2, bank target flip-gb1-plmfit-scoreboard-spearman.
Python standard library only; no network; object/ is the only input.

1. object/ integrity
  ok   predictions_A.csv sha256 matches
  ok   predictions_B.csv sha256 matches
  ok   run_output.txt present (3743 bytes, sha256 ae2a6e25f1312a1cdf42503e148a553fe137bba90260cd4625ed29703aac7c1e)
  ok   scored_pairs.csv sha256 matches
  ok   summary.json sha256 matches
  ok   no unexpected files in object/

2. the scored set
  ok   all three tables carry the same 5743 keys in the same order
  ok   5743 distinct keys, no duplicates, none missing
  ok   every key is four letters of ACDEFGHIKLMNPQRSTVWY (sites 39, 40, 41, 54)
  ok   every prediction and every score is finite
  ok   the score column takes 4683 distinct values

3. the claimed Spearman of each configuration, recomputed from object/ alone
  ok   configuration A: recomputed Spearman 0.902852, matches summary.json
  ok   configuration B: recomputed Spearman 0.897451, matches summary.json

4. the Spearman implementation, on a known positive and a known negative
  ok   known positive (predictions = scores):  +1.000000
  ok   known negative (predictions = -scores): -1.000000

5. the three seeds, the mean and the standard deviation
  ok   configuration A: seeds [1, 2, 3], mean 0.902852, sd(ddof=0) 0.000000
  ok   configuration A: standard deviation is exactly 0, as summary.json states; summary.json also records 1 distinct prediction-file sha256 per configuration, which is the reason - the configuration is an input, so nothing in the fit is random
  ok   configuration B: seeds [1, 2, 3], mean 0.897451, sd(ddof=0) 0.000000
  ok   configuration B: standard deviation is exactly 0, as summary.json states; summary.json also records 1 distinct prediction-file sha256 per configuration, which is the reason - the configuration is an input, so nothing in the fit is random
  ok   the determinism statement is present and machine-readable

6. this checker's own bootstrap of the mean, 2000 resamples, seed 20261120
  ok   configuration A, mean's 95% interval here: [0.898260, 0.907084]
       the claim's own interval, 10,000 resamples under seed 0: [0.898044, 0.907247]
  ok   the two intervals agree to better than 0.002 at both endpoints

7. partial win p2, its two conditions
  ok   three-seed mean 0.902852 strictly above the scoreboard value 0.879100: True (margin +0.023752)
  ok   the mean's bootstrap 95% interval excludes 0.879100 (lower bound 0.898260): True
  ok   p2 MET: True

8. the full success criterion - reported, NOT claimed by this package
       mean >= scoreboard + 0.02 = 0.8991 : True
       mean >  highest published value 0.8995 +- 0.0058 : True (margin +0.003352)
       the mean's interval [0.898260, 0.907084] excludes 0.8995 : False
       -> the margin over the published value is smaller than that value's own
          uncertainty and the interval does not exclude it, which is why this
          package claims p2 and not the full criterion.  See README.md, Not claimed.

9. optional: rebuild the keys, the scores and the full-sequence prediction files
  ok   GB1_CSV sha256 matches the pinned released file
  ok   the object's keys are exactly the split's test rows, in file order: True
  ok   the object's score column is exactly the released score column for those rows: True
  ok   configuration A expands to the full-sequence prediction file the REPRODUCE panellist verified (sha256 30ad1d2601a2f3edaa8d1b7950988f1627f514ea0d7c2edcf3943e7a553221f2): True
  ok   configuration B expands to the full-sequence prediction file the REPRODUCE panellist verified (sha256 e323a6a3d9c60d95fbdd2ffd348a8bb0653411399a482a751d15ebc015ebc490): True

10. what this checker cannot do
    - It cannot refit the models; group 9 only proves the shipped predictions are the
      ones the panel verified. RUN_IT_YOURSELF.md refits them.
    - It cannot check the leakage test, only that the package records byte-identical
      prediction files from a refit with every test score replaced by nan; re-running
      that test needs the released file and is step 4 of RUN_IT_YOURSELF.md.
    - It cannot check novelty, and it does not fetch the scoreboard. the-record-we-beat/
      holds the snapshot with its fetch time and HTTP status.
    - It cannot quantify configuration-selection noise: the configuration was chosen in
      an earlier run and the only interval here is over test-sequence sampling.

0 check(s) failed.
PASS
```
