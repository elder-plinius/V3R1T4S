# Technical Methodology & Complete Variable-to-Meaning Map for Track `p2` (`conway-99-graph`)

## 1. Overview of Track `p2` and the Two Independent Cardinality Encodings

Conway's 99-graph problem asks whether there exists a strongly regular graph $\Gamma = \mathrm{srg}(99, 14, 1, 2)$: a 99-vertex regular graph of degree $k = 14$ in which every adjacent pair of vertices shares $\lambda = 1$ common neighbor and every non-adjacent pair shares $\mu = 2$ common neighbors.

In Section 2.3 (*A Forced-Structure Reduction*, pp. 2–4) of `arXiv:2608.11211v2`, Aalok Thakkar and Simone Severini fix a root vertex $0 \in V(\Gamma)$, partition $V(\Gamma) = \{0\} \cup \Gamma_1(0) \cup \Gamma_2(0)$ with $|\Gamma_1(0)| = 14$ and $|\Gamma_2(0)| = 84$, and reduce the $\mathrm{srg}(99, 14, 1, 2)$ axioms to five propositions (`p2_1` through `p2_5`).

This package re-derives all five propositions across **two independent SAT cardinality encodings** and certifies each refutation as a **Pure-RUP LRAT proof (`0` RAT steps)**:

1. **Encoding A (`Sinz_2005_Sequential_Counter`, `add_exact_sinz` in `verify.py` lines 34–62):**
   Given a list of $n$ literals $L = [L_0, \dots, L_{n-1}]$ and a target sum $k \ge 1$, Sinz's (2005) linear sequential counter allocates $n \cdot k$ register variables $s_{i,j} = \text{next\_var} + i \cdot k + j$ for $0 \le i < n$ and $0 \le j < k$, where $s_{i,j}$ represents the partial-sum predicate $\sum_{r=0}^i L_r \ge j + 1$. It emits:
   - Base clauses ($i = 0$): $(\neg L_0 \vee s_{0,0})$, $(L_0 \vee \neg s_{0,0})$, and $\neg s_{0,j}$ for $1 \le j < k$.
   - Inductive step clauses ($1 \le i < n$):
     - For $j = 0$: $(\neg s_{i-1,0} \vee s_{i,0})$, $(\neg L_i \vee s_{i,0})$, and $(s_{i-1,0} \vee L_i \vee \neg s_{i,0})$.
     - For $1 \le j < k$: $(\neg s_{i-1,j} \vee s_{i,j})$, $(\neg s_{i-1,j-1} \vee \neg L_i \vee s_{i,j})$, $(s_{i-1,j} \vee s_{i-1,j-1} \vee \neg s_{i,j})$, and $(s_{i-1,j} \vee L_i \vee \neg s_{i,j})$.
     - Overflow clause: $(\neg s_{i-1,k-1} \vee \neg L_i)$.
   - Final target clause: $(s_{n-1,k-1})$.
   (When $k = 0$, it emits unit clauses $(\neg L_i)$ for all $L_i \in L$ without allocating new variables.)

2. **Encoding B (`Bailleux_Boufkhad_2003_Binary_Tree_Totalizer`, `add_exact_totalizer` in `verify.py` lines 65–113):**
   Given $L = [L_0, \dots, L_{n-1}]$ and $k \ge 1$, Bailleux & Boufkhad's (2003) binary tree unary totalizer recursively splits any slice `items` of length $m > 1$ at `mid = m // 2` into `left = items[:mid]` and `right = items[mid:]` (leaves of length $1$ return `[items[0]]` directly without allocating new variables). In post-order (left subtree, then right subtree, then parent), each internal node allocates $w = \min(k, |\text{left}| + |\text{right}|)$ unary output variables $\text{out}[0 \dots w-1]$, where $\text{out}[c-1]$ represents $\text{sum}(\text{items}) \ge c$, and emits:
   - Upward sum/overflow clauses for $0 \le a \le |\text{left}|, 0 \le b \le |\text{right}|$ with $a + b \ge 1$:
     - If $a + b \le k$: $(\neg \text{left}[a-1] \vee \neg \text{right}[b-1] \vee \text{out}[a+b-1])$ (omitting $\neg \text{left}[a-1]$ if $a=0$, or $\neg \text{right}[b-1]$ if $b=0$).
     - If $a + b > k$: the overflow clause $(\neg \text{left}[a-1] \vee \neg \text{right}[b-1])$.
   - Downward witness clauses for $1 \le c \le w$ and $0 \le a < c, b = c - 1 - a$:
     $(\neg \text{out}[c-1] \vee \text{left}[a] \vee \text{right}[b])$ (omitting $\text{left}[a]$ if $a = |\text{left}|$, or $\text{right}[b]$ if $b = |\text{right}|$).
   - Root target unit clause: $(\text{root}[k-1])$.

---

## 2. Summary of the 10 Shipped Track `p2` Certificates

| Proposition ID | Section 2.3 Statement in `arXiv:2608.11211` | Enc A Full Vars / Clauses | Enc A Core Clauses | Enc A RUP Lemmas | Enc B Full Vars / Clauses | Enc B Core Clauses | Enc B RUP Lemmas | RAT Lemmas |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `p2_1_inner_matching_k14` | $\Gamma_1(0) \cong 7 K_2$ (1-regular of order $k=14$ under $\lambda = 1$) | 273 / 716 | 4 | 1 | 259 / 688 | 4 | 1 | 0 |
| `p2_2_outer_bijection_k14` | Bijection $\Gamma_2(0) \leftrightarrow 84$ non-matched pairs $\{a,b\} \subset \Gamma_1(0)$ (Constraint 1) | 1,598 / 1,578 | 13 | 3 | 1,585 / 1,576 | 12 | 3 | 0 |
| `p2_3_inner_outer_balance_k14` | Inner-outer degree balance $\in \{1, 2\}$ (Constraint 4) | 548 / 2,733 | 2,487 | 836 | 522 / 2,717 | 2,483 | 780 | 0 |
| `p2_4_outer_pair_cn_k14` | Outer pair common-neighbor equation $E(u,v) + \mathrm{cn}_{\Gamma_2(0)}(u,v) = 2 - |P_u \cap P_v|$ (Constraints 2 & 3) | 91 / 407 | 345 | 142 | 87 / 407 | 342 | 111 | 0 |
| `p2_5_srg9_uniqueness` | Uniqueness of reduced outer graph on $\mathrm{srg}(9, 4, 1, 2) \cong K_3 \square K_3$ | 66 / 201 | 13 | 1 | 42 / 147 | 7 | 1 | 0 |
| **Total (`p2`)** | **5 Propositions (10 Pure-RUP LRAT Certificates)** | — | **2,862** | **983** | — | **2,848** | **896** | **0** |

