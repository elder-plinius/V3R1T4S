# Null & Perturbation Controls (`2026-10-29-mizopl-61e59c7d`)

1. **Impure Stabilizer Controls (`[[15, 0, 8]]_5` & Pre-`2026-10-21` `[[15, 0, 8]]_7`):**
   - `[[15, 0, 8]]_5` (`QECC.php?q=25&n=15&k=0`, `sha256: e2877a2731fae0b79afffddd6e82093b10df08af554f82d7707d0a82bcf67706`) has generator row 9 of symplectic weight $w_{\text{pure}} = 7 < 8$ and fails full rank on **`190 / 6,435`** seven-party cuts (all 190 of rank 14).
   - Pre-`2026-10-21` `[[15, 0, 8]]_7` (`[[14, 0, 8]]_7` $\oplus$ 1-qudit stabilizer on coordinate 14) has generator row 14 of symplectic weight $w_{\text{pure}} = 1 < 8$ and fails full rank on **`3,003 / 6,435`** seven-party cuts, whereas Markus Grassl's `2026-10-21` cyclic replacement (`sha256: c4511cff304494b4ce074bc38f403676802c1a4d0a9d77880447c43fd4ac54d4`) has **`0 / 6,435`** rank-deficient cuts ($w_{\text{pure}} = 8$).
2. **Shift-Vector Null & Random Perturbation Controls (`AME(9, 10)` & `AME(11, 10)` Cross-Checks):**
   - Setting $c_9 = 0 \in \mathbb{F}_5^9$ survives **`0 / 72`** cuts where the binary `[[9, 2, 3]]_2` off-diagonal partial traces are non-zero.
   - Setting $c_{11} = 0 \in \mathbb{F}_5^{11}$ survives **`0 / 129`** cuts where the binary `[[11, 1, 5]]_2` off-diagonal partial traces are non-zero.
   - Sampling `400` random vectors in $\mathbb{F}_5^9$ (`seed = 42`) yields **`0 / 400`** vectors surviving all 72 affected cuts (maximum random survival: `69 / 72`, vs. `72 / 72` for $c_9 = (0, 0, 0, 1, 4, 4, 3, 1, 1)$).
