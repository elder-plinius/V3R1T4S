# Skeptic 3: Target Criterion & Zero-Leakage Audit

- Context: Fresh independent verification from the package root auditing target criteria in `bank/targets.json` and zero-leakage compliance.
- Question: Does the solver strictly obey all target rules in `bank/targets.json` without ground-truth leakage or per-event hardcoding?

## Audit Summary

1. Inspected `how-we-built-it/solve_roman_dc18.py` and `how-we-built-it/binary_lens_kernel.c` and verified via static AST and source analysis that the solver is 100% self-contained and operates exclusively on the two-band light curves (`ulwdc1_<NNN>_W149.txt` and `ulwdc1_<NNN>_Z087.txt`) with zero access to `master_file.txt`, `Answers/`, or team entries during prediction, and zero per-event hardcoded rules or external cache files.
2. Verified that `verify-it-yourself/check_roman_dc18.py` implements the exact `bank/targets.json` tolerances (`|dlog10 s| <= 0.1` with `s <-> 1/s` degeneracy allowed, `|dlog10 q| <= 0.3` on `0 < q < 0.03` USBL events) and requires every recovered planet to also be classified as `USBL` by the three-class classifier.
3. Confirmed that partial-win criteria `p2` (`274 / 293 > 268 / 293`), `p3` (`3 / 3 >= 2 / 3`), and `p4` (`9 / 10 >= 8 / 10`) in `bank/targets.json` are all strictly satisfied.

pass: true
