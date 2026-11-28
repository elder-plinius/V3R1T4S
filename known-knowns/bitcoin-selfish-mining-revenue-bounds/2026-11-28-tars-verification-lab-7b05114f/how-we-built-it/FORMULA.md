# Definition of N_rho^T used in this claim

Source: data/arxiv-1507.06183.pdf, sha256 0cc1fdc04eb5c925e294eff74dc5388f2921b6cd8164985b29dae4cf34da2b34.
Table 1 is on PDF page 8 (data/ssz-page-08-table1.png). Equation (7) and the following display are on PDF page 11 (data/ssz-page-11.png). Appendix C, Lemma 13 and eqs. (26)-(27) justify the grouping of (7) used here. Section 4.2 truncation: only adopt is legal when max(a,h)=T.

Parameters of the claimed object: alpha = 9/20, gamma = 0, rho = 169/250, T = 95.

Published SSZ Table 2 upper bound at alpha = 0.45 is 0.70109. The bank bar is 0.70099 (1e-4 below that published upper bound). They are not the same number.

## States and actions (Sections 2-4, Table 1)

States are triples (a, h, fork) with a,h integers in {0,...,T} and fork in {irrelevant, relevant, active}.
Actions: adopt, override, match, wait.
- adopt is always feasible (and is the only legal action when a=T or h=T).
- override is feasible only when a > h (and not at the cap).
- match is feasible only when fork=relevant and a >= h (Table 1 footnote), including the 95 states (a, 0, relevant) with a < T. The exact dual checker includes those 95 inequalities.
- wait is feasible when a < T and h < T.

Every transition corresponds to the creation of a new block. Immediate rewards are pairs (r_att, r_hon); the scalar used in the average-reward MDP is w_rho = r_att - rho * (r_att + r_hon), except at cap adopt in the over-paying MDP, where the scalar is the compensation described below.

## Table 1 transitions

(a,h,·), adopt:
- (1, 0, irrelevant) with probability alpha, reward (0, h)
- (0, 1, irrelevant) with probability 1-alpha, reward (0, h)

(a,h,·), override (a > h):
- (a-h, 0, irrelevant) with probability alpha, reward (h+1, 0)
- (a-h-1, 1, relevant) with probability 1-alpha, reward (h+1, 0)

(a,h,irrelevant), wait and (a,h,relevant), wait:
- (a+1, h, irrelevant) with probability alpha, reward (0, 0)
- (a, h+1, relevant) with probability 1-alpha, reward (0, 0)

(a,h,active), wait and (a,h,relevant), match (match only if a >= h):
- (a+1, h, active) with probability alpha, reward (0, 0)
- (a-h, 1, relevant) with probability gamma*(1-alpha), reward (h, 0)
- (a, h+1, relevant) with probability (1-gamma)*(1-alpha), reward (0, 0)

When gamma=0 the middle branch has probability 0.

Cap adopt (Section 4.2) uses the same X0 successors as ordinary adopt, namely (1,0,irrelevant) and (0,1,irrelevant) with probabilities alpha and 1-alpha.

## Compensation (over-paying cap adopt only)

### T = a >= h: equation (7)

As typeset on page 11, (1-rho) multiplies only the first term:

    (1-rho)*C  +  (1/2)*((a-h)/(1-2*alpha) + a + h),
    C = alpha*(1-alpha)/(1-2*alpha)^2

This claim uses the re-bracketed reading, not the literal typesetting:

    w_rho = (1-rho) * E[last(a,h)]
    E[last(a,h)] = C + (1/2)*((a-h)/(1-2*alpha) + a + h)

Justification: appendix eqs. (26)-(27) and Lemma 13. The left-hand side of (27) is (1-rho)*E[last(a,h)], and the paper says this is precisely the reward given in N_rho^T. The 1/2 factor multiplies the whole group ((a-h)/(1-2*alpha)+a+h) in both readings. Appendix (24)-(25) give the same E[last].

The literal typesetting, applied to the saved bias of the claimed object, yields g_bar = 99419735166796393739/281474976710656000 ≈ +353.20985307 and is not a certificate. It is also inconsistent with SSZ's published Table 2 upper bound 0.70109 (the resulting over-pay is far too loose).

### T = h >= a: following display / eq. (28)

With q = (alpha/(1-alpha))^(h-a), the printed display is

    w_rho = (1-q)*(-rho*h) + q*(1-rho)*( C + (h-a)/(1-2*alpha) )

The term (h-a)/(1-2*alpha) is the expected hitting time of the diagonal, not the attacker's block count at that hitting time, which is a + (h-a)*(1-alpha)/(1-2*alpha). For large a the printed display can under-pay, so Proposition 3 as printed is not airtight. The primary claimed object uses the printed display, as written. A supplementary conservative over-pay (pointwise max of printed and corrected rewards) is certified in object/recert_corrected_ht_dual.json, still with g_bar < 0 at the same rho.

Under-paying cap or interior adopt uses the ordinary scalar w_rho = -rho*h.

## Dual inequality

For a bias vector h and a rational g, the certificate asserts that for every state s and every action a allowed in s (including match at (a,0,relevant)),

    r_rho(s,a) + sum_{s'} P(s'|s,a) h(s') - h(s)  <=  g

with g < 0. By SSZ Proposition 3 (contrapositive): if the optimal average reward u of N_rho^T is < 0, then the untruncated value v_rho* is < 0, hence max REV < rho. The h=T caveat above is the reason for the supplementary max-compensation re-certification.
