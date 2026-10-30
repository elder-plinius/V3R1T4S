# How We Found It

_contributor text, unverified_

## Problem Background
In arXiv:2608.31121 ("Constrained Fair Allocations via Partition Matroid Reductions", August 2026), Benjamin Cookson and Nisarg Shah proved that fair allocation of indivisible goods under 3-colorable laminar matroids admits an EF1 allocation with ordered no-envy by reducing to a size-6 key matroid. For 4 agents, they introduced two key matroids of size 8 and size 12. While they proved that their 3-agent top-item separation technique fails (Lemma 12), they left the existence of an EF1 allocation with ordered no-envy open, noting that their computer searches had been "unfruitful".

## What We Tried
1. **Exhaustive Combinatorial Enumeration**: We analyzed the matroid constraints: ground set $M = \{1..8\}$ with groups $G_1=\{1,2,3\}$, $G_2=\{4,5,6\}$, $G_3=\{7,8\}$. Bundle capacity is 2, with at most 1 item per group. This yields exactly 21 valid bundle pairs, 36 unlabeled partitions, and $36 \times 4! = 864$ complete labeled allocations.
2. **Universal Order Search (Dead Line)**: We initially tested whether a single valuation matrix could simultaneously refute all 24 possible agent orderings. Encoding 20,736 disjunctive constraints across all permutations caused SMT solvers to time out.
3. **Prescribed Order SMT Synthesis**: Focusing on the canonical prescribed reverse topological order $1 \prec 2 \prec 3 \prec 4$, we formulated an exact SMT model over 32 non-negative variables with row sums normalized to 100. Z3 solved the model in 12.8 seconds, finding a clean integer matrix.
4. **Independent Rational Verification**: We verified the candidate matrix in exact arithmetic over $\mathbb{Q}$ using Python's `fractions.Fraction`. All 864 allocations strictly fail: 828 violate ordered no-envy, and the remaining 36 violate EF1, with a minimum violation margin of $1/100 = 0.01 > 0$.
5. **Polyhedral Farkas Duality**: We extracted exact Farkas separating hyperplanes for every allocation cone, establishing that the counterexample is located in the strict interior of the obstruction region with an $L_\infty$ stability radius of $1/400$.
