# Prior Published Baselines & Literature Comparison (`conway-99-graph`)

## 1. Primary Literature References

1. **Aalok Thakkar and Simone Severini (18 Sep 2026):**
   - **Title:** *A Forced-Structure Reduction and Verifiable Bounds for Conway's 99-Graph*
   - **Reference:** `arXiv:2608.11211v2` (`https://arxiv.org/abs/2608.11211`)
   - **Reported Results:**
     - Formulated the 4-part forced-structure neighborhood reduction on $\mathrm{srg}(99, 14, 1, 2)$ (inner matching $7 K_2$, outer bijection of 84 non-neighbors onto non-matched pairs $\{u,v\} \subset \Gamma_1(0)$, inner-outer degree balance $\in \{1,2\}$, and outer pair common-neighbor equation $e_{pq} + \sum_r e_{pr} e_{qr} = 2 - |P_p \cap P_q|$), and validated it on the sibling graph $\mathrm{srg}(9, 4, 1, 2) \cong K_3 \square K_3$.
     - Excluded circulant graphs ($\mathbb{Z}/99$), Cayley graphs over $\mathbb{Z}_3 \times \mathbb{Z}_3 \times \mathbb{Z}_{11}$, and block CP-SAT over $\mathbb{Z}/11, \mathbb{Z}/9$ (Table 1).
     - Tested single-fixed-point $\mathbb{Z}_7$ (`p7_fix1`, 1 fixed vertex and 14 orbits of size 7) via CP-SAT on 14 cores for **48 hours** (`172,800` seconds), returning **`UNKNOWN` (timeout)**.
     - Tested fixed-point-free $\mathbb{Z}_3$ (33 orbits of size 3) for 1800 seconds, returning **`UNKNOWN`**.
     - Did not publish standalone DRAT/LRAT proof certificates for the forced-structure propositions (`p2`) or prime-order automorphism cases (`p1`).

2. **Patrick G. Cesarz and Andrew J. Woldar (6 Aug 2023):**
   - **Title:** *On the automorphism group of a putative Conway 99-graph*
   - **Reference:** `arXiv:2308.02978v1` (`https://arxiv.org/abs/2308.02978`)
   - **Reported Results & Cited Refinements:**
     - Cites **A. A. Makhnev and I. M. Minakova (2004, *Discrete Math. Appl.* 14(2):201–210, Theorem 2.7)** and **M. Behbahani and C. Lam (2011, *Discrete Math.* 311:897–906)**:
       - Makhnev & Minakova (2004) showed $|\mathrm{Aut}(\Gamma)| \mid 2 \cdot 3^3 \cdot 7 \cdot 11$ (excluding $p = 5$ and $p = 13$), showed that for $p = 3$ any order-3 automorphism has $|\mathrm{Fix}(g)| \in \{0, 3\}$ (excluding $|\mathrm{Fix}(g)| = 33$, `p3_t1_fix33`), and analyzed fixed-point subgraphs of involutions ($p = 2$), showing that an involution with more than one fixed vertex has $|\mathrm{Fix}(g)| = 9$ inducing a star of 4 triangles (`p2_a0_b5_c2_fix9`, profile `(0,5,2)`), while leaving $p = 2$ open.
       - Behbahani & Lam (2011) excluded $p = 11$, reducing $|\mathrm{Aut}(\Gamma)|$ to a divisor of $2 \cdot 3^3 \cdot 7 = 378$.
     - Proves no order-14 automorphism exists (Theorem 3.11) and $14 \nmid |\mathrm{Aut}(\Gamma)|$ (Proposition 4.1).
     - Proves Corollary 4.4(a): if $2 \mid |\mathrm{Aut}(\Gamma)|$, then $|\mathrm{Aut}(\Gamma)| \mid 6$ ($\mathrm{Aut}(\Gamma) \in \{\mathbb{Z}_2, \mathbb{Z}_6, S_3\}$), leaving $p = 2$ ($\mathbb{Z}_2$) **open**.
     - Proves Lemma 2.2 & Corollary 4.4(b): if $7 \mid |\mathrm{Aut}(\Gamma)|$, any order-7 automorphism fixes a unique vertex and has 14 orbits of size 7 (`p7_fix1`), and $\mathrm{Aut}(\Gamma) \cong \mathbb{Z}_7$ or $\mathrm{Frob}(21)$.
     - Excludes $\mathrm{Frob}(21) = \mathbb{Z}_7 \rtimes \mathbb{Z}_3$ (`frob21_z7_z3`) in Section 6 via an uncertified GAP/GRAPE search (`2,916` iterations), leaving standalone $\mathbb{Z}_7$ (`p7_fix1`) **open**.

