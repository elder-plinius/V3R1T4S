# Receipt: output of `sh verify-it-yourself/run_checks.sh` (with the per-check lines of verify.py)

```
ok    call list has 437 calls (437)
ok    100 real draws, draw_000 to draw_099
ok    folds stratified by caller x receiver in every draw (0 problems)
ok    every habit prediction follows the caller-habit rule (0 problems)
ok    every forest prediction is a receiver present in the training folds (0 problems)
ok    saved accuracies equal the recomputed ones (0 problems)
ok    habit mean 0.492243 equals summary
ok    rf mean 0.269542 equals summary
ok    1,000 controls, ids 0-999, folds of draw id mod 100
ok    control mean 0.210668 equals summary
ok    control 99.9th percentile 0.242565 equals summary
ok    control maximum 0.244851 equals summary
ok    p3: |rf mean - 0.275| = 0.0055 <= 0.02
ok    p3 statement: 0.275 does not exceed the caller-habit baseline 0.4922
ok    p3 statement: 0.275 and the rf mean 0.2695 exceed the shuffle 99.9th percentile 0.2426
ok    call list has 437 calls (437)
ok    100 real draws, draw_000 to draw_099
ok    folds stratified by caller x receiver in every draw (0 problems)
ok    every habit prediction follows the caller-habit rule (0 problems)
ok    every forest prediction is a receiver present in the training folds (0 problems)
ok    saved accuracies equal the recomputed ones (0 problems)
ok    habit mean 0.492243 equals summary
ok    rf mean 0.269542 equals summary
ok    1,000 controls, ids 0-999, folds of draw id mod 100
ok    control mean 0.210668 equals summary
ok    control 99.9th percentile 0.242565 equals summary
ok    control maximum 0.244851 equals summary
ok    p3: |rf mean - 0.275| = 0.0055 <= 0.02
ok    p3 statement: 0.275 does not exceed the caller-habit baseline 0.4922
ok    p3 statement: 0.275 and the rf mean 0.2695 exceed the shuffle 99.9th percentile 0.2426
PASS
```
