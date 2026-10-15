# CRITERION verdict

context: codex exec (fresh context via codex-fresh)

confirmed_scope: For every real x,y,z>0 with x<y in the all-in game defined in the source paper, f(x,y,z)-f(y,y,z) is at least 379/1813985280>0.

criterion_met: Full success criterion (B), by a computer-assisted exact region proof.

The statement in `CLAIM.md` and `target.md` agrees literally with Conjecture 9 in Section 5.3 of the source. The six equally likely ordered winner/loser outcomes, transfer of the smaller stack, and stopping at the first zero stack agree with the abstract and Section 1. The comparison preserves the second and third initial stacks; it neither swaps players nor imposes equal initial totals. No integer, rational-only, generic-position, bounded-ratio, or almost-everywhere restriction has been introduced.

## Continuous coverage and analytic bounds

I checked the mathematical argument in `PROOF.md` independently of the replay result. Positive scaling maps every admissible triple into exactly one of the three stated normalized domains. The leader domain includes its open z=y edge, and the shortest domain includes its open z=x edge. The omitted outer edges and vertices violate positivity or x<y. The middle domain supplies the remaining strict ordering.

The relative-interior convention is sound: an affine function nonnegative at every vertex and positive at some vertex is positive throughout the relative interior. When a line crosses that interior, the relative interiors of the negative closure, equality section, and positive closure partition it. This remains true for segment splits, whose equality child is a point. Thus boundary signs cannot silently be treated as generic signs. The replay checks all roots, reconstructed child hulls, references, and reachable nodes. It verifies 1,291 point leaves, 3,280 segment leaves, and 1,990 two-dimensional leaves, including internal equality faces.

Every live pair has at most one continuing outcome; a tied pair has none. Consequently survival through n rounds is at most 2^-n. With at most two immediate player-1 eliminations and three continuing outcomes, the constant 4/5 is a valid supersolution because (2+3(4/5))/6=11/15<=4/5. Induction on cumulative finite-horizon probabilities and their increasing limit establishes 0<=f<=4/5 without assuming the desired inequality. This justifies the recursion's terminal interval for the infinite-horizon quantity.

For an unresolved pair containing player 1, its two outcomes contribute between 0 and 1+4/5 before division by six; for the other pair the upper bound is 4/5. These are valid simultaneous region bounds even where the comparison changes sign. Resolved unequal pairs contribute the immediate elimination and the unique live successor; exact ties terminate both outcomes. Induction therefore validates each recomputed interval. This is not an inference from finite-depth positivity with an omitted tail.

## Replay and exactness

I ran `python3 portable/run.py` to completion. It returned PASS in about 39 seconds. `review/portable-replay.log`, `portable/output/`, and `review/transcript-audit.json` preserve the evidence. All four stored bound numerators were recomputed on every leaf, rather than accepted from a stored minimum or transcript hash.

| Domain | Nodes | Leaves | Verified minimum separation |
|---|---:|---:|---:|
| z>=y | 128 | 86 | 181/1399680 |
| x<z<y | 7 | 5 | 1/135 |
| z<=x | 9704 | 6470 | 379/1813985280 |

I inspected `portable/independent.py` and `portable/independent_memo.cpp`. They import no prover implementation: geometry uses rational hulls and clipping, and the bounds kernel evolves stack values at vertices rather than the prover's affine coefficient states. Its memoization is over the full evaluated state and remaining depth. The geometry checks use unbounded rational arithmetic; the kernel uses integers with explicit size guards. For these certificates the maximum homogeneous coordinate is only 3937, there are at most six vertices per region, and depth is at most 13, comfortably within the audited arithmetic limits. The positive common minimum follows from these exact bounds over the finite exhaustive partition.

## Null models and scope checks

I wrote `review/scalar_checks.py` directly from the six ordered outcomes, without importing supplied verifier or prover modules. Its exact finite-horizon propagation checks probability conservation, the survival bound, the all-equal value 1/3, scaling, and interchangeability of the two opponents. It also checks both admissible outer equality cases, representatives of all three minimum-bound leaves, and the near-degenerate point (x/y,z/y)=(999999999999/1000000000000,1/10000000000). Every resulting scalar enclosure lies inside the corresponding certified enclosure and has a positive rigorous comparison margin; results are in `review/scalar-checks.json`. These controls supplement the continuous proof and are not used as a sampling-based substitute for it. The all-equal null also confirms why x<y must remain strict.

The source's proved Theorem 1 compares permutations of one stack triple. It does not subsume this comparison of different triples, and the martingale formula for eventual overall victory is a different probability. A generic MeshItUp procedure or an unsuccessful finite-depth LP calculation alone would not meet the criterion; the supplied complete partition and verified positive bounds do.

Fresh primary-source checks are recorded in `review/current-source-receipts.json`. The current arXiv page lists only v1, whose Section 5.3 still states this exact conjecture and describes its attempted computation as incomplete. The author's current main commit and both other branches match the supplied source artifacts; the other branches are behind main. I found no subsuming result in these checked sources or in the supplied related papers. This is a bounded source check, not a claim of exhaustive bibliographic coverage.

All three named orderings are established together, so this qualifies as the full win rather than merely one instance of partial p1. It is a computer-assisted proof with a checked analytic bridge, not a claimed Lean, Coq, or Isabelle formalization.

pass: true