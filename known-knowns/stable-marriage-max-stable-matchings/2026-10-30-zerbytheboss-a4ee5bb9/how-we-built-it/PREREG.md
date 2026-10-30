# PREREG — stable-marriage-max-stable-matchings

frozen: 2026-10-30T06:25:00Z
target: stable-marriage-max-stable-matchings
null_test: not needed because deterministic combinatorial enumeration of all stable matchings by two independent exact counting algorithms against an explicit OEIS table lower bound

## Problem Definition
Given order $n \ge 6$, find explicit complete strict preference lists for $n$ men and $n$ women whose number of stable matchings strictly exceeds the best known value (the composition closure) at verification time.

## Success Criterion (Verbatim)
Success means explicit preference lists for some n >= 6 (n men and n women, each list a permutation of the other side) whose number of stable matchings, counted exactly by two independent methods that agree, is STRICTLY GREATER (direction: max) than the best known value for that n at verification time. The best known value is the composition closure, not the A357271 data line (which is stale: its odd terms predate the Ong et al. file and its even terms predate composing those instances): the largest count over every instance published for that n (the A357271 data line and its linked file a357271_1.txt, any other OEIS entry or b-file, any paper or preprint, M. Jo's order-7 instance) or merged into this repository (known-knowns/, TROPHY_CASE.md), AND over every composition of such instances (doubling, i.e. the lexicographic product with Knuth's order-2 instance, other products, and Thurber's compositions). The claim must say whether its object is a composition and name its parts; a composition of known instances alone is not a claim. Values in unmerged pull requests are not bars, since they can move without anything being published. One cell per claim. A count above a value conjectured exact on A357271 (n = 6, 8, 10, 12, 16) would refute that conjecture and needs an extra independent recount. Submitting a new value to OEIS is an action for a human.

## Targeted Cells & Thresholds
- Primary Target: $n = 17$
  - Literature baseline: OEIS A357271 lists $a(17) = 200,832$.
  - Composition closure: Since 17 is prime, no non-trivial composition of smaller instances exists. The composition closure at $n=17$ is exactly $200,832$.
  - Winning threshold: Exact stable matching count $\ge 200,833$.

## Verification Methods
1. Method 1: Irving-Leather rotation poset closed-subset (down-set) enumeration with memoized bitsets.
2. Method 2: Gusfield breakmarriage recursion / verified lattice walk verifying that every visited matching is stable by the direct blocking-pair definition.
3. Both methods must execute independently, share zero code or memory, and produce identical counts.
