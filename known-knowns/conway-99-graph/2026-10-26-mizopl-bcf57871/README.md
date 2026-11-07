# `conway-99-graph` (Track `p2`): Dual-Encoded Pure-RUP LRAT Re-Derivation of the Forced-Structure Reduction of `arXiv:2608.11211`

## What

Track p2 on conway-99-graph (srg(99, 14, 1, 2)): Dual-encoded pure-RUP LRAT (0 RAT lemmas) UNSAT certificates across two independent SAT cardinality encodings (Encoding A = Sinz 2005 Sequential Counter, Encoding B = Bailleux & Boufkhad 2003 Binary Tree Totalizer) re-deriving all 5 forced-structure reduction propositions (p2_1_inner_matching_k14, p2_2_outer_bijection_k14, p2_3_inner_outer_balance_k14, p2_4_outer_pair_cn_k14, and p2_5_srg9_uniqueness) of Thakkar & Severini (arXiv:2608.11211, Section 2.3), together with a positive SAT non-vacuity check on srg(9, 4, 1, 2) = K_3 box K_3 in both encodings (10 LRAT certificates: 2,862 core clauses and 983 RUP lemmas in Encoding A; 2,848 core clauses and 896 RUP lemmas in Encoding B; 5,710 core clauses and 1,879 RUP lemmas combined, 0 RAT lemmas).

---

## Check It Yourself

Run the standalone pure-Python checker from the root of this package:

```bash
sh verify-it-yourself/run_checks.sh
```

What `verify-it-yourself/verify.py` checks in $< 1$ second using only the Python 3 standard library:
1. **Positive Non-Vacuity Control on $\mathrm{srg}(9, 4, 1, 2) \cong K_3 \square K_3$ (`verify_positive_control_srg9`):** Builds the forced-structure CNF for $k = 4$ in both Encoding A (`66` variables, `200` clauses) and Encoding B (`42` variables, `146` clauses) without the blocking clause and verifies that the unique outer 4-cycle assignment propagates to a satisfying assignment of every clause.
2. **Track `p2` Forced-Structure Reduction (`p2_1` through `p2_5`, 10 Pure-RUP LRAT proofs):** Freshly generates all 10 full CNF formulas in Encoding A (`Sinz_2005_Sequential_Counter`) and Encoding B (`Bailleux_Boufkhad_2003_Binary_Tree_Totalizer`), checks that every clause of `object/proofs/p2_*_core.cnf` (`2,862` core clauses in Encoding A + `2,848` core clauses in Encoding B = `5,710` core clauses total) belongs to the freshly generated formula, verifies that `object/proofs/` contains exclusively the 20 Track `p2` files, and verifies all `1,879` LRAT proof steps (`983` in Encoding A + `896` in Encoding B, `0` RAT lemmas) via pure-Python Reverse Unit Propagation, printing `VERIFY: PASS`.

---

## Compared To

- **Aalok Thakkar and Simone Severini (`arXiv:2608.11211v2`, 18 Sep 2026), *A Forced-Structure Reduction and Verifiable Bounds for Conway's 99-Graph*, Section 2.3 (pp. 2–4):**
  - Formulated the forced-structure neighborhood reduction on $\mathrm{srg}(99, 14, 1, 2)$ around a fixed root vertex $0$ and validated it on $\mathrm{srg}(9, 4, 1, 2) \cong K_3 \square K_3$, without standalone SAT CNF encodings or DRAT/LRAT proof certificates.
  - This Track `p2` package provides standalone Pure-RUP LRAT UNSAT certificates (`1,879` RUP lemmas, `0` RAT lemmas) across both Encoding A (Sinz 2005 Sequential Counter) and Encoding B (Bailleux & Boufkhad 2003 Binary Tree Totalizer) for all 5 forced-structure propositions (`p2_1`–`p2_5`), plus the positive SAT non-vacuity check on $\mathrm{srg}(9, 4, 1, 2)$.

