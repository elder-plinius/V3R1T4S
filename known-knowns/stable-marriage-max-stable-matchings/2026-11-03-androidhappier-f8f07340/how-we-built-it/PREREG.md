# PREREG (frozen 2026-11-03T15:56:05Z, before any search output exists)
id: stable-marriage-max-stable-matchings
criterion (verbatim): see target.md (bank success_criterion).
cells: n = 9 (bar 365, Ong et al. a357271_1.txt), n = 11 (bar 1690, same file), n = 13 (bar 7698, merged known-knowns
2026-10-14-r-nikhil-ec9b2daf). Bars re-read from data/ files fetched 2026-11-03T15:55:29Z; composition closure for these odd
n is no higher than those instances (odd n cannot be a product of the order-2 instance; recorded composition values
330, 1231, 6720 are below them) - to be rechecked before any claim.
statistic / checker: exact count of stable matchings by smcount3.c (rotation-poset ideal DP, with lattice-walk cross check)
and, independently, count_stable.py --brute (exhaustive enumeration, different code) - must agree.
threshold: count STRICTLY GREATER than the bar for that n. Ties = nothing.
null_test: not needed because the object is an explicit instance whose count is computed exactly by deterministic checkers against a table value.
search: iterated local search (smcount3 climb), warm starts from the published/merged instances, plus cold random starts.
