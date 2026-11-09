context: subagent

# Novelty skeptic: C_42 >= 501/1000 (route ii, lower bound)

Written 2026-10-31T22:33Z. Inputs read: claim/CLAIM.md, claim/HYPOTHESES.md, claim/PROOF.md, claim/CERT.md, claim/REPRODUCE.md, claim/V_b.json, claim/table/record.txt, claim/table/pulls_open.json (for comparison only), and the repo copy's TROPHY_CASE.md, known-knowns/ and (for the target's brief) known-unknowns/erdos-and-proofs/turan-pure-power-sum-c42-upper-bound.md. I did not read the code, logs or V_b.npy (correctness is not my panel seat).

## 1. Primary status page (fetched once, no retry)

| URL | UTC time | HTTP | Value read |
|---|---|---|---|
| https://teorth.github.io/optimizationproblems/constants/42a.html | 2026-10-31T22:19:37Z | 200 | 8660 bytes, sha256 990f853a6222a995a1dcb88032c199e1259b513145ea8d1d841dcb5d442ebf43, byte-identical (cmp) to claim/table/42a.html saved at 22:02:55Z |

Lower-bound table on the page: 1/6 (Atkinson 1961), 1/3 (Atkinson, unpublished report), pi/8 (Atkinson 1969), 1/2 (Biro 1994), then ">1/2" (Biro [Bir00b], Indag. Math. 11 (2000) 343-358) with the comment "Biro's proof delivers some computable constant 1/2<c<1/sqrt2, but it is not computed there exactly which."
Best explicit lower bound listed on the page: **1/2**. No explicit value of Biro's c is listed.
Upper-bound column (context only): best on page 0.6873358063* (Koshta); open PR #305 proposes 0.6863607950*, open PR #302 0.68637*. None of this touches the lower-bound cell.

## 2. teorth/optimizationproblems pull requests, issues, releases (GitHub API, one request at a time, unauthenticated)

Rate limit seen: 60/hour for core, 57 left after the first request, 47 left at the last core request; search bucket 10/min, never exhausted. No 401, 403 or 429 from any GitHub endpoint.

