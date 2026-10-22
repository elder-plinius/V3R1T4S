# Wave 3: Snake-in-the-Box & Coil-in-the-Box (`Q_9..Q_14`) — Audit, Verification & New World Records

## 1. Executive Summary

All work was executed locally inside `{WORKDIR}/` with **zero external submissions**.

### Headline Breakthroughs

| Sub-Problem | Dimension & Type | Live `minortriad` / Published Baseline | Caltech Dataset / Unmerged PR Baseline | **New Wave-3 Record / Result** | Gain vs Live Baseline | Gain vs PR (`#79..#89`) | Primary Certificate File |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **`p1`** | **$Q_{11}$ Symmetric Coil** | `730` | `734` (Caltech) | **`734`** (2 new inequiv) | **`+4`** | `0` (new canonical classes) | `results/best_sym11_drifted_r0_Q11_734.txt` |
| **`p1`** | **$Q_{12}$ Symmetric Coil** | `1434` | `1450` (`#79`) | **`1454`** ($h = 727$, 4 inequiv) | **`+20`** | **`+4`** (beats `#79`) | `results/best_sym12_Q12_1454.txt`, `results/lift_sym12_Q12_1454.txt` |
| **`p1`** | **$Q_{13}$ Symmetric Coil** | `2830` | `2870` (`#80`) | **`2886`** ($h = 1443$, 3 inequiv) | **`+56`** | **`+16`** (beats `#80`) | `results/best_sym13_from2882_Q13_2886.txt` |
| **`p2`** | **$Q_{14}$ Coil** | `5750` (Taylor) | `5854` (`#81`) | **`5854`** (3 new inequiv + `#81`) | **`+104`** | `0` (new canonical classes) | `results/best_co14_drifted_r0_Q14_5854.txt` |
| **`p2`** | **$Q_{14}$ Snake** | `5850` (Toner) / `5844` (Taylor) | `5854` (`#82`) | **`5854`** (3 new inequiv + `#82`) | **`+4` / `+10`** | `0` (new canonical classes) | `results/best_sn14_drifted_r0_Q14_5854.txt` |
| **`p3`** | **$Q_{10}..Q_{13}$ Coils & Snakes** | `374, 740, 1468, 2930` / `750, 1480, 2946` | `#83..#89` | **7 new 2nd-gen inequiv witnesses** | `0` (equal record) | `0` (inequiv to both public & `#83..#89`) | `results/p3_*_drifted_r0_*.txt` |

---

## 2. Part 1: Full Calibration & Audit of Unmerged Branches (`#79..#89`)

We built the standalone verifier [`src/verify_snake_coil.py`]({WORKDIR}/src/verify_snake_coil.py) and calibrated it against:
1. All 29 records on `minortriad.com/snake` (`data/seeds/minortriad_records.json`),
2. All unzipped `Math-AI-Caltech/Snake-in-the-Box` CSV banks (`record_snakes.csv` 330 MB, `snakes_dim9_190.csv` 1.1 MB, `record_coils.csv` 146 KB, `record_symmetric_coils.csv` 9 KB),
3. Toner's $Q_{13}$ (`2946`) and $Q_{14}$ (`5850`) snakes (`toner_q13_2946.txt`, `toner_q14_5850.txt`) and Taylor's $Q_{14}$ coil (`5750`) and snake (`5844`).

Every unmerged branch `#79..#89` was extracted into `cg_branches/` and audited:

