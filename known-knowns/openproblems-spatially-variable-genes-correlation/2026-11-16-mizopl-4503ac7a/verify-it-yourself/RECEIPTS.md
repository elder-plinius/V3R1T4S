# Verification Receipts (`RECEIPTS.md`)

## 1. Clean Package Execution (`exit 0`)

Command:

```sh
sh verify-it-yourself/run_checks.sh
```

Output:

```text
VERIFICATION SUMMARY: 12/12 panel datasets (9 technologies) + 6 JSON certificates verified in 44.73s | 50-ds mean tau = 0.945981 (46-holdout = 0.953362; Wave2 EB v2 = 0.945966) | melanoma v1 = 0.797905 / v2 = 0.799619 (bead0.85: v2=0.7642 > v1=0.7596 > SPX=0.5507) | col_perm_err = 9.99e-16 | isometry_err = 1.04e-14 | null_tau = +0.0152
PASS
```

Exit status: `0`

## 2. Adversarial `--corrupt` Negative Control (`exit 1`)

Command:

```sh
sh verify-it-yourself/run_checks.sh --corrupt
```

Output:

```text
VERIFICATION ERROR: Panel recomputation mismatch vs certificate vector[0] (01_10x_Visium_mouse_brain)
FAIL
```

Exit status: `1`
