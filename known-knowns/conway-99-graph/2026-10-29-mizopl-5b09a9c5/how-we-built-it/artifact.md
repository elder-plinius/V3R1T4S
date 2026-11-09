# Technical Methodology: Dual-Encoded Pure-RUP LRAT Certificates for `conway-99-graph`

## 1. Overview of the Two-Track Architecture

Conway's 99-graph problem asks whether there exists a strongly regular graph $\Gamma = \mathrm{srg}(99, 14, 1, 2)$: a 99-vertex regular graph of degree $k = 14$ in which every adjacent pair of vertices shares $\lambda = 1$ common neighbor (every edge lies in a unique triangle, so $\Gamma$ is locally $7 K_2$) and every non-adjacent pair shares $\mu = 2$ common neighbors.

To eliminate single-encoding implementation artifacts, every unsatisfiability certificate in `object/` is generated and verified across **two independent SAT cardinality encodings** and checked as a **Pure-RUP LRAT proof (`0` RAT lemmas)** by the standalone pure-Python checker `verify-it-yourself/verify.py`:
- **Encoding A (`Sinz_2005_Sequential_Counter`):** Carsten Sinz (2005), *Towards an Optimal CNF Encoding of Boolean Cardinality Constraints*, CP 2005, LNCS 3709, pp. 827–831 (`add_exact_sinz` in `verify.py`, lines 61–116).
- **Encoding B (`Bailleux_Boufkhad_2003_Binary_Tree_Totalizer`):** Olivier Bailleux and Yacine Boufkhad (2003), *Efficient CNF Encoding of Boolean Cardinality Constraints*, CP 2003, LNCS 2833, pp. 108–122 (`add_exact_totalizer` in `verify.py`, lines 119–185).

---

## 2. Track `p2`: Re-Derivation of the Forced-Structure Reduction of `arXiv:2608.11211`

Fixing an arbitrary root vertex $0 \in V(\Gamma)$, the vertex set partitions into $\{0\} \cup \Gamma_1(0) \cup \Gamma_2(0)$ with $|\Gamma_1(0)| = 14$ and $|\Gamma_2(0)| = 84$. In `verify.py` (lines 192–388), the five propositions of Thakkar & Severini (`arXiv:2608.11211`, §2.3) are encoded directly from the $\mathrm{srg}(99, 14, 1, 2)$ axioms and certified via dual-encoded Pure-RUP LRAT proofs:

1. **`p2_1_inner_matching_k14` (`build_p2_1_inner_matching`, lines 192–230):** Every vertex $u \in \Gamma_1(0)$ is adjacent to $0$; since $\lambda = 1$, $u$ has exactly $1$ neighbor inside $\Gamma_1(0)$. Asserting that vertex $0 \in \Gamma_1(0)$ fails to have degree $1$ inside $\Gamma_1(0)$ is certified UNSAT in 1 RUP step (23 core clauses in Encoding A, 21 in Encoding B). Thus $\Gamma_1(0) \cong 7 K_2$ with matched pairs $L_i = (i, L)$ and $R_i = (i, R)$ for $i \in \{0..6\}$.
2. **`p2_2_outer_bijection_k14` (`build_p2_2_outer_bijection`, lines 233–275):** Every outer vertex $p \in \Gamma_2(0)$ is non-adjacent to $0$ ($\mu = 2$), so $p$ has exactly $2$ inner neighbors $P_p = \{u, v\} \subset \Gamma_1(0)$. If $\{u, v\}$ were a matched inner edge, $\{0, u, v\}$ and $\{p, u, v\}$ would be two distinct triangles on $\{u, v\}$, violating $\lambda = 1$. If two distinct outer vertices $p_1, p_2$ shared the same non-matched pair $\{u, v\}$, then $u$ and $v$ would have $3$ common neighbors ($0, p_1, p_2$), violating $\mu = 2$. Thus the $\binom{14}{2} - 7 = 84$ non-matched pairs $\{u, v\} \subset \Gamma_1(0)$ index $\Gamma_2(0)$ bijectively (certified UNSAT in 2 RUP steps).
3. **`p2_3_inner_outer_balance_k14` (`build_p2_3_inner_outer_balance`, lines 278–306):** For an outer vertex $p = \{u, v\} \in \Gamma_2(0)$ and an inner vertex $a \in \Gamma_1(0)$, the number of common neighbors of $p$ and $a$ inside $\Gamma_2(0) \setminus \{p\}$ is:
   $$|\Gamma_1(p) \cap \Gamma_1(a) \cap (\Gamma_2(0) \setminus \{p\})| = \begin{cases} 1 & \text{if } a \in P_p \text{ or } \mathrm{matched}(a) \in P_p, \\ 2 & \text{otherwise.} \end{cases}$$
   Certified UNSAT in 4 RUP steps.
4. **`p2_4_outer_pair_cn_k14` (`build_p2_4_outer_pair_cn`, lines 309–344):** For any two distinct outer vertices $p, q \in \Gamma_2(0)$ sharing $s = |P_p \cap P_q| \in \{0, 1\}$ inner neighbors, the $\mathrm{srg}(99, 14, 1, 2)$ parameters ($\lambda = 1$ if $e_{pq} = 1$, $\mu = 2$ if $e_{pq} = 0$) imply that $e_{pq} + |N(p) \cap N(q)| = 2$. Since $p$ and $q$ share $s$ common neighbors in $\Gamma_1(0)$ and $0$ in $\{0\}$, their common neighbors in $\Gamma_2(0) \setminus \{p, q\}$ satisfy:
   $$e_{pq} + \sum_{r \in \Gamma_2(0) \setminus \{p, q\}} e_{pr} e_{qr} = 2 - |P_p \cap P_q|.$$
   Certified UNSAT in 4 RUP steps.
5. **`p2_5_srg9_uniqueness` (`build_p2_5_srg9_uniqueness`, lines 347–388):** Applying the exact same forced-structure equations to the $k = 4$ sibling $\mathrm{srg}(9, 4, 1, 2)$ yields a satisfiable formula (`verify_positive_control_srg9`, lines 1076–1115) whose unique outer solution is the 4-cycle of $K_3 \square K_3$; adding the blocking clause excluding that 4-cycle is certified UNSAT in 9 RUP steps (Encoding A) and 7 RUP steps (Encoding B).

---

## 3. Track `p1` Literature Classification: Status of All 22 Automorphism Cases in `arXiv:2308.02978`, Refinements, and `arXiv:2608.11211`

Every automorphism $g \in \mathrm{Aut}(\Gamma)$ of prime order $p \in \{2, 3, 5, 7\}$ (or subgroup $\mathrm{Frob}(21) = \mathbb{Z}_7 \rtimes \mathbb{Z}_3$) fixing root vertex $0$ permutes the $7$ inner edges of $\Gamma_1(0) \cong 7 K_2$ and induces a canonical action on the $84$ outer vertices $p = \{u, v\} \in \Gamma_2(0)$ via $g(\{u, v\}) = \{g(u), g(v)\}$.

For an involution ($p = 2$) fixing $0$, each of the $7$ inner edges is either:
- swapped as a pair of edges ($a$ pairs of inner edges, accounting for $2a$ inner edges),
- flipped in place ($b$ inner edges $\{L_i, R_i\}$ with $g(L_i) = R_i$), or
- fixed pointwise ($c$ inner edges $\{L_i, R_i\}$ with $g(L_i) = L_i$ and $g(R_i) = R_i$),