---

## 2. Track `p2` Comparison: Forced-Structure Reduction Propositions (`p2_1` through `p2_5`)

| Proposition ID | Statement in `arXiv:2608.11211` (§2.3) | `arXiv:2608.11211` Certificate Status | Dual-Encoded Pure-RUP LRAT Status (`object/certificate.json`) |
| :--- | :--- | :--- | :--- |
| `p2_1_inner_matching_k14` | $\Gamma_1(0) \cong 7 K_2$ (1-regular of order 14) | Prose proof only (no SAT/LRAT certificate) | **Certified UNSAT** in Enc A (23 core clauses, 1 RUP step) & Enc B (21 core clauses, 1 RUP step) |
| `p2_2_outer_bijection_k14` | Bijection $\Gamma_2(0) \leftrightarrow$ 84 non-matched pairs $\{u,v\} \subset \Gamma_1(0)$ | Prose proof only (no SAT/LRAT certificate) | **Certified UNSAT** in Enc A (12 core clauses, 2 RUP steps) & Enc B (12 core clauses, 2 RUP steps) |
| `p2_3_inner_outer_balance_k14` | Inner-outer degree balance $\in \{1, 2\}$ | Prose proof only (no SAT/LRAT certificate) | **Certified UNSAT** in Enc A (16 core clauses, 4 RUP steps) & Enc B (17 core clauses, 4 RUP steps) |
| `p2_4_outer_pair_cn_k14` | Outer pair common-neighbor equation $e_{pq} + \sum_r e_{pr} e_{qr} = 2 - |P_p \cap P_q|$ | Prose proof only (no SAT/LRAT certificate) | **Certified UNSAT** in Enc A (355 core clauses, 4 RUP steps) & Enc B (491 core clauses, 4 RUP steps) |
| `p2_5_srg9_uniqueness` | Forced-structure uniqueness of $\mathrm{srg}(9, 4, 1, 2) \cong K_3 \square K_3$ | CP-SAT validation script (no LRAT certificate) | **Certified SAT** (without blocking clause) & **Certified UNSAT** (with blocking clause) in Enc A (75 core clauses, 9 RUP steps) & Enc B (76 core clauses, 7 RUP steps) |

---

## 3. Track `p1` Comparison: All 22 Automorphism Cases vs. `arXiv:2308.02978`, Refinements, and `arXiv:2608.11211`

For each of the 22 automorphism cases in `object/certificate.json`, the table below states whether `arXiv:2308.02978`, its cited background/refinements (Makhnev & Minakova 2004; Behbahani & Lam 2011), or `arXiv:2608.11211` already exclude it, and whether it counts as an open `p1` exclusion:

