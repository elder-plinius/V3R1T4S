# Criterion Skeptic Report — `unit-demand-lottery-vs-item-pricing-gap`

context: subagent (fresh invocation)
target_id: unit-demand-lottery-vs-item-pricing-gap
review_utc: 2026-10-29T03:08:00Z

## Verbatim Success Criterion Audit

1. **Bank Success Criterion (Verbatim)**:
   > *"An explicit instance (k >= 2 independent item-value distributions, given either with finite rational supports or as closed-form CDFs) and an explicit finite menu of lotteries with rational entries (x >= 0, sum_i x_i <= 1, price l). A checker must confirm three things. (a) The menu's revenue R is computed exactly. With finite supports, enumerate all value profiles; the buyer picks a utility-maximising entry, ties go to the LOWEST-priced maximiser, and the buyer buys nothing when the best utility is <= 0. With closed-form CDFs, use interval-certified integration over the regions where each entry is chosen. (b) An upper bound D on optimal item-pricing revenue: either D = sum_i max_p p * Pr[v_i >= p], always valid for a unit-demand buyer, or the exact OIP from a search over a price set proved sufficient in the write-up. (c) D > 0 and R/D > 1 + ln(2)/5. Direction: higher is better. The bar is the Chawla-Malec-Sivan constant as restated in Jin-Lu, arXiv 2606.10169, Corollary 2(ii); re-check arXiv for newer lower bounds before claiming. The checker must first reproduce the CMS menu's revenue on CMS's capped equal-revenue pair for several n. Use interval integration of the continuous version, or exact enumeration of a fine rational discretisation with the discretisation error bounded. Derive the source menu revenue independently. Match printed finite numerical calibration values within one unit of the last printed digit. Do not turn a rounded appendix calculation into an exact identity. An exact rational or symbolic certificate of any strict improvement counts. For floating-point certificates require a certified ratio at least 1+ln(2)/5+1e-4. Values in unmerged pull requests are not bars."*

2. **Step-by-Step Criterion Verification**:
   - **Instance Representation**:
     - Explicit instance with $k = 2$ independent items given as closed-form CDFs: $F(v) = 1 - 1/v$ for $v \in [1, n)$ and point mass $1/n$ at $v = n = 50000$.
     - Explicit finite menu of lotteries with rational entries:
       - Entry 1: $x = (1/2, 1/2)$, price $p_1 = 23/10 = 2.3$.
       - Entry 2: $x = (1, 0)$, price $p_2 = 18750$.
       - Entry 3: $x = (0, 1)$, price $p_3 = 18750$.
       - All allocations satisfy $x_i \ge 0$ and $\sum x_i \le 1$.
   - **Clause (a) Menu Revenue Computation**:
     - Revenue $R$ computed by interval-certified integration over the precise decision regions under conservative lowest-price tie-breaking.
     - Buyer buys nothing when best utility is $\le 0$.
     - Tied utilities strictly favor the lowest-priced maximizer ($p_1 = 2.3 < 18750$).
     - Certified integration: $R = 2.27813998782 \in [2.2781399, 2.2781401]$.
   - **Clause (b) Upper Bound $D$**:
     - Single-item monopoly revenue: for any $p \in [1, n]$, $p \Pr[v \ge p] = p(1/p) = 1.0$.
     - $D = \sum_{i=1}^2 \max_p p \Pr[v_i \ge p] = 1.0 + 1.0 = 2.0$, mathematically valid for any unit-demand buyer.
   - **Clause (c) Ratio and Margin**:
     - $D = 2.0 > 0$.
     - $R/D = 1.13906999391$.
     - Target CMS bar: $1 + \frac{\ln 2}{5} \approx 1.13862943611$.
     - Certified surplus: $R/D - (1 + \ln(2)/5) = +0.00044055780 > 10^{-4}$.
     - Fully satisfies the requirement: *"For floating-point certificates require a certified ratio at least 1+ln(2)/5+1e-4"*.
   - **Calibration Controls**:
     - CMS calibration reproduced for $n \in \{8, 16, 32, 64, 100, 500, 1000, 5000\}$.
     - At $n = 64$, reports $R = 2.164275$, $R/D = 1.082138 > 1.073$, matching literature values.
   - **Partial Win `p1`**:
     - Solved discrete equal-revenue LP for $n=8$.
     - Primal LP objective = Dual LP objective = $15/8 = 1.875$ with 0 duality gap.
     - Proved deterministic item-pricing supremum is $15/8$, approached by $(8-\epsilon, 8-\epsilon)$.

confirmed_scope: An explicit two-item closed-form equal-revenue instance (n=50000) and rational menu M={(1/2, 1/2, 2.3), (1, 0, 18750), (0, 1, 18750)} certifying revenue ratio R/D = 1.139069994 strictly beating the Chawla-Malec-Sivan lower bound 1 + ln(2)/5 approx 1.138629436 by surplus +4.40558e-4 under conservative lowest-price tie-breaking, with exact rational primal-dual lottery LP certification (15/8) for discrete n=8.

pass: true
