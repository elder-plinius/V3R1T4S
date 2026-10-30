# Honesty Gate — `bilateral-trade-best-offer-vs-second-best`

status: CONFIRMED_SOLUTION
confirmed_scope: An explicit finite-support bilateral trade instance (|S|=4, |B|=4) with exact rational probabilities and posted price mechanism M=8 certifying max(GFT_SO, GFT_BO) / GFT_M = 19080/26767 approx 0.712818 strictly below the 3/4 bar under GFT-favourable tie-breaking with strictly unique optimal offers for all types.

## Gate Audit Summary
- **REPRODUCE (`panel/reproduce.md`)**: `pass: true` (Independent verification of BDK 2x2 calibration [1 favourable, 3/4 adversarial] and AlphaEvolve calibration [FB ~ 1.2322, SO ~ 0.3312, BO ~ 0.8565]; exact rational verification of 4x4 instance confirming all offers strictly unique, GFT_SO = 7133/1250 = 5.7064, GFT_BO = 1431/250 = 5.7240, GFT_M = 80301/10000 = 8.0301, and exact ratio 19080/26767 ~ 0.712818 < 3/4).
- **NOVELTY (`panel/novelty.md`)**: `pass: true` (BDK 2021 arXiv:2111.07790 Section 3 established 3/4 on 2x2 only under adversarial ties; universal lower bound is 1/2 from BCWZ 2017; fresh arXiv search on 2026-10-28 confirms no published instance achieving max(SO, BO) / SB < 3/4 under favourable ties; zero competing PRs on elder-plinius/V3R1T4S; first certified instance beating 3/4 bar).
- **CRITERION (`panel/criterion.md`)**: `pass: true` (Clause (a) satisfied by posted price p=8 dominant-strategy IC/IR/BB by construction; Clause (b) satisfied with exact rational offers and strict uniqueness; Clause (c) satisfied with GFT_M > 0 and 19080/26767 < 3/4; calibrations reproduce verbatim; partial win p2 also settled for BDK H=3..20 and AlphaEvolve).
- **Downgrade Checks**: Zero hedging, zero reproduction mismatches, zero stretched criteria, zero leaks. Final status is CONFIRMED_SOLUTION.