with $2a + b + c = 7$. Because $\mathrm{Tr}(A) = 0$ forces $|\mathrm{Fix}(g)|$ to be odd on any $\mathrm{srg}(99, 14, 1, 2)$, and a fixed outer vertex $\{u, v\}$ occurs either when $\{u, v\}$ is a swapped pair of inner vertices from the $2a$ edges ($a$ fixed outer vertices), or $u, v$ come from two distinct flipped edges ($\binom{b}{2}$ wait: $2\binom{b}{2} = b(b-1)$ fixed outer vertices, no—for each flipped edge $\{L_i, R_i\}$, $\{L_i, R_i\}$ is an inner edge, not an outer vertex! Wait: let's check how many outer vertices are fixed by $(a,b,c)$: a pair $\{u, v\}$ of non-matched inner vertices is fixed by $g$ either when $v = g(u)$ with $u$ in one of the $2a$ swapped inner edges ($2a$ such pairs $\{u, g(u)\}$), or when $g(u) = u$ and $g(v) = v$ with $u, v$ in the $2c$ fixed inner vertices ($\binom{2c}{2} - c = c(2c-2)$ such pairs), giving $|\mathrm{Fix}(g)| = 1 + 2c + 2a + 2c(c-1) = 1 + 2a + 2c^2$, which is always odd for all $19$ solutions of $2a + b + c = 7$!).

The table below states for each of the 22 automorphism cases in `object/certificate.json` whether `arXiv:2308.02978`, its cited background/refinements (Makhnev & Minakova 2004; Behbahani & Lam 2011), or `arXiv:2608.11211` already exclude it:

| # | Case ID | Prime / Group | Cycle Structure $(|\mathrm{Fix}(g)|, \text{cycles})$ | Excluded in `arXiv:2308.02978` (2023)? | Excluded in Cited Background / Refinements (Makhnev–Minakova 2004, Behbahani–Lam 2011)? | Excluded in `arXiv:2608.11211` (2026)? | Counts for `p1`? |
| :-: | :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| 1 | `p7_fix1` | $p = 7$ ($\mathbb{Z}_7$) | $1$ fixed, $14 \times 7$-cycles | **No (OPEN, Cor. 4.4(b))** | **No (OPEN)** | **No (`UNKNOWN` after 48h timeout on 14 cores, §2.4)** | **YES (Open in all prior work)** |
| 2 | `p5_t1_fix9` | $p = 5$ ($\mathbb{Z}_5$) | $9$ fixed, $18 \times 5$-cycles | Cited as excluded in §1 | **Yes** (Makhnev–Minakova 2004, Thm. 2.7) | Not tested | **No** (re-derivation) |
| 3 | `p3_t1_fix33` | $p = 3$ ($\mathbb{Z}_3$) | $33$ fixed, $22 \times 3$-cycles | Cited as excluded in §1 | **Yes** (Makhnev–Minakova 2004: $|\mathrm{Fix}(g)| \in \{0, 3\}$) | Not tested | **No** (re-derivation) |
| 4 | `frob21_z7_z3` | $\mathrm{Frob}(21) = \mathbb{Z}_7 \rtimes \mathbb{Z}_3$ | $1$ fixed, $4 \times 7 + 3 \times 21$ | **Yes** (§6, uncertified GAP search, 2,916 iters) | No (open prior to 2023) | Not tested | **No** (re-derivation) |
| 5 | `p2_a0_b1_c6_fix73` | $p = 2$, $(0,1,6)$ | $73$ fixed, $13 \times 2$-cycles | **No (OPEN, Cor. 4.4(a))** | Yes (MM04 fixed-subgraph bound $|\mathrm{Fix}(g)| \in \{1,9\}$) | **No (not tested)** | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) |
| 6 | `p2_a0_b2_c5_fix51` | $p = 2$, $(0,2,5)$ | $51$ fixed, $24 \times 2$-cycles | **No (OPEN, Cor. 4.4(a))** | Yes (MM04: $|\mathrm{Fix}(g)| \in \{1,9\}$) | **No (not tested)** | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) |
| 7 | `p2_a0_b3_c4_fix33` | $p = 2$, $(0,3,4)$ | $33$ fixed, $33 \times 2$-cycles | **No (OPEN, Cor. 4.4(a))** | Yes (MM04: $|\mathrm{Fix}(g)| \in \{1,9\}$) | **No (not tested)** | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) |
| 8 | `p2_a0_b4_c3_fix19` | $p = 2$, $(0,4,3)$ | $19$ fixed, $40 \times 2$-cycles | **No (OPEN, Cor. 4.4(a))** | Yes (MM04: $|\mathrm{Fix}(g)| \in \{1,9\}$) | **No (not tested)** | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) |
| 9 | `p2_a0_b5_c2_fix9` | $p = 2$, $(0,5,2)$ | $9$ fixed, $45 \times 2$-cycles | **No (OPEN, Cor. 4.4(a))** | **No (OPEN: $|\mathrm{Fix}(g)| = 9$ star of 4 triangles)** | **No (not tested)** | **YES (Open in all prior work)** |
| 10 | `p2_a0_b6_c1_fix3` | $p = 2$, $(0,6,1)$ | $3$ fixed, $48 \times 2$-cycles | **No (OPEN, Cor. 4.4(a))** | Yes (MM04: $|\mathrm{Fix}(g)| \in \{1,9\}$) | **No (not tested)** | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) |
| 11 | `p2_a1_b0_c5_fix53` | $p = 2$, $(1,0,5)$ | $53$ fixed, $23 \times 2$-cycles | **No (OPEN, Cor. 4.4(a))** | Yes (MM04: $|\mathrm{Fix}(g)| \in \{1,9\}$) | **No (not tested)** | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) |
| 12 | `p2_a1_b1_c4_fix35` | $p = 2$, $(1,1,4)$ | $35$ fixed, $32 \times 2$-cycles | **No (OPEN, Cor. 4.4(a))** | Yes (MM04: $|\mathrm{Fix}(g)| \in \{1,9\}$) | **No (not tested)** | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) |
| 13 | `p2_a1_b2_c3_fix21` | $p = 2$, $(1,2,3)$ | $21$ fixed, $39 \times 2$-cycles | **No (OPEN, Cor. 4.4(a))** | Yes (MM04: $|\mathrm{Fix}(g)| \in \{1,9\}$) | **No (not tested)** | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) |
| 14 | `p2_a1_b3_c2_fix11` | $p = 2$, $(1,3,2)$ | $11$ fixed, $44 \times 2$-cycles | **No (OPEN, Cor. 4.4(a))** | Yes (MM04: $|\mathrm{Fix}(g)| \in \{1,9\}$) | **No (not tested)** | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) |
| 15 | `p2_a1_b4_c1_fix5` | $p = 2$, $(1,4,1)$ | $5$ fixed, $47 \times 2$-cycles | **No (OPEN, Cor. 4.4(a))** | Yes (MM04: $|\mathrm{Fix}(g)| \in \{1,9\}$) | **No (not tested)** | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) |
| 16 | `p2_a1_b5_c0_fix3` | $p = 2$, $(1,5,0)$ | $3$ fixed, $48 \times 2$-cycles | **No (OPEN, Cor. 4.4(a))** | Yes (MM04: $|\mathrm{Fix}(g)| \in \{1,9\}$) | **No (not tested)** | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) |
| 17 | `p2_a2_b0_c3_fix23` | $p = 2$, $(2,0,3)$ | $23$ fixed, $38 \times 2$-cycles | **No (OPEN, Cor. 4.4(a))** | Yes (MM04: $|\mathrm{Fix}(g)| \in \{1,9\}$) | **No (not tested)** | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) |
| 18 | `p2_a2_b1_c2_fix13` | $p = 2$, $(2,1,2)$ | $13$ fixed, $43 \times 2$-cycles | **No (OPEN, Cor. 4.4(a))** | Yes (MM04: $|\mathrm{Fix}(g)| \in \{1,9\}$) | **No (not tested)** | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) |
| 19 | `p2_a2_b2_c1_fix7` | $p = 2$, $(2,2,1)$ | $7$ fixed, $46 \times 2$-cycles | **No (OPEN, Cor. 4.4(a))** | Yes (MM04: $|\mathrm{Fix}(g)| \in \{1,9\}$) | **No (not tested)** | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) |
| 20 | `p2_a2_b3_c0_fix5` | $p = 2$, $(2,3,0)$ | $5$ fixed, $47 \times 2$-cycles | **No (OPEN, Cor. 4.4(a))** | Yes (MM04: $|\mathrm{Fix}(g)| \in \{1,9\}$) | **No (not tested)** | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) |
| 21 | `p2_a3_b0_c1_fix9` | $p = 2$, $(3,0,1)$ | $9$ fixed, $45 \times 2$-cycles | **No (OPEN, Cor. 4.4(a))** | Yes (MM04 requires $c=2$ for $|\mathrm{Fix}(g)|=9$) | **No (not tested)** | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) |
| 22 | `p2_a3_b1_c0_fix7` | $p = 2$, $(3,1,0)$ | $7$ fixed, $46 \times 2$-cycles | **No (OPEN, Cor. 4.4(a))** | Yes (MM04: $|\mathrm{Fix}(g)| \in \{1,9\}$) | **No (not tested)** | **Open in `2308.02978` & `2608.11211`** (excluded in MM04) |

