# `conway-99-graph` (Track `p2`): Dual-Encoded Pure-RUP LRAT Re-Derivation of the Forced-Structure Reduction of `arXiv:2608.11211`

## What

Track p2 on conway-99-graph (srg(99, 14, 1, 2)): Dual-encoded pure-RUP LRAT (0 RAT lemmas) UNSAT certificates across two independent SAT cardinality encodings (Encoding A = Sinz 2005 Sequential Counter, Encoding B = Bailleux & Boufkhad 2003 Binary Tree Totalizer) re-deriving all 5 forced-structure reduction propositions (p2_1_inner_matching_k14, p2_2_outer_bijection_k14, p2_3_inner_outer_balance_k14, p2_4_outer_pair_cn_k14, and p2_5_srg9_uniqueness) of Thakkar & Severini (arXiv:2608.11211), together with a positive SAT non-vacuity check on srg(9, 4, 1, 2) = K_3 box K_3 in both encodings (10 LRAT certificates, 38 RUP steps, 0 RAT lemmas, verified alongside the full 27-theorem / 54-certificate suite by verify-it-yourself/verify.py).

---

## Check It Yourself

Run the standalone pure-Python checker from the root of this package:

```bash
sh verify-it-yourself/run_checks.sh
```

What `verify-it-yourself/verify.py` checks in ~20 seconds using only the Python 3 standard library:
1. **Positive Non-Vacuity Control on $\mathrm{srg}(9, 4, 1, 2) \cong K_3 \square K_3$ (`verify_positive_control_srg9`):** Builds the forced-structure CNF for $k = 4$ in both Encoding A and Encoding B without the blocking clause and verifies that the unique outer 4-cycle assignment propagates to a satisfying assignment of every clause.
2. **Track `p2` Forced-Structure Reduction (`p2_1` through `p2_5`, 10 Pure-RUP LRAT proofs):** Freshly generates the full CNF formulas in Encoding A (`Sinz_2005_Sequential_Counter`) and Encoding B (`Bailleux_Boufkhad_2003_Binary_Tree_Totalizer`), checks that every clause of `object/proofs/p2_*_core.cnf` belongs to the freshly generated formula, and verifies every LRAT proof step via pure-Python Reverse Unit Propagation (`0` RAT lemmas).
3. **Full Suite Integrity Check:** Also verifies all 22 Track `p1` certificates stored in `object/` (54 total UNSAT proofs across 27 theorems, 92,259 RUP lemmas, `0` RAT lemmas) and prints `VERIFY: PASS`.

---

## Compared To

- **Aalok Thakkar and Simone Severini (`arXiv:2608.11211v2`, 18 Sep 2026), *A Forced-Structure Reduction and Verifiable Bounds for Conway's 99-Graph*:**
  - Formulated the 4-part forced-structure neighborhood reduction on $\mathrm{srg}(99, 14, 1, 2)$ (§2.3) and validated it on $\mathrm{srg}(9, 4, 1, 2) \cong K_3 \square K_3$, without standalone DRAT/LRAT certificates across two independent SAT cardinality encodings.
  - This Track `p2` package provides standalone Pure-RUP LRAT UNSAT certificates (`0` RAT lemmas) across both Encoding A (Sinz 2005 Sequential Counter) and Encoding B (Bailleux & Boufkhad 2003 Binary Tree Totalizer) for all 5 forced-structure propositions (`p2_1`–`p2_5`), plus the positive SAT non-vacuity check on $\mathrm{srg}(9, 4, 1, 2)$.

| Proposition ID | Statement in `arXiv:2608.11211` (§2.3) | Enc A Full Vars / Clauses | Enc A Core Clauses | Enc A RUP Steps | Enc B Full Vars / Clauses | Enc B Core Clauses | Enc B RUP Steps | RAT Lemmas |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `p2_1_inner_matching_k14` | $\Gamma_1(0) \cong 7 K_2$ (1-regular of order 14) | 469 / 1,107 | 23 | 1 | 595 / 1,457 | 21 | 1 | 0 |
| `p2_2_outer_bijection_k14` | Bijection $\Gamma_2(0) \leftrightarrow 84$ non-matched pairs $\{u,v\} \subset \Gamma_1(0)$ | 4,005 / 9,532 | 12 | 2 | 5,264 / 13,221 | 12 | 2 | 0 |
| `p2_3_inner_outer_balance_k14` | Inner-outer degree balance $\in \{1, 2\}$ | 22 / 49 | 16 | 4 | 31 / 66 | 17 | 4 | 0 |
| `p2_4_outer_pair_cn_k14` | Outer pair common-neighbor equation $e_{pq} + \sum_r e_{pr} e_{qr} = 2 - |P_p \cap P_q|$ | 674 / 1,622 | 355 | 4 | 839 / 2,348 | 491 | 4 | 0 |
| `p2_5_srg9_uniqueness` | Uniqueness of $\mathrm{srg}(9, 4, 1, 2) \cong K_3 \square K_3$ (UNSAT with blocking clause; SAT without) | 124 / 298 | 75 | 9 | 168 / 442 | 76 | 7 | 0 |
| **Track `p2` Total** | **5 Propositions (10 Pure-RUP LRAT Certificates)** | — | **481** | **20** | — | **617** | **18** | **0** |

