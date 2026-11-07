# DNA Minimizer Density Improvement at `(w = 12, k = 4)`: `0.133718 -> 0.132770` (`-0.7085%` vs `Minimizers`, `-2.4076%` vs `10-minimizers`)

## What

An explicit 256-entry 4-ary DNA minimizer rank order object/w12_k4_4ary.gm (2,056 bytes, sha256 956170573df55e04f43e55c20d6bba0b134c9b8054a92f995428dc9df4410ddb) and companion CSV table object/w12_k4_4ary.csv (4,518 bytes, sha256 72557c44cc3c4b10d4735faeee9d6745f40872674c54118a311e258f775431d1) for (w, k) = (12, 4) with exact expected DNA density 570,244,411 / 2^32 = 0.1327703733 (density factor 1.7260148523), strictly lowering the smallest listed value in OrensteinLab/Minimizers lowest-density/binary/best-orders.csv (k4-w12.txt, 574,313,157 / 2^32 = 0.1337177020) by 0.7085% relative and lowering OrensteinLab/10-minimizers w12_k4.gm (584,312,429 / 2^32 = 0.1360458389) by 2.4076% relative.

- **Target ID:** `minimizer-density-record-tables` (`biology`)
- **Parameters:** $w = 12, k = 4$ (DNA alphabet $\sigma = 4$, $4^4 = 256$ DNA 4-mers)
- **Minimizer rank file (`.gm` format):** `object/w12_k4_4ary.gm` (`2,056` bytes, `sha256: 956170573df55e04f43e55c20d6bba0b134c9b8054a92f995428dc9df4410ddb`)
- **Companion CSV rank table:** `object/w12_k4_4ary.csv` (`4,518` bytes, `sha256: 72557c44cc3c4b10d4735faeee9d6745f40872674c54118a311e258f775431d1`)
- **DNA 4-mer indexing convention:** Each DNA nucleotide $c \in \{A, C, G, T\}$ is encoded in 2 bits as $0, 1, 2, 3$ (`00, 01, 10, 11`), read most-significant base first ($x = \sum_{i=0}^3 c_i 4^{3-i} \in \{0, \dots, 255\}$), with strict rank `rank[x]` in `0..255` and leftmost tie-breaking when the same 4-mer repeats in a window.
- **Exact expected DNA density:** $\frac{570,244,411}{2^{32}} \approx 0.1327703733$ ($283,110,423$ prefix gamechangers + $287,133,988$ suffix gamechangers out of $4^{16} = 4,294,967,296$ DNA contexts; density factor $(w+1) \cdot d = 1.7260148523$).
- **Storage cost:** `2,056` bytes on disk in `.gm` 64-bit vector format (`8`-byte `size_t` length prefix `256` + $256 \times 8$-byte `uint64_t` ranks), or `256` bytes ($256 \times 8$ bits) as an unpacked 1-byte rank lookup table.

## Check It Yourself

From the root of this package directory, run:

```bash
sh verify-it-yourself/run_checks.sh
```

This fetches the upstream precalculated order `k4-w12.txt` (`sha256: 9a8f7447e569399a594588e695a963da59078b34cf4aac23a6fd3d998d06d877`) from `OrensteinLab/Minimizers` at pinned commit `7b9430fce07a1fcf6b0fe023e9c7c135d6a5bf46` as well as `k_extension_k16_w12.csv` (`sha256: 88c4f8fcd0ea6d4308f4e1fc716bb901ea78d3c6112b7e70d4af42bb631bf2fa`) and `w12_k4.gm` (`sha256: 7c04487e1489e8d37302230424f32522f3c9af537680c6319009fb49ef180131`) from `OrensteinLab/10-minimizers` at pinned commit `916daebd399d15d061e2fd437326aee5cf0e7292` (stopping on any SHA-256 mismatch), runs `verify-it-yourself/verify.py` on `object/w12_k4_4ary.gm` and `object/w12_k4_4ary.csv`, verifies exact expected DNA density via two independent 4-ary de Bruijn transfer-matrix DP algorithms (`570,244,411 / 2^32 = 0.1327703733`), and prints `PASS` on the final line in ~2 seconds.

## Compared To

- **`OrensteinLab/Minimizers` Lowest-Density Order (`lowest-density/binary/best-orders.csv` `sha256: 57a369a010498cb6ab3ba0bce73ed015980a11a8c8c29f09d537db34e3e32313` and `lowest-density/binary/individual-orders/ranks/k4-w12.txt` `sha256: 9a8f7447e569399a594588e695a963da59078b34cf4aac23a6fd3d998d06d877`, recorded in `the-record-we-beat/minimizer_record_snapshot.md`):**
  - Precalculated binary order for $k=4, w=12$ (UHS size 7: `[3, 16, 2, 16, 16, 4, 1, 0, 16, 16, 16, 16, 16, 16, 5, 6]`), extended to DNA as described in the `GreedyMini` README (`136` bytes in `.gm` format, or `16` bytes unpacked): exact expected DNA density `574,313,157 / 2^32 = 0.1337177020`.
  - Required `>= 0.5%` relative threshold below `0.1337177020`: `<= 0.1330491135` (`<= 571,441,591 / 2^32`).
  - Our direct 4-ary DNA order `object/w12_k4_4ary.gm` achieves `570,244,411 / 2^32 = 0.1327703733`, reducing gamechanger contexts by `-4,068,746` out of $4^{16} = 4,294,967,296$ (**`-0.7085%` relative**, clearing the `0.5%` relative bar by `1,197,180` contexts).
