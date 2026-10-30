# Unit-Demand Lottery vs Item Pricing Revenue Gap

## What
An explicit two-item closed-form equal-revenue instance (n=50000) and rational menu M={(1/2, 1/2, 2.3), (1, 0, 18750), (0, 1, 18750)} certifying revenue ratio R/D = 1.139069994 strictly beating the Chawla-Malec-Sivan lower bound 1 + ln(2)/5 approx 1.138629436 by surplus +4.40558e-4 under conservative lowest-price tie-breaking, with exact rational primal-dual lottery LP certification (15/8) for discrete n=8.

## Check It Yourself
Run the standalone checker from this package folder:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:
```text
Running verification for unit-demand-lottery-vs-item-pricing-gap...
Calibration (CMS n=64): R = 2.164275, R/D = 1.082138 > 1.073 -> PASS
Partial Win p1 (n=8): Exact primal-dual LP = 15/8 = 15/8 with 0 gap -> PASS
Solution Instance (n=50000, S=4.6): R = 2.278139987, D = 2.0, R/D = 1.139069994 > 1+ln(2)/5 by +0.000441 -> PASS
SUCCESS: ALL CHECKS PASSED
PASS
```

Runtime is under 2 seconds on a standard laptop.

## Compared To
- **Status Source**: Y. Jin and P. Lu, "Tight Bounds on Revenue Gaps in Multi-Item Unit-Demand Auctions", arXiv:2606.10169 (Corollary 2(ii)); S. Chawla, D. L. Malec, and B. Sivan, "The Power of Randomness in Mechanism Design", arXiv:1002.3893; EC 2010.
- **Incumbent Record**: Chawla, Malec, and Sivan established a lower bound gap of $1 + \frac{\ln 2}{5} \approx 1.1386294361$ on 2-item capped equal-revenue distributions using a 3-entry menu with threshold $S = 5$. Jin and Lu proved an upper bound of 3 and retained $1 + \frac{\ln 2}{5}$ as the literature lower bound.
- **Our Value**: Certified $R/D = 1.139069994$, strictly exceeding the CMS constant $1 + \frac{\ln 2}{5} \approx 1.138629436$ by surplus $+4.40558 \times 10^{-4} > 10^{-4}$ under conservative lowest-price tie-breaking. The limiting continuous formula $2 + \frac{\ln(S-1)}{S}$ optimized at $S = 23/5 = 4.6$ yields asymptotic ratio $1 + \frac{5}{46}\ln(18/5) \approx 1.139231935$.

## Not Claimed
- We do not claim that $1.13923$ is the supremum of the lottery-to-item-pricing ratio over all distributions or menus; we claim an explicit instance and rational menu certifying a ratio strictly greater than $1 + \frac{\ln 2}{5}$.
- We do not claim that $D = 2.0$ is the exact optimal item-pricing revenue; $D = \sum_{i=1}^2 \max_p p \Pr[v_i \ge p] = 2.0$ is a mathematically rigorous upper bound on optimal item pricing for any unit-demand buyer, ensuring $R / \text{Rev}(\text{Item Pricing}) \ge R / D > 1 + \frac{\ln 2}{5}$.

## Credits
- Shuchi Chawla, David L. Malec, and Balasubramanian Sivan for the original equal-revenue lower-bound construction and 3-entry menu framework (arXiv:1002.3893, EC 2010).
- Yiding Jin and Pinyan Lu for the upper bound of 3 and the comprehensive multi-item unit-demand review (arXiv:2606.10169, 2026).
- V3R1T4S autonomous multi-agent discovery architecture.
