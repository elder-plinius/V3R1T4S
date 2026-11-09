# `conway-99-graph` (Track `p1`): Dual-Encoded Pure-RUP LRAT UNSAT Certificates for Prime-Order Automorphism Cases

## What

Track p1 on conway-99-graph (srg(99, 14, 1, 2)): Dual-encoded pure-RUP LRAT (0 RAT lemmas) UNSAT certificates across two independent SAT cardinality encodings (Encoding A = Sinz 2005 Sequential Counter, Encoding B = Bailleux & Boufkhad 2003 Binary Tree Totalizer) for prime-order automorphisms fixing a root vertex 0 not already excluded by Cesarz & Woldar (arXiv:2308.02978, 2023), its cited background/refinements (Makhnev & Minakova 2004; Behbahani & Lam 2011), or Thakkar & Severini (arXiv:2608.11211, 2026): specifically p=7 with 1 fixed vertex and 14 7-cycles (p7_fix1, open in arXiv:2308.02978 Cor. 4.4(b) and UNKNOWN after 48h in arXiv:2608.11211 §2.4) and p=2 profile (0,5,2) with 9 fixed vertices and 45 2-cycles (p2_a0_b5_c2_fix9, open in Makhnev & Minakova 2004, arXiv:2308.02978 Cor. 4.4(a), and arXiv:2608.11211), together with the 17 remaining certified p=2 involution profiles across (0,1,6)..(3,1,0) (open in arXiv:2308.02978 and arXiv:2608.11211, excluded analytically in Makhnev & Minakova 2004) and LRAT re-derivations of frob21_z7_z3, p5_t1_fix9, and p3_t1_fix33 (already excluded in arXiv:2308.02978 or Makhnev & Minakova 2004 and not counted as new p1 exclusions).

---

## Check It Yourself

Run the standalone pure-Python checker from the root of this package:

```bash
sh verify-it-yourself/run_checks.sh
```

