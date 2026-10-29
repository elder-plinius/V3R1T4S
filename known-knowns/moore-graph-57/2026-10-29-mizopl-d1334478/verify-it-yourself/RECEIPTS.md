# Verification Receipts (`moore-graph-57` — `2026-10-29-mizopl-d1334478`)

- **Command:** `sh verify-it-yourself/run_checks.sh`
- **Certificate Verified:** `object/certificate.json` (`sha256: d13344783df1b7cf33f19e9b3408bad1bbe96939c5e087b02460113f03dc9c07`)
- **Execution Time:** `< 0.1 seconds` (100% exact Python standard-library `fractions.Fraction`, `int`, and finite-field $\mathbb{F}_p$ Gaussian elimination)
- **Corrupted-Object Rejection:** Mutating any digit in `object/certificate.json` causes `verify.py` to print `FAIL` on its last line and exit with status `1`.

## Verified Output
```text
All Track p2 (arXiv:2606.29183v2 exact verification) checks matched certificate.json digit-for-digit.
PASS
```
