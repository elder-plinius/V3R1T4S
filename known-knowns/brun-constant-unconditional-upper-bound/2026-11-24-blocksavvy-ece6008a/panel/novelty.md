role: NOVELTY
context: fresh subagent (no prior conversation; given only kit/RULES.md, the PANEL_BRIEFS.md common header and NOVELTY section, and a copy of claim/ at sandbox/panel-0729-novelty/claim; did not open attempts/, notes/, runs/2026-11-24-0527/ or any earlier panel file)
claim: under GRH (Dirichlet L-functions incl. RH), Brun's constant B < 2.1257395 (partial win p1); one-step change (section R, per-modulus combination of the Selberg remainder) to the same contributor's unmerged e6b84d42 claim B < 2.126988
date_utc: 2026-11-24T08:31:58Z

## 1. Primary status page (one plain fetch, UA "V3R1T4S-novelty-panel/1.0 ...", no retry)
- https://teorth.github.io/optimizationproblems/constants/81a.html  HTTP 200  2026-11-24T08:20:13Z  6066 bytes,
  sha256 f8344f6ab5e7162878949de7b362dcbe4e5a54a48df35185e564e1901d4e0cc9, byte-identical to claim/data/81a.html.
  Value quoted from the page: upper bound "2.1594 [D2025] Conditional on the Generalised Riemann Hypothesis, and the best conditional
  bound known"; other upper rows 2.347 [CP2005], 2.175398 [K2007] (GRH), 2.288513 [PT2018] (unconditional). (KNOWN)
- Source file https://raw.githubusercontent.com/teorth/optimizationproblems/main/constants/81a.md  HTTP 200  08:30:58Z: same rows.
  Commit history of constants/81a.md (api.github.com .../commits?path=constants/81a.md, HTTP 200, 08:30:59Z): last change
  2026-08-23T17:16:13Z "C_81: record Dunn's GRH-conditional bound B < 2.1594".
