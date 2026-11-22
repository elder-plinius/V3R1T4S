# PREREG (frozen 2026-11-01T23:45:17Z per date -u, before any n = 8 output exists)

Target: windmill-kn2-harmonious-graham-sloane, cell n = 8 (q = 56).

Criterion (bank, verbatim): Success means, for n = 8, EITHER (a) an explicit assignment of 15 distinct residues mod 56
to the vertices of K_8^(2) such that the 56 edge sums are pairwise distinct mod 56 (refuting the conjecture), OR (b) a
certified proof that no such labeling exists: an exhaustive search by two independent programs, or a SAT/CP encoding
whose UNSAT result carries a DRAT/LRAT proof checked by drat-trim or cake_lpr plus an independent second method, with
every symmetry reduction used (translation f -> f+t, multiplication by a unit mod 56) justified in the write-up.
Before claiming, re-check the latest DS6 edition (Table 2, 'windmills') and the literature for a published decision
of K_8^(2).

Statistic / checker:
- (a) branch: any labeling output is accepted only if check_label.py (written from the definition) prints VALID:
  15 distinct residues mod 56, 56 edge sums pairwise distinct.
- (b) branch: program P1 (C backtracker wsearch.c) and program P2 (independently written, different algorithm:
  meet-in-the-middle join over sum masks) must both report 0 labelings for n = 8, with the only reduction being
  translation (f(c) = 0), justified in writing. Consistency requirement: P1 and P2 report the same number of
  sum-distinct 8-sets of Z_56 containing 0, and both reproduce the known small cases (n = 4 harmonious with the same
  number of solutions; n = 3, 5, 6, 7 not harmonious). Any disagreement = no claim.
- Optional third method (solver-based, e.g. CP-SAT/pysat) reported as supporting evidence only.
Thresholds: exact agreement (integers), no tolerance.

null_test: not needed because the claim is an exhaustive decision (or an explicit object) checked by deterministic
exact programs against a definition, not a search score or a "beats chance" statistic.