| Proposition ID | Statement in `arXiv:2608.11211` (§2.3) | Enc A Full Vars / Clauses | Enc A Core Clauses | Enc A RUP Lemmas | Enc B Full Vars / Clauses | Enc B Core Clauses | Enc B RUP Lemmas | RAT Lemmas |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `p2_1_inner_matching_k14` | $\Gamma_1(0) \cong 7 K_2$ (1-regular of order 14 under $\lambda=1$) | 273 / 716 | 4 | 1 | 259 / 688 | 4 | 1 | 0 |
| `p2_2_outer_bijection_k14` | Bijection $\Gamma_2(0) \leftrightarrow 84$ non-matched pairs $\{a,b\} \subset \Gamma_1(0)$ (Constraint 1) | 1,598 / 1,578 | 13 | 3 | 1,585 / 1,576 | 12 | 3 | 0 |
| `p2_3_inner_outer_balance_k14` | Inner-outer degree balance $\in \{1, 2\}$ (Constraint 4) | 548 / 2,733 | 2,487 | 836 | 522 / 2,717 | 2,483 | 780 | 0 |
| `p2_4_outer_pair_cn_k14` | Outer pair common-neighbor equation $E(u,v) + \mathrm{cn}_{\Gamma_2(0)}(u,v) = 2 - |P_u \cap P_v|$ (Constraints 2 & 3) | 91 / 407 | 345 | 142 | 87 / 407 | 342 | 111 | 0 |
| `p2_5_srg9_uniqueness` | Uniqueness of $\mathrm{srg}(9, 4, 1, 2) \cong K_3 \square K_3$ (UNSAT with blocking clause; SAT without) | 66 / 201 | 13 | 1 | 42 / 147 | 7 | 1 | 0 |
| **Track `p2` Total** | **5 Propositions (10 Pure-RUP LRAT Certificates)** | — | **2,862** | **983** | — | **2,848** | **896** | **0** |

---

## Complete Variable-to-Meaning Mapping and Re-Derivation of `p2_1` through `p2_5`

Every DIMACS variable ID in the 10 shipped core files (`object/proofs/p2_*_core.cnf`) and in the full generated formulas is mapped below to its exact mathematical meaning in $\mathrm{srg}(99, 14, 1, 2)$ and its corresponding statement in `arXiv:2608.11211` Section 2.3 (see `how-we-built-it/artifact.md` §1–§3 for the full clause schemas of `add_exact_sinz` and `add_exact_totalizer`).

### 1. `p2_1_inner_matching_k14` (`arXiv:2608.11211` §2.3, p. 2, paragraph 2)
- **Statement re-derived:** For root vertex $0$ with $\Gamma_1(0) = \{0, \dots, 13\}$ ($k = 14$), $\lambda = 1$ on edges $\{0, a\}$ forces every $a \in \Gamma_1(0)$ to have degree $\sum_{b \ne a} e_{a,b} = 1$ inside $\Gamma_1(0)$, so $\Gamma_1(0) \cong 7 K_2$. Negation: vertex $a = 0$ is adjacent to two distinct inner vertices $b = 1$ (`e_{0,1} = 1`) and $b = 2$ (`e_{0,2} = 1`).
- **Variable Map (`273` full vars in Enc A; `259` full vars in Enc B):**
  - `1..91`: Primary inner-edge variables $e_{a,b}$ for $0 \le a < b < 14$ in lexicographic order (`var 1` $= e_{0,1}$, `var 2` $= e_{0,2}$, ..., `var 13` $= e_{0,13}$).
  - `92..273` (Enc A): $14 \times 13 = 182$ Sinz prefix-sum registers $s_{i,0}^{(a)}$ for $a \in \{0..13\}, i \in \{0..12\}$, where **`var 92`** $= s_{0,0}^{(0)} \iff e_{0,1}$ is the first prefix-sum register on $L^{(0)} = [1, 2, \dots, 13]$.
  - `92..259` (Enc B): $14 \times 12 = 168$ Totalizer internal tree variables for $a \in \{0..13\}$. For $a = 0$, post-order bisection of $L^{(0)} = [1..13]$ splits $[1..13] \to [1..6] \to [1, 2, 3] \to \text{leaf } [1]$ and subtree $[2, 3] \to \text{leaf } [2]$ and $\text{leaf } [3]$. Thus the **first internal tree node allocated** (`var 92`) merges leaves `2` and `3`, so **`var 92`** $= t_{\{2,3\}, 1}^{(0)} \iff (e_{0,2} \vee e_{0,3})$.
