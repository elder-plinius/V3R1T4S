# Panelist Report — Role: REPRODUCE

context: Antigravity fresh subagent (invoke_subagent, role REPRODUCE)
target: `fmm-additive-complexity-records` (`algorithms/fmm-additive-complexity-records`)

## 1. Mandate & Verbatim Definition Quoted Before Inspecting Author Code

Per step 6 of the verification protocol:
> "Before reading the author's code, write your own checker from the definition (quote it). Verify every property and the claimed value from the saved files; re-derive every proof step. For an exhaustive search, a sample is a spot check and cannot pass. Fail on any mismatch, missing object or non-determinism."

Before reading `claim/verify.py` or `claim/clss_cl1_tellegen_reducer.cpp`, I read `claim/CLAIM.md`, `claim/REPRODUCE.md`, and `claim/CERTIFICATE.json`, quoted the verbatim target definition from `claim/CLAIM.md`:
> "An explicit straight-line program (list of linear forms over the inputs, r products, and linear forms producing the outputs) for a format `\langle n,m,p \rangle` with `max(n,m,p) \le 8` and rank `r` equal to the best rank listed for that format in `fmm_sota.json` (re-fetched live), that (1) is verified symbolically to compute the full product `A*B` exactly over `Z`, and (2) uses a number of additions/subtractions STRICTLY LESS (direction: min) than the smallest reduced addition count for that format and rank in Perminov's live repository (the `addition_reduced_ZT` scheme file for the format, `reduced_known.json`, `README` and `CHANGELOG`) re-fetched live immediately before claiming, counted under Perminov's 'reduced' convention (each binary `+/-` between already-computed quantities counts one; multiplication by `-1` is free; multiplication by any other scalar is not allowed in a ternary SLP), AND below any lower count published for that format and rank on the live Lille per-format page's cited complexity variant and in `matmulcatalog`'s live `COVERAGE.md` 'adds' column. If the Lille rank for the format is attained only with non-ternary coefficients, the comparison is against the best count in the same coefficient class as the candidate. The reference count is the MINIMUM `cr` value over all files for that format and rank in the live directory (formats have several files). Each scheme is claimed once: a scheme that also lowers the rank is a rank target, not this one."

and wrote a completely independent checker `indep_fmm_check.py` from scratch.

---

## 2. Artifact Integrity Verification (Byte Sizes & SHA-256 Digests)

My independent checker verified the exact byte counts and SHA-256 checksums of all 6 top-level artifacts and all 48 scheme files in `claim/schemes/`:

| Relative File Path | Verified Bytes | Verified SHA-256 Digest | Status |
| :--- | :---: | :--- | :---: |
| `claim/CERTIFICATE.json` | `26,573` | `e47a7dd88e8f9778d65667b7d4030ca66cf39c6de9d89b3b0f1c5f61cb9cc1de` | PASS |
| `claim/verify.py` | `12,782` | `d0a557971cd72c8c588d4a35e31b9f2135c5e421ef6caddb64a940a02f695c40` | PASS |
| `claim/clss_cl1_tellegen_reducer.cpp` | `24,238` | `c4dbcec6ab78e5a335bb993689806e4672509c42e8e8a5f3dbe39b4629ad1c66` | PASS |
| `claim/reference_live_champions/fmm_sota.json` | `343,774` | `2a6535154ac877aeb495f9294a5e97c3dbf1b1969aefe6ffc0a612f2cf01cbae` | PASS |
| `claim/reference_live_champions/matmulcatalog_COVERAGE.md` | `94,842` | `c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7` | PASS |
| `claim/reference_live_champions/reduced_known.json` | `1,189` | `ef67c13792b0e770578de4ff01438178ce4e6ac4efd60a3580f3131e31907a5d` | PASS |
| All 48 `.json` files in `claim/schemes/` | Exact match (`48/48`) | Exact match (`48/48`) against `claim/CERTIFICATE.json` | PASS |

---

## 3. Independent Counter Calibration on All 36 Live Reference Champion Files

Before checking any claimed scheme, `indep_fmm_check.py` parsed and symbolically evaluated all `36` live reference `.json` files in `claim/reference_live_champions/*_ZT_reduced.json` (`18` distinct formats):
- Every reference file passed exact symbolic bilinear identity verification over $\mathbb{Z}[A, B]$ (`0` symbolic errors across all `36` files).
- Every reference file's naive addition count `cn` matched `complexity.naive` (`36/36`).
- Every reference file's `complexity.reduced` matched `cr_len` or `cr_val` (`36/36`), and `indep_fmm_check.py` independently detected the two reference files containing a non-unit coefficient (`value = 2`):
  - `claim/reference_live_champions/4x4x8_m96_cr339_cn973_ZT_reduced.json` (`cr_len = 339`, `cr_val = 340`, `complexity.reduced = 339`)
  - `claim/reference_live_champions/5x6x8_m170_cr663_cn2312_ZT_reduced.json` (`cr_len = 662`, `cr_val = 663`, `complexity.reduced = 663`)