---

## 3. Complete Variable-to-Meaning Mapping and Re-Derivation Guide for `p2_1` through `p2_5`

This section maps **every DIMACS variable ID** appearing in the 10 shipped core files (`object/proofs/p2_*_core.cnf`) and in the full generated formulas to its mathematical meaning in $\mathrm{srg}(99, 14, 1, 2)$, cites the corresponding statement of `arXiv:2608.11211` Section 2.3, and shows how each core is derived and refuted without running `verify.py`.

---

### 3.1. `p2_1_inner_matching_k14` (`verify.py` lines 134–149)

- **Statement in `arXiv:2608.11211` Section 2.3 (p. 2, paragraph 2):**
  Fix vertex $0 \in V(\Gamma)$ with neighborhood $\Gamma_1(0) = \{0, 1, \dots, 13\}$ ($k = 14$). Because every edge $\{0, a\}$ ($a \in \Gamma_1(0)$) has $\lambda = 1$ common neighbor in $\Gamma$, every vertex $a \in \Gamma_1(0)$ has degree exactly $1$ inside the induced subgraph $\Gamma[\Gamma_1(0)]$. Consequently, $\Gamma[\Gamma_1(0)]$ is a $1$-regular matching $M_0 \cong 7 K_2$ (no vertex $a \in \Gamma_1(0)$ can be adjacent to two distinct vertices $b_1, b_2 \in \Gamma_1(0)$).

- **Full Formula Variable Map (`273` vars / `716` clauses in Encoding A; `259` vars / `688` clauses in Encoding B):**
  1. **Variables `1..91` (Primary inner-edge variables $e_{a,b}$ for $0 \le a < b < 14$):**
     Enumerated in lexicographic order of $(a, b)$:
     - For $a = 0$: `var 1` $= e_{0,1}$, `var 2` $= e_{0,2}$, `var 3` $= e_{0,3}$, ..., `var 13` $= e_{0,13}$.
     - In general, for $0 \le a < b < 14$, $\text{pair\_var}(a, b) = \sum_{r=0}^{a-1} (13 - r) + (b - a)$.
  2. **Cardinality constraints ($\sum_{b \ne a} e_{a,b} = 1$ for each $a \in \{0, \dots, 13\}$):**
     For $a = 0$, the input list of $13$ incident inner edges is $L^{(0)} = [1, 2, 3, \dots, 13]$ and $k = 1$, starting at `next_var = 92`:
     - **In Encoding A (`Sinz_2005_Sequential_Counter`):** Allocates $13 \times 1 = 13$ prefix-sum register variables per vertex $a \in \{0..13\}$ ($14 \times 13 = 182$ auxiliary variables `92..273`, giving $91 + 182 = 273$ total variables). For $a = 0$, the registers are `92..104`, where **`var 92`** $= s_{0,0}^{(0)} \iff (e_{0,1} \ge 1) \iff e_{0,1}$.
     - **In Encoding B (`Bailleux_Boufkhad_2003_Binary_Tree_Totalizer`):** Recursively bisects the $13$-element list $L^{(a)}$ into a binary tree with $12$ internal nodes per vertex $a \in \{0..13\}$ ($14 \times 12 = 168$ auxiliary variables `92..259`, giving $91 + 168 = 259$ total variables). For $a = 0$, post-order traversal bisects $L^{(0)} = [1..13] \to [1..6] \to [1, 2, 3] \to \text{leaf } [1]$ and subtree $[2, 3] \to \text{leaf } [2]$ and $\text{leaf } [3]$. Thus the **very first internal node allocated** (`next_var = 92`) merges leaves `[2]` and `[3]`, so **`var 92`** $= t_{\{2,3\}, 1}^{(0)} \iff (e_{0,2} \vee e_{0,3})$.
  3. **Negation of the proposition (two distinct inner neighbors of $a = 0$):**
     Unit clauses `(1)` ($e_{0,1} = 1$) and `(2)` ($e_{0,2} = 1$).

- **Variable Map & Clauses of the Shipped Cores (`p2_1_inner_matching_k14_encA_core.cnf` and `encB_core.cnf`):**

| Variable ID | Meaning in Encoding A (`p2_1_..._encA_core.cnf`) | Meaning in Encoding B (`p2_1_..._encB_core.cnf`) |
| :---: | :--- | :--- |
| `1` | Primary edge $e_{0,1} \in E(\Gamma_1(0))$ | Primary edge $e_{0,1} \in E(\Gamma_1(0))$ |
| `2` | Primary edge $e_{0,2} \in E(\Gamma_1(0))$ | Primary edge $e_{0,2} \in E(\Gamma_1(0))$ |
| `92` | Sinz prefix register $s_{0,0}^{(0)} \iff e_{0,1}$ (partial sum of $L^{(0)}[0..0] = [e_{0,1}]$ is $\ge 1$) | Totalizer internal subtree bit $t_{\{2,3\},1}^{(0)} \iff (e_{0,2} \vee e_{0,3})$ (first post-order internal node merging leaves $e_{0,2}$ and $e_{0,3}$) |

