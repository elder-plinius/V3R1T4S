context: Claude Code subagent, fresh context [Sonnet 5.5]

novelty: no published or merged bound of 28 or less for [[504,12]] was found. The claimed weight-28 witness appears new relative to everything I could check. I did not independently run the verification script (that is another skeptic's job); this report is novelty only.

Status source read honestly, once, no retries (all times UTC, full log in a working copy (not shipped)):
- 2026-11-16T02:46:41Z https://raw.githubusercontent.com/mohammad-rowshan/BB-Codes-Distance-Logical-Decomposition/main/README.md, HTTP 200, sha256 90b3ef5c...f3bff (same hash as the package's snapshot). It names only the [[360,12]] code (18 <= d <= 30 after 60 s, weight-24 logical known) and the [[288,12,18]] node count. It has no entry for [[504,12]] and no bound for it. Repo: no releases (0), latest commit 2026-09-30 (not shipped in this package).
- 2026-11-16T02:46:42Z https://arxiv.org/abs/2511.13560, HTTP 200: versions v1, v2, v3 listed; https://arxiv.org/abs/2511.13560v4 returns 404 (no v4). 2026-11-16T02:46:48Z https://arxiv.org/pdf/2511.13560 (HTTP 200) is v3 dated 6 Aug 2026. Its Table 1 row: [[504, 12, d <= 30]], l=42, m=6, h=7, A = x^27+y+y^2, B = y^3+x^37+x^38. That is the only mention of 504 in the paper. No ancillary-file link appears on the abstract page.
- 2026-11-16T02:46:42Z https://arxiv.org/abs/2609.39395 (HTTP 200) and 2026-11-16T02:46:48Z https://arxiv.org/pdf/2609.39395 (HTTP 200): full text has no mention of 504 or of any n above 288 distance bound beyond the README facts. Gives no bound for [[504,12]].

Bound each source gives for [[504,12]]:
- Symons-Rajput-Browne v3: d <= 30.
- Rowshan-Devitt (paper v2 and README): none stated.

Literature search (arXiv API, 2026-11-16T02:46Z onward; queries for "bivariate bicycle" with distance, minimum distance, upper bound, covering graphs, Symons; last 24 months of results, newest first). I downloaded and grepped the full text of: 2610.18130 (Distance Prediction), 2610.03214 (certificate paper), 2609.06572 (weight-8 BB), 2608.27565 (Spectral theory, covering codes), 2608.09115 (Divisor-driven search), 2606.02418 (LLM-guided BB), 2605.14173 (Univariate bicycle), 2502.17052 (Existence and characterisation). None gives a bound for this [[504,12]] code. The only hits for 2511.13560 are citations (2609.06572, 2608.27565, 2606.02418) that do not restate a distance for it. (2610.18130 contains "3,504 codes", unrelated.) I did not read every BB paper in full; the search is the arXiv API keyword search, not exhaustive.

Neighbouring cells: [[504,12]] covers the [[72,12,6]] code (h=7). A base-code logical lifts to a cover logical of weight times h, so base codes give no upper bound below 30 by that rule; intermediate covers (l=14 or 21) are not tabulated with a 504 bound in the sources I read. I found no published restriction, propagation, or relabelling rule that gives 28 for this code. The package's witness is not seeded from a published object that I could identify (the paper gives no explicit logical for 504).

Repository search (read-only gh): elder-plinius/V3R1T4S. TROPHY_CASE.md has no bicycle/504/bivariate entry. The repository's known-knowns folder has no bivariate-bicycle folder (list checked; nearest: codetables and bigger-codes, unrelated). Open and closed PR searches for "bivariate", "bivariate bicycle", "bivariate-bicycle-exact-distance", "covering BB code", "Symons", "[[504", "[[432", "[[360", "weight-28" returned no BB-code claims (only unrelated claims such as PR 504 on codetables GF(4), which matches the number only). GitHub code search for the polynomials found nothing relevant; repo search for BB covering codes found no tool or bound table for 504. Rowshan repo has no releases.

Limits: arXiv listing page for the authors returned 303 and was not used; web search beyond the arXiv API and gh was not done. No tool I used would surface a bound hidden in an unlisted ancillary file, but no ancillary link is shown for 2511.13560.

Verdict: strictly better than the only published bound (30 to 28); nothing known ties or beats it.

pass: true
