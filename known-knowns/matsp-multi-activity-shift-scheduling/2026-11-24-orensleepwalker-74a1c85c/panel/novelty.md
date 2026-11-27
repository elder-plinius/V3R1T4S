# Novelty verdict
context: fresh subagent started for this claim only

Scope: claim/ (CLAIM.md, rows.csv, data/, provenance/, object/ for the roster comparison) for 123 rows. Every claimed penalty is strictly below the TRA26 best known value. Smallest margins: #38, #93, #173 and #219 by 2 points, #81 by 4, #6 and #188 by 8, #82 by 9. My work files are in panel/work-novelty/ (fetches in fetch/, downloads in dl/, my own scripts in scripts/, outputs similarity.csv and repo_files.sha256). I ran no downloaded program.

## Sources checked

All times are UTC on 2026-11-24. There was one plain request per page with User-Agent "V3R1T4S-novelty-check/1.0", and nothing was retried.

| # | Source | Time | HTTP | sha256 / note |
|---|---|---|---|---|
| 1 | https://www.schedulingbenchmarks.org/matsp/ | 14:00:41Z | 200 | f14664f5e33d0a99e1bf19d97f6e7eedfad344fbd45b744dbfdb1bbbb17ee984. Byte-identical to claim/data/matsp.html. |
| 2 | https://www.schedulingbenchmarks.org/changes.html | 14:00:42Z | 200 | 6eb567e75bfe9a5615fc79a58a6210c980764d2fb1d2a900706bbaff41cfef3b. Byte-identical to claim/data/changes.html. |
| 3 | https://www.schedulingbenchmarks.org/matsp/index.php | 14:10:56Z | 200 | f14664f5... Same bytes as #1. |
| 4 | https://www.schedulingbenchmarks.org/matsp/instances1_225.html | 14:01:13Z | 200 | 3dea83c42cd64edfd8949ff1003908edc69e4069cfb9e42e4f500869535ca81d. Format guide only. |
| 5 | https://www.schedulingbenchmarks.org/matsp/verify.html | 14:01:14Z | 200 | 027ae9f7dac966546294a1781daa918edf1df18c040afa541737093beb2c76e2. Links only to the verifier, RosterViewer and the 889 example. |
| 6 | https://www.schedulingbenchmarks.org/index.html | 14:10:57Z | 200 | 321f9ba620c2209669881e036b0a3fdd07142362eedbccb74646c547c86ff8dc. No news. |
| 7 | https://www.schedulingbenchmarks.org/papers/VNS_for_MASSP.pdf (QU20) | 14:01:30Z | 200 | 95b9e3d70aff616d6728a4f02c857ba2ea4c9a6218d47d8a8c7b7c35056a63e0 |
| 8 | https://doi.org/10.1007/s10951-026-00886-z, which resolves to the link.springer.com article (TRA26, open access, CC BY 4.0, online 2026-08-27) | 14:02:07Z | 200 | 37bbffe30cc21cf713ca4ff1371b18360f51b16af630ed11e0666187be558406 |
| 9 | TRA26 Tables 5, 7, 8 (…/tables/5, /7, /8) | 14:02:32-34Z | 200 each | 280a65d1…, b6cc5d58…, 096c2f86… (html). Parsed CSVs: 4add6eb5…, 4b77b54f…, 417add45… |
| 10 | https://github.com/trautschlaci/massp_sa (code and solutions named in TRA26) | 14:03:09Z | gh API | 3 commits (2025-01-13, 2025-01-13, 2025-09-10). No forks, releases, issues or other branches. best_solutions/ has 225 files at both content commits. The 123 files for claimed instances were downloaded at commit 1bb70a3bca (hashes in work-novelty/repo_files.sha256, list hash 3af741f2…). |
| 11 | https://patatconference.org/patat2024/proceedings/papers/125.pdf (Trautsch and Kovari, PATAT 2024, earlier SA version) | 14:05:36Z | 200 | 2a8265fb824336e34b745fef637db2d047b09a9b0f438dde0fc8c7a461dee50c |
| 12 | OpenAlex: TRA26 record, works citing QU20, searches | 14:07:28-14:11:27Z | 200 | TRA26 has 0 citing works. The 5 works citing QU20 were each screened (see below). |
| 13 | https://publications.polymtl.ca/76810/1/2026_FarinRastgarAmini.pdf (2026 PhD thesis citing QU20) | 14:07:58Z | 200 | Bot challenge (Incapsula HTML, 212 bytes). Stopped, not retried. |
| 14 | export.arxiv.org API query | 14:08:22Z | 429 | Stopped, not retried. Replaced by web searches restricted to arxiv.org. |
| 15 | https://pub.uni-bielefeld.de/record/2981218 (Römer, block-based MASSP) | ~14:11Z | denied (Anubis) | Stopped. Abstract read via OpenAlex instead. |
| 16 | https://arxiv.org/abs/2608.30419 | ~14:09Z | 200 | Healthcare CP-SAT on INRC-II instances. Not this benchmark. |
| 17 | GitHub repository and code search (gh) | 14:06Z | API | Terms searched: multi-activity shift scheduling, massp, matsp, schedulingbenchmarks, schedulingbenchmarks.org/matsp |
| 18 | elder-plinius/V3R1T4S PRs and issues (gh) | 14:08:54-14:10:44Z | API | All 1177 PRs listed by title, plus search over PRs and issues |
| 19 | Web searches (standard and extended) | 14:04-14:11Z | | Searched for: Curtois-Qu benchmark new best; schedulingbenchmarks matsp 2026; Trautsch Kovari preprint or thesis; multi-activity multi-day 2025/2026; arxiv.org-restricted; PATAT 2026 |