- **Why the two `p2_1` cores have the same four clauses up to the sign of `var 92`, and what makes the encodings independent:**
  - The full generated formulas are structurally distinct (`273` vars / `716` clauses in Encoding A's linear register chain vs. `259` vars / `688` clauses in Encoding B's binary totalizer tree).
  - Refuting $e_{0,1} = 1$ (`c1: 1 0`) and $e_{0,2} = 1$ (`c2: 2 0`) under $\sum_{b=1}^{13} e_{0,b} = 1$ requires only the pairwise at-most-$1$ path between `var 1` and `var 2`, which in both encodings passes through `var 92`—but with **opposite meanings**:
    - In **Encoding A (Sinz)**: `var 92` is the prefix register $s_{0,0}^{(0)} \iff e_{0,1}$, emitting the forward implication `c3: 92 -1 0` ($e_{0,1} \implies s_{0,0}^{(0)}$) and the step-$1$ overflow clause `c4: -92 -2 0` ($\neg s_{0,0}^{(0)} \vee \neg e_{0,2}$).
    - In **Encoding B (Totalizer)**: `var 92` is the subtree bit $t_{\{2,3\},1}^{(0)} \iff (e_{0,2} \vee e_{0,3})$, emitting the upward subtree implication `c4: 92 -2 0` ($e_{0,2} \implies t_{\{2,3\},1}^{(0)}$) at node `[2, 3]` and the parent overflow clause `c3: -92 -1 0` ($\neg e_{0,1} \vee \neg t_{\{2,3\},1}^{(0)}$) at parent node `[1] + [2, 3]`.
  - Both 4-clause cores are refuted in 1 RUP step (`5 0 1 2 3 4 0`).

### 2. `p2_2_outer_bijection_k14` (`arXiv:2608.11211` §2.3, Constraint 1, p. 2)
- **Statement re-derived:** Each of the $M = 84$ outer vertices $u \in \Gamma_2(0)$ has $|P_u| = 2$ neighbors in $\Gamma_1(0)$ ($\mu = 2$). By $\lambda = 1$, $0$ outer vertices can have a matched inner edge $\{0, 1\} \in M_0$ as $P_u$; by $\mu = 2$, exactly $1$ outer vertex has any non-matched pair $\{0, 2\} \notin M_0$ as $P_u$.
- **Variable Map (`1,598` full vars in Enc A; `1,585` full vars in Enc B):**
  - `1..1176`: Incidence bits $b_{u,a} = 14u + a + 1$ ($u \in \{0..83\}, a \in \{0..13\}$). In the shipped cores: **`1`** $= b_{0,0}$, **`2`** $= b_{0,1}$, **`3`** $= b_{0,2}$, **`15`** $= b_{1,0}$, **`17`** $= b_{1,2}$.
  - `1177..1344` (Enc A) / `1177..1332` (Enc B): Cardinality counter variables for $\sum_{a=0}^{13} b_{u,a} = 2$ ($u = 0..5$).
  - `1345..1428` (Enc A) / `1333..1416` (Enc B): Conjunction bits $\text{and\_01}[u] \iff (b_{u,0} \wedge b_{u,1})$ for $u = 0..83$ (with $\sum_u \text{and\_01}[u] = 0$). In the shipped cores: **`1345`** (Enc A) / **`1333`** (Enc B) $= \text{and\_01}[0] \iff (b_{0,0} \wedge b_{0,1})$.
  - `1429..1512` (Enc A) / `1417..1500` (Enc B): Conjunction bits $\text{and\_02}[u] \iff (b_{u,0} \wedge b_{u,2})$ for $u = 0..83$. In the shipped cores: **`1429`** (Enc A) / **`1417`** (Enc B) $= \text{and\_02}[0] \iff (b_{0,0} \wedge b_{0,2})$; **`1430`** (Enc A) / **`1418`** (Enc B) $= \text{and\_02}[1] \iff (b_{1,0} \wedge b_{1,2})$.
  - `1513..1596` (Enc A) / `1501..1583` (Enc B): Cardinality counter variables for $\sum_{u=0}^{83} \text{and\_02}[u] = 1$. In the shipped Enc A core: **`1513`** $= s_{0,0} \iff \text{and\_02}[0]$ (`c12: 1513 -1429 0`, `c13: -1513 -1430 0`). In Enc B, post-order bisection of the 84 leaves pairs `1417` and `1418` at a leaf-merge node with $k = 1$, directly emitting `c12: -1418 -1417 0`.
  - **`1597, 1598`** (Enc A) / **`1584, 1585`** (Enc B): Disjunctive violation selectors $z_1$ ($u=0$ has matched pair $\{0,1\}$) and $z_2$ ($u=0$ and $u=1$ both have non-matched pair $\{0,2\}$). Refuted in `3` RUP steps (`13` core clauses in Enc A, `12` in Enc B).