| URL (api.github.com/repos/teorth/optimizationproblems/...) | UTC time | HTTP | Value read |
|---|---|---|---|
| pulls?state=open&per_page=100 | 2026-10-31T22:19:57Z | 200 | 43 open PRs; same PR numbers as claim/table/pulls_open.json (none added, none gone). Open PRs on 42a: #305 (rpinho, upper 0.6863607950*), #302 (Bakeas, upper 0.68637*), #184 (AndreRoehrig, upper 0.688983). No open PR proposes any lower bound for C_42. Other hits for "Biro/Turan" in bodies were hex digests or unrelated text. |
| pulls?state=closed&per_page=100&page=1,2,3 | 22:20:17Z, 22:20:22Z, 22:20:28Z | 200 x3 | 246 closed PRs (#1 to #295). 42a-related: #26 (page created), #29 (accent fix), #85 (Griego upper 0.6906538), #137 (typo fix), #251 (Pinho upper 0.6888863712), #263 (Koshta upper 0.6873358063). None concerns a lower bound. |
| releases?per_page=30 | about 22:20:45Z | 200 | empty list: the repository has no releases |
| issues?state=all (3 pages, all PRs filtered out) | 22:20:51Z to 22:21:16Z | 200 x3 | non-PR issues #8, #10, #43, #51, #65, #67, #150, #168, #190, #211, #218, #233, #289, #304: none about 42a or a lower bound |

## 3. Other GitHub, Zenodo, arXiv, web

| URL | UTC time | HTTP | Value read |
|---|---|---|---|
| api.github.com/search/repositories, 5 queries ("turan power sum", "c42 turan", "erdos 519", "biro power sum", "optimizationproblems 42a") | 22:23:58Z to 22:24:51Z | 200 x5 | All Turan C_42 repos are upper-bound repos: rpinho/c42-certificate, Bakeas/turan-c42-bound, Bakeas/turan-power-sum-certificates, DennisKoshta/c42-turan-power-sum-certificate, krplatz/turan-c42-six-level-review, sebastian-griego/turan-c42-certificate. "biro power sum" returned 0. |
| raw.githubusercontent.com .../README.md of those 6 repos, plus rpinho/math-certificates | 22:24:59Z to 22:25:32Z | 200 x7 | grep for lower bound / Biro / "> 1/2": only Bakeas/turan-power-sum-certificates line 16 ("Lower bound: R_n > q for every n, for an absolute constant q > 1/2 (Biro 2000...)", citing the constant without a value) and bibliography lines. rpinho/math-certificates row for C42 lists only the upper bound 0.6863607950. No explicit lower bound anywhere. |
| api.github.com/users/{Bakeas,rpinho,DennisKoshta}/repos | 22:25:19Z to 22:25:27Z | 200 x3 | No repository about a C_42 lower bound or Biro's constant. Bakeas has 3 repos (all upper bounds). |
| raw.githubusercontent.com/Bakeas/turan-c42-bound/main/NOTES.md | about 22:25Z | 200 | upper-bound note only |
| github.com releases (via search result titles): Bakeas/turan-c42-bound v1.0.0 and v1.1.0, Bakeas/turan-power-sum-certificates v1.0.0 | seen in search results | n/a | titles: "C42 <= 0.6865", "C42 <= 0.68637", "certified bounds for n = 300 to 1 000 000" (upper bounds for finite n). Release pages not opened; repo READMEs checked as above. |
| https://zenodo.org/api/records?q="power sum" AND Turán&sort=mostrecent&size=25 | 2026-10-31T22:29:35Z | 200 | 2 hits: 10.5281/zenodo.23836302 "Turán's pure power sum constant: C42 <= 0.68637" and 10.5281/zenodo.23806909 "Certified upper bounds in Turán's pure power sum problem (Erdős #519)". Both upper bounds. |
| https://zenodo.org/api/records?q=Turán C42&sort=mostrecent&size=25 | 22:29:41Z | 200 | 1939 unrelated hits in the top 25 (Uzbek, Turkish, health papers); nothing on this constant. |
| http://export.arxiv.org/api/query (6 queries: all:"power sum" AND all:Turan; abs:"pure power sum"; all:Biro AND all:"power sum"; all:Turán AND all:"power sums"; abs:"sums of powers of complex numbers"; abs:Atkinson AND abs:"power sum"; plus id_list for 2607.22017, 0704.1879) | 22:25:48Z to 22:26:35Z (first try returned 301 to https; followed once, same query) | 200 | Nothing newer than 2007 on this constant. 2607.22017 "Exterior power sums" (July 2026) concerns |z_j| >= 1 and Erdős 973, a different problem. 0704.1879 (Andersson) is max over m = c n^2, a different quantity. math/0607238, 0706.4131, math/0609271 are Andersson's papers on other power-sum problems (2006 to 2007). |
| https://hexagonmath.org/2610.00485 (WebFetch) | about 22:29Z | 200 | Pinho's upper-bound preprint; states no lower bound and no explicit value of Biro's constant. |
| Web searches (standard and extended, about 11 queries on Biro's constant, "Turan pure power sum lower bound above 1/2", Zenodo, GitHub, arXiv, 2025/2026 citations, hexagon) | 22:22Z to 22:30Z | n/a | No source gives a numerical value of Biro's c or any explicit lower bound above 1/2 for this constant. |
| https://users.renyi.hu/~biroand/pdfs/Turan1.pdf (Biro 2000 paper, 16 pp.) | 2026-10-31T22:22:35Z | 200 | read in full (pdftotext). Quote: "We do not compute a concrete value of q, but it would be possible following the steps of our proof. It would be interesting (and it seems to be rather complicated) to determine the best constant obtainable by the ideas of this proof." |
| https://users.renyi.hu/~biroand/pdfs/AnUpperEstimateinTuran.pdf (Biro 2000b, upper bound) | 2026-10-31T22:28:02Z | 200 | intro restates "R_n > q for every n, where q is an absolute constant larger than 1/2"; no value. |
| https://www.renyi.hu/~gharcos/biro.pdf (Harcos note) | 2026-10-31T22:28:01Z | **403** | **BLOCKED. Stopped. Not retried, no other spelling, URL or tool.** Not read. (Its content as reported by Biro 2000b: Harcos's computer work gives the upper bound 0.69368.) |

### Not checked
- https://www.erdosproblems.com (any page, including 519, its forum and history): not fetched, per the rule that the site returned HTTP 403 earlier in this run. Search-engine result summaries (not a fetch by me) quote the problem 519 page as "improved by Biro first to c=1/2 [Bi94], and later to an absolute constant c>1/2 [Bi00]" and a forum comment proposing to compute a bound above 1/2 with Biro's method, with a reply "as far as I know nobody has actually computed what this method gives". This is second-hand and undated, so I treat it as unconfirmed supporting evidence only.
- MathSciNet, zbMATH, Google Scholar citing lists: not searched.
- Full-text search of GitHub code and arXiv full text: not available to me (search API for code needs login; arXiv API searches title and abstract only). A claim hidden inside an unindexed file or note cannot be excluded.

### For the main session (copy to NEEDS_YOU.txt and REPORT.md)
- HTTP 403 from https://www.renyi.hu/~gharcos/biro.pdf at 2026-10-31T22:28:01Z (Harcos's note on Biro's method). Step stopped, not retried. The same author's other host users.renyi.hu returned 200 for Biro's two papers.
- www.erdosproblems.com not checked in this seat (earlier 403 in this run; rule forbids retry).

## 4. This repo's record

- TROPHY_CASE.md: no entry for C_42, Turan power sums, Erdos 519 or optimizationproblems 42a (grep for Turan, power sum, C_42, 42a, Biro, 519 returned nothing relevant).
- known-knowns/ (all target folders): no entry for this target; the only "Turan" hits are the unrelated hypergraph Turan numbers in the sunflower-free capacity folders.
- known-unknowns/erdos-and-proofs/turan-pure-power-sum-c42-upper-bound.md (the target's brief, the only file outside the two named places that I opened): states Biro's c is "computable but uncomputed" and that win (ii) requires L above 1/2 and above Biro's explicit value "once that value has been published or established under p1". Consistent with what I found: it has not been published.

## 5. Comparison with the published objects for this cell and the neighbouring cells

Published objects in the cell (lower bound for C_42, equivalently for R_n for all n):
1. Atkinson 1961: 1/6. Atkinson 1969: pi/8 = 0.3927.
2. Biro 1994: 1/2, from the two Newton-Girard identities (3), (4) by absolute-value estimates. Biro 2000 says that without new formulas "it would be impossible to improve 1/2".
3. Biro 2000: some effectively computable q > 1/2, value never computed. The proof (read in full) is a contradiction argument that assumes |s_j| <= q with q "very close to 1/2", uses the new identity (14), and ends with "fix alpha < pi/4 close enough to pi/4, and then fix q > 1/2 close enough to 1/2". Its error functions f_i(q, alpha) go to 0 as q goes to 1/2 and alpha to pi/4, and they involve log-type decay in k (e.g. f_9 built from log log Q / log Q) and unspecified "large enough" absolute constants K_i. Any value this proof could yield is an unspecified number close to 1/2. This is my reading of the structure, not a computed value: I cannot show that Biro's c is below 0.501, only that the proof is built for q barely above 1/2 and no one has published a value.

Neighbouring cells (upper bounds 0.6863607950 and above, Andersson's other power-sum quantities, Exterior power sums): different quantity or opposite direction, nothing that edits into a lower bound.

Trivial edits (deletion, restriction, propagation, relabelling, symmetry, polish) of published objects: none gives an explicit number above 1/2. The only published object above 1/2 is non-explicit, so there is no explicit value to tie or beat except 1/2 itself. The claim's 0.501 is strictly above 1/2 (and above everything on the page and in the PR lists).

Seeding: claim/PROOF.md names Biro 2000 explicitly: "formula (F2) below is formula (14) of G. Biro's 2000 paper... The barrier at rho = 1/sqrt2 that (F1) expresses is the geometry of Biro's argument... it uses one test functional with fixed beta and gamma at each time, and a value function, so it is not an evaluation of his constant." I checked formula (14) in Biro's PDF: S_t + c_1 S_{t-1} + ... + c_{t-1} S_1 = 2(1 + c_1 + ... + c_{t-1}) - t c_t, with c_t = 1 + b_1 + ... + b_t. This matches (F2) (E1_t = sum s_i c_{t-i} = 2 N_t - t c_t, c_0 = 1). The credit is accurate. The identity (1.1) is the Newton-Girard identity that Biro and Harcos already use (Harcos remarks (14) also follows from inverse Newton-Girard). What is not in Biro: the test functional with fixed complex beta and gamma, the time-indexed value function V(tau, phi) on a grid with an HJB-type inequality, the one-sided path lemma, and the finite certificate. I found no paper, note, repository, PR or release using this construction for this constant. The proof is therefore a new route seeded from Biro's identity, not a numerical evaluation of Biro's own argument (which would only be partial win p1 in the target's rules).

Method known? Ingredients known (Newton-Girard recursion, Biro's (14), the 1/sqrt2 geometry); the combination (value function plus test functional) is not found in the literature or in code within what I could search.

## 6. Residual risks for the panel (not proven either way)

1. If someone later computes Biro's c and it exceeds 0.501, the claim would tie or lose under the frozen criterion. Evidence against that: Biro's proof is designed for q within an unspecified neighbourhood of 1/2, never computed (his own words), and nobody (page, three PR lists, issues, repos, Zenodo, arXiv) has published a value.
2. Erdos problems pages and forum were not read (second-hand snippets only).
3. The 42a page and the PR list move fast (several AI-driven fleets, last PR #305 today); a fresh re-fetch just before any outward step is needed. At 22:19Z the page was identical to the 22:02Z copy and the open PR list had the same 43 numbers.
4. Search tools cannot see inside files that are not indexed; absence of evidence, not proof of absence.

## Verdict

novelty: PASS. No explicit lower bound above 1/2 for C_42 exists on the status page, in any open or closed pull request, issue, release, repository, Zenodo record or arXiv listing that I could reach; Biro's constant is explicitly uncomputed by its author and by everyone else I could find; the claim names its seed (Biro's formula (14) and geometry) and is not an edit of any published explicit object. 0.501 strictly exceeds the best explicit value (1/2). Correctness of the proof and the certificates is for the other two skeptics; this verdict says nothing about it.

pass: true
