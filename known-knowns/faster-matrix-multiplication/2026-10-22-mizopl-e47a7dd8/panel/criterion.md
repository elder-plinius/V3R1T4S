# Panelist Report — CRITERION (`fmm-additive-complexity-records`)

context: Antigravity fresh subagent (invoke_subagent, role CRITERION)
role: CRITERION
target_id: fmm-additive-complexity-records
confirmed_scope: 4 explicit ternary (ZT) straight-line programs in object/schemes/ (indexed in object/CERTIFICATE.json, 3699 bytes, sha256 4a2e07b5d438be3327737929448819782885fb1eb1ba946acabeda846082cbb6, and verified symbolically over Z[A, B] by verify-it-yourself/verify.py, 10050 bytes, sha256 f6fad5a2883ba369fb33c743e2f45ab2c9167c15ec443c677a33b26fac0b505d), synthesized from Perminov's unreduced/naive source schemes (3x3x7_m49_ZT.json, 3x5x6_m68_ZT.json, 3x5x7_m79_ZT.json, 5x6x6_m130_c1697_ZT.json) across 4 exact-SOTA-rank formats with max(n, m, p) <= 8: 3x3x7 m=49 (cr=167, cn=404; no rank-49 file upstream when PR opened at 2026-10-22T02:57Z), 3x5x6 m=68 (cr=245, cn=494; no rank-68 file upstream vs m=70 cr=252), 3x5x7 m=79 (cr=294, cn=520; no rank-79 file upstream), and 5x6x6 m=130 (cr=492, cn=1697 vs live 499 [-7] and merged V3R1T4S 502 [-10]), later tied independently upstream by Alexander Perminov in commit 1781ca392cb26808f88e6f92a26894ab3727910f (2026-10-22T15:24:59Z, docs/additions.md).

---

## 1. Mandate & Literal Clause-by-Clause Audit

As the **CRITERION** skeptic panelist, my mandate is to decide literally whether the result in `object/` meets the full `success_criterion` and/or enumerated `partial_wins` (`p3`), hunt hidden quantifiers and stretched definitions, check null models and negative controls, and write an exact `confirmed_scope` no wider than the evidence.

### Clause (1): Format $(n, m, p)$ with $\max(n, m, p) \le 8$, Exact `fmm_sota.json` Rank $r$, and No Double-Counting with Rank-Reduction Targets
- **Reference Snapshot Verified:** `https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json` (`343,774` bytes, `sha256: 2a6535154ac877aeb495f9294a5e97c3dbf1b1969aefe6ffc0a612f2cf01cbae`).
- **Audit Result:** All `4` submitted formats satisfy $\max(n, m, p) \le 8$ and have rank $m$ literally equal to the best rank $r$ listed in `fmm_sota.json` (`m == sota_rank`):
  1. `3x3x7`: $\max(3, 3, 7) = 7 \le 8$, $m = 49 = r_{\text{SOTA}}$, synthesized from `schemes/results/ZT/3x3x7_m49_ZT.json` (`sha256: 52147707b318e29596e6faf0d66102911dd9e3f86d9bd0094b0e6b1896070fff`).
  2. `3x5x6`: $\max(3, 5, 6) = 6 \le 8$, $m = 68 = r_{\text{SOTA}}$, synthesized from `schemes/results/ZT/3x5x6_m68_ZT.json` (`sha256: 9675decf7533fae8ac643c4cf6fccff63f9ef76f41fc781888a7b806cd6e8cac`).
  3. `3x5x7`: $\max(3, 5, 7) = 7 \le 8$, $m = 79 = r_{\text{SOTA}}$, synthesized from `schemes/results/ZT/3x5x7_m79_ZT.json` (`sha256: 9f94da6729e900a0ee525b97935d03d35306159626459768a553abf852cff0c6`).
  4. `5x6x6`: $\max(5, 6, 6) = 6 \le 8$, $m = 130 = r_{\text{SOTA}}$, synthesized from `schemes/results/naive_addition_reduced_ZT/5x6x6_m130_c1697_ZT.json` (`sha256: 125bdb24d3c3303130fc9be98c98f9421ddd197b27894dada481a8d23ab4b0c7`).
