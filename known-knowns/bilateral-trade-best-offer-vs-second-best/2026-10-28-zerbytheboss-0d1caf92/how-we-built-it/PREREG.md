# Preregistered Evaluation Bar (`bilateral-trade-best-offer-vs-second-best`)

frozen_utc: 2026-10-28T22:16:00Z
target_id: bilateral-trade-best-offer-vs-second-best
category: graphs-games-automata
null_test: not needed because exact rational linear programming certificates and exact finite-support mechanism evaluations are deterministic algebraic proofs

## 1. Verbatim Target Bank Criteria
> An instance given by two finite-support distributions (rational support points and rational probabilities) for s and b, independent, plus an explicit mechanism M, such that a checker in exact rational arithmetic confirms all of the following. (a) M is feasible. Either M is a posted price p (trade iff s <= p <= b), which is incentive compatible, individually rational and budget balanced by construction. Or M is given by allocation probabilities x(s,b) in [0,1] and interim expected transfers, and every BIC constraint (each type against each misreport) and every interim IR constraint holds for both agents, together with ex-ante budget balance (E[buyer payment] >= E[seller receipt]). This makes GFT_M = E[(b - s) x(s,b)] a lower bound on SB. (b) GFT_SO and GFT_BO are computed exactly. Seller offers range over the buyer's support points and buyer offers over the seller's support points. Among tied profit-maximising offers, each agent takes the one giving the LARGEST GFT, so the claim holds under every tie-breaking rule. (c) GFT_M > 0 and max(GFT_SO, GFT_BO) < (3/4) * GFT_M. Direction: lower ratio is better. The bar is 3/4 from BDK, arXiv 2111.07790, Section 3. Before claiming, re-run the status search and compare against any newer bound. The checker must first reproduce two calibration values. On BDK's 2x2 instance it must report ratio 1 under the GFT-favourable tie rule and 3/4 under BDK's adversarial rule. On the AlphaEvolve instance (appendix code of arXiv 2603.08679) it must reproduce FB ~ 1.2322, SO ~ 0.3312 and BO ~ 0.8565 under that paper's own tie rule. Any exact rational certificate of this strict inequality counts, however small the improvement. Match printed numerical calibration values within one unit of the last printed digit. The exact BDK calibration fractions remain exact. Values in unmerged pull requests are not bars.

## 2. Partial Wins (Verbatim)
- **p1:** An explicit instance whose certified ratio FB/RO exceeds 2.28862548 + 1e-6, where RO = (GFT_SO + GFT_BO)/2 with GFT-favourable tie-breaking. Supports may be finite and checked exactly, or distributions closed-form with interval-arithmetic integrals in the style of M. Jo 2026. This pushes the worst-case random-offerer ratio below 0.436943488, the limit of Shang-Chen's recursive families (arXiv 2610.06547); Bei et al. (arXiv 2609.37997) show RO >= FB/e, so the open window for FB/RO is (2.28862548, e]. The cell is crowded (several 2026 papers, one using AI-guided evolutionary search).
- **p2:** Exact second-best values, each an LP optimum with a rational primal-dual certificate, for the published hard instances. These are the AlphaEvolve instance in the appendix code of arXiv 2603.08679 and BDK's Section 2 family for H = 3..20. Report max(SO,BO)/SB for each. No second-best figures for these instances are published, so the table settles whether the first-best-hard instances are also second-best-hard.

## 3. Evaluation Metric & Thresholds
- Exact rational arithmetic: all probabilities $p_S(s), p_B(b)$, support points, allocation probabilities $x(s,b)$, transfers $T_S(s), T_B(b)$, and dual multipliers must be represented as `fractions.Fraction`.
- Seller Offering ($\text{GFT}_{SO}$):
  $$\text{GFT}_{SO} = \sum_{s \in S} p_S(s) \sum_{b \in B, b \ge p_s^*(s)} p_B(b) (b - s)$$
  where for each $s \in S$, $p_s^*(s) \in \arg\max_{p \in B, p \ge s} (p - s) \sum_{b \in B, b \ge p} p_B(b)$, breaking ties by maximizing $\sum_{b \ge p} p_B(b) (b - s)$.
- Buyer Offering ($\text{GFT}_{BO}$):
  $$\text{GFT}_{BO} = \sum_{b \in B} p_B(b) \sum_{s \in S, s \le p_b^*(b)} p_S(s) (b - s)$$
  where for each $b \in B$, $p_b^*(b) \in \arg\max_{p \in S, p \le b} (b - p) \sum_{s \in S, s \le p} p_S(s)$, breaking ties by maximizing $\sum_{s \le p} p_S(s) (b - s)$.
- Mechanism Feasibility:
  - $0 \le x(s, b) \le 1$ for all $s \in S, b \in B$.
  - Seller BIC: $T_S(s) - s X_S(s) \ge T_S(s') - s X_S(s')$ for all $s, s' \in S$.
  - Buyer BIC: $b X_B(b) - T_B(b) \ge b X_B(b') - T_B(b')$ for all $b, b' \in B$.
  - Seller IR: $T_S(s) - s X_S(s) \ge 0$ for all $s \in S$.
  - Buyer IR: $b X_B(b) - T_B(b) \ge 0$ for all $b \in B$.
  - Ex-ante Budget Balance: $\sum_{b \in B} p_B(b) T_B(b) \ge \sum_{s \in S} p_S(s) T_S(s)$.
- Target thresholds:
  - For full win: $\max(\text{GFT}_{SO}, \text{GFT}_{BO}) < \frac{3}{4} \text{GFT}_M$ under GFT-favourable tie-breaking.
  - For partial win `p2`: exact rational primal-dual certificates for BDK $H = 3..20$ and AlphaEvolve.
- Mandatory calibrations:
  1. BDK $2 \times 2$: ratio $1$ under GFT-favourable ties, $3/4$ under BDK adversarial ties.
  2. AlphaEvolve ($H=20000$): $\text{FB} \approx 1.2322$, $\text{SO} \approx 0.3312$, $\text{BO} \approx 0.8565$.
