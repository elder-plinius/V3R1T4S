role: novelty
context: fresh research subagent invoked via invoke_subagent
problem_id: conway-99-graph
claim_targeted: p1 + p2

# Skeptic 2 (`novelty`) Audit — `conway-99-graph` (`p1 + p2`)

## 1. Scope & Files Inspected

This audit inspected only the permitted target, scout, and claim files:
- `target.md`
- `scout.md`
- `claim/artifact.md`
- `claim/certificate.json`

## 2. Prior-Art Baseline vs. Claimed Contributions

### 2.1 Track `p2`: Forced-Structure Reduction of `arXiv:2608.11211`

- **Prior-Art Baseline:**
  Thakkar & Severini (`arXiv:2608.11211v2`, 18 Sep 2026, Section 2.3) introduced the forced-structure reduction around a fixed root vertex $x \in V(\Gamma)$ for $\Gamma = \mathrm{srg}(99, 14, 1, 2)$, showing analytically and via CP-SAT/backtracking models that:
  1. $\Gamma_1(x)$ is forced to be $1$-regular (a perfect matching $M_x$ of $k/2 = 7$ edges),
  2. $\Gamma_2(x)$ ($84$ vertices) stands in canonical bijection with the $M = \binom{k}{2} - k/2 = 84$ non-matched pairs $P_u \in \binom{\Gamma_1(x)}{2} \setminus M_x$,
  3. Every $u \in \Gamma_2(x)$ and $a \in \Gamma_1(x)$ satisfies the inner-outer coordinate balance $\mathbf{1}_{m(a) \in P_u} + \deg_{N(a)}(u) = 2$,
  4. Every distinct pair $u, v \in \Gamma_2(x)$ with $s = |P_u \cap P_v| \in \{0, 1\}$ satisfies $E(u, v) + \mathrm{cn}_{\Gamma_2(x)}(u, v) = 2 - s$,
  5. The reduced system is exact and uniquely satisfied on the smaller parameter-family member $\mathrm{srg}(9, 4, 1, 2) \cong K_3 \square K_3$.
  However, `arXiv:2608.11211v2` did not publish SAT CNF encodings or machine-checkable DRAT/LRAT proof certificates for these reduction steps.

- **Novelty of the Present Claim on Track `p2`:**
  The artifact provides the first standalone, dual-encoded DRAT and pure-RUP LRAT (`0 RAT lemmas`) machine-checked re-derivation of all $5$ forced-structure reduction propositions (`p2_1_inner_matching_k14`, `p2_2_outer_bijection_k14`, `p2_3_inner_outer_balance_k14`, `p2_4_outer_pair_cn_k14`, and `p2_5_srg9_uniqueness`), together with positive SAT non-vacuity verification on $\mathrm{srg}(9, 4, 1, 2) \cong K_3 \square K_3$. Every proposition is independently encoded and certified across two structurally distinct SAT cardinality encodings:
  - **Encoding A (`Sinz_2005_Sequential_Counter`):** $4 + 13 + 2,487 + 345 + 13 = 2,862$ trimmed core clauses and $1 + 3 + 836 + 142 + 1 = 983$ pure-RUP LRAT steps (`0 RAT lemmas`).
  - **Encoding B (`Bailleux_Boufkhad_2003_Binary_Tree_Totalizer`):** $4 + 12 + 2,483 + 342 + 7 = 2,848$ trimmed core clauses and $1 + 3 + 780 + 111 + 1 = 896$ pure-RUP LRAT steps (`0 RAT lemmas`).

### 2.2 Track `p1`: DRAT/LRAT-Certified Prime-Order and Frobenius Subgroup Automorphism Exclusions

- **Prior-Art Baseline:**
  - Makhnev & Minakova (2004) and Behbahani & Lam (2011) restricted prime divisors of $|\mathrm{Aut}(\Gamma)|$ for $\Gamma = \mathrm{srg}(99, 14, 1, 2)$ to $p \in \{2, 3, 7\}$.
  - Wilbrink (1983), Crnković, Maksimović & Švob (`arXiv:2308.02978`, 2023), and Thakkar & Severini (`arXiv:2608.11211v2`, 2026) excluded prime-order automorphisms ($p = 3$, $p = 2$) and the order-$21$ Frobenius subgroup $\mathrm{Frob}(21) = \mathbb{Z}_7 \rtimes \mathbb{Z}_3$ via custom backtracking, GAP scripts, or CP-SAT runs without emitting machine-checkable DRAT/LRAT UNSAT proof certificates. Furthermore, Section 2.4 of `arXiv:2608.11211v2` tested generic block-circulant orbit models without hanging the forced-structure reduction at a fixed root vertex $x$.