---

## Complete List of Encoding Constraints Beyond `srg(99, 14, 1, 2)` and the Stated Automorphism, with Derivations

For complete transparency across the shared `verify-it-yourself/verify.py` verifier and `object/` archive, every constraint added by `verify.py` beyond the raw $\mathrm{srg}(99, 14, 1, 2)$ conditions (`p2_3` inner-outer balance and `p2_4` outer-pair common neighbors) and the stated automorphism `perms` is documented below with its derivation and exact line numbers in `verify.py` (see also `how-we-built-it/artifact.md` §4 for expanded derivations):

1. **`p7_fix1` (`r4_mode = "p7_orbit_top6"`, `build_p7_fix1_orbit_cnf` in `verify.py` lines 395–565):**
   - Encodes the top $6 \times 12$ rows $i \in I_{LL} \cup I_{RR} = \{0..5\}$ and columns $j \in \{0..11\}$ of the $12 \times 12$ outer orbit-valency matrix $B = (b_{ij})$ ($b_{ij} = u_0 + u_1 + u_2 \in \{0, 1, 2, 3\}$ for $i \ne j$, $b_{ji} = b_{ij}$ for $0 \le i < j < 6$).
   - **Off-diagonal bound $b_{ij} \le 3$ (lines 424–433):** Lemma 4.6 of `arXiv:2308.02978` ($b_{ij} \ge 4$ on a $7$-cycle violates $\lambda = 1$ or $\mu = 2$).
   - **Trace condition $b_{ii} = 0$ (`t_vars[(i, i)] = []`, line 422):** By Galois conjugation over $\mathbb{Q}(\zeta_7)$, the adjacency eigenspaces $E_3$ ($\dim 54$) and $E_{-4}$ ($\dim 44$) have constant multiplicity $m_3, m_{-4}$ across $\zeta_7^k$ ($k=1..6$) with $m_3 + m_{-4} = 14$, giving $-\mathrm{Tr}(B) = 6(3m_3 - 4m_{-4}) = 42m_3 - 336 \equiv 0 \pmod{42}$. Since $b_{ii} \in \{0, 2\}$ ($\lambda = 1$), $\mathrm{Tr}(B) \in [0, 24]$ is a multiple of $42$, forcing $\mathrm{Tr}(B) = 0 \implies b_{ii} = 0$ (matching Prop. 4.7 of `arXiv:2308.02978`).
   - **Normalizer symmetry breaking (lines 449–467):** Under the orbit normalizer $S_3(I_{LL}) \times S_3(I_{RR}) \rtimes \mathbb{Z}_2 \times S_6(I_{LR})$, orders $b_{0,1} \ge b_{0,2} \ge b_{1,2}$ (lines 450–453), $b_{3,4} \ge b_{3,5} \ge b_{4,5}$ (lines 455–457), $b_{0,1} \ge b_{3,4}$ (line 459), and lexicographically orders columns $6..11$ of $I_{LR}$ (lines 461–467).
   - **Inner-outer $L/R$ coordinate balance on rows and columns (lines 469–484, 510–532):** By `p2_3` (Lemma 4.8 of `arXiv:2308.02978`), every outer vertex has $12$ $L$-coordinates and $12$ $R$-coordinates among its $12$ outer neighbors: $2 \sum_{j \in I_{LL}} b_{ij} + \sum_{j \in I_{LR}} b_{ij} = 12$ (`L_ll == 12`, line 515) and $2 \sum_{j \in I_{RR}} b_{ij} + \sum_{j \in I_{LR}} b_{ij} = 12$ (`L_rr == 12`, line 523), which implies $\sum_{j \in I_{LL}} b_{ij} = \sum_{j \in I_{RR}} b_{ij}$ on every row (`L_bal`, line 476; summed over $I_{LL}$ as `L_sll == 9`, line 484) and on every column $j \in I_{LR}$ (`L_col == 9`, line 532).
   - **Outer row degree $12$ (`L_tot == 12`, line 490):** $\sum_{j=0}^{11} b_{ij} = 12$.
   - **Diagonal 2-path identity (`L_diag == 5`, line 507) and linear row identity (`L_diff == 18`, line 498):** Counting two-paths between $u \in O_i$ and the $6$ other vertices of $O_i \setminus \{u\}$ ($6 \times 2 = 12$ total common neighbors, minus $2$ in $\Gamma_1(0)$) gives $\sum_{j \ne i} b_{ij}(b_{ij}-1) = 10 \iff \sum_{j \ne i} \binom{b_{ij}}{2} = \sum_{j \ne i} (u_1 + 2u_2) = 5$ (`L_diag == 5`). Subtracting from $\sum_{j \ne i} (u_0 + u_1 + u_2) = 12$ gives $\sum_{j \ne i} (u_0 - u_2) = 7$; rewriting $-u_2$ as $(1 - u_2)$ across the $11$ off-diagonal columns $j \ne i$ yields $\sum_{j \ne i} (u_0 + (1 - u_2)) = 18$ (`L_diff == 18`).
   - **Column upper bounds for $j \in I_{LR}$ (`L_c_up <= 6`, `L_c_diag <= 5`, lines 534–544):** Since column $j \in I_{LR}$ has $\sum_{i=0}^{11} b_{ij} = 12$ with $\sum_{i \in I_{LL}} b_{ij} = \sum_{i \in I_{RR}} b_{ij}$ and $b_{ij} \ge 0$ on $i \in I_{LR}$, $\sum_{i=0}^{2} b_{ij} \le 6$ (`L_c_up <= 6`, line 537). Since $\sum_{i \ne j} (u_1 + 2u_2) = 5$ across all $11$ rows $i \ne j$, the top-6-row partial sum satisfies $\sum_{i=0}^{5} (u_1 + 2u_2) \le 5$ (`L_c_diag <= 5`, line 544).
   - **Off-diagonal 2-path equation (`rhs_ij = 10` or `14`, lines 546–563):** Counting two-paths between $u \in O_i$ and $O_j$ ($0 \le i < j < 6$) gives $b_{ij} + \sum_{k \notin \{i,j\}} b_{ik} b_{jk} = 14 - \text{inner}_{ij}$, where $\text{inner}_{ij} = 4$ if $i, j$ are both in $I_{LL}$ or both in $I_{RR}$ (`rhs_ij = 10`), and $0$ if $i \in I_{LL}, j \in I_{RR}$ (`rhs_ij = 14`).

