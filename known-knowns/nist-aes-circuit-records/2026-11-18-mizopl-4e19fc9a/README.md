# NIST AES Straight-Line Circuits (`nist-aes-circuit-records`, Milestones `p3` & `p4` + `8` `[Inv]S-box` 4D Pareto Cells)

## What

CONFIRMED_PARTIAL (partial_win: p3 and p4 Route 1 + 8 zero-NOT [Inv]S-box 4D Pareto cells, recorded by our local three-skeptic review panel check, not upstream maintainer acceptance): Thirteen explicit `%NCFF-0.1-2026` straight-line circuits with zero NOT gates, zero constants, zero self-inputs, and zero dead gates — led by Milestone p3 pure-2-input-{XOR} FIPS 197 InvMixColumns circuits object/aes-invmixcols-xor92-depth10.circ.txt (sha256 4e19fc9a8d5760e80e94a6c33b1576e00d18eac15ef1f2865cd982e019138e44) and non-isomorphic companion object/aes-invmixcols-xor92-depth10-alt.circ.txt (sha256 b3bc80eef37100bd092e9b3e01df7f53ddaadb8a476944bd4f4d5bd638ce8ae0) at G = 92, GD = 10 (improving the 2026-11-17 multi-repository GD <= 10 minimum from 93@10 to 92@10 and Pareto-dominating 92@11), Milestone p4 Route 1 strict 2-input {AND, XOR, XNOR} FIPS 197 InvSBox() circuits object/aes-invsbox-a57-ad4-g152-gd10-xx95-25.circ.txt (57/4/152/10, sha256 3cea2983de3590acc3d5755055f28e8f74306d1101ab9b18a598c451aad0fed6) and object/aes-invsbox-a56-ad4-g155-gd10-xx99-26.circ.txt (56/4/155/10, sha256 c83ba275b29dddeb4b435b3a3c6a1e41fd51d93ab3023a62fe70e699de0629b6) improving the strict zero-NOT InvS-box minimum depth from GD = 11 (PR #1 143@11; master 141@12; excluding 2-NOT files 148@10 and aes-invsbox-a47-ad4-g141-gd11-xxn94-44-2.circ.txt) to GD = 10, and eight strict zero-NOT [Inv]S-box 4D Pareto cells (9 witnesses) led by object/aes-invsbox-a33-ad4-g111-gd14-xx78-39.circ.txt (33/4/111/14, sha256 aa18325ecb4675691d77c177623191086acf36ba935d78541ce14afff788633e, -12 gates below 33/4/123@14 at the same A=33; 7-AND-middle companion object/aes-invsbox-a34-ad4-g111-gd14-xx77-41.circ.txt 34/4/111/14, sha256 7dad433aafaf21e6e97ebd345ba71efefd1ec45c3943dc863a6ba7e5bf9749ab), object/aes-invsbox-a33-ad4-g109-gd15-xx76-36.circ.txt (33/4/109/15, sha256 71c604e3f0f3b4c4bfb2c0d11dcc18ba14f1cececb193febb29c1cbf1e1217ab, -4 gates at GD=15), object/aes-invsbox-a35-ad4-g129-gd13-xx94-42.circ.txt (35/4/129/13, sha256 0a0d9bcc0073d04c4a6369e44db22360a5583502cf02f364b94b3046621107a1, -2 gates at GD=13), and object/aes-sbox-a37-ad4-g119-gd14-xx82-33.circ.txt (37/4/119/14, sha256 3380e6da4f6a7dc3886d6cdecd51b996d0552b28911e8d718e91a32875d61df3, -2 gates on forward S-box at GD=14), accompanied by object/00_nist_aes_gd10_and_barriers_certificate.json (sha256 717e3701dc2a42b9966c099120b68c41b1633773141617d0cf8f97674554305d) — without claiming any of the 6 CSRC wish-list targets (111@14 is +1 gate above <=110@14), p1, p2, or p4 Route 2.

- **Central File (Standalone Verifier):** [`verify-it-yourself/verify.py`](./verify-it-yourself/verify.py) (`sha256: 8cd6e40c4333ee55034766b67030374b33d0a3fd6d69a1be7f00c1eb3eea62c8`)
- **Unified Barrier & Baseline Certificate:** [`object/00_nist_aes_gd10_and_barriers_certificate.json`](./object/00_nist_aes_gd10_and_barriers_certificate.json) (`sha256: 717e3701dc2a42b9966c099120b68c41b1633773141617d0cf8f97674554305d`)

## Check it yourself

From this package directory, run:

```sh
sh verify-it-yourself/run_checks.sh
sh verify-it-yourself/run_checks.sh --corrupt   # negative control: exits 1 with final line FAIL
```

- **Dependencies:** Python 3.9+ standard library only (`0` third-party packages, `100%` offline).
- **Runtime:** `< 0.3` seconds on a laptop CPU.
- **Expected final line:** `PASS` (and `sh verify-it-yourself/run_checks.sh --corrupt` exits `1` with final line `FAIL`).

## Compared to

Exact raw upstream URLs, UTC fetch timestamps, HTTP statuses, and `sha256` digests are recorded in [`the-record-we-beat/README.md`](./the-record-we-beat/README.md).

### 1. Summary of All `13` Verified `%NCFF-0.1-2026` Constructions (Waves 1–7)

Every circuit below uses strictly 2-input `{XOR}` (for `InvMixColumns`) or 2-input `{AND, XOR, XNOR}` (for `[Inv]S-box`) with `#NOT = 0`, zero constants (`0`/`1`), zero self-input gates (`u == v`), and zero dead gates, verified exhaustively by `verify.py` against the `2026-11-17` `8`-repository baseline (`457` individual files + `18,938` forward and `14,324` inverse `kste` `88`-XOR circuits).

| Circuit File (`sha256` prefix) | Function | `(A, AD, G, GD)` | `#XOR / #XNOR / #NOT` | Comparison vs. `2026-11-17` Multi-Repo Baseline |
| :--- | :---: | :---: | :---: | :--- |
| `aes-invmixcols-xor92-depth10.circ.txt` (`4e19fc9a8d57...`) | `invmixcols` | **`(0, 0, 92, 10)`** | `92 / 0 / 0` | -1 XOR at GD <= 10 (93 -> 92) and -1 depth level at G = 92 (11 -> 10), rendering 92@11 Pareto-dominated |
| `aes-invmixcols-xor92-depth10-alt.circ.txt` (`b3bc80eef371...`) | `invmixcols` | **`(0, 0, 92, 10)`** | `92 / 0 / 0` | Independent 92@10 {XOR} DAG (symmetric difference 40 vs primary 92@10) |
| `aes-invsbox-a57-ad4-g152-gd10-xx95-25.circ.txt` (`3cea2983de35...`) | `invsbox` | **`(57, 4, 152, 10)`** | `70 / 25 / 0` | -1 gate-depth level on strict zero-NOT InvS-box (GD = 11 -> GD = 10 at G = 152, A = 57) |
| `aes-invsbox-a56-ad4-g155-gd10-xx99-26.circ.txt` (`c83ba275b29d...`) | `invsbox` | **`(56, 4, 155, 10)`** | `73 / 26 / 0` | 4D Pareto companion at GD = 10 with A = 56 (-1 AND vs 152@10) |
| `aes-invsbox-a33-ad4-g111-gd14-xx78-39.circ.txt` (`aa18325ecb46...`) | `invsbox` | **`(33, 4, 111, 14)`** | `39 / 39 / 0` | -12 gates below 33/4/123/14 at the same A = 33 (-10 vs 1-NOT 121@14, -1 AND vs 34/4/111/14; +1 gate above CSRC Wish-List (c) <=110@14) |
| `aes-invsbox-a34-ad4-g111-gd14-xx77-41.circ.txt` (`7dad433aafaf...`) | `invsbox` | **`(34, 4, 111, 14)`** | `36 / 41 / 0` | 7-AND-middle companion at 111@14 (A = 34; dominated on A by 33/4/111/14, retained for T5a..T8 sub-block verification) |
| `aes-invsbox-a33-ad4-g109-gd15-xx76-36.circ.txt` (`71c604e3f0f3...`) | `invsbox` | **`(33, 4, 109, 15)`** | `40 / 36 / 0` | -4 gates at GD <= 15 (113 -> 109; -9 vs NIST 118@15), -2 depth levels at G = 109 (vs 109@17), and dominates 110@16 |
| `aes-invsbox-a35-ad4-g129-gd13-xx94-42.circ.txt` (`0a0d9bcc0073...`) | `invsbox` | **`(35, 4, 129, 13)`** | `52 / 42 / 0` | -2 gates at GD <= 13 (131 -> 129; -1 vs 1-NOT 130@13) |
| `aes-sbox-a37-ad4-g119-gd14-xx82-33.circ.txt` (`3380e6da4f6a...`) | `sbox` | **`(37, 4, 119, 14)`** | `49 / 33 / 0` | -2 gates on forward S-box at GD <= 14 (121 -> 119 vs Joe-b-20 37/4/121/14 & 2026-11-18 NIST 21f076fa 33/4/121/14; -6 vs 3d807741 125@14) |
| `aes-invsbox-a32-ad5-g116-gd16-xx84-46.circ.txt` (`92b64b24cef6...`) | `invsbox` | **`(32, 5, 116, 16)`** | `38 / 46 / 0` | -6 gates at A <= 32, GD <= 16 (122 -> 116 vs Joe-b-20; -12 vs NIST 32/5/128/16 and -9 vs 32/5/125/15) |
| `aes-invsbox-a32-ad5-g114-gd19-xx82-17.circ.txt` (`7cb05a3d5132...`) | `invsbox` | **`(32, 5, 114, 19)`** | `65 / 17 / 0` | -4 gates at A <= 32, GD <= 19 (118 -> 114) |
| `aes-invsbox-a28-ad4-g143-gd16-xx115-59.circ.txt` (`44eb1bf275f5...`) | `invsbox` | **`(28, 4, 143, 16)`** | `56 / 59 / 0` | -7 gates at A = 28, AD = 4, GD <= 16 (150 -> 143; eliminates 1 NOT gate vs Joe-b-20 xxn115-59-1) |
| `aes-invsbox-a28-ad4-g134-gd19-xx106-46.circ.txt` (`e9faba1333a2...`) | `invsbox` | **`(28, 4, 134, 19)`** | `60 / 46 / 0` | -1 gate at A = 28, AD = 4, GD <= 19 (-6 vs NIST 140@19; eliminates 1 NOT gate vs Joe-b-20 xxn106-46-1) |

### 2. Multi-Repository AES Reference Frontier & Gate-Model Context (`2026-11-17`)

| Function & Regime | Metric `(A, AD, G, GD)` | `#XOR / #XNOR / #NOT` | Source (`2026-11-17` Snapshot) | Strict Zero-`NOT` Status |
| :--- | :---: | :---: | :--- | :--- |
| **`InvMixColumns` (`GD = 10`, Milestone `p3`)** | **`(0, 0, 92, 10)`** | **`92 / 0 / 0`** | **This package (`2` witnesses, `symdiff = 40`)** | **Valid (`-1` XOR vs `93@10`, dominates `92@11`)** |
| `InvMixColumns` (`GD = 10` prior min) | `(0, 0, 93, 10)` | `93 / 0 / 0` | `usnistgov/Circuits` & `Joe-b-20` | Valid (superseded by `92@10`) |
| `InvMixColumns` (`GD = 11` prior min) | `(0, 0, 92, 11)` | `92 / 0 / 0` | `usnistgov/Circuits` & `Joe-b-20` | Valid (Pareto-dominated by `92@10`) |
| `InvMixColumns` (`GD = 5 / 6 / 16` bars) | `(0, 0, 118, 5)` | `118 / 0 / 0` | `Joe-b-20` (`NIST` `119@5`, `104@6`; `kste` `88@16`) | Valid (Wish-List `(f)` `<= 105@5` open) |
| `MixColumns` (`GD = 5 / 4 / 3` bars) | `(0, 0, 88, 5)` | `88 / 0 / 0` | `NIST` / `Joe-b-20` / `kste` (`89@4`, `97@3`) | Valid (Wish-List `(d,e)` open) |
| **`InvS-box` (`GD = 10`, Milestone `p4` Route 1)** | **`(57, 4, 152, 10)`** | **`70 / 25 / 0`** | **This package (`companion: 56/4/155/10`)** | **Valid (`GD = 10` zero-`NOT`)** |
| `InvS-box` (`GD = 11` prior zero-`NOT` min) | `(55, 4, 143, 11)` | `65 / 23 / 0` | `usnistgov/Circuits` `PR #1` (`ZKNoxHQ`) | Valid (`GD = 11`) |
| `InvS-box` (`GD = 10` / `GD = 11` with `2` `NOT`s) | `(55, 4, 148, 10)` | `65 / 26 / 2` | `NIST` `xxn93-26-2` (`Joe-b-20` `47/4/141/11` `xxn94-44-2`: `48/44/2`) | Excluded (`2` unary `NOT` gates) |
| **`InvS-box` (`GD = 14`, min `G` & `A = 33` apex)** | **`(33, 4, 111, 14)`** | **`39 / 39 / 0`** | **This package (`5` archived across `2` classes; `A = 34` ref: `34/4/111/14`)** | **Valid (`-12g` vs `33/4/123@14`, `-10g` vs `121@14`; `+1g` from `<=110@14`)** |
| `InvS-box` (`GD = 14` prior zero-`NOT` / `1`-`NOT`) | `(33, 4, 123, 14)` | `74 / 16 / 0` | `usnistgov/Circuits` (`Joe-b-20` `121@14` has `1` `NOT`) | Valid (superseded by `33/4/111/14`) |
| **`InvS-box` (`GD = 15` / `GD = 13` Pareto)** | **`(33, 4, 109, 15)`** | **`40 / 36 / 0`** | **This package (`GD = 13`: `35/4/129/13`)** | **Valid (`-4g` vs `113@15`, `-2g` vs `131@13`)** |
| **`S-box` (`GD = 14` Pareto)** | **`(37, 4, 119, 14)`** | **`49 / 33 / 0`** | **This package (`aes-sbox-a37-ad4-g119-gd14-xx82-33.circ.txt`)** | **Valid (`-2g` vs `Joe-b-20` `37/4/121@14` & `NIST` `21f076fa` `33/4/121@14`; `-6g` vs `3d807741` `125@14`)** |
| `[Inv]S-box` (`p1`, `p2`, `p4` Route 2 bars) | `(32, 7, 105, 27)` | `59 / 14 / 0` | `NIST` `105@27` (`S-box` `103@29`; `A=28`: `126@27` / `124@27`; `AD=3`: `A=35`) | Valid (unbeaten) |

### 3. Algebraic Mechanisms Behind Milestone `p3` (`92@10`), Milestone `p4` (`GD = 10`), and `33/4/111/14`

1. **Milestone `p3` — Two Non-Isomorphic `92`-XOR `GD = 10` `InvMixColumns` Circuits (`how-we-built-it/xorflux_cpp.cpp`):**
   - Applying incremental `uint64_t` value-set plateau walks and connected-cone `2->1`, `2->2`, `3->2` Meet-in-the-Middle synthesis across all `14,376` seed circuits (`42` `NIST` + `10` `Joe-b-20` + `14,324` `kste` `88`-XOR circuits) produced two distinct `92`-XOR `GD = 10` DAGs (`aes-invmixcols-xor92-depth10.circ.txt` on local M1 `XORFlux v8` and `aes-invmixcols-xor92-depth10-alt.circ.txt` on 12-vCPU C++17 `xorflux_cpp`). Their `92`-vector linear value sets share `72` vectors (`symmetric_difference = 40`), and `HiGHS` Top-2-Layer MILP confirms both `GD <= 8` prefixes (`75` and `74` gates) are globally minimal (`opt = 92`) at `GD <= 10`.
2. **Milestone `p4` Route 1 — Zero-`NOT` `GD = 10` Tower-Norm Asymmetry (`how-we-built-it/synthesize_invsbox_gd10.cpp`, `how-we-built-it/gd10_super_synth.cpp`):**
   - Over $\mathbb{F}_{2^8} = \mathbb{F}_2[x]/(x^8 + x^4 + x^3 + x + 1)$ (`GF(2^4)` coordinate basis `["0x01", "0xbc", "0xe1", "0xb1"]`), Depth-`1` zero-`NOT` affine gates on distinct inputs have linear weight `2`, forbidding $(1 \oplus x_i) \wedge (\dots)$ at Depth `2`. Exhaustive enumeration over all `3,604,462` degree-$\le 2$ `D <= 3` signals (`[8, 92, 4358]` at `D <= 0, 1, 2`) and `16,208,265` unrestricted `D <= 3` zero-`NOT` Boolean functions shows unshifted forward `S-box` ($z = x$) reaches only **`2 / 15`** nonzero $z^{17}$ norm masks (`{10, 13}`, `rank 2 < 4`), whereas `InvS-box` ($z = A_{\mathrm{AES}}^{-1}(x \oplus \text{0x63})$) absorbs complement parities into Depth-`1` `XNOR` gates across **`8 / 15`** masks (`{1, 4, 7, 9, 10, 12, 13, 15}`, `rank 4 / 4`), including two Frobenius normal-basis orbits `[7, 12, 4, 9]` and `[15, 9, 7, 10]` yielding `152@10` (`A = 57`) and `155@10` (`A = 56`).
3. **Cross-Stage Nonlinear Seam Compression & Uncapped-`A` Saddle Traversal (`33/4/123/14 -> 33/4/111/14`, `109@15`, `129@13`, `119@14`):**
   - Coupling parent-seeded 3-level `GF(2^4)` normal-basis inverter joins, partial distributive `GD = 11` `AND` splitting (`A = 33 -> 34` intermediate saddle with uncapped-`A` `cost,gd` acceptance), observable don't-care (`ODC`) `AND`-window replacement, and deadline-aware linear resynthesis compressed zero-`NOT` `InvS-box` at `GD <= 14` by `-12` gates at the same `A = 33, AD = 4` (`33/4/123/14 -> 33/4/111/14`, `59` constructed witnesses across `2` canonical `Zone_Bot` classes, dominating both `34/4/111/14` and `33/4/112/14`) and at `GD <= 15` by `-4` gates (`113@15 -> 109@15`).

### 4. Exact Sub-Block Optimality & Coupled Obstruction Certificates (`T1..T11`)

| Theorem | Circuit & Sub-Block | Exact Method (`verify.py` / `kissat 4.0.4` / `HiGHS`) | Certified Bound / Status |
| :--- | :--- | :--- | :--- |
| **`T1`** | `invsbox-105` `Zone_Top` (`8 -> 17`) | Exact $\mathbb{F}_2^8$ `0`-helper closure + `kissat` (`340v`, `rc=20`, `0.013s`); `K=18` `SAT` (`1/230` unique `mask=66`) | **Global depth-free minimum `= 18` gates** |
| **`T2`** | `invsbox-126` `Zone_Top` (`8 -> 16`) | Exact $\mathbb{F}_2^8$ `0/1`-helper closure (`231` masks) + `kissat` (`1,173v`, `rc=20`, `0.064s`); `K=18` `SAT` | **Global depth-free minimum `= 18` gates** |
| **`T3`** | `sbox-124` `Zone_Top` (`8 -> 17`) | Exact $\mathbb{F}_2^8$ `0/1`-helper closure (`230` masks) + `kissat` (`1,299v`, `rc=20`, `0.073s`); `sbox-103` ctrl `SAT` | **Global depth-free minimum `= 19` gates** |
| **`T4`** | `152@10` `GD <= 7` feeder (`t45..t71`) | Bilinear rank `37/37` (`nullity = 0`) + `32 - 5 = 27` Pigeonhole + `HiGHS` `status=0` (`0.018s`) | **Global depth-free minimum `= 27` gates (`0` helpers)** |
| **`T5a`** | `34/4/111/14` `GD = 5..10` middle (`P = 16` states) | `|S5|=6, |S6|=45, |S7|=643, |S8|=33,602` (`0/9` targets in `S7` -> `|G_{>=8}|>=9`) + `kissat` `rc=20` across all `4` `K=19` cases, `16` polarities, and `|Stab|=72` `GL(4,2)` Karatsuba orbits (`K=20` ctrl `SAT`) | **Global zero-`NOT` minimum `= 20` gates (`K <= 19` `UNSAT`)** |
| **`T5b`** | `34/4/111/14` widened `GD = 4..10` middle (`P = 61`) | `|S4|=6, |U5|=51, |U6|=1,562, |U7|=982,724` (`0/9` targets in `U7`) + `kissat` hitting-DAG `K=25` `rc=20` (`7.18s`; `K=26` ctrl `SAT`) | **Global zero-`NOT` minimum `= 26` gates (`K <= 25` `UNSAT`)** |
| **`T5c`** | `34/4/111/14` coupled `t58 @ GD <= 9` slack test | `kissat` exact hitting-DAG pulling `t58` from `GD=10` to `GD<=9` at `K=20` (`GD=5`, `0.057s`) & `K=26` (`GD=4`, `9.96s`) | **Exact `UNSAT` (`rc = 20`; `a29, a31` cannot drop to `GD=10` for free)** |
| **`T6`** | `34/4/111/14` & `109@15` `2,040` `GF(2^8)` conjugates | Exhaustive `2,040`-automorphism $(\lambda, k)$ `0/1`-helper `Zone_Top` & `(1 ^ x6)` screen (`verify.py` `< 0.05s`) | **`0 / 2,040` conjugates achieve `Top <= 17` or `Top+(1^x6) <= 18`** |
| **`T7`** | `34/4/111/14` `Zone_Bot` (`GD = 10..14`, `29` gates) | 19-bit FWHT floors `[12,13,13,14,13,14,14,12]`; unpruned `Top-2` (`kissat rc=20`, `HiGHS OPTIMAL=29.0`) & `w2_aug35_cut28` (`3,423v`, `HiGHS status=2 INFEASIBLE`, `0.165s`) | **`Top-2` & `w2_aug35` optimal `= 29g` (unconstrained 5-layer `K=28` CDCL / `73,410v` Top-3 MILP: `TIMEOUT_UNKNOWN` / `ITERATION_LIMIT`)** |
| **`T8-GL4`** | `72` `GL(4,2)` Karatsuba stabilizers (`9` orbits) | Exact `kissat` early-bottleneck (`t58 @ GD <= 9`) sweep across all `9` `GL(4,2)` stabilizer orbits at `K = 21` (`+1g`) & `K = 22` (`+2g`), plus `GD = 4` (`P = 61`) at `K = 27` (`21.47s`) | **`0 / 72` stabilizers `SAT` at `K <= 22` (`min K = 24` ctrl `SAT`); `GD = 4` `K = 27` `UNSAT`** |
| **`T9`** | `A=33` `112@14` `Top-2`, `c109` splices & Ghost `@GD=9` | `HiGHS` `Top-2` (`29.0` on `3/3`) & `aug K<=27 INFEASIBLE`; `6/6` Kraft-valid `c109_nx6` `G=110` splices `INFEASIBLE`; Backward Ghost-Wire `@GD=9` (`n_10=0`); `1.30M` `GF(2)` tensor flips (`29,763` `AD=4`) | **`Top-2 = 112`; `6/6` `c109` `G=110` splices `INFEASIBLE`; `C`-weight `52 -> >=61` on non-Karatsuba flips** |
| **`T10`** | `33/4/111/14` `Zone_Top = 19` & `2/2` `Zone_Bot` classes | `19` distinct $\mathbb{F}_2^8 / \langle 1 \rangle$ targets (`0` Steiner helpers -> global depth-free `Zone_Top >= 19`); `64` witnesses collapse to `2` canonical `Zone_Bot` classes (`[10^{10}, 11^6, 12^2]`), both `HiGHS Top-2 = 111` & `GD<=12` 2-sum `aug K<=28 INFEASIBLE` | **Global `Zone_Top = 19`; `2 / 2` canonical `33/4/111/14` `Zone_Bot` classes `Top-2` & `aug` optimal (`= 111`)** |
| **`T11`** | Official `%NCFF` unary `NOT` `@ GD=14` & `MixCols D=3` LP | `GD=10` `Separator` (`NIST 148@10` `-4g` vs `152@10`) vs `GD=14`: `2/2` zero-net-cost `nx6 = XNOR(x6,0)` rewrites induce `a20 -> a20 ^ a26`, pushing `y5` `FWHT_min_depth = 15 > 14` (Kraft infeasible); `29,180v` `MixCols D=3` `HiGHS` root LP | **`0` feasible zero-net-cost unary-`NOT` rewrites at `GD <= 14`; `MixColumns D=3` exact Root LP `= 92.00` (`rot16 = 115@3`)** |

### 5. Five Quantitative `[Inv]MixColumns` Structural Barriers (`B1..B5`, Certificate `sha256: 717e3701dc2a...`)

| Barrier ID | Hypothesis / Decomposition Tested | Certified Outcome |
| :--- | :--- | :--- |
| **`B1`** | $\mathbb{Z}_4$ byte-rotational quotient (`rot8(U) == U`) | Floors at **`143@5`** (`+25g` vs. asymmetric `118@5`) on `InvMixColumns` and **`106@3`** (`+9g` vs. `97@3`) on `MixColumns` (`rot8` `4x`-duplicates directed cancellation chains) |
| **`B2`** | Coupled Even/Odd $M \oplus M^{-1} = (1+X^2)(\text{0x0C}+\text{0x08}X)$ | $\Delta(E_0, E_1)$ (`GF(2)` rank `16`) arrives at `GD = 4`, but pays a mandatory **`+32`-gate double-output penalty (`156@5`)** since all `32` `MixColumns` outputs have internal fanout `0` |
| **`B3`** | Top-2-Layer & Augmented Multi-Layer Cutoff MILP (`how-we-built-it/exact_toplayer_milp.py`) | All `10` frontier Top-2-Layer instances proved **`OPTIMAL` (`status = 0`)**; `118@5 -> <=117@5` (`6,582v`), `90@12 -> <=89@12` (`27,718v`), and `89@15 -> <=89@14` (`25,485v`) proved **`INFEASIBLE` (`status = 2`)** |
| **`B4`** | `kste` `88`-XOR `InvMixColumns` corpus (`14,324` circuits) | Minimum depth is **`GD = 16`** (`105` circuits); every `GD = 16` circuit has $\ge 4$ mandatory output targets at depth $\ge 15$ in two rotational daisy chains (`+2g -> 90@14` to shortcut) |
| **`B5`** | `GD = 3` `MixColumns` exact-pair-cover ILS (`186.75M` steps) | Held at `97@3` across `186.75M` ILS steps and `51.12M` Wave 4 `InvMixColumns` proposals outside `GD = 10` (`118@5`, `104@6`, `99@7`, `96@8`, `94@9`, `90@12`, `89@15`, `88@16` held) |

## Not claimed

1. **Partial Milestone Wins Only (`0 / 6` CSRC Wish-List Targets Claimed):** None of the `6` live `2026-11-17` NIST CSRC wish-list targets (`A <= 27`, `G <= 100`, `G <= 110` at `GD <= 14`, `MixColumns <= 86`, `MixColumns <= 93` at `GD = 3`, `InvMixColumns <= 105` at `GD <= 5`), nor `p1` (`InvS-box <= 104`), `p2` (`A = 28` `<= 123 / <= 125`), nor `p4` Route 2 (`AD = 3, A <= 34`) are claimed (`111@14` is `+1` gate above `(c)` `<= 110@14`).
2. **`NOT`-Gate Exclusion Note (`148@10` & `141@11` vs. `152@10`):** Milestone `p3` (`InvMixColumns` `92@10`) uses pure `{XOR}` gates with zero `NOT` ambiguity, and `33/4/111/14` and `35/4/129/13` use strictly fewer total gates than both zero-`NOT` and `1`-`NOT` baselines (`T11` proves zero-net-cost unary `NOT` rewrites on `33/4/111/14` push `FWHT` depth to `15 > 14`). At `GD = 10`, `usnistgov/Circuits` `master` contains `aes-invsbox-a55-ad4-g148-gd10-xxn93-26-2.circ.txt` (`2` unary `NOT` gates) and `Joe-b-20` contains `aes-invsbox-a47-ad4-g141-gd11-xxn94-44-2.circ.txt` (`2` unary `NOT` gates); if unary `NOT` gates are permitted, `148@10` uses `4` fewer total gates than `152@10`.
3. **Construction Upper Bounds & `TIMEOUT_UNKNOWN` / `ITERATION_LIMIT`:** Circuit counts are upper bounds, not global circuit-size lower bounds. Full-`Zone_Bot` `18..21`-helper CDCL runs and unconstrained 5-layer `111@14` `Zone_Bot` `K = 28` slot-CNF / `73,410`-var Top-3 MILP runs hit `TIMEOUT_UNKNOWN` / `ITERATION_LIMIT` and do not prove unconstrained multi-layer `Zone_Bot` optimality. `CONFIRMED_PARTIAL` in `panel/gate.md` records our own local three-skeptic review panel check (not upstream maintainer acceptance).

## Credits

- **NIST Circuit Complexity Project:** Luis Brandao and Rene Peralta (`https://github.com/usnistgov/Circuits`, commits `3d807741` and `21f076fa`, and `https://csrc.nist.gov/Projects/circuit-complexity/list-of-circuits`).
- **Compared Repositories & Prior Constructions:** Renaud Dubois / ZKNoxHQ (`https://github.com/usnistgov/Circuits/pull/1`), `Joe-b-20/xor-circuit-research` (`https://github.com/Joe-b-20/xor-circuit-research`), Milad Nasr (NIST `A = 28` & `A = 35 / AD = 3` circuits), Joan Boyar and Rene Peralta (`https://www.cs.yale.edu/homes/peralta/CircuitStuff/CMT.html`), `Swapnil-jain/gf2m-circuits`, Stefan Kolbl (`https://github.com/kste/mixcolumns_xor`), Jeremy Jean (`https://eprint.iacr.org/2026/1481`), `chengxuandi/aes-sbox-circuit-optimizations`, `umizame/S-box_29-AND`, and `NicolasMasselot/ai-guided-aes29-affine-resynthesis`.
- **Synthesis & Verification:** **we\*** (`PROOFER` powered by Gemini + `@mizopl`).
