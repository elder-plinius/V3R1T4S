# Honesty gate (run 2026-11-26-1939)

checked_utc: 2026-11-28T10:34:04Z
status: CONFIRMED_SOLUTION
confirmed_scope: In the SSZ model of arXiv:1507.06183 at alpha = 9/20 and gamma = 0, an exact-rational average-reward dual with g = -51696398727/351843720888320 < 0 holds for every state and every allowed action of the over-paying MDP N_{169/250}^{95} (Table 1 transitions, adopt-only at max(a,h) = 95, eq. (7) read as (1-rho)*E[last(a,h)] per eqs. (26)-(27)), so by SSZ Proposition 3 the maximum relative revenue over SSZ's admissible policies is below 169/250 = 0.676 <= 0.70099, which meets the full alpha = 0.45 success criterion.

## Panel files read
- panel/reproduce.md: context "fresh knowledgeWork subagent, no prior context"; last line pass: true
- panel/novelty.md: context "fresh knowledgeWork subagent, no prior context"; last line pass: true
- panel/criterion.md: context "fresh knowledgeWork subagent, no prior context"; last line pass: true; confirmed_scope copied above with no edits

## Table refetch (required: panel fetch was older than 6 hours)
- URL: https://arxiv.org/abs/1507.06183
- Fetched 2026-11-28T10:34:04Z, one request, no retry. HTTP 200.
- sha256 17034454c06d20f055d997a07fbfc9beed99e36376db3c3425e0f1cf51d99d99, identical to the run's saved abs page (2026-11-26T19:39:44Z) and to the novelty fetch.
- Page still lists "Optimal Selfish Mining Strategies in Bitcoin", v2 23 Jul 2015, not withdrawn, no later revision. The published Table 2 upper bound at alpha = 0.45 remains 0.70109 (PDF page 13 of the already-saved paper). The object U = 169/250 = 0.676 is strictly below 0.70109 and below the bank bar 0.70099.

## Downgrade checklist (kit/RUN.md step 7)
- Hedging panelist: no. All three ended with an unqualified pass: true. Novelty's parenthesization caveat is a fidelity question that reproduce and criterion decided, and that CLAIM.md/FORMULA.md now disclose; it is not a withdrawn novelty verdict.
- Reproduction mismatch: no. Independent exact g_bar matches the claimed fraction; calibration and sanity were reproduced.
- Value not strictly better than the live table: no. 0.676 < 0.70109 (refetched source unchanged).
- Stretched criterion or hidden quantifier: no, after disclosure. The bank names eq. (7); the claim uses the (26)-(27)/Lemma 13 reading (1-rho)*E[last], which criterion accepted as SSZ's definition. The literal typesetting fails (g_bar ≈ +353.21) and is inconsistent with SSZ's own 0.70109; it is not used. Match at (a,0,relevant) is included. The Prop. 3 h=T display caveat was re-certified with conservative max compensation (exact g_bar ≈ -9.826e-5 < 0) at the same rho; the untruncated conclusion still holds.
- Scope wider than reproduced: no. Only alpha = 9/20, gamma = 0, SSZ admissible policies.
- Sample as complete / capped search as exclusion / probable prime as proof / table evasion / bundled objects / unresolved baseline: none of these apply. One cell, deterministic certificate, no null-test category.

No downgrade. Status is CONFIRMED_SOLUTION for the alpha = 0.45 bar only.