- **Why the two `p2_1` cores are the same four clauses up to the sign of `var 92`, and what makes the encodings independent:**
  - In the **full generated formulas**, Encoding A (`273` variables, `716` clauses, linear chain of $13$ prefix registers per vertex) and Encoding B (`259` variables, `688` clauses, balanced binary tree of $12$ internal nodes per vertex) have completely different topologies.
  - Because the negated hypothesis asserts $e_{0,1} = 1$ (`var 1`) and $e_{0,2} = 1$ (`var 2`), refuting $\sum_{b=1}^{13} e_{0,b} = 1$ only requires the pairwise at-most-$1$ interaction between $e_{0,1}$ and $e_{0,2}$, which in both encodings is mediated by the first allocated auxiliary variable `var 92`—but with **opposite structural semantics**:
    - In **Encoding A (Sinz Sequential Counter)**:
      - Base clause (`verify.py` line 50): `92 -1 0` ($e_{0,1} \implies s_{0,0}^{(0)}$, i.e. `var 1 -> var 92`).
      - Step $i = 1$ overflow clause (`verify.py` line 64): `-92 -2 0` ($\neg s_{0,0}^{(0)} \vee \neg e_{0,2}$, i.e. if the prefix sum after $e_{0,1}$ is already $\ge 1$, then $e_{0,2}$ cannot be $1$).
      - Shipped Encoding A core (`4` clauses) & LRAT (`1` RUP step):
        ```text
        c1: 1 0
        c2: 2 0
        c3: 92 -1 0
        c4: -92 -2 0
        lrat: 5 0 1 2 3 4 0
        ```
    - In **Encoding B (Bailleux–Boufkhad Binary Tree Totalizer)**:
      - At the first post-order internal node `var 92` merging leaf `left = [2]` ($e_{0,2}$) and leaf `right = [3]` ($e_{0,3}$), the upward sum clause for $a = 1, b = 0$ (`verify.py` line 101) is `92 -2 0` ($e_{0,2} \implies t_{\{2,3\},1}^{(0)}$, i.e. `var 2 -> var 92`).
      - At the parent internal node merging leaf `left = [1]` ($e_{0,1}$) with `right = [92]` ($t_{\{2,3\},1}^{(0)}$), the upward overflow clause for $a = 1, b = 1 > k = 1$ (`verify.py` line 99) is `-92 -1 0` ($\neg e_{0,1} \vee \neg t_{\{2,3\},1}^{(0)}$).
      - Shipped Encoding B core (`4` clauses) & LRAT (`1` RUP step):
        ```text
        c1: 1 0
        c2: 2 0
        c3: -92 -1 0
        c4: 92 -2 0
        lrat: 5 0 1 2 3 4 0
        ```
  - Thus, `var 92` is $e_{0,1}$ in Encoding A's linear prefix chain (`1 -> 92`, `92 -> -2`) and $e_{0,2} \vee e_{0,3}$ in Encoding B's binary totalizer tree (`2 -> 92`, `92 -> -1`). Formally substituting $92 \mapsto \neg 92$ interchanges the two 4-clause cores because a 2-variable at-most-$1$ path of length 2 ($1 \to 92 \to \neg 2$ vs. $2 \to 92 \to \neg 1$) is reversed by negating the intermediate literal.

---

### 3.2. `p2_2_outer_bijection_k14` (`verify.py` lines 152–195)

- **Statement in `arXiv:2608.11211` Section 2.3 (p. 2, paragraph 3 & Constraint 1):**
  Each of the $M = k(k-2)/2 = 84$ outer vertices $u \in \Gamma_2(0)$ ($u \in \{0, \dots, 83\}$) is non-adjacent to $0$ ($\mu = 2$) and therefore has exactly $2$ neighbors in $\Gamma_1(0)$, denoted $P_u \subset \Gamma_1(0)$ ($|P_u| = 2$).
  - **(a) Matched inner pairs excluded ($\lambda = 1$):** If $P_u = \{0, 1\}$ were a matched edge of $M_0$, then $\{0, 1\}$ would have two common neighbors ($0$ and $u$), violating $\lambda = 1$; thus $0$ outer vertices have $\{0, 1\} \subset P_u$.
  - **(b) Distinct outer vertices have distinct non-matched pairs ($\mu = 2$):** For any non-matched pair $\{0, 2\} \subset \Gamma_1(0)$, vertices $0$ and $2$ already share root vertex $0$ as a common neighbor, so by $\mu = 2$ they share **exactly $1$** common neighbor in $\Gamma_2(0)$; thus no two distinct outer vertices $u=0, u=1$ can both have $\{0, 2\} \subset P_u$.

- **Full Formula Variable Map (`1,598` vars / `1,578` clauses in Encoding A; `1,585` vars / `1,576` clauses in Encoding B):**
  1. **Variables `1..1176` (Inner-outer incidence variables $b_{u,a}$ for $u \in \{0..83\}, a \in \{0..13\}$):**
     $\text{b\_var}(u, a) = 14 u + a + 1$ represents $a \in P_u$ (outer vertex $u$ is adjacent to inner vertex $a$).
     In particular:
     - For outer vertex $u = 0$: `var 1` $= b_{0,0}$, `var 2` $= b_{0,1}$, `var 3` $= b_{0,2}$ (`1..14`).
     - For outer vertex $u = 1$: `var 15` $= b_{1,0}$, `var 16` $= b_{1,1}$, `var 17` $= b_{1,2}$ (`15..28`).
  2. **Outer degree-into-$\Gamma_1(0)$ constraints ($\sum_{a=0}^{13} b_{u,a} = 2$ for $u \in \{0..5\}$):**
     - **Encoding A:** Allocates $6 \times (14 \times 2) = 168$ Sinz register variables `1177..1344`.
     - **Encoding B:** Allocates $6 \times (13 \times 2) = 156$ Totalizer internal tree variables `1177..1332`.
  3. **Conjunction variables $\text{and\_01}[u] \iff (b_{u,0} \wedge b_{u,1})$ for $u \in \{0..83\}$ ($84$ variables) and $\sum_{u=0}^{83} \text{and\_01}[u] = 0$:**
     - **Encoding A:** Variables `1345..1428` (where **`var 1345`** $= b_{0,0} \wedge b_{0,1}$); `add_exact_sinz(and_01, 0)` emits unit clauses `(-1345)`, ..., `(-1428)`.
     - **Encoding B:** Variables `1333..1416` (where **`var 1333`** $= b_{0,0} \wedge b_{0,1}$); `add_exact_totalizer(and_01, 0)` emits unit clauses `(-1333)`, ..., `(-1416)`.
  4. **Conjunction variables $\text{and\_02}[u] \iff (b_{u,0} \wedge b_{u,2})$ for $u \in \{0..83\}$ ($84$ variables) and $\sum_{u=0}^{83} \text{and\_02}[u] = 1$:**
     - **Encoding A:** Variables `1429..1512` (where **`var 1429`** $= b_{0,0} \wedge b_{0,2}$ and **`var 1430`** $= b_{1,0} \wedge b_{1,2}$), followed by $84 \times 1 = 84$ Sinz prefix registers `1513..1596` (where **`var 1513`** $= s_{0,0} \iff \text{and\_02}[0]$).
     - **Encoding B:** Variables `1417..1500` (where **`var 1417`** $= b_{0,0} \wedge b_{0,2}$ and **`var 1418`** $= b_{1,0} \wedge b_{1,2}$), followed by $83$ Totalizer internal tree variables `1501..1583`. Because post-order bisection of the $84$-element list `and_02[0..83]` (`84 -> 42 -> 21 -> 10 -> 5 -> 2`) pairs the first two leaves `1417` and `1418` at an internal node with $k = 1$, line 99 ($a = 1, b = 1 > k = 1$) directly emits the binary overflow clause `-1418 -1417 0` without needing an intermediate variable in the core!
  5. **Disjunctive violation selectors $z_1, z_2$ (`z1 V z2`):**
     - **Encoding A:** **`var 1597`** $= z_1$ (violates (a): $z_1 \implies b_{0,0} \wedge b_{0,1}$) and **`var 1598`** $= z_2$ (violates (b): $z_2 \implies b_{0,0} \wedge b_{0,2} \wedge b_{1,0} \wedge b_{1,2}$).
     - **Encoding B:** **`var 1584`** $= z_1$ and **`var 1585`** $= z_2$.

