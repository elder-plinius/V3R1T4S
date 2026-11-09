# How We Built It

- `PREREG.md`: Pre-registered target specification, baseline OEIS b-file hashes, and three-method verification plan.
- `check_fault_free.py`: Self-contained pure-Python solver and verifier implementing Method 1 (Chebyshev-Resultant Bareiss Determinant + Integer-Partition Horizontal Fault Compression + 1D Renewal Inversion), Method 2 (Bipartite Kasteleyn Transfer + Broken-Profile DP + Parity-Split Even-Composition Decomposition), and Method 3 (Direct Unbroken-Line Bitmask Profile Transfer on `6 x 6`, `8 x 8`, and `10 x 10` without inclusion-exclusion).