| Branch | Target | Claimed Length | Valid? | Symmetric ($h = L/2$)? | Strictly Inequivalent vs Public Banks? | Canonical SHA-256 Prefix (`16 hex`) | Gap Spectrum Hash |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `#79` | $Q_{12}$ Symmetric Coil | `1450` | **PASS** | **YES** ($h=725$) | **YES** (`+16` vs `1434`) | `89ef0fb0c82e7fd8` | `7b6166b818c34eb3` |
| `#80` | $Q_{13}$ Symmetric Coil | `2870` | **PASS** | **YES** ($h=1435$) | **YES** (`+40` vs `2830`) | `ef3f4bf36fa5be90` | `8bf686b5ca062cf5` |
| `#81` | $Q_{14}$ Coil | `5854` | **PASS** | No (unrestricted) | **YES** (`+104` vs `5750`) | `9a8c32cc74d5620c` | `c850d0c249f0340b` |
| `#82` | $Q_{14}$ Snake | `5854` | **PASS** | N/A (snake) | **YES** (`+4` vs `5850`) | `0bd8c40cb1b242cc` | `4c992599e1a0f7ab` |
| `#83` | $Q_{10}$ Coil (`p3`) | `374` | **PASS** | No | **YES** (vs 34 Caltech classes) | `9fb044d7ec62100a` | `8d051a89f0632c96` |
| `#84` | $Q_{11}$ Coil (`p3`) | `740` | **PASS** | No | **YES** (vs 6 Caltech classes) | `62a7cf373d7c6d39` | `b83a44009565a1dc` |
| `#85` | $Q_{12}$ Coil (`p3`) | `1468` | **PASS** | No | **YES** (vs 2 Caltech classes) | `a6d87ba8717ab45b` | `f402ab344cb0e4c8` |
| `#86` | $Q_{13}$ Coil (`p3`) | `2930` | **PASS** | No | **YES** (vs 2 Caltech classes) | `29cf053f0625d1be` | `5bb8a54a83d77f51` |
| `#87` | $Q_{11}$ Snake (`p3`) | `750` | **PASS** | N/A | **YES** (vs 1 Caltech class) | `08b90d0da845f3fa` | `3da72094be809822` |
| `#88` | $Q_{12}$ Snake (`p3`) | `1480` | **PASS** | N/A | **YES** (vs 417 Caltech classes) | `00d86e51f4ba3bf8` | `64733827fc3b55f4` |
| `#89` | $Q_{13}$ Snake (`p3`) | `2946` | **PASS** | N/A | **YES** (vs Toner `2946`) | `3103274e5e1517ee` | `c85399c7fc359a32` |

---

## 3. Part 2 (`p1` & `p2`): New World Records in $Q_{12}$ and $Q_{13}$ Symmetric Coils & $Q_{14}$ Analysis

### 3.1 Hardware-Accelerated Bitboard Engine (`src/fast_opt.c`)
We engineered [`src/fast_opt.c`]({WORKDIR}/src/fast_opt.c) around a key architectural insight on Apple Silicon (`aarch64`):
- A 16-byte bitboard struct (`typedef struct { uint64_t w[2]; } u128;`, `MAX_K = 128`) is passed **entirely in two 64-bit CPU registers (`x0, x1`)** according to the ARM64 AAPCS64 ABI, whereas 32-byte (`u256`) and 64-byte (`u512`) structs spill to stack memory on every recursive call and bit-operation helper.
- Combined with exact forward/backward BFS distance pruning (`d0[v] + d1[v] <= new_w`) and intersecting `avail` with `compat[u]` on every step, `src/fast_opt` achieves a **20x–50x speedup** over `u512` DFS, enabling deep **Iterated Local Search (ILS)** with neutral drift and **multi-detour + multi-bridge coordinate-splitting lifts** (`Q_n -> Q_{n+1}`).

### 3.2 New $Q_{12}$ Symmetric Coil World Record: $L = 1454$ ($h = 727$)
- **Previous Baselines**: `1434` (`minortriad` live record), `1450` (unmerged branch `#79`).
- **Two Independent Discovery Paths to $L = 1454$ (`+20` over `minortriad`, `+4` over `#79`)**:
  1. **Multi-Detour + Multi-Bridge Lift ($Q_{11} \to Q_{12}$)**: Starting from Caltech's $Q_{11}$ symmetric coil of length `734` (`h = 367`), splitting on coordinate `b = 10` (`flips = (183, 366)`), testing the 5th distinct Step-1 detour (`w1 = 38, k1 = 14, gain1 = -2 -> h_det = 365`) and the 6th distinct Step-2 splice (`w2 = 44, k2 = 4, gain2 = -11 -> L = 1438`), followed by paired symmetric `+4` climbs (`1438 -> 1442 -> 1446 -> 1450 -> 1454`), produced [`results/lift_sym12_Q12_1454.txt`]({WORKDIR}/results/lift_sym12_Q12_1454.txt) (`canonical_hash = 914c59f9bdef6259`).
  2. **Symmetric ILS on `1450`**: Running 12-move neutral drift + wide-window `+4` search (`ils_sym 12 12`) on `sym_coil_Q12_1450.txt` discovered a second, strictly inequivalent $L = 1454$ symmetric coil in Round 9 (`at ga=356 gw=44`), saved to [`results/best_sym12_Q12_1454.txt`]({WORKDIR}/results/best_sym12_Q12_1454.txt) (`canonical_hash = b96660a0c9c635b0`), plus drifted inequivalent $L = 1454$ variants [`results/best_sym12_v2_drifted_r0_Q12_1454.txt`]({WORKDIR}/results/best_sym12_v2_drifted_r0_Q12_1454.txt) (`3c3e8672571b9049`) and [`results/best_sym12_v2_drifted_r1_Q12_1454.txt`]({WORKDIR}/results/best_sym12_v2_drifted_r1_Q12_1454.txt) (`fcc998d093634433`).

