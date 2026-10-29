# DNA Minimizer Density Improvement at `(w = 12, k = 4)`: `0.136046 -> 0.133629` (`-1.776%` Relative)

## What

An explicit binary-projected DNA minimizer rank order object/w12_k4_improved.gm (136 bytes, sha256 537faa127958cbb7f10b0e90c8832449b375b2fad8360bfd4c7e596eee187bc4, rank vector [15, 6, 7, 12, 10, 4, 11, 3, 0, 1, 8, 9, 14, 2, 13, 5]) for (w, k) = (12, 4) with exact expected DNA density 573,933,439 / 2^32 = 0.1336292920, strictly lowering the smallest listed value for expected DNA density 584,312,429 / 2^32 = 0.1360458389 across OrensteinLab/10-minimizers and OrensteinLab/GreedyMini by 1.776274% relative at identical 136-byte storage cost.

- **Target ID:** `minimizer-density-record-tables` (`biology`)
- **Parameters:** $w = 12, k = 4$
- **Minimizer rank file (`.gm` format):** `object/w12_k4_improved.gm` (`136` bytes, `sha256: 537faa127958cbb7f10b0e90c8832449b375b2fad8360bfd4c7e596eee187bc4`)
- **CSV rank table (`GreedyMini --mode export --save_format csv`):** `object/w12_k4_improved.csv` (`129` bytes, `sha256: e542885cc0668c8fa166514faccbba226ccaa833fc352df9d5b17aaf2537078b`)
- **Rank vector (`0000..1111`):** `[15, 6, 7, 12, 10, 4, 11, 3, 0, 1, 8, 9, 14, 2, 13, 5]`
- **Exact expected DNA density (`prob_gc_dna` and 4-ary de Bruijn DP):** $\frac{573,933,439}{2^{32}} \approx 0.1336292920$ (density factor $(w+1) \cdot d = 1.7371807962$)
- **Storage cost:** `136` bytes on disk (`8`-byte `size_t` length prefix `16` + $16 \times 8$-byte `uint64_t` ranks, identical to `OrensteinLab/GreedyMini`'s precomputed `w12_k4.gm`), or `64` bits ($16 \times 4$ bits) of rank information.

## Check It Yourself

From the root of this package directory, run:

```bash
sh verify-it-yourself/run_checks.sh
```

This fetches the upstream reference table `k_extension_k16_w12.csv` (`sha256: 88c4f8fcd0ea6d4308f4e1fc716bb901ea78d3c6112b7e70d4af42bb631bf2fa`) and precomputed `w12_k4.gm` (`sha256: 7c04487e1489e8d37302230424f32522f3c9af537680c6319009fb49ef180131`) at pinned commit `916daebd399d15d061e2fd437326aee5cf0e7292` (stopping on any SHA-256 mismatch), runs `verify-it-yourself/author_checker_minimizer_check.py` on `object/w12_k4_improved.gm`, verifies exact expected DNA density via both high-bit/low-bit bit-plane enumeration (`573,933,439 / 2^32 = 0.1336292920`) and 4-ary de Bruijn transfer-matrix DP (`573,933,439 / 2^32 = 0.1336292920`), and prints `PASS` on the final line in ~1.2 seconds.

## Compared To

- **`OrensteinLab/GreedyMini` & `OrensteinLab/10-minimizers` Precomputed `w12_k4.gm` (`sha256: 7c04487e1489e8d37302230424f32522f3c9af537680c6319009fb49ef180131`, recorded in `the-record-we-beat/minimizer_record_snapshot.md`):**
  - Exact expected DNA density (`prob_gc_dna`): `584,312,429 / 2^32 = 0.1360458389` (the smallest listed value `0.136046` in `k_extension_k16_w12.csv`).
  - Our order reduces gamechanger windows by `-10,378,990` out of $4^{16} = 4,294,967,296$ (**`-1.776274%` relative**, exceeding the `0.5%` relative threshold by `3.55x`).
- **All Listed Methods in `k_extension_k16_w12.csv` (`OrensteinLab/10-minimizers`, column `4`, recorded in `the-record-we-beat/minimizer_record_snapshot.md`):**
  - `GreedyMini`: `0.136046` (smallest listed value; `-1.7764%` relative)
  - `angle-based`: `0.138322748` (`-3.3931%` relative)
  - `decycling`: `0.143956` (`-7.1735%` relative)
  - `double decycling`: `0.145236` (`-7.9916%` relative)
  - `miniception`, `mod-minimizer`, `open-close-syncmer`: `0.156164` (`-14.4302%` relative)
- **Additional Baselines Computed by Us (not listed in `k_extension_k16_w12.csv`):**
  - `ABB+` (our own exact 4-ary DP computation from the scheme definition in `OrensteinLab/10-minimizers`): `591,565,027 / 2^32 = 0.1377344660` (`-2.9805%` relative)
  - `One-zero` / `10-minimizer` (our own exact 4-ary DP computation from the scheme definition in `OrensteinLab/10-minimizers`): `606,522,331 / 2^32 = 0.1412169847` (`-5.3731%` relative)

## Not Claimed

- We do not claim global optimality over arbitrary 4-ary orders of size $4^4 = 256$; `object/w12_k4_improved.gm` is an explicit binary-projected `.gm` order of size $2^4 = 16$ (`136` bytes).
- *(Unverified remark)* Although our exploratory sweep with `how-we-built-it/sos_dna_optimizer.cpp` observed improvements across 17 `(w, k)` precomputed `.gm` cells by $\ge 0.5\%$ relative (up to `-4.274%` at $w=8, k=3$), that 17-cell remark is **unverified**; this submission package claims and certifies only the explicit order `object/w12_k4_improved.gm` for $(w, k) = (12, 4)$.

## Credits

- **Credit:** `mizopl` (`@mizopl`)
- **GreedyMini:** Golan, Tziony, Kraus, Orenstein, and Shur (*Bioinformatics*, 2025) — [`OrensteinLab/GreedyMini`](https://github.com/OrensteinLab/GreedyMini) (pinned commit [`a67eb90dc278ea78111a76d5813cf2ac7662b0ae`](https://github.com/OrensteinLab/GreedyMini/tree/a67eb90dc278ea78111a76d5813cf2ac7662b0ae), upstream C++ evaluator [`code/density_and_gc.cpp`](https://github.com/OrensteinLab/GreedyMini/blob/a67eb90dc278ea78111a76d5813cf2ac7662b0ae/code/density_and_gc.cpp)).
- **10-minimizers:** Shur, Tziony, and Orenstein (*WABI*, 2026) — [`OrensteinLab/10-minimizers`](https://github.com/OrensteinLab/10-minimizers) (pinned commit [`916daebd399d15d061e2fd437326aee5cf0e7292`](https://github.com/OrensteinLab/10-minimizers/tree/916daebd399d15d061e2fd437326aee5cf0e7292), upstream density notebook [`density-measurement-and-plots/greedymini_density.ipynb`](https://github.com/OrensteinLab/10-minimizers/blob/916daebd399d15d061e2fd437326aee5cf0e7292/density-measurement-and-plots/greedymini_density.ipynb)).