## Findings per source

1. **Live table and changes page.** Both are byte-identical to the frozen copies taken at 13:34:54Z. All 225 rows still credit TRA26. For all 123 claimed rows the live best known equals rows.csv `record`, and every claimed penalty is below it (my parse: 0 mismatches). The newest changes entry about multi-activity instances is 07-Oct-2026 (the verifier). Later entries (15, 21, 27 and 29 Oct) concern nurse rostering only. The site publishes no per-instance MATSP solution files. The only MATSP solution it hosts is the 2019 example 8_7_20_2.Solution.889.xml (instance 8, not claimed). The commented-out links "computational_results…pdf" and "misc/instances1_24solutions.zip" are nurse-rostering leftovers in an HTML comment. The table credits only one other source, QU20, and only in the references list; no current row cites it.
2. **QU20 (Qu and Curtois, ICORES 2020, VNS).** I parsed Table 1 for all 225 instances, taking the min of the 5-minute and 10-minute values. 0 claimed rows have a QU20 value at or below ours. Example: #38 is 3894 in QU20, against 3270 ours.
3. **TRA26 article.** The abstract says new best solutions on all 225 instances. I parsed Table 5 for the tuning-subset instances: VNS, SA short/medium/long minimum, CP UB/LB and IP UB/LB. I parsed Tables 7 and 8 for the long-run SA minimum on all other instances. For every claimed instance, the article's lowest value equals the site's best known. 0 rows have any article value (any run length, CP or IP) at or below ours. On the site, only two instances fall below the article's minimum, and neither is claimed: #1 (site 383 vs article 385; the 383 comes from PATAT 2024) and #5 (site 0 vs article 1; the 0 comes from the repo). For claimed instances in Table 5, no published lower bound (CP or IP) exceeds our penalty, so there is no contradiction. The tight rows match the article exactly: #38 3272, #93 2988, #173 7399, #219 18990, #81 1510, #188 13799.
4. **TRA26 repository (trautschlaci/massp_sa).** The value in each best_solutions filename equals the site's best known for all 123 claimed instances at both commits (2c8cbd6149 and 1bb70a3bca, identical file lists). 0 are at or below ours. The repo was last pushed 2025-09-10, before the paper's publication, and has no later or better runs.
5. **PATAT 2024 (earlier version by the same authors).** Table 4 parsed for all 225 instances (VNS and SA columns). 0 values at or below ours. Example: #173 is 7765, against 7397 ours.
6. **Other work found.** None of it publishes penalties on these instances under the benchmark objective:
   - Shariat and Huang (J. Heuristics 2024, and the McMaster MSc thesis 2022; GitHub repo Ranash1375/LNS-…) use industrial and random instances.
   - Römer (J. Sched. 2024) works on the single-day anonymous MASSP.
   - Dahmen and Rekik (hybrid heuristic) uses a heterogeneous-workforce instance set.
   - Rastgar-Amini (Polytechnique Montréal thesis 2026 and the related J. Sched. 2025 / TELO papers) uses shift enumeration for retail MILP. The PDF was blocked (see limits).
   - MatiasGutierrez1/Simulated-Annealing-for-MSSP (2023) has no per-instance result files on these instances.
   - PetterS/monolith (Strandmark, 2020) has the instance files, a column-generation and local-search solver and run_all.py. It publishes no result table. Its only solution files are test_solution_1a and test_solution_10a, for instances 1 and 10, which are not claimed.
   - git791/Ordivanta (2026-10/11) runs a simplified model on 5 MATSP instances. It reports coverage, hours and fairness, not benchmark penalties, so its "OPTIMAL" labels do not compare to ours.
   - OpenAlex lists no works citing TRA26.
   - No arXiv preprint of TRA26 and no other 2024-2026 paper with per-instance results on this benchmark was found.