2. **`p5_t1_fix9` (`r4_mode = "p5_orbit_sym"`, `build_p5_t1_orbit_cnf` in `verify.py` lines 568–772):**
   - Encodes the $20 \times 20$ orbit-valency matrix on the $16$ outer $5$-cycles and $4$ fixed outer vertices $O_{16}..O_{19}$, with: induced 4-cycle on $O_{16}..O_{19}$ from $\mathrm{Fix}(g) \cong K_3 \square K_3$ (`p2_5`, lines 656–661); $b_{ii} = 0$ and $b_{ij} \le 2$ (lines 662–670); normalizer symmetry breaking $b_{0,2} \ge b_{0,3}$, $b_{0,1} \ge b_{2,3}$, and $S_4$ ordering on columns $16..19$ of row $0$ (lines 684–702); inner-outer balance $B C = R$ (lines 704–730); diagonal 2-path identity $\sum_{j \ne i} u_2(i,j) = (4 - \text{inner}_{ii})/2 \in \{1, 2\}$ and linear row difference $\sum_{j \ne i} u_1(i,j) = 12 - \text{rhs\_diag}$ (lines 732–745); and off-diagonal 2-path equations (lines 754–770).

3. **`frob21_z7_z3` (`r4_mode = "frob21_fig10"`, `verify.py` lines 1024–1042):**
   - Adds the orbit valencies from Proposition 4.10 / Figure 10 of `arXiv:2308.02978`: $LR$ and $RL$ are cocliques (lines 1035–1039) and $b_{LL,LL} = b_{LL,RR} = b_{RR,RR} = 2$ (lines 1040–1042).