- **Variable Map of the Shipped Cores (`p2_2_outer_bijection_k14_encA_core.cnf` and `encB_core.cnf`):**

| Enc A Var | Enc B Var | Mathematical Meaning |
| :---: | :---: | :--- |
| `1` | `1` | $b_{0,0}$: outer vertex $u=0$ is adjacent to inner vertex $a=0$ |
| `2` | `2` | $b_{0,1}$: outer vertex $u=0$ is adjacent to inner vertex $a=1$ (matched partner of $a=0$) |
| `3` | `3` | $b_{0,2}$: outer vertex $u=0$ is adjacent to inner vertex $a=2$ (non-matched with $a=0$) |
| `15` | `15` | $b_{1,0}$: outer vertex $u=1$ is adjacent to inner vertex $a=0$ |
| `17` | `17` | $b_{1,2}$: outer vertex $u=1$ is adjacent to inner vertex $a=2$ |
| `1345` | `1333` | $\text{and\_01}[0] \iff (b_{0,0} \wedge b_{0,1})$: outer vertex $u=0$ contains matched inner pair $\{0, 1\}$ |
| `1429` | `1417` | $\text{and\_02}[0] \iff (b_{0,0} \wedge b_{0,2})$: outer vertex $u=0$ contains non-matched pair $\{0, 2\}$ |
| `1430` | `1418` | $\text{and\_02}[1] \iff (b_{1,0} \wedge b_{1,2})$: outer vertex $u=1$ contains non-matched pair $\{0, 2\}$ |
| `1513` | *(none)* | Sinz prefix register $s_{0,0} \iff \text{and\_02}[0]$ (in Enc B, the leaf-pair merge of `1417` and `1418` directly emits `-1418 -1417 0`) |
| `1597` | `1584` | Violation selector $z_1$: asserts $b_{0,0} = 1$ and $b_{0,1} = 1$ |
| `1598` | `1585` | Violation selector $z_2$: asserts $b_{0,0} = b_{0,2} = b_{1,0} = b_{1,2} = 1$ |

- **Complete Clauses & 3-Step LRAT Refutations of Both `p2_2` Cores:**
  - **Encoding A (`13` core clauses, `3` RUP lemmas):**
    - Clauses `c1..c13`: `c1: 1597 1598 0` ($z_1 \vee z_2$), `c2: -1345 0` ($\neg \text{and\_01}[0]$), `c3: -1 -2 1345 0` ($b_{0,0} \wedge b_{0,1} \implies \text{and\_01}[0]$), `c4: -1598 1 0` ($z_2 \implies b_{0,0}$), `c5: -1597 1 0` ($z_1 \implies b_{0,0}$), `c6: 2 -1597 0` ($z_1 \implies b_{0,1}$), `c7: 3 -1598 0` ($z_2 \implies b_{0,2}$), `c8: 15 -1598 0` ($z_2 \implies b_{1,0}$), `c9: 17 -1598 0` ($z_2 \implies b_{1,2}$), `c10: 1429 -3 -1 0` ($b_{0,0} \wedge b_{0,2} \implies \text{and\_02}[0]$), `c11: 1430 -17 -15 0` ($b_{1,0} \wedge b_{1,2} \implies \text{and\_02}[1]$), `c12: 1513 -1429 0` ($\text{and\_02}[0] \implies s_{0,0}$), `c13: -1513 -1430 0` ($\neg s_{0,0} \vee \neg \text{and\_02}[1]$).
    - LRAT steps:
      - Step `14`: `-2 -1 0` (hints `2 3`: from $\neg \text{and\_01}[0]$ and $b_{0,0} \wedge b_{0,1} \implies \text{and\_01}[0]$, derive $\neg b_{0,0} \vee \neg b_{0,1}$).
      - Step `15`: `1 0` (hints `4 1 5`: since both $z_1$ and $z_2$ imply $b_{0,0}$ and $z_1 \vee z_2$, derive $b_{0,0}$).
      - Step `16`: `0` (hints `15 14 6 1 7 8 9 10 11 12 13`: $b_{0,0}$ and $\neg b_{0,0} \vee \neg b_{0,1}$ give $\neg b_{0,1} \implies \neg z_1 \implies z_2 \implies b_{0,2}, b_{1,0}, b_{1,2} \implies \text{and\_02}[0], \text{and\_02}[1] \implies s_{0,0}$ and $\neg s_{0,0}$, conflict!).
  - **Encoding B (`12` core clauses, `3` RUP lemmas):**
    - Identical 3-step RUP refutation (`13: -2 -1 0`, `14: 1 0`, `15: 0`), with `c12: -1418 -1417 0` directly refuting $\text{and\_02}[0] \wedge \text{and\_02}[1]$ from the Totalizer leaf pair `[1417, 1418]`.