- Open PRs in teorth/optimizationproblems (api.github.com .../pulls?state=open, HTTP 200, 08:30:58Z; 49 open): none concerns C_81 /
  81a / Brun (regex hits in #330, #203 were hex substrings "81a" inside commit hashes). Search API "81a is:pr" (HTTP 200, 08:24:37Z):
  only #147 (closed, Klyve marked GRH); "Brun is:pr" (HTTP 200, 08:24:43Z): only #48 (closed, page creation).

## 2. Owner requirement (ii): any published GRH bound below Dunn's 2.1594?  Answer: none found.
Every source, with URL, UTC fetch time and HTTP status (full log with sizes/hashes: sandbox/panel-0729-novelty/fetch/LOG.txt):
- Dunn, arXiv:2504.15658 https://arxiv.org/abs/2504.15658  200  08:20:29Z: versions [v1],[v2]; abstract "yielding B < 2.1594".
  Published version DOI 10.1017/s0004972725100233 (Crossref https://api.crossref.org/works/10.1017/s0004972725100233, 200, 08:30:37Z:
  Bull. Aust. Math. Soc., published 2025-07-04, is-referenced-by-count 0).
- github.com/LachlanJDunn/B_Under_GRH: repo API 200 08:20:29Z (pushed_at 2025-05-16T09:09:25Z); releases 200 08:20:29Z = [] ;
  tags 200 08:20:29Z = [] (no release assets); commits 200 08:20:29Z (16 commits, last 2025-05-16 "v2"); tree 200 08:31:06Z
  (compute_B.jl, B_result.jld2, V_list.jld2, README, LICENSE); compute_B.jl raw 200 08:31:14Z: r_coeff_up(z) = M(z) (count of odd
  squarefree <= z, i.e. |lambda_d| <= 1 and the pair-by-pair remainder); no per-modulus grouping, no smaller bound.
- Platt-Trudgian arXiv:1803.01925 https://arxiv.org/abs/1803.01925  200  08:20:30Z: unconditional 1.840503 < B < 2.288513.
- Klyve thesis 2007: read from claim/data/klyve2007.txt (not re-fetched); GRH bound 2.1754 per the 81a page, superseded by Dunn.
- arXiv API export.arxiv.org/api/query (5 queries) 500 at 08:20:33Z-08:20:49Z (server error, not a block; not retried); the same
  searches were run once each on arxiv.org/search instead:
  "Brun's constant" all fields 200 08:21:01Z: 6 results, newest 2504.15658; "Brun constant twin" abstracts 200 08:21:19Z: 3 results
  (2504.15658, 1803.01925, 1002.4174); "twin prime explicit" 200 08:21:36Z: 19 results, none a Brun bound; "explicit Selberg sieve"
  200 08:21:55Z: 12 results, none on Brun's constant.
- Zenodo API (size=50 returned 400 "Page size cannot be greater than 25" at 08:22:17Z/08:22:23Z: my malformed request; re-issued once
  with size=25): "Brun's constant" 200 08:23:16Z (9 records); "twin prime" AND explicit 200 08:23:53Z (131 hits, newest 25 read);
  "Daniyarov Parseval" 200 08:26:24Z; "Brun constant GRH" 200 08:26:52Z (newest 25, none relevant). Relevant records opened:
  * Sergaev, "Updating explicit bounds for Brun's constant at 10^19", 10.5281/zenodo.24434238 (2026-11-22), PDF 200 08:25:18Z,
    script 200 08:25:26Z: UNCONDITIONAL 1.84179421 < B < 2.281721; no GRH bound.
  * Daniyarov, "Aggregate Parseval Sieving ... Explicit Bounds for Brun Constants", 10.5281/zenodo.23261476 v1.0.0 (2026-10-09;
    versions API 200 08:28:13Z: v0.9.0 23211850, v1.0.0), PDF 200 08:27:46Z: Theorem 1.1 UNCONDITIONAL B2 < 2.27428; text says
    "Dunn proved the stronger conditional estimate B2 < 2.1594 under the generalized Riemann hypothesis". Companion
    10.5281/zenodo.23210498 (certificates, same bounds). No GRH bound below 2.1594.
- Citations of Dunn: Google Scholar https://scholar.google.com/scholar?...  403  08:22:16Z; Semantic Scholar
  https://api.semanticscholar.org/graph/v1/paper/arXiv:2504.15658?...  429  08:22:16Z. Both STOPPED, not retried (RULES 5):
  PENDING HUMAN CHECK for these two indexes. Independent indexes: OpenAlex work W4412042085 (https://api.openalex.org/works/W4412042085,
  200, 08:29:07Z; cited_by_count 0) and filter=cites:W4412042085 (200, 08:29:07Z): 0 citing works; OpenCitations
  https://api.opencitations.net/index/v2/citations/doi:10.1017/s0004972725100233 200 08:30:37Z: [] ; Crossref count 0 (above).
  (An earlier OpenAlex cites query at 08:24:31Z returned 400 because my script passed an empty id; corrected once.)
  Crossref bibliographic search "Brun's constant" from 2024-11 (200, 08:22:17Z): 40 rows, none mathematical.
- GitHub repository search "Brun constant twin prime" (200, 08:25:03Z): 0 repositories.
- elder-plinius/V3R1T4S PRs: pulls?state=all (100 most recent, 200, 08:24:50Z) and search "Brun is:pr" (200, 08:24:56Z, 21 hits):
  the only Brun PRs are #1231 (open draft, B < 2.156967) and #1232 (open draft, branch claim/2026-11-24-blocksavvy-e6b84d42,
  B < 2.126988), both by this contributor, unmerged; not prior art, and 2.1257395 < 2.126988 < 2.156967 (strict).
- This repo: TROPHY_CASE.md (local repo copy and upstream raw https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md,
  200, 08:30:38Z): no Brun / twin-prime entry. known-knowns/ (local, and upstream contents API 200 08:30:38Z, 47 entries): no Brun
  target directory; local "brun" text hits are only "Brun-Devetak-Hsieh" (quantum codes). Bank entry
  brun-constant-unconditional-upper-bound p1: "Under GRH, a bound B < U' with U' strictly below Dunn's 2.1594, at the same proof
  and certification standard."
Result (ii): best published GRH bound remains Dunn's 2.1594 (KNOWN, from sources opened above). 2.1257395 < 2.1594 strictly
(gap 0.0337) and < the contributor's own 2.126988 strictly (gap 0.0012485). Not a tie.

## 3. Owner requirement (i): is rho_q = sum_{[d1,d2]=q} lambda_d1 lambda_d2 standard?  Answer: YES (KNOWN).
- Tao, 254A Notes 4 "Some sieve theory", https://terrytao.wordpress.com/2015/01/21/254a-notes-4-some-sieve-theory/ (200, 08:29:49Z),
  eq. (28): "lambda^+_d := sum_{d_1,d_2: [d_1,d_2] = d} rho_{d_1} rho_{d_2} ... is a sequence of upper bound sieve coefficients", then
  "|lambda^+_d| <= sum_{[d_1,d_2]=d} 1 = tau_3(d)". The Selberg sieve written as an upper-bound sieve with remainder sum_d |lambda^+_d| |r_d|
  is exactly Sigma(z) * max|R_q| after taking the max. So the per-modulus combination is textbook.
