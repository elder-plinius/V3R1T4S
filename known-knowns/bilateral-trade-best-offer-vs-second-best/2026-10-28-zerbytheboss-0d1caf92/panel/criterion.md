# Criterion Skeptic Report — `bilateral-trade-best-offer-vs-second-best`

context: subagent (fresh invocation)
target_id: bilateral-trade-best-offer-vs-second-best
review_utc: 2026-10-28T22:27:00Z

## Verbatim Success Criterion Audit

1. **Bank Success Criterion (Verbatim)**:
   > *"An instance given by two finite-support distributions (rational support points and rational probabilities) for s and b, independent, plus an explicit mechanism M, such that a checker in exact rational arithmetic confirms all of the following. (a) M is feasible. Either M is a posted price p (trade iff s <= p <= b), which is incentive compatible, individually rational and budget balanced by construction. Or M is given by allocation probabilities x(s,b) in [0,1] and interim expected transfers, and every BIC constraint (each type against each misreport) and every interim IR constraint holds for both agents, together with ex-ante budget balance (E[buyer payment] >= E[seller receipt]). This makes GFT_M = E[(b - s) x(s,b)] a lower bound on SB. (b) GFT_SO and GFT_BO are computed exactly. Seller offers range over the buyer's support points and buyer offers over the seller's support points. Among tied profit-maximising offers, each agent takes the one giving the LARGEST GFT, so the claim holds under every tie-breaking rule. (c) GFT_M > 0 and max(GFT_SO, GFT_BO) < (3/4) * GFT_M. Direction: lower ratio is better. The bar is 3/4 from BDK, arXiv 2111.07790, Section 3. Before claiming, re-run the status search and compare against any newer bound. The checker must first reproduce two calibration values. On BDK's 2x2 instance it must report ratio 1 under the GFT-favourable tie rule and 3/4 under BDK's adversarial rule. On the AlphaEvolve instance (appendix code of arXiv 2603.08679) it must reproduce FB ~ 1.2322, SO ~ 0.3312 and BO ~ 0.8565 under that paper's own tie rule. Any exact rational certificate of this strict inequality counts, however small the improvement. Match printed numerical calibration values within one unit of the last printed digit. The exact BDK calibration fractions remain exact. Values in unmerged pull requests are not bars."*

2. **Step-by-Step Criterion Verification**:
   - **Distributions**: Two finite-support distributions with rational support points and rational probabilities:
     - Seller: $S = [1, 2, 7, 14]$, $p_S = [53/100, 3/100, 42/100, 2/100]$ (all in $\mathbb{Q}$, positive, sum to 1).
     - Buyer: $B = [4, 8, 10, 14]$, $p_B = [1/100, 19/100, 24/100, 56/100]$ (all in $\mathbb{Q}$, positive, sum to 1).
     - Independence holds by construction (product probability space).
   - **Clause (a) Feasibility of $M$**:
     - $M$ is an explicit posted price $p = 8$ (trade iff $s \le 8 \le b$).
     - As specified verbatim in the criterion: *"Either M is a posted price p (trade iff s <= p <= b), which is incentive compatible, individually rational and budget balanced by construction."*
     - This makes $\text{GFT}_M = \mathbb{E}[(b - s) \mathbf{1}\{s \le 8 \le b\}] = \frac{80301}{10000} = 8.0301$ a rigorous certified lower bound on Second-Best ($\text{GFT}_M \le \text{SB}$).
   - **Clause (b) Exact Calculation of Offers & Tie-Breaking**:
     - Seller offers range over buyer support points $B = [4, 8, 10, 14]$. For each $s \in S$, profit is computed exactly in rational arithmetic. The optimal offer is $p^* = 14$ for all $s \in S$. Every profit maximizer is strictly unique (profit margin $\ge 0.0800$).
     - Buyer offers range over seller support points $S = [1, 2, 7, 14]$. For each $b \in B$, profit is computed exactly in rational arithmetic. The optimal offer is $p^* = 1$ for all $b \in B$. Every profit maximizer is strictly unique (profit margin $\ge 0.0300$).
     - Because all offers are strictly unique, the requirement that *"Among tied profit-maximising offers, each agent takes the one giving the LARGEST GFT, so the claim holds under every tie-breaking rule"* is satisfied unconditionally.
     - $\text{GFT}_{SO} = \frac{7133}{1250} = 5.7064$.
     - $\text{GFT}_{BO} = \frac{1431}{250} = 5.7240$.
     - $\max(\text{GFT}_{SO}, \text{GFT}_{BO}) = \frac{1431}{250} = 5.7240$.
   - **Clause (c) Inequality Verification**:
     - $\text{GFT}_M = \frac{80301}{10000} > 0$.
     - $\max(\text{GFT}_{SO}, \text{GFT}_{BO}) < \frac{3}{4} \text{GFT}_M$:
       $$\frac{1431}{250} = \frac{57240}{10000} < \frac{3}{4} \times \frac{80301}{10000} = \frac{240903}{40000} = 6.022575$$
       $$\iff \frac{228960}{40000} < \frac{240903}{40000} \iff - \frac{11943}{40000} < 0.$$
     - Ratio: $\frac{19080}{26767} \approx 0.71281802 < 0.75000000$.
   - **Calibration Controls**:
     - BDK 2x2: reports ratio 1 under favourable ties, 3/4 under adversarial ties. Matches exactly.
     - AlphaEvolve: reports $\text{FB} = 1.232226 \approx 1.2322$, $\text{SO} = 0.331178 \approx 0.3312$, $\text{BO} = 0.856511 \approx 0.8565$. Matches within 1 unit of last printed digit.
   - **Partial Wins**:
     - Lens 1 additionally computed exact rational primal-dual certificates for BDK Section 2 family ($H = 3..20$) and evaluated Second-Best for AlphaEvolve, settling partial win `p2`.

confirmed_scope: An explicit finite-support bilateral trade instance (|S|=4, |B|=4) with exact rational probabilities and posted price mechanism M=8 certifying max(GFT_SO, GFT_BO) / GFT_M = 19080/26767 approx 0.712818 strictly below the 3/4 bar under GFT-favourable tie-breaking with strictly unique optimal offers for all types.

pass: true
