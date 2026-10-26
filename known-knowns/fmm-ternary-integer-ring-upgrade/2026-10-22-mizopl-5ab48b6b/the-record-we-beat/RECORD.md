# The Record We Beat: 7 Ternary (`ZT`) & Integer (`Z`) Fast Matrix Multiplication Upgrades (`fmm-ternary-integer-ring-upgrade`)

## 1. Summary Comparison Against Live `dronperminov/FastMatrixMultiplication` Table

| Format | Claimed File | Ring | Live `ZT` Rank | Live `Z` Rank | Live `Q` / `fmm_sota` Rank | Our Rank | Delta vs Live `ZT` | Delta vs Live `Z` | `ZT > Z` Gap Status |
|---|---|---|---|---|---|---|---|---|---|
| `6x12x14` | `object/6x12x14_m654_ZT.json` | `ZT` | `666` | `654` | `645` | **`654`** | **`-12`** | `0` | **Closed to `0`** |
| `9x10x13` | `object/9x10x13_m763_ZT.json` | `ZT` | `771` | `763` | `758` | **`763`** | **`-8`** | `0` | **Closed to `0`** |
| `9x10x16` | `object/9x10x16_m920_ZT.json` | `ZT` | `924` | `920` | `916` | **`920`** | **`-4`** | `0` | **Closed to `0`** |
| `10x15x16` | `object/10x15x16_m1484_ZT.json` | `ZT` | `1,488` | `1,484` | `1,482` | **`1,484`** | **`-4`** | `0` | **Closed to `0`** |
| `11x15x16` | `object/11x15x16_m1629_ZT.json` | `ZT` | `1,641` (`README.md`) / `1,632` (`status.json`) | `1,629` | `1,605` | **`1,629`** | **`-12`** (`-3` vs `status.json`) | `0` | **Closed to `0`** |
| `12x13x16` | `object/12x13x16_m1546_ZT.json` | `ZT` | `1,548` | `1,544` | `1,509` | **`1,546`** | **`-2`** | `+2` | Reduced from `4` to `2` |
| `12x13x16` | `object/12x13x16_m1541_Z.json` | `Z` | `1,548` | `1,544` | `1,509` | **`1,541`** | — | **`-3`** | New integer `Z` record |

All 7 schemes satisfy the target criteria:
1. Every ternary (`ZT`) claim has rank `r` strictly less than the live `ZT` rank (`654 < 666`, `763 < 771`, `920 < 924`, `1484 < 1488`, `1629 < 1632 < 1641`, `1546 < 1548`), and the integer (`Z`) claim `12x13x16_m1541_Z.json` has rank `r = 1541 < 1544`.
2. Every rank `r` is greater than or equal to the format's overall rational `Q` / `fmm_sota.json` rank (`654 >= 645`, `763 >= 758`, `920 >= 916`, `1484 >= 1482`, `1629 >= 1605`, `1546 >= 1509`, `1541 >= 1509`), so none crosses into `fmm-catalogue-small-format-rank`.
3. None of these 7 schemes exists in `dronperminov/FastMatrixMultiplication` (`schemes/results/ZT/` or `schemes/results/Z/`) or in `MerlijnW70/fmm-schemes`. Five of the six `ZT` format upgrades (`9x10x13`, `9x10x16`, `10x15x16`, `11x15x16`, and `12x13x16 ZT`) also have zero overlap with any open or merged PR on `elder-plinius/V3R1T4S` (for transparency, open V3R1T4S PR `#356` independently addresses `6x12x14 ZT 654` and open PR `#412` addresses `12x13x16 Z`).
4. All `29,648,196` Brent equations across the 7 schemes hold identically over $\mathbb{Z}$ in exact 64-bit integer arithmetic (`0` mismatches).

## 2. Primary Live Table Fetches (UTC Time, URL, HTTP Status, Bytes, SHA-256)

1. **Perminov FastMatrixMultiplication `README.md`**
   - **URL:** `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md`
   - **Fetched UTC:** `2026-10-22T02:23:22Z`
   - **HTTP status:** `200`
   - **Bytes:** `112,906`
   - **SHA-256:** `5f8eb46827fd667f0200990f0e91d2f439db13f6555f63eeecbb39bc7b9fc17e`
   - **Note on upstream merge of our Part I schemes:** Commit `b4f756b` ("Update table with best known schemes", `2026-10-21`) in `dronperminov/FastMatrixMultiplication` officially merged our 4 earlier ternary schemes (`9x12x14:954`, `10x15x15:1389`, `12x15x15:1640`, `14x15x15:1894`) into `schemes/known/mizopl/` and credited `mizopl` in `README.md`.
   - **Exact live rows in `README.md` (`Format | ZT rank | Z rank | Q rank | omega`):**
     ```text
     | `6x12x14`  |  666 (20)   |   654 (22)   |   645 (28)   | **2.813019801** |
     | `9x10x13`  |  771 (28)   |   763 (31)   |   758 (59)   | **2.811748807** |
     | `9x10x16`  |  924 (31)   |   920 (28)   |   916 (28)   | **2.801574074** |
     | `10x15x16` | 1488 (560)  |  1484 (44)   |  1482 (123)  | **2.813987693** |
     | `11x15x16` | 1641 (144)  |  1629 (45)   |  1605 (71)   | **2.805860166** |
     | `12x13x16` | 1548 (185)  |  1544 (68)   |  1509 (84)   | **2.796627014** |
     ```

2. **Perminov FastMatrixMultiplication `schemes/status.json`**
   - **URL:** `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/status.json`
   - **Fetched UTC:** `2026-10-22T02:23:23Z`
   - **HTTP status:** `200`
   - **Bytes:** `2,180,006`
   - **SHA-256:** `8f129ee5cf9683c769de46143323219eeebbc7fed24b201cc02a22f4a851cf1c`
   - **Exact `ranks` entries in `schemes/status.json`:**
     - `6x12x14`: `{"ZT": 666, "Z": 654, "Q": 645}`
     - `9x10x13`: `{"ZT": 771, "Z": 763, "Q": 758}`
     - `9x10x16`: `{"ZT": 924, "Z": 920, "Q": 916}`
     - `10x15x16`: `{"ZT": 1488, "Z": 1484, "Q": 1482}`
     - `11x15x16`: `{"ZT": 1632, "Z": 1629, "Q": 1605}` (`1641` in live `README.md`)
     - `12x13x16`: `{"ZT": 1548, "Z": 1544, "Q": 1509}`

3. **Sedoglavic `fmm_sota.json`**
   - **URL:** `https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json`
   - **Fetched UTC:** `2026-10-22T02:23:23Z`
   - **HTTP status:** `200`
   - **Bytes:** `343,774`
   - **SHA-256:** `2a6535154ac877aeb495f9294a5e97c3dbf1b1969aefe6ffc0a612f2cf01cbae`
   - **Exact `fmm_sota.json` entries:** `[6, 12, 14]: 645`, `[9, 10, 13]: 758`, `[9, 10, 16]: 916`, `[10, 15, 16]: 1482`, `[11, 15, 16]: 1605`, `[12, 13, 16]: 1509`.