---

### 3.3. `p2_3_inner_outer_balance_k14` (`verify.py` lines 198–230)

- **Statement in `arXiv:2608.11211` Section 2.3 (Constraint 4, p. 3; also Lemma 4.8 of `arXiv:2308.02978`):**
  Fix an outer vertex $u \in \Gamma_2(0)$ with non-matched inner-neighbor pair $P_u = \{0, 2\} \subset \Gamma_1(0)$, where the $7$ matched inner edges of $M_0$ are $\{2r, 2r+1\}$ for $r \in \{0..6\}$ (so the matched partner of $a \in \{0..13\}$ is $m(a) = a \oplus 1$).
  For each inner vertex $a \in \{0, \dots, 13\}$:
  - By the $\mathrm{srg}(99, 14, 1, 2)$ condition between $u$ and $a$, the total number of common neighbors of $u$ and $a$ in $\Gamma$ is $\mathrm{cn}_\Gamma(u, a) = \lambda = 1$ if $a \in P_u$ ($a \in \{0, 2\}$), and $\mathrm{cn}_\Gamma(u, a) = \mu = 2$ if $a \notin P_u$.
  - Every neighbor of $a$ in $\Gamma$ is either the root $0$ (which is not adjacent to $u \in \Gamma_2(0)$), its unique inner partner $m(a) \in \Gamma_1(0)$ (which is adjacent to $u$ iff $m(a) \in P_u$), or one of the $k - 2 = 12$ outer neighbors $w_0, \dots, w_{11} \in \Gamma_2(0) \cap N(a)$ of $a$.
  - Therefore:
    $$\mathbf{1}_{m(a) \in P_u} + \sum_{j=0}^{11} E(u, w_j) = \begin{cases} 1 & \text{if } a \in P_u \text{ ($a \in \{0, 2\}$)}, \\ 2 & \text{if } a \notin P_u \text{ ($a \in \{1, 3, 4, \dots, 13\}$)}. \end{cases}$$
    Since $P_u = \{0, 2\}$ is non-matched, $a \in P_u \implies m(a) \notin P_u$ ($\mathbf{1}_{m(a) \in P_u} = 0$), whereas $m(a) \in P_u \iff a \in \{1, 3\}$ ($\mathbf{1}_{m(a) \in P_u} = 1$). Subtracting $\mathbf{1}_{m(a) \in P_u}$ yields the **Inner-Outer Degree Balance Equation (Constraint 4)**:
    $$\deg_{\Gamma_2(0) \cap N(a)}(u) = \sum_{j=0}^{11} E(u, w_j) = \text{target\_rhs}(a) := \begin{cases} 1 & \text{if } a \in P_u \cup m(P_u) = \{0, 1, 2, 3\}, \\ 2 & \text{if } a \in \{4, 5, \dots, 13\}. \end{cases}$$

- **Complete Variable-to-Meaning Table for `p2_3_inner_outer_balance_k14` (`548` vars in Encoding A; `522` vars in Encoding B):**
  `build_p2_3_inner_outer_balance(14, encoding)` iterates over $a = 0, 1, \dots, 13$ and allocates a contiguous block of variables for each inner vertex $a$:
  - **`edge_vars` ($12$ variables $x_{a,0}, \dots, x_{a,11}$):** $x_{a,j} = E(u, w_j) \in \{0, 1\}$ indicating whether $u$ is adjacent to the $j$-th outer neighbor $w_j \in \Gamma_2(0) \cap N(a)$ of $a$.
  - **`m_in_Pu` ($1$ variable $m_a$):** Indicator $\mathbf{1}_{m(a) \in P_u}$, fixed by a unit clause `(m_a)` for $a \in \{1, 3\}$ and `(-m_a)` for $a \notin \{1, 3\}$.
  - **`counter_vars` for $\text{add\_exact}([m_a, x_{a,0}, \dots, x_{a,11}], \text{full\_rhs}(a))$:**
    Here $\text{full\_L} = [m_a, x_{a,0}, \dots, x_{a,11}]$ has length $13$, and $\text{full\_rhs}(a) = 1$ for $a \in \{0, 2\}$ ($\lambda = 1$) and $2$ for $a \notin \{0, 2\}$ ($\mu = 2$):
    - In **Encoding A (`Sinz_2005_Sequential_Counter`):** Allocates $13 \times \text{full\_rhs}(a)$ register variables ($13$ vars when $a \in \{0, 2\}$; $26$ vars when $a \notin \{0, 2\}$).
    - In **Encoding B (`Bailleux_Boufkhad_2003_Binary_Tree_Totalizer`):** A $13$-leaf binary tree has $12$ internal nodes, allocating $12 \times \text{full\_rhs}(a)$ internal tree variables ($12$ vars when $a \in \{0, 2\}$; $24$ vars when $a \notin \{0, 2\}$).
  - **`v_low` and `v_high` ($2$ violation variables $v_{\text{low}}^{(a)}, v_{\text{high}}^{(a)}$):**
    - $v_{\text{low}}^{(a)}$ asserts $\sum_{j=0}^{11} x_{a,j} < \text{target\_rhs}(a)$ via $\binom{12}{\text{target\_rhs}(a)}$ clauses $(\neg v_{\text{low}}^{(a)} \vee \bigvee_{x \in C} \neg x)$ forbidding every subset $C \subset \{x_{a,0}..x_{a,11}\}$ of size $\text{target\_rhs}(a)$ (`12` clauses if $\text{target\_rhs}(a)=1$; `66` clauses if $\text{target\_rhs}(a)=2$).
    - $v_{\text{high}}^{(a)}$ asserts $\sum_{j=0}^{11} x_{a,j} > \text{target\_rhs}(a)$ via $\binom{12}{12 - \text{target\_rhs}(a)}$ clauses $(\neg v_{\text{high}}^{(a)} \vee \bigvee_{x \in C} x)$ forbidding every subset of $12 - \text{target\_rhs}(a)$ false literals (`12` clauses if $\text{target\_rhs}(a)=1$; `66` clauses if $\text{target\_rhs}(a)=2$).
  - Finally, the 28-literal disjunction $\bigvee_{a=0}^{13} (v_{\text{low}}^{(a)} \vee v_{\text{high}}^{(a)})$ asserts that Constraint 4 fails for at least one $a \in \{0..13\}$.

