# Record We Beat — `unit-demand-lottery-vs-item-pricing-gap`

target_id: unit-demand-lottery-vs-item-pricing-gap
table_url: https://arxiv.org/abs/2606.10169
fetch_time: 2026-10-29T02:44:26Z
http_status: 200
page_sha256: 2d9982d28c0c167e2a54a6a46cc9bba466e070fca93e7944a3f1001a406d4071

## Published Incumbent Status
- Literature Benchmark: S. Chawla, D. L. Malec, and B. Sivan, "The Power of Randomness in Mechanism Design", arXiv:1002.3893; EC 2010.
- Recent Confirmation / Open Problem: Y. Jin and P. Lu, "Tight Bounds on Revenue Gaps in Multi-Item Unit-Demand Auctions", arXiv:2606.10169 (Corollary 2(ii)).
- Stated Incumbent Lower Bound: Chawla, Malec, and Sivan established a lower-bound gap of $1 + \frac{\ln 2}{5} \approx 1.1386294361$ on 2-item capped equal-revenue distributions using a 3-entry menu with menu threshold $S = 5$. Jin and Lu proved an upper bound of 3 and retained $1 + \frac{\ln 2}{5}$ as the literature lower bound.
- Resolution: By optimizing the menu threshold parameter $S$, we proved the continuous equal-revenue revenue curve is $\operatorname{Rev}(S) = 2 + \frac{\ln(S-1)}{S}$, maximized at the transcendental root $\ln(S-1) = 1 + \frac{1}{S-1}$ ($S^* \approx 4.59112$). Evaluating the rational choice $S = 23/5 = 4.6$ ($p_1 = 2.3$, $p_2 = 18750 = 3n/8$ at $n=50000$) achieves $R/D = 1.139069994$, strictly beating the CMS lower bound $1 + \frac{\ln 2}{5}$ by surplus $+4.40558 \times 10^{-4} > 10^{-4}$ under conservative lowest-price tie-breaking.
