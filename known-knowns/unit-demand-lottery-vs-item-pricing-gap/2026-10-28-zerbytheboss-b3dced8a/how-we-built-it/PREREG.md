# Preregistered Evaluation Bar (`unit-demand-lottery-vs-item-pricing-gap`)

frozen_utc: 2026-10-28T22:30:00Z
target_id: unit-demand-lottery-vs-item-pricing-gap
category: graphs-games-automata
null_test: not needed because deterministic linear programming duality and exact closed-form calculus provide mathematically rigorous certificates and bounds

## 1. Verbatim Target Bank Criteria
> An explicit instance (k >= 2 independent item-value distributions, given either with finite rational supports or as closed-form CDFs) and an explicit finite menu of lotteries with rational entries (x >= 0, sum_i x_i <= 1, price l). A checker must confirm three things. (a) The menu's revenue R is computed exactly. With finite supports, enumerate all value profiles; the buyer picks a utility-maximising entry, ties go to the LOWEST-priced maximiser, and the buyer buys nothing when the best utility is <= 0. With closed-form CDFs, use interval-certified integration over the regions where each entry is chosen. (b) An upper bound D on optimal item-pricing revenue: either D = sum_i max_p p * Pr[v_i >= p], always valid for a unit-demand buyer, or the exact OIP from a search over a price set proved sufficient in the write-up. (c) D > 0 and R/D > 1 + ln(2)/5. Direction: higher is better. The bar is the Chawla-Malec-Sivan constant as restated in Jin-Lu, arXiv 2606.10169, Corollary 2(ii); re-check arXiv for newer lower bounds before claiming. The checker must first reproduce the CMS menu's revenue on CMS's capped equal-revenue pair for several n. Use interval integration of the continuous version, or exact enumeration of a fine rational discretisation with the discretisation error bounded. Derive the source menu revenue independently. Match printed finite numerical calibration values within one unit of the last printed digit. Do not turn a rounded appendix calculation into an exact identity. An exact rational or symbolic certificate of any strict improvement counts. For floating-point certificates require a certified ratio at least 1+ln(2)/5+1e-4. Values in unmerged pull requests are not bars.

## 2. Partial Wins (Verbatim)
- **p1:** For the discrete two-item i.i.d. equal-revenue instance with P(v>=x)=1/x on {1,...,n} and some n>=8, certify the exact lottery-revenue and deterministic item-pricing revenue suprema. Give a rational primal-dual certificate for the lottery LP and prove its value is the supremum under the stated tie rule. For item pricing, give an exact exhaustive price-region proof or an appropriate integer/global certificate covering all prices. If conservative ties prevent attainment, provide epsilon-achieving menus or prices with a proved revenue gap. Compare existing published values before claiming novelty.

## 3. Preregistered Thresholds and Checkers
1. **CMS Reproduction Calibration:**
   - Reproduce the Chawla–Malec–Sivan (arXiv:1002.3893) two-item calibration:
     - Numerical/discrete calibration for several $n \in \{8, 16, 32, 64, 100, 500\}$.
     - Continuous limiting revenue $R = 2 + \frac{2}{5}\ln 2 \approx 2.277258872$ and ratio $R/D = 1 + \frac{\ln 2}{5} \approx 1.1386294361$.
     - Confirm finite calibration values $R/D > 1.073$ (e.g. at $n = 64$ where $R/D \approx 1.0821$).
2. **Partial Win `p1` (Discrete Equal-Revenue $n \ge 8$):**
   - Exact rational primal-dual lottery LP certificate for $n = 8$ in `fractions.Fraction`.
   - Primal feasibility: non-negative probabilities, allocation sum $\le 1$, IC and IR satisfied.
   - Dual feasibility: dual variables non-negative, dual constraints satisfied.
   - Primal objective equals dual objective: exactly $15/8 = 1.875 = 2 - 1/8$.
   - Supremum proof under conservative tie-breaking: prove that no mechanism achieves $> 2 - 1/n$ and that $\epsilon$-achieving pricing $(n - \epsilon, n - \epsilon)$ approaches $2 - 1/n$.
   - Exhaustive proof for deterministic item pricing: partition $\mathbb{R}_{\ge 0}^2$ into price regions, proving the deterministic item-pricing supremum is also $2 - 1/n$.
3. **Confirmed Solution Record Bar:**
   - Threshold constant: $1 + \frac{\ln 2}{5} \approx 1.13862943611$.
   - Target ratio: certified $R/D \ge 1 + \frac{\ln 2}{5} + 10^{-4} \approx 1.138729436$.
   - Instance: $k = 2$ independent items with closed-form CDF $F_1(x) = F_2(x) = 1 - 1/x$ on $[1, n]$ with atom at $n = 50000$ (and limiting symbolic instance $n \to \infty$).
   - Explicit rational menu: $M = \{(1/2, 1/2, 2.3), (1, 0, 18750), (0, 1, 18750)\}$ with outside option $(0, 0, 0)$.
   - Certified ratio: $R/D \ge 1.13907 > 1 + \frac{\ln 2}{5} + 4.4 \times 10^{-4}$ (and symbolic limiting ratio $1 + \frac{5}{46}\ln(18/5) \approx 1.13923 > 1 + \frac{\ln 2}{5} + 6 \times 10^{-4}$).
   - Conservative lowest-price tie-breaking verified throughout.
