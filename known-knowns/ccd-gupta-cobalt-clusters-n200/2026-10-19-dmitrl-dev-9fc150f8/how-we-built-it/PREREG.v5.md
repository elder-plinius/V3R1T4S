# PREREG.v5 (changed plan during part B; earlier PREREG files unchanged)

Reason: the corrected growth move of lens 3b (3-fold and 4-fold sites from a 40-direction sphere around surface atoms)
reproduces the Co.zip minima from their decahedral neighbours (196->197, 121->122 exact) while lens 1's growth move used
convex-hull facets only. Lens 1b repeats lens 1's GROWTH half with the lens-3b site set: for N = 200 down to 101,
candidates = best(N-1) + one atom at each lens-3b site (best = min(polished table, polished Co.zip)); quick relax, polish
the best three, compare with E_best(N). Lens 1's etch half (remove each atom with coordination < 10 from best(N+1)) is
not repeated. Same potential, same budget rule (part B total <= 2 h wall from 04:02Z, i.e. stop by 06:02Z).
null_test: not needed because the claim is an explicit object (coordinates) checked by a deterministic checker against a table value
FROZEN 2026-10-19T04:40:14Z
