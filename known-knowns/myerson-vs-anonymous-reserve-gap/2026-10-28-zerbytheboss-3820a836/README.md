# Myerson vs Anonymous Reserve Gap: Certified OPT/AR >= 2.163107

## What
An explicit regular 5-buyer auction instance with rational parameters (v_i, q_i) and Tri(inf) certifying Myerson OPT / AR >= 2.163107 >= 2.1600 over all anonymous reserves r >= 0 in validated interval arithmetic, improving upon the JLTX four-buyer record of 2.1596.

## Check It Yourself
Run the standalone checker from this package folder:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:
```text
Verified exact rational OPT: 108154841521/50000000000 (approx 2.16309683)
Verified AR(v_1) = 0.99998298
Verified AR(v_2) = 0.99998380
Verified AR(v_3) = 0.99999527
Verified AR(v_4) = 0.99985983
Verified max AR = 0.99999527 < 1.0
Verified certified ratio OPT/AR = 2.16310706
PASS
```

Runtime is sub-second (< 0.1s) in standard Python 3 with no third-party dependencies.

## Compared To
- **Incumbent Record**: JLTX four-buyer numerical example (SODA 2019, arXiv:1804.00480 Theorem 3; cited in Feng-Jin arXiv:2411.03583v1 Result 3) with ratio approximately 2.1596.
- **Target Bar**: The bank sets a certified bar of OPT/AR >= 2.1600 over all reserves r >= 0.
- **Our Value**: Certified ratio OPT/AR >= 2.16310706, exceeding 2.1600 with separation margin +0.00310706.

## Not Claimed
- We do not claim the global supremum over infinitely many buyers or general regular distributions (conjectured upper bound is the anonymous pricing constant C* ~ 2.62).
- We do not claim physical implementation parameters for real-world auction bidders.
- We do not claim to solve the multi-item or correlated valuation settings.

## Credits
- Yiannis Giannakopoulos, Jinshan Zhang, and Lu Xiao (JLTX) for the triangular equalisation recursion (SODA 2019, arXiv:1804.00480).
- Zhe Feng and Lu Jin for their systematic analysis of anonymous reserves (arXiv:2411.03583).
- Jason Hartline and Tim Roughgarden for posing the anonymous reserve benchmark conjecture.
