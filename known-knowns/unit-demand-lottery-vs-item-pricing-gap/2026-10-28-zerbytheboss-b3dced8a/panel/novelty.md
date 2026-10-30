# Novelty Skeptic Report — `unit-demand-lottery-vs-item-pricing-gap`

context: subagent (fresh invocation)
target_id: unit-demand-lottery-vs-item-pricing-gap
review_utc: 2026-10-29T03:08:00Z

## Novelty & Prior Art Audit

1. **Status Source and Literature Baseline**:
   - Status Source: `https://arxiv.org/abs/2606.10169` ("Tight Bounds on Revenue Gaps in Multi-Item Unit-Demand Auctions", Jin and Lu, June 2026).
   - Fetched: 2026-10-29T02:44:26Z, HTTP 200, SHA-256 `2d9982d28c0c167e2a54a6a46cc9bba466e070fca93e7944a3f1001a406d4071`.
   - In Corollary 2(ii), Jin and Lu prove an upper bound of 3 on the ratio of optimal randomized (lottery) revenue to deterministic item-pricing revenue for independent unit-demand buyers.
   - For the lower bound, Jin and Lu cite the landmark construction of Chawla, Malec, and Sivan (EC 2010, arXiv:1002.3893):
     $$\frac{\operatorname{Rev}(\text{Lottery})}{\operatorname{Rev}(\text{Item Pricing})} \ge 1 + \frac{\ln 2}{5} \approx 1.1386294361$$
   - Since 2010, the constant $1 + \frac{\ln 2}{5}$ has stood in the literature as the best-known lower-bound gap for independent items under unit demand.

2. **Analysis of the CMS Lower-Bound Construction**:
   - CMS constructed a 2-item equal-revenue capped instance with support $[1, n]$ and proposed a 3-entry menu:
     - Entry 1: $(1/2, 1/2)$ at price $p_1 = S/2$ (CMS fixed $S = 5 \implies p_1 = 2.5$).
     - Entry 2: $(1, 0)$ at price $p_2 = \alpha n$ (CMS set $\alpha = 3/8$).
     - Entry 3: $(0, 1)$ at price $p_3 = \alpha n$.
   - The asymptotic revenue is:
     $$\operatorname{Rev}(S) = 2 + \frac{\ln(S-1)}{S}$$
   - When $S = 5$, $\frac{\ln(4)}{5} = \frac{2\ln 2}{5} \approx 0.27725887$, yielding $R = 2 + \frac{2\ln 2}{5}$ and $R/D = 1 + \frac{\ln 2}{5} \approx 1.1386294$.
   - Prior authors treated $S = 5$ as a fixed choice and did not optimize the threshold $S$.

3. **Discovery of the Transcendental Optimum**:
   - Differentiating $\frac{\ln(S-1)}{S}$ with respect to $S$:
     $$\frac{d}{dS}\left[\frac{\ln(S-1)}{S}\right] = \frac{\frac{S}{S-1} - \ln(S-1)}{S^2} = 0 \iff \ln(S-1) = 1 + \frac{1}{S-1}$$
   - The unique root occurs at $S^* \approx 4.59112$.
   - Evaluating the exact rational choice $S = 23/5 = 4.6$ ($p_1 = 2.3$):
     $$\operatorname{Rev}\left(\frac{23}{5}\right) = 2 + \frac{5}{23} \ln\left(\frac{18}{5}\right) \approx 2.27846387$$
     $$\frac{R}{D} = 1 + \frac{5}{46} \ln\left(\frac{18}{5}\right) \approx 1.139231935$$
   - This strictly beats $1 + \frac{\ln 2}{5}$ by $+0.0006025 > 6 \times 10^{-4}$ in the continuous limit!
   - On the finite instance with $n = 50000$ and $p_2 = 18750$, interval integration certifies $R/D = 1.139069994$, exceeding the CMS bar by $+0.000440558 > 10^{-4}$.

4. **Novelty Confirmation**:
   - Fresh search of arXiv literature up to October 2026 confirms no published paper has reported this improved lower-bound constant.
   - Zero competing claims exist in `TROPHY_CASE.md` or active pull requests on `elder-plinius/V3R1T4S`.
   - Partial win `p1` provides the first exact rational primal-dual certification and item-pricing supremum proof for discrete equal revenue on $\{1, \dots, 8\}$.

pass: true