- **Novelty of the Present Claim on Track `p1`:**
  By anchoring the forced-structure reduction at the fixed root vertex $x$ and quotienting the $84$ pair-labeled outer vertices $\Gamma_2(x)$ by the induced action $g(P_u) = \{g(a), g(b)\}$, the artifact produces the first dual-encoded DRAT and pure-RUP LRAT (`0 RAT lemmas`) UNSAT certificates for $8$ distinct prime-order and Frobenius automorphism actions:
  1. `p3_t1_fix33`: Prime order $p = 3$ fixing $33$ vertices ($1 + 8 + 24$) with $22$ cycles of length $3$ ($1,346$ primary edge-orbit variables, $44$ outer vertex orbits; $166$ / $251$ core clauses and $23$ / $35$ RUP steps in Encodings A / B).
  2. `p2_a0_b1_c6_fix73`: Involution $p = 2$, $(a,b,c) = (0,1,6)$, fixing $73$ vertices ($1 + 12 + 60$) with $13$ transpositions ($178$ / $170$ core clauses, $1$ / $1$ RUP step).
  3. `p2_a0_b2_c5_fix51`: Involution $p = 2$, $(a,b,c) = (0,2,5)$, fixing $51$ vertices ($1 + 10 + 40$) with $24$ transpositions ($440$ / $720$ core clauses, $115$ / $308$ RUP steps).
  4. `p2_a1_b0_c5_fix53`: Involution $p = 2$, $(a,b,c) = (1,0,5)$, fixing $53$ vertices ($1 + 10 + 42$) with $23$ transpositions ($666$ / $637$ core clauses, $174$ / $157$ RUP steps).
  5. `p2_a0_b4_c3_fix19`: Involution $p = 2$, $(a,b,c) = (0,4,3)$, fixing $19$ vertices ($1 + 6 + 12$) with $40$ transpositions ($6,427$ / $5,536$ core clauses, $1,035$ / $1,697$ RUP steps).
  6. `p2_a1_b2_c3_fix21`: Involution $p = 2$, $(a,b,c) = (1,2,3)$, fixing $21$ vertices ($1 + 6 + 14$) with $39$ transpositions ($16,282$ / $10,280$ core clauses, $2,924$ / $2,605$ RUP steps).
  7. `p2_a1_b3_c2_fix11`: Involution $p = 2$, $(a,b,c) = (1,3,2)$, fixing $11$ vertices ($1 + 4 + 6$) with $44$ transpositions ($3,328$ / $2,172$ core clauses, $1,308$ / $1,162$ RUP steps).
  8. `frob21_z7_z3`: Order-$21$ Frobenius subgroup $\mathrm{Frob}(21) = \mathbb{Z}_7 \rtimes \mathbb{Z}_3$ fixing root $x$, generated by an order-$7$ automorphism ($1$ fixed vertex, $14$ cycles of length $7$) and an order-$3$ automorphism ($3$ fixed vertices, $32$ cycles of length $3$), compressed to $166$ primary edge-orbit variables and $4$ outer vertex orbits ($14,407$ / $8,678$ core clauses and $3,253$ / $3,016$ RUP steps in Encodings A / B).

## 3. Conclusion

Across both tracks (`5` forced-structure reduction propositions in Track `p2` and `8` prime-order / Frobenius subgroup automorphism exclusions in Track `p1`), the artifact delivers $26$ independent DRAT and pure-RUP LRAT UNSAT certificates ($19,693$ total RUP steps, $0$ RAT lemmas) across two structurally distinct SAT cardinality encodings, upgrading prior uncertified backtracking/CP-SAT results into standalone, zero-dependency, machine-checkable proof certificates. The claim genuinely advances beyond the existing literature on Conway's 99-graph problem.

pass: true
