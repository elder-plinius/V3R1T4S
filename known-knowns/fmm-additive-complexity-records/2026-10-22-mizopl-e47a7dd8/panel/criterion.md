# Panelist Report — CRITERION (`fmm-additive-complexity-records`)

context: Antigravity fresh subagent (invoke_subagent, role CRITERION)
role: CRITERION
target_id: fmm-additive-complexity-records
confirmed_scope: 48 explicit ternary (ZT) straight-line programs in claim/schemes/ (indexed in claim/CERTIFICATE.json, sha256 e47a7dd88e8f9778d65667b7d4030ca66cf39c6de9d89b3b0f1c5f61cb9cc1de, and verified symbolically over Z[A, B] by claim/verify.py, sha256 d0a557971cd72c8c588d4a35e31b9f2135c5e421ef6caddb64a940a02f695c40) establishing strictly lower reduced addition counts cr = cu + cv + cw below the live minimum cr across all files in Perminov's addition_reduced_ZT repository, reduced_known.json, Lille catalogue, and matmulcatalog COVERAGE.md for 9 distinct exact-SOTA-rank formats with max(n, m, p) <= 8 (2x4x7 m=45: cr=157 and 164 vs 168, -11; 2x5x5 m=40: cr=145 vs 147, -2; 4x5x8 m=118: cr=447 vs 466, -19; 4x6x7 m=123: cr=464 vs 468, -4; 5x5x6 m=110: cr=406 vs 411, -5; 5x5x8 m=144: cr=548 vs 555, -7; 5x6x6 m=130: cr=492 vs 499, -7; 5x6x7 m=150: cr=573 and 576 vs 577, -4; 5x7x7 m=176: cr=680 vs 694, -14; satisfying both the full success criterion and partial win p3 >= 3 formats by 3x), plus 2 ZT-best formats (4x4x8 m=96: cr=338 vs 339/340; 3x3x6 m=43: cr=152 vs 153) and 21 newly addition-reduced exact-SOTA-rank ZT formats (6 of which also beat the older higher-rank cr: 2x6x6 m=56 cr=221, 3x5x6 m=68 cr=245, 3x6x8 m=108 cr=381, 4x7x8 m=161 cr=625, 4x8x8 m=180 cr=734, 5x7x8 m=204 cr=835).

---

## 1. Mandate & Literal Clause-by-Clause Audit

As the **CRITERION** skeptic panelist, my mandate is to decide literally whether the result in `claim/` meets the full `success_criterion` and/or enumerated `partial_wins` (`p3`), hunt hidden quantifiers and stretched definitions, check null models and negative controls, and write an exact `confirmed_scope` no wider than the evidence.

### Clause (1): Format $(n, m, p)$ with $\max(n, m, p) \le 8$, Exact `fmm_sota.json` Rank $r$, and No Double-Counting with Rank-Reduction Targets
- **Reference Snapshot Verified:** `claim/reference_live_champions/fmm_sota.json` (`343,774` bytes, `sha256: 2a6535154ac877aeb495f9294a5e97c3dbf1b1969aefe6ffc0a612f2cf01cbae`).
- **Audit Result:** All `9` primary winning formats satisfy $\max(n, m, p) \le 8$, have rank $m$ literally equal to the best rank $r$ listed in `claim/reference_live_champions/fmm_sota.json`, and match the rank of the existing `addition_reduced_ZT` files (`m == sota_rank == live_min_m`):
  1. `2x4x7`: $\max(2, 4, 7) = 7 \le 8$, $m = 45 = r_{\text{SOTA}} = m_{\text{live}}$.
  2. `2x5x5`: $\max(2, 5, 5) = 5 \le 8$, $m = 40 = r_{\text{SOTA}} = m_{\text{live}}$.
  3. `4x5x8`: $\max(4, 5, 8) = 8 \le 8$, $m = 118 = r_{\text{SOTA}} = m_{\text{live}}$.
  4. `4x6x7`: $\max(4, 6, 7) = 7 \le 8$, $m = 123 = r_{\text{SOTA}} = m_{\text{live}}$.
  5. `5x5x6`: $\max(5, 5, 6) = 6 \le 8$, $m = 110 = r_{\text{SOTA}} = m_{\text{live}}$.
  6. `5x5x8`: $\max(5, 5, 8) = 8 \le 8$, $m = 144 = r_{\text{SOTA}} = m_{\text{live}}$.
  7. `5x6x6`: $\max(5, 6, 6) = 6 \le 8$, $m = 130 = r_{\text{SOTA}} = m_{\text{live}}$.
  8. `5x6x7`: $\max(5, 6, 7) = 7 \le 8$, $m = 150 = r_{\text{SOTA}} = m_{\text{live}}$.
  9. `5x7x7`: $\max(5, 7, 7) = 7 \le 8$, $m = 176 = r_{\text{SOTA}} = m_{\text{live}}$.
