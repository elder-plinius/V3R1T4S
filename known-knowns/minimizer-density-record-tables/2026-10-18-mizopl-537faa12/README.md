# DNA Minimizer Density Improvement at `(w = 12, k = 4)`: `0.136046 -> 0.133629` (`-1.776%` Relative)

## What

An explicit binary-projected DNA minimizer rank order claim/w12_k4_improved.gm (136 bytes, sha256 537faa127958cbb7f10b0e90c8832449b375b2fad8360bfd4c7e596eee187bc4, rank vector [15, 6, 7, 12, 10, 4, 11, 3, 0, 1, 8, 9, 14, 2, 13, 5]) for (w, k) = (12, 4) with exact expected DNA density 573,933,439 / 2^32 = 0.1336292920, strictly lowering the best known expected DNA density 584,312,429 / 2^32 = 0.1360458389 across OrensteinLab/10-minimizers and OrensteinLab/GreedyMini by 1.776274% relative at identical 136-byte storage cost.

- **Target ID:** `minimizer-density-record-tables` (`biology`)
- **Parameters:** $w = 12, k = 4$
- **Minimizer rank file (`.gm` format):** `object/w12_k4_improved.gm` (`136` bytes, `sha256: 537faa127958cbb7f10b0e90c8832449b375b2fad8360bfd4c7e596eee187bc4`)
- **CSV rank table (`GreedyMini --mode export --save_format csv`):** `object/w12_k4_improved.csv` (`129` bytes, `sha256: e542885cc0668c8fa166514faccbba226ccaa833fc352df9d5b17aaf2537078b`)
- **Rank vector (`0000..1111`):** `[15, 6, 7, 12, 10, 4, 11, 3, 0, 1, 8, 9, 14, 2, 13, 5]`
- **Exact expected DNA density (`prob_gc_dna` and 4-ary de Bruijn DP):** $\frac{573,933,439}{2^{32}} \approx 0.1336292920$ (density factor $(w+1) \cdot d = 1.7371807960$)
- **Storage cost:** `136` bytes on disk (`8`-byte `size_t` length prefix `16` + $16 \times 8$-byte `uint64_t` ranks, identical to `OrensteinLab/GreedyMini`'s precomputed `w12_k4.gm`), or `64` bits ($16 \times 4$ bits) of rank information.

## Check It Yourself

From the root of this package directory, run:

```bash
sh verify-it-yourself/run_checks.sh
```

This runs the standalone Python verifier `verify-it-yourself/author_checker_minimizer_check.py` on `object/w12_k4_improved.gm`, `the-record-we-beat/published_w12_k4.gm`, and `the-record-we-beat/k_extension_k16_w12.csv`, verifying exact expected DNA density via both `prob_gc_dna` (`573,933,439 / 2^32 = 0.1336292920`) and 4-ary de Bruijn transfer-matrix DP (`573,933,439 / 2^32 = 0.1336292920`), plus empirical sampling via `10-minimizers`'s `random_density_function_dna_includes_tiebreaking`, and prints `PASS` on the final line in ~1.5 seconds.

## Compared To

- **`OrensteinLab/GreedyMini` & `OrensteinLab/10-minimizers` Precomputed `w12_k4.gm` (`the-record-we-beat/published_w12_k4.gm`, `sha256: 7c04487e1489e8d37302230424f32522f3c9af537680c6319009fb49ef180131`):**
  - Exact expected DNA density (`prob_gc_dna`): `584,312,429 / 2^32 = 0.1360458389` (listed as `0.136046` in `k_extension_k16_w12.csv`).
  - Our order reduces gamechanger windows by `-10,378,990` out of $4^{16} = 4,294,967,296$ (**`-1.776274%` relative**, exceeding the `0.5%` relative threshold by `3.55x`).
- **All Published Methods in `k_extension_k16_w12.csv` (`OrensteinLab/10-minimizers`, column `4`) and `minimizer_density_comparison.ipynb`:**
  - `GreedyMini`: `0.136046` (`-1.7764%` relative)
  - `ABB+` (`minimizer_density_comparison.ipynb`, exact 4-ary DP): `591,565,027 / 2^32 = 0.1377344660` (`-2.9805%` relative)
  - `angle-based`: `0.138322748` (`-3.3931%` relative)
  - `One-zero` / `10-minimizer` (`minimizer_density_comparison.ipynb`, exact 4-ary DP): `606,522,331 / 2^32 = 0.1412169847` (`-5.3731%` relative)
  - `decycling`: `0.143956` (`-7.1735%` relative)
  - `double decycling`: `0.145236` (`-7.9916%` relative)
  - `miniception`, `mod-minimizer`, `open-close-syncmer`: `0.156164` (`-14.4302%` relative)

## Not Claimed

- We do not claim global optimality over arbitrary 4-ary orders of size $4^4 = 256$; `object/w12_k4_improved.gm` is an explicit binary-projected `.gm` order of size $2^4 = 16$ (`136` bytes).
- Although our SOS-DP optimizer `how-we-built-it/sos_dna_optimizer.cpp` strictly improved 17 `(w, k)` precomputed `.gm` cells by $\ge 0.5\%$ relative (up to `-4.274%` at $w=8, k=3$), this submission package claims and certifies the explicit order `object/w12_k4_improved.gm` for $(w, k) = (12, 4)$.

## Credits

- **Credit:** `mizopl` (`@mizopl`)
- **Benchmark & Repositories:** Golomb, Orenstein, et al. (`OrensteinLab/GreedyMini` and `OrensteinLab/10-minimizers`).
