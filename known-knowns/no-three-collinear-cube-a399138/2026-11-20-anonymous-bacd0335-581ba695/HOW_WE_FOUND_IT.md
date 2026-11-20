# How we found it

**Contributor text, unverified.** (The machine-checked facts live in `panel/` and `verify-it-yourself/`; this is the narrative, not a claim.)

The brief was the `no-three-collinear-cube-a399138` target: find an explicit improvement to a published record table, where a fast exact evaluator is available. The 7x7x7 no-three-in-line cube had a wide open window (73 to 98) and reused certification machinery already built for earlier work in the same hunt: a SAT encoder plus drat-trim receipt pipeline.

Three lenses ran in parallel that night: an LP dual packing bound (gave 98, not tight enough alone), a quadratic-surface greedy construction (found a 66-point admissible set — a lead, not a record), and a SAT "ceiling-saturation" model. The ceiling idea came from an elementary counting fact: any 98-point admissible set must hit every one of the 147 axis-parallel lines with exactly 2 points (3 incidences per point x 98 points = 294 = 2 x 147, and no-three-collinear forbids more than 2 per line). That turns "does a 98-point set exist" into a small, concrete decision problem: is the "exactly-2-per-axis-line, at-most-2-per-any-line" model satisfiable? CaDiCaL said no, with a proof; drat-trim verified it.

Calibration before trusting the result: the encoder pipeline was run on n=3 and n=4 (the run itself), where the true values (16 and 28) are already known, and it reproduced them exactly (UNSAT at the ceiling, SAT at the true K, UNSAT at K+1). The reproduce reviewer separately calibrated n=2 and n=3 with a fully independent encoder, and the criterion reviewer calibrated n=4 with an independent encoder built on the claimant's line-enumeration helper (`n3l.py`) only. That gave confidence the encoder wasn't accidentally unsatisfiable for a trivial reason before trusting it at n=7.

What failed: the LP dual bound alone (98, not an improvement) and the smaller "decision" question at m=74 (still running when the night's attack window closed — a separate, still-open lead, not part of this submission).

What a three-skeptic panel added beyond this account: the reproduce reviewer's fully independent rebuild of the encoder from the bare definition (not reading this code at all), which came out clause-for-clause identical and was solved and verified completely separately; a second, structurally different encoding of the same question (an explicit cardinality counter instead of the counting shortcut), also UNSAT with its own verified proof; and a hand-check of the counting argument itself, done programmatically rather than by eye.
