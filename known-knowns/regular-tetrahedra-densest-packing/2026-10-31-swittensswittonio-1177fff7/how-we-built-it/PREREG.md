# PREREG (frozen)
Frozen at: 2026-10-31T06:01:00Z (date -u). No attack output of this run has been scored yet. Preceding: scout, copy of the previous run's checker
(checker/tetra_check.py, sha256 1ca6bdaf45e07259d45190d9cb650967ab7d9313d08ee1ac611f342b479e5499) and a rerun of its baseline and selftest (baseline/).

null_test: not needed because every claim is an explicit object (lattice and tetrahedra, exact rational coordinates) checked by a deterministic exact checker against a table value (4000/4671), or a re-runnable interval computation for an upper bound; no statistical or search-significance claim is made.

## Criterion (verbatim, bank success_criterion and partial wins)
See target.md (verbatim copy). Main: a periodic packing of exactly regular tetrahedra, pairwise disjoint interiors (exact
separating plane per pair incl. lattice translates within the circumradius cutoff), density k*(a^3/(6*sqrt2))/|det L| STRICTLY
GREATER than 4000/4671 and than any denser published value at verification time. p1: primitive cell with k != 4, certified density > 100/117.
p2: rigorous upper bound strictly below 1 - 2.6e-25, machine-checked or a re-runnable exact/interval computation re-executed by the skeptic, with a matching written reduction.

## Judging instrument
checker/tetra_check.py check_packing(L, bodies): exact integer arithmetic; fails unless (a) six equal squared edges within and across bodies,
(b) U^2 = (a^2)^3/72, (c) every pair (i, j, lattice translate within 2R) has a weak separating axis among face normals and edge-edge cross
products, found and then tested against all 8 vertices, (d) density = k*U/|det L| exact Fraction.
Thresholds: main claim = ok AND density > Fraction(4000,4671); p1 additionally primitive k != 4 (primitive_k after an exact test that no
nonzero fractional lattice translation maps the body set onto itself) and density > Fraction(100,117). Ties and float-only or
tolerance-based overlap results are never claims.
For p2 in this run: a lens claim must (i) strictly improve on the density bound of the previous run's package (1 - 1.0215562e-15, draft PR #863)
or (ii) remove one or more of its stated conditions (GEK Lemma 3.3 / Lemma 3.5 / K3 construction) by a re-runnable interval or exact
computation with a written reduction, and in either case the bound must still be < 1 - 2.6e-25. A claim of type (ii) is a
confirmation of the conditional claim's inputs, not a new bound, and is scoped as such.

## Baseline (calibration named by the criterion)
CEG double dimer packing, arXiv:1001.0586v3 Theorem 1 (data/arxiv_1001.0586v3.txt, sha256 4a406d450ae336a0e81053358d18bc567aa41e9449dcbd61ff4af5ddbf4a7d5c);
code checker/tetra_check.py; data version arXiv v3, deterministic; metric exact density; expected score 4000/4671 exactly, tolerance 0
(baseline/baseline_output.txt, rerun this run: equal True). Secondary calibrations KEG 100/117 and Torquato-Jiao 12250/14319 (baseline/selftest_output.txt).
If it misses, the comparison is unresolved and no improvement is claimed.

## Lens evaluation rules
A lens may use any method; whatever it reports as a claim must pass the instrument above. Float densities in lens reports are NUMERICAL.
A lens is dead only when report.md documents at least 3 dead lines.
