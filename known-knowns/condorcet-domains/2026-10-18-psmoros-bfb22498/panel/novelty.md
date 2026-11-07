Saved by the main session from the subagent's returned text (NOVELTY skeptic, Agent tool, fresh context, model opus; returned about 07:12Z 2026-10-18). The text below is verbatim.

# NOVELTY skeptic: condorcet-domains, eleven rows (n = 14..20, 22..25)

context: subagent (Agent tool, fresh context, model opus; saw only a copy of claim/ plus TROPHY_CASE.md and the web)

Judged 2026-10-18 from 06:57Z to 07:12Z UTC. Disclosures:
- I read the source of the run's fetch helper (vfetch.py) once, to learn how to call it.
- I read the workspace stop lists, as instructed.
- The harness loaded the repository's CLAUDE.md pointer when I opened TROPHY_CASE.md.
- I read no other file outside claim/.
- I made no request to arxiv.org, export.arxiv.org or any arXiv mirror (ar5iv, arxiv.com). When search results linked to arXiv, a mirror or a stopped host, I did not open the link.
- This session's stop list was empty before my work and was still empty at 07:11:50Z. None of my requests was blocked.

## 1. Status source and how it was read

**Status source:** Table 4 ("Maximum size of Condorcet domains") of arXiv:2601.07336v1 (Karpov, Markström, Riis, Zhou). URLs: https://arxiv.org/html/2601.07336 and the abstract page https://arxiv.org/abs/2601.07336.

**Why I could not fetch it myself.** arxiv.org is on this workspace's stop list: HTTP 429 at 2026-10-17T22:56:05Z, on a different URL (the cs.GT /list page). Kit rule 5 forbids any further request from any process, so the honest single GET of RUN.md step 6 cannot be made in this panel.

**What exists instead. I checked each item myself:**
- **The saved HTML page.** status/arxiv_html_2601.07336.html is the session-2220 scout's own GET of https://arxiv.org/html/2601.07336: HTTP 200 at 2026-10-17T22:25:36Z.
  - I recomputed its sha256: 13e2470223a195ce47f4d8da36c05c6352ef1aecf062c21a75cf85b234c7bd1b. It matches CLAIM.md.
  - The page identifies itself as 2601.07336v1 (4 occurrences, no other version).
  - I re-read Table 4 in the raw HTML and in status/arxiv_html_2601.07336.extracted.txt (sha256 2a0e811a…14e7, matches). Every value for n = 14..25 matches status/records_table4.tsv (sha256 7ca09d5a…c0c6, matches).
- **The saved abstract page.** status/arxiv_abs_2601.07336.html: HTTP 200 at 2026-10-17T22:25:20Z, sha256 b763f9927bb848258da8d47876a5dc37752f7afabf47cfa55a3696d3082183fa (matches). Its submission history shows only "[v1] Mon, 12 Jan 2026 09:03:12 UTC (26 KB)".
- **The human's hand check.** status/human_status_check.md, sha256 26223b9f…3ef3 (matches). The human opened https://arxiv.org/abs/2601.07336 in a browser at 2026-10-18T00:58Z and saw only v1, no later version. This is the remedy the kit prescribes when the source is blocked ("the human checks by hand").
- **Freshness bound (supporting).** arXiv's help page "Availability of submissions" says announcements run Sunday to Thursday at 20:00 ET, none on Friday or Saturday, and replacements are announced the same way. I read this through a web search summary, not a fetch: info.arxiv.org belongs to the stopped arXiv service.
  - The last announcement before the scout's fetch was Thu 2026-10-15 20:00 EDT (2026-10-16T00:00Z).
  - The next is Sun 2026-10-18 20:00 EDT (2026-10-19T00:00Z).
  - The scout's reads (22:25Z), the human's check (00:58Z) and this judgment (07:12Z) all fall in that one gap between announcements. So no later version can have become public since the version list was read.
- **Content cannot drift.** An arXiv version's text cannot change once posted, so Table 4 of v1 is fixed.

