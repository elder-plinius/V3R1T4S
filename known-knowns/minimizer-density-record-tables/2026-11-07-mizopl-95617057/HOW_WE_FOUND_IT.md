# How We Found It (`contributor text, unverified`)

> **Note:** This narrative is contributor text, unverified; only the rank files `object/w12_k4_4ary.gm` and `object/w12_k4_4ary.csv` and their mechanical verification in `verify-it-yourself/` constitute the verified claim.

## 1. Why Binary-Projected `.gm` Orders Plateau at `0.133629` on `(w = 12, k = 4)`

In `OrensteinLab/Minimizers` (Golan, Tziony, Kraus, Orenstein, and Shur, *Bioinformatics* 2025), the precalculated binary order for $(w = 12, k = 4)$ (`lowest-density/binary/individual-orders/ranks/k4-w12.txt`, UHS size 7: `[3, 16, 2, 16, 16, 4, 1, 0, 16, 16, 16, 16, 16, 16, 5, 6]`), extended to DNA via the high-bit/low-bit split, achieves exact expected DNA density `574,313,157 / 2^32 = 0.1337177020` (improving upon `w12_k4.gm` in `OrensteinLab/10-minimizers` at `584,312,429 / 2^32 = 0.1360458389`).

Within the 16-entry binary-projected `.gm` subspace, all 16 DNA 4-mers sharing the same high-bit 4-mer $\text{bin}(x) \in \{0,\dots,15\}$ are constrained to occupy a contiguous block of 16 ranks ordered lexicographically by their low-bit 4-mer $\text{low}(x) \in \{0,\dots,15\}$. Optimizing over all $16!$ binary permutations plateaus at `[15, 6, 7, 12, 10, 4, 11, 3, 0, 1, 8, 9, 14, 2, 13, 5]`, which gives `573,933,439 / 2^32 = 0.1336292920` (`-0.0661%` relative below `k4-w12.txt`, short of the `0.5%` relative threshold `0.1330491135`).

## 2. Direct 4-Ary DNA Order Optimization (`how-we-built-it/opt_4ary_dna.cpp`)

Attacking the bit-interleaving extension directly by allowing the 256 DNA 4-mers (`0..255`) to take an arbitrary strict rank permutation `rank[0..255]` breaks the contiguous-block constraint. Using an active-set forward/backward 4-ary de Bruijn transfer-matrix evaluator (`Dna4AryEvaluator::eval_gc` in `how-we-built-it/opt_4ary_dna.cpp`, ~1,000 exact $4^{16}$-window evaluations per second), hill-climbing over swaps involving low-rank active 4-mers (`r1 < 115`) starting from the binary-projected seed `[15, 6, 7, 12, 10, 4, 11, 3, 0, 1, 8, 9, 14, 2, 13, 5]` crossed the `-0.5%` threshold (`571,441,591 / 2^32 = 0.1330491135`) at iteration 4,475 (`4.37s`) and reached `570,244,411 / 2^32 = 0.1327703733` (`-0.7085%` relative below `OrensteinLab/Minimizers` `k4-w12.txt` and `-2.4076%` relative below `OrensteinLab/10-minimizers` `w12_k4.gm`) at iteration 35,266 (`34.69s`).
