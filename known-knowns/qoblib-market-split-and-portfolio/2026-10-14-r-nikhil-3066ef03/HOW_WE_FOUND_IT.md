# How we found it (contributor text, unverified)

**Brief.** QOBLIB class 06 (multi-period portfolio with transaction costs and short selling), instance
`po_a200_t10_orig`, budget 50, lambda 0.01. The official table has no row for a200 instances; two open pull requests
post values, the better being −551385 (PR #87), whose authors note their method is weak at high lambda.

**What failed.** Local search with one- and two-asset block moves from PR #87's portfolio stalls at once (it is a
local optimum of that neighbourhood); iterated local search from it gains only ~0.5%. Cold starts are far worse. A
compiled simulated annealer (single, transfer and pair moves, exact deltas) did not improve the final portfolio in ten
runs with different temperature schedules (up to 8e9 proposals each). Plain LLL plus Babai rounding toward the relaxed optimum leaves large risk residuals.

**What worked.** The covariance in every period is a 30-day sample covariance of rank 29, so integer baskets whose
29-dimensional factor exposure nearly cancels carry almost no risk: a closest-vector problem more than a quadratic
one. A continuous relaxation (risk on the 29 factors; about −836k) showed large headroom. Rounding it and descending
exactly gave −552k to −565k; iterated local search from those reached −596k. Since good portfolios re-trade ~90% of
their units every period, periods nearly decouple: an exact chain DP that mixes periods from different solutions,
followed by rounds of per-period local search with both neighbours fixed, reached −691624.