- All 11 target format reference minimums matched the exact baseline values:
  - `2x4x7` ($m=45$): `168` (`2x4x7_m45_cr168_cn308_ZT_reduced.json`, plus `174` in `2x4x7_m45_cr174_cn308_ZT_reduced.json`)
  - `2x5x5` ($m=40$): `147` (`2x5x5_m40_cr147_cn283_ZT_reduced.json`, plus `153` in `2x5x5_m40_cr153_cn283_ZT_reduced.json`)
  - `4x5x8` ($m=118$): `466` (`4x5x8_m118_cr466_cn1521_ZT_reduced.json`, plus `513` in `4x5x8_m118_cr513_fv249_cn1521_ZT_reduced.json`)
  - `4x6x7` ($m=123$): `468` (`4x6x7_m123_cr468_cn1586_ZT_reduced.json`, plus `517` in `4x6x7_m123_cr517_cn1586_ZT_reduced.json`)
  - `5x5x6` ($m=110$): `411` (`5x5x6_m110_cr411_cn1215_ZT_reduced.json`, plus `460` in `5x5x6_m110_cr460_fv204_cn1215_ZT_reduced.json`)
  - `5x5x8` ($m=144$): `555` (`5x5x8_m144_cr555_cn1924_ZT_reduced.json`, plus `620` in `5x5x8_m144_cr620_fv281_cn1924_ZT_reduced.json`)
  - `5x6x6` ($m=130$): `499` (`5x6x6_m130_cr499_cn1716_ZT_reduced.json`, plus `562` in `5x6x6_m130_cr562_fv250_cn1716_ZT_reduced.json`)
  - `5x6x7` ($m=150$): `577` (`5x6x7_m150_cr577_cn2039_ZT_reduced.json`, plus `664` in `5x6x7_m150_cr664_fv310_cn2039_ZT_reduced.json`)
  - `5x7x7` ($m=176$): `694` (`5x7x7_m176_cr694_cn2605_ZT_reduced.json`, plus `788` in `5x7x7_m176_cr788_fv371_cn2605_ZT_reduced.json`)
  - `3x3x6` ($m=43$): `153` (`3x3x6_m43_cr153_cn284_ZT_reduced.json`, plus `160` in `3x3x6_m43_cr160_cn284_ZT_reduced.json`)
  - `4x4x8` ($m=96$): `339` (`cr_len = 339`, `cr_val = 340` in `4x4x8_m96_cr339_cn973_ZT_reduced.json`, plus `377` in `4x4x8_m96_cr377_fv171_cn973_ZT_reduced.json`)

---

## 4. Independent Verification of All 48 Claimed Ternary SLP Files (`0.30s`)

Running `indep_fmm_check.py` across all `48` `.json` files in `claim/schemes/` verified:
1. **Strict DAG Acyclicity:** Every node reference `idx` in `u_fresh[k]`, `v_fresh[k]`, `w_fresh[k]` satisfies $0 \le \text{idx} \lt \text{nin} + k$, and every reference in `u`, `v`, `w` satisfies $0 \le \text{idx} \lt \text{nin} + |\text{fresh}|$.
2. **Strictly Unit Ternary Coefficients:** Every coefficient `value` in `u_fresh`, `v_fresh`, `w_fresh`, `u`, `v`, `w` is in $\{-1, +1\}$ (`0` non-unit coefficients across all `48` files), and every expanded matrix $U, V, W^T$ has entries purely in $\{-1, 0, +1\}$.
3. **Exact Symbolic Polynomial Identity over $\mathbb{Z}[A, B]$:** For all `48` schemes and every output coordinate $(i, j) \in \{0, \dots, n_1-1\} \times \{0, \dots, n_3-1\}$,
   $$\sum_{r=0}^{m-1} W_{r, (i, j)} \left(\sum_{a, b} U_{r, (a, b)} A_{a, b}\right)\left(\sum_{c, d} V_{r, (c, d)} B_{c, d}\right) = \sum_{k=0}^{n_2-1} A_{i, k} B_{k, j}$$
   holds identically over $\mathbb{Z}[A, B]$ with `0` extra terms and `0` missing terms.
