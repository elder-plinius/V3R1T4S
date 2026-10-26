# Panelist Report — Role: REPRODUCE

context: Antigravity fresh subagent (invoke_subagent, role REPRODUCE)
target: `fmm-additive-complexity-records` (`algorithms/fmm-additive-complexity-records`)

## 1. Mandate & Verbatim Definition Quoted Before Inspecting Author Code

Per step 6 of the verification protocol:
> "Before reading the author's code, write your own checker from the definition (quote it). Verify every property and the claimed value from the saved files; re-derive every proof step. For an exhaustive search, a sample is a spot check and cannot pass. Fail on any mismatch, missing object or non-determinism."

Before reading `verify-it-yourself/verify.py` or `how-we-built-it/clss_cl1_tellegen_reducer.cpp`, I read `README.md`, `RUN_IT_YOURSELF.md`, and `object/CERTIFICATE.json`, quoted the verbatim target definition:
> "An explicit straight-line program (list of linear forms over the inputs, r products, and linear forms producing the outputs) for a format `\langle n,m,p \rangle` with `max(n,m,p) \le 8` and rank `r` equal to the best rank listed for that format in `fmm_sota.json` (re-fetched live), that (1) is verified symbolically to compute the full product `A*B` exactly over `Z`, and (2) uses a number of additions/subtractions STRICTLY LESS (direction: min) than the smallest reduced addition count for that format and rank in Perminov's live repository (the `addition_reduced_ZT` scheme file for the format, `reduced_known.json`, `README` and `CHANGELOG`) re-fetched live immediately before claiming, counted under Perminov's 'reduced' convention (each binary `+/-` between already-computed quantities counts one; multiplication by `-1` is free; multiplication by any other scalar is not allowed in a ternary SLP), AND below any lower count published for that format and rank on the live Lille per-format page's cited complexity variant and in `matmulcatalog`'s live `COVERAGE.md` 'adds' column. If the Lille rank for the format is attained only with non-ternary coefficients, the comparison is against the best count in the same coefficient class as the candidate. The reference count is the MINIMUM `cr` value over all files for that format and rank in the live directory (formats have several files). Each scheme is claimed once: a scheme that also lowers the rank is a rank target, not this one."

and wrote a completely independent checker `indep_fmm_check.py` from scratch.

---

## 2. Artifact Integrity Verification (Byte Sizes & SHA-256 Digests)

My independent checker verified the exact byte counts and SHA-256 checksums of all package artifacts and all 4 scheme files in `object/schemes/`:

| Relative File Path | Verified Bytes | Verified SHA-256 Digest | Status |
| :--- | :---: | :--- | :---: |
| `object/CERTIFICATE.json` | `3,699` | `4a2e07b5d438be3327737929448819782885fb1eb1ba946acabeda846082cbb6` | PASS |
| `verify-it-yourself/verify.py` | `10,050` | `f6fad5a2883ba369fb33c743e2f45ab2c9167c15ec443c677a33b26fac0b505d` | PASS |
| `how-we-built-it/clss_cl1_tellegen_reducer.cpp` | `24,238` | `c4dbcec6ab78e5a335bb993689806e4672509c42e8e8a5f3dbe39b4629ad1c66` | PASS |
| `object/schemes/3x3x7_m49_cr167_cn404_ZT_reduced.json` | `26,027` | `2f10739cd6200745967118e413c1433a1781a8db374eb3343c3fe92c7a7fc280` | PASS |
| `object/schemes/3x5x6_m68_cr245_cn494_ZT_reduced.json` | `37,078` | `4271edeb86e3c452ebaa6edec9647590162e7093a0b4468b5c5dbc866acc850f` | PASS |
| `object/schemes/3x5x7_m79_cr294_cn520_ZT_reduced.json` | `45,808` | `7aaaceef49b6d190b1a50d3779209c6b216bedef03578144602a8d3808c4e977` | PASS |
| `object/schemes/5x6x6_m130_cr492_cn1697_ZT_reduced.json` | `77,200` | `b17cdb716cc62a02d0b7d5fa982067147dd3c2ea721723986fa5af9e3e2a27b2` | PASS |

