Registered UTC: 2026-10-15T10:36:57.321642+00:00

Criterion (verbatim):
Settle Angel-Holmes Conjecture 9 as stated in arXiv:2410.15329 Section 5.3 (direction: settle, either way), for the game exactly as defined in that paper's abstract and Section 1. EITHER (A) COUNTEREXAMPLE: explicit positive rationals x < y and z with f(x, y, z) <= f(y, y, z), proved by rigorous enclosures: f(s) lies in [h_n(s), h_n(s) + 2^-n] where h_n(s) is the exact (rational) probability that player 1 is eliminated first within n rounds, so it suffices to exhibit n with h_n(x, y, z) + 2^-n <= h_n(y, y, z), computed in exact rational arithmetic (or interval arithmetic with directed rounding) by a checker that shares no code with the search. OR (B) PROOF: a machine-checked proof (Lean, Coq or Isabelle, no sorry/axioms) or a computer-assisted proof whose certificate (region partition plus the bounds used in each region, in exact arithmetic) is verified by an independent checker, that f(x, y, z) > f(y, y, z) for ALL real x, y, z > 0 with x < y.

Partial p1 (verbatim):
A certified computer-assisted proof of Conjecture 9 on one of the three orderings of z separately, with an independently verified certificate: z >= y (player 3 is the chip leader), or z <= x (player 3 is the shortest), or x < z < y. All three together are the full win (B).

Statistic: exact cumulative elimination probability H_n (the bank h_n; the paper uses h_n for exactly round n). A rational counterexample requires H_n(x,y,z)+2^-n <= H_n(y,y,z), x<y and all positive. A proof requires a finite exact region partition with sound inequalities covering an entire named ordering, including every admissible equality boundary; no finite grid stands for continuous coverage. Region bounds may use sharper rigorously derived survival tails, but any claim must imply the literal conjecture. Checker shares no code with the search/prover.

null_test: not needed because the candidate is an explicit rational counterexample or a deterministic exact-arithmetic region certificate, judged against a mathematical inequality; randomized search diagnostics are not statistical claims.

Compute: at most four single-thread workers and total memory below 7 GB, disk below 6 GB. setpriority was denied in preflight; therefore only short capped compute chunks (under one minute), with serialized checkpoints between chunks, and proof work. No long jamfold job. No new research line after minute 84; report and check_run by minute 110.
