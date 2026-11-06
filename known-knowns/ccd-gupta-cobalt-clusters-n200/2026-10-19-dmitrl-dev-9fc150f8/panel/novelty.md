# NOVELTY panel report: claim p1, target `ccd-gupta-cobalt-clusters-n200`

context: subagent (fresh-context delegation)

Role: NOVELTY (kit/RUN.md step 6). Input: only the claim archive `claim_p1.zip` (sha256 `b700d809cbe05fb1feeb02bea1fd5b8ef9c266231b33fcefe60de5f63279c285`, 314438 bytes, 12 entries), plus independent public sources. No outward action was taken. File names below are relative to `claim/` unless marked `repo:`.

## Bottom line

- **The live status page is unchanged.** One GET at 2026-10-19T04:56:43Z returned HTTP 200 and 40715 bytes, with a sha256 identical to `TABLE_RECORD.md` and the same bytes as `data/cobalt.html`. All 199 live rows (N, point group, energy) equal the `point_group` / `E_table_posted` columns of `object/ccd_cobalt_audit.csv` (0 mismatches).
- **No existing p1 claim for this target is in the repo.** Checked: `repo:TROPHY_CASE.md`, `repo:known-knowns/` on main (HEAD = the commit named in `CLAIM.md`), all 176 open pull requests, and a GitHub issue/PR search over all states.
- **No published audit or merged table of the CCD cobalt table was found** in arXiv, Crossref, forward citations of the table's source paper, or web search. The closest prior art is J. Chem. Inf. Model. 63, 6727 (2023), an independent re-search of Co_N, N = 3-200, compared against the CCD. It falls outside the 24-month window and is not a file-level audit or a merged table (details in section 4). The literature absence call is **provisional** because of the search limits in section 5.
- **This is not a tie.** No equivalent audit exists to tie with. p1 makes no lower-energy (record) claim.

## 1. Status page (one honest GET, default User-Agent, no retries)

| field | value |
|---|---|
| URL | https://www-wales.ch.cam.ac.uk/~wales/CCD/CoCCD/cobalt.html |
| time (UTC) | 2026-10-19T04:56:43Z (completed 2026-10-19T04:56:44Z) |
| HTTP / bytes | 200 / 40715 |
| Last-Modified | Mon, 26 Feb 2018 16:57:00 GMT |
| Content-Type | text/html |
| sha256 (live) | `b1033b4142e8db518d0e9ef448c5e9d9e7fe651bc2088a0d54aad671eec030ef` |
| sha256 in `TABLE_RECORD.md` (fetched 2026-10-19T03:57:05Z) | `b1033b4142e8db518d0e9ef448c5e9d9e7fe651bc2088a0d54aad671eec030ef`: **identical** |
| live bytes == `data/cobalt.html` | True |
| User-Agent sent | python-requests/2.34.2 |

Values quoted from the live page (N, point group, E/eV): 163 Cs -635.6974681; 175 Cs -684.4569924; 179 Cs -700.5051534; 183 C2v -717.2330494; 185 C1 -725.0514853; 188 Cs -737.5849134; 189 Cs -741.7933500; 190 D5h -746.1251704; 200 C1 -786.4906393. The page credits Zhan, Chen, Liu and Lai, J. Chem. Phys. 122, 244707 (2005). Its note on improved minima lists sizes "84, 95, 101, 113, 121, 122, 196, 107, 198, 200". However, `data/Co.zip` contains Co197, not Co107. The bank's own pitfalls already record this discrepancy, and the claim's merged table uses N = 197. The local sha256 of all three files in `data/` matches `TABLE_RECORD.md` (3/3). Only the status page was re-fetched; points.tgz and Co.zip were not re-downloaded, per this role.

## 2. Repository checks (github.com/elder-plinius/V3R1T4S, read-only, unauthenticated)