- **`OrensteinLab/GreedyMini` & `OrensteinLab/10-minimizers` Precomputed `w12_k4.gm` (`sha256: 7c04487e1489e8d37302230424f32522f3c9af537680c6319009fb49ef180131`, recorded in `the-record-we-beat/minimizer_record_snapshot.md`):**
  - Exact expected DNA density (`prob_gc_dna`): `584,312,429 / 2^32 = 0.1360458389` (the smallest listed value `0.136046` in `k_extension_k16_w12.csv`).
  - Our order reduces gamechanger contexts by `-14,068,018` out of $4^{16}$ (**`-2.4076%` relative**).
- **All Listed Methods in `k_extension_k16_w12.csv` (`OrensteinLab/10-minimizers`, column `4`, recorded in `the-record-we-beat/minimizer_record_snapshot.md`):**
  - `GreedyMini`: `0.136046` (smallest listed value in `k_extension_k16_w12.csv`; `-2.4077%` relative)
  - `angle-based`: `0.138322748` (`-4.0141%` relative)
  - `decycling`: `0.143956` (`-7.7702%` relative)
  - `double decycling`: `0.145236` (`-8.5830%` relative)
  - `miniception`, `mod-minimizer`, `open-close-syncmer`: `0.156164` (`-14.9802%` relative)
- **Additional Baselines Computed by Us (not listed in `k_extension_k16_w12.csv`):**
  - Optimal binary-projected `.gm` order `[15, 6, 7, 12, 10, 4, 11, 3, 0, 1, 8, 9, 14, 2, 13, 5]` (our own computation within the 16-entry binary-projected subspace): `573,933,439 / 2^32 = 0.1336292920` (`-0.6428%` relative)
  - `ABB+` (our own exact 4-ary DP computation from the scheme definition in `OrensteinLab/10-minimizers`): `591,565,027 / 2^32 = 0.1377344660` (`-3.6041%` relative)
  - `One-zero` / `10-minimizer` (our own exact 4-ary DP computation from the scheme definition in `OrensteinLab/10-minimizers`): `606,522,331 / 2^32 = 0.1412169847` (`-5.9813%` relative)

## Not Claimed

- We do not claim global optimality over all $256!$ permutations of the 256 DNA 4-mers; `object/w12_k4_4ary.gm` is an explicit 256-entry 4-ary DNA rank order obtained by local swap optimization (`how-we-built-it/opt_4ary_dna.cpp`).
- Unlike 16-entry binary-projected `.gm` orders (`136` bytes), which assign primary ranks only to the 16 high-bit 4-mers and break ties lexicographically on the 16 low-bit 4-mers, `object/w12_k4_4ary.gm` stores an explicit 256-entry rank table over all $4^4 = 256$ DNA 4-mers (`2,056` bytes in `.gm` 64-bit format, or `256` bytes unpacked).

## Credits

- **Credit:** `mizopl` (`@mizopl`)
- **GreedyMini & Minimizers:** Golan, Tziony, Kraus, Orenstein, and Shur (*Bioinformatics*, 2025) — [`OrensteinLab/Minimizers`](https://github.com/OrensteinLab/Minimizers) (pinned commit [`7b9430fce07a1fcf6b0fe023e9c7c135d6a5bf46`](https://github.com/OrensteinLab/Minimizers/tree/7b9430fce07a1fcf6b0fe023e9c7c135d6a5bf46)) and [`OrensteinLab/GreedyMini`](https://github.com/OrensteinLab/GreedyMini) (pinned commit [`a67eb90dc278ea78111a76d5813cf2ac7662b0ae`](https://github.com/OrensteinLab/GreedyMini/tree/a67eb90dc278ea78111a76d5813cf2ac7662b0ae), upstream C++ evaluator [`code/density_and_gc.cpp`](https://github.com/OrensteinLab/GreedyMini/blob/a67eb90dc278ea78111a76d5813cf2ac7662b0ae/code/density_and_gc.cpp)).
- **10-minimizers:** Shur, Tziony, and Orenstein (*WABI*, 2026) — [`OrensteinLab/10-minimizers`](https://github.com/OrensteinLab/10-minimizers) (pinned commit [`916daebd399d15d061e2fd437326aee5cf0e7292`](https://github.com/OrensteinLab/10-minimizers/tree/916daebd399d15d061e2fd437326aee5cf0e7292), upstream density notebook [`density-measurement-and-plots/greedymini_density.ipynb`](https://github.com/OrensteinLab/10-minimizers/blob/916daebd399d15d061e2fd437326aee5cf0e7292/density-measurement-and-plots/greedymini_density.ipynb)).