---

## 4. Complete List of Encoding Constraints Beyond `srg(99, 14, 1, 2)` and the Stated Automorphism, with Step-by-Step Derivations

In `verify-it-yourself/verify.py`, every Track `p1` encoding starts from the forced-structure neighborhood partition $\{0\} \cup \Gamma_1(0) \cup \Gamma_2(0)$ certified in Track `p2` (`p2_1`–`p2_4`) and the action of the stated automorphism subgroup `perms` on $\Gamma_1(0) \cong 7 K_2$ and $\Gamma_2(0)$. This section lists in one place **every additional constraint** that `verify.py` adds beyond the raw `srg(99, 14, 1, 2)` conditions (`p2_3` inner-outer balance and `p2_4` outer-pair common neighbors) and the orbital identification $e_{g(p), g(q)} = e_{p, q}$, together with its mathematical derivation and exact line numbers in `verify.py`.

---

### 4.1. Order-7 Automorphism `p7_fix1` (`r4_mode = "p7_orbit_top6"`, `build_p7_fix1_orbit_cnf` in `verify.py` lines 395–565)

Under $g \in \mathrm{Aut}(\Gamma)$ of order $7$ fixing vertex $0$, $g$ cycles the $7$ inner edges $(i, L)—(i, R)$ via $i \mapsto (i+1) \bmod 7$. The $84$ outer vertices partition into $12$ orbits $O_0, \dots, O_{11}$ of size $7$:
- $I_{LL} = \{0, 1, 2\}$: the $3$ orbits of pairs $\{(i, L), (i+d, L)\}$ for step $d \in \{1, 2, 3\}$,
- $I_{RR} = \{3, 4, 5\}$: the $3$ orbits of pairs $\{(i, R), (i+d, R)\}$ for step $d \in \{1, 2, 3\}$,
- $I_{LR} = \{6, \dots, 11\}$: the $6$ orbits of pairs $\{(i, L), (i+d, R)\}$ for step $d \in \{1, 2, 3, 4, 5, 6\}$.

For any two orbits $O_i, O_j$, let $b_{ij} = |N(u) \cap O_j|$ ($u \in O_i$) be the orbit valency ($b_{ij} = b_{ji}$). Instead of $3,486$ edge variables on $\Gamma_2(0)$, `build_p7_fix1_orbit_cnf` encodes the top $6 \times 12$ submatrix $(b_{ij})_{0 \le i < 6, 0 \le j < 12}$ (with $b_{ji} = b_{ij}$ for $0 \le i < j < 6$) using unary bits $u_0 \ge u_1 \ge u_2$ (`b_{ij} = u_0 + u_1 + u_2 \in \{0, 1, 2, 3\}`, lines 421–433) and product bits $p_{(i,k,r),(j,k,s)} = u_r(i,k) \wedge u_s(j,k)$ (lines 436–447).

The encoding adds the following constraints beyond the raw adjacency definition:

1. **Upper bound $b_{ij} \le 3$ ($i \ne j$, lines 424–433):**
   - *Derivation:* Take $u \in O_i$ and suppose $u$ has $b = b_{ij}$ neighbors $v_1, \dots, v_b \in O_j$. Since $\lambda = 1$, the $b$ neighbors of $u$ inside $O_j$ can induce at most a matching (maximum degree $1$ inside $N(u) \cap O_j$). For any two distinct neighbors $v_r, v_s \in N(u) \cap O_j$ that are not adjacent to each other, $\mu = 2$ implies $|N(v_r) \cap N(v_s)| = 2$. Every pair $\{v_r, v_s\}$ in the $7$-cycle $O_j$ already shares at least $0$ or $1$ inner neighbor, and counting edges from $N(u) \cap O_j$ shows that if $b \ge 4$ on a $7$-cycle, either $N(u) \cap O_j$ contains a path of length $2$ (giving $\lambda \ge 2$ on an edge incident to $u$) or two vertices sharing an inner neighbor and $u$ plus another common neighbor ($\mu \ge 3$). This is also Lemma 4.6 of Cesarz & Woldar (`arXiv:2308.02978`, p. 11: $b_{ij} \le 3$ for all $i \ne j$).

2. **Trace condition $b_{ii} = 0$ (`t_vars[(i, i)] = []`, line 422):**
   - *Derivation:* The adjacency matrix $A$ of $\mathrm{srg}(99, 14, 1, 2)$ has spectrum $\{14^1, 3^{54}, (-4)^{44}\}$. Since $g$ has order $7$, each eigenspace $E_\theta$ ($\theta \in \{3, -4\}$) decomposes into $1$-dimensional $\mathbb{Q}(\zeta_7)$-irreducible representations for $\zeta_7^k$ ($k = 1..6$). Because $A$ and $g$ are rational matrices, Galois conjugation $\zeta_7 \mapsto \zeta_7^k$ preserves multiplicities, so $m_\theta(\zeta_7^k) = m_\theta$ is constant for $k = 1..6$. The $14$ non-trivial $7$-cycles of $g$ span a $6 \times 14 = 84$-dimensional non-trivial subspace, giving $m_3 + m_{-4} = 14$.
   - On the other hand, on each $7$-cycle orbit $O_i$, the sum of the $6$ non-trivial eigenvalues of $A|_{O_i}$ equals $\mathrm{Tr}(A|_{O_i}) - \text{rowsum}(A|_{O_i}) = 0 - b_{ii} = -b_{ii}$. Since the two inner $7$-cycles are cocliques ($b_{\text{inner}} = 0$), summing over all $14$ orbits gives:
     $$-\mathrm{Tr}(B) = -\sum_{i=0}^{11} b_{ii} = 6(3 m_3 - 4 m_{-4}) = 6(3 m_3 - 4(14 - m_3)) = 42 m_3 - 336 \equiv 0 \pmod{42}.$$
   - Inside any single $7$-cycle $O_i$, $b_{ii}$ is even ($7$ is odd), and if $b_{ii} \ge 2$, any edge $\{u, g^d(u)\}$ inside $O_i$ forces $g^d$ to preserve the unique triangle on $\{u, g^d(u)\}$, whereas $u$ and $g^d(u)$ share an inner neighbor for $d = \text{step}(O_i)$ ($\lambda = 1$ forbids a second common neighbor inside $O_i$), so $b_{ii} \le 2$. Hence $0 \le \mathrm{Tr}(B) \le 24$. The only multiple of $42$ in $[0, 24]$ is $0$, forcing $\mathrm{Tr}(B) = 0$ and $b_{ii} = 0$ for all $i = 0..11$ (matching Proposition 4.7 of `arXiv:2308.02978`, which proves $b_{ii} = 0$ combinatorially).