4. **Prime $p = 2$ Involutions (`verify.py` lines 828–1022):**
   - **Subset selection of `p2_4` equations (`r4_mode`):** `"conj"` (conjugate pairs $q = g(p)$), `"conj_or_fix"` ($q = g(p)$ or $p, q \in \mathrm{Fix}(g)$), `"spectral_trace"` ($q = g(p)$ or $p \in \mathrm{Fix}(g)$ or $q \in \mathrm{Fix}(g)$, with multiplicity folding `L_odd` / `L_even` on lines 909–927 and 1002–1020 and $S_b$ symmetry breaking on the $b$ flipped inner edges on lines 894–900), and `"global_triangle_bijection"` (`p2_3` plus the global flipped-edge and spectral trace equations on lines 828–874).
   - **Spectral trace identity ($\mathrm{Tr}(B) = 8a + 3b + 4k_2 - 7m_3(-1)$, lines 863–893):** Equating the combinatorial trace $\mathrm{Tr}(g A) = 2b + 2\,\mathrm{Tr}(B)$ with the spectral trace $\mathrm{Tr}(g A) = 14 + 3(54 - 2m_3(-1)) - 4(44 - 2m_{-4}(-1)) = -6m_3(-1) + 8m_{-4}(-1)$ using $m_3(-1) + m_{-4}(-1) = 7 - c + a + k_2$ gives $\mathrm{Tr}(B) = 8a + 3b + 4k_2 - 7m_3(-1)$, so $(8a + 3b + 4k_2 - \mathrm{Tr}(B)) \equiv 0 \pmod{7}$.
   - **Fixed-inner-edge triangle window for $c = 1$ ($12 - 4a \le \mathrm{Tr}(B) \le 12 + 2a$, lines 880–881):** Counts $g$-transversal edges inside the neighborhoods $\Gamma_1(6_L), \Gamma_1(6_R) \cong 7 K_2$ of the unique fixed inner edge $\{6_L, 6_R\}$.
   - **Global flipped-edge triangle bijection ($\mathrm{Tr}(B) = \sum_{z \in \mathrm{Fix}(g) \setminus \{0\}} b_z$, lines 828–861):** Every transversal outer edge $\{p, g(p)\} \in E(\Gamma)$ ($p \ne g(p)$) lies in a unique triangle $\{p, g(p), z\}$ whose third vertex $z$ is fixed by $g$ ($z \in \mathrm{Fix}(g) \setminus \{0\}$), establishing a bijection with the $g$-flipped edges in $\Gamma_1(z) \cong 7 K_2$ across $z \in \mathrm{Fix}(g) \setminus \{0\}$.
   - **How `(0,6,1)` (`p2_a0_b6_c1_fix3`) follows in 1 RUP step (`verify.py` lines 880–893 & 981–1010):** In $(0,6,1)$, $|\mathrm{Fix}(g)| = 3$ ($0, 6_L, 6_R$), so **zero outer vertices are fixed by $g$** ($k_2 = 42$). For each of the $12$ conjugate outer pairs $p_0 = \{(i, L), (6, s)\}, q_0 = \{(i, R), (6, s)\}$ ($i \in \{0..5\}, s \in \{L, R\}$; variables `742, 804, 1282, 1324, 1570, 1596, 1702, 1716, 1750, 1756, 1762, 1764`), $p_0$ and $q_0$ share the inner neighbor $(6, s)$, so `p2_4` has $\text{rhs} = 2 - 1 = 1$. Since every other outer vertex $r \notin \{p_0, q_0\}$ lies in a 2-cycle $\{r, g(r)\}$, every conjunction literal $e_{p_0, r} \wedge e_{q_0, r}$ appears twice in `L` (`cnt == 2`, falsified by `cnt > rhs`), leaving `L_odd = [e_{p_0, q_0}]` as a singleton forced to `1` by `add_eq(L_odd, 1)` (line 1010). Meanwhile, $8a + 3b + 4k_2 = 186$ and $t_{\max,\text{bound}} = 12$ give `valid_tr = [4, 11]` ($t_{\max} = 11$), so `add_eq(conj_vars + [y_0]*7, 11)` (line 893) enforces $\sum_{v \in \text{conj\_vars}} v \le 11$, which conflicts with the $12$ forced unit variables in **1 RUP step**.
   - **How `(3,0,1)` (`p2_a3_b0_c1_fix9`) follows in 1 RUP step (`verify.py` lines 828–874):** In $(3,0,1)$, $b = 0$ and $t_{\text{tri}} = \sum_{z \in \mathrm{Fix}(g) \setminus \{0\}} b_z = 0$ (line 833), so `add_eq(list(conj_vars), 0)` (line 850) emits unit clauses `[-v]` falsifying all $k_2 = 39$ diagonal variables $v \in \text{conj\_vars}$. Meanwhile, $8a + 3b + 4k_2 = 24 + 0 + 156 = 180$ gives `valid_tr = [5, 12, 19, 26, 33]` ($t_{\max} = 33, M = 4$), and `add_eq(conj_vars + [y_0]*7 + [y_1]*7 + [y_2]*7 + [y_3]*7, 33)` (line 874) requires a sum of $33$, whereas the $4$ auxiliary variables can contribute at most $4 \times 7 = 28 < 33$ once `conj_vars` are falsified, reaching a conflict in **1 RUP step**.

