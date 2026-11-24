role: novelty
context: fresh subagent (new context, no prior conversation; saw only repo/kit/RULES.md, the NOVELTY section and header of PANEL_BRIEFS.md, and a copy of claim/ in sandbox/panel-0527-novelty/claim; did not open attempts/, notes/ or other panel files)
claim: Assuming GRH for Dirichlet L-functions (and RH), Brun's constant satisfies B < 2.126988 (CLAIM.md; partial win p1).
date_utc: Tue Nov 24 06:07:50 UTC 2026

## 1. Primary status page (one plain fetch, no retry)
- URL: https://teorth.github.io/optimizationproblems/constants/81a.html, User-Agent "V3R1T4S-panel-novelty/1.0", fetched 2026-11-24T06:01:30Z, HTTP 200.
  sha256 f8344f6ab5e7162878949de7b362dcbe4e5a54a48df35185e564e1901d4e0cc9 (identical to the claim's data/81a.html).
- Upper-bound rows quoted: 2.347 [CP2005]; 2.175398 [K2007] "Conditional on the Generalised Riemann Hypothesis"; 2.288513 [PT2018]
  "Unconditional"; 2.1594 [D2025] "Conditional on the Generalised Riemann Hypothesis, and the best conditional bound known".
  Lower bound 1.840503 [PT2018]. No row below 2.1594. (KNOWN)

## 2. Literature and code, last 24 months and the named classics (all fetched with UA V3R1T4S-panel-novelty/1.0)
| source | URL / DOI | fetched (UTC) | HTTP | finding |
|---|---|---|---|---|
| Dunn, arXiv:2504.15658v2 / BAustMS 113 (2026) 293-303 | claim/data/dunn_arxiv2504.15658v2.txt (claim copy); DOI 10.1017/S0004972725100233 via api.crossref.org | 06:05:57Z (Crossref) | 200 | B < 2.1594 under GRH; remainder via r(z)^2 (|lambda_d| <= 1); Sec. 5 "Potential Improvements" lists only splicing, larger x0, parameter optimisation, no use of the weights. Crossref is-referenced-by-count 0. |
| Dunn code github.com/LachlanJDunn/B_Under_GRH | api.github.com/repos/LachlanJDunn/B_Under_GRH (+ /commits, /releases, /contents) | 06:03:50Z | 200 x4 | last push 2025-05-16 ("v2"); 0 releases; files compute_B.jl, B_result.jld2, V_list.jld2. No newer bound. |
| Klyve, thesis 2007 Ch. 5 | claim/data/klyve2007.txt (claim copy, text of the Dartmouth PDF) | (claim copy) | n/a | Bounds the remainder by bounding every |lambda_delta| (lines ~5226-5305: "|lambda_delta| = 1"); B < 2.1754 (Thm 5.16). No sum |lambda_d| saving. |
| Platt-Trudgian arXiv:1803.01925v1 | https://arxiv.org/pdf/1803.01925v1 | 06:05:38Z | 200 | Unconditional 2.288513; pi_2 via Riesel-Vaughan and the Montgomery-Vaughan large sieve (Cor. 1), no Selberg lambda_d remainder. |
| Riesel-Vaughan, Ark. Mat. 21 (1983) 45-74, DOI 10.1007/BF02384300 | https://archive.ymsc.tsinghua.edu.cn/pacm_download/116/7384-11512_2006_Article_BF02384300.pdf | 06:05:38Z | 200 | Sieve estimate from Montgomery-Vaughan large sieve Cor. 1 (their Lemma 5); no lambda_d weights. |
| Vaughan, "Some remarks on Selberg's sieve" (notes) | https://personal.science.psu.edu/rcv4/Selberg.pdf | 06:05:21Z | 200 | Textbook use of the exact weight formula: |lambda_m| <= m phi(m)^-1 G(D/m)/G(D), then R << D^2 log^-2 D, i.e. sum |lambda_m| << D/log D (dimension 1, Brun-Titchmarsh). |
| Vaughan, Math 571 Ch. 4 (2025) | https://personal.science.psu.edu/rcv4/571s25/Class571-04.pdf | 06:05:21Z | 200 | |R| <= (sum_d |lambda_d|)^2; |lambda_m| <= 1 from the exact weights. |
| Elkies, Math 229 sieve notes | https://people.math.harvard.edu/~elkies/M229.20/sieve.pdf | 06:05:21Z | 200 | |lambda_d| <= 1 from the exact weights; no sum identity. |
| Daniyarov, Zenodo 10.5281/zenodo.23211849 (2026-10-09) + software 10.5281/zenodo.23210497 | https://zenodo.org/api/records/23211849, .../23261476/files/aggregate-capacity-paper-1.0.0.pdf, https://zenodo.org/api/records/23210497 | 06:02:29Z, 06:02:35Z, 06:03:40Z | 200 x3 | Unconditional B2 < 2.27428 (unrefereed preprint); cites Dunn 2.1594 as the conditional record; no GRH bound. |
| Sergaev, Zenodo 10.5281/zenodo.24434237 (2026-11-22) | https://zenodo.org/api/records/24434237, .../24434238/files/sergaev-brun-preprint.pdf | 06:03:30Z, 06:03:39Z | 200 x2 | Chaffin counts 1.84179421208934 < B(1e19) < 1.84180921261947; unconditional B < 2.281721; no RH used. |
| Johnston, UNSW thesis 2025, DOI 10.26190/unsworks/31766 | https://unsworks.unsw.edu.au/bitstreams/dbc4cbe9-fbbd-4d35-98e4-250c5e945c80/download | 06:06:15Z | 200 | Explicit linear sieve; no Brun's constant, no Dunn. |
| arXiv 2602.22720v4 (explicit Selberg Lambda-Lambda^2 lower sieve) | https://arxiv.org/pdf/2602.22720v4 | 06:04:39Z | 200 | Not Brun/pi_2; no sum |lambda_d| identity. |
| arXiv API: abs "Brun's constant" | export.arxiv.org/api/query (https) | 06:02:58Z | 200 | Only 2504.15658 since 2018 (plus unrelated). (http:// variant at 06:02:46Z returned 500.) |
| arXiv API: abs "twin primes" AND explicit; abs "Selberg sieve" AND explicit; all:Brun AND math.NT; au:Dunn_L; abs "twin prime" AND Selberg | export.arxiv.org/api/query | 06:03:01Z, 06:03:05Z, 06:06:34Z, 06:06:37Z, 06:06:40Z | 200 x5 | Nothing since 2024-11 giving a Brun bound or applying exact Selberg weights to pi_2 / Brun (2005.04280 Zuniga Alterman: explicit Selberg-sieve log sums, dimension 1, Brun-Titchmarsh application only). |
| OpenAlex: works citing Dunn (W4412042085); search "Brun's constant" since 2024-11; search "selberg sieve twin primes explicit" since 2024-11 | api.openalex.org | 06:03:23Z, 06:05:57Z | 200 x4 | 0 citing works; 22 and 103 hits screened by title: only Dunn, the two Zenodo items above and crank/unrelated items. |
| Google Scholar (citations of Dunn) | https://scholar.google.com/scholar?q=... | 06:05:57Z | 403 | Blocked; not retried. Scholar citation check PENDING (human). |
| Semantic Scholar citations API | api.semanticscholar.org/graph/v1/paper/arXiv:2504.15658/citations | 06:03:23Z | 429 | Rate-limited; not retried. |
| Zenodo search API | zenodo.org/api/records?q=... | 06:02:45Z, 06:02:54Z | 400 x2 | Query syntax rejected; Zenodo covered via OpenAlex instead. |
| WebSearch (3 queries on Brun GRH bounds; 4 on sum |lambda_d| / textbook) | search tool | ~06:01-06:05Z | n/a | Surfaced the items above, MathWorld (Dunn 2026 as GRH record) and Wikipedia (quotes Dunn v1 2.1609). |
Not opened (paywalled books, no free full text found): Halberstam-Richert "Sieve Methods" Ch. 3; Friedlander-Iwaniec "Opera de Cribro";
Greaves "Sieves in Number Theory"; Montgomery-Vaughan "Multiplicative Number Theory I". Statements about them are not made from the source.

## 3. Repo checks
- TROPHY_CASE.md: local repo/TROPHY_CASE.md and https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md (06:03:58Z, 200): no Brun/twin/Selberg/sieve entry.
- known-knowns/: local tree and api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns (06:03:58Z, 200, 47 entries): no Brun/twin-prime entry.
- elder-plinius/V3R1T4S PRs: search API "brun", "twin prime", "selberg" is:pr (06:01:47-48Z, 200) and full list of the 200 most recent PRs, all states
  (06:01:58-59Z, 200, created 2026-11-08..2026-11-24): the only Brun PR is #1231 (open, 2026-11-24T03:28:35Z, B < 2.156967, same contributor; read as metadata only).
  Releases: 0 (06:03:51Z, 200).
- teorth/optimizationproblems PRs: search "brun", "81a", "twin" (06:01:48-49Z, 200): #48 (merged 2026-03-11, adds constant 81) and #147 (merged 2026-08-23,
  Klyve marked conditional). 200 most recently updated PRs (06:02:00-01Z, 200): no 81a/Brun PR open. Releases: 0.

## 4. Owner's questions
(i) Closed form sum_{d<=z} |lambda_d| = W(z)/V(z): the technique of bounding the remainder through the exact Selberg weights (rather than |lambda_d| <= 1) is classical
    and appears in Vaughan's notes (sum |lambda_m| << D/log D, dimension 1) [KNOWN]. I did not find, in any source I opened, the exact identity in Dunn/Klyve's
    twin-prime setting; it is a two-line rearrangement (PROOF.md S2) and is very likely folklore [HEURISTIC]. Either way, per the brief, this does not decide novelty of the bound.
(ii) Exact Selberg weights / sum |lambda_d| bounds applied to Brun's constant or to explicit pi_2(x): none found. Klyve and Dunn use |lambda_d| <= 1 (r(z)^2 = M(z)^2);
    Platt-Trudgian and Riesel-Vaughan use the large sieve; the 2026 Zenodo preprints are unconditional and use other methods [KNOWN, from opened sources].

## 5. Comparison with the cell and neighbours
- Cell (GRH upper bound): best published 2.1594 (Dunn). Claim 2.126988 < 2.1594, strict, margin ~0.0324. Also below the same contributor's unmerged 2.156967 (PR #1231)
  and Klyve's 2.1754.
- Neighbour (unconditional): 2.288513 (PT2018), 2.281721 (Sergaev, Zenodo), 2.27428 (Daniyarov, Zenodo); none conditional, none below 2.126988.
- Trivial-edit test: the claim is Dunn's framework with a changed remainder estimate, not a deletion, restriction, relabelling, symmetry or local polish of a published object.
  The claim's own ablations (out/, not rerun by me; REPRODUCE's job) put Dunn's framework with all other changes and free parameter optimisation at 2.1569674, and Dunn's
  original inputs plus the weights at 2.1282623, so the gain comes from the weights. A valid propagation from published data (Chaffin's B(1e19) <= 1.841810 in place of
  B(4e18) <= 1.840518) only moves the start of Dunn's tail from 4e18 to 1e19; Dunn's bound is 1.840518 + tail, the tail is ~0.319, and the part of it between 4e18 and 1e19 is far less
  than the 0.032 needed (HEURISTIC estimate, not computed). The claim is seeded from Dunn and names him.
- Residual risk: Google Scholar and Semantic Scholar citation checks were blocked (403/429) and the paywalled sieve books were not opened. OpenAlex and Crossref show 0 citations
  of Dunn, and no source anywhere states a GRH bound below 2.1594.

Verdict: on everything I could open (fetched 2026-11-24 06:01-06:07Z), B < 2.126988 under GRH strictly beats every published or submitted bound for this cell (best 2.1594, Dunn),
and no source applies exact Selberg weights or sum|lambda_d| bounds to Brun's constant or pi_2. Novelty is in the bound and in this application, not in the sieve technique, which is classical.
This pass covers novelty only, not correctness.
pass: true
