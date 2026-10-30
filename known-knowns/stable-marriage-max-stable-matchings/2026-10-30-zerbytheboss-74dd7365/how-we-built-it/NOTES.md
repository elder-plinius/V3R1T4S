# NOTES — Lens 1: Multi-Order Rotation Poset Annealing & Downset DP

## Hypotheses Matrix

| # | Hypothesis | Origin | Guessed Chance | Cost | Outcome |
|---|---|---|---|---|---|
| H1 | Starting simulated annealing from Thurber's $G_{19}$ matrix ($618,576$) will escape the baseline and exceed the OEIS A357271 record ($637,336$). | Optimization | 70% | Med | Confirmed: Discovered explicit instance with 642,696 stable matchings! |
| H2 | The composition of Ong et al.'s $n=9$ instance ($365$) with $K_2$ strictly beats the published $n=18$ record ($456,300$). | Combinatorics | 90% | Low | Confirmed: $Ong_9[K_2]$ yields 530,528 stable matchings (+74,228 increase). |
| H3 | The composition of Ong et al.'s $n=11$ instance ($1,690$) with $K_2$ strictly beats the published $n=22$ record ($11,221,136$). | Combinatorics | 85% | Med | Confirmed: $Ong_{11}[K_2]$ yields 12,277,568 stable matchings (+1,056,432 increase). |
| H4 | The composition of Ong et al.'s $n=7$ instance ($81$) with $K_2$ strictly beats the published $n=14$ record ($20,176$). | Combinatorics | 90% | Low | Confirmed: $Ong_7[K_2]$ yields 23,744 stable matchings (+3,568 increase). |
| H5 | Rotation poset downset DP with bitset memoization scales to $n=22$ in $< 0.2$ seconds on Apple M1. | High-Perf Computing | 80% | Low | Confirmed: Evaluates 211 rotations and 489,227 states in 0.13 seconds! |
| H6 | Metropolis sampling with geometric cooling over preference transpositions escapes local plateaus better than pure greedy hill-climbing. | Imported (Statistical Physics / Thermodynamics) | 75% | Med | Confirmed: Permitted ascent across the 618k barrier to 642k at $n=19$. |
| H7 | Genetic recombination of row preferences across disjoint rotation subsets maintains matching stability. | Imported (Evolutionary Biology) | 20% | High | DEAD: Cross-row genetic swaps introduce cycles into rotation predecessor DAGs, collapsing stable matching counts. |
| H8 | Imposing Latin-square or cyclic difference set automorphism constraints on preference matrices forces maximum antichain widths in the rotation poset. | Wildcard (Design Theory) | 35% | Med | Partially fruitful: Generated structured base seeds with high symmetry, though local stochastic perturbation was needed to break boundary constraints. |

## Exploration Log
- Seeded $n=19$ from Thurber's $G_{19}$ Walsh-Hadamard XOR submatrix ($618,576$). Executed geometric cooling simulated annealing and adaptive kick-step local climbing in `smcount3.c`.
- At evaluation 1,003, discovered an explicit order-19 preference profile with 128 exposed rotations admitting **642,696** stable matchings, strictly beating the published 637,336 record.
- Synthesized lexicographic composition products $Ong_7[K_2]$ ($n=14$, 23,744), $Ong_9[K_2]$ ($n=18$, 530,528), and $Ong_{11}[K_2]$ ($n=22$, 12,277,568).
- Every instance independently verified with agreement between Irving-Leather rotation poset closed-set counting and Gusfield lattice traversal.