- **No Double-Counting Check:** None of these `4` schemes lowers the rank $r$; all `4` use existing rank-$r$ ternary tensors from Perminov's `ZT/` and `naive_addition_reduced_ZT/` directories and optimize the reduced addition count `cr = cu + cv + cw`.

### Clause (2): Explicit Straight-Line Program Verified Symbolically over $\mathbb{Z}$ under Perminov's `reduced` Convention
- **Verifier & Certificate Integrity:**
  - `object/CERTIFICATE.json`: `3,699` bytes, `sha256: 4a2e07b5d438be3327737929448819782885fb1eb1ba946acabeda846082cbb6`.
  - `verify-it-yourself/verify.py`: `10,050` bytes, `sha256: f6fad5a2883ba369fb33c743e2f45ab2c9167c15ec443c677a33b26fac0b505d`.
  - `how-we-built-it/clss_cl1_tellegen_reducer.cpp`: `24,238` bytes, `sha256: c4dbcec6ab78e5a335bb993689806e4672509c42e8e8a5f3dbe39b4629ad1c66`.
- **Symbolic Polynomial Identity & Ternary SLP Rules:**
  Running `verify-it-yourself/verify.py` confirms across all `4` scheme files in `object/schemes/`:
  - Every `u_fresh`, `v_fresh`, `w_fresh` node references strictly earlier indices (`0 <= idx < cur_idx`, strict DAG acyclicity).
  - Every coefficient `value` in `u_fresh`, `u`, `v_fresh`, `v`, `w_fresh`, `w` belongs strictly to $\{-1, +1\}$ (`require_unit_coeffs=True`), with zero scalar multiplications by $\pm 2$ or any non-unit scalar (`cr_len == cr_val` on all `4 / 4` claimed files).
  - The three blocks $U$, $V$, and $W$ are completely separated (`nin = n1*n2`, `n2*n3`, and `m` respectively), with zero cross-sharing between $A$-linear forms and $B$-linear forms.
  - Symbolic expansion over $\mathbb{Z}[A, B]$ confirms that $\sum_{r=0}^{m-1} W_{r, (i, j)} U_r(A) V_r(B) = \sum_{k=0}^{n_2-1} A_{i, k} B_{k, j}$ holds with `0` polynomial errors across all $(i, j)$ entries for all `4` schemes.

### Clause (3): Comparison Against Live Sources at PR Opening (`2026-10-22T02:57Z`) and Dated Independent Upstream Ties
- **Reference Snapshots Checked (by URL & SHA-256):**
  - `https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json` (`343,774` bytes, `sha256: 2a6535154ac877aeb495f9294a5e97c3dbf1b1969aefe6ffc0a612f2cf01cbae`).
  - `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/reduced_known.json` (`1,189` bytes, `sha256: ef67c13792b0e770578de4ff01438178ce4e6ac4efd60a3580f3131e31907a5d`).
  - `https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md` (`94,842` bytes, `sha256: c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7`; current `COVERAGE.md` values at ranks `49`, `68`, `79`, `130`: `+404`, `+482`, `+520`, `+1716`).
  - Upstream `addition_reduced_ZT` files at PR opening (`2026-10-22T02:57Z`): `3x5x6_m70_cr252_cn561_ZT_reduced.json` (`sha256: 61d9be14020b7c2e2a5193b4a4c616e3414e53840d3d2c5a6a876af6836bc0f0`), `3x5x6_m70_cr265_cn561_ZT_reduced.json` (`sha256: 4b5148d2af0c2ce96e809274b01011568fedd33687082859c2012c994b4379f9`), `5x6x6_m130_cr499_cn1716_ZT_reduced.json` (`sha256: f1f3b7a40fee69e36ebe57f82ba2b1ac983fbacc7f4299cad39a47080f7f9a0b`), `5x6x6_m130_cr562_fv250_cn1716_ZT_reduced.json` (`sha256: 8f899e560b2d2976b031272c59ebf6ea0472ae2d9616eaeb05d52027d818344f`).
- **Exact Comparison Across the 4 Submitted Formats:**