- **main HEAD:** `04fdfba48c6e277fe083b6811f1a5deb3c52b74e` (2026-10-17T16:23:28Z), the commit cited in `CLAIM.md`. The full tree has 5166 entries (not truncated).
- **`repo:bank/targets.json` (287 targets):** the target is present. The p1 text in `CLAIM.md` equals the bank's p1 statement verbatim (string equality True), and so do the success criterion and status_source. status_checked is 2026-10-15. `repo:known-unknowns/packings-physics/ccd-gupta-cobalt-clusters-n200.md` says "open as of 2026-10-15".
- **`repo:TROPHY_CASE.md` (31235 bytes, 100 lines):** 0 matches for cobalt / Gupta / Co / ccd-gupta / Wales / Zhan / Cleri / Rosato, and 0 for ccd / cluster.
- **`repo:known-knowns/`:** 20 target directories with 186 entry directories, none for this target. The only CCD-related directory is `lennard-jones-ccd-doye-table`.
- **Open PRs (176, two API pages):** 4 hits for cobalt/Gupta-related terms, none about cobalt:
  - #374: Murrell-Mottram target, a Gupta audit of 780 Zn/Cd/Pb/Na point files, i.e. different CCD tables.
  - #466: binary Gupta CuAg.
  - #367 and #193: false positives on the author name "Gupta".
