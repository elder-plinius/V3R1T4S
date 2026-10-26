# CRITERION Panel Report — 7 Ternary (`ZT`) & Integer (`Z`) Fast Matrix Multiplication Schemes

role: CRITERION
context: Antigravity fresh subagent (invoke_subagent, role CRITERION)
target: fmm-ternary-integer-ring-upgrade
formats: 6x12x14, 9x10x13, 9x10x16, 10x15x16, 11x15x16, 12x13x16
claimed_ranks: 654 (ZT), 763 (ZT), 920 (ZT), 1484 (ZT), 1629 (ZT), 1546 (ZT), 1541 (Z)
confirmed_scope: Seven explicit bilinear fast matrix multiplication schemes (6 in ZT = {-1, 0, 1} and 1 in Z) verified in exact 64-bit integer arithmetic across all 29,648,196 Brent equations over Z with 0 mismatches: object/6x12x14_m654_ZT.json (rank 654 vs live ZT 666, -12, sha256 5ab48b6b88fd1a7b9fbe8c81670522bd45f290e580be8a4443751e208f2f2bc4), object/9x10x13_m763_ZT.json (rank 763 vs live ZT 771, -8, sha256 a351d9eef1a62ff9ab7a300e67928a880200e9fcb4ba7f3accffc900e99c1923), object/9x10x16_m920_ZT.json (rank 920 vs live ZT 924, -4, sha256 42ad6efd9f8b6aab2320058835d85c565300f616d007b57535bf1968c0cb0076), object/10x15x16_m1484_ZT.json (rank 1484 vs live ZT 1488, -4, sha256 02199a88ebd24b1457c5cae7a5a2dcb895aa396ada9e5daaf0ea1cc4846d09d3), object/11x15x16_m1629_ZT.json (rank 1629 vs live ZT 1641, -12, sha256 0d2eb6e651f61c7c9fa5d137eb4813f37f287016eaa91e95deae53107016b288), object/12x13x16_m1546_ZT.json (rank 1546 vs live ZT 1548, -2, sha256 b639c891628cd5e5042311d19adfa2c29eff95d6c0b1077466c36ce3204e796a), and object/12x13x16_m1541_Z.json (rank 1541 vs live Z 1544, -3, sha256 911599680fd3bbe0558dbf7fe5e0886deb863c4244915812d28404156660f780).

## 1. Clause-by-Clause Audit Against Verbatim Bank Criterion

- **Format Bounds & Ring Preconditions:** All 6 formats (`6x12x14`, `9x10x13`, `9x10x16`, `10x15x16`, `11x15x16`, `12x13x16`) satisfy `max(n, m, p) <= 16` and `sorted(n, m, p) != (4, 4, 4)`. All 6 `ZT` schemes have `max_abs = 1` (`0` non-ternary coefficients), and `12x13x16_m1541_Z.json` has `max_abs = 2` over $\mathbb{Z}$. All 7 schemes have `zero_terms = 0` and `distinct_triples = m`.
- **Clause (1) (Strict Improvement over Live Table):**
  - `6x12x14` (`ZT`): `654 < 666` (`-12`)
  - `9x10x13` (`ZT`): `763 < 771` (`-8`)
  - `9x10x16` (`ZT`): `920 < 924` (`-4`)
  - `10x15x16` (`ZT`): `1,484 < 1,488` (`-4`)
  - `11x15x16` (`ZT`): `1,629 < 1,632 < 1,641` (`-12` vs `README.md`, `-3` vs `status.json`)
  - `12x13x16` (`ZT`): `1,546 < 1,548` (`-2`)
  - `12x13x16` (`Z`): `1,541 < 1,544` (`-3`)
  - **Verdict on Clause (1):** SATISFIED.
- **Clause (2) (Within Target Scope, `>= Q` Rank):**
  - `654 >= 645`, `763 >= 758`, `920 >= 916`, `1,484 >= 1,482`, `1,629 >= 1,605`, `1,546 >= 1,509`, `1,541 >= 1,509`.
  - **Verdict on Clause (2):** SATISFIED.
- **Clause (3) (Absence from Live Repositories):** Verified against live `dronperminov/FastMatrixMultiplication` (`schemes/status.json` sha256 `8f129ee5cf9683c769de46143323219eeebbc7fed24b201cc02a22f4a851cf1c`) and `MerlijnW70/fmm-schemes`.
  - **Verdict on Clause (3):** SATISFIED.
- **Clause (4) (Exact Integer Brent Equations Over $\mathbb{Z}$):** All `29,648,196` equations (`1,016,064 + 1,368,900 + 2,073,600 + 5,760,000 + 6,969,600 + 6,230,016 + 6,230,016`) verified over $\mathbb{Z}$ in exact 64-bit integer arithmetic with `0` mismatches.
  - **Verdict on Clause (4):** SATISFIED.

pass: true
