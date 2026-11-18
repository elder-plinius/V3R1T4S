# Verification Receipts: `mint-net-below-digital-bound` (Partial Win `p1`)

Command executed from the package root:

```sh
sh verify-it-yourself/run_checks.sh
```

Exit code: `0`

Captured standard output:

```text
[Python] Positive soundness calibrations on explicit base-3 and base-2 nets: OK
[Python] VERIFIED (Python Fraction): M >= 2403828588527406331/13544324988667 (~177478.655491) > 3^11 = 177147 across all 8854 non-diagonal shapes (min_LHS = 0)
[Python] Negative corruption checks (sign violation & dual slack violation rejected): OK
[C99 __int128] VERIFIED: M >= 177478.655491 > 3^11 = 177147 across all 8854 non-diagonal shapes (min_scaled_LHS = 0)
[C99 __int128] Negative corruption checks (sign & slack violations rejected): OK
PASS
```