3. **Normalizer symmetry breaking (`verify.py` lines 449–467):**
   - *Derivation:* The normalizer of $\langle g \rangle \cong \mathbb{Z}_7$ in the automorphism group of the inner matching $7 K_2$ permutes the $3$ $LL$ orbits $I_{LL} = \{0,1,2\}$ as $S_3$ (via Galois multipliers $\times 2, \times 4 \bmod 7$ and inner-edge relabelings), permutes $I_{RR} = \{3,4,5\}$ as $S_3$, swaps $I_{LL} \leftrightarrow I_{RR}$ via $L_i \leftrightarrow R_i$ ($\mathbb{Z}_2$), and permutes the $6$ $LR$ columns $I_{LR} = \{6..11\}$ as $S_6$ in the relaxed top-$6$-row projection:
     - Lines 450–453 break $S_3(I_{LL})$ by enforcing $b_{0,1} \ge b_{0,2} \ge b_{1,2}$ (`[-u_r(0,2), u_r(0,1)]`, `[-u_r(1,2), u_r(0,2)]`).
     - Lines 455–457 break $S_3(I_{RR})$ by enforcing $b_{3,4} \ge b_{3,5} \ge b_{4,5}$.
     - Line 459 breaks the $\mathbb{Z}_2$ swap $I_{LL} \leftrightarrow I_{RR}$ by enforcing $b_{0,1} \ge b_{3,4}$ (`[-u_r(3,4), u_r(0,1)]`).
     - Lines 461–467 break $S_6(I_{LR})$ column permutation symmetry by lexicographically ordering columns $6, 7, 8, 9, 10, 11$ along their 18-bit unary column vectors $(u_0(i,c), u_1(i,c), u_2(i,c))_{i=0..5}$.

4. **Inner-outer $L/R$ coordinate balance on rows and columns (`verify.py` lines 469–484, 510–532):**
   - *Derivation:* By `p2_3` (inner-outer balance; Lemma 4.8 of `arXiv:2308.02978`), for an outer vertex $u \in O_i$ ($i \in I_{LL}$, so $P_u = \{(r, L), (s, L)\}$ has two $L$ inner neighbors), $u$ has $1$ outer neighbor sharing each of $(r,L), (s,L), (r,R), (s,R)$ and $2$ outer neighbors sharing each of the remaining $5$ $L$-vertices and $5$ $R$-vertices. Summing over all $7$ $L$-vertices and all $7$ $R$-vertices in $\Gamma_1(0)$, each $LL$ outer neighbor of $u$ contributes $2$ to the $L$-sum and $0$ to the $R$-sum; each $RR$ outer neighbor contributes $0$ to the $L$-sum and $2$ to the $R$-sum; and each $LR$ outer neighbor contributes $1$ to each:
     $$2 \sum_{j \in I_{LL}} b_{ij} + \sum_{j \in I_{LR}} b_{ij} = 2(1) + 5(2) = 12 \quad (\text{line 515, } \texttt{L\_ll == 12}),$$
     $$2 \sum_{j \in I_{RR}} b_{ij} + \sum_{j \in I_{LR}} b_{ij} = 2(1) + 5(2) = 12 \quad (\text{line 523, } \texttt{L\_rr == 12}).$$
     Subtracting these two equations yields $\sum_{j \in I_{LL}} b_{ij} = \sum_{j \in I_{RR}} b_{ij}$ for every row $i \in \{0..5\}$ (lines 469–476: encoded by negating the unary literals of $I_{RR}$; for $i \in I_{LL}$, $b_{ii}=0$ has $0$ literals so $I_{RR}$ has $3 \times 3 = 9$ negated literals, shifting the RHS to $9$; for $i \in I_{RR}$, $b_{ii}=0$ leaves $2 \times 3 = 6$ negated literals, shifting the RHS to $6$). Summing $\sum_{j \in I_{LL}} b_{ij} = \sum_{j \in I_{RR}} b_{ij}$ over $i \in I_{LL}$ and using $\sum_{i<j \in I_{LL}} 2 b_{ij} = \sum_{i \in I_{LL}, j \in I_{RR}} b_{ij}$ gives $\sum_{0 \le i < j < 3} 2 b_{ij} - \sum_{i \in I_{LL}, j \in I_{RR}} b_{ij} = 0$, encoded with $9 \times 3 = 27$ negated literals wait: $3 \times 3 = 9$ negated literals on lines 478–484 (`L_sll == 9`).
     By the same inner-outer balance applied to a vertex in $O_j$ for $j \in I_{LR}$ (which has one $L$ and one $R$ inner neighbor), its $L$-sum and $R$-sum both equal $12$, so $\sum_{i \in I_{LL}} b_{ij} = \sum_{i \in I_{RR}} b_{ij}$ for every column $j \in \{6..11\}$ (`L_col == 9`, lines 525–532).

5. **Outer row degree $12$ (`L_tot == 12`, line 490):**
   - *Derivation:* Every outer vertex $u \in \Gamma_2(0)$ has degree $14$, with $2$ neighbors in $\Gamma_1(0)$ and $12$ neighbors in $\Gamma_2(0)$, so $\sum_{j=0}^{11} b_{ij} = 12$.

6. **Diagonal 2-path identity (`L_diag == 5`, line 507) and linear row identity (`L_diff == 18`, line 498):**
   - *Derivation:* Fix $u \in O_i$ ($0 \le i < 6$). Because $b_{ii} = 0$, $u$ is non-adjacent to all $6$ other vertices $u' \in O_i \setminus \{u\}$, so by $\mu = 2$ there are $6 \times 2 = 12$ two-paths between $u$ and $O_i \setminus \{u\}$ in $\Gamma$. Each of the $2$ inner neighbors of $u$ lies in an inner $7$-cycle and is adjacent to $1$ other vertex of $O_i \setminus \{u\}$, accounting for $2$ of the $12$ two-paths. The remaining $10$ two-paths must pass through intermediate outer vertices $w \in \Gamma_2(0)$. An orbit $O_j$ ($j \ne i$) in which $u$ has $b_{ij}$ neighbors contributes $b_{ij}(b_{ij} - 1)$ ordered pairs of distinct neighbors of $u$ in $O_j$, each translating under $\mathbb{Z}_7$ to a two-path from $u$ to some $u' \in O_i \setminus \{u\}$. Hence:
     $$\sum_{j \ne i} b_{ij}(b_{ij} - 1) = 10 \iff \sum_{j \ne i} \binom{b_{ij}}{2} = 5.$$
     For $b_{ij} = u_0 + u_1 + u_2 \in \{0, 1, 2, 3\}$ with $u_0 \ge u_1 \ge u_2 \in \{0, 1\}$, one checks for all four values $b_{ij} \in \{0, 1, 2, 3\}$ that $\binom{b_{ij}}{2} = u_1 + 2 u_2$. Thus $\sum_{j \ne i} (u_1(i,j) + 2 u_2(i,j)) = 5$ (`L_diag == 5`, line 507).
     Subtracting $\sum_{j \ne i} (u_1(i,j) + 2 u_2(i,j)) = 5$ from the outer degree equation $\sum_{j \ne i} (u_0(i,j) + u_1(i,j) + u_2(i,j)) = 12$ yields the linear identity:
     $$\sum_{j \ne i} (u_0(i,j) - u_2(i,j)) = 12 - 5 = 7.$$
     Replacing each $-u_2(i,j)$ across the $11$ off-diagonal columns $j \ne i$ by $(1 - u_2(i,j))$ (the negated literal `-u_2`) adds $11$ to the RHS, giving $\sum_{j \ne i} (u_0(i,j) + (1 - u_2(i,j))) = 18$ (`L_diff == 18`, line 498).

7. **Column upper bounds for $j \in I_{LR} = \{6..11\}$ (`L_c_up <= 6`, `L_c_diag <= 5`, lines 534–544):**
   - *Derivation:* For any column $j \in I_{LR}$, the full column sum is $\sum_{i=0}^{11} b_{ij} = 12$. Since $b_{ij} \ge 0$ on the bottom $6$ rows $i \in I_{LR}$ and $\sum_{i \in I_{LL}} b_{ij} = \sum_{i \in I_{RR}} b_{ij}$ (by Item 4 above), we have $2 \sum_{i \in I_{LL}} b_{ij} \le 12 \implies \sum_{i=0}^{2} b_{ij} \le 6$ (`L_c_up <= 6`, line 537).
   - Likewise, the full column $j \in I_{LR}$ satisfies the diagonal 2-path identity $\sum_{i \in \{0..11\} \setminus \{j\}} (u_1(i,j) + 2 u_2(i,j)) = 5$. Restricting the sum of non-negative terms to the top $6$ rows $i \in \{0..5\}$ gives $\sum_{i=0}^{5} (u_1(i,j) + 2 u_2(i,j)) \le 5$ (`L_c_diag <= 5`, line 544).