| Inner Vertex $a$ | Role of $a$ wrt $P_u=\{0,2\}$ | $\text{full\_rhs}$ / $\text{target\_rhs}$ | Enc A `edge_vars` ($x_{a,0..11}$) | Enc A $m_a$ | Enc A Sinz Counter Vars | Enc A $v_{\text{low}}^{(a)}, v_{\text{high}}^{(a)}$ | Enc B `edge_vars` ($x_{a,0..11}$) | Enc B $m_a$ | Enc B Totalizer Tree Vars | Enc B $v_{\text{low}}^{(a)}, v_{\text{high}}^{(a)}$ |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `0` | $a \in P_u$ ($m(0)=1 \notin P_u$) | `1` / `1` | `1..12` | `13` (`-13`) | `14..26` | `27, 28` | `1..12` | `13` (`-13`) | `14..25` | `26, 27` |
| `1` | $m(1)=0 \in P_u$ ($a \notin P_u$) | `2` / `1` | `29..40` | `41` (`+41`) | `42..67` | `68, 69` | `28..39` | `40` (`+40`) | `41..64` | `65, 66` |
| `2` | $a \in P_u$ ($m(2)=3 \notin P_u$) | `1` / `1` | `70..81` | `82` (`-82`) | `83..95` | `96, 97` | `67..78` | `79` (`-79`) | `80..91` | `92, 93` |
| `3` | $m(3)=2 \in P_u$ ($a \notin P_u$) | `2` / `1` | `98..109` | `110` (`+110`) | `111..136` | `137, 138` | `94..105` | `106` (`+106`) | `107..130` | `131, 132` |
| `4` | $a \notin P_u \cup m(P_u)$ | `2` / `2` | `139..150` | `151` (`-151`) | `152..177` | `178, 179` | `133..144` | `145` (`-145`) | `146..169` | `170, 171` |
| `5` | $a \notin P_u \cup m(P_u)$ | `2` / `2` | `180..191` | `192` (`-192`) | `193..218` | `219, 220` | `172..183` | `184` (`-184`) | `185..208` | `209, 210` |
| `6` | $a \notin P_u \cup m(P_u)$ | `2` / `2` | `221..232` | `233` (`-233`) | `234..259` | `260, 261` | `211..222` | `223` (`-223`) | `224..247` | `248, 249` |
| `7` | $a \notin P_u \cup m(P_u)$ | `2` / `2` | `262..273` | `274` (`-274`) | `275..300` | `301, 302` | `250..261` | `262` (`-262`) | `263..286` | `287, 288` |
| `8` | $a \notin P_u \cup m(P_u)$ | `2` / `2` | `303..314` | `315` (`-315`) | `316..341` | `342, 343` | `289..300` | `301` (`-301`) | `302..325` | `326, 327` |
| `9` | $a \notin P_u \cup m(P_u)$ | `2` / `2` | `344..355` | `356` (`-356`) | `357..382` | `383, 384` | `328..339` | `340` (`-340`) | `341..364` | `365, 366` |
| `10` | $a \notin P_u \cup m(P_u)$ | `2` / `2` | `385..396` | `397` (`-397`) | `398..423` | `424, 425` | `367..378` | `379` (`-379`) | `380..403` | `404, 405` |
| `11` | $a \notin P_u \cup m(P_u)$ | `2` / `2` | `426..437` | `438` (`-438`) | `439..464` | `465, 466` | `406..417` | `418` (`-418`) | `419..442` | `443, 444` |
| `12` | $a \notin P_u \cup m(P_u)$ | `2` / `2` | `467..478` | `479` (`-479`) | `480..505` | `506, 507` | `445..456` | `457` (`-457`) | `458..481` | `482, 483` |
| `13` | $a \notin P_u \cup m(P_u)$ | `2` / `2` | `508..519` | `520` (`-520`) | `521..546` | `547, 548` | `484..495` | `496` (`-496`) | `497..520` | `521, 522` |

(Note: for the $10$ blocks $a \in \{4, \dots, 13\}$, each block starts at base variable $139 + 41(a-4)$ in Encoding A and $133 + 39(a-4)$ in Encoding B.)
The shipped core `p2_3_inner_outer_balance_k14_encA_core.cnf` has `2,487` clauses and is refuted in `836` RUP steps; `p2_3_inner_outer_balance_k14_encB_core.cnf` has `2,483` clauses and is refuted in `780` RUP steps.

---

### 3.4. `p2_4_outer_pair_cn_k14` (`verify.py` lines 232–265)

- **Statement in `arXiv:2608.11211` Section 2.3 (Constraints 2 & 3, p. 3):**
  Let $u, v \in \Gamma_2(0)$ be two distinct outer vertices sharing $s = |P_u \cap P_v| \in \{0, 1\}$ inner neighbors in $\Gamma_1(0)$ (by `p2_2`, $P_u \ne P_v$, so $s \in \{0, 1\}$), and let $e_{uv} = E(u, v) \in \{0, 1\}$ be their adjacency bit and $c_0, \dots, c_{11} \in \{0, 1\}$ be the indicators of whether each of the $12$ remaining candidate outer neighbors of $u$ is also adjacent to $v$ ($\mathrm{cn}_{\Gamma_2(0)}(u, v) = \sum_{i=0}^{11} c_i$).
  - By $\lambda = 1$ (when $e_{uv} = 1$) and $\mu = 2$ (when $e_{uv} = 0$), the total number of common neighbors of $u$ and $v$ in $\Gamma$ satisfies $e_{uv} + \mathrm{cn}_\Gamma(u, v) = 2$.
  - Since $\mathrm{cn}_\Gamma(u, v) = s + \sum_{i=0}^{11} c_i$, the $14$-variable list $\text{full\_L} = [s_{\text{var}}, e_{uv}, c_0, \dots, c_{11}]$ has exact sum $2$:
    $$s + e_{uv} + \sum_{i=0}^{11} c_i = 2 \iff \sum_{i=0}^{11} c_i = \text{target}(s, e_{uv}) := (2 - s) - e_{uv}.$$
  - Specifically:
    - **Constraint 2 ($e_{uv} = 1$, adjacent outer vertices):** $\mathrm{cn}_{\Gamma_2(0)}(u, v) = 1 - s$ ($1$ if $s = 0$, $0$ if $s = 1$).
    - **Constraint 3 ($e_{uv} = 0$, non-adjacent outer vertices):** $\mathrm{cn}_{\Gamma_2(0)}(u, v) = 2 - s$ ($2$ if $s = 0$, $1$ if $s = 1$).

