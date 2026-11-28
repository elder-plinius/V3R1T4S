context: subagent (fresh context, knowledgeWork)
role: NOVELTY

target: bitcoin-selfish-mining-revenue-bounds (status_source per claim/CRITERION.txt: https://arxiv.org/abs/1507.06183)
claim under review: max REV < 0.67005787 (alpha = 0.45, gamma = 0, SSZ model), exact dual certificate at T = 2000
(claim/CLAIM.md), plus errata E1 (Lemma 13 / eq. 22, so eq. 7) and E2 (eq. 28 / proof of Prop. 3).

## 1. Status source, one honest fetch (no retries)
- URL: https://arxiv.org/abs/1507.06183. Fetched once at 2026-11-27T02:39:24Z UTC (2026-11-26 21:39:24 ET). HTTP 200.
  sha256 of the page 17034454c06d20f055d997a07fbfc9beed99e36376db3c3425e0f1cf51d99d99, the same as claim/scout_record.md.
  Submission history: v1 Wed 22 Jul 2015, v2 Thu 23 Jul 2015. No v3 and no erratum version.
- The abs page holds no table, so the value comes from the paper PDF (claim/1507.06183.pdf, sha256 0cc1fdc0...2b34,
  matching scout_record). Table 2 (gamma = 0, T = 95, eps = 1e-5), row "0.45 0.65177 0.66891 0.70109".
  Incumbent upper bound: 0.70109. The bank bar is 0.70099.
- Neighbouring published variant: the FC'16 short version at https://www.avivz.net/pubs/2016/OptSelfishMining.pdf
  (fetched 2026-11-27T02:42:27Z UTC / 21:42:27 ET, HTTP 200). Its Table 2 row "0.45 0.65177 0.66809 0.72203" (T = 75)
  is weaker. It has no appendix, so it holds no corrected Lemma 13.

## 2. V3R1T4S repo (unauthenticated GitHub API, 2026-11-27T02:39:36Z to 02:40:13Z UTC / 21:39:36 to 21:40:13 ET, all HTTP 200)
- Issue/PR search, repo:elder-plinius/V3R1T4S, for "selfish", "bitcoin-selfish-mining-revenue-bounds", "1507.06183" and
  "sapirshtein": 2 hits each.
  - #659 [bank] (closed 2026-10-25T19:29:21Z UTC, not merged). The maintainer comment checks SSZ Table 2 (0.66891 / 0.70109)
    and PTO Table 1 (0.66894) and finds "no certified upper bound below SSZ's".
  - #814 [claim] (open, created 2026-10-28T23:29:16Z UTC, not merged, 0 comments). Head 901a828e on HindsightWise/V3R1T4S.
    object/claim.json: alpha 9/20, "certified_upper_bound_U": "70099/100000" (0.70099), truncation_T 95,
    gain g = -3170481/200000000. Its how-we-built-it/ssz_model.py uses the compensation as printed
    (term1 = alpha(1-alpha)/(1-2alpha)^2; "term_ret = term1 + (h-a)/denom"). So it does NOT report either erratum.
    Best value in the repo: 0.70099, which is weaker than 0.67005787.
- TROPHY_CASE.md (main, blob 18b731d7): no mention of selfish, bitcoin, 1507 or SSZ.
- known-knowns/ on main: 50 folders, none for this target. #814's known-knowns folder exists only in that PR.
- Releases: 0, so there are no release assets.

## 3. Literature and code (last 24 months, plus the anchors)
- PTO, arXiv 2007.05614 (https://arxiv.org/pdf/2007.05614, fetched 2026-11-27T02:40:52Z UTC / 21:40:52 ET, HTTP 200).
  Table 1, "0.45 0.668 94 0.668 91" (fork length 95). This is the revenue of a policy, so it is a lower-side value
  and not an upper bound. The claim's certified lower bound, > 0.67005786, is consistent with it: a larger T allows
  better policies.
- arXiv 2607.24415, Sakurai/Nakai/Shudo, "Near-Tight Theoretical Bounds for Incentive Compatibility in Bitcoin Mining",
  2026-07-27 (abs and pdf fetched 2026-11-27T02:40:30Z to 02:40:35Z UTC / 21:40:30 to 21:40:35 ET, HTTP 200).
  It bounds the incentive-compatibility threshold, not REV at alpha = 0.45. A grep for 0.45 / 0.67 / 0.70 / errata /
  Lemma 13 / compensation found no revenue bound and no erratum.
- arXiv 2501.03227 (When Should Selfish Miners Double-Spend?), Table I, alpha 0.45: rho_OSM 0.66891, rho_PTO 0.66894.
  These are restated lower values only.
- Scanned with no hit for an upper bound below 0.70109, for 0.670xx, or for an erratum:
  2512.13213, 2501.10888, 2511.11538, 2502.17307, 2601.02984, 2606.06860, 2606.03153, 2604.06092, 2508.16202, 2607.23952,
  2611.13252 and 2607.01209 (PDFs fetched 2026-11-27T02:41:32Z to 02:41:50Z UTC / 21:41:32 to 21:41:50 ET).
  - arXiv API, abs:"selfish mining", newest first (02:41:25Z UTC): no relevant item.
  - Semantic Scholar citations of arXiv:1507.06183 (675 citing papers, fetched 02:41:43Z UTC / 21:41:43 ET): no title
    since 2024-11 is about certified or improved Bitcoin gamma = 0 revenue upper bounds, and none reports SSZ errata.
- Code: github.com/nirenzang/Optimal-Selfish-Mining-Strategies-in-Bitcoin (pushed 2017-05-30, files fetched 02:40:59Z UTC).
  SolveStrategy.m uses the printed compensation:
  "mid1 = (1-rou)*alphaPower*(1-alphaPower)/(1-2*alphaPower)^2+0.5*(...)" and "mid3=...*(mid1+(h-a)/(1-2*alphaPower))".
  It has no correction and publishes no larger-T values.
- Web searches for a corrected SSZ, for over-paying compensation errata, and for larger-T upper bounds at alpha = 0.45
  turned up nothing. Note: the search-engine "synthesis" text claiming 0.66894 is "the converged optimum" has no source;
  PTO itself fixes fork length 95.

## 4. Comparison and trivial-edit test (alpha = 0.45 cell; neighbours are alpha 0.425 / 0.475 and the FC version)
- Known upper bounds for this cell: SSZ 0.70109 (T = 95), FC'16 0.72203 (T = 75), PR #814 0.70099 (T = 95, open and
  uncertified by panel), and the trivial alpha/(1-alpha) = 0.81818. None is at or below 0.67005787.
  - Claimed 0.67005787 is strictly lower by 0.03103 (SSZ) and by 0.03093 (#814).
  - No published exact optimum or upper bound near 0.6689 exists. The 0.66891 / 0.66894 figures are truncated policy
    values (lower side) and are below the claimed enclosure (0.67005786, 0.67005787), so they do not give an equal or
    better upper bound. Not a tie.
- Trivial edits. No deletion, restriction, propagation rule, relabelling, symmetry or local polish of the published
  T = 95 objects (SSZ's MDP or #814's certificate) gives 0.67006. At T = 95 the gain margin of #814 (-0.0159 at 0.70099)
  cannot move rho to 0.670, and the claim reports the corrected T = 95 root as 0.6808712.
  The bound needs a new, much larger MDP (T = 2000, about 32M state-action pairs) and a new exact bias vector.
- Flag: methodologically this is SSZ's own Algorithm 1 run at a larger T, plus an exact certificate and the corrected
  compensation. The claim says the certificate also passes for the printed compensation, so "SSZ at T = 2000" would give
  the same number. A larger T is not one of the listed trivial edits, and the bank criterion lets the claimant choose T.
  So I count it as a new object, but its novelty is computational rather than conceptual.
  It is not seeded from a published certificate: none exists at large T.
- Soundness (validity of the corrected Prop. 3, the checker) belongs to the REPRODUCE/CRITERION skeptics, not to this
  review.

## 5. Errata novelty (reported separately)
- E1 (Lemma 13). In SSZ's text, success is "a visit of the origin which never returns to it" with probability
  "1 - alpha/(1-alpha)", giving E[N] = alpha/(1-2alpha).
  - Never returning to the nonnegative side from the origin needs a -1 step and then no return:
    (1-alpha)(1 - alpha/(1-alpha)) = 1 - 2alpha, so E[N] = 2alpha/(1-2alpha). This agrees with the claim's E1, and I
    checked it by hand.
  - E2 (E[a0 | return] in eq. 28) is plausible as derived in claim/CLAIM.md. I did not re-derive it.
- Neither erratum appears in any source I searched: the arXiv versions (only v1/v2), the FC version, PTO, 2607.24415,
  the 24-month citing literature, the nirenzang code, or V3R1T4S PRs #659 / #814 (which use the printed formulas).
  Within this search, both errata look new. This is search-limited and covers no paywalled venues or private
  correspondence.

## 6. Injection check
No instruction in claim/ or in any fetched page tried to steer the verdict. claim/CLAIM.md's "NOVELTY must re-check"
note is a neutral request. injection_suspected: no.

## Verdict
The claimed U = 0.67005787 is strictly below every known upper bound for alpha = 0.45, gamma = 0 (best known: open
PR #814 at 0.70099; published: SSZ 0.70109). It is not a tie, and it does not come from trivial edits of a published
object. NOVELTY passes on the bound, conditional on the other skeptics confirming soundness. The errata are new as far
as this search reaches.
pass: true