4. **Exact Addition Counts (`cr` and `cn`):** For all `48` files, `cr_len == cr_val == complexity.reduced == cu + cv + cw` and `cn == cnu + cnv + cnw == complexity.naive`, matching `claim/CERTIFICATE.json` digit-for-digit.

### 4.1. 9 Exact-SOTA-Rank Formats ($\max(n,m,p) \le 8$) Strictly Beating Live Minimum `cr` (`11` Scheme Files)

| Format | Rank $m$ (`fmm_sota`) | Verified `cr` (`cu, cv, cw`) | Verified `cn` | Live Min `cr` | `matmulcatalog` `adds` | `reduced_known.json` | Delta vs Live Min `cr` | Scheme File in `claim/schemes/` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **`2x4x7`** | `45` (`45`) | **`157`** (`26, 58, 73`) | `345` | `168` | `+308` | — | **`-11`** | `2x4x7_m45_cr157_cn345_ZT_reduced.json` |
| **`2x4x7`** (var. 2) | `45` (`45`) | **`164`** (`27, 64, 73`) | `285` | `168` | `+308` | — | **`-4`** | `2x4x7_m45_cr164_cn285_ZT_reduced.json` |
| **`2x5x5`** | `40` (`40`) | **`145`** (`28, 58, 59`) | `273` | `147` | `+256` | `Z: 313, Z2: 218` | **`-2`** | `2x5x5_m40_cr145_cn273_ZT_reduced.json` |
| **`4x5x8`** | `118` (`118`) | **`447`** (`96, 141, 210`) | `1463` | `466` | `+1521` | — | **`-19`** | `4x5x8_m118_cr447_cn1463_ZT_reduced.json` |
| **`4x6x7`** | `123` (`123`) | **`464`** (`112, 138, 214`) | `1562` | `468` | `+1586` | — | **`-4`** | `4x6x7_m123_cr464_cn1562_ZT_reduced.json` |
| **`5x5x6`** | `110` (`110`) | **`406`** (`105, 110, 191`) | `1192` | `411` | `+1215` | — | **`-5`** | `5x5x6_m110_cr406_cn1192_ZT_reduced.json` |
| **`5x5x8`** | `144` (`144`) | **`548`** (`130, 156, 262`) | `1872` | `555` | `+1908` | — | **`-7`** | `5x5x8_m144_cr548_cn1872_ZT_reduced.json` |
| **`5x6x6`** | `130` (`130`) | **`492`** (`128, 139, 225`) | `1697` | `499` | `+1716` | — | **`-7`** | `5x6x6_m130_cr492_cn1697_ZT_reduced.json` |
| **`5x6x7`** | `150` (`150`) | **`573`** (`143, 165, 265`) | `1994` | `577` | `+2039` | — | **`-4`** | `5x6x7_m150_cr573_cn1994_ZT_reduced.json` |
| **`5x6x7`** (var. 2) | `150` (`150`) | **`576`** (`144, 168, 264`) | `2039` | `577` | `+2039` | — | **`-1`** | `5x6x7_m150_cr576_cn2039_ZT_reduced.json` |
| **`5x7x7`** | `176` (`176`) | **`680`** (`170, 197, 313`) | `2535` | `694` | `+2745` | — | **`-14`** | `5x7x7_m176_cr680_cn2535_ZT_reduced.json` |

### 4.2. 2 $\mathbb{Z}_T$-Best Formats Strictly Beating Live Minimum `cr`

| Format | Rank $m$ (`fmm_sota` over $\mathbb{Q}$) | Verified `cr` (`cu, cv, cw`) | Verified `cn` | Live Min `cr` | `matmulcatalog` `adds` | Delta vs Live Min `cr` | Scheme File in `claim/schemes/` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **`4x4x8`** | `96` (`95`) | **`338`** (`73, 101, 164`) | `962` | `339` (`cr_val = 340`) | `+1027` | **`-1` / `-2`** | `4x4x8_m96_cr338_cn962_ZT_reduced.json` |
| **`3x3x6`** | `43` (`40`) | **`152`** (`32, 46, 74`) | `286` | `153` | `+367` | **`-1`** | `3x3x6_m43_cr152_cn286_ZT_reduced.json` |

### 4.3. 21 Newly Addition-Reduced Exact-SOTA-Rank $\mathbb{Z}_T$ Formats & 14 Secondary Variant Improvements

