# How to Rebuild the Certificate from Scratch

`build_certificate.py` uses only the Python `3` standard library (`fractions`, `itertools`, `json`, `math`, `os`, `sys`) with zero external packages and zero floating-point arithmetic.

Run from the package root directory:

```sh
python3 -B how-we-built-it/build_certificate.py object/d19_nonisometric_periodic_packing_certificate.json
sh verify-it-yourself/run_checks.sh
```

`build_certificate.py` deterministically constructs:
1. The `4096`-codeword extended binary Golay code `G_24` in standard `4 x 6` Miracle Octad Generator (MOG) coordinates and the `24 x 24` Hermite Normal Form basis of `sqrt(8) * Lambda_24` (`det = 2^36`).
2. Both `Co_0`-inequivalent saturated rank-`5` cross-sections `K_II` (discovered here) and `K_I` (Ruitao Chen, Jiachen Hu, Binghui Li, Liwei Wang, and Tianyi Wu, `2025`, `arXiv:2505.02394`) of determinant `300` inside `Lambda_24`, integer Smith Normal Form right-inverse saturation witnesses (`Y_A * Z_A = I_5`, `Y_B * Z_B = I_19`), `19`-dimensional orthogonal complement lattices `L_II` and `L_I`, exact rational LLL-reduced integer bases, and exact rational `R^T * D * R` Cholesky decompositions.
3. The exact rational discriminant-square ray shift `u_ray / 1860` (`22560^2 - 1440 * 14880 = 22080^2`, `alpha = 1/31`, reduced common ambient denominator `465`, basis-coordinate denominator `930`) applied to translates `1, 2, 3` of `P19_II_vtx`, achieving `bilateral_contact_rank_trans = 95/95` and `bilateral_contact_rank_full = 285/285` (`0`-dimensional vertex isolation inside its `12166`-contact kissing-graph stratum) while preserving exact minimal squared distance `52/15`.
