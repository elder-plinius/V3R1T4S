# PREREG covering-designs-record (run 2026-10-20-1253)
date_utc: Tue Oct 20 12:57:48 UTC 2026
Frozen before any attack output of this run exists.

success_criterion: copied verbatim into target.md from repo/bank/targets.json.

cells: C(v,k,3), k in {5,6}, v in 29..40, excluding C(29,5,3) (PR #572) and C(20,6,3) (PR #353).
statistic: b = number of blocks of an explicit design file that tools/check_cover.py prints VALID for (every block a
k-subset of 1..v with distinct points, all C(v,3) triples covered, no duplicate blocks), and b >= Schonheim L(v,k,3).
comparisons: (a) LJCR GitHub coverdata.json size (data/coverdata.json, fetched this run); (b) the live
coveringrepository.com plain (v,k,3) value; (c) any value for that cell found in a GitHub/arXiv search (last 6 months).
thresholds: a lead iff VALID and b < (a) strictly. A tie is not a record. (b) cannot be read by machine (PENDING TABLE
CHECK), so a lead below (a) stays a lead, never PROMISING, until a human reads (b) by hand and it is above b; only then
PROMISING (single-context, unpanelled) and a panel.

lens structured: exact orbit set cover (CP-SAT) under intransitive G-sets of PSL(2,7), A5, S5 and new groups, per job
cap 60-90 s, 2 CP-SAT workers per job, nice 10, timeout. Capped rows are CAPPED (never exclusions); OPTIMAL rows are
exhaustive for their own (cell, G-set) only.
lens solver: subgroup refinement of the best near-miss covers, warm-started with the full-group solution as a hint,
longer caps (<= 300 s per job); plus exact LNS re-cover. All CAPPED unless OPTIMAL.

null_test: not needed because any claim would be an explicit design checked by a deterministic exhaustive coverage checker against a fixed table value (no score against chance, no key, no statistical claim).