**Decision: the status source has been read honestly, and its current status is confirmed. I do not write PENDING STATUS CHECK.** Reasons:
1. The source is a fixed document version, not a live table.
2. Its exact bytes come from one honest HTTP 200 GET, made before the block. The block was on a different URL and came 30 minutes later.
3. The human checked independently that no later version exists, which is what the kit asks for when the source is blocked.
4. arXiv's schedule means that version state still holds now.

The gate or the human may take the stricter view that NOVELTY must fetch the page itself. In that case this lens's outcome becomes `novelty: PENDING STATUS CHECK`, and nothing below changes.

**Values read (Table 4, column "f(n) & h(n)", every entry printed with "≥"):**

| n | Table 4 |
|---|---|
| 14 | 27026 |
| 15 | 59430 |
| 16 | 131536 |
| 17 | 292015 |
| 18 | 649079 |
| 19 | 1432836 |
| 20 | 3155366 |
| 22 | 15037178 (ks) |
| 23 | 33162136 (ks) |
| 24 | 73279872 (ks) |
| 25 | 160316046 (ks) |

The fetch time is 2026-10-17T22:25:36Z, and the version state was confirmed by hand at 2026-10-18T00:58Z.

**Other numbers in the saved paper:**
- I listed every number of 5 or more digits in the paper. None for n = 14..25 is a domain size above Table 4. The Fishburn column, the old Karpov-Slinko values and Table 1 are all at or below Table 4.
- The column "⌈4/5^1.5 · √5^n⌉" is a formula: it equals 4·5^((n-3)/2) and matches the exact maxima for n = 5..8. It is not a construction or a lower bound; for n = 9 it gives 500, while the best known value is 492.
- I combined Table 4's own values with the paper's product constructions: Fishburn replacement f(n+m-1) ≥ f(n)f(m), and Proposition 1, e(n+m) ≥ 2e(n)e(m). For every claimed n the best implied value stays below Table 4, so Table 4 is internally the best known.

## 2. Searches (UTC time, status, what each showed)

All URL requests went through the run's helper: one plain GET each, honest User-Agent, no retries.

