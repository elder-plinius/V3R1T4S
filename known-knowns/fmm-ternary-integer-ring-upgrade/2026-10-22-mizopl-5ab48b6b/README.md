# Seven Ternary (`ZT`) & Integer (`Z`) Fast Matrix Multiplication Upgrades (`fmm-ternary-integer-ring-upgrade`)

## What

Seven explicit bilinear fast matrix multiplication schemes (6 in ZT = {-1, 0, 1} and 1 in Z) verified in exact 64-bit integer arithmetic across all 29,648,196 Brent equations over Z with 0 mismatches: object/6x12x14_m654_ZT.json (rank 654 vs live ZT 666, -12, sha256 5ab48b6b88fd1a7b9fbe8c81670522bd45f290e580be8a4443751e208f2f2bc4), object/9x10x13_m763_ZT.json (rank 763 vs live ZT 771, -8, sha256 a351d9eef1a62ff9ab7a300e67928a880200e9fcb4ba7f3accffc900e99c1923), object/9x10x16_m920_ZT.json (rank 920 vs live ZT 924, -4, sha256 42ad6efd9f8b6aab2320058835d85c565300f616d007b57535bf1968c0cb0076), object/10x15x16_m1484_ZT.json (rank 1484 vs live ZT 1488, -4, sha256 02199a88ebd24b1457c5cae7a5a2dcb895aa396ada9e5daaf0ea1cc4846d09d3), object/11x15x16_m1629_ZT.json (rank 1629 vs live ZT 1641, -12, sha256 0d2eb6e651f61c7c9fa5d137eb4813f37f287016eaa91e95deae53107016b288), object/12x13x16_m1546_ZT.json (rank 1546 vs live ZT 1548, -2, sha256 b639c891628cd5e5042311d19adfa2c29eff95d6c0b1077466c36ce3204e796a), and object/12x13x16_m1541_Z.json (rank 1541 vs live Z 1544, -3, sha256 911599680fd3bbe0558dbf7fe5e0886deb863c4244915812d28404156660f780).