| Case ID | Prime / Group | Cycle Structure $(|\mathrm{Fix}(g)|, \text{cycles})$ | Status in `arXiv:2308.02978` (2023) | Status in Refinements / Cited Background (Makhnev–Minakova 2004, Behbahani–Lam 2011) | Status in `arXiv:2608.11211` (2026) | Counts for `p1`? | Dual-Encoded Pure-RUP LRAT (Enc A / Enc B RUP Steps) |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: | :---: |
| `p7_fix1` | $p = 7$ ($\mathbb{Z}_7$) | $1$ fixed, $14 \times 7$-cycles | **OPEN** (Cor. 4.4(b)) | **OPEN** | **OPEN** (`UNKNOWN` after 48h on 14 cores, §2.4) | **YES (Open in all prior work)** | **Certified UNSAT** (`56,515` / `23,551`) |
| `p5_t1_fix9` | $p = 5$ ($\mathbb{Z}_5$) | $9$ fixed, $18 \times 5$-cycles | Cited as excluded in §1 | **Already excluded** (Makhnev–Minakova 2004, Thm. 2.7) | Not re-tested | **No** (re-derivation) | **Certified UNSAT** (`3,667` / `3,130`) |
| `p3_t1_fix33` | $p = 3$ ($\mathbb{Z}_3$) | $33$ fixed, $22 \times 3$-cycles | Cited as excluded in §1 | **Already excluded** (Makhnev–Minakova 2004: $|\mathrm{Fix}(g)| \in \{0,3\}$) | Not re-tested | **No** (re-derivation) | **Certified UNSAT** (`17` / `20`) |
| `frob21_z7_z3` | $\mathrm{Frob}(21) = \mathbb{Z}_7 \rtimes \mathbb{Z}_3$ | $1$ fixed, $4 \times 7 + 3 \times 21$ | **Already excluded** (§6, uncertified GAP search, 2,916 iters) | Open prior to 2023 | Not re-tested | **No** (re-derivation) | **Certified UNSAT** (`25` / `16`) |
| `p2_a0_b1_c6_fix73` | $p = 2$, $(0,1,6)$ | $73$ fixed, $13 \times 2$-cycles | **OPEN** ($G \cong \mathbb{Z}_2$ open in Cor. 4.4(a)) | Excluded analytically by fixed-subgraph bound ($|\mathrm{Fix}(g)| \in \{1,9\}$) | **OPEN** (not tested) | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) | **Certified UNSAT** (`11` / `12`) |
| `p2_a0_b2_c5_fix51` | $p = 2$, $(0,2,5)$ | $51$ fixed, $24 \times 2$-cycles | **OPEN** (Cor. 4.4(a)) | Excluded analytically in MM04 ($|\mathrm{Fix}(g)| \in \{1,9\}$) | **OPEN** (not tested) | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) | **Certified UNSAT** (`11` / `12`) |
| `p2_a0_b3_c4_fix33` | $p = 2$, $(0,3,4)$ | $33$ fixed, $33 \times 2$-cycles | **OPEN** (Cor. 4.4(a)) | Excluded analytically in MM04 ($|\mathrm{Fix}(g)| \in \{1,9\}$) | **OPEN** (not tested) | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) | **Certified UNSAT** (`112` / `109`) |
| `p2_a0_b4_c3_fix19` | $p = 2$, $(0,4,3)$ | $19$ fixed, $40 \times 2$-cycles | **OPEN** (Cor. 4.4(a)) | Excluded analytically in MM04 ($|\mathrm{Fix}(g)| \in \{1,9\}$) | **OPEN** (not tested) | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) | **Certified UNSAT** (`88` / `90`) |
| `p2_a0_b5_c2_fix9` | $p = 2$, $(0,5,2)$ | $9$ fixed, $45 \times 2$-cycles | **OPEN** (Cor. 4.4(a)) | **OPEN** (survives MM04 fixed-subgraph star $K_{1,3}$ of 4 triangles) | **OPEN** (not tested) | **YES (Open in all prior work)** | **Certified UNSAT** (`184` / `200`) |
| `p2_a0_b6_c1_fix3` | $p = 2$, $(0,6,1)$ | $3$ fixed, $48 \times 2$-cycles | **OPEN** (Cor. 4.4(a)) | Excluded analytically in MM04 ($|\mathrm{Fix}(g)| \in \{1,9\}$) | **OPEN** (not tested) | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) | **Certified UNSAT** (`1` / `1`) |
| `p2_a1_b0_c5_fix53` | $p = 2$, $(1,0,5)$ | $53$ fixed, $23 \times 2$-cycles | **OPEN** (Cor. 4.4(a)) | Excluded analytically in MM04 ($|\mathrm{Fix}(g)| \in \{1,9\}$) | **OPEN** (not tested) | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) | **Certified UNSAT** (`164` / `165`) |
| `p2_a1_b1_c4_fix35` | $p = 2$, $(1,1,4)$ | $35$ fixed, $32 \times 2$-cycles | **OPEN** (Cor. 4.4(a)) | Excluded analytically in MM04 ($|\mathrm{Fix}(g)| \in \{1,9\}$) | **OPEN** (not tested) | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) | **Certified UNSAT** (`16` / `25`) |
| `p2_a1_b2_c3_fix21` | $p = 2$, $(1,2,3)$ | $21$ fixed, $39 \times 2$-cycles | **OPEN** (Cor. 4.4(a)) | Excluded analytically in MM04 ($|\mathrm{Fix}(g)| \in \{1,9\}$) | **OPEN** (not tested) | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) | **Certified UNSAT** (`150` / `150`) |
| `p2_a1_b3_c2_fix11` | $p = 2$, $(1,3,2)$ | $11$ fixed, $44 \times 2$-cycles | **OPEN** (Cor. 4.4(a)) | Excluded analytically in MM04 ($|\mathrm{Fix}(g)| \in \{1,9\}$) | **OPEN** (not tested) | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) | **Certified UNSAT** (`65` / `62`) |
| `p2_a1_b4_c1_fix5` | $p = 2$, $(1,4,1)$ | $5$ fixed, $47 \times 2$-cycles | **OPEN** (Cor. 4.4(a)) | Excluded analytically in MM04 ($|\mathrm{Fix}(g)| \in \{1,9\}$) | **OPEN** (not tested) | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) | **Certified UNSAT** (`127` / `126`) |
| `p2_a1_b5_c0_fix3` | $p = 2$, $(1,5,0)$ | $3$ fixed, $48 \times 2$-cycles | **OPEN** (Cor. 4.4(a)) | Excluded analytically in MM04 ($|\mathrm{Fix}(g)| \in \{1,9\}$) | **OPEN** (not tested) | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) | **Certified UNSAT** (`1,073` / `996`) |
| `p2_a2_b0_c3_fix23` | $p = 2$, $(2,0,3)$ | $23$ fixed, $38 \times 2$-cycles | **OPEN** (Cor. 4.4(a)) | Excluded analytically in MM04 ($|\mathrm{Fix}(g)| \in \{1,9\}$) | **OPEN** (not tested) | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) | **Certified UNSAT** (`182` / `216`) |
| `p2_a2_b1_c2_fix13` | $p = 2$, $(2,1,2)$ | $13$ fixed, $43 \times 2$-cycles | **OPEN** (Cor. 4.4(a)) | Excluded analytically in MM04 ($|\mathrm{Fix}(g)| \in \{1,9\}$) | **OPEN** (not tested) | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) | **Certified UNSAT** (`202` / `200`) |
| `p2_a2_b2_c1_fix7` | $p = 2$, $(2,2,1)$ | $7$ fixed, $46 \times 2$-cycles | **OPEN** (Cor. 4.4(a)) | Excluded analytically in MM04 ($|\mathrm{Fix}(g)| \in \{1,9\}$) | **OPEN** (not tested) | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) | **Certified UNSAT** (`39` / `39`) |
| `p2_a2_b3_c0_fix5` | $p = 2$, $(2,3,0)$ | $5$ fixed, $47 \times 2$-cycles | **OPEN** (Cor. 4.4(a)) | Excluded analytically in MM04 ($|\mathrm{Fix}(g)| \in \{1,9\}$) | **OPEN** (not tested) | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) | **Certified UNSAT** (`40` / `40`) |
| `p2_a3_b0_c1_fix9` | $p = 2$, $(3,0,1)$ | $9$ fixed, $45 \times 2$-cycles | **OPEN** (Cor. 4.4(a)) | Excluded analytically in MM04 ($c=2$ required for $|\mathrm{Fix}(g)|=9$) | **OPEN** (not tested) | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) | **Certified UNSAT** (`1` / `1`) |
| `p2_a3_b1_c0_fix7` | $p = 2$, $(3,1,0)$ | $7$ fixed, $46 \times 2$-cycles | **OPEN** (Cor. 4.4(a)) | Excluded analytically in MM04 ($|\mathrm{Fix}(g)| \in \{1,9\}$) | **OPEN** (not tested) | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) | **Certified UNSAT** (`185` / `185`) |

