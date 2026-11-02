# DNA Minimizer Density Improvement at `(w = 12, k = 3)`: `0.138389 -> 0.136569` (`-1.3155%` vs `angle-based`, `-1.6382%` vs `GreedyMini`)

## What

An explicit binary-projected DNA minimizer rank order object/w12_k3_improved.gm (72 bytes, sha256 dd85465d87f23d688778ff35175ed19e4c9f00e71cad28b535d7a9d73294f302, rank vector [4, 7, 1, 0, 6, 5, 2, 3]) for (w, k) = (12, 3) with exact expected DNA density 146,639,789 / 2^30 = 0.1365689458, strictly lowering the smallest listed expected DNA density 0.138389448 (angle-based) by 1.315492% relative and the published GreedyMini density 149,082,035 / 2^30 = 0.1388434647 by 1.638189% relative across OrensteinLab/10-minimizers and OrensteinLab/GreedyMini at identical 72-byte storage cost.

- **Target ID:** `minimizer-density-record-tables` (`biology`)
- **Parameters:** $w = 12, k = 3$
- **Minimizer rank file (`.gm` format):** `object/w12_k3_improved.gm` (`72` bytes, `sha256: dd85465d87f23d688778ff35175ed19e4c9f00e71cad28b535d7a9d73294f302`)
- **CSV rank table (`GreedyMini --mode export --save_format csv`):** `object/w12_k3_improved.csv` (`59` bytes, `sha256: 24790fb381b985fe053ea4d82ae225412815e1a2df754a55fe5a53448ab7b55a`)
- **Rank vector (`000..111`):** `[4, 7, 1, 0, 6, 5, 2, 3]`
- **DNA extension convention:** Each 2-bit DNA base $c \in \{0, 1, 2, 3\}$ is split into a high bit $b_1 = \lfloor c / 2 \rfloor \in \{0, 1\}$ and a low bit $b_2 = c \bmod 2 \in \{0, 1\}$, with each $k$-mer read most-significant base first. A DNA $k$-mer is ordered first by the `GreedyMini` rank order `order[0..7]` applied to the high bit of each base, then by lexicographic order on the low bits of the $k$-mer, with remaining ties between identical DNA $k$-mers broken by leftmost window position.
- **Exact expected DNA density:** $\frac{146,639,789}{2^{30}} \approx 0.1365689458$ (exact global minimum over all $8! = 40,320$ strict binary 3-mer orders within this binary-projected DNA extension construction)
- **Storage cost:** `72` bytes on disk (`8`-byte `size_t` length prefix `8` + $8 \times 8$-byte `uint64_t` ranks, identical to `OrensteinLab/10-minimizers`'s precomputed `w12_k3.gm`), or `24` bits ($8 \times 3$ bits) of rank information.

## Check It Yourself

From the root of this package directory, run:

```bash
sh verify-it-yourself/run_checks.sh
```

This fetches the upstream reference table `k_extension_k16_w12.csv` (`sha256: 88c4f8fcd0ea6d4308f4e1fc716bb901ea78d3c6112b7e70d4af42bb631bf2fa`) and precomputed `w12_k3.gm` (`sha256: c592519b57ad8104860b7e1559b28c2d37ef329db82298b151a65e056ce27f1d`) at pinned commit `916daebd399d15d061e2fd437326aee5cf0e7292` (stopping on any SHA-256 mismatch), runs `verify-it-yourself/author_checker_minimizer_check.py` on `object/w12_k3_improved.gm`, verifies exact expected DNA density via both high-bit/low-bit bit-plane enumeration (`146,639,789 / 2^30 = 0.1365689458`) and 4-ary de Bruijn transfer-matrix DP (`146,639,789 / 2^30 = 0.1365689458`), and prints `PASS` on the final line in ~0.4 seconds.

## Compared To

- **`angle-based` in `k_extension_k16_w12.csv` (`OrensteinLab/10-minimizers`, column `3`, recorded in `the-record-we-beat/minimizer_record_snapshot.md`):**
  - Smallest listed expected DNA density at $(w=12, k=3)$: `0.138389448` (where `angle-based` previously beat `GreedyMini = 0.138843`).
  - Our binary-projected `.gm` order achieves `0.1365689458`, improving on `angle-based` by **`-1.315492%` relative** (`2.63x` the `0.5%` relative threshold).
- **`OrensteinLab/10-minimizers` Precomputed `w12_k3.gm` (`sha256: c592519b57ad8104860b7e1559b28c2d37ef329db82298b151a65e056ce27f1d`, recorded in `the-record-we-beat/minimizer_record_snapshot.md`):**
  - Exact expected DNA density: `149,082,035 / 2^30 = 0.1388434647` (listed as `0.138843` in `k_extension_k16_w12.csv`).
  - Our order reduces gamechanger windows by `-2,442,246` out of $4^{15} = 1,073,741,824$ (**`-1.638189%` relative**, exceeding the `0.5%` relative threshold by `3.28x`).

## Not Claimed

- We do not claim global optimality over arbitrary 4-ary orders of size $4^3 = 64$; `object/w12_k3_improved.gm` is an explicit binary-projected `.gm` order of size $2^3 = 8$ (`72` bytes), where the $8! = 40,320$ global optimum holds within the binary-projected DNA extension construction (GreedyMini order on the high bit of each base, $k$-mer read most-significant base first, lexicographic order on the low bits, leftmost ties).
- This submission package claims and certifies the explicit order `object/w12_k3_improved.gm` for $(w, k) = (12, 3)$.

## Credits

- **Credit:** `mizopl` (`@mizopl`)
- **GreedyMini:** Golan, Tziony, Kraus, Orenstein, and Shur (*Bioinformatics*, 2025) — [`OrensteinLab/GreedyMini`](https://github.com/OrensteinLab/GreedyMini) (pinned commit [`a67eb90dc278ea78111a76d5813cf2ac7662b0ae`](https://github.com/OrensteinLab/GreedyMini/tree/a67eb90dc278ea78111a76d5813cf2ac7662b0ae), upstream C++ evaluator [`code/density_and_gc.cpp`](https://github.com/OrensteinLab/GreedyMini/blob/a67eb90dc278ea78111a76d5813cf2ac7662b0ae/code/density_and_gc.cpp)).
- **10-minimizers:** Shur, Tziony, and Orenstein (*WABI*, 2026) — [`OrensteinLab/10-minimizers`](https://github.com/OrensteinLab/10-minimizers) (pinned commit [`916daebd399d15d061e2fd437326aee5cf0e7292`](https://github.com/OrensteinLab/10-minimizers/tree/916daebd399d15d061e2fd437326aee5cf0e7292), upstream density notebook [`density-measurement-and-plots/greedymini_density.ipynb`](https://github.com/OrensteinLab/10-minimizers/blob/916daebd399d15d061e2fd437326aee5cf0e7292/density-measurement-and-plots/greedymini_density.ipynb)).