8. **Off-diagonal 2-path equation for $0 \le i < j < 6$ (`verify.py` lines 546–563):**
   - *Derivation:* Fix $u \in O_i$ and consider the $7$ vertices of $O_j$ ($0 \le i < j < 6$). In $\Gamma$, $u$ has $b_{ij}$ adjacent vertices in $O_j$ (each sharing $\lambda = 1$ common neighbor with $u$) and $7 - b_{ij}$ non-adjacent vertices in $O_j$ (each sharing $\mu = 2$ common neighbors with $u$), so the total number of two-paths from $u$ to $O_j$ is $b_{ij} \cdot 1 + (7 - b_{ij}) \cdot 2 = 14 - b_{ij}$.
   - If $i, j$ are both in $I_{LL}$ or both in $I_{RR}$, each of the $2$ inner neighbors of $u$ is adjacent to $2$ vertices of $O_j$, contributing $4$ two-paths through $\Gamma_1(0)$; if $i \in I_{LL}$ and $j \in I_{RR}$, $u$ and $O_j$ share $0$ common neighbors in $\Gamma_1(0)$. Since $b_{ii} = b_{jj} = 0$, the two-paths through $\Gamma_2(0)$ are counted by $\sum_{k \notin \{i,j\}} b_{ik} b_{jk}$. Therefore:
     $$b_{ij} + \sum_{k \notin \{i,j\}} b_{ik} b_{jk} = \begin{cases} 10 & \text{if } (i, j \in I_{LL}) \text{ or } (i, j \in I_{RR}), \\ 14 & \text{if } i \in I_{LL} \text{ and } j \in I_{RR} \end{cases}$$
     (`rhs_ij = 14 if (i < 3 and j >= 3) else 10`, line 548).

---

### 4.2. Order-5 Automorphism `p5_t1_fix9` (`r4_mode = "p5_orbit_sym"`, `build_p5_t1_orbit_cnf` in `verify.py` lines 568–772)

Under $g \in \mathrm{Aut}(\Gamma)$ of order $5$ fixing $0$ and cycling the first $5$ inner edges ($i \in \{0..4\}$) while fixing inner edges $5$ and $6$ ($|\mathrm{Fix}(g)| = 9$), the $84$ outer vertices form $16$ orbits of size $5$ ($O_0, \dots, O_{15}$) and $4$ fixed outer vertices ($O_{16}, O_{17}, O_{18}, O_{19}$). `build_p5_t1_orbit_cnf` encodes the $20 \times 20$ orbit-valency matrix $B = (b_{ij})$ with the following constraints:
1. **Induced fixed subgraph $\mathrm{Fix}(g) \cong K_3 \square K_3$ on $O_{16}..O_{19}$ (lines 656–661):** Because every edge in $\mathrm{Fix}(g)$ has its unique triangle in $\mathrm{Fix}(g)$ and every non-adjacent pair of fixed vertices has both common neighbors fixed (since $5$ is odd and cannot partition $1$ or $2$ common neighbors into $5$-cycles), $\mathrm{Fix}(g)$ is an $\mathrm{srg}(9, 4, 1, 2) \cong K_3 \square K_3$, so the $4$ fixed outer vertices $O_{16}..O_{19}$ form the 4-cycle $(16,17), (16,18), (17,19), (18,19)$ (`p2_5`).
2. **Diagonal $b_{ii} = 0$ and off-diagonal $b_{ij} \le 2$ (lines 662–670):** By the same triangle/4-cycle argument on $5$-cycles, $b_{ii} = 0$ and $b_{ij} = u_1(i,j) + u_2(i,j) \in \{0, 1, 2\}$.
3. **Normalizer symmetry breaking (lines 684–702):** Lexicographic ordering of $b_{0,2} \ge b_{0,3}$ (Galois multiplier $\times 2 \bmod 5$), $L/R$ swap on the $5$-cycles ($b_{0,1} \ge b_{2,3}$), and $S_4$ ordering of the $4$ fixed outer columns $16..19$ on row $0$.
4. **Inner-outer degree balance $B C = R$ (lines 704–730):** Exact projection of `p2_3` onto the $20$ orbits (`add_eq(L, rhs)`).
5. **Diagonal 2-path identity (lines 732–735) and linear row identity (lines 737–745):** For a $5$-cycle $O_i$, counting two-paths from $u \in O_i$ to the other $4$ vertices of $O_i$ ($4 \times 2 = 8$ common neighbors, minus $2$ in $\Gamma_1(0)$ if $O_i$ is a $5$-cycle on one inner $5$-cycle, or $0$ if $O_i$ connects a $5$-cycle to a fixed inner vertex) gives $\sum_{j \ne i} b_{ij}(b_{ij} - 1) = 4 - \text{inner}_{ii} \iff \sum_{j \ne i} u_2(i,j) = (4 - \text{inner}_{ii})/2 \in \{1, 2\}$ (`rhs_diag`, line 733), and subtracting from $\sum_{j \ne i} (u_1 + u_2) = 12$ gives $\sum_{j \ne i} u_1(i,j) = 12 - \text{rhs\_diag}$ (line 739).
6. **Off-diagonal 2-path equation (lines 754–770):** Exact projection of `p2_4` between distinct orbits $O_i, O_j$.

---

### 4.3. Order-21 Frobenius Subgroup `frob21_z7_z3` (`r4_mode = "frob21_fig10"`, `verify.py` lines 1024–1042)

For $\mathrm{Frob}(21) = \mathbb{Z}_7 \rtimes \mathbb{Z}_3$, the $84$ outer vertices partition into $4$ orbits of size $21$: $LL$, $RR$, $LR$, and $RL$. In addition to the orbital `p2_3` and `p2_4` equations, lines 1024–1042 encode the orbit valencies derived in Proposition 4.10 / Figure 10 of Cesarz & Woldar (`arXiv:2308.02978`, p. 16):
- $LR$ and $RL$ are cocliques (`clauses.append([-pair_to_var[(p, q)]])` for $p < q$ in $LR$ or $RL$, lines 1035–1039), and
- Each vertex in $LL$ has $2$ neighbors in $LL$ and $2$ neighbors in $RR$, and each vertex in $RR$ has $2$ neighbors in $RR$ (`add_eq(L, 2)`, lines 1040–1042).

---

### 4.4. Prime $p = 3$ (`p3_t1_fix33`) and Prime $p = 2$ Involutions (`verify.py` lines 828–1022)

For `p3_t1_fix33` and the $18$ involution profiles $(a, b, c)$, `build_automorphism_cnf` uses the primary edge-orbit variables `pair_to_var[(p, q)]` on $\Gamma_2(0)$ ($0 \le p < q < 84$). Beyond the inner-outer balance (`p2_3`, lines 902–933) and outer-pair common-neighbor equation (`p2_4`, lines 946–1022), the modes add:

1. **Subset selection of outer-pair common-neighbor equations (`r4_mode`, lines 934–994):**
   - Since any unsatisfiable subset of the true $\mathrm{srg}(99, 14, 1, 2)$ equations suffices to certify UNSAT, `r4_mode` emits `p2_4` equations on:
     - `"none"` (`p3_t1_fix33`): `p2_3` alone is already UNSAT in 17 RUP steps.
     - `"conj"` (`(0,1,6)`): `p2_4` restricted to conjugate pairs $q = g(p)$.
     - `"conj_or_fix"` (10 profiles): `p2_4` restricted to pairs $(p, q)$ where $q = g(p)$ or both $p, q \in \mathrm{Fix}(g)$.
     - `"spectral_trace"` (`(0,5,2)`, `(0,6,1)`, `(1,4,1)`, `(1,5,0)`): `p2_4` restricted to pairs $(p, q)$ where $q = g(p)$ or $p \in \mathrm{Fix}(g)$ or $q \in \mathrm{Fix}(g)$.
     - `"global_triangle_bijection"` (`(2,2,1)`, `(2,3,0)`, `(3,0,1)`, `(3,1,0)`): `p2_3` plus the global flipped-edge and spectral trace constraints below (no `p2_4` clauses needed).

