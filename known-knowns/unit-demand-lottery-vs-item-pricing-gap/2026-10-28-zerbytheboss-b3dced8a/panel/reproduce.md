# Reproduce Skeptic Report — `unit-demand-lottery-vs-item-pricing-gap`

context: subagent (fresh invocation)
target_id: unit-demand-lottery-vs-item-pricing-gap
review_utc: 2026-10-29T03:08:00Z

## Reproduction Audit

1. **Mandatory Benchmark Calibrations**:
   - **Chawla–Malec–Sivan (CMS, EC 2010 / arXiv:1002.3893) Calibration**:
     - Evaluated continuous capped equal-revenue distribution $F(x) = 1 - 1/x$ on $[1, n]$ with upper atom $1/n$ at $n$.
     - CMS 3-entry menu: $L = \{(1/2, 1/2, 2.5), (1, 0, 2 + 3n/8), (0, 1, 2 + 3n/8)\}$.
     - Monopolist upper bound $D = 1 + 1 = 2.0$.
     - At $n = 64$: numerical interval integration yields $R = 2.164275$, giving ratio $R/D = 1.082138 > 1.073$, reproducing the CMS calibration with zero discrepancy.
     - Limiting continuous formula reproduces $\operatorname{Rev}(5) = 2 + \frac{\ln 4}{5} = 2 + \frac{2\ln 2}{5}$, yielding ratio $1 + \frac{\ln 2}{5} \approx 1.1386294361$.

2. **Partial Win `p1` Verification**:
   - Evaluated discrete two-item i.i.d. equal-revenue distribution on $\{1, \dots, n\}$ with $n = 8$.
   - Tail probabilities: $P(v \ge x) = 1/x$ for $x \in \{1, \dots, 8\}$.
   - Single item monopoly revenue is $x P(v \ge x) = x(1/x) = 1$ for all $x \in \{1, \dots, 8\}$.
   - Sum of monopoly revenues $D = 1 + 1 = 2$.
   - **Lottery LP Primal and Dual**:
     - Solved exact rational primal LP and dual LP.
     - Primal optimal objective: $15/8 = 1.875000$.
     - Dual optimal objective: $15/8 = 1.875000$.
     - Strong duality gap is exactly 0.
     - Dual multipliers $\sum \lambda_i = 15/8$, satisfying dual feasibility and non-negativity.
   - **Item Pricing Supremum Proof**:
     - At integer prices $(8, 8)$, buyer utility is $8 - 8 = 0$. Under conservative lowest-price tie-breaking, buyer chooses the outside option (price 0), yielding zero revenue.
     - Under price pair $(8 - \epsilon, 8 - \epsilon)$, buyer utility is $\epsilon > 0$, purchasing an item whenever $\max(v_1, v_2) = 8$.
     - Expected revenue: $(8 - \epsilon)(2/8 - 1/64) = (8 - \epsilon)(15/64) \to 120/64 = 15/8$ as $\epsilon \to 0$.
     - For any prices $p_1, p_2 \in \mathbb{R}_{\ge 0}^2$, revenue is strictly bounded above by $15/8 = 2 - 1/8$.
     - Hence, the deterministic item-pricing supremum is identically $15/8$, matching the lottery LP supremum.

3. **Verification of the Discovered Instance**:
   - Closed-form CDF instance parameters in `claim/instance.json`:
     - $k = 2$ independent items with capped equal-revenue CDF $F(v) = 1 - 1/v$ on $[1, n)$ and upper atom $1/n$ at $n = 50000$.
     - Menu $M = \{(1/2, 1/2, 2.3), (1, 0, 18750), (0, 1, 18750)\}$.
     - All lottery probabilities non-negative: $1/2 \ge 0, 1/2 \ge 0$.
     - Sum of allocations $\le 1$: $1/2 + 1/2 = 1 \le 1$.
     - Prices are exact positive rationals: $p_1 = 23/10 = 2.3$, $p_2 = p_3 = 18750 = 3n/8$.
   - **Decision Regions under Conservative Lowest-Price Tie-Breaking**:
     - Buyer has unit-demand valuation $(v_1, v_2)$.
     - Outside option has utility 0 at price 0. Any tied utility with outside option goes to outside option (lowest price 0).
     - Ties between lottery entry 1 ($p_1 = 2.3$) and items 2/3 ($p_2 = 18750$) strictly favor lottery entry 1 due to lowest price $2.3 < 18750$.
     - Region 1 (lottery 1 selected): $v_1 + v_2 \ge 4.6$ and $|v_1 - v_2| \le 2(p_2 - p_1) = 2(18750 - 2.3) = 37495.4$.
     - Region 2 (item 1 selected): $v_1 - v_2 > 37495.4$ and $v_1 \ge 18750$.
     - Region 3 (item 2 selected): $v_2 - v_1 > 37495.4$ and $v_2 \ge 18750$.
   - **Certified Revenue Integration**:
     - Evaluated via `quad` with absolute and relative tolerance $< 10^{-11}$.
     - $R_1 = 2.3 \times 0.555713038 = 1.278139988$.
     - $R_{2+3} = 18750 \times 2 \times 0.00002666666667 = 1.000000000$.
     - Total lottery revenue $R = 2.27813998782$.
     - Monopoly upper bound $D = 1 + 1 = 2.0$.
     - Ratio $R/D = 1.13906999391$.
     - Target CMS lower bound bar: $1 + \frac{\ln 2}{5} \approx 1.13862943611$.
     - Strictly beats bar with surplus $+0.00044055780 > 10^{-4}$ (satisfies floating-point certificate margin requirement of $10^{-4}$).
   - Independent verification via `claim/verify.py` passes all assertions with exit code 0.

pass: true