**V3R1T4S pull requests, issues and repository (api.github.com, unauthenticated):**
- 06:59:16Z, search/issues?q=repo:elder-plinius/V3R1T4S+type:pr+condorcet: 200, total_count 0.
- 06:59:24Z, …repo:elder-plinius/V3R1T4S+condorcet (issues and PRs): 200, 0.
- 06:59:31Z, …+type:pr+"never condition": 200, 0.
- 06:59:39Z, …+2601.07336: 200, 0.
- 06:59:46Z, …+type:pr+Karpov: 200, 0.
- 06:59:54Z, …+type:pr+"linear orders": 200, 0.
- 07:00:01Z, …+type:pr+"majority"+domain: 200, 0.
- 07:00:17Z, control query …repo:elder-plinius/V3R1T4S+type:pr: 200, total_count 365. The search works; the newest PR is #375 (2026-10-18T05:19:58Z).
- 07:00:28Z-07:00:31Z, repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100, pages 1-4: 200 each.
  - The list holds all 365 PRs (#1-#375), 68 of them open.
  - I searched every title and body for condorcet, never condition, social choice, linear order, majority, Karpov, Markström, Riis, 2601.07336, peak-pit and Fishburn. The only 3 hits are #187-#189, sunflower-free claims that cite Markström's Turán tables; they are unrelated.
  - None of the eleven claimed values appears in any PR title or body. Neither does the separate n = 21 value 7467760, nor its n = 20 restriction 3311844.
- 07:00:47Z, repos/elder-plinius/V3R1T4S: 200. The repository is public; default branch main, last push 2026-10-17T16:23:29Z.
- 07:00:48Z, contents/TROPHY_CASE.md (public, current main): 200, blob 571f2411…, 31235 bytes, 100 lines. It has 0 matches for condorcet, never condition, Karpov, social choice or linear order.
  - The pinned local copy of TROPHY_CASE.md (100 lines) also has 0 matches. It lists six families and no Condorcet domain.
- 07:00:55Z, git/trees/main?recursive=1: 200, 5166 entries, not truncated. No path matches condorcet, social, karpov or voting.

**Wider GitHub:**
- 07:01:56Z, search/repositories?q=condorcet+domain: 200, 3 repositories.
  - DolicaAkelloEgwel/Condorcet-Domains (2020) and sagebei/Local_Diversity_of_Condorcet_Domains (2024).
  - Project-AGREE/Outer-Diversity-Condorcet (2026-09-25): code for the outer-diversity paper, which works on small n.
- 07:01:57Z, search/repositories?q=condorcet+domains+in:name,description,readme: 200, 345 results. The only further relevant one is sagebei/cdl.
- 07:02:15Z, users/sagebei/repos (Bei Zhou): 200, 12 repositories, none holding record data.
- 07:02:25Z, sagebei/cdl commits since 2025-10-01: 200, 4 commits (2026-02-23 README, 2026-03-11 orderly algorithm, 2026-06-09 logo and update).
  - 07:02:26Z, its file tree: 200, 143 entries, no record-domain data.
- 07:05:47Z, search/issues?q=condorcet+domain+in:title,body (all of GitHub): 200, 80 items.
  - The only Condorcet-domain item is The-Last-Math-Competition #321 (2026-10-03). It disproves a bound with the 4-order domain on 3 alternatives; it is not a size record.
  - 07:05:59Z, the same repository searched for condorcet: 200, 1 item (#321).
- 07:09:37Z, search/issues?q=condorcet+user:teorth: 200, 0.
- 07:09:38Z, search/repositories for condorcet + domain pushed after 2026-01-01: 200, 279 results. The only Condorcet-domain repository is Project-AGREE/Outer-Diversity-Condorcet.

**Authors' pages and other sources:**
- 07:02:57Z, https://www.ipu.ru/node/80126: 200. It is the record of Karpov, Markström, Riis and Zhou, Discrete Applied Mathematics 370 (2025), "Coherent domains…". That paper gives an asymptotic bound of 2.1973^n and is reference [15] of the status source.
- 07:03:44Z, https://link.springer.com/book/10.1007/978-3-032-15115-5: 404. My DOI guess was wrong; this is not a block.
- 07:04:07Z, https://micro.econ.kit.edu/english/2902.php: 200. It serves a PDF (sha256 53352340…), the draft dated 14 Nov 2025 of Puppe and Slinko's book "Condorcet Domains" (Springer, April 2026).
  - Its Table 8.2 gives n = 14..20 as 24481, 54752, 123004, 271758, 602299, 1323862 and 2917604 (Karpov-Slinko values), all below Table 4. Its newest bound is 2.1973^n.
  - 07:05:02Z, https://micro.econ.kit.edu/downloads/CondorcetDomains_Buch_Puppe_Slinko.pdf: 200, the identical file.
- 07:05:27Z, https://zenodo.org/api/records?q="condorcet domain"…: NOT requested, because the helper found that zenodo.org's robots.txt disallows it for our User-Agent. This is not a block, so no stop-list line.
- 07:06:21Z, http://abel.math.umu.se/~klasm/Uppsatser/index.html (Markström's papers): 200. The newest Condorcet item is "An orderly algorithm…" (2509.20865); nothing later.
- 07:06:24Z, https://researchpublications.its.qmul.ac.uk/publications/staff/20178.html (Riis's publications): 200. The newest Condorcet item is 2601.07336 itself (2026).
- 07:06:48Z, http://abel.math.umu.se/~klasm/: 200. 07:06:55Z, …/Data/index.html: 200. 07:07:06Z, …/Data/CONDORCET/: 200. The data page holds domains for n ≤ 8 only.

**Web searches.** These used the search tool, which reports no HTTP status. They ran between about 07:01Z and 07:10Z, in this order:
- "largest Condorcet domain new lower bound 2026"
- "Condorcet domains" maximum size 21 22 23 24 25 alternatives construction improved
- Condorcet domain AlphaEvolve / FunSearch / evolutionary record 2026
- "3155366" Condorcet
- "160316046" OR "6674931" OR "15037178" Condorcet domain
- Puppe-Slinko book ISBN 9783032151155, and its table of contents
- Condorcet domains 2026 arXiv peak-pit maximal size new
- Bei Zhou thesis Condorcet domains Queen Mary
- Markström Condorcet data download
- "Improved lower bounds for the maximum size of Condorcet domains" cited
- asymptotic bound beyond 2.198139
- Karpov Slinko 2026 new construction
- extended search: largest known size table n=20 2026, Zhou / Riis / Markström
- our values: "3336208" OR "178950728" OR "81912986" OR "36894088" OR "16571072"
- our values: "300388" OR "135072" OR "675512" OR "1497276"
- OEIS maximal Condorcet domain sequence
- LLM or machine-learning search for large Condorcet domains, 2026
- extended search: Condorcet domains arXiv 2026 by these authors
- "Coxeter Condorcet domains" 2606.01690
- Condorcet domain PhD thesis 2025/2026
- zenodo / github Condorcet domain dataset
- the same restricted to zenodo.org, then to github / researchgate / openreview / huggingface
- extended search: journal version of 2601.07336 in 2026
- "2601.07336"
- never conditions with n=20 / 25 alternatives
- arXiv announcement schedule
- A144685 OEIS

What they showed:
- No source after January 2026 gives any Condorcet domain size for n = 14..25.
- arXiv:2601.07336 has no journal version and nothing citing it with new values.
- The 2026 Condorcet-domain items found are structural, small-n or a survey: arXiv:2606.01690 (Coxeter Condorcet domains), arXiv:2610.00720 (outer diversity), arXiv:2509.20865 (orderly generation), arXiv:2505.19520, arXiv:2509.19614, and the Puppe-Slinko book.
- OEIS A144685 and A144686 hold the Fishburn alternating-scheme sizes, not records.
- No public page shows any of the eleven claimed values.

**Limits of the literature check.** I could not query:
- arXiv listings, oeis.org, Semantic Scholar, OpenAlex, Crossref, dblp, IA Scholar, spiral.imperial.ac.uk or qmro.qmul.ac.uk: all on the workspace stop lists.
- the Zenodo API: refused by its robots.txt.

So the 24-month check rests on web-search indexing (which surfaced arXiv Condorcet papers up to 2026-09-30), the authors' own pages and repositories, and GitHub.

**injection_suspected:** none. The only "Instructions" text in the saved arXiv pages is arXiv's standard footer, "Instructions for reporting errors". The human's note is data.

## 3. My own size cross-check (type L; data only, not my lens's threshold)

I decompressed every type-L list (parts joined in name order). Line counts, joined-xz sha256 and text sha256 all equal CLAIM.md:

| n | lines |
|---|---|
| 14 | 27040 |
| 15 | 60956 |
| 16 | 135072 |
| 17 | 300388 |
| 18 | 675512 |
| 19 | 1497276 |
| 20 | 3336208 |
| 22 | 16571072 |

For n = 20 and n = 22, `sort -u` gives the same count, so no line is duplicated.

The type-A assignment sha256 values (n = 23, 24, 25) match CLAIM.md. I did not recount |D(A)| for n = 23..25: that is the other skeptics' job, and the sizes below are the claim's own exact counts.

## 4. Per-row verdict

Each size is strictly larger than Table 4 for its n. I found no later paper, preprint, thesis, repository, data page, record list, book, TROPHY_CASE.md entry or V3R1T4S PR, open or closed, that shows an equal or larger value. No tie occurs.
- Rows 14, 15, 18 and 19 are restrictions of this folder's own unsubmitted rows 15, 16, 19 and 20. These are our own objects, not rivals.
- The workspace's separate n = 21 object (7467760) is not public. Its n = 20 restriction (3311844) is below row 20 anyway.

row n=14: PASS (27040 > 27026; +14, +0.0518 %)
row n=15: PASS (60956 > 59430; +2.5677 %)
row n=16: PASS (135072 > 131536; +2.6882 %)
row n=17: PASS (300388 > 292015; +2.8673 %)
row n=18: PASS (675512 > 649079; +4.0724 %)
row n=19: PASS (1497276 > 1432836; +4.4974 %)
row n=20: PASS (3336208 > 3155366; +5.7313 %)
row n=22: PASS (16571072 > 15037178; +10.2007 %)
row n=23: PASS (36894088 > 33162136; +11.2537 %)
row n=24: PASS (81912986 > 73279872; +11.7810 %)
row n=25: PASS (178950728 > 160316046; +11.6237 %)

pass: true
