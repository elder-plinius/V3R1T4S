# Run It Yourself — `laminar-ef1-four-agent-key-matroids`

## Quick Verification
To verify the counterexample and obstruction certificate from within this package directory:

```bash
sh verify-it-yourself/run_checks.sh
```

Expected output:
```text
Evaluated all 864 complete allocations.
Ordered no-envy violations: 828
EF1 violations: 36
Universal obstruction confirmed: 0 valid allocations exist.
PASS
```

## How to Rebuild the Object from Scratch
To rerun the exact SMT synthesis and re-generate `object/valuation_matrix.json` and `object/obstruction_certificate.json`:

```bash
python3 how-we-built-it/code/find_and_verify_counterexample.py
```

Requirements: Python 3 with standard library (`itertools`, `fractions`, `json`). No third-party packages required for verification.