What `verify-it-yourself/verify.py` checks in ~20 seconds using only the Python 3 standard library:
1. **Positive Non-Vacuity Control on $\mathrm{srg}(9, 4, 1, 2) \cong K_3 \square K_3$ (`verify_positive_control_srg9`):** Verifies that the forced-structure encoding is satisfiable for $k = 4$ in both Encoding A and Encoding B.
2. **Foundational Forced-Structure Propositions (`p2_1`–`p2_5`):** Verifies the 10 dual-encoded LRAT certificates for the neighborhood partition $\{0\} \cup \Gamma_1(0) \cup \Gamma_2(0)$ on which the orbital encodings rest (claimed separately in PR #774, `known-knowns/conway-99-graph/2026-10-26-mizopl-bcf57871/`).
3. **Track `p1` Automorphism Exclusions (22 cases $\times$ 2 encodings = 44 Pure-RUP LRAT proofs):** Freshly generates the full CNF formulas in Encoding A (`Sinz_2005_Sequential_Counter`) and Encoding B (`Bailleux_Boufkhad_2003_Binary_Tree_Totalizer`), verifies exact CNF subset membership of every `*_core.cnf`, and checks every LRAT proof step via pure-Python Reverse Unit Propagation (`0` RAT lemmas), printing `VERIFY: PASS`.

---

## Compared To

For each of the 22 automorphism cases in `object/certificate.json`, the table below states whether `arXiv:2308.02978` (Cesarz & Woldar 2023), its cited background/refinements (Makhnev & Minakova 2004, *Discrete Math. Appl.* 14(2):201–210; Behbahani & Lam 2011, *Discrete Math.* 311:897–906), or `arXiv:2608.11211` (Thakkar & Severini 2026) already exclude it, and which cases count for `p1`:

| # | Case ID | Prime / Group | Cycle Structure $(|\mathrm{Fix}(g)|, \text{cycles})$ | Excluded in `arXiv:2308.02978` (2023)? | Excluded in Cited Background / Refinements (Makhnev–Minakova 2004, Behbahani–Lam 2011)? | Excluded in `arXiv:2608.11211` (2026)? | Counts for `p1`? | Enc A / Enc B RUP Steps (`0` RAT) |
| :-: | :--- | :--- | :--- | :--- | :--- | :--- | :---: | :---: |
| 1 | `p7_fix1` | $p = 7$ ($\mathbb{Z}_7$) | $1$ fixed, $14 \times 7$-cycles | **No (OPEN, Cor. 4.4(b))** | **No (OPEN)** | **No (`UNKNOWN` after 48h timeout on 14 cores, §2.4)** | **YES (Open in all prior work)** | `56,515` / `23,551` |
| 2 | `p5_t1_fix9` | $p = 5$ ($\mathbb{Z}_5$) | $9$ fixed, $18 \times 5$-cycles | Cited as excluded in §1 | **Yes** (Makhnev–Minakova 2004, Thm. 2.7) | Not tested | **No** (re-derivation only) | `3,667` / `3,130` |
| 3 | `p3_t1_fix33` | $p = 3$ ($\mathbb{Z}_3$) | $33$ fixed, $22 \times 3$-cycles | Cited as excluded in §1 | **Yes** (Makhnev–Minakova 2004: $|\mathrm{Fix}(g)| \in \{0, 3\}$) | Not tested | **No** (re-derivation only) | `17` / `20` |
| 4 | `frob21_z7_z3` | $\mathrm{Frob}(21) = \mathbb{Z}_7 \rtimes \mathbb{Z}_3$ | $1$ fixed, $4 \times 7 + 3 \times 21$ | **Yes** (§6, uncertified GAP search, 2,916 iters) | No (open prior to 2023) | Not tested | **No** (re-derivation only) | `25` / `16` |
| 5 | `p2_a0_b1_c6_fix73` | $p = 2$, $(0,1,6)$ | $73$ fixed, $13 \times 2$-cycles | **No (OPEN, Cor. 4.4(a))** | Yes (MM04 fixed-subgraph bound $|\mathrm{Fix}(g)| \in \{1,9\}$) | **No (not tested)** | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) | `11` / `12` |
| 6 | `p2_a0_b2_c5_fix51` | $p = 2$, $(0,2,5)$ | $51$ fixed, $24 \times 2$-cycles | **No (OPEN, Cor. 4.4(a))** | Yes (MM04: $|\mathrm{Fix}(g)| \in \{1,9\}$) | **No (not tested)** | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) | `11` / `12` |
| 7 | `p2_a0_b3_c4_fix33` | $p = 2$, $(0,3,4)$ | $33$ fixed, $33 \times 2$-cycles | **No (OPEN, Cor. 4.4(a))** | Yes (MM04: $|\mathrm{Fix}(g)| \in \{1,9\}$) | **No (not tested)** | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) | `112` / `109` |
| 8 | `p2_a0_b4_c3_fix19` | $p = 2$, $(0,4,3)$ | $19$ fixed, $40 \times 2$-cycles | **No (OPEN, Cor. 4.4(a))** | Yes (MM04: $|\mathrm{Fix}(g)| \in \{1,9\}$) | **No (not tested)** | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) | `88` / `90` |
| 9 | `p2_a0_b5_c2_fix9` | $p = 2$, $(0,5,2)$ | $9$ fixed, $45 \times 2$-cycles | **No (OPEN, Cor. 4.4(a))** | **No (OPEN: $|\mathrm{Fix}(g)| = 9$ star of 4 triangles)** | **No (not tested)** | **YES (Open in all prior work)** | `184` / `200` |
| 10 | `p2_a0_b6_c1_fix3` | $p = 2$, $(0,6,1)$ | $3$ fixed, $48 \times 2$-cycles | **No (OPEN, Cor. 4.4(a))** | Yes (MM04: $|\mathrm{Fix}(g)| \in \{1,9\}$) | **No (not tested)** | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) | `1` / `1` |
| 11 | `p2_a1_b0_c5_fix53` | $p = 2$, $(1,0,5)$ | $53$ fixed, $23 \times 2$-cycles | **No (OPEN, Cor. 4.4(a))** | Yes (MM04: $|\mathrm{Fix}(g)| \in \{1,9\}$) | **No (not tested)** | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) | `164` / `165` |
| 12 | `p2_a1_b1_c4_fix35` | $p = 2$, $(1,1,4)$ | $35$ fixed, $32 \times 2$-cycles | **No (OPEN, Cor. 4.4(a))** | Yes (MM04: $|\mathrm{Fix}(g)| \in \{1,9\}$) | **No (not tested)** | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) | `16` / `25` |
| 13 | `p2_a1_b2_c3_fix21` | $p = 2$, $(1,2,3)$ | $21$ fixed, $39 \times 2$-cycles | **No (OPEN, Cor. 4.4(a))** | Yes (MM04: $|\mathrm{Fix}(g)| \in \{1,9\}$) | **No (not tested)** | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) | `150` / `150` |
| 14 | `p2_a1_b3_c2_fix11` | $p = 2$, $(1,3,2)$ | $11$ fixed, $44 \times 2$-cycles | **No (OPEN, Cor. 4.4(a))** | Yes (MM04: $|\mathrm{Fix}(g)| \in \{1,9\}$) | **No (not tested)** | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) | `65` / `62` |
| 15 | `p2_a1_b4_c1_fix5` | $p = 2$, $(1,4,1)$ | $5$ fixed, $47 \times 2$-cycles | **No (OPEN, Cor. 4.4(a))** | Yes (MM04: $|\mathrm{Fix}(g)| \in \{1,9\}$) | **No (not tested)** | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) | `127` / `126` |
| 16 | `p2_a1_b5_c0_fix3` | $p = 2$, $(1,5,0)$ | $3$ fixed, $48 \times 2$-cycles | **No (OPEN, Cor. 4.4(a))** | Yes (MM04: $|\mathrm{Fix}(g)| \in \{1,9\}$) | **No (not tested)** | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) | `1,073` / `996` |
| 17 | `p2_a2_b0_c3_fix23` | $p = 2$, $(2,0,3)$ | $23$ fixed, $38 \times 2$-cycles | **No (OPEN, Cor. 4.4(a))** | Yes (MM04: $|\mathrm{Fix}(g)| \in \{1,9\}$) | **No (not tested)** | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) | `182` / `216` |
| 18 | `p2_a2_b1_c2_fix13` | $p = 2$, $(2,1,2)$ | $13$ fixed, $43 \times 2$-cycles | **No (OPEN, Cor. 4.4(a))** | Yes (MM04: $|\mathrm{Fix}(g)| \in \{1,9\}$) | **No (not tested)** | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) | `202` / `200` |
| 19 | `p2_a2_b2_c1_fix7` | $p = 2$, $(2,2,1)$ | $7$ fixed, $46 \times 2$-cycles | **No (OPEN, Cor. 4.4(a))** | Yes (MM04: $|\mathrm{Fix}(g)| \in \{1,9\}$) | **No (not tested)** | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) | `39` / `39` |
| 20 | `p2_a2_b3_c0_fix5` | $p = 2$, $(2,3,0)$ | $5$ fixed, $47 \times 2$-cycles | **No (OPEN, Cor. 4.4(a))** | Yes (MM04: $|\mathrm{Fix}(g)| \in \{1,9\}$) | **No (not tested)** | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) | `40` / `40` |
| 21 | `p2_a3_b0_c1_fix9` | $p = 2$, $(3,0,1)$ | $9$ fixed, $45 \times 2$-cycles | **No (OPEN, Cor. 4.4(a))** | Yes (MM04 requires $c=2$ for $|\mathrm{Fix}(g)|=9$) | **No (not tested)** | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) | `1` / `1` |
| 22 | `p2_a3_b1_c0_fix7` | $p = 2$, $(3,1,0)$ | $7$ fixed, $46 \times 2$-cycles | **No (OPEN, Cor. 4.4(a))** | Yes (MM04: $|\mathrm{Fix}(g)| \in \{1,9\}$) | **No (not tested)** | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) | `185` / `185` |

