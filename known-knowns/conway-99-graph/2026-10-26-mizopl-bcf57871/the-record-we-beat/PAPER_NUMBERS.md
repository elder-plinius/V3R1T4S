# Prior Published Baseline & Literature Comparison (`conway-99-graph`, Track `p2`)

## 1. Primary Literature Reference

- **Aalok Thakkar and Simone Severini (18 Sep 2026):**
  - **Title:** *A Forced-Structure Reduction and Verifiable Bounds for Conway's 99-Graph*
  - **Reference:** `arXiv:2608.11211v2` (`https://arxiv.org/abs/2608.11211`), Section 2.3 (*A Forced-Structure Reduction*, pp. 2–4)
  - **Reported Results:**
    - Formulated the forced-structure neighborhood reduction on $\mathrm{srg}(99, 14, 1, 2)$ around a fixed vertex $0 \in V(\Gamma)$:
      1. The neighborhood $\Gamma_1(0)$ ($k = 14$ vertices) is $1$-regular under $\lambda = 1$, forming a perfect matching $M_0$ of $7$ disjoint edges (`p2_1_inner_matching_k14`).
      2. Each of the $M = 84$ outer vertices $u \in \Gamma_2(0)$ has $\mu = 2$ neighbors in $\Gamma_1(0)$, which cannot form a matched edge of $M_0$ (by $\lambda = 1$) and cannot coincide for two distinct outer vertices $u \ne v$ (by $\mu = 2$ on non-matched pairs of $\Gamma_1(0)$), establishing a canonical bijection between $\Gamma_2(0)$ and the $\binom{14}{2} - 7 = 84$ non-matched pairs $P_u \subset \Gamma_1(0)$ (**Constraint 1**, `p2_2_outer_bijection_k14`).
      3. For any outer vertex $u \in \Gamma_2(0)$ and inner vertex $a \in \Gamma_1(0)$ with matched partner $m(a)$, counting common neighbors of $u$ and $a$ in $\Gamma$ ($\lambda = 1$ if $a \in P_u$, $\mu = 2$ if $a \notin P_u$) forces the outer degree balance $\deg_{\Gamma_2(0) \cap N(a)}(u) = 1$ if $a \in P_u \cup m(P_u)$ and $2$ otherwise (**Constraint 4**, `p2_3_inner_outer_balance_k14`).
      4. For any two distinct outer vertices $u, v \in \Gamma_2(0)$ sharing $s = |P_u \cap P_v| \in \{0, 1\}$ inner neighbors, counting common neighbors of $u$ and $v$ in $\Gamma$ ($\lambda = 1$ if $E(u,v) = 1$, $\mu = 2$ if $E(u,v) = 0$) forces $E(u,v) + \mathrm{cn}_{\Gamma_2(0)}(u,v) = 2 - s$ (**Constraints 2 & 3**, `p2_4_outer_pair_cn_k14`).
      5. Validated the exactness of the forced-structure reduction on the smaller sibling parameter set $\mathrm{srg}(9, 4, 1, 2) \cong K_3 \square K_3$ ($k = 4, M = 4$), where the reduced system uniquely forces the $4$-cycle on the $4$ outer vertices (`p2_5_srg9_uniqueness`).
    - Did not publish standalone SAT CNF encodings or DRAT/LRAT proof certificates for these five reduction propositions.

---

## 2. Track `p2` Comparison: Forced-Structure Reduction Propositions (`p2_1` through `p2_5`)

| Proposition ID | Statement in `arXiv:2608.11211` (§2.3) | `arXiv:2608.11211` Certificate Status | Enc A (`Sinz_2005_Sequential_Counter`) Full Vars / Clauses, Core Clauses, RUP Lemmas | Enc B (`Bailleux_Boufkhad_2003_Binary_Tree_Totalizer`) Full Vars / Clauses, Core Clauses, RUP Lemmas | RAT Lemmas |
| :--- | :--- | :--- | :--- | :--- | :---: |
| `p2_1_inner_matching_k14` | $\Gamma_1(0) \cong 7 K_2$ (1-regular of order 14 under $\lambda = 1$) | Prose derivation only (no SAT/LRAT certificate) | `273` vars / `716` clauses; `4` core clauses; `1` RUP lemma | `259` vars / `688` clauses; `4` core clauses; `1` RUP lemma | `0` |
| `p2_2_outer_bijection_k14` | Bijection $\Gamma_2(0) \leftrightarrow 84$ non-matched pairs $\{a,b\} \subset \Gamma_1(0)$ (Constraint 1) | Prose derivation only (no SAT/LRAT certificate) | `1,598` vars / `1,578` clauses; `13` core clauses; `3` RUP lemmas | `1,585` vars / `1,576` clauses; `12` core clauses; `3` RUP lemmas | `0` |
| `p2_3_inner_outer_balance_k14` | Inner-outer degree balance $\in \{1, 2\}$ (Constraint 4) | Prose derivation only (no SAT/LRAT certificate) | `548` vars / `2,733` clauses; `2,487` core clauses; `836` RUP lemmas | `522` vars / `2,717` clauses; `2,483` core clauses; `780` RUP lemmas | `0` |
| `p2_4_outer_pair_cn_k14` | Outer pair common-neighbor equation $E(u,v) + \mathrm{cn}_{\Gamma_2(0)}(u,v) = 2 - |P_u \cap P_v|$ (Constraints 2 & 3) | Prose derivation only (no SAT/LRAT certificate) | `91` vars / `407` clauses; `345` core clauses; `142` RUP lemmas | `87` vars / `407` clauses; `342` core clauses; `111` RUP lemmas | `0` |
| `p2_5_srg9_uniqueness` | Forced-structure uniqueness of $\mathrm{srg}(9, 4, 1, 2) \cong K_3 \square K_3$ | CP-SAT script (no LRAT certificate) | `66` vars / `201` clauses; `13` core clauses; `1` RUP lemma (SAT without blocking clause) | `42` vars / `147` clauses; `7` core clauses; `1` RUP lemma (SAT without blocking clause) | `0` |
| **Total (`p2`)** | **5 Propositions (10 Pure-RUP LRAT Certificates)** | — | **`2,862` core clauses; `983` RUP lemmas** | **`2,848` core clauses; `896` RUP lemmas** | **`0`** |