**Summary of Track `p1` Literature Status:**
- **Strictly open in all prior literature (`arXiv:2308.02978`, Makhnev–Minakova 2004, Behbahani–Lam 2011, and `arXiv:2608.11211`):**
  1. `p7_fix1` ($p = 7$, $1$ fixed vertex, $14 \times 7$-cycles) — left open in `arXiv:2308.02978` Cor. 4.4(b) and timed out (`UNKNOWN` after 48 hours on 14 cores) in `arXiv:2608.11211` §2.4.
  2. `p2_a0_b5_c2_fix9` ($p = 2$, profile `(0,5,2)`, $9$ fixed vertices inducing the 4-triangle star, $45 \times 2$-cycles) — left open in Makhnev–Minakova (2004), `arXiv:2308.02978` Cor. 4.4(a), and `arXiv:2608.11211`.
- **Open in `arXiv:2308.02978` (Cor. 4.4(a)) and `arXiv:2608.11211`, though excluded analytically by fixed-point subgraph counting in Makhnev & Minakova (2004):**
  - The remaining 17 certified $p = 2$ involution profiles: `(0,1,6)`, `(0,2,5)`, `(0,3,4)`, `(0,4,3)`, `(0,6,1)`, `(1,0,5)`, `(1,1,4)`, `(1,2,3)`, `(1,3,2)`, `(1,4,1)`, `(1,5,0)`, `(2,0,3)`, `(2,1,2)`, `(2,2,1)`, `(2,3,0)`, `(3,0,1)`, and `(3,1,0)`. (The 19th profile `(0,7,0)` with $|\mathrm{Fix}(g)| = 1$ remains open.)
- **Already excluded in `arXiv:2308.02978` or Makhnev & Minakova (2004) (included only as machine-checked LRAT re-derivations, not counted as new `p1` exclusions):**
  - `frob21_z7_z3` (excluded in `arXiv:2308.02978` §6 via GAP), `p5_t1_fix9` (excluded in Makhnev–Minakova 2004 Thm. 2.7), and `p3_t1_fix33` (excluded in Makhnev–Minakova 2004).