- **No Double-Counting Check:** None of these `9` primary formats lowers the rank $r$, strictly obeying the clause *"Each scheme is claimed once: a scheme that also lowers the rank is a rank target, not this one."* Furthermore, the `21` newly addition-reduced SOTA-rank `ZT` formats (`m == sota_rank < live_min_m`) use existing rank-$r$ ternary tensors from Perminov's `ZT/` and `naive_addition_reduced_ZT/` directories (so they do not claim a new rank record either; they provide the first `addition_reduced_ZT` straight-line programs at the known SOTA rank).

### Clause (2): Explicit Straight-Line Program Verified Symbolically over $\mathbb{Z}$ under Perminov's `reduced` Convention
- **Verifier & Certificate Integrity:**
  - `claim/CERTIFICATE.json`: `26,573` bytes, `sha256: e47a7dd88e8f9778d65667b7d4030ca66cf39c6de9d89b3b0f1c5f61cb9cc1de`.
  - `claim/verify.py`: `12,782` bytes, `sha256: d0a557971cd72c8c588d4a35e31b9f2135c5e421ef6caddb64a940a02f695c40`.
  - `claim/clss_cl1_tellegen_reducer.cpp`: `24,238` bytes, `sha256: c4dbcec6ab78e5a335bb993689806e4672509c42e8e8a5f3dbe39b4629ad1c66`.
- **Symbolic Polynomial Identity & Ternary SLP Rules:**
  Running `claim/verify.py` (and our independent audit script) confirms across all `48` scheme files in `claim/schemes/`:
  - Every `u_fresh`, `v_fresh`, `w_fresh` node references strictly earlier indices (`0 <= idx < cur_idx`, strict DAG acyclicity).
  - Every coefficient `value` in `u_fresh`, `u`, `v_fresh`, `v`, `w_fresh`, `w` belongs strictly to $\{-1, +1\}$ (`require_unit_coeffs=True`), with zero scalar multiplications by $\pm 2$ or any non-unit scalar (`cr_len == cr_val` on all `48 / 48` claimed files).
  - The three blocks $U$, $V$, and $W$ are completely separated (`nin = n1*n2`, `n2*n3`, and `m` respectively), with zero cross-sharing between $A$-linear forms and $B$-linear forms.
  - Symbolic expansion over $\mathbb{Z}[A, B]$ confirms that $\sum_{r=0}^{m-1} W_{r, (i, j)} U_r(A) V_r(B) = \sum_{k=0}^{n_2-1} A_{i, k} B_{k, j}$ holds with `0` polynomial errors across all $(i, j)$ entries for all `48` schemes.
- **Counter Calibration on 36 Live Reference Champion Files:**
  Calibrating the addition counter across all `36` reference `.json` files (`18` formats) in `claim/reference_live_champions/*_ZT_reduced.json` confirms `0` symbolic errors and exact agreement with Perminov's `complexity.reduced` and `complexity.naive` fields, while exposing two undocumented `value = 2` entries inside Perminov's own reference files (`4x4x8_m96_cr339_cn973_ZT_reduced.json` at `w_fresh[60]` index `71`, where `cr_len = 339, cr_val = 340`; and `5x6x8_m170_cr663_cn2312_ZT_reduced.json` at `v[92]` index `106`, where `cr_len = 662, cr_val = 663`).

### Clause (3): Strictly Less (`direction: min`) Than the Minimum `cr` Across All Live Sources
- **Reference Snapshots Checked:**
  - All `36` live `addition_reduced_ZT` files for the target formats in `claim/reference_live_champions/*_ZT_reduced.json`.
  - `claim/reference_live_champions/reduced_known.json` (`1,189` bytes, `sha256: ef67c13792b0e770578de4ff01438178ce4e6ac4efd60a3580f3131e31907a5d`).
  - `claim/reference_live_champions/matmulcatalog_COVERAGE.md` (`94,842` bytes, `sha256: c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7`).
- **Exact Comparison Across All 9 Primary Exact-SOTA Formats (`11` Scheme Files):**

