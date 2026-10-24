# DNA Minimizer Density Improvement at `(w = 12, k = 3)`: `0.138389 -> 0.136569` (`-1.3155%` vs `angle-based`, `-1.6382%` vs `GreedyMini`)

## What

An explicit binary-projected DNA minimizer rank order claim/w12_k3_improved.gm (72 bytes, sha256 dd85465d87f23d688778ff35175ed19e4c9f00e71cad28b535d7a9d73294f302, rank vector [4, 7, 1, 0, 6, 5, 2, 3]) for (w, k) = (12, 3) with exact expected DNA density 146,639,789 / 2^30 = 0.1365689458, strictly lowering the smallest listed expected DNA density 0.138389448 (angle-based) by 1.315492% relative and the published GreedyMini density 149,082,035 / 2^30 = 0.1388434647 by 1.638189% relative across OrensteinLab/10-minimizers and OrensteinLab/GreedyMini at identical 72-byte storage cost.

- **Target ID:** `minimizer-density-record-tables` (`biology`)
- **Parameters:** $w = 12, k = 3$
- **Minimizer rank file (`.gm` format):** `object/w12_k3_improved.gm` (`72` bytes, `sha256: dd85465d87f23d688778ff35175ed19e4c9f00e71cad28b535d7a9d73294f302`)
- **CSV rank table (`GreedyMini --mode export --save_format csv`):** `object/w12_k3_improved.csv` (`59` bytes, `sha256: 24790fb381b985fe053ea4d82ae225412815e1a2df754a55fe5a53448ab7b55a`)
- **Rank vector (`000..111`):** `[4, 7, 1, 0, 6, 5, 2, 3]`
- **Exact expected DNA density (`prob_gc_dna` and 4-ary de Bruijn DP):** $\frac{146,639,789}{2^{30}} \approx 0.1365689458$ (provable global minimum over all $8! = 40,320$ strict binary 3-mer permutations)
- **Storage cost:** `72` bytes on disk (`8`-byte `size_t` length prefix `8` + $8 \times 8$-byte `uint64_t` ranks, identical to `OrensteinLab/10-minimizers`'s precomputed `w12_k3.gm`), or `24` bits ($8 \times 3$ bits) of rank information.

## Check It Yourself

From the root of this package directory, run:

```bash
sh verify-it-yourself/run_checks.sh
```

This runs the standalone Python verifier `verify-it-yourself/author_checker_minimizer_check.py` on `object/w12_k3_improved.gm`, `the-record-we-beat/published_w12_k3.gm`, and `the-record-we-beat/k_extension_k16_w12.csv`, verifying exact expected DNA density via both `prob_gc_dna` (`146,639,789 / 2^30 = 0.1365689458`) and 4-ary de Bruijn transfer-matrix DP (`146,639,789 / 2^30 = 0.1365689458`), and prints `PASS` on the final line in ~0.4 seconds.

## Compared To

- **`angle-based` in `k_extension_k16_w12.csv` (`OrensteinLab/10-minimizers`, column `3`):**
  - Smallest published expected DNA density at $(w=12, k=3)$: `0.138389448` (where `angle-based` previously beat `GreedyMini = 0.138843`).
  - Our binary-projected `.gm` order achieves `0.1365689458`, improving on `angle-based` by **`-1.315492%` relative** (`2.63x` the `0.5%` relative threshold) while restoring binary-projected `.gm` superiority at $(w=12, k=3)$.
- **`OrensteinLab/10-minimizers` Precomputed `w12_k3.gm` (`the-record-we-beat/published_w12_k3.gm`, `sha256: c592519b57ad8104860b7e1559b28c2d37ef329db82298b151a65e056ce27f1d`):**
  - Exact expected DNA density (`prob_gc_dna`): `149,082,035 / 2^30 = 0.1388434647` (listed as `0.138843` in `k_extension_k16_w12.csv`).
  - Our order reduces gamechanger windows by `-2,442,246` out of $4^{15} = 1,073,741,824$ (**`-1.638189%` relative**, exceeding the `0.5%` relative threshold by `3.28x`).

## Not Claimed

- We do not claim global optimality over arbitrary 4-ary orders of size $4^3 = 64$; `object/w12_k3_improved.gm` is an explicit binary-projected `.gm` order of size $2^3 = 8$ (`72` bytes), where it achieves the exact global minimum over all $8! = 40,320$ strict binary 3-mer permutations.
- This submission package claims and certifies the explicit order `object/w12_k3_improved.gm` for $(w, k) = (12, 3)$.

## Credits

- **Credit:** `mizopl` (`@mizopl`)
- **Benchmark & Repositories:** Golomb, Orenstein, et al. (`OrensteinLab/GreedyMini` and `OrensteinLab/10-minimizers`).
