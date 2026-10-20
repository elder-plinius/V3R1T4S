# How we found it

**Contributor text, unverified.** This account is not part of the independently verified claim.

Starting from the repository's 6 630-vertex graph, we sought one additional vertex while preserving maximum degree 13 and diameter at most 4. A greedy radius-3 cover selected eight attachment vertices. Edge pivots freed attachment slots, and a screened simulated annealer repaired distance violations.

The constructor's recorded pivot-chain costs were 268 → 145 → 108 → 79 → 57 for seeds 31–34. Further annealing produced the submitted object. The object, rather than the heuristic search trajectory, is the result of record: verify it with `sh verify-it-yourself/run_checks.sh`.

Unsuccessful greedy insertion searches do not prove insertion impossible. Exploratory voltage-lift and sampled-lift experiments are omitted because their implementations and timing claims were not sufficiently validated. No completeness, optimality, or literature-wide novelty is claimed.

Search source is included in `how-we-built-it/`; it requires numpy and numba. This package does not promise a complete deterministic reconstruction of the search. Verification of the supplied graph uses only the Python standard library.