- **GitHub issue/PR search, all states:** `cobalt` returns 0 and `"ccd-gupta-cobalt-clusters-n200"` returns 0. The control query `gupta` returns 7 (including #374 and #466), so the search index works.

## 3. Literature, window 2024-10-19 to 2026-10-19

- **arXiv API**, 17 queries (`abs:cobalt AND abs:Gupta`; `abs:cobalt AND abs:cluster AND abs:"global minimum"`; `abs:cobalt AND abs:clusters AND abs:"global minima"`; `abs:"Cambridge Cluster Database"`; `abs:Gupta AND abs:clusters AND abs:"global optimization"`; `abs:"dynamic lattice search"`; `abs:cobalt AND abs:"basin hopping"`; `abs:"cobalt nanoclusters"`; `abs:cobalt`; `all:cobalt AND all:Gupta`; `all:Gupta AND all:clusters AND all:potential`; `abs:Gupta AND abs:potential AND abs:cluster`; `abs:Gupta AND abs:nanoclusters`; `abs:"second moment" AND abs:cobalt`; `abs:cobalt AND abs:clusters AND abs:"global optimization"`; `abs:"putative global minima" AND abs:clusters`; `abs:Co AND abs:clusters AND abs:Gupta`). No relevant paper in the window. In-window hits containing "Gupta" were author names. Sanity checks: `abs:cobalt` gives 1410 results; `all:cobalt AND all:Gupta` gives 15, of which the 2 in-window hits are author-name matches.
- **Crossref** (filter from-pub-date:2024-10-19, top 100 per query, no mailto), 13 queries (`query=cobalt clusters Gupta global minimum`; `query=Gupta potential cobalt clusters`; `query=Cambridge Cluster Database`; `query=dynamic lattice searching clusters Gupta`; `query=global optimization metal clusters Gupta potential`; `query=cobalt nanoclusters structure global optimization`; `query=Co clusters tight-binding second moment approximation structure`; `query.bibliographic=cobalt clusters Gupta`; `query.bibliographic=Co clusters global minimum structures Gupta potential`; `query.bibliographic=cobalt clusters structural optimization`; `query.bibliographic=iterated dynamic lattice search clusters`; `query.bibliographic=Gupta potential clusters global minima`; `query.bibliographic=cobalt nanoclusters Gupta potential lowest energy structures`): 1039 unique DOIs, screened by title/abstract regex and then read by hand. No audit or merged table of the CCD Co table. The nearest in-window items are all off-target:
  - Wu & Zhang, J. Nanopart. Res. 27, 205 (2025), doi 10.1007/s11051-025-06399-8: Co-Pt bimetallic clusters (38, 98 and some 147 atoms) under two Gupta parameter sets.
  - Lai, Hao, Guo, Wen and Fu, Comput. Phys. Commun. 314, 109655 (2025), doi 10.1016/j.cpc.2025.109655: silver clusters.
  - Mubeen, Farooq and Chen, AIP Advances (2026), doi 10.1063/5.0344056: EAM potential, includes Pt6Co7.
  - Tsasse et al., SPIN (2025), doi 10.1142/s2010324725500146: Mo clusters.
  - Wu, He and Lin, Nanoscale (2025), doi 10.1039/d5nr03763h, and Wu, Lin, He and Chen, Nanoscale (2026), doi 10.1039/d6nr01123c: bimetallic clusters.
- **Forward citations of the source paper** (Zhan et al. 2005, doi 10.1063/1.1940028; Crossref title "Asynchronous multicanonical basin hopping method and its application to cobalt nanoclusters", is-referenced-by-count 54). Semantic Scholar returned 50 citing records (2006-2026). None of the 6 records dated 2024-2026 is an audit or merged table. Two papers are relevant:
  - Yang, Yu, Huang, Shao, Liu and Wen, J. Chem. Inf. Model. 63(21), 6727-6739, doi 10.1021/acs.jcim.3c01331, published online 2023-10-19 (pre-window). A SaNSDE global search of Co_N, Pt_N and Fe_N for N = 3-200, benchmarked against the CCD. Per its abstract, lower-energy structures were reported only for Fe_N (13). No Co improvements are reported.
  - Yang et al., Nanoscale 16(37), 17537-17548, doi 10.1039/d4nr02431a (Crossref record created 2024-09-03, just before the window). Co11-Co50 under a DFT-trained deep potential, with improvements over CCD structures reported in that model. This is a different energy model, not the Gupta table.
- **Web search** (substitute for Google Scholar), 5 queries including 'cobalt clusters Gupta global minimum'. Nothing beyond the items above. Older Gupta Co work (e.g. Phys. Rev. B 67, 174413 (2003), Co_N with N <= 60) predates the CCD table.

## 4. Assessment against "strictly beats everything known; a tie is not a record"

For a p1 audit, "beats" means that the deliverable does not already exist. Three findings support that it does not:

- **Repo side: confirmed** by full enumeration. There is no p1 claim, no known-knowns entry, no trophy row, and no open or closed PR or issue mentioning cobalt.
- **Literature side: none found (provisional).** The closest prior art, JCIM 2023, compares independently found minima with the *posted energies*. Per its abstract it does not recompute the posted point files, test them at 1e-5 eV, run a polish test at 1e-4 eV, or merge the Co.zip patch.
- **The claim's specific content appears in no examined source:**
  - 8 posted table files (N = 163, 175, 179, 183, 185, 188, 189, 190) are off their posted energy by more than 1e-5 eV as posted, but reproduce it after polishing.
  - 0 posted structures polish lower by more than 1e-4 eV.
  - All 10 Co.zip files reproduce, and they supply the best value at their 10 sizes (best_source: table 189, Co.zip 10).
  - These counts are read from `object/ccd_cobalt_audit.csv`. Reproducing them is the other panelists' job; I only checked that they agree with the one-sentence statement in `CLAIM.md`.
- **Merged-table caveat (not a novelty failure).** `E_best` is the minimum over the two CCD sources only:
  - Table rows: the polished energy rounded to 1e-7 eV (max deviation from the posted value 1.1e-6 eV, over 24 rows with N = 2-102).
  - Co.zip rows: the recomputed Co.zip energy rounded to 1e-7 eV.
  - Literature values were not merged. Per the JCIM 2023 abstract, none is lower for Co.
- **Note for the bank (does not affect p1).** The target statement says the 2..200 range "rests on a single 2005 search". JCIM 2023 is a second independent search over N = 3-200 for Co, and the full target's comparator (c) should cite it.

## 5. Scope, limits and blocked sources (these make the literature absence provisional)

- **Blocked:** OpenCitations (api.opencitations.net) was refused by the sandbox proxy. Access was not requested, because the task forbids questions to the user.
- **Rate-limited:** the Semantic Scholar batch request for abstracts returned HTTP 429 and was not retried. The Wu & Zhang abstract was seen only via a web-search snippet; the Lai et al. 2025 abstract was not obtained.
- **Not queried:** OpenAlex (no API key configured; asking was not allowed), and Google Scholar directly (web search was used instead).
- **Crossref:** only the top 100 relevance-ranked hits per query were screened, and most records carry no abstract.
- **Full texts:** not read for JCIM 2023, Wu & Zhang 2025 or Lai et al. 2025; abstracts or metadata only.
- **Pre-window literature:** covered only through Zhan 2005 forward citations (50 Semantic Scholar records against a Crossref count of 54) and web search.

## 6. Network log (every HTTP request made; web searches were run server-side and are not listed)

| time (UTC) | request | HTTP | bytes |
|---|---|---|---|
| 2026-10-19T04:56:43Z | GET https://www-wales.ch.cam.ac.uk/~wales/CCD/CoCCD/cobalt.html | 200 | 40715 |
| 2026-10-19T04:58:29Z | GET https://api.github.com/repos/elder-plinius/V3R1T4S | 200 | 5397 |
| 2026-10-19T04:58:30Z | GET https://api.github.com/repos/elder-plinius/V3R1T4S/commits/main | 200 | 4089 |
| 2026-10-19T04:58:44Z | GET https://api.github.com/repos/elder-plinius/V3R1T4S/git/trees/04fdfba48c6e277fe083b6811f1a5deb3c52b74e?recursive=1 | 200 | 1572801 |
| 2026-10-19T04:59:08Z | GET https://raw.githubusercontent.com/elder-plinius/V3R1T4S/04fdfba48c6e277fe083b6811f1a5deb3c52b74e/TROPHY_CASE.md | 200 | 31235 |
| 2026-10-19T04:59:10Z | GET https://raw.githubusercontent.com/elder-plinius/V3R1T4S/04fdfba48c6e277fe083b6811f1a5deb3c52b74e/known-unknowns/packings-physics/ccd-gupta-cobalt-clusters-n200.md | 200 | 6738 |
| 2026-10-19T04:59:11Z | GET https://raw.githubusercontent.com/elder-plinius/V3R1T4S/04fdfba48c6e277fe083b6811f1a5deb3c52b74e/bank/targets.json | 200 | 1747396 |
| 2026-10-19T05:00:06Z | GET https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100&page=1 | 200 | 2146221 |
| 2026-10-19T05:00:09Z | GET https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100&page=2 | 200 | 1558893 |
| 2026-10-19T05:01:01Z | GET https://api.github.com/search/issues?q=repo%3Aelder-plinius/V3R1T4S%20cobalt&per_page=100 | 200 | 79 |
| 2026-10-19T05:01:20Z | GET https://api.github.com/search/issues?q=repo%3Aelder-plinius/V3R1T4S%20%22ccd-gupta-cobalt-clusters-n200%22&per_page=100 | 200 | 79 |
| 2026-10-19T05:01:46Z | GET https://api.github.com/search/issues?q=repo%3Aelder-plinius/V3R1T4S%20gupta&per_page=100 | 200 | 44424 |
| 2026-10-19T05:02:37Z | GET https://export.arxiv.org/api/query?search_query=abs%3Acobalt+AND+abs%3AGupta&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending | 200 | 725 |
| 2026-10-19T05:02:43Z | GET https://export.arxiv.org/api/query?search_query=abs%3Acobalt+AND+abs%3Acluster+AND+abs%3A%22global+minimum%22&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending | 200 | 785 |
| 2026-10-19T05:02:50Z | GET https://export.arxiv.org/api/query?search_query=abs%3Acobalt+AND+abs%3Aclusters+AND+abs%3A%22global+minima%22&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending | 200 | 785 |
| 2026-10-19T05:02:56Z | GET https://export.arxiv.org/api/query?search_query=abs%3A%22Cambridge+Cluster+Database%22&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending | 200 | 8882 |
| 2026-10-19T05:03:01Z | GET https://export.arxiv.org/api/query?search_query=abs%3AGupta+AND+abs%3Aclusters+AND+abs%3A%22global+optimization%22&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending | 200 | 795 |
| 2026-10-19T05:03:07Z | GET https://export.arxiv.org/api/query?search_query=abs%3A%22dynamic+lattice+search%22&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending | 200 | 737 |
| 2026-10-19T05:03:12Z | GET https://export.arxiv.org/api/query?search_query=abs%3Acobalt+AND+abs%3A%22basin+hopping%22&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending | 200 | 4004 |
| 2026-10-19T05:03:18Z | GET https://export.arxiv.org/api/query?search_query=abs%3A%22cobalt+nanoclusters%22&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending | 200 | 731 |
| 2026-10-19T05:03:42Z | GET https://export.arxiv.org/api/query?search_query=abs%3Acobalt&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending | 200 | 254659 |
| 2026-10-19T05:03:56Z | GET https://export.arxiv.org/api/query?search_query=all%3Acobalt+AND+all%3AGupta&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending | 200 | 37610 |
| 2026-10-19T05:04:02Z | GET https://export.arxiv.org/api/query?search_query=all%3AGupta+AND+all%3Aclusters+AND+all%3Apotential&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending | 200 | 227639 |
| 2026-10-19T05:04:42Z | GET https://export.arxiv.org/api/query?search_query=abs%3AGupta+AND+abs%3Apotential+AND+abs%3Acluster&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending | 200 | 23688 |
| 2026-10-19T05:04:48Z | GET https://export.arxiv.org/api/query?search_query=abs%3AGupta+AND+abs%3Ananoclusters&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending | 200 | 2984 |
| 2026-10-19T05:04:53Z | GET https://export.arxiv.org/api/query?search_query=abs%3A%22second+moment%22+AND+abs%3Acobalt&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending | 200 | 749 |
| 2026-10-19T05:04:59Z | GET https://export.arxiv.org/api/query?search_query=abs%3Acobalt+AND+abs%3Aclusters+AND+abs%3A%22global+optimization%22&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending | 200 | 797 |
| 2026-10-19T05:05:04Z | GET https://export.arxiv.org/api/query?search_query=abs%3A%22putative+global+minima%22+AND+abs%3Aclusters&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending | 200 | 7492 |
| 2026-10-19T05:05:09Z | GET https://export.arxiv.org/api/query?search_query=abs%3ACo+AND+abs%3Aclusters+AND+abs%3AGupta&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending | 200 | 753 |
| 2026-10-19T05:05:27Z | GET https://api.crossref.org/works?query=cobalt+clusters+Gupta+global+minimum&filter=from-pub-date%3A2024-10-19&rows=100&select=DOI%2Ctitle%2Cpublished%2Cauthor%2Ccontainer-title%2Cabstract%2Ctype | 200 | 79913 |
| 2026-10-19T05:05:39Z | GET https://api.crossref.org/works?query=Gupta+potential+cobalt+clusters&filter=from-pub-date%3A2024-10-19&rows=100&select=DOI%2Ctitle%2Cpublished%2Cauthor%2Ccontainer-title%2Cabstract%2Ctype | 200 | 116727 |
| 2026-10-19T05:05:45Z | GET https://api.crossref.org/works?query=Cambridge+Cluster+Database&filter=from-pub-date%3A2024-10-19&rows=100&select=DOI%2Ctitle%2Cpublished%2Cauthor%2Ccontainer-title%2Cabstract%2Ctype | 200 | 135492 |
| 2026-10-19T05:05:48Z | GET https://api.crossref.org/works?query=dynamic+lattice+searching+clusters+Gupta&filter=from-pub-date%3A2024-10-19&rows=100&select=DOI%2Ctitle%2Cpublished%2Cauthor%2Ccontainer-title%2Cabstract%2Ctype | 200 | 120944 |
| 2026-10-19T05:05:52Z | GET https://api.crossref.org/works?query=global+optimization+metal+clusters+Gupta+potential&filter=from-pub-date%3A2024-10-19&rows=100&select=DOI%2Ctitle%2Cpublished%2Cauthor%2Ccontainer-title%2Cabstract%2Ctype | 200 | 76981 |
| 2026-10-19T05:06:00Z | GET https://api.crossref.org/works?query=cobalt+nanoclusters+structure+global+optimization&filter=from-pub-date%3A2024-10-19&rows=100&select=DOI%2Ctitle%2Cpublished%2Cauthor%2Ccontainer-title%2Cabstract%2Ctype | 200 | 121324 |
| 2026-10-19T05:06:07Z | GET https://api.crossref.org/works?query=Co+clusters+tight-binding+second+moment+approximation+structure&filter=from-pub-date%3A2024-10-19&rows=100&select=DOI%2Ctitle%2Cpublished%2Cauthor%2Ccontainer-title%2Cabstract%2Ctype | 200 | 103546 |
| 2026-10-19T05:07:24Z | GET https://api.crossref.org/works?query.bibliographic=cobalt+clusters+Gupta&filter=from-pub-date%3A2024-10-19&rows=100&select=DOI%2Ctitle%2Cpublished%2Cauthor%2Ccontainer-title%2Cabstract%2Ctype | 200 | 176497 |
| 2026-10-19T05:07:28Z | GET https://api.crossref.org/works?query.bibliographic=Co+clusters+global+minimum+structures+Gupta+potential&filter=from-pub-date%3A2024-10-19&rows=100&select=DOI%2Ctitle%2Cpublished%2Cauthor%2Ccontainer-title%2Cabstract%2Ctype | 200 | 126105 |
| 2026-10-19T05:07:32Z | GET https://api.crossref.org/works?query.bibliographic=cobalt+clusters+structural+optimization&filter=from-pub-date%3A2024-10-19&rows=100&select=DOI%2Ctitle%2Cpublished%2Cauthor%2Ccontainer-title%2Cabstract%2Ctype | 200 | 93371 |
| 2026-10-19T05:07:36Z | GET https://api.crossref.org/works?query.bibliographic=iterated+dynamic+lattice+search+clusters&filter=from-pub-date%3A2024-10-19&rows=100&select=DOI%2Ctitle%2Cpublished%2Cauthor%2Ccontainer-title%2Cabstract%2Ctype | 200 | 105785 |
| 2026-10-19T05:07:44Z | GET https://api.crossref.org/works?query.bibliographic=Gupta+potential+clusters+global+minima&filter=from-pub-date%3A2024-10-19&rows=100&select=DOI%2Ctitle%2Cpublished%2Cauthor%2Ccontainer-title%2Cabstract%2Ctype | 200 | 109133 |
| 2026-10-19T05:07:52Z | GET https://api.crossref.org/works?query.bibliographic=cobalt+nanoclusters+Gupta+potential+lowest+energy+structures&filter=from-pub-date%3A2024-10-19&rows=100&select=DOI%2Ctitle%2Cpublished%2Cauthor%2Ccontainer-title%2Cabstract%2Ctype | 200 | 155517 |
| 2026-10-19T05:08:50Z | GET https://api.crossref.org/works/10.1063/1.1940028 | 200 | 11618 |
| 2026-10-19T05:08:55Z | POST https://api.semanticscholar.org/graph/v1/paper/batch?fields=title,abstract,year,externalIds | 429 | 174 |
| 2026-10-19T05:08:59Z | GET https://api.semanticscholar.org/graph/v1/paper/DOI:10.1063/1.1940028/citations?fields=title,year,externalIds,abstract&limit=1000 | 200 | 84407 |
| 2026-10-19T05:09:03Z | GET https://api.opencitations.net/index/v2/citations/doi:10.1063/1.1940028 | blocked: ProxyError: HTTPSConnectionPool(host='api.opencitations.net' |  |
| 2026-10-19T05:09:51Z | GET https://api.crossref.org/works/10.1039/d4nr02431a | 200 | 16948 |
| 2026-10-19T05:11:53Z | GET https://api.crossref.org/works/10.1021/acs.jcim.3c01331 | 200 | 10387 |

pass: true