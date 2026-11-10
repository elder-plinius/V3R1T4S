# Skeptic 1: Reproducibility & Independent Computation Audit

- Context: Fresh independent verification from the package root (`sh verify-it-yourself/run_checks.sh`).
- Question: Does `verify-it-yourself/run_checks.sh` independently recompute all 293 Roman DC18 predictions, compile and test the C99 binary-lens kernel, execute a live smoke test of `how-we-built-it/solve_roman_dc18.py`, and fail on object corruption?

## Audit Summary

1. Executed `sh verify-it-yourself/run_checks.sh` from a clean temporary copy of the package.
2. Verified that `verify-it-yourself/check_roman_dc18.py` compiles and executes the C99 5th-degree complex binary-lens polynomial solver (`how-we-built-it/binary_lens_kernel.c`), imports `how-we-built-it/solve_roman_dc18.py` and runs a live functional smoke test, audits `how-we-built-it/solve_roman_dc18.py` via `ast` to confirm zero ground-truth leakage, and independently recomputes every event's `dlog10_s = min(|log10(pred_s) - log10(true_s)|, |log10(1/pred_s) - log10(true_s)|)`, `dlog10_q = |log10(pred_q) - log10(true_q)|`, three-class accuracy (`280 / 293`), low-q planet recovery (`46 / 51`), false low-q predictions (`5 <= 9`), `p3` recovery (`3 / 3` on `log10 q < -5`), and `p4` recovery (`10 / 10` on `s > 2, q < 0.03`) against `verify-it-yourself/data/roman_dc18_eval_ref.json.gz`, matching all 293 event rows in `object/roman_dc18_predictions.tsv`.
3. Confirmed that mutating a single digit in `object/roman_dc18_predictions.tsv` causes `run_checks.sh` to exit with code 1 and output `FAIL`.

pass: true