---

## Complete List of Encoding Constraints Beyond `srg(99, 14, 1, 2)` and the Stated Automorphism, with Derivations

Every constraint added by `verify-it-yourself/verify.py` beyond the raw $\mathrm{srg}(99, 14, 1, 2)$ conditions (`p2_3` inner-outer balance and `p2_4` outer-pair common neighbors) and the stated automorphism `perms` is listed below in one place with its mathematical derivation and exact line numbers in `verify.py` (see `how-we-built-it/artifact.md` §4 for expanded derivations):

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

## Not Claimed

- **Full Solution of Conway's 99-Graph Problem:** We do **not** claim a `CONFIRMED_SOLUTION` (either constructing an $\mathrm{srg}(99, 14, 1, 2)$ or certifying that no such graph exists without symmetry assumptions).
- **One Claim Per Package (Track `p1` Only in This PR):** Per repository convention (`kit/SUBMIT.md`), this package (`known-knowns/conway-99-graph/2026-10-29-mizopl-5b09a9c5/`) claims **only Track `p1`**, while Track `p2` (the forced-structure reduction re-derivation of `arXiv:2608.11211`) is claimed separately in PR #774 (`known-knowns/conway-99-graph/2026-10-26-mizopl-bcf57871/`).
- **Cases Already Excluded in Prior Literature:** As documented in the `Compared To` table above, `frob21_z7_z3` (excluded in `arXiv:2308.02978` §6), `p5_t1_fix9` (excluded in Makhnev & Minakova 2004, Thm. 2.7), and `p3_t1_fix33` (excluded in Makhnev & Minakova 2004) are included only as dual-encoded LRAT re-derivations and are not counted as new `p1` exclusions; likewise, for $p = 2$, we distinguish between `p2_a0_b5_c2_fix9` (open in all prior literature) and the 17 profiles `(0,1,6)`..`(3,1,0)` (open in `arXiv:2308.02978` and `arXiv:2608.11211`, excluded analytically in Makhnev & Minakova 2004).
- **Remaining Open Automorphism Cases:** Prime order $p = 3$ with $|\mathrm{Fix}(g)| \in \{0, 3\}$ and the 19th involution profile $(0, 7, 0)$ ($|\mathrm{Fix}(g)| = 1$, $49 \times 2$-cycles) remain open.

---

## Credits

- **Contributor:** `@mizopl`
- **Target:** `conway-99-graph` (`known-knowns`)