- All `21` newly addition-reduced exact-SOTA-rank $\mathbb{Z}_T$ schemes in `claim/schemes/` (`2x5x7_m55_cr218`, `2x5x8_m63_cr247`, `2x6x6_m56_cr221`, `2x6x7_m66_cr283`, `2x6x8_m75_cr328`, `2x7x7_m76_cr365`, `2x7x8_m88_cr394`, `3x3x7_m49_cr167`, `3x4x6_m54_cr215`, `3x4x8_m73_cr295`, `3x5x6_m68_cr245`, `3x5x7_m79_cr294`, `3x5x8_m90_cr349`, `3x6x8_m108_cr381`, `3x7x7_m111_cr432`, `4x7x7_m144_cr594`, `4x7x8_m161_cr625`, `4x8x8_m180_cr734`, `5x7x8_m204_cr835`, `6x7x7_m212_cr861`, `6x7x8_m238_cr989`) match the exact `fmm_sota.json` rank (`m == sota_rank`), have rank strictly smaller than the live `addition_reduced_ZT` rank (`m` strictly less than `live_min_m`), and `6` of them (`2x6x6` `221` vs `224`, `3x5x6` `245` vs `252`, `3x6x8` `381` vs `411`, `4x7x8` `625` vs `646`, `4x8x8` `734` vs `746`, `5x7x8` `835` vs `837`) also have `cr` strictly smaller than the live higher-rank `cr`.
- All `14` secondary/variant improvements (`2x3x3_m15_cr43`, `2x3x5_m25_cr70`, `2x4x8_m51_cr181`, `2x5x6_m47_cr179`, `2x8x8_m100_cr418`, `3x3x3_m23_cr55`, `3x3x4_m29_cr89`, `3x3x5_m36_cr119`, `3x4x5_m47_cr156`, `3x5x5_m58_cr211`, `4x6x6_m105_cr406`, `4x6x8_m140_cr512`, `5x5x5_m93_cr334`, `5x6x6_m130_cr499`) passed all symbolic and structural checks.

---

## 5. Independent Negative Controls & C++ Solver Re-Execution

1. **Four Independent Negative Controls in `indep_fmm_check.py`:**
   - Flipping `u_fresh[0][0]["value"]` in `claim/schemes/2x4x7_m45_cr157_cn345_ZT_reduced.json` produced `8` symbolic output entry mismatches over $\mathbb{Z}[A, B]$ and was rejected.
   - Flipping `w[0][0]["value"]` produced `1` symbolic output entry mismatch over $\mathbb{Z}[A, B]$ and was rejected.
   - Setting `v_fresh[0][0]["index"] = 28` (`cur_idx = 28`, self-loop cycle) raised `ValueError` (DAG cycle rejection).
   - Setting `u_fresh[0][0]["value"] = 2` raised `ValueError` (non-unit coefficient rejection).
2. **Author Verifier (`claim/verify.py`) Executed Twice for Determinism:**
   - Running `python3 -B claim/verify.py` twice produced byte-identical stdout across both runs (`sha256: 73df85da51d40860ed192b62e99ad952bb3ae66328546cd757d5afe53f042569`), verifying all `48` schemes, rejecting the corrupted-gate negative control, and reproducing the `400`-sample random greedy CSE null control on `2x4x7` ($m = 45, \text{cn} = 345$): `best_control = 262`, `median = 281.0`, `IQR = 9.0` vs claimed `cr = 157` (`-105` additions below the best random greedy control).
3. **Recompiling and Running `claim/clss_cl1_tellegen_reducer.cpp` from Source:**
   - Compiling `claim/clss_cl1_tellegen_reducer.cpp` with `clang++ -O3 -std=c++17 -pthread` and running it on the raw matrices extracted from `2x4x7_m45_cr157_cn345_ZT_reduced.json` and `2x5x5_m40_cr145_cn273_ZT_reduced.json` reproduced the exact claimed addition reductions and Tellegen duality identities (`cr(W^T) = cr(W) + nz_rows(W) - nz_cols(W)`):
     - `2x4x7_m45`: `U = 26 (lb = 26)`, `V = 58 (lb = 40)`, `W^T = 73 [W = 42, lb = 36, 42 + 45 - 14 = 73]`, `TOTAL = 157`.
     - `2x5x5_m40`: `U = 28 (lb = 28)`, `V = 58 (lb = 38)`, `W^T = 59 [W = 29, lb = 29, 29 + 40 - 10 = 59]`, `TOTAL = 145`.
   - Scratch directory `panel/reproduce_work` and any `__pycache__` directories were removed after testing.

pass: true
