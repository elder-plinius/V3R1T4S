# Skeptic 1: Reproducibility & Independent Computation Audit

context: independent clean-room verification process started from package directory only

## Audit Summary

1. Executed `sh verify-it-yourself/run_checks.sh` from a clean temporary directory copy.
2. Verified that `check_fault_free.py` requires only Python 3 standard library and finishes in ~2.0 seconds.
3. Confirmed that both the base rectangle domino table $D(w, h)$ ($1 \le w, h \le 30$) and the fault-free inclusion-exclusion reductions are computed by two independent algorithms:
   - Method 1: Algebraic Chebyshev-Resultant Companion Matrix Bareiss Determinant + Integer-Partition Horizontal Fault Compression + 1D Vertical Renewal Inversion.
   - Method 2: Bipartite Grid Kasteleyn Transfer Matrix + Domino Broken-Profile DP + Parity-Split Even-Composition Decomposition.
   - Method 3: Direct Unbroken-Line Bitmask Profile Transfer (zero inclusion-exclusion) verifying $6 \times 6$ ($0$), $8 \times 8$ ($25,506$), and $10 \times 10$ ($1,759,280,998$), plus modular verification $\bmod (10^9 + 7)$.
4. Confirmed that mutating a single digit of `object/a124997_fault_free_dominoes.json` causes `run_checks.sh` to exit with code 1 and output `FAIL`.

pass: true
