# Verification Receipts (`RECEIPTS.md`)

## 1. Clean Package Execution (`exit 0`)

Command:

```sh
sh verify-it-yourself/run_checks.sh
```

Output:

```text
VERIFICATION SUMMARY: Live upstream-joined recomputation across 127/127 P2-Raw (2,450,592 ranked entries, 0 mismatches) + 988/988 P2-Holdout (98,800 top-100 entries, 0 mismatches) + 40/40 Pos-40 verified in 50.19s | P2-Raw MARG-P2 MRR=0.001089 (Med=8957.0) vs LIRICAL=0.000083 (Med=12109.0) | P2-Holdout MARG-P2 MRR=0.008803 (Top-1=5/988, Top-10=9/988, Med=4052.5) vs LIRICAL=0.000089 & Shuffled-Ctrl=0.000991
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
VERIFICATION ERROR: blind_p2_raw_127.marg_p2_seam.mrr mismatch: recomputed=0.0010885247192337782 vs cert=0.011088524719233779
FAIL
```

Exit status: `1`