- **Target:** `fmm-ternary-integer-ring-upgrade` (`algorithms`)
- **Claim level:** `solution_claim` (`CONFIRMED_SOLUTION`)
- **Upstream Context:** Follows up on our 4 earlier ternary schemes merged upstream into [`dronperminov/FastMatrixMultiplication`](https://github.com/dronperminov/FastMatrixMultiplication) in commit [`b4f756b`](https://github.com/dronperminov/FastMatrixMultiplication/commit/b4f756b) (`schemes/known/mizopl/`: `9x12x14:954`, `10x15x15:1389`, `12x15x15:1640`, `14x15x15:1894`; V3R1T4S PRs [#402](https://github.com/elder-plinius/V3R1T4S/pull/402) and [#432](https://github.com/elder-plinius/V3R1T4S/pull/432)).
- **Master Certificate:** `object/CERTIFICATE.json` (`7,788` bytes, `sha256: 4050811589871e8e0b91e766d8587a39fe00649cce86b6e1fb974e755aae0bcf`)
- **Primary Object:** `object/6x12x14_m654_ZT.json` (`114,018` bytes, `sha256: 5ab48b6b88fd1a7b9fbe8c81670522bd45f290e580be8a4443751e208f2f2bc4`)

| File | Format | Ring | Claimed Rank (`m`) | Live `ZT` Rank | Live `Z` Rank | Live `Q` / `fmm_sota` Rank | Delta vs Live `ZT` | Delta vs Live `Z` | `max_abs` | Naive Complexity | Nonzeros (`U / V / W / Total`) | Exact Brent Equations | Bytes | SHA-256 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `object/6x12x14_m654_ZT.json` | `6x12x14` | `ZT` | **`654`** | `666` | `654` | `645` | **`-12`** | `0` | `1` | `13,241` | `4,149 / 5,477 / 5,007 / 14,633` | `1,016,064` | `114,018` | `5ab48b6b88fd1a7b9fbe8c81670522bd45f290e580be8a4443751e208f2f2bc4` |
| `object/9x10x13_m763_ZT.json` | `9x10x13` | `ZT` | **`763`** | `771` | `763` | `758` | **`-8`** | `0` | `1` | `14,116` | `4,852 / 5,069 / 5,838 / 15,759` | `1,368,900` | `123,209` | `a351d9eef1a62ff9ab7a300e67928a880200e9fcb4ba7f3accffc900e99c1923` |
| `object/9x10x16_m920_ZT.json` | `9x10x16` | `ZT` | **`920`** | `924` | `920` | `916` | **`-4`** | `0` | `1` | `17,397` | `5,856 / 6,056 / 7,469 / 19,381` | `2,073,600` | `153,081` | `42ad6efd9f8b6aab2320058835d85c565300f616d007b57535bf1968c0cb0076` |
| `object/10x15x16_m1484_ZT.json` | `10x15x16` | `ZT` | **`1,484`** | `1,488` | `1,484` | `1,482` | **`-4`** | `0` | `1` | `28,160` | `11,226 / 10,136 / 9,926 / 31,288` | `5,760,000` | `254,512` | `02199a88ebd24b1457c5cae7a5a2dcb895aa396ada9e5daaf0ea1cc4846d09d3` |
| `object/11x15x16_m1629_ZT.json` | `11x15x16` | `ZT` | **`1,629`** | `1,641` (`1,632` in `status.json`) | `1,629` | `1,605` | **`-12`** (`-3`) | `0` | `1` | `39,490` | `14,532 / 14,854 / 13,538 / 42,924` | `6,969,600` | `349,814` | `0d2eb6e651f61c7c9fa5d137eb4813f37f287016eaa91e95deae53107016b288` |
| `object/12x13x16_m1546_ZT.json` | `12x13x16` | `ZT` | **`1,546`** | `1,548` | `1,544` | `1,509` | **`-2`** | `+2` | `1` | `64,887` | `18,520 / 25,516 / 24,135 / 68,171` | `6,230,016` | `547,710` | `b639c891628cd5e5042311d19adfa2c29eff95d6c0b1077466c36ce3204e796a` |
| `object/12x13x16_m1541_Z.json` | `12x13x16` | `Z` | **`1,541`** | `1,548` | `1,544` | `1,509` | — | **`-3`** | `2` | `64,983` | `18,608 / 25,480 / 24,169 / 68,257` | `6,230,016` | `548,395` | `911599680fd3bbe0558dbf7fe5e0886deb863c4244915812d28404156660f780` |

## Check It Yourself

Run the standalone exhaustive checker from the root of this package (~3 seconds):

```sh
sh verify-it-yourself/run_checks.sh
```

It runs a positive control (Strassen `2x2x2` rank 7) and two negative controls (corrupted Brent tensor and non-ternary coefficient `2`), verifies the SHA-256 digests, dimensions, coefficient bounds, non-degeneracy, and all `29,648,196` exact integer Brent equations over `Z` across all 7 scheme files in `object/`, and prints `PASS` on its final line.

## Compared To

- **Perminov FastMatrixMultiplication table (`https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md`, fetched `2026-10-22T02:23:22Z`, `112,906` bytes, `sha256: 5f8eb46827fd667f0200990f0e91d2f439db13f6555f63eeecbb39bc7b9fc17e`, and `schemes/status.json`, fetched `2026-10-22T02:23:23Z`, `2,180,006` bytes, `sha256: 8f129ee5cf9683c769de46143323219eeebbc7fed24b201cc02a22f4a851cf1c`):**
  - `6x12x14`: `ZT = 666`, `Z = 654`, `Q = 645` $\to$ our `ZT = 654` (`-12`, closes `ZT > Z` gap to `0`)
  - `9x10x13`: `ZT = 771`, `Z = 763`, `Q = 758` $\to$ our `ZT = 763` (`-8`, closes `ZT > Z` gap to `0`)
  - `9x10x16`: `ZT = 924`, `Z = 920`, `Q = 916` $\to$ our `ZT = 920` (`-4`, closes `ZT > Z` gap to `0`)
  - `10x15x16`: `ZT = 1,488`, `Z = 1,484`, `Q = 1,482` $\to$ our `ZT = 1,484` (`-4`, closes `ZT > Z` gap to `0`)
  - `11x15x16`: `ZT = 1,641` (`1,632` in `status.json`), `Z = 1,629`, `Q = 1,605` $\to$ our `ZT = 1,629` (`-12` vs `README.md`, `-3` vs `status.json`, closes `ZT > Z` gap to `0`)
  - `12x13x16`: `ZT = 1,548`, `Z = 1,544`, `Q = 1,509` $\to$ our `ZT = 1,546` (`-2` in `ZT`) and `Z = 1,541` (`-3` in `Z`)
- **Sedoglavic `fmm_sota.json` (`https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json`, fetched `2026-10-22T02:23:23Z`, `343,774` bytes, `sha256: 2a6535154ac877aeb495f9294a5e97c3dbf1b1969aefe6ffc0a612f2cf01cbae`):** Overall best (`Q`) ranks are `645`, `758`, `916`, `1,482`, `1,605`, and `1,509` respectively (`654 >= 645`, `763 >= 758`, `920 >= 916`, `1,484 >= 1,482`, `1,629 >= 1,605`, `1,546 >= 1,509`, `1,541 >= 1,509`).

## Not Claimed

- We do not claim any new rational (`Q`) rank record below the live `Q` / `fmm_sota.json` ranks (`645`, `758`, `916`, `1,482`, `1,605`, `1,509`), which would belong to `fmm-catalogue-small-format-rank`.
- We transparently note that while 5 of the 6 `ZT` upgrades (`9x10x13`, `9x10x16`, `10x15x16`, `11x15x16`, and `12x13x16 ZT`) have zero overlap with any open or merged PR on `elder-plinius/V3R1T4S`, open PR `#356` independently addresses `6x12x14 ZT 654` and open PR `#412` addresses `12x13x16 Z`.

## Credits

- **Contributor:** `mizopl`
- **External data & literature:** Base decompositions and status tables from A. Perminov's `FastMatrixMultiplication` repository (`https://github.com/dronperminov/FastMatrixMultiplication`, arXiv:2606.02480, arXiv:2603.18699) and A. Sedoglavic's `fmm_digest` / Universite de Lille FMM catalogue (`https://fmm.univ-lille.fr`).
