# How we found it (contributor text, unverified)

**Brief.** QOBLIB class 06 (multi-period portfolio with transaction costs and short selling), instance
`po_a200_t10_s00`, budget 50, lambda 0.01. The official table has no row for a200 instances; two open pull requests
post values, the better being −401535 (PR #87), whose authors note their method is weak at high lambda.

**What we reused.** A day earlier the same pipeline beat the posted values on the sibling instance `po_a200_t10_orig`
(a separate package). Its key observation carries over: each period's covariance is a 30-day sample covariance of
rank 29, so integer baskets whose 29-dimensional factor exposure nearly cancels carry almost no risk, and good
portfolios re-trade ~90% of their units every period, so periods nearly decouple.

**What worked.** Relaxation + rounding (−487k), two local-search books (−517k), an exact chain DP mixing periods across
solutions (−520k), then rounds of per-period local search with both neighbours fixed plus the chain DP over every
period's pool of local optima: 6 rounds reached −618978, 60 more rounds with fresh seeds −644342. Gains per round fell
from ~1.5k to ~0.2k and the last seven rounds found nothing, so this neighbourhood is close to its limit.

**What we checked against ourselves.** Two independent exact evaluators agree; the comparison survives every
rounding tie rule (200 exact 5/2 ties shift both our value and the bar by 23); the format has no overlaps or
out-of-range counts.