### 3. `p2_3_inner_outer_balance_k14` (`arXiv:2608.11211` §2.3, Constraint 4, p. 3)
- **Statement re-derived:** Fix $u \in \Gamma_2(0)$ with $P_u = \{0, 2\}$ and inner matching $m(a) = a \oplus 1$ ($a \in \{0..13\}$). For each $a \in \{0..13\}$, $\mathbf{1}_{m(a) \in P_u} + \sum_{j=0}^{11} x_{a,j} = \text{full\_rhs}(a)$ (where $\text{full\_rhs}(a) = 1$ if $a \in \{0, 2\}$ else $2$, and $x_{a,j} = E(u, w_j)$ for the $12$ outer neighbors $w_0..w_{11}$ of $a$), forcing $\sum_{j=0}^{11} x_{a,j} = \text{target\_rhs}(a)$ ($1$ if $a \in \{0, 1, 2, 3\}$ else $2$).
- **Variable Map (`548` full vars / `2,487` core clauses / `836` RUP lemmas in Enc A; `522` full vars / `2,483` core clauses / `780` RUP lemmas in Enc B):**
  For each $a \in \{0..13\}$ sequentially:
  - $12$ outer-edge variables $x_{a,0..11}$, $1$ indicator $m_a = \mathbf{1}_{m(a) \in P_u}$, cardinality counter variables for $\text{add\_exact}([m_a, x_{a,0..11}], \text{full\_rhs}(a))$ ($13 \cdot \text{full\_rhs}(a)$ Sinz registers in Enc A; $12 \cdot \text{full\_rhs}(a)$ Totalizer tree variables in Enc B), and $2$ violation bits $v_{\text{low}}^{(a)}, v_{\text{high}}^{(a)}$:
    - $a = 0$: `edge_vars = 1..12`, $m_0 = 13$, `counter = 14..26` (Enc A) / `14..25` (Enc B), $v_{\text{low}}, v_{\text{high}} = 27, 28$ (Enc A) / `26, 27` (Enc B).
    - $a = 1$: `edge_vars = 29..40` (Enc A) / `28..39` (Enc B), $m_1 = 41$ / `40`, `counter = 42..67` / `41..64`, $v_{\text{low}}, v_{\text{high}} = 68, 69$ / `65, 66`.
    - $a = 2$: `edge_vars = 70..81` (Enc A) / `67..78` (Enc B), $m_2 = 82$ / `79`, `counter = 83..95` / `80..91`, $v_{\text{low}}, v_{\text{high}} = 96, 97$ / `92, 93`.
    - $a = 3$: `edge_vars = 98..109` (Enc A) / `94..105` (Enc B), $m_3 = 110$ / `106`, `counter = 111..136` / `107..130`, $v_{\text{low}}, v_{\text{high}} = 137, 138$ / `131, 132`.
    - $a \in \{4..13\}$: block $a$ starts at base variable $B_A(a) = 139 + 41(a-4)$ in Encoding A (`edge_vars` $= B_A..B_A+11$, $m_a = B_A+12$, `counter` $= B_A+13..B_A+38$, $v_{\text{low}}, v_{\text{high}} = B_A+39, B_A+40$) and at $B_B(a) = 133 + 39(a-4)$ in Encoding B (`edge_vars` $= B_B..B_B+11$, $m_a = B_B+12$, `counter` $= B_B+13..B_B+36$, $v_{\text{low}}, v_{\text{high}} = B_B+37, B_B+38$).

