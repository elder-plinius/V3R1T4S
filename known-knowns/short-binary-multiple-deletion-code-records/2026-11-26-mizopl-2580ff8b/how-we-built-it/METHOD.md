# Method Summary

- Explicit set-packing / MIS search on binary deletion conflict graphs `G_{n,s}` without external codebook seeding.
- Symmetry-quotient orbit search (`<c, r>`, `<rc>`, `<r>`, `<c>`) for `(16, 3) = 44`.
- Dynamic `min d_free` + adaptive random walk for `(15, 3) = 31`.
- Run-aware dual-LP weighted `<c>`-orbit seeding followed by unrestricted unbiased unfreeze for `(15, 2) = 137`.
- Independent verification via exact `D_s` hashing, full pairwise DP `LCS`, `--corrupt` negative control, and standalone zero-dependency Lean 4.36.0 (`lake env leanchecker`).