| Format | Rank $m$ (`fmm_sota`) | Claimed `cr` (`cu, cv, cw`) | Claimed `cn` | Credited Source Scheme | Upstream Status at PR Opening (`2026-10-22T02:57Z`) | Independent Upstream Tie (`commit 1781ca39`, `2026-10-22T15:24:59Z`, `docs/additions.md`) | `matmulcatalog` `adds` | Scheme File in `object/schemes/` | SHA-256 Digest |
| :--- | :---: | :---: | :---: | :--- | :--- | :--- | :---: | :--- | :--- |
| **`3x3x7`** | `49` (`49`) | **`167`** (`33, 53, 81`) | `404` | `3x3x7_m49_ZT.json` | No `m=49` file (`m=51, cr=146`) | `167` (`3x3x7_m49_cr167_cn404_ZT_reduced.json`, published independently) | `+404` ($r=49$) | `3x3x7_m49_cr167_cn404_ZT_reduced.json` | `2f10739cd6200745967118e413c1433a1781a8db374eb3343c3fe92c7a7fc280` |
| **`3x5x6`** | `68` (`68`) | **`245`** (`56, 78, 111`) | `494` | `3x5x6_m68_ZT.json` | No `m=68` file (`m=70, cr=252`) | `245` (`3x5x6_m68_cr245_cn494_ZT_reduced.json`, published independently) | `+482` ($r=68$) | `3x5x6_m68_cr245_cn494_ZT_reduced.json` | `4271edeb86e3c452ebaa6edec9647590162e7093a0b4468b5c5dbc866acc850f` |
| **`3x5x7`** | `79` (`79`) | **`294`** (`66, 97, 131`) | `520` | `3x5x7_m79_ZT.json` | No `m=79` file (`m=83, cr=291`) | `294` (`3x5x7_m79_cr294_cn520_ZT_reduced.json`, published independently) | `+520` ($r=79$) | `3x5x7_m79_cr294_cn520_ZT_reduced.json` | `7aaaceef49b6d190b1a50d3779209c6b216bedef03578144602a8d3808c4e977` |
| **`5x6x6`** | `130` (`130`) | **`492`** (`128, 139, 225`) | `1697` | `5x6x6_m130_c1697_ZT.json` | `499` (`cr499`, `cr562_fv250`); V3R1T4S merged `502` | `492` (`5x6x6_m130_cr492_cn1697_ZT_reduced.json`, published independently) | `+1716` ($r=130$) | `5x6x6_m130_cr492_cn1697_ZT_reduced.json` | `b17cdb716cc62a02d0b7d5fa982067147dd3c2ea721723986fa5af9e3e2a27b2` |

### Clause (4): Enumerated Partial Win `p3`
- Partial win `p3` requires *"Strict reduced-addition improvements for at least three distinct formats with `max dim <= 8` in one shift, each verified symbolically and each below the live `addition_reduced_ZT` count."*
- With `4` distinct exact-SOTA-rank formats (`3x3x7`, `3x5x6`, `3x5x7`, `5x6x6`), `p3` (`4 >= 3`) and the full success criterion at filing are satisfied.

### Clause (5): Negative Control & Null Model Verification
- **Corrupted-Gate Negative Control:** Flipping `u_fresh[0][0]["value"] *= -1` in `object/schemes/3x3x7_m49_cr167_cn404_ZT_reduced.json` causes `verify_symbolic_product_over_Z` in `verify-it-yourself/verify.py` to immediately raise `AssertionError`.
- **400-Sample Random Greedy CSE Null Control (`seed = 20261022`):** Running `400` random-order disjoint-pair greedy CSE reductions on the exact same `3x3x7` ($m = 49, \text{cn} = 404$) tensor yields `best_control = 304`, `median = 336`, `IQR = 13` additions, whereas the $\text{Cl}_1$ + Tellegen SLP in `object/schemes/3x3x7_m49_cr167_cn404_ZT_reduced.json` achieves `cr = 167` (`-137` additions below `best_control`).

---

## 2. Verdict

Every clause of the `success_criterion`, enumerated partial win `p3`, and `verification_method` is literally satisfied with zero stretched definitions or hidden quantifiers.

pass: true
