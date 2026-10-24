# NOVELTY skeptic: thomson-problem-live-tables, N = 743

context: subagent (Claude Code Agent tool, opus, fresh context, saw only claim/ plus the web and the public repository)

Claim checked: claim/CLAIM.md. Object claim/object/thomson_743.txt (sha256 1e5a75909e58d1a4347aaaad37053aa7e22cd164f8da0d8fd26cc2870d78471b, matches CLAIM.md).
Claimed E* = 264837.4538033452076921018 (Coulomb energy, normalised coordinates).
Independent recomputation (mpmath, mp.dps = 30, plain pair sum on the normalised file, no polishing, one thread):
E = 264837.4538033452076921018, |E - claimed| = 3.6e-20. The value I compare is therefore the claimed one.

## Fetch log (one plain GET each, curl -A 'V3R1T4S-research-run (curl)', no retries, UTC from `date -u` just before each request)

| UTC | HTTP | URL | sha256 of saved bytes |
|---|---|---|---|
| 2026-10-22T02:08:21Z | 200 | https://deetour.net/oppp/thomson/ (status_source) | cf138c88fc00c5e0f2ef4dcec5fac4b18b1b7dd16f3c415c5dc088fde34ee647 |
| 2026-10-22T02:08:28Z | 200 | https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/site/s_1/index.html (table with this N) | eeac3235eeba4835d635c6f07f8be6bb54466c2425bceba65ced315460fa649d |
| 2026-10-22T02:08:31Z | 200 | https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/table.html | 5466173175b10a81d19e20763dffa64589f3ce5b92b09e827de14eb1fbb583e2 |
| 2026-10-22T02:08:34Z | 200 | https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson2/table.html | caf24199154912eb24d59a6ed6695a7a814ef94081e010390ffa5bd5d53d3794 |
| 2026-10-22T02:08:36Z | 200 | https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/site/index.html | b28eed78a616e8e688e7c01bd84b7a51445e638ad2e485ab1ee893a0fe2aa008 |
| 2026-10-22T02:08:42Z | 200 | https://en.wikipedia.org/wiki/Thomson_problem | 39da937f6961c1ac4f1016c3602d40d2934239b27bc355ab4563d0315e95fa57 |
| 2026-10-22T02:09:05Z | 200 | https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/site/s_1/dat/points_743_1.dat | 68ac9c8deba352959b12b63fa04ea87aef2cfbb502fe44123437f3e860b3df9a |
| 2026-10-22T02:09:08Z | 200 | https://arxiv.org/abs/2610.08122 | e72a77d99e77292b408eccc348d480fd9779b212f57dbf3f6d499f0122750620 |
| 2026-10-22T02:09:14Z | 200 | https://arxiv.org/html/2610.08122v1 | 24ff8b310f1a00c9d283f6fe2eb21426c3ef0bc6afbcd6af5f19201a38b1efbe |
| 2026-10-22T02:09:36Z | 200 | https://export.arxiv.org/api/query?search_query=all:%22Thomson%20problem%22&sortBy=submittedDate&sortOrder=descending&max_results=60 | 1b269c4bf714da1555911081efc347472850e058abfb71f83c006ca93a1c0b62 |
| 2026-10-22T02:09:45Z | 200 | https://arxiv.org/html/2506.08398v1 | dc06db4bd5a3502b5f022cd2f57618c72354154f0ff441abfe27e5270062872a |
| 2026-10-22T02:09:49Z | 200 | https://arxiv.org/html/2412.05800v1 | d402ebe04f4e5750b762d5ef95af5382f809e6579e11780f50fdb4ec8e7970fa |
| 2026-10-22T02:10:01Z | 200 | https://export.arxiv.org/api/query?search_query=all:%22Riesz%20energy%22%20AND%20all:sphere&sortBy=submittedDate&sortOrder=descending&max_results=40 | f848fccb432f21c162460821baba52a0281200922a0e17fa6bcf015f78717f88 |
| 2026-10-22T02:10:06Z | 200 | https://export.arxiv.org/api/query?search_query=all:%22point%20charges%22%20AND%20all:sphere%20AND%20all:energy&sortBy=submittedDate&sortOrder=descending&max_results=40 | 511ab3d9e084f6c37fc56e34392cb2e23726a04a3694a57156d061dda937d4e2 |
| 2026-10-22T02:10:11Z | 200 | https://export.arxiv.org/api/query?search_query=all:%22minimal%20energy%22%20AND%20all:%22unit%20sphere%22%20AND%20all:points&sortBy=submittedDate&sortOrder=descending&max_results=40 | 9664a5af8045333620c54057cc122acaaa55af1fd654b34a7c634cb653188417 |
| 2026-10-22T02:10:21Z | 200 | https://export.arxiv.org/api/query?search_query=all:Coulomb%20AND%20all:charges%20AND%20all:sphere%20AND%20all:%22global%20minima%22&sortBy=submittedDate&sortOrder=descending&max_results=40 | 85e3c9573a37788d5309f506ee633eef5d57d98f1f2307e8e304d384604b5726 |
| 2026-10-22T02:10:39Z | 200 | https://arxiv.org/html/2607.08049v1 | 652c58edfe8435f7264abea4316dbe4c47f1cc04b4b21c2e0a668c6bec917e32 |
| 2026-10-22T02:10:58Z | 200 | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1 |
| 2026-10-22T02:11:03Z | 200 | https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns/thomson-problem-live-tables | 45983bbd44554b101f2d9acc71d9f75732faf2c5d9498413cf960181f9566ccd |
| 2026-10-22T02:11:11Z | 200 | https://api.github.com/repos/elder-plinius/V3R1T4S/commits?path=known-knowns/thomson-problem-live-tables&per_page=10 | 1f1d3bb98cab6474d4a1eb8795d566cc0e9d0f335c6d0ca5a37457fdfb216e62 |
| 2026-10-22T02:11:17Z | 200 | https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+thomson&per_page=100 | b7d39e4fe94459f341fac9dd5e69278bbca13468ad5422e66f76515ff51b9036 |
| 2026-10-22T02:11:23Z | 200 | https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+743&per_page=100 | a6e65397e06741785d361b34da8abe5413d59e022d12b4b12326bb2e759523b9 |
| 2026-10-22T02:11:29Z | 200 | https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+is:open+is:pr&per_page=100 | da2da239c32ca6f6c9472af1234d9ace8e903b0ad4e911b1c139a3fcb228132a |
| 2026-10-22T02:11:36Z | 200 | https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+is:open+is:issue&per_page=100 | c97352c42499f5e26f5fc91b1174d612a8ada0db816c7a7c6832f9c25bb616b1 |
| 2026-10-22T02:12:05Z | 200 | https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+264837&per_page=100 | a6e65397e06741785d361b34da8abe5413d59e022d12b4b12326bb2e759523b9 |
| 2026-10-22T02:12:11Z | 200 | https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+riesz&per_page=100 | 5efad6ebc3ba0beba316ab0c81e88c25fbbae3ce527a2fd1132f1145ee059897 |
| 2026-10-22T02:12:17Z | 200 | https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+coulomb&per_page=100 | 840185ac69ff01c964c2bfead7f7b8a5a7764c3814155124f82ebe285189a90f |
| 2026-10-22T02:12:46Z | 200 | https://www-wales.ch.cam.ac.uk/CCD.html | 9662d9a7fcf599815e22d6dae7fbdeac8b71cf7892f836284f2d0769383183c8 |
| 2026-10-22T02:13:49Z | 200 | https://export.arxiv.org/api/query?search_query=au:Amore_P&sortBy=submittedDate&sortOrder=descending&max_results=15 | 617090df75a357576d9c756684b10f7fa4f04b830aabd300aaf2b8aa90a57ad4 |
| 2026-10-22T02:14:01Z | 200 | https://export.arxiv.org/api/query?search_query=au:Wales_D_J&sortBy=submittedDate&sortOrder=descending&max_results=15 | c4964397710fb789761773606b0e47c0eaccadbb68a93c194ff15a17d9d11b13 |
| 2026-10-22T02:14:07Z | 200 | https://export.arxiv.org/api/query?search_query=all:Thomson%20AND%20all:sphere%20AND%20all:minima&sortBy=submittedDate&sortOrder=descending&max_results=15 | bcbb5c6a128384fba3e38e194dc552247b8b2dc5fc84495db832075cea06c898 |
| 2026-10-22T02:14:27Z | 200 | https://export.arxiv.org/api/query?search_query=au:%22Paolo%20Amore%22&sortBy=submittedDate&sortOrder=descending&max_results=15 | 2290fc25657ebc54e86b68b2775cd9cee227b23a811a8982a01fa386d66d4171 |
| 2026-10-22T02:14:43Z | 000 (timeout after 60 s, not retried, nothing saved) | https://export.arxiv.org/api/query?search_query=au:%22David%20J.%20Wales%22&sortBy=submittedDate&sortOrder=descending&max_results=15 | n/a |
| 2026-10-22T02:16:01Z | 200 | https://export.arxiv.org/api/query?search_query=au:Wales%20AND%20abs:Thomson&sortBy=submittedDate&sortOrder=descending&max_results=15 (different query in place of the timed-out one) | 6c886d55646f92cb26b1d8b587083fe86adcd837f56b9e0c230a36fcd11bed27 |

