# How We Found It: Exact SOS-DP DNA Objective & Global Permutation Optimum at `(w = 12, k = 3)`

*(contributor text, unverified)*

## 1. The `(w = 12, k = 3)` Crossing Point in `k_extension_k16_w12.csv`

In `OrensteinLab/10-minimizers` (Shur, Tziony, and Orenstein, WABI 2026) and `OrensteinLab/GreedyMini` (Golan, Tziony, Kraus, Orenstein, and Shur, Bioinformatics 2025), `(w = 12, k = 3)` in `k_extension_k16_w12.csv` is the cell where `angle-based` (`0.138389448`) had a lower listed expected DNA density than `GreedyMini` (`0.138843`, precomputed `w12_k3.gm` with rank vector `[8, 2, 8, 8, 0, 4, 1, 3]` and exact DNA density `149,082,035 / 2^30 = 0.1388434647`).

## 2. Fast SOS-DP DNA Gamechanger Evaluation & Exhaustive `8! = 40,320` Proof

Because `GreedyMini`'s pipeline trains `.gm` orders on the binary (`2^{w+k}`) objective and stops at an early singleton rank (`8`), the precomputed `w12_k3.gm` leaves 3 of the 8 binary 3-mers tied at the maximum rank `8` and misses the DNA (`4^{w+k}`) optimum. Using our fast Sum-Over-Subsets (`SOS-DP`) exact DNA gamechanger evaluator (`how-we-built-it/sos_dna_optimizer.cpp`) and an exhaustive sweep over all $8! = 40,320$ strict permutations of `0..7`, we found that the permutation `[4, 7, 1, 0, 6, 5, 2, 3]` (`object/w12_k3_improved.gm`) achieves the **exact global minimum** expected DNA density over all $8! = 40,320$ strict binary 3-mer orders within the binary-projected DNA extension construction (GreedyMini order on the high bit of each base, $k$-mer read most-significant base first, lexicographic order on the low bits, leftmost ties):
$$\frac{146,639,789}{2^{30}} \approx 0.1365689458,$$
strictly beating `angle-based` (`0.138389448`) by **`-1.315492%` relative** and `GreedyMini` (`0.1388434647`) by **`-1.638189%` relative**.