7. **V3R1T4S.** Only three PRs concern this target: #1215 (instance 80, head 72b9cb40), #1216 (instance 155, head ac089c23) and #1217 (94 optimality certificates, head 8151a57b). All three are open drafts by the same account. No issue mentions the target. Instances 80 and 155 are not among the claimed rows. I fetched #1217's object/certificates.csv (94 instances, sha256 293c822d…). Its instances do not overlap the 123 claimed rows, so no claimed row goes below a value the team itself certified optimal. The bank target file was last changed 2026-10-28. No known-knowns entry for MATSP exists on main.
8. **Near-copy check (task 5).** The only published rosters for the claimed instances are the 123 TRA26 repo files. Both formats count days from 0. Overlap of ours against theirs:
   - Identical shifts (same day, start and task sequence, as a multiset, ignoring employee IDs): median 5.3%, max 34.7% (#156). The single-task rows #156, #157, #82, #86 and #6 are the highest, where the shift choices are few.
   - Matching on day, start and total length only: median 14.6%, max 34.7%.
   - Whole-employee schedules identical: 0 of all employees in all 123 rows.
   - Same-ID employee identical: 0.
   - Tight rows: #38 5.7%, #93 8.1%, #173 0.5%, #219 0.0%, #81 26.6%, #188 1.7%.

   None of our rosters is a near copy or a small edit of a published roster (details in work-novelty/similarity.csv).

## Failing rows

None. No source I could read publishes a value at or below our penalty for any of the 123 claimed instances.

## Residual limits

- The Polytechnique Montréal 2026 thesis PDF (bot challenge) and the Bielefeld record page (access denied) could not be read. From their abstracts and the authors' related papers, neither appears to report penalties on the Curtois-Qu instances, but this was not checked in the full text.
- The arXiv API returned 429. Coverage of arXiv rests on web searches, which found no relevant preprint.
- I did not read Google Scholar or ResearchGate directly, and I did not use the Wayback Machine. Earlier table versions credited QU20 values, which are all higher than ours.
- Unpublished results cannot be ruled out, such as solutions emailed to the site but not yet posted, or later runs by the TRA26 authors not pushed to GitHub. The site was unchanged at 14:00:41Z.
- The near-copy check compares only against the TRA26 repo rosters. No other published rosters exist for these instances as far as I found.
- I did not re-verify the penalties or feasibility of our rosters; that is the other skeptics' task.

pass: true