2. **Multiplicity / parity folding on `p2_3` and `p2_4` in `spectral_trace` (lines 909–927 and 1002–1020):**
   - *Derivation:* In an involution equation $\sum_{q} x_q = \text{rhs}$ where $\text{rhs} \in \{1, 2\}$, any orbital variable $v$ that appears in the sum with multiplicity $\text{cnt}(v) > \text{rhs}$ cannot be $1$ without exceeding $\text{rhs}$, so `clauses.append([-v])` (lines 915, 1008). The remaining variables partition into `L_odd` ($\text{cnt}(v) = 1$) and `L_even` ($\text{cnt}(v) = 2$), so $\sum_{v \in L_{\text{odd}}} v + 2 \sum_{w \in L_{\text{even}}} w = \text{rhs}$.
     - If $\text{rhs} = 1$: every $w \in L_{\text{even}}$ has $\text{cnt}(w) = 2 > 1$ (already falsified), leaving $\sum_{v \in L_{\text{odd}}} v = 1$ (`add_eq(L_odd, 1)`, lines 917, 1010).
     - If $\text{rhs} = 2$: introducing a single auxiliary bit $z \in \{0, 1\}$ (`z == 1` iff the sum comes from $L_{\text{even}}$), we have $\sum_{v \in L_{\text{odd}}} v + 2z = 2$ and $\sum_{w \in L_{\text{even}}} w + (1 - z) = 1$ (lines 924–927, 1017–1020).

3. **Normalizer symmetry breaking on the $b$ flipped inner edges in `spectral_trace` (lines 894–900):**
   - *Derivation:* For an involution with $b$ flipped inner edges $\{ (idx, L), (idx, R) \}$ ($2a \le idx < 2a + b$), the symmetric group $S_b$ permuting those $b$ flipped inner edges commutes with $g$. Selecting a fixed reference inner vertex `anchor` (`(6, L)` when $c \ge 1$, or `(0, L)` when $c = 0$), the $b$ conjugate outer-edge variables $e_{p(idx), g(p(idx))}$ where $p(idx) = \{(idx, L), \text{anchor}\}$ are permuted by $S_b$ (for $b$ or $b-1$ edges), so we break $S_b$ symmetry by ordering $e_{p(idx), g(p(idx))} \le e_{p(idx+1), g(p(idx+1))}$ (`clauses.append([-pair_to_var[(p1, q1)], pair_to_var[(p2, q2)]])`, line 900).

4. **Spectral trace identity for $p = 2$ involutions (`verify.py` lines 863–893):**
   - *Derivation:* Let $g \in \mathrm{Aut}(\Gamma)$ be an involution with inner profile $(a, b, c)$ ($2a + b + c = 7$), $k_2 = |\text{conj\_vars}| = (84 - |\mathrm{Fix}_{\text{outer}}(g)|)/2$ outer 2-cycles $\{p, g(p)\}$, and $\mathrm{Tr}(B) = \sum_{i=1}^{k_2} e_{p_i, g(p_i)}$ the number of $g$-transversal outer edges $\{p_i, g(p_i)\} \in E(\Gamma)$.
   - Since $g^2 = I$, $g$ has eigenvalues $+1$ and $-1$ on $V(\Gamma)$. On the adjacency eigenspaces $E_{14}$ ($\dim 1$), $E_3$ ($\dim 54$), and $E_{-4}$ ($\dim 44$), let $m_3(-1)$ and $m_{-4}(-1)$ be the multiplicities of the $-1$ eigenvalue of $g$ on $E_3$ and $E_{-4}$.
   - The total multiplicity of $-1$ for $g$ on $\mathbb{R}^{99}$ equals the number of 2-cycles of $g$ on $V(\Gamma)$: inside $\Gamma_1(0)$, $g$ has $2a + b = 7 - c + a$ 2-cycles; inside $\Gamma_2(0)$, $g$ has $k_2$ 2-cycles. Thus:
     $$m_3(-1) + m_{-4}(-1) = 7 - c + a + k_2.$$
   - Next, compute $\mathrm{Tr}(g A)$ in two ways:
     - **Combinatorially:** For any vertex $v \in V(\Gamma)$, $(g A)_{vv} = A_{v, g(v)}$, which is $1$ if $\{v, g(v)\} \in E(\Gamma)$ and $0$ otherwise. Inside $\{0\}$, $A_{0,0} = 0$. Inside $\Gamma_1(0)$, $\{u, g(u)\} \in E(\Gamma)$ iff $\{u, g(u)\}$ is one of the $b$ flipped inner edges, contributing $2b$ to $\mathrm{Tr}(g A)$. Inside $\Gamma_2(0)$, $\{p, g(p)\} \in E(\Gamma)$ iff $\{p, g(p)\}$ is one of the $\mathrm{Tr}(B)$ transversal outer edges, contributing $2\,\mathrm{Tr}(B)$ to $\mathrm{Tr}(g A)$. Hence:
       $$\mathrm{Tr}(g A) = 2b + 2\,\mathrm{Tr}(B).$$
     - **Spectrally:** On $E_{14}$, $g = +1$; on $E_3$, $\mathrm{Tr}(g|_{E_3}) = 54 - 2 m_3(-1)$; on $E_{-4}$, $\mathrm{Tr}(g|_{E_{-4}}) = 44 - 2 m_{-4}(-1)$. Thus:
       $$\mathrm{Tr}(g A) = 14(1) + 3(54 - 2 m_3(-1)) - 4(44 - 2 m_{-4}(-1)) = 14 + 162 - 176 - 6 m_3(-1) + 8 m_{-4}(-1) = -6 m_3(-1) + 8 m_{-4}(-1).$$
   - Equating the two expressions and dividing by $2$ gives:
     $$b + \mathrm{Tr}(B) = -3 m_3(-1) + 4 m_{-4}(-1) = -3 m_3(-1) + 4(7 - c + a + k_2 - m_3(-1)) = 28 - 4c + 4a + 4k_2 - 7 m_3(-1).$$
     Substituting $28 - 4c = 4(7 - c) = 4(2a + b) = 8a + 4b$ yields the exact **Involution Spectral Trace Identity**:
     $$\mathrm{Tr}(B) = 8a + 3b + 4k_2 - 7 m_3(-1) \implies (8a + 3b + 4k_2 - \mathrm{Tr}(B)) \equiv 0 \pmod{7}.$$
   - In `verify.py` (lines 863–874 and 882–893), `rhs_base = 8 * a + 3 * b + 4 * k2`, and `valid_tr` collects all integers $t$ in the allowed range satisfying `(rhs_base - t) % 7 == 0`. Writing $t_{\max} = \max(\text{valid\_tr})$ and introducing $M = (t_{\max} - \min(\text{valid\_tr})) / 7$ ordered unary variables $y_0 \ge y_1 \ge \dots \ge y_{M-1}$, the congruence $\mathrm{Tr}(B) \in \text{valid\_tr}$ is encoded as the linear cardinality equation:
     $$\sum_{v \in \text{conj\_vars}} v + 7 \sum_{r=0}^{M-1} y_r = t_{\max}.$$