| Format | Rank $m$ (`fmm_sota`) | Claimed `cr` (`cu, cv, cw`) | Claimed `cn` | Live `addition_reduced_ZT` All Files (`cr_len / cr_val`) | `reduced_known.json` | `matmulcatalog` `adds` | Delta vs Live Min `cr` | Scheme File in `claim/schemes/` | SHA-256 Digest |
| :--- | :---: | :---: | :---: | :--- | :---: | :---: | :---: | :--- | :--- |
| **`2x4x7`** | `45` (`45`) | **`157`** (`26, 58, 73`) | `345` | `168` (`cr168`), `174` (`cr174`) | — | `+308` | **`-11`** | `2x4x7_m45_cr157_cn345_ZT_reduced.json` | `13925cb4e3fef5c3e0a79d18855b4a16ef3a0f361923e4f53fa835b9df231840` |
| **`2x4x7`** (var. 2) | `45` (`45`) | **`164`** (`27, 64, 73`) | `285` | `168` (`cr168`), `174` (`cr174`) | — | `+308` | **`-4`** | `2x4x7_m45_cr164_cn285_ZT_reduced.json` | `2d85f22f397ead7f6895ecaf7645a83aacc429c857b3a9f4cebe2e42110c7730` |
| **`2x5x5`** | `40` (`40`) | **`145`** (`28, 58, 59`) | `273` | `147` (`cr147`), `153` (`cr153`) | `Z: 313, Z2: 218` | `+256` | **`-2`** | `2x5x5_m40_cr145_cn273_ZT_reduced.json` | `c7e30b3f2d2eb218e6015b88ad44e4e3631a41832237f48c5351514ac9eb9c3a` |
| **`4x5x8`** | `118` (`118`) | **`447`** (`96, 141, 210`) | `1463` | `466` (`cr466`), `513` (`cr513_fv249`) | — | `+1521` | **`-19`** | `4x5x8_m118_cr447_cn1463_ZT_reduced.json` | `6a20a2b001f5255155c8a4da0d93bc8b2fd9562f03ddccea8ed0b4180287022d` |
| **`4x6x7`** | `123` (`123`) | **`464`** (`112, 138, 214`) | `1562` | `468` (`cr468`), `517` (`cr517`) | — | `+1586` | **`-4`** | `4x6x7_m123_cr464_cn1562_ZT_reduced.json` | `2b78b41c57f3b26640504a2fbc2fbc555a85dc0b535f1b19e40b0aab56e2e082` |
| **`5x5x6`** | `110` (`110`) | **`406`** (`105, 110, 191`) | `1192` | `411` (`cr411`), `460` (`cr460_fv204`) | — | `+1215` | **`-5`** | `5x5x6_m110_cr406_cn1192_ZT_reduced.json` | `4cbc3596ab458b161d627f90cf2969eac1f9926844eb2d1bcda0702cc7d20ffe` |
| **`5x5x8`** | `144` (`144`) | **`548`** (`130, 156, 262`) | `1872` | `555` (`cr555`), `620` (`cr620_fv281`) | — | `+1908` | **`-7`** | `5x5x8_m144_cr548_cn1872_ZT_reduced.json` | `26e8fee0b3ca63a807b866972ea65448afba7d4188c09fd18b9f249e5c964244` |
| **`5x6x6`** | `130` (`130`) | **`492`** (`128, 139, 225`) | `1697` | `499` (`cr499`), `562` (`cr562_fv250`) | — | `+1716` | **`-7`** | `5x6x6_m130_cr492_cn1697_ZT_reduced.json` | `b17cdb716cc62a02d0b7d5fa982067147dd3c2ea721723986fa5af9e3e2a27b2` |
| **`5x6x7`** | `150` (`150`) | **`573`** (`143, 165, 265`) | `1994` | `577` (`cr577`), `664` (`cr664_fv310`) | — | `+2039` | **`-4`** | `5x6x7_m150_cr573_cn1994_ZT_reduced.json` | `e7b7f15ceb2237c93ba7ac363c3f70bf0bd520b669ff32d0595bd57a716059d4` |
| **`5x6x7`** (var. 2) | `150` (`150`) | **`576`** (`144, 168, 264`) | `2039` | `577` (`cr577`), `664` (`cr664_fv310`) | — | `+2039` | **`-1`** | `5x6x7_m150_cr576_cn2039_ZT_reduced.json` | `e2e3d0b05e3e142fb07b104f45c2dbbcd6eb48b9c071ca1acbdaaf95766220b2` |
| **`5x7x7`** | `176` (`176`) | **`680`** (`170, 197, 313`) | `2535` | `694` (`cr694`), `788` (`cr788_fv371`) | — | `+2745` | **`-14`** | `5x7x7_m176_cr680_cn2535_ZT_reduced.json` | `d8735ca9ebf4adf6a4bac9ab5af0906aafdc5247f80ec0a62f4507014e749d39` |