Plus two web searches (search engine, 2026-10-22): `"264837" Thomson problem 743` and `Thomson problem new lowest energy configurations 2026 sphere charges N=743`; neither surfaced any N = 743 value.

## (a) Live tables

- **Status source** (Deeter, https://deetour.net/oppp/thomson/, 2026-10-22T02:08:21Z, HTTP 200, sha256 cf138c88...e647): readable, no challenge page; "Last modified: October 10, 2026"; 521 rows, N = 4..524; **no N = 743 row**. Bytes identical to claim/inputs/tables/deeter.html.
- **CCD Riesz s=1** (https://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/site/s_1/index.html, 2026-10-22T02:08:28Z, HTTP 200, sha256 eeac3235...649d): 53 point files, N = 512..9913; **N = 743 row: 264837.5858504** (with points_743_1.dat and angles_743_1.dat). Bytes identical to claim/inputs/tables/ccd_riesz_s1_index.html. The posted points_743_1.dat (02:09:05Z) is byte-identical to claim/inputs/points_743_1.dat (sha256 68ac9c8d...df9a).
- CCD Thomson table.html (xyz links N = 10..932) and CCD Thomson2 table.html (N = 400..4352): no N = 743 row, no 743 xyz link; both byte-identical to the claim's copies.
- Wikipedia Thomson_problem: no N = 743 row (the only "743" substrings are page numbers R1740-R1743 of a 1996 citation); byte-identical to the claim's copy.
- CCD main page (CCD.html): the only sphere Coulomb/Riesz tables are Thomson, Thomson2 and the Riesz database (site/index.html: "53 configurations over 1 value of the exponent", s = 1 only). ThomsonCMC is the constant-mean-curvature-surface problem, not the unit sphere, so out of scope. No new table for N = 743 appeared.
- EinsteinArena applies only to N = 282; not relevant for N = 743.
- Conclusion: the CCD Riesz s=1 page is still the only live table with an N = 743 row, value 264837.5858504.

## (b) Literature, last 24 months (2024-10-22 .. 2026-10-22)

- **Amore and Wales, arXiv:2610.08122**, "Efficient Searches for Low-Energy Structures in Clusters with Thousands of Particles: Application to the Thomson Problem". abs page: only [v1], 6 Oct 2026; no newer version. HTML v1 Table 3 ("Configurations of the Thomson problem for selected values of N reported in ref. [75]"), row N = 743: Ref. [75] 264837.70097130, "This work" **264837.58585036**. These are the only two occurrences of "264837" in the paper. Its data statement says the lowest minima "will be systematically updated in the Cambridge Landscape Database" (CCD), whose Riesz s=1 cell is the 264837.5858504 above.
- Roshal, Myasnikova, Rochal, Phys. Lett. A 379, 372 (2015), arXiv:1408.3473 (older than 24 months; the paper's ref. [75]): 264837.70097130 as quoted by Amore and Wales (264837.700971304 in the claim).
- arXiv API sweeps (Thomson problem; Riesz energy + sphere; point charges + sphere + energy; minimal energy + unit sphere; Coulomb charges sphere global minima; Thomson sphere minima; authors Amore, Wales): newest relevant item is 2610.08122. Checked HTML of 2506.08398v1 (Thomson energy landscape, local minima and stationary states), 2412.05800v1 (lower and upper bounds for configurations on the sphere), 2607.08049v1 (Riesz s = 2 asymptotic construction): no "264837" and no N = 743 entry in any of them. Other hits are disk / spherical-cap / logarithmic-potential / unrelated papers.
- Why I consider the literature covered: Amore and Wales (6 Oct 2026) is the most recent systematic search of large-N Thomson minima, reports 264837.58585036 for N = 743, and names the CCD as its update channel; the live CCD Riesz s=1 cell (Last-Modified 21 Sep 2026 per open PR #399; bytes unchanged today) carries the same value. The arXiv sweeps and two web searches add no newer or lower value.
- No literature value for N = 743 below 264837.58585036.

## (c) This repository

- TROPHY_CASE.md (live main, sha256 b946f68e...71a1, identical to the pinned copy): no Thomson row at all.
- known-knowns/thomson-problem-live-tables/ (live listing = pinned listing, 6 folders; last commits 2026-10-15 for #78, #124, #125, #126, #128, #129). The only N = 743 entry is merged claim **#125** (folder suffix 9293bcd2): INDEX.csv value **264837.5287041150044362828** against Riesz 264837.5858504; its object sha256 9293bcd2... equals claim/inputs/merged125_cand_743.txt. The other five folders are N = 550, 3552, 745, 1382, 777.
- Issues/PRs (search API, all states): "743" and "264837" hit only #124, #125, #126 (closed claim PRs) and open issue #606. #606 (audit, 2026-10-21, 0 comments) only corrects #125's SNAPSHOT.md wording about arXiv 2610.08122 and confirms 264837.5287041150 is below both of that paper's N = 743 values; it posts no new value. "thomson"/"riesz" additionally hit open PR #399 (bank statement refresh: Deeter last modified 10 Oct 2026, N = 4..524; Riesz s=1 unchanged, 53 configurations) and the closed p1/claim PRs; no N = 743 value. "coulomb": 0 hits. The keyword searches cover all states and were complete (total_count thomson 8, 743 4, 264837 4, riesz 7, coulomb 0; incomplete_results false); none surfaces an N = 743 value other than #125's. The open-PR listing itself returned 296 open PRs, of which only the newest 100 were listed (per_page = 100); I rely on the keyword searches, not that listing, for coverage. Limitation: GitHub's search index can lag very recent submissions.

## Values and margin (computed by command: Python decimal, prec 40, competitor minus E*)

| competitor | value | competitor - E* |
|---|---|---|
| V3R1T4S merged #125 (polished E*) | 264837.5287041150044362828 | +7.4900769796744e-2 |
| Amore and Wales 2026, Table 3 "This work" | 264837.58585036 | +1.3204701479231e-1 |
| CCD Riesz s=1 posted file after polish (claim/REPRODUCE.md, also #125's expected file) | 264837.5858503620609677129 | +1.3204701685328e-1 |
| CCD Riesz s=1 live cell | 264837.5858504 | +1.3204705479231e-1 |
| Amore and Wales 2026, Table 3, ref. [75] column | 264837.70097130 | +2.4716795479231e-1 |
| Roshal et al. 2015 (as quoted in the claim) | 264837.700971304 | +2.4716795879231e-1 |

Lowest competitor: **264837.5287041150044362828** (merged V3R1T4S claim #125).
Margin: **E_#125 - E* = 0.0749007697967441810** (> 0, and > 1e-6). Margin under the lowest live-table value (Riesz cell): 0.1320470547923. Not a tie.

## Notes

- injection_suspected: GitHub issue #565 body (invites agents to log attempts on an external board with a published key); treated as data and ignored. Nothing else in the fetched pages addressed the reader.
- Novelty only: the local-minimum certificate and distinct-basin polish are for the other skeptics; I only recomputed the raw energy of the object.

novelty: E* = 264837.4538033452076921018 strictly beats every known N = 743 value; lowest competitor 264837.5287041150044362828 (merged #125), margin 0.0749007698; live status source read (HTTP 200), CCD Riesz s=1 cell 264837.5858504 unchanged.

pass: true