- **Complete Variable-to-Meaning Table for `p2_4_outer_pair_cn_k14` (`91` vars in Encoding A; `87` vars in Encoding B):**
  `build_p2_4_outer_pair_cn(encoding)` constructs two blocks: $s = 0$ ($|P_u \cap P_v| = 0$) and $s = 1$ ($|P_u \cap P_v| = 1$).

| Case $s = |P_u \cap P_v|$ | Variable Role | Mathematical Meaning | Encoding A Variable IDs (`91` total) | Encoding B Variable IDs (`87` total) |
| :---: | :--- | :--- | :---: | :---: |
| **$s = 0$** | $e_{uv}^{(0)}$ | Adjacency $E(u, v) \in \{0, 1\}$ when $|P_u \cap P_v| = 0$ | `1` | `1` |
| **$s = 0$** | $s_{\text{var}}^{(0)}$ | Inner intersection bit $s = 0$ (fixed false by unit clause `-2 0`) | `2` | `2` |
| **$s = 0$** | $c_0^{(0)} \dots c_{11}^{(0)}$ | Outer common-neighbor indicators $w_i \in \Gamma_2(0) \cap N(u) \cap N(v)$ ($i = 0..11$) | `3..14` | `3..14` |
| **$s = 0$** | `counter_vars` | Exact cardinality counter for $s_{\text{var}}^{(0)} + e_{uv}^{(0)} + \sum_{i=0}^{11} c_i^{(0)} = 2$ (14 inputs, $k = 2$) | `15..42` ($14 \times 2 = 28$ Sinz registers) | `15..40` ($13 \times 2 = 26$ Totalizer tree vars) |
| **$s = 0$** | $v_{\text{low}}^{(0, e=1)}, v_{\text{high}}^{(0, e=1)}$ | Violation bits for $e_{uv}^{(0)} = 1$ with $\sum c_i^{(0)} < 1$ (`v_low`) or $\sum c_i^{(0)} > 1$ (`v_high`) | `43, 44` | `41, 42` |
| **$s = 0$** | $v_{\text{low}}^{(0, e=0)}, v_{\text{high}}^{(0, e=0)}$ | Violation bits for $e_{uv}^{(0)} = 0$ with $\sum c_i^{(0)} < 2$ (`v_low`) or $\sum c_i^{(0)} > 2$ (`v_high`) | `45, 46` | `43, 44` |
| **$s = 1$** | $e_{uv}^{(1)}$ | Adjacency $E(u, v) \in \{0, 1\}$ when $|P_u \cap P_v| = 1$ | `47` | `45` |
| **$s = 1$** | $s_{\text{var}}^{(1)}$ | Inner intersection bit $s = 1$ (fixed true by unit clause `48 0` in Enc A / `46 0` in Enc B) | `48` | `46` |
| **$s = 1$** | $c_0^{(1)} \dots c_{11}^{(1)}$ | Outer common-neighbor indicators $w_i \in \Gamma_2(0) \cap N(u) \cap N(v)$ ($i = 0..11$) | `49..60` | `47..58` |
| **$s = 1$** | `counter_vars` | Exact cardinality counter for $s_{\text{var}}^{(1)} + e_{uv}^{(1)} + \sum_{i=0}^{11} c_i^{(1)} = 2$ (14 inputs, $k = 2$) | `61..88` ($28$ Sinz registers) | `59..84` ($26$ Totalizer tree vars) |
| **$s = 1$** | $v_{\text{high}}^{(1, e=1)}$ | Violation bit for $e_{uv}^{(1)} = 1$ with $\sum c_i^{(1)} > 0$ ($\text{target} = 0$, so no `v_low`) | `89` | `85` |
| **$s = 1$** | $v_{\text{low}}^{(1, e=0)}, v_{\text{high}}^{(1, e=0)}$ | Violation bits for $e_{uv}^{(1)} = 0$ with $\sum c_i^{(1)} < 1$ (`v_low`) or $\sum c_i^{(1)} > 1$ (`v_high`) | `90, 91` | `86, 87` |

The 7-literal disjunction of all violation bits (`43 44 45 46 89 90 91 0` in Encoding A; `41 42 43 44 85 86 87 0` in Encoding B) asserts that Constraints 2 & 3 fail in at least one case. The shipped core `p2_4_outer_pair_cn_k14_encA_core.cnf` has `345` clauses and is refuted in `142` RUP steps; `p2_4_outer_pair_cn_k14_encB_core.cnf` has `342` clauses and is refuted in `111` RUP steps.

---

### 3.5. `p2_5_srg9_uniqueness` (`verify.py` lines 267–325)

- **Statement in `arXiv:2608.11211` Section 2.3 (p. 4, Validation on $\mathrm{srg}(9, 4, 1, 2)$):**
  For the $k = 4$ sibling $\mathrm{srg}(9, 4, 1, 2) \cong K_3 \square K_3$, $\Gamma_1(0)$ is a matching of $k/2 = 2$ inner edges $\{0_L, 0_R\}$ and $\{1_L, 1_R\}$, and $\Gamma_2(0)$ consists of the $M = 4(4-2)/2 = 4$ non-matched pairs:
  $$p_0 = \{0_L, 1_L\}, \quad p_1 = \{0_L, 1_R\}, \quad p_2 = \{0_R, 1_L\}, \quad p_3 = \{0_R, 1_R\}.$$
  Applying Constraint 4 (`p2_3`) and Constraints 2 & 3 (`p2_4`) to the $\binom{4}{2} = 6$ outer pairs $\{p, q\}$ forces the unique outer $4$-cycle where $p_0—p_1—p_3—p_2—p_0$ are edges ($s = |P_p \cap P_q| = 1$) and the diagonals $\{p_0, p_3\}, \{p_1, p_2\}$ are non-edges ($s = 0$).

