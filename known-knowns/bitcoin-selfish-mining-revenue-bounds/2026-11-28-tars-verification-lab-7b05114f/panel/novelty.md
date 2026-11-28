# Novelty review: bitcoin-selfish-mining-revenue-bounds (run 2026-11-26-1939)

context: fresh knowledgeWork subagent, no prior context

Role: NOVELTY (skeptical). Inputs read: claim/ only (CLAIM.md, scout.md, FORMULA.md, REPRODUCE.md, code/, object/, data/), public web, and the repo's TROPHY_CASE.md and known-knowns/ (local clone), plus read-only GitHub PR/issue listings.

## Object under review
max REV < 169/250 = 0.676 at alpha = 9/20, gamma = 0, T = 95, exact rational dual certificate with g_bar = -51696398727/351843720888320 (~ -1.469e-4), 72583 inequalities, 0 off-board (object/exact_dual_rho169_250.json).

## Status fetch (one attempt, no retries)
- URL: https://arxiv.org/abs/1507.06183
- Fetched 2026-11-26T20:24:29Z (21:24:29 CET). HTTP 200. sha256 17034454c06d20f055d997a07fbfc9beed99e36376db3c3425e0f1cf51d99d99, the same as data/arxiv-1507.06183-abs.html (saved 2026-11-26T19:39:44Z, 45 min old, so under the 6 h freshness limit).
- Page: "Optimal Selfish Mining Strategies in Bitcoin", v1 22 Jul 2015, v2 23 Jul 2015. Not withdrawn. No later revision.
- The table value comes from the saved PDF data/arxiv-1507.06183.pdf (sha256 0cc1fdc0..., matching the claim). It is on PDF page 13, Table 2, row alpha = 0.45: SM1 0.65177, eps-OPT 0.66891, Upper Bound **0.70109** (T = 95, eps = 1e-5). The arXiv HTML render (https://arxiv.org/html/1507.06183v2, via web search 2026-11-26 ~20:25Z) shows the same row.
- Note: the brief calls 0.70099 the "published Table 2 upper bound". It is not. 0.70109 is the published value, and 0.70099 is the bank bar set 1e-4 below it. The object beats both.

## Comparison for this cell and neighbouring cells (gamma = 0)
| alpha | best published upper bound | best lower bound / value | object |
|---|---|---|---|
| 0.425 | 0.57226 (SSZ Table 2) | 0.56808 (SSZ eps-OPT) | n/a |
| **0.45** | **0.70109** (SSZ Table 2); 0.70099 claimed in open, unmerged PR #814 | 0.66891 (SSZ), 0.66894 (PTO, arXiv:2007.05614) | **< 0.676 (exact)** |
| 0.475 | 0.90476 (SSZ); 0.90466 claimed in PR #814 | 0.80172 (SSZ), 0.80184 (PTO) | n/a |

At alpha = 0.45, 0.676 is 0.02509 below the published 0.70109 and 0.02499 below PR #814's 0.70099. It is a strict improvement, not a tie. It is still above the known optimum of ~0.66894, so the interval is narrowed, not closed.

## Literature and code search (last 24 months, plus older baselines)
- arXiv API queries, run 2026-11-26T20:25:17Z to 20:25:28Z: "selfish mining" AND "upper bound"; "selfish mining" AND bitcoin AND optimal; abs:"selfish mining" AND abs:MDP; plus the saved data/arxiv-api-selfish-certif.xml (19:39:45Z, 1 irrelevant hit). Hits since Nov 2024: 2607.01209 (block withholding under PPS), 2511.21552 (MAD-DAG, an upper-bound model for DAG protocols, not SSZ), 2511.11538 (DAA incentive attacks), 2503.10185, 2502.20360 (stochastic rewards), 2501.10888 (DAG selfish-mining automation), 2411.11702, 2502.17307 (RL survey). I read the abstracts of 2502.20360, 2607.24415, 2501.10888 and 2511.11538 (API id_list, 20:25:28Z). None gives a REV upper bound for the SSZ Bitcoin model at gamma = 0.
- arXiv:2607.24415 (Sakurai, Nakai, Shudo 2026, data/arxiv-2607.24415-abs.html): bounds on the incentive-compatibility threshold in a different model (gamma-/gamma+). This is not a REV bound at alpha = 0.45.
- arXiv:2007.05614 (PTO, Bar-Zur, Eyal, Tamar 2020): lower bounds/policies (0.66894) with an O(1/H) error statement and no numeric certified upper bound.
- Web searches (2026-11-26 ~20:25Z) for tighter or certified SSZ upper bounds, eq. (7) errata and over-paying implementations: nothing tighter than 0.70109. blockchainkit (https://cpoli.github.io/blockchainkit/api/economics.html) gives lower values only. I found no release assets or code giving a better upper bound.
- Repo TROPHY_CASE.md and known-knowns/: no selfish-mining family or trophy. An rg for "selfish|sapirshtein|SSZ" matched only unrelated evidence text files in graph-automata-max-period.
- GitHub (read-only), fetched 2026-11-26 ~20:25Z, https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+selfish: 2 items. #814 is open (created 2026-10-28T23:29:16Z) and claims U <= 0.70099 at alpha = 0.45 and U <= 0.90466 at alpha = 0.475 (https://github.com/elder-plinius/V3R1T4S/pull/814). #659 (bank entry) is closed. The object strictly beats #814 at alpha = 0.45. The direct API call for pull #814 returned 403; I read the PR page through the web fetch instead.

## Skeptical caveat (material; for the soundness and model-fidelity reviewers)
The whole improvement comes from how the compensation in eq. (7) is read, not from a larger T. SSZ also used T = 95.
- Printed eq. (7) on PDF page 11 (data/ssz-page-11.png and the arXiv HTML) reads `(1-rho)*alpha(1-alpha)/(1-2alpha)^2 + 1/2*((a-h)/(1-2alpha) + a + h)`. Only the first term carries the factor (1-rho).
- FORMULA.md and code/exact_table1_dual.py (line 55: `(1 - rho) * elast_eq7(...)`) apply (1-rho) to the whole sum, but call this "printed equation (7)". That label is inaccurate. The printed text does not parenthesize it that way.
- Check run in a scratch copy outside claim/, with claim/ untouched: I replaced line 55 with the literal printed form and ran the same bias. Result: g_bar = +353.21 (not negative), with the worst inequality at (a=95, h=0, adopt). So the certificate does not hold for the literally printed over-paying MDP. Since SSZ's own printed-formula bound at T = 95 is 0.70109, the literal MDP probably has positive gain at rho = 0.676.
- The (1-rho)-on-everything reading is dimensionally consistent: w_rho = r_att - rho*(r_att + r_hon) gives (1-rho)*L when the attacker gets L blocks. It is also consistent with Appendix C (24)-(25) as cited in FORMULA.md, and it is plausibly SSZ's intent. If it is a valid over-payment, the object is a genuine and strictly better upper bound on max REV. Whether it is valid, and whether it meets the bank wording "compensation rewards from eq. (7)", is a soundness/fidelity question outside the novelty role. The panel must decide it explicitly. Novelty does not survive an unsound compensation.

## Verdict
Novelty: the object (max REV < 0.676 at alpha = 0.45, gamma = 0) strictly beats every bound found: SSZ 0.70109, the bank bar 0.70099, and open PR #814's 0.70099. I found nothing tighter in the last 24 months of arXiv/web/code or in TROPHY_CASE/known-knowns. The pass is conditional on the panel accepting the parenthesization of eq. (7) above. The claim's "printed eq. (7)" wording should be corrected to say it uses a reparenthesized form.

pass: true
