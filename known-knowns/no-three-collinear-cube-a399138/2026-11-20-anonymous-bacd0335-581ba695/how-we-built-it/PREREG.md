# PREREG — frozen 2026-11-20 14:32 UTC (before any attack output)

Criterion (bank, verbatim): p1 = exact a(7) — witness of size m + checked DRAT/LRAT (or cake_lpr-verified) unsat proof for m+1. p2 = certified upper bound a(7) <= 97 (any bound below trivial 98), checked unsat proof without matching witness.

Statistics and thresholds:
- Lens A (dual packing bound): the bound is B = 2 * sum(w) for fractional line weights w >= 0 covering every grid point by total incident weight >= 1. Claim level "progress" only if B < 98 with the weight file saved and an independent pointwise verification script recomputing every cover constraint. B < 98 is NOT p2 by itself (p2 demands a checked UNSAT proof); it is a lead and a target for a SAT/LP certificate.
- Lens B (quadratic-surface construction): a 74-point admissible set (verified by the definition checker, every line <= 2) is a p1-half (witness) — still needs UNSAT at 75 for p1. Any set of size 74+ counts as a major lead regardless.
- Lens C (ceiling-saturation SAT at 98): decide satisfiability of "exactly 2 per axis-parallel line + at-most-2 per other line". UNSAT with a drat-trim-verified receipt => candidate p2 (a(7) <= 97), pending panel. SAT => 98 reachable (record object). UNKNOWN (timeout) => log, stop, no extra nights.
- Calibration gate: the line enumerator + checker must be tested on one known positive (small hand-built admissible set) and one known negative (3 collinear points) before any lens output is scored.

null_test: not needed because the claims are explicit objects checked by a deterministic checker against table values (LP dual weights verified constraint-by-constraint; SAT verdict via drat-trim on a saved receipt) — no "beats chance" statistical claim is made.
