# Verification Receipts (`moore-graph-57` — `2026-10-26-mizopl-659ce5b9`)

- **Command:** `sh verify-it-yourself/run_checks.sh`
- **Certificate Verified:** `object/certificate.json` (`sha256: 659ce5b9f841936bf9b859ab527ab00183adad85edb7371ae2cddd035019b2a6`)
- **Execution Time:** `< 0.1 seconds` (100% exact Python standard-library `fractions.Fraction`, `int`, and finite-field $\mathbb{F}_p$ Gaussian elimination)
- **Corrupted-Object Rejection:** Mutating any digit in `object/certificate.json` causes `verify.py` to print `FAIL` on its last line and exit with status `1`.

## Verified Output
```text
All Track p1 (unconditional & conditional automorphism group exclusions) and Track p2 (arXiv:2606.29183v2 exact verification) checks matched certificate.json digit-for-digit.
PASS
```
