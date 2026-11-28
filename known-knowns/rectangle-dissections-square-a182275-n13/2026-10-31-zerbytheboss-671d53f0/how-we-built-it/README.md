# How We Built It

- `PREREG.md`: Pre-registered target specification, baseline OEIS b-file hashes, and three-method verification plan.
- `check_dissections.py`: Self-contained pure-Python solver and verifier implementing Method 1 (1-Bit Broken-Profile Vertex-Degree Continuity DP), Method 2 (Recursive Kronecker-Block Divide-and-Conquer on `(M_m, B_m)` + Transpose Symmetry), and Method 3 (Fibonacci `F(2m+1)` Vertical-Cut Open-Rectangle Transfer Matrix).