---

## Literature Classification of the 22 Track `p1` Cases in `object/certificate.json`

| Case ID | Prime / Group | Cycle Structure | Excluded in `arXiv:2308.02978`? | Excluded in Cited Refinements (MM04 / BL11)? | Excluded in `arXiv:2608.11211`? | Counts for `p1`? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `p7_fix1` | $p = 7$ ($\mathbb{Z}_7$) | $1$ fixed, $14 \times 7$-cycles | **No (OPEN)** | **No (OPEN)** | **No (`UNKNOWN` after 48h timeout)** | **YES** |
| `p5_t1_fix9` | $p = 5$ ($\mathbb{Z}_5$) | $9$ fixed, $18 \times 5$-cycles | Cited in §1 | **Yes** (MM04 Thm. 2.7) | Not tested | **No** |
| `p3_t1_fix33` | $p = 3$ ($\mathbb{Z}_3$) | $33$ fixed, $22 \times 3$-cycles | Cited in §1 | **Yes** (MM04: $|\mathrm{Fix}(g)| \in \{0, 3\}$) | Not tested | **No** |
| `frob21_z7_z3` | $\mathrm{Frob}(21)$ | $1$ fixed, $4 \times 7 + 3 \times 21$ | **Yes** (§6, GAP search) | No | Not tested | **No** |
| `p2_a0_b5_c2_fix9` | $p = 2$, $(0,5,2)$ | $9$ fixed, $45 \times 2$-cycles | **No (OPEN)** | **No (OPEN)** | **No (not tested)** | **YES** |
| Remaining 17 $p = 2$ profiles `(0,1,6)`..`(3,1,0)` | $p = 2$ ($\mathbb{Z}_2$) | Odd $|\mathrm{Fix}(g)| \in [3, 73]$ | **No (OPEN, Cor. 4.4(a))** | Yes (MM04 fixed-subgraph bound) | **No (not tested)** | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) |

---

## Not Claimed

- **Full Solution of Conway's 99-Graph Problem:** We do **not** claim a `CONFIRMED_SOLUTION` (either constructing an $\mathrm{srg}(99, 14, 1, 2)$ or certifying that no such graph exists without symmetry assumptions).
- **One Claim Per Package (Track `p2` Only in This PR):** Per repository convention (`kit/SUBMIT.md`), this package (`known-knowns/conway-99-graph/2026-10-26-mizopl-bcf57871/`) claims **only Track `p2`** (the dual-encoded Pure-RUP LRAT re-derivation of the 5 forced-structure reduction propositions `p2_1`–`p2_5` of `arXiv:2608.11211` and the $\mathrm{srg}(9, 4, 1, 2) \cong K_3 \square K_3$ validation). The Track `p1` automorphism exclusions are claimed separately in the companion Track `p1` package (`known-knowns/conway-99-graph/2026-10-29-mizopl-5b09a9c5/`).
- **Remaining Open Automorphism Cases:** Prime order $p = 3$ with $|\mathrm{Fix}(g)| \in \{0, 3\}$ and the 19th involution profile $(0, 7, 0)$ ($|\mathrm{Fix}(g)| = 1$, $49 \times 2$-cycles) are not excluded here.

---

## Credits

- **Contributor:** `@mizopl`
- **Target:** `conway-99-graph` (`known-knowns`)
