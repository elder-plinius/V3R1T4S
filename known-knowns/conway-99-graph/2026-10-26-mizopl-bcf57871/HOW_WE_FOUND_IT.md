# How We Found It (`conway-99-graph`, Track `p2`)

*Note: contributor text, unverified (for the machine-verified claims and proof certificates, see `object/certificate.json`, `object/proofs/`, and `verify-it-yourself/verify.py`).*

## Methodology
1. **Anchoring the Forced-Structure Reduction at a Fixed Vertex $0$ (`arXiv:2608.11211`, Section 2.3):**
   In Section 2.3 of `arXiv:2608.11211`, Aalok Thakkar & Simone Severini (2026) formulated a forced-structure neighborhood reduction around a fixed root vertex $0 \in V(\Gamma)$ of a hypothetical $\Gamma = \mathrm{srg}(99, 14, 1, 2)$, showing that:
   - `p2_1_inner_matching_k14`: $\lambda = 1$ on edges incident to $0$ forces $\Gamma_1(0)$ ($k = 14$ vertices) to be $1$-regular (a perfect matching $M_0$ of $7$ disjoint edges).
   - `p2_2_outer_bijection_k14` (**Constraint 1** of `arXiv:2608.11211` §2.3): $\lambda = 1$ on $M_0$ and $\mu = 2$ on non-matched pairs force a canonical bijection between $\Gamma_2(0)$ ($M = 84$ vertices) and the $\binom{14}{2} - 7 = 84$ non-matched pairs $P_u \in \binom{\Gamma_1(0)}{2} \setminus M_0$.
   - `p2_3_inner_outer_balance_k14` (**Constraint 4** of `arXiv:2608.11211` §2.3): For every outer vertex $u \in \Gamma_2(0)$ and inner vertex $a \in \Gamma_1(0)$ with matched partner $m(a)$, the common-neighbor count $\mathrm{cn}_\Gamma(u, a) = \mathbf{1}_{m(a) \in P_u} + \deg_{\Gamma_2(0) \cap N(a)}(u)$ forces $\deg_{\Gamma_2(0) \cap N(a)}(u) = 1$ if $a \in P_u \cup m(P_u)$ and $2$ otherwise.
   - `p2_4_outer_pair_cn_k14` (**Constraints 2 & 3** of `arXiv:2608.11211` §2.3): For every distinct pair $u, v \in \Gamma_2(0)$ sharing $s = |P_u \cap P_v| \in \{0, 1\}$ inner neighbors, $\mathrm{cn}_\Gamma(u, v) = s + \mathrm{cn}_{\Gamma_2(0)}(u, v)$ forces $E(u, v) + \mathrm{cn}_{\Gamma_2(0)}(u, v) = 2 - s$.
   - `p2_5_srg9_uniqueness` (**Section 2.3 Validation on $\mathrm{srg}(9, 4, 1, 2)$**): Applying Constraints 1–4 to the smaller sibling parameter set $\mathrm{srg}(9, 4, 1, 2)$ ($k = 4, M = 4$) yields a satisfiable system whose unique outer solution is the $4$-cycle of $K_3 \square K_3$.
2. **Dual SAT Cardinality Encodings & Pure-RUP LRAT Extraction:**
   To re-derive all five propositions with machine-checkable certificates across two independent SAT cardinality encodings, we encoded every exact cardinality constraint $\sum_{i=1}^n L_i = k$ in:
   - **Encoding A (`Sinz_2005_Sequential_Counter`):** Carsten Sinz's (2005) linear sequential counter, which allocates $n \cdot k$ prefix-sum register variables $s_{i,j}$ (`0 <= i < n`, `0 <= j < k`) representing $\sum_{r=0}^i L_r \ge j + 1$.
   - **Encoding B (`Bailleux_Boufkhad_2003_Binary_Tree_Totalizer`):** Olivier Bailleux & Yacine Boufkhad's (2003) binary tree unary totalizer, which recursively bisects $L$ into balanced subtrees `L[:mid]` and `L[mid:]` and allocates $\min(k, |\text{left}| + |\text{right}|)$ unary sum variables at each internal tree node in post-order.
   Running `kissat` (with RAT-producing inprocessing disabled) followed by `drat-trim -L` produced the 10 trimmed CNF cores (`2,862` core clauses in Encoding A + `2,848` core clauses in Encoding B = `5,710` core clauses total) and 10 Pure-RUP LRAT refutations (`983` RUP lemmas in Encoding A + `896` RUP lemmas in Encoding B = `1,879` RUP lemmas total, `0` RAT steps).
