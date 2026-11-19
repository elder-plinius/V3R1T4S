# PREREG covering-designs-record (run 2026-10-19-2300)
date_utc: Mon Oct 19 23:03:00 UTC 2026
Frozen before any attack output of this run exists (the lead file data/lead_C29_5_3_399_from_run1303.txt was produced
by run 2026-10-19-1303 and is scored here for the first time).

success_criterion: copied verbatim into target.md from repo/bank/targets.json (checked by string match).

cell: C(29,5,3) (v=29, k=5, t=3; C(29,3)=3654 triples, far below the 5e9 same-day limit). Schonheim L(29,5,3)=366.

statistic: b = number of blocks of an explicit design file for which BOTH tools/check_cover.py (independent checker
written in this run from the definition) and the run-1303 checker print VALID: every block a 5-subset of 1..29 with
distinct points, all 3654 3-subsets covered, no duplicate blocks.

comparisons: (a) LJCR GitHub coverdata.json size (data/coverdata.json, fetched this run); (b) the live
coveringrepository.com plain (29,5,3) value; (c) any value for C(29,5,3) found in a GitHub/arXiv search (last 6 months).
thresholds: a lead iff VALID and b < every value in (a)-(c) that could be read and b >= 366. A tie is not a record.
If (b) cannot be read with one honest request, the result is PENDING TABLE CHECK, never PROMISING or better.
Only a lead below a read live value (b) could be called PROMISING (single-context, unpanelled).

lens evaluator: independent checker, self-tested on a known positive (the published 2022 LJCR design is not stored
locally, so the positive is a design built here and checked by both checkers) and a known negative (the lead with one
block removed must be INVALID); then score the lead; then honest status reads.
lens optimizer: warm-started local search from the 399 lead: delete one block, then tabu/simulated-annealing moves
(replace one block by another 5-set) minimising the number of uncovered triples; success at u=0 with b-1 blocks,
repeat. Hard cap 12 min wall clock at nice 10. Any result of this lens is CAPPED (a local search never excludes).

null_test: not needed because any claim would be an explicit design checked by a deterministic exhaustive coverage checker against a fixed table value (no score against chance, no key, no statistical claim).