- **Primary Edge Variable Map (`1..6` in both Encoding A and Encoding B):**
  - `var 1` $= E(p_0, p_1)$: edge between $\{0_L, 1_L\}$ and $\{0_L, 1_R\}$ ($s = 1$, shared inner vertex $0_L$).
  - `var 2` $= E(p_0, p_2)$: edge between $\{0_L, 1_L\}$ and $\{0_R, 1_L\}$ ($s = 1$, shared inner vertex $1_L$).
  - `var 3` $= E(p_0, p_3)$: diagonal between $\{0_L, 1_L\}$ and $\{0_R, 1_R\}$ ($s = 0$, disjoint inner pairs).
  - `var 4` $= E(p_1, p_2)$: diagonal between $\{0_L, 1_R\}$ and $\{0_R, 1_L\}$ ($s = 0$, disjoint inner pairs).
  - `var 5` $= E(p_1, p_3)$: edge between $\{0_L, 1_R\}$ and $\{0_R, 1_R\}$ ($s = 1$, shared inner vertex $1_R$).
  - `var 6` $= E(p_2, p_3)$: edge between $\{0_R, 1_L\}$ and $\{0_R, 1_R\}$ ($s = 1$, shared inner vertex $0_R$).

- **Why the Shipped Encoding A Core (`13` clauses) Uses Variables `1..6, 7, 10, 11, 16, 18, 21` While the Encoding B Core (`7` clauses) Uses Only `1..6`:**
  In `build_p2_5_srg9_uniqueness` (`verify.py` lines 290–297), for each outer vertex $p \in \{0, 1, 2, 3\}$ and each inner vertex $a \in \{0_L, 0_R, 1_L, 1_R\}$, the inner-outer balance equation (`p2_3`) constrains $L(p, a) = [E(p, q) : q \ne p, a \in P_q]$ to sum to $\text{rhs} = 1$ (since $k = 4 \implies P_p \cup m(P_p) = \Gamma_1(0)$ for every $p$):
  - When $a \in P_p$, only **one** other outer vertex $q \ne p$ contains $a$, so $|L(p, a)| = 1$:
    - In **Encoding A (`Sinz_2005_Sequential_Counter`):** Even for a 1-element list $L = [v]$ with $k = 1$, `add_exact_sinz` allocates $1 \times 1 = 1$ register variable $s_{0,0}$ and emits `(s_{0,0})`, `(-v V s_{0,0})`, `(v V -s_{0,0})`. Specifically:
      - `var 7` $= s_{0,0}$ for $(p_0, a = 0_L)$ where $L = [1]$ (`c1: 7 0`, `c5: 1 -7 0` $\implies \text{var } 1 = 1$).
      - `var 10` $= s_{0,0}$ for $(p_0, a = 1_L)$ where $L = [2]$ (`c2: 10 0`, `c6: 2 -10 0` $\implies \text{var } 2 = 1$).
      - `var 18` $= s_{0,0}$ for $(p_1, a = 1_R)$ where $L = [5]$ (`c3: 18 0`, `c7: 5 -18 0` $\implies \text{var } 5 = 1$).
      - `var 21` $= s_{0,0}$ for $(p_2, a = 0_R)$ where $L = [6]$ (`c4: 21 0`, `c8: 6 -21 0` $\implies \text{var } 6 = 1$).
    - In **Encoding B (`Bailleux_Boufkhad_2003_Binary_Tree_Totalizer`):** For a 1-element list $L = [v]$, `build_tree([v])` returns the leaf `[v]` without allocating a new variable (`verify.py` lines 81–82), and `clauses.append([root[0]])` (line 116) directly emits the unit clauses `c1: 1 0`, `c2: 2 0`, `c3: 5 0`, `c4: 6 0`!
  - When $a \notin P_p$, both outer vertices containing $a$ are distinct from $p$, so $|L(p, a)| = 2$ and $\text{rhs} = 1$:
    - For $(p_0, a = 1_R)$, $L = [1, 3]$ ($E(p_0, p_1) + E(p_0, p_3) = 1$):
      - In **Encoding A**, `var 11` is the Sinz prefix register $s_{0,0} \iff \text{var } 1$ (`c9: 11 -1 0`) and `c11: -3 -11 0` is the overflow clause ($\text{var } 1 \implies \text{var } 11 \implies \neg \text{var } 3$).
      - In **Encoding B**, merging the two leaves `[1]` and `[3]` at $k = 1$ directly emits the binary overflow clause `c6: -3 -1 0` (`verify.py` line 99 for $a = 1, b = 1 > k = 1$).
    - For $(p_1, a = 1_L)$, $L = [1, 4]$ ($E(p_0, p_1) + E(p_1, p_2) = 1$):
      - In **Encoding A**, `var 16` is the Sinz prefix register $s_{0,0} \iff \text{var } 1$ (`c10: 16 -1 0`) and `c12: -4 -16 0` is the overflow clause ($\text{var } 1 \implies \text{var } 16 \implies \neg \text{var } 4$).
      - In **Encoding B**, merging leaves `[1]` and `[4]` at $k = 1$ directly emits `c5: -4 -1 0`.
  - Together with the blocking clause `3 4 -2 -1 -5 -6 0` (`c13` in Encoding A; `c7` in Encoding B, forbidding the assignment $v_1 = v_2 = v_5 = v_6 = 1, v_3 = v_4 = 0$), unit propagation derives the empty clause in **1 RUP step** in both encodings (`14 0 1 2 3 4 5 6 7 8 9 10 11 12 13 0` in `p2_5_srg9_uniqueness_encA_core.lrat`; `8 0 1 2 3 4 5 6 7 0` in `p2_5_srg9_uniqueness_encB_core.lrat`).