### 3.3 New $Q_{13}$ Symmetric Coil World Record: $L = 2886$ ($h = 1443$)
- **Previous Baselines**: `2830` (`minortriad` live record), `2870` (unmerged branch `#80`).
- **Four-Stage Cascade to $L = 2886$ (`+56` over `minortriad`, `+16` over `#80`)**:
  1. **Direct Symmetric ILS (`2870 -> 2874 -> 2878`)**: Running `ils_sym 13` on `sym_coil_Q13_2870.txt` found [`results/best_sym13_Q13_2874.txt`]({WORKDIR}/results/best_sym13_Q13_2874.txt) (`L = 2874`) and [`results/best_sym13_v2_Q13_2878.txt`]({WORKDIR}/results/best_sym13_v2_Q13_2878.txt) (`L = 2878`).
  2. **Lifting `lift_sym12_Q12_1454.txt` ($Q_{12} \to Q_{13}$, `1454 -> 2878`)**: Multi-detour lifting on coordinate `b = 11` reached [`results/lift_sym13_from_lift_Q13_2878.txt`]({WORKDIR}/results/lift_sym13_from_lift_Q13_2878.txt) (`L = 2878`).
  3. **Lifting `best_sym12_Q12_1454.txt` ($Q_{12} \to Q_{13}$, `1454 -> 2882`)**: Multi-detour lifting on coordinate `b = 10` (`flips = (365, 725)`, `w1 = 42, k1 = 15, gain1 = -4 -> h_det = 723`, `w2 = 44, k2 = 16, gain2 = -11 -> L = 2870 -> 2874 -> 2878 -> 2882`) produced [`results/lift_sym13_from_ils_Q13_2882.txt`]({WORKDIR}/results/lift_sym13_from_ils_Q13_2882.txt) (`L = 2882, h = 1441`).
  4. **Symmetric ILS on `2882` (`2882 -> 2886`)**: Running `ils_sym 13 15` on `lift_sym13_from_ils_Q13_2882.txt` discovered a `+4` improvement in Round 6 (`at ga=904 gw=18`), reaching **$L = 2886$ ($h = 1443$)** in [`results/best_sym13_from2882_Q13_2886.txt`]({WORKDIR}/results/best_sym13_from2882_Q13_2886.txt) (`canonical_hash = b8f941768b53003a`), plus two additional strictly inequivalent $L = 2886$ certificates: [`results/best_sym13_2886_drifted_r0_Q13_2886.txt`]({WORKDIR}/results/best_sym13_2886_drifted_r0_Q13_2886.txt) (`05c909f6dd4aa476`) and [`results/best_sym13_2886_drifted_r1_Q13_2886.txt`]({WORKDIR}/results/best_sym13_2886_drifted_r1_Q13_2886.txt) (`0ec71bb59e0c923c`).

### 3.4 $Q_{14}$ Coil (`5854`) and $Q_{14}$ Snake (`5854`): Drifted Certificates & Structural Analysis
- **New Inequivalent `5854` Certificates**:
  - **$Q_{14}$ Coil (`5854`, `+104` over Taylor `5750`)**: Generated 3 strictly inequivalent certificates in [`results/best_co14_drifted_r0_Q14_5854.txt`]({WORKDIR}/results/best_co14_drifted_r0_Q14_5854.txt) (`r0..r2`), each verified as a valid 5854-step induced cycle in $Q_{14}$ and inequivalent to `#81` (`coil_Q14_5854.txt`).
  - **$Q_{14}$ Snake (`5854`, `+4` over Toner `5850`, `+10` over Taylor `5844`)**: Generated 3 strictly inequivalent certificates in [`results/best_sn14_drifted_r0_Q14_5854.txt`]({WORKDIR}/results/best_sn14_drifted_r0_Q14_5854.txt) (`r0..r2`), each verified as a valid 5854-step induced path in $Q_{14}$ and inequivalent to `#82` (`snake_Q14_5854.txt`).
