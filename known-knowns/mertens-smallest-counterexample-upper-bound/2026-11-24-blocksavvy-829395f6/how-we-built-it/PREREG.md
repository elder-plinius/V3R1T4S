null_test: required
frozen_utc: Tue Nov 24 07:32:35 UTC 2026 (date -u, written before any h evaluation, zero computation or lattice run of this session)

# PREREG: Mertens first-counterexample bound (bank id mertens-smallest-counterexample-upper-bound)

## Definitions (frozen)
For each zeta zero rho = 1/2 + i*gamma (gamma > 0): alpha = 1/|rho zeta'(rho)|, psi = arg(rho zeta'(rho)).
h_StR(y) = 2 * sum_{0 < gamma < 74000} alpha * exp(-3e-9 gamma^2) * cos(gamma*y - psi)      (Saouter-te Riele, via KN (2.7))
h_P(y)   = 2 * sum_{0 < gamma < 14000} alpha * exp(-1.5e-6 gamma^2) * cos(gamma*y - psi)   (Pintz, KN Thm 2.1)
Zeros: my own computation with python-flint 0.9.0 acb.zeta_zeros (FLINT/Arb, rigorous isolation by index),
working precision 256 bits; zeta'(rho) from acb_series(...).zeta() on the zero's ball. Completeness: zero number
N+1 (by rigorous index) has gamma > cutoff and zero N has gamma < cutoff. KN's Zenodo zeros are used ONLY as a
cross-check of my zeros (agreement of gamma, alpha, psi), never as an input to a certified value.
y values are evaluated at their exact printed decimal expansion.
Certified statistic: the arb ball of h(y) at prec 256, recomputed at prec 320; a result counts only if both agree.

## Lens replay (p1)
Statistic: certified h_StR at the 14 y in KN Zenodo Test-ST.txt and h_P at the y in Test-Pinch.txt, plus the
printed Table 1-2 values. Threshold: "confirmed" iff my ball midpoint equals KN's printed value to within half a
unit of KN's last printed digit, or to within 5e-4 when KN printed more than 3 decimals (bank asks for 3 decimals);
otherwise "corrected" with my value. KN record point y_KN = 19571878850562201959.215107: certified iff the lower
end of |h_StR(y_KN)| exceeds 1 + 6e-8.

## Lens lattice (p2/p3)
Hit (frozen): an exact decimal y with y < 19571878850562201959.215107 (strict) and certified |h_StR(y)| > 1 + 6e-8
(lower end of the ball), over the complete zero list gamma < 74000, at prec 256 and 320. A p2 hit is
|h_StR| > 1+6e-8 with y < 1.0e20, not in KN Tables 1-2. A p3 hit is the strict-below-y_KN case. Comparison of
bounds: exp(y + sqrt(y)) for both points (same formula; no Lemma E refinement on either side).
Method: KN lattice (3.2) built from my own zeros, fpylll LLL/BKZ, CVP enumeration (fpylll), then a local
polish of y (maximize |h_StR| over a window of +-1e-3 around each candidate with float64 on the top terms, then
the certified arb sum). The polish step is part of the pipeline and is applied identically to the null controls.

## Null test (frozen design)
400 controls: y drawn uniformly at random (fixed seed 20261124) from [1e18, 1.957e19], each passed through the
same polish window and the same certified h_StR evaluation. Statistic: certified |h_StR| after polish.
Real result must beat every control (expected: controls far below 1). Also: checker known-positive = y_KN
(must certify |h|>1+6e-8), known-negative = a y_KN shifted by +0.5 (must not certify).

## Lens bzyzz (p4 / honesty)
(i) certified h_StR (StR parameters) at bzyzz Peak2 v = 3484971332733132396.5383341489440461 (and its u = v - k);
    their README states 0.9957 there, i.e. below 1: we record whatever the ball says.
(ii) certified h_StR at all 25 points of their search/results/subrecord_peaks_summary.csv (y_exact_base + dy as
    given, and y_exact_base), checking whether ANY reaches 1 + 6e-8 at StR parameters (would be a p2/p3 hit, credited
    to bzyzz, not to us).
(iii) partial K2 sum at k = 1.5e-10 over my certified zeros below the highest cutoff reachable in budget, with an
    explicitly labelled NUMERICAL (not certified) tail estimate; a full certified 2,325,572-zero sum is
    attempted only if time allows. Outcome classes: "consistent with 1.0003052504 to 1e-4", "inconsistent", or
    "not completed". Review of THEOREM.md: list which inequalities we checked numerically; anything not
    checked stays "unchecked".

## Status ceiling
Single context: at most PROMISING. Any CONFIRMED needs three fresh-context skeptics (write PANEL_BRIEFS.md).
Never claim below exp(3.485e18) unless the criterion's own text is met.

## Budget
~5 h wall (stop new work at ~4 h), <= 3 worker processes, nice 10, timeout per job, no cloud.
