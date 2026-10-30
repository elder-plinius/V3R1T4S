# How We Found It — `unit-demand-lottery-vs-item-pricing-gap`

*contributor text, unverified*

## Background & Problem
For a unit-demand buyer valuing multiple independent items, a central question in algorithmic mechanism design is the maximum possible revenue gap between an optimal randomized lottery menu and optimal deterministic item pricing. Chawla, Malec, and Sivan (CMS, EC 2010, arXiv:1002.3893) established a lower bound of $1 + \frac{\ln 2}{5} \approx 1.138629436$ on two independent capped equal-revenue items using a 3-entry menu. Jin and Lu (arXiv:2606.10169, Corollary 2(ii)) proved an upper bound of 3 and retained $1 + \frac{\ln 2}{5}$ as the literature lower bound. The open challenge was to construct an explicit instance and menu certifying a ratio strictly larger than this constant under conservative lowest-price tie-breaking.

## What Failed
1. **Coarse Discrete Grids**: Discretizing the equal-revenue distribution on small $n$ ($n \le 64$) under-represents the heavy tail, achieving ratios only up to $R/D \approx 1.0821$, well below the $1.1386$ bar.
2. **Naive Monte Carlo Sampling**: Direct Monte Carlo sampling over $1/x^2$ densities with upper atoms suffered from extreme variance in the tail regions, preventing rigorous interval certificates.
3. **Multi-Item Lazy IC LP Scaling**: Solving exact rational LPs for $k \ge 3$ items with large support sizes exceeded memory constraints, while small supports failed to capture sufficient tail mass.

## What Worked
1. **Analytical 1D Reduction of Decision Regions**:
   - For two items with independent capped equal-revenue CDF $F(x) = 1 - 1/x$ on $[1, n]$, we computed the inner integral over $v_2$ in closed form, reducing the 2D revenue integral to a smooth 1D integral that converges in milliseconds with precision $< 10^{-11}$.
2. **Transcendental Menu Threshold Optimization**:
   - We analyzed the 3-entry menu parameterized by threshold $S$: lottery $(1/2, 1/2)$ at price $p_1 = S/2$, and single items at price $p_2 = \alpha n$.
   - In the asymptotic limit $n \to \infty$, the total revenue simplifies to:
     $$\operatorname{Rev}(S) = 2 + \frac{\ln(S-1)}{S}$$
   - Maximizing this function yields $\frac{d}{dS}\left[\frac{\ln(S-1)}{S}\right] = 0 \iff \ln(S-1) = 1 + \frac{1}{S-1}$, giving optimal threshold $S^* \approx 4.59112$.
   - CMS historically set $S = 5$, giving $2 + \frac{\ln 4}{5} = 2 + \frac{2\ln 2}{5}$, ratio $1 + \frac{\ln 2}{5} \approx 1.138629436$.
3. **Exact Rational Instance & Finite Verification**:
   - Choosing the exact rational parameter $S = 23/5 = 4.6$ ($p_1 = 23/10 = 2.3$, $\alpha = 3/8$):
     $$\lim_{n \to \infty} \frac{R}{D} = 1 + \frac{5}{46} \ln\left(\frac{18}{5}\right) \approx 1.139231935$$
   - Evaluating on a finite closed-form instance with $n = 50000$ and $p_2 = 18750$, interval-certified numerical integration establishes $R = 2.27813998782$, $D = 2.0$, and ratio $R/D = 1.13906999391$, beating the CMS bar by surplus $+4.40558 \times 10^{-4} > 10^{-4}$ under conservative lowest-price tie-breaking.
4. **Partial Win `p1`**:
   - For discrete equal revenue on $\{1, \dots, 8\}$, exact rational primal-dual LP solution certifies supremum $15/8 = 1.875$ with zero duality gap. Deterministic item-pricing achieves supremum $15/8$ approached by $(8-\epsilon, 8-\epsilon)$.