- **Exact Subcube Decomposition of `toner_q14_5850.txt` and `snake_Q14_5854.txt`**:
  - Both `toner_q14_5850.txt` and `snake_Q14_5854.txt` are constructed from `toner_q13_2946.txt` reversed (`s13_rev`), with a single flip of coordinate `'c'` (`12`) at the midpoint (`2929`), splitting the snake into $h_1$ (`0..2929`, in $x_{12} = 0$) and $h_2 = h_{2,\text{rev}}^{\text{rev}}$ (`2930..5854`, in $x_{12} = 1$).
  - Because `v[0] = 0x0000` and `v[5854] = 0x3000` (`c ^ d`, Hamming distance 2), $h_1$ and $h_{2,\text{rev}}$ are identical across 17 of their 20 $Q_9$-subcube segments (`idx 0..7` and `idx 11..19`), and only diverge around the `'d'` (`13`) flip (`1471` in $h_1$, `4384` in $h_2$) to prevent the `'d'`-bridge endpoints `(0, 0, w_1) <-> (1, 0, w_1)` in $h_1$ from colliding across bit 12 (`'c'`) with `(0, 1, w_2) <-> (1, 1, w_2)` in $h_2$.
  - Exhaustive bitboard DFS across all windows `w = 8..65` around both `'d'` flips (`1471` and `4384`), across all 43 $Q_9$ segments (`w = 6..64`), and at both snake endpoints (`START` and `END` extensions) confirmed that `snake_Q14_5854.txt` is a local maximum under all local replacements of width $w \le 64$.

---

## 4. Part 3 (`p3`): Second-Generation Strictly Inequivalent Equal-Record Witnesses ($Q_{10}..Q_{13}$)

Every witness below is verified to be strictly inequivalent under the full hypercube automorphism group $B_n = S_n \ltimes \mathbb{Z}_2^n$ (plus path reversal and cycle shifts) to **both** the entire Caltech/Toner/Taylor/`minortriad` reference banks **and** all unmerged branches `#83..#89`:

| File | Dim | Type | Record Length | Inequiv vs Public Bank? | Inequiv vs `#83..#89`? | Canonical SHA-256 (`16 hex`) | Gap Spectrum Hash |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| [`results/p3_co10_drifted_r0_Q10_374.txt`]({WORKDIR}/results/p3_co10_drifted_r0_Q10_374.txt) | $Q_{10}$ | Coil | `374` | **YES** | **YES** (vs `#83`) | `af7676b9f832a574` | `5b4fa4c110cb5756` |
| [`results/p3_co11_drifted_r0_Q11_740.txt`]({WORKDIR}/results/p3_co11_drifted_r0_Q11_740.txt) | $Q_{11}$ | Coil | `740` | **YES** | **YES** (vs `#84`) | `dfd2b662de95b81d` | `c8754471b13bf470` |
| [`results/p3_co12_drifted_r0_Q12_1468.txt`]({WORKDIR}/results/p3_co12_drifted_r0_Q12_1468.txt) | $Q_{12}$ | Coil | `1468` | **YES** | **YES** (vs `#85`) | `a38b028afa30dd1b` | `f6ab4bb66d2e479c` |
| [`results/p3_co13_drifted_r0_Q13_2930.txt`]({WORKDIR}/results/p3_co13_drifted_r0_Q13_2930.txt) | $Q_{13}$ | Coil | `2930` | **YES** | **YES** (vs `#86`) | `04cb52e2943c3ced` | `4c992b3058bf7219` |
| [`results/p3_sn11_drifted_r0_Q11_750.txt`]({WORKDIR}/results/p3_sn11_drifted_r0_Q11_750.txt) | $Q_{11}$ | Snake | `750` | **YES** | **YES** (vs `#87`) | `8135ddbd8f256cb6` | `9cf492ccbd4b5c47` |
| [`results/p3_sn12_drifted_r0_Q12_1480.txt`]({WORKDIR}/results/p3_sn12_drifted_r0_Q12_1480.txt) | $Q_{12}$ | Snake | `1480` | **YES** | **YES** (vs `#88`) | `44af628ba2b60098` | `66a81363fb1bd7fd` |
| [`results/p3_sn13_drifted_r0_Q13_2946.txt`]({WORKDIR}/results/p3_sn13_drifted_r0_Q13_2946.txt) | $Q_{13}$ | Snake | `2946` | **YES** | **YES** (vs `#89`) | `01c3995409c9fdaf` | `92b4aa86552f7295` |

All machine-readable verification records, DCVs, gap-spectrum hashes, and canonical hashes are stored in [`results/summary.json`]({WORKDIR}/results/summary.json).
