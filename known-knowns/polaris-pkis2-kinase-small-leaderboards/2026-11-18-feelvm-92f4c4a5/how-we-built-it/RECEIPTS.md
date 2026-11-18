# RECEIPTS — how the object was built and re-checked (real outputs)

## Retrain determinism (producing machine, pinned stack)

The portable `lokslk_pipeline.py` was run from this folder with the official inputs staged here
temporarily (both sha256-pinned; the files are not part of the package — see COMMANDS.md and
RUN_IT_YOURSELF.md for the curl commands). Output (retrain_test.log):

    CLASS_LOK platt a=9.000716 b=-7.882329
    CLASS_SLK platt a=5.744524 b=-5.822587
    wrote preds.csv with 132 rows

The retrained `preds.csv` was compared with the shipped `object/preds.csv`: identical row order,
identical Platt coefficients, and **bit-identical probabilities** (max abs diff 0.000e+00 for both
targets), i.e. the shipped object is exactly reproducible from the pinned recipe and the official
inputs. Recomputed on the official test labels: CLASS_LOK pr_auc 0.634334, roc_auc 0.880208;
CLASS_SLK pr_auc 0.377857, roc_auc 0.838074.

Two earlier defects in this portability test were caught and fixed before the package was finalised
(recorded for honesty): (1) the out-of-fold step indexed the full-table feature matrix with
positional fold indices, which inverted the CLASS_LOK Platt map in the retrained copy (the shipped
object was built from the correctly indexed saved OOFs and was never affected); (2) the producing run
used float32-cached descriptor blocks, so the portable script rounds its descriptors to float32 to
be bit-identical. Both fixes are in `lokslk_pipeline.py` (the OOF step slices the train rows; the
feature builder casts to float32).

## Harness calibration (published null-model values reproduced exactly)

`baseline/lokslk_null_model.py`, real output (baseline/lokslk_null_model_output.txt):

    CLASS_LOK: constant-1 pr_auc 0.18181818181818182  n_pos 24/132  expected 0.18181818181818182
       matches a listed value: True
    CLASS_SLK: constant-1 pr_auc 0.09848484848484848  n_pos 13/132  expected 0.09848484848484848
       matches a listed value: True
    CLASS_LOK constant-1 accuracy 0.18181818181818182 vs listed 0.18181818181818182 match True

    BASELINE CALIBRATION: PASS

## Null test (400 label-permutation controls through the same pipeline)

See `null_test.md` in this folder: control CLASS_LOK pr_auc min 0.117245 / mean 0.251396 /
max 0.607118; the real CLASS_LOK pr_auc 0.634334 beats all 400. The Platt-invariance assertion of
the runner printed `platt_invariance_check raw 0.634333770922 platt 0.634333770922 equal True`.

## Corrections made before submission (recorded, not hidden)

The pre-claim page sha256 was hand-transcribed into three package files with a duplicated "fa"
(66 characters instead of 64). The mechanical gate caught it (`CHECK_RUN: FAIL` on
"the-record-we-beat/ needs ... the page's sha256"), and all copies were corrected to the fetched
page's real hash 5671da872b25a3afad11552ace4f0301c3f5afa3db0ac23f45868c9cddb58fbc (64 hex,
recomputed from the saved page file). This is a documentation pin for the fetch, not an input to any
computation: the leaderboard values are identical in every fetch, and the parquet/bench-json pins the
REPRODUCE skeptic verified byte-for-byte were never affected. The NOVELTY verdict's note that "the
claim folder records a different hash" quotes the pre-correction string; its own fetch
(a1da2c1c64e5241f5910166883ee2ed478f9028b7ceafe83d289ffd9722b5eaf, same byte size, same values)
remains recorded there as written.

## InChIKey audit + independent recomputation (self-break)

Real output of the producing run's independent verifier:

    PASS 640 unique InChIKeys
    PASS train/test InChIKey overlap 0
    PASS test keys unique
    PASS split union covers 640
    PASS test order is API order
    PASS no test InChIKey skeleton in auxiliary files
    PASS pred rows == official test rows
    PASS probabilities in [0,1]
    independent CLASS_LOK pr_auc 0.634333770922 roc 0.880208333333
    independent CLASS_SLK pr_auc 0.377856659137 roc 0.838073691015
    independent mean pr_auc 0.506095215029
    PASS CLASS_LOK pr_auc equals scored value
    PASS beats every listed pr_auc (max listed 0.2553191489361702)
    PASS margin >= +0.020
    PASS mean also above margin
    PASS probs not a copy of labels
    PASS 6 entries listed
    PASS our value above max listed
    PASS manifest parquet sha256
    PASS manifest test array
    PASS no browser-UA/cookie/retry code

    SELF_BREAK: SURVIVES
