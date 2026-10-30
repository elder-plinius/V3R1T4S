# Notes: Lens 1 — Exact SMT / MILP Counterexample Search

## Hypotheses
1. **H1 (Primal SMT integer search)**: SMT QF_LIA over 864 allocation disjunctions with row-sum normalization ($\sum v_{ig} = 100$) can locate an integer valuation matrix refuting all 864 complete feasible allocations simultaneously under prescribed order $1 \prec 2 \prec 3 \prec 4$. (Guessed chance: 50%, Cost: Low).
2. **H2 (Primal SMT QF_LRA rational search)**: Continuous linear real arithmetic with disjunctions can find rational counterexamples and produce exact fraction models. (Guessed chance: 40%, Cost: Low).
3. **H3 (Universal order-invariant counterexample)**: A single valuation matrix refutes all 24 possible agent orderings simultaneously. (Guessed chance: 15%, Cost: Medium).
4. **H4 (Automorphism orbit reduction)**: Reducing the 864 allocations by the matroid automorphism group $S_3 \times S_3 \times S_2$ (order 72) reduces the clause count to fundamental partition orbits. (Guessed chance: 35%, Cost: Medium).
5. **H5 (Draft-picking extensive-form simulation)**: Forward simulation of sequential drafting over the 36 partitions reveals unavoidable envy trapping states. (Guessed chance: 30%, Cost: Low).
6. **H6 (Social choice Arrow-type preference cycle obstruction - Imported)**: In bounded bundle partitions, top-tier item concentration forces later agents into unavoidable EF1 deficits. (Guessed chance: 35%, Cost: Low).
7. **H7 (Spectral graph theory envy-graph Laplacian - Imported)**: Directed acyclic envy conditions impose spectral constraints that are incompatible with the bipartite bundle graph matching structure. (Guessed chance: 20%, Cost: Medium).
8. **H8 (Zero-sum adversarial game saddle point - Wildcard)**: A two-player zero-sum game between an adversary choosing $V$ and a planner choosing $A \in \{1..864\}$ yields a strictly positive game value $> 0$, proving no allocation is universally valid. (Guessed chance: 40%, Cost: Medium).

## Decisive Tests Executed
1. **Test 1 on H1 (Primal SMT integer search)**: Formulated exact SMT model with 32 integer variables $v_{i,g} \ge 0$, $\sum_{g=1}^8 v_{i,g} = 100$, and 864 disjunctive obstruction clauses. Result: **SAT** in 12.8s. Produced explicit $4 \times 8$ integer matrix. **CONFIRMED**.
2. **Test 2 on H3 (Universal order-invariant counterexample)**: Formulated simultaneous 24-permutation SMT search (20,736 clauses). Result: Solver timed out (`unknown`). The current matrix refutes order $(1, 2, 3, 4)$ with 0 valid allocations, but other orders admit 5–21 valid allocations. **DEAD / SCOPED to prescribed order**.
3. **Test 3 on H8 / Exact Verification**: Evaluated the discovered valuation matrix against every single one of the 864 allocations generated from group constraints using exact integer and rational arithmetic (`fractions.Fraction`). Found: exactly 0 allocations valid; 828 allocations fail ordered no-envy, 36 allocations fail EF1. Minimum violation margin is strictly $1/100 > 0$. **CONFIRMED**.
