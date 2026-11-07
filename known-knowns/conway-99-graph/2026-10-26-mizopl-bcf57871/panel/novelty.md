role: novelty
context: fresh research subagent invoked via invoke_subagent
problem_id: conway-99-graph
claim_targeted: p2

# Skeptic 2 (`novelty`) Audit — `conway-99-graph` (Track `p2`)

## 1. Scope & Files Inspected

This audit inspected only the permitted package files:
- `the-record-we-beat/table_status.md`
- `the-record-we-beat/PAPER_NUMBERS.md`
- `how-we-built-it/artifact.md`
- `object/certificate.json`

## 2. Prior-Art Baseline vs. Claimed Contributions on Track `p2`

- **Prior-Art Baseline:**
  Aalok Thakkar & Simone Severini (`arXiv:2608.11211v2`, 18 Sep 2026, Section 2.3) introduced the forced-structure reduction around a fixed root vertex $0 \in V(\Gamma)$ for $\Gamma = \mathrm{srg}(99, 14, 1, 2)$, showing analytically and via CP-SAT/backtracking models that:
  1. $\Gamma_1(0)$ is forced to be $1$-regular (a perfect matching $M_0$ of $k/2 = 7$ edges),
  2. $\Gamma_2(0)$ ($84$ vertices) stands in canonical bijection with the $M = \binom{k}{2} - k/2 = 84$ non-matched pairs $P_u \in \binom{\Gamma_1(0)}{2} \setminus M_0$ (Constraint 1),
  3. Every $u \in \Gamma_2(0)$ and $a \in \Gamma_1(0)$ satisfies the inner-outer coordinate balance $\mathbf{1}_{m(a) \in P_u} + \deg_{\Gamma_2(0) \cap N(a)}(u) = 2$ for $a \notin P_u$ and $\deg_{\Gamma_2(0) \cap N(a)}(u) = 1$ for $a \in P_u$ (Constraint 4),
  4. Every distinct pair $u, v \in \Gamma_2(0)$ with $s = |P_u \cap P_v| \in \{0, 1\}$ satisfies $E(u, v) + \mathrm{cn}_{\Gamma_2(0)}(u, v) = 2 - s$ (Constraints 2 & 3),
  5. The reduced system is exact and uniquely satisfied on the smaller parameter-family member $\mathrm{srg}(9, 4, 1, 2) \cong K_3 \square K_3$.
  However, `arXiv:2608.11211v2` did not publish standalone SAT CNF encodings or DRAT/LRAT proof certificates for these five reduction propositions.

- **Contribution of the Present Package on Track `p2`:**
  The artifact provides standalone, dual-encoded pure-RUP LRAT (`0` RAT lemmas) UNSAT certificates re-deriving all $5$ forced-structure reduction propositions (`p2_1_inner_matching_k14`, `p2_2_outer_bijection_k14`, `p2_3_inner_outer_balance_k14`, `p2_4_outer_pair_cn_k14`, and `p2_5_srg9_uniqueness`), together with positive SAT non-vacuity verification on $\mathrm{srg}(9, 4, 1, 2) \cong K_3 \square K_3$. Every proposition is independently encoded and certified across two SAT cardinality encodings:
  - **Encoding A (`Sinz_2005_Sequential_Counter`):** $4 + 13 + 2,487 + 345 + 13 = 2,862$ trimmed core clauses and $1 + 3 + 836 + 142 + 1 = 983$ pure-RUP LRAT lemmas (`0` RAT lemmas).
  - **Encoding B (`Bailleux_Boufkhad_2003_Binary_Tree_Totalizer`):** $4 + 12 + 2,483 + 342 + 7 = 2,848$ trimmed core clauses and $1 + 3 + 780 + 111 + 1 = 896$ pure-RUP LRAT lemmas (`0` RAT lemmas).

## 3. Conclusion

Across the $5$ forced-structure reduction propositions in Track `p2`, the artifact delivers $10$ pure-RUP LRAT UNSAT certificates (`5,710` core clauses, `1,879` total RUP lemmas, `0` RAT lemmas) across two SAT cardinality encodings.

pass: true