- **Additional Verified Categories in `claim/CERTIFICATE.json`:**
  - **2 $\mathbb{Z}_T$-Best Formats** (where `fmm_sota.json`'s rank uses non-ternary $\mathbb{Q}$ coefficients):
    - `4x4x8` ($m = 96$, best $\mathbb{Z}_T / \mathbb{Z}$ rank; `fmm_sota.json` `95` is over $\mathbb{Q}$): `claim/schemes/4x4x8_m96_cr338_cn962_ZT_reduced.json` (`54,254` bytes, `sha256: eae682903920cd0ad9b3fda33f483b23cefaf1612e089e175367ba50249d1ae4`), **`cr = 338`** (`cu = 73, cv = 101, cw = 164`, `cn = 962`) vs live `339` (`cr_val = 340`) and `377` (`cr377_fv171`), and `+1027` in `matmulcatalog` `COVERAGE.md` (**`-1` / `-2` additions**).
    - `3x3x6` ($m = 43$): `claim/schemes/3x3x6_m43_cr152_cn286_ZT_reduced.json` (`23,856` bytes, `sha256: 1753cc9f70d6d518d22bd8612c21de2d35db0b05b9ecc42f5de9e4b8bdbec136`), **`cr = 152`** (`cu = 32, cv = 46, cw = 74`, `cn = 286`) vs live `153` (`cr153`) and `160` (`cr160`) (**`-1` addition**).
  - **21 Newly Addition-Reduced Exact-SOTA-Rank $\mathbb{Z}_T$ Formats** (`6` of which also achieve `cr` strictly below the older higher-rank `cr` in `addition_reduced_ZT`):
    - `2x6x6` ($m = 56$ vs live $m = 57$): `cr = 221` vs `224` (`-1` mult, `-3` additions; `reduced_known.json` `Z: 419, Z2: 327`; `matmulcatalog` `+535`).
    - `3x5x6` ($m = 68$ vs live $m = 70$): `cr = 245` vs `252` (`-2` mults, `-7` additions; `matmulcatalog` `+482`).
    - `3x6x8` ($m = 108$ vs live $m = 113$): `cr = 381` vs `411` (`-5` mults, `-30` additions; `matmulcatalog` `+1412`).
    - `4x7x8` ($m = 161$ vs live $m = 164$): `cr = 625` vs `646` (`-3` mults, `-21` additions; `matmulcatalog` `+2270`).
    - `4x8x8` ($m = 180$ vs live $m = 182$): `cr = 734` vs `746` (`-2` mults, `-12` additions; `matmulcatalog` `+2888`).
    - `5x7x8` ($m = 204$ vs live $m = 206$): `cr = 835` vs `837` (`-2` mults, `-2` additions; `matmulcatalog` `+2606`).

### Clause (4): Enumerated Partial Win `p3`
- Partial win `p3` requires *"Strict reduced-addition improvements for at least three distinct formats with `max dim <= 8` in one shift, each verified symbolically and each below the live `addition_reduced_ZT` count."*
- With `9` distinct exact-SOTA formats (plus `2` $\mathbb{Z}_T$-best formats and `6` newly reduced SOTA-rank formats beating the older higher-rank `cr`), `p3` is exceeded by $3\times$ (`9 >= 3`) and subsumed into the full success criterion.

### Clause (5): Negative Control & Null Model Verification
- **Corrupted-Gate Negative Control:** Flipping `u_fresh[0][0]["value"] *= -1` in `claim/schemes/2x4x7_m45_cr157_cn345_ZT_reduced.json` causes `verify_symbolic_product_over_Z` in `claim/verify.py` to immediately raise `AssertionError`.
- **400-Sample Random Greedy CSE Null Control (`seed = 20261022`):** Running `400` random-order disjoint-pair greedy CSE reductions (without $\text{Cl}_1$ target closure or Tellegen transposition on $W^T$) on the exact same `2x4x7` ($m = 45, \text{cn} = 345$) tensor yields `best_control = 262`, `median = 281.0`, `IQR = 9.0` additions, whereas the $\text{Cl}_1$ + Tellegen SLP in `claim/schemes/2x4x7_m45_cr157_cn345_ZT_reduced.json` achieves `cr = 157` (`-105` additions below `best_control`).

---

## 2. Verdict

Every clause of the `success_criterion`, enumerated partial win `p3`, and `verification_method` is literally satisfied with zero stretched definitions or hidden quantifiers.

pass: true