### 4. `p2_4_outer_pair_cn_k14` (`arXiv:2608.11211` §2.3, Constraints 2 & 3, p. 3)
- **Statement re-derived:** For distinct $u, v \in \Gamma_2(0)$ with $s = |P_u \cap P_v| \in \{0, 1\}$, $s + e_{uv} + \sum_{i=0}^{11} c_i = 2$, forcing $\sum_{i=0}^{11} c_i = (2 - s) - e_{uv}$ (Constraint 2 when $e_{uv} = 1$; Constraint 3 when $e_{uv} = 0$).
- **Variable Map (`91` full vars / `345` core clauses / `142` RUP lemmas in Enc A; `87` full vars / `342` core clauses / `111` RUP lemmas in Enc B):**
  - **Block $s = 0$:** `1` $= e_{uv}^{(0)}$, `2` $= s_{\text{var}}^{(0)}$ (unit `-2 0`), `3..14` $= c_{0..11}^{(0)}$, cardinality counter variables `15..42` ($28$ Sinz registers in Enc A) / `15..40` ($26$ Totalizer vars in Enc B), violation bits for $e_{uv}^{(0)}=1$: `43, 44` (Enc A) / `41, 42` (Enc B), and for $e_{uv}^{(0)}=0$: `45, 46` (Enc A) / `43, 44` (Enc B).
  - **Block $s = 1$:** `47` (Enc A) / `45` (Enc B) $= e_{uv}^{(1)}$, `48` / `46` $= s_{\text{var}}^{(1)}$ (unit `+48 0` / `+46 0`), `49..60` / `47..58` $= c_{0..11}^{(1)}$, cardinality counter variables `61..88` (Enc A) / `59..84` (Enc B), violation bit for $e_{uv}^{(1)}=1$ ($\sum c_i > 0$): `89` (Enc A) / `85` (Enc B), and violation bits for $e_{uv}^{(1)}=0$ ($\sum c_i \ne 1$): `90, 91` (Enc A) / `86, 87` (Enc B).

### 5. `p2_5_srg9_uniqueness` (`arXiv:2608.11211` §2.3, p. 4, Validation on $\mathrm{srg}(9, 4, 1, 2)$)
- **Statement re-derived:** On $\mathrm{srg}(9, 4, 1, 2) \cong K_3 \square K_3$ ($k = 4, M = 4$ outer vertices $p_0 = \{0_L, 1_L\}, p_1 = \{0_L, 1_R\}, p_2 = \{0_R, 1_L\}, p_3 = \{0_R, 1_R\}$), Constraints 1–4 uniquely force the outer 4-cycle $e_{0,1} = e_{0,2} = e_{1,3} = e_{2,3} = 1, e_{0,3} = e_{1,2} = 0$.
- **Variable Map of the Shipped Cores (`13` core clauses in Enc A; `7` core clauses in Enc B; `1` RUP lemma each):**
  - **`1..6` (Primary outer edges in both encodings):** `1` $= E(p_0, p_1)$, `2` $= E(p_0, p_2)$, `3` $= E(p_0, p_3)$ (diagonal), `4` $= E(p_1, p_2)$ (diagonal), `5` $= E(p_1, p_3)$, `6` $= E(p_2, p_3)$.
  - **Additional Sinz register variables in `p2_5_srg9_uniqueness_encA_core.cnf` (`7, 10, 11, 16, 18, 21`):**
    - `7` $= s_{0,0}$ for $(p_0, 0_L)$ on $L=[1]$ (`c1: 7 0`, `c5: 1 -7 0`);
    - `10` $= s_{0,0}$ for $(p_0, 1_L)$ on $L=[2]$ (`c2: 10 0`, `c6: 2 -10 0`);
    - `11` $= s_{0,0}$ for $(p_0, 1_R)$ on $L=[1, 3]$ (`c9: 11 -1 0`, `c11: -3 -11 0`);
    - `16` $= s_{0,0}$ for $(p_1, 1_L)$ on $L=[1, 4]$ (`c10: 16 -1 0`, `c12: -4 -16 0`);
    - `18` $= s_{0,0}$ for $(p_1, 1_R)$ on $L=[5]$ (`c3: 18 0`, `c7: 5 -18 0`);
    - `21` $= s_{0,0}$ for $(p_2, 0_R)$ on $L=[6]$ (`c4: 21 0`, `c8: 6 -21 0`).
    (In Encoding B, 1-leaf trees return the leaf directly and 2-leaf trees emit binary overflow clauses `-3 -1 0` and `-4 -1 0` directly, so the 7-clause Encoding B core uses only variables `1..6`.)

---

## Not Claimed

- **Full Solution of Conway's 99-Graph Problem:** We do **not** claim a `CONFIRMED_SOLUTION` (either constructing an $\mathrm{srg}(99, 14, 1, 2)$ or certifying that no such graph exists without symmetry assumptions).
- **Automorphism Exclusion Claims:** This package contains and claims **only Track `p2`** (`p2_1`–`p2_5`, re-deriving the published Section 2.3 forced-structure reductions of `arXiv:2608.11211v2` as dual-encoded Pure-RUP LRAT certificates).

---

## Credits

- **Contributor:** `@mizopl`
- **Target:** `conway-99-graph` (`known-knowns`, Track `p2`)