---

## 3. Upstream Reference Metadata & Credited Source Schemes

`README.md`, `the-record-we-beat/table_status.md`, and `object/CERTIFICATE.json` record the URLs, byte sizes, and SHA-256 digests of the upstream reference sources (replacing third-party file copies):
- `https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json` (`343,774` bytes, `sha256: 2a6535154ac877aeb495f9294a5e97c3dbf1b1969aefe6ffc0a612f2cf01cbae`)
- `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/reduced_known.json` (`1,189` bytes, `sha256: ef67c13792b0e770578de4ff01438178ce4e6ac4efd60a3580f3131e31907a5d`)
- `https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md` (`94,842` bytes, `sha256: c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7`; current `COVERAGE.md` `adds` values: `+404`, `+482`, `+520`, `+1716` at ranks `49`, `68`, `79`, `130`)
- Upstream `addition_reduced_ZT` reference files at PR opening (`2026-10-22T02:57Z`):
  - `3x5x6_m70_cr252_cn561_ZT_reduced.json` (`17,967` bytes, `sha256: 61d9be14020b7c2e2a5193b4a4c616e3414e53840d3d2c5a6a876af6836bc0f0`)
  - `3x5x6_m70_cr265_cn561_ZT_reduced.json` (`17,027` bytes, `sha256: 4b5148d2af0c2ce96e809274b01011568fedd33687082859c2012c994b4379f9`)
  - `5x6x6_m130_cr499_cn1716_ZT_reduced.json` (`37,336` bytes, `sha256: f1f3b7a40fee69e36ebe57f82ba2b1ac983fbacc7f4299cad39a47080f7f9a0b`)
  - `5x6x6_m130_cr562_fv250_cn1716_ZT_reduced.json` (`35,833` bytes, `sha256: 8f899e560b2d2976b031272c59ebf6ea0472ae2d9616eaeb05d52027d818344f`)
- Credited Perminov unreduced/naive source schemes used as input tensors:
  - `schemes/results/ZT/3x3x7_m49_ZT.json` (`sha256: 52147707b318e29596e6faf0d66102911dd9e3f86d9bd0094b0e6b1896070fff`)
  - `schemes/results/ZT/3x5x6_m68_ZT.json` (`sha256: 9675decf7533fae8ac643c4cf6fccff63f9ef76f41fc781888a7b806cd6e8cac`)
  - `schemes/results/ZT/3x5x7_m79_ZT.json` (`sha256: 9f94da6729e900a0ee525b97935d03d35306159626459768a553abf852cff0c6`)
  - `schemes/results/naive_addition_reduced_ZT/5x6x6_m130_c1697_ZT.json` (`sha256: 125bdb24d3c3303130fc9be98c98f9421ddd197b27894dada481a8d23ab4b0c7`)

---

## 4. Independent Verification of All 4 Claimed Ternary SLP Files (`< 0.5s`)

Running `indep_fmm_check.py` across all `4` `.json` files in `object/schemes/` verified:
1. **Strict DAG Acyclicity:** Every node reference `idx` in `u_fresh[k]`, `v_fresh[k]`, `w_fresh[k]` satisfies $0 \le \text{idx} \lt \text{nin} + k$, and every reference in `u`, `v`, `w` satisfies $0 \le \text{idx} \lt \text{nin} + |\text{fresh}|$.
2. **Strictly Unit Ternary Coefficients:** Every coefficient `value` in `u_fresh`, `v_fresh`, `w_fresh`, `u`, `v`, `w` is in $\{-1, +1\}$ (`0` non-unit coefficients across all `4` files), and every expanded matrix $U, V, W^T$ has entries purely in $\{-1, 0, +1\}$.
3. **Exact Symbolic Polynomial Identity over $\mathbb{Z}[A, B]$:** For all `4` schemes and every output coordinate $(i, j) \in \{0, \dots, n_1-1\} \times \{0, \dots, n_3-1\}$,
   $$\sum_{r=0}^{m-1} W_{r, (i, j)} \left(\sum_{a, b} U_{r, (a, b)} A_{a, b}\right)\left(\sum_{c, d} V_{r, (c, d)} B_{c, d}\right) = \sum_{k=0}^{n_2-1} A_{i, k} B_{k, j}$$
   holds identically over $\mathbb{Z}[A, B]$ with `0` extra terms and `0` missing terms.