5. **Fixed-inner-edge triangle window for $c = 1$ ($12 - 4a \le \mathrm{Tr}(B) \le 12 + 2a$, `verify.py` lines 880–881):**
   - *Derivation:* When $c = 1$, there is a unique fixed inner edge $\{6_L, 6_R\}$. Consider the $2a$ swapped inner edges $\{2r, 2r+1\}$ ($r = 0..a-1$) and $b$ flipped inner edges. Every transversal outer edge $e = \{p, g(p)\} \in E(\Gamma)$ ($p \ne g(p)$) lies in a unique triangle $\{p, g(p), z\}$ in $\Gamma$ ($\lambda = 1$). Since $g$ swaps $p \leftrightarrow g(p)$, $g$ must fix the third vertex $z$, so $z \in \mathrm{Fix}(g) \setminus \{0\}$.
   - For $c = 1$, $\mathrm{Fix}(g) \setminus \{0\}$ consists of the $2$ fixed inner vertices $6_L, 6_R$ and the $2a$ fixed outer vertices $z_r = \{(2r, s), (2r+1, s')\}$ ($s, s' \in \{L, R\}$ with $g(2r,s) = (2r+1,s')$).
   - Each fixed inner vertex $6_s$ ($s \in \{L, R\}$) has $12$ outer neighbors, namely $p = \{(i, t), (6, s)\}$ for $i \in \{0..5\}, t \in \{L, R\}$. Its $12$ outer neighbors form $6$ matched pairs in $\Gamma_1(6_s) \cong 7 K_2$ (excluding the inner edge $\{0, 6_s\}$). For the $b = 6 - 2a$ flipped inner edges $i \in \{2a..5\}$, $g$ swaps $\{(i, L), (6, s)\} \leftrightarrow \{(i, R), (6, s)\}$. At least $6 - 2a$ of the $6$ edges of $\Gamma_1(6_s)$ inside $\Gamma_2(0)$ must be $g$-invariant transversal edges (since each of the $2a$ non-flipped vertices in $\Gamma_1(6_s)$ can absorb at most one non-transversal matching edge), so $6_L$ and $6_R$ together contribute between $2(6 - 2a) = 12 - 4a$ and $12$ to $\mathrm{Tr}(B)$, while the $2a$ fixed outer vertices contribute at most $2a$ fixed-inner-neighbor triangles (and for $c=1$ in `spectral_trace`, where $a \in \{0, 1\}$, `t_min = 12 - 4*a` for $a=1$ and `0` for $a=0$, while `t_max_bound = 12 + 2*a`).

6. **Global flipped-edge triangle bijection (`r4_mode = "global_triangle_bijection"`, `verify.py` lines 828–861):**
   - *Derivation:* Let $e = \{p, g(p)\} \in E(\Gamma)$ be any of the $\mathrm{Tr}(B)$ transversal outer edges ($p \in \Gamma_2(0), p \ne g(p)$). By $\lambda = 1$, $e$ lies in a unique triangle $T(e) = \{p, g(p), z\}$ in $\Gamma$. Because $g$ swaps $p$ and $g(p)$, $g$ preserves $T(e)$ and therefore fixes the third vertex $z$: $g(z) = z$. Since $p, g(p) \in \Gamma_2(0)$, $z \ne 0$, so $z \in \mathrm{Fix}(g) \setminus \{0\}$.
   - Conversely, for any fixed vertex $z \in \mathrm{Fix}(g) \setminus \{0\}$, $g$ acts as an involution on the neighborhood $\Gamma_1(z) \cong 7 K_2$. Any edge $\{u, v\}$ of the matching $\Gamma_1(z)$ that is **flipped** by $g$ ($v = g(u) \ne u$) satisfies $u, g(u) \in \Gamma_2(0)$ (unless $z \in \Gamma_2(0)$ and $\{u, g(u)\} \subset \Gamma_1(0)$ is one of the $b$ flipped inner edges, wait: if $z = \{L_i, R_i\}$ were an outer vertex, $\{L_i, R_i\}$ cannot be an outer vertex because $\{L_i, R_i\}$ is a matched inner edge by `p2_2`! And if $z = \{u, g(u)\} \in \mathrm{Fix}_{\text{outer}}(g)$ has inner neighbors $u$ and $g(u)$, then $u$ and $g(u)$ are non-matched in $\Gamma_1(0)$, so $\{u, g(u)\} \notin E(\Gamma)$!). Therefore, **every** flipped edge $\{u, g(u)\}$ in $\Gamma_1(z)$ for **every** $z \in \mathrm{Fix}(g) \setminus \{0\}$ consists of two outer vertices $u, g(u) \in \Gamma_2(0)$!
   - Thus $e = \{p, g(p)\} \mapsto z$ is a bijection between the $\mathrm{Tr}(B)$ transversal outer edges and the disjoint union over all $z \in \mathrm{Fix}(g) \setminus \{0\}$ of the flipped edges in $\Gamma_1(z)$:
     $$\mathrm{Tr}(B) = \sum_{z \in \mathrm{Fix}(g) \setminus \{0\}} b_z,$$
     where $b_z$ denotes the number of $g$-flipped edges in $\Gamma_1(z) \cong 7 K_2$.
   - Now compute $b_z$ for every $z \in \mathrm{Fix}(g) \setminus \{0\}$:
     - Since $|\mathrm{Fix}(g)|$ is odd, every fixed vertex $z \in \mathrm{Fix}(g)$ has an even degree $d_{\text{fix}}(z)$ inside the induced fixed subgraph $\Gamma[\mathrm{Fix}(g)]$, paired into $c_z = d_{\text{fix}}(z)/2$ fixed edges in $\Gamma_1(z) \cong 7 K_2$.
     - The remaining $14 - 2c_z$ neighbors of $z$ lie in $\Gamma \setminus \mathrm{Fix}(g)$ and partition into $7 - c_z$ involution 2-cycles $\{u, g(u)\}$. Each 2-cycle $\{u, g(u)\} \subset \Gamma_1(z)$ is either a flipped edge of $\Gamma_1(z)$ ($b_z$ of them) or paired with another 2-cycle into a swapped pair of edges of $\Gamma_1(z)$ ($a_z$ pairs, accounting for $2a_z$ 2-cycles). Hence $2a_z + b_z + c_z = 7$, which implies:
       $$b_z \equiv 7 - c_z \pmod{2}, \quad 0 \le b_z \le 7 - c_z.$$
     - For the four profiles in `global_triangle_bijection` (`(2,2,1)`, `(2,3,0)`, `(3,0,1)`, `(3,1,0)`):
       - **Case `(3,0,1)` ($a=3, b=0, c=1$, $|\mathrm{Fix}(g)| = 9$):** Here $b = 0$. The $9$ fixed vertices are $\{0\}$, the $2$ fixed inner vertices $6_L, 6_R$, and the $6$ fixed outer vertices $z \in \mathrm{Fix}_{\text{outer}}(g)$ (which form the $6$ swapped inner pairs from the $a = 3$ swapped inner edges). Because $b = 0$, every vertex in $\mathrm{Fix}(g)$ has $d_{\text{fix}}(z) = 4$ ($c_z = 2$, inducing $\mathrm{Fix}(g) \cong K_3 \square K_3$), and for $6_L, 6_R$, their $10$ non-fixed outer neighbors have inner coordinates in the $a = 3$ swapped inner edges where $g$ acts fixed-point-freely on the edge labels, forcing $b_{6_L} = b_{6_R} = 0$, and likewise $b_z = 0$ for all $6$ fixed outer vertices. Thus $t_{\text{tri}} = \sum_{z \in \mathrm{Fix}(g) \setminus \{0\}} b_z = 0$ (line 833).
       - **Case `(2,2,1)` ($a=2, b=2, c=1$, $|\mathrm{Fix}(g)| = 7$):** The $6$ fixed vertices in $\mathrm{Fix}(g) \setminus \{0\}$ are $6_L, 6_R$ (with $c_{6_L} = c_{6_R} = 1$, $b_{6_L} + b_{6_R} = 8$) and $4$ fixed outer vertices (forming $1$ fixed outer edge with $c_z = 1$, so $3$ of them have $b_z = 1$ or $0$ and the parity/triangle sum gives $\mathrm{Tr}(B) \in \{8, 11\}$, encoded via $t_{\text{tri}} = 11$ and $1$ ternary slack variable $w_0 \in \{0, 1\}$ with weight $3$: $\mathrm{Tr}(B) + 3 w_0 = 11$, lines 835–838 and 858–861).
       - **Case `(2,3,0)` ($a=2, b=3, c=0$, $|\mathrm{Fix}(g)| = 5$):** Here $c = 0$, so $\mathrm{Fix}(g) \setminus \{0\}$ consists of $4$ fixed outer vertices. Each has $c_z \in \{0, 2\}$ ($b_z \in \{3, 5\}$), giving $\mathrm{Tr}(B) \in \{12, 15\}$, encoded via $t_{\text{tri}} = 15$ and $1$ ternary slack variable $w_0 \in \{0, 1\}$ with weight $3$: $\mathrm{Tr}(B) + 3 w_0 = 15$ (lines 839–842).
       - **Case `(3,1,0)` ($a=3, b=1, c=0$, $|\mathrm{Fix}(g)| = 7$):** Here $c = 0$, so $\mathrm{Fix}(g) \setminus \{0\}$ consists of $6$ fixed outer vertices, giving $\mathrm{Tr}(B) \in \{6, 9, 12\}$, encoded via $t_{\text{tri}} = 12$ and $2$ ordered ternary slack variables $w_0 \ge w_1 \in \{0, 1\}$ each of weight $3$: $\mathrm{Tr}(B) + 3 w_0 + 3 w_1 = 12$ (lines 843–847).

---

### 4.5. Step-by-Step Derivation of the 1-RUP-Step Proofs for `(0,6,1)` (`p2_a0_b6_c1_fix3`) and `(3,0,1)` (`p2_a3_b0_c1_fix9`)

Maintainers can inspect and re-derive the 1-RUP-step certificates for `(0,6,1)` and `(3,0,1)` directly from the generated CNF clauses in `verify.py` as follows:

#### A. How `(0,6,1)` (`p2_a0_b6_c1_fix3`) Follows in 1 RUP Step (`verify.py` lines 876–893 & 981–1010)
1. **Profile parameters:** $a = 0, b = 6, c = 1$. The involution $g$ fixes $0$, $6_L$, and $6_R$ ($|\mathrm{Fix}(g)| = 3$), and flips all $6$ remaining inner edges $(i, L) \leftrightarrow (i, R)$ for $i \in \{0..5\}$.
2. **Zero fixed outer vertices ($k_2 = 42$):** Because $a = 0$ and $c = 1$, **no outer vertex is fixed by $g$**: all $84$ outer vertices partition into $k_2 = 42$ involution 2-cycles $\{p_0, q_0\}$ with $q_0 = g(p_0) \ne p_0$.
3. **12 Conjugate Outer Edges Forced to `True` by `p2_4` Parity Folding (lines 981–1010):**
   - Consider the $12$ conjugate outer pairs $\{p_0, q_0\}$ where $p_0 = \{(i, L), (6, s)\}$ and $q_0 = g(p_0) = \{(i, R), (6, s)\}$ for $i \in \{0..5\}$ and $s \in \{L, R\}$. (In `verify.py`, their primary edge-orbit variable IDs are `742, 804, 1282, 1324, 1570, 1596, 1702, 1716, 1750, 1756, 1762, 1764`.)
   - Because $p_0$ and $q_0$ share the fixed inner vertex $(6, s)$, they have $s_{\text{inner}} = |P_{p_0} \cap P_{q_0}| = 1$ common inner neighbor, so the `p2_4` outer-pair common-neighbor equation (line 996) has $\text{rhs} = 2 - 1 = 1$:
     $$e_{p_0, q_0} + \sum_{r \in \Gamma_2(0) \setminus \{p_0, q_0\}} (e_{p_0, r} \wedge e_{q_0, r}) = 1.$$
   - Because **every** outer vertex $r \notin \{p_0, q_0\}$ lies in a 2-cycle $\{r, g(r)\}$ ($r \ne g(r)$) and $g$ swaps $p_0 \leftrightarrow q_0$, the unordered pair of edge-orbits $\{\{p_0, r\}, \{q_0, r\}\}$ is identical to $\{\{q_0, g(r)\}, \{p_0, g(r)\}\}$. Consequently, in the list `L` (lines 997–1001), **every** auxiliary conjunction variable $c_r = \text{get\_and\_var}(e_{p_0, r}, e_{q_0, r})$ appears with multiplicity $\text{cnt}(c_r) = 2$, whereas $e_{p_0, q_0}$ appears with multiplicity $\text{cnt}(e_{p_0, q_0}) = 1$!
   - Therefore `L_odd = [e_{p_0, q_0}]` is a singleton, and `add_eq(L_odd, 1)` (line 1010) emits the unit/implication clauses (clauses 1–24 of `p2_a0_b6_c1_fix3_encA_core.cnf` and `encB_core.cnf`) forcing $e_{p_0, q_0} = 1$ for all $12$ pairs (`742..1764`).
4. **Conflict with the Spectral Trace Cardinality Counter in 1 RUP Step (lines 880–893):**
   - For $(0, 6, 1)$, $t_{\min} = 0$, $t_{\max,\text{bound}} = 12 + 2a = 12$, and $\text{rhs\_base} = 8a + 3b + 4k_2 = 0 + 18 + 168 = 186$.
   - The valid trace values in $[0, 12]$ satisfying $(186 - t) \equiv 0 \pmod{7}$ are `valid_tr = [4, 11]`, so $t_{\max} = 11$ and $M = 1$.
   - Line 893 encodes `add_eq(conj_vars + [y_0]*7, 11)`, whose cardinality counter (clauses 25–56 in Encoding A; clauses 25–44 in Encoding B) enforces $\sum_{v \in \text{conj\_vars}} v \le 11$.
   - Propagating the $12$ forced unit variables (`742..1764`) through the $\le 11$ cardinality counter produces an immediate unit-propagation conflict in **1 RUP step** (`57 0 1 2 ... 56 0` in `p2_a0_b6_c1_fix3_encA_core.lrat`; `45 0 1 2 ... 44 0` in `p2_a0_b6_c1_fix3_encB_core.lrat`).

#### B. How `(3,0,1)` (`p2_a3_b0_c1_fix9`) Follows in 1 RUP Step (`verify.py` lines 828–874)
1. **Profile parameters:** $a = 3, b = 0, c = 1$. The involution $g$ fixes $9$ vertices ($0$, $6_L, 6_R$, and $6$ outer vertices), and the remaining $78$ outer vertices form $k_2 = 39$ involution 2-cycles (`len(conj_vars) == 39`).
2. **All 39 Diagonal Variables Forced to `False` (`0`) by `t_tri = 0` (lines 832–850):**
   - Because $b = 0$, there are no flipped inner edges and $t_{\text{tri}} = \sum_{z \in \mathrm{Fix}(g) \setminus \{0\}} b_z = 0$ (line 833).
   - Line 850 calls `add_eq(list(conj_vars), 0)`, which emits the $39$ unit clauses `[-v]` for all $v \in \text{conj\_vars}$ (forcing $\mathrm{Tr}(B) = 0$).
3. **Conflict with the Spectral Trace Cardinality Counter in 1 RUP Step (lines 863–874):**
   - For $(3, 0, 1)$ with $k_2 = 39$, $\text{rhs\_base} = 8a + 3b + 4k_2 = 24 + 0 + 156 = 180$.
   - Since $180 \equiv 5 \pmod{7}$, the valid trace values in $[0, 39]$ satisfying $(180 - t) \equiv 0 \pmod{7}$ are `valid_tr = [5, 12, 19, 26, 33]`, with $t_{\max} = 33$ and $M = (33 - 5)/7 = 4$ auxiliary variables $y_0, y_1, y_2, y_3$.
   - Line 874 calls `add_eq(L_trace, 33)` where `L_trace = conj_vars + [y_0]*7 + [y_1]*7 + [y_2]*7 + [y_3]*7` (total length $39 + 28 = 67$).
   - Because all $39$ variables in `conj_vars` are falsified by unit clauses `[-v]`, at most $28$ literals in `L_trace` (`[y_0]*7 + ... + [y_3]*7`) can be true, which is strictly less than the required target $33$. Unit propagation through the cardinality counter for `add_eq(L_trace, 33)` reaches a conflict in **1 RUP step** (`p2_a3_b0_c1_fix9_encA_core.lrat` and `p2_a3_b0_c1_fix9_encB_core.lrat`).
