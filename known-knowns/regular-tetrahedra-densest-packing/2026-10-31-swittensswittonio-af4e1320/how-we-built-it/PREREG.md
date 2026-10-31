# PREREG (frozen)
Frozen at: 2026-10-31T00:53:37Z (date -u). No attack output has been scored yet. Only the literature scout and a checker
self-test (checker/tetra_check.py --selftest, run before this file as a tool test) precede it; the baseline run below is
scored after this freeze.

null_test: not needed because every claim is an explicit object (lattice and tetrahedra, exact rational coordinates) checked by a deterministic exact checker against a table value (4000/4671); no statistical or search-significance claim is made.

## Criterion (verbatim, bank success_criterion)
See target.md. In short: a periodic packing with exactly regular tetrahedra, pairwise disjoint interiors (exact
separating plane per pair incl. lattice translates within the circumradius cutoff), and density k*(a^3/(6*sqrt2))/|det L|
STRICTLY GREATER than 4000/4671 and than any denser published value at verification time.
Partial wins p1 (primitive cell with k != 4 tetrahedra, certified density > 100/117) and p2 (rigorous upper bound strictly
below 1 - 2.6e-25, machine-checked or re-runnable exact/interval computation) as quoted in target.md.

## Judging instrument
checker/tetra_check.py check_packing(L, bodies): exact integer arithmetic; fails unless (a) six equal squared edges within and
across bodies, (b) U^2 = (a^2)^3/72, (c) every pair (i, j, lattice translate within 2R) has a weak separating axis among face
normals and edge-edge cross products, found and then tested against all 8 vertices, (d) density = k*U/|det L| exact Fraction.
Claim thresholds: ok == True AND density > Fraction(4000,4671) (main); for p1 additionally k_primitive != 4 and density >
Fraction(100,117), where k_primitive is the body count after an exact test shows no nonzero fractional lattice translation maps
the body set onto itself (a 4-per-cell or a supercell-of-dimer packing does not count). Density <= 4000/4671 is not a main
claim; a tie is not a record. A float-only or tolerance-based overlap result is never a claim. A packing found by a lens counts
only after check_packing returns ok on rational coordinates written to a file.

## Baseline (calibration named by the criterion)
- Baseline: Chen-Engel-Glotzer double dimer packing, arXiv:1001.0586v3 Theorem 1 (data/arxiv_1001.0586v3.txt,
  sha256 4a406d450ae336a0e81053358d18bc567aa41e9449dcbd61ff4af5ddbf4a7d5c).
- Code: checker/tetra_check.py (this run's checker), construction from the paper's Eq. (1),(2),(6) and Theorem 1 Eq. (15),(16).
- Data version: arXiv v3, no split or seed; deterministic.
- Metric: exact density k*U/|det L| with k=4 tetrahedra per cell of L+ = span(a+b, b+c, c+a).
- Expected score: 4000/4671 exactly. Tolerance: 0 (exact rational equality). Secondary calibrations: KEG 100/117 and
  Torquato-Jiao 12250/14319 (paper Sec. II.5).
- If it misses, the comparison is unresolved and no improvement is claimed.

## Lens evaluation rules
A lens may use any method; whatever it reports as a claim must pass the instrument above. Density numbers in lens reports are
exact Fractions printed by the checker, or labelled NUMERICAL (float) if they come from a search stage. A lens is dead only
when report.md documents at least 3 dead lines.