4. **Exact Addition Counts (`cr` and `cn`):** For all `4` files, `cr_len == cr_val == complexity.reduced == cu + cv + cw` and `cn == cnu + cnv + cnw == complexity.naive`, matching `object/CERTIFICATE.json` digit-for-digit:

| Format | Rank $m$ (`fmm_sota`) | Verified `cr` (`cu, cv, cw`) | Verified `cn` | Credited Source Scheme | Upstream Status at PR Opening (`2026-10-22T02:57Z`) | `matmulcatalog` `adds` | Scheme File in `object/schemes/` |
| :--- | :---: | :---: | :---: | :--- | :--- | :---: | :--- |
| **`3x3x7`** | `49` (`49`) | **`167`** (`33, 53, 81`) | `404` | `3x3x7_m49_ZT.json` | No `m=49` file (`m=51, cr=146`) | `+404` | `3x3x7_m49_cr167_cn404_ZT_reduced.json` |
| **`3x5x6`** | `68` (`68`) | **`245`** (`56, 78, 111`) | `494` | `3x5x6_m68_ZT.json` | No `m=68` file (`m=70, cr=252`) | `+482` | `3x5x6_m68_cr245_cn494_ZT_reduced.json` |
| **`3x5x7`** | `79` (`79`) | **`294`** (`66, 97, 131`) | `520` | `3x5x7_m79_ZT.json` | No `m=79` file (`m=83, cr=291`) | `+520` | `3x5x7_m79_cr294_cn520_ZT_reduced.json` |
| **`5x6x6`** | `130` (`130`) | **`492`** (`128, 139, 225`) | `1697` | `5x6x6_m130_c1697_ZT.json` | `499` (`cr499`, `cr562_fv250`); V3R1T4S merged `502` | `+1716` | `5x6x6_m130_cr492_cn1697_ZT_reduced.json` |

---

## 5. Independent Negative Controls & Verifier Re-Execution

1. **Corrupted-Gate & Structural Negative Controls:**
   - Flipping `u_fresh[0][0]["value"]` in `object/schemes/3x3x7_m49_cr167_cn404_ZT_reduced.json` causes symbolic output entry mismatches over $\mathbb{Z}[A, B]$ and is immediately rejected (`AssertionError`).
   - Introducing a self-loop index (`index == cur_idx`) or a non-unit coefficient (`value = 2`) immediately raises `ValueError`.
2. **Author Verifier (`verify-it-yourself/verify.py`) Executed via `sh verify-it-yourself/run_checks.sh`:**
   - Running `sh verify-it-yourself/run_checks.sh` deterministically verifies all `4` schemes, baseline comparisons (`sota_rank`, `live_min_m`, `live_min_cr`, and `matmulcatalog_adds`), the corrupted-gate negative control, and the `400`-sample random greedy CSE null control on `3x3x7` ($m = 49, \text{cn} = 404$): `best_control = 304`, `median = 336`, `IQR = 13` vs claimed `cr = 167` (`-137` additions below `best_control`), printing:
     ```text
     VERIFIED: All 4 ternary SLP record schemes, baseline comparisons, negative control, and 400 null controls passed.
     PASS
     ```

pass: true