- Vaughan, "Selberg" notes https://personal.science.psu.edu/rcv4/Selberg.pdf (200, 08:20:30Z): keeps the signed remainder
  R = sum_d sum_e lambda_d lambda_e R_[d,e] and bounds it by (sum |lambda_d|)^2 (Example 8); no explicit numerical use of the grouping.
- Klyve thesis (claim/data/klyve2007.txt, (5.16)) and Dunn (claim/data/dunn_arxiv2504.15658v2.txt, Theorem 2.1:
  R(x,z) = sum_{d1,d2} |E(x;[d1,d2])|; compute_B.jl r = M(z)) do NOT use it: both put absolute values on each pair.
- Not opened (books/paywalled, so not cited): Halberstam-Richert Ch. 3, Friedlander-Iwaniec "Opera de Cribro", Greaves,
  Montgomery-Vaughan, explicit Brun-Titchmarsh papers. arXiv 2602.22720 and 2211.11012 (explicit Selberg-sieve applications,
  both 200 08:29:50Z) were opened; text search found no use of the grouped weights.
Consequence: the IDEA of change R is KNOWN and must not be presented as a new sieve method; the claim itself labels R2 "PROVED-HERE,
elementary", which is fair for the two-line identity but the package should credit the standard form (e.g. Tao Notes 4 eq. (28),
Selberg's upper-bound-sieve coefficients) - a credit gap (RULES 13) to fix in packaging, not a novelty failure of the number.

## 4. Trivial-edit test (kit text)
Seeded from: Dunn arXiv:2504.15658v2 / compute_B.jl (named in CLAIM.md and PROOF.md) via the contributor's unmerged a26bba47 and
e6b84d42. The new step is not a deletion, restriction, relabelling, symmetry, or a re-optimisation of Dunn's parameters: it replaces
Lambda(z)^2 by a different, smaller certified quantity Sigma(z) that requires a new exact computation (20 levels n in 3363..19999).
Own spot check (sandbox/panel-0729-novelty/sigma_small.py, exact Fractions from Klyve (5.24)-(5.26) as quoted in PROOF.md R3,
NUMERICAL): Sigma(n)/Lambda(n)^2 = 0.6328 (n=50), 0.6561 (100), 0.6337 (200), 0.6222 (300); lambda_1 = 1 exactly. The cancellation is
real and consistent with the claimed ~0.645 for n in 3000..20000, so the gain is not a relabelling. The claim's control K1
(out/K1_rho_off_p128.json, change off -> 2.1269872000642055706 = e6b84d42 value) attributes the 0.0012478 gain to R alone, not to a
z_i polish. I did not run a parameter polish of Dunn's own Julia code; the 0.0337 gap to 2.1594 is far beyond what Dunn's paper
or code suggests for re-optimisation alone, and the earlier steps (a26bba47, e6b84d42) are not this panel's object.
Correctness of R1-R3, of the Sigma certificate and of the whole e6b84d42 base is the REPRODUCE skeptic's job; whether a 0.00125 step
over an unmerged own claim is a non-subsumed p1 win is the CRITERION skeptic's job (note: p1 is defined relative to Dunn's 2.1594).

## 5. Injection / anomalies
injection_suspected: none. The Sergaev and Daniyarov Zenodo preprints state AI-drafted content; treated as data only, both unconditional.

## Needs you
- Google Scholar (403) and Semantic Scholar (429) citations of Dunn could not be checked; please check by hand. OpenAlex, Crossref and
  OpenCitations all show 0 citing works.
- Packaging: credit the standard per-modulus (lambda^+_q) form of the Selberg remainder (e.g. Tao 254A Notes 4 eq. (28)).

confirmed_scope (novelty only): no published or posted GRH-conditional upper bound for Brun's constant below Dunn's 2.1594 was found
in the sources listed above as of 2026-11-24T08:31Z, and 2.1257395 is strictly below both 2.1594 and the contributor's unmerged
2.126988 and 2.156967; the per-modulus grouping it uses is a known textbook form, newly applied numerically here.
pass: true
