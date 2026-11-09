# Honesty Gate: `levine-hat-two-player-value`

status: CONFIRMED_PARTIAL
confirmed_scope: Exact rational certification of V_{2,4} = 89/256 = 0.34765625 via exhaustive canonical search over all 4-hat strategies (Partial Win p1).

## Gate Summary
- **REPRODUCE (`panel/reproduce.md`)**: `pass: true` (Independent verification of bucket reduction, calibrations h=1..3, exhaustive canonical search proving max wins strictly 89/256, matrix calibrations 2x2, 4x6, 8x14, and 16x30 local search lower bound 57/160 in check_v24.py).
- **NOVELTY (`panel/novelty.md`)**: `pass: true` (Status source arXiv:2508.01737v2 confirmed open; first exhaustive search across all asymmetric and symmetric 4-hat strategies settling Bouquet et al. conjecture; zero prior claims in TROPHY_CASE.md).
- **CRITERION (`panel/criterion.md`)**: `pass: true` (Literal clause-by-clause satisfaction of Partial Win p1 with exact rational value and certified optimal witness pair).
- **Verdict**: CONFIRMED_PARTIAL (Partial Win p1 candidate certified, packaged for draft submission).
