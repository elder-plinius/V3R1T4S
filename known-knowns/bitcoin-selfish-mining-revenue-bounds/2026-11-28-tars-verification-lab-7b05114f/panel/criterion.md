# CRITERION review: bitcoin-selfish-mining-revenue-bounds (run 2026-11-26-1939)

context: fresh knowledgeWork subagent, no prior context

confirmed_scope: In the SSZ model of arXiv:1507.06183 at alpha = 9/20 and gamma = 0, an exact-rational average-reward dual with g = -51696398727/351843720888320 < 0 holds for every state and every allowed action of the over-paying MDP N_{169/250}^{95} (Table 1 transitions, adopt-only at max(a,h) = 95, eq. (7) read as (1-rho)*E[last(a,h)] per eqs. (26)-(27)), so by SSZ Proposition 3 the maximum relative revenue over SSZ's admissible policies is below 169/250 = 0.676 <= 0.70099, which meets the full alpha = 0.45 success criterion.

verdict: full success criterion met (alpha = 0.45 bar, U = 0.676 <= 0.70099). This is not just a partial win. p1, p2 and p3 are not needed.

## What I checked, and how

Files read: CLAIM.md, FORMULA.md, REPRODUCE.md, scout.md, code/exact_table1_dual.py, code/calibrate_and_sanity.py, object/exact_dual_rho169_250.json, object/table1_scan.json, data/ssz-page-08-table1.png, data/ssz-page-11.png, and data/arxiv-1507.06183.pdf (Sections 4.2 and Appendix C, eqs. (22)-(28), rendered from the PDF).

1. Hashes. The sha256 values of object/over_bias.npy, object/over_policy.npy, object/exact_dual_rho169_250.json and data/arxiv-1507.06183.pdf match CLAIM.md.

2. Independent rebuild (part iii). I wrote my own exact-Fraction checker from Table 1 and Section 4.2. It does not reuse the claimant's code and takes only the bias vector, converting each float64 to an exact dyadic rational. It reproduces max residual = -51696398727/351843720888320 (about -1.4693e-4) exactly over 72583 inequalities, with no off-board successors.
   - Hidden-quantifier check on the action set: the claimant's checker drops `match` at (a, 0, relevant), which Table 1 literally allows ("feasible only when a >= h"). I added those 95 inequalities, making 72678 in total. g is unchanged, so the certificate covers every action Table 1 allows.
   - The state space is all triples (a,h,fork) with a,h in {0..95}. It is closed under the transitions, so it is a superset of the reachable set, and a dual that holds on it bounds the optimal gain from every start state.
   - The cap rule (only adopt when max(a,h) = T) matches Section 4.2 ("same constraint as M_rho^T"). Cap adopt goes to X0 with the compensation in place of the ordinary adopt reward, which matches "it is awarded".

3. Parenthesization of eq. (7), the main stretched-definition risk. As typeset on page 11 (and on the RHS of eq. (27) on page 29), eq. (7) reads (1-rho)*C + 1/2*((a-h)/(1-2alpha)+a+h). No outer bracket puts (1-rho) over the whole sum. FORMULA.md's phrase "as parenthesized on page 11" only covers the 1/2 factor and passes over this point. The paper itself settles the meaning:
   - eq. (27)'s LHS is (1-rho)*E[last(a,h)];
   - eq. (26)/(22) gives E[last] = C + 1/2(...);
   - the text says "This is precisely the reward given in ... N_rho^T".
   So the claimant's reading (1-rho)*(C + 1/2(...)) is SSZ's definition. The literal-typography reading also contradicts SSZ's own numbers. With my relative value iteration at T=75, alpha=0.45, rho=0.66891, the literal reading gives an over-paying gain of +0.066 (rho+2u about 0.80 > SSZ's published 0.70109 upper bound), while the (27) reading gives rho+2u about 0.682. Under the literal reading this certificate would fail: g = +353 with this bias, and the re-solved optimal gain at rho=0.676 is +0.043. So the pass depends on the (27) reading, and I accept that reading as the paper's definition.

4. Calibration and sanity (I re-solved these with my own builder, not the claimant's):
   - Under-paying MDP at T=95, using the gain sign at bracketing rho values: REV(0.45) is in (0.66890, 0.66892) and REV(0.425) is in (0.56807, 0.56809). Both are within one last-printed digit of Table 2's 0.66891 and 0.56808.
   - Over-paying N at alpha=0.45, rho=0.66, T=95: gain +0.010006 > 0, so the sanity test passes. It matches object/table1_scan.json.

5. Transfer from the truncated model to the claimed untruncated object. Proposition 3 says that if v* >= 0 then u^T >= v*. By contrapositive, u^T <= g < 0 gives v*_rho < 0. Then Lemma 8 / Prop. 2 (v^pi has the sign of REV(pi) - rho over SSZ's admissible class A) gives REV(pi) < rho for all admissible pi. The criterion explicitly allows concluding via Prop. 3.
   - Caveat I found in SSZ's own proof: in the h = T >= a display (eq. (28)), SSZ use E[a0 | return] = (h-a)/(1-2alpha). That is the expected hitting time, not the attacker's block count at the diagonal, which is a + (h-a)(1-alpha)/(1-2alpha). For large a the printed display can therefore under-pay, so Prop. 3 as printed is not airtight.
   - Robustness check: I replaced the h = T compensation with max(printed, corrected) and re-solved at rho = 0.676, T = 95. An exact-rational dual still certifies g = -276576516729/2814749767106560 (about -9.83e-5) < 0. So the conclusion max REV < 0.676 survives this correction. This is a supplementary check by the reviewer; it is not part of the claimant's object.

6. Null model / incumbent. 0.676 is 0.025 below the bar of 0.70099. scout.md (pages fetched this run) finds no certified incumbent below SSZ Table 2. The gain comes from larger T plus an exact dual instead of SSZ's epsilon slack. That is still a genuine certified improvement under the numeric criterion, and nothing subsumes it.

## Limits of the scope
- The result covers only alpha = 0.45, gamma = 0. The alpha = 0.475 bar is not addressed.
- The policy class is SSZ's admissible class (non-pathological policies, Section 3).
- The untruncated conclusion depends on SSZ Prop. 3's oracle argument, plus the reviewer's corrected-display re-certification noted above.
- The bias is float64 converted to exact dyadic rationals, which is acceptable as a rational certificate.

pass: true
