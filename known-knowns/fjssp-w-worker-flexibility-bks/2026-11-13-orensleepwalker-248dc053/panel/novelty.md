# Novelty review: FJSSP-W claim, version 2 (65 rows)

context: I am the novelty reviewer on a three-person panel. A parent agent started me with a brief file, and I had no earlier context. I read only files inside the claim folder, plus the public web and GitHub (read-only). I wrote only to panel-v2/work-novelty/ and this file. Partway through the review, the agent harness automatically inserted the workspace's CLAUDE.md and AGENTS.md (the authors' project notes) into my context. I did not open them and did not use them as evidence. Everything below comes from public sources and the claim folder. The one thing those notes mention that matters here is the version-1 result, and CLAIM.md's version note already states it.

Verdict: all 65 rows hold. I found no public value at or below our makespan for any row, and no published schedule that reaches our makespan under trivial edits.

## 1. Status source (fetched once, no retries)
- URL: https://raw.githubusercontent.com/jrc-rodec/FJSSP-W-Benchmarking/main/instances/InstanceData/FJSSP-W/best_known.csv
- Fetched at 2026-11-13T01:35:50Z. HTTP 200, 11252 bytes, sha256 74f982d5fdbdd7ebf6b889b0a57106474f9dd677a3813cf5762fc54afdfe30cf.
- The fetched file is byte-identical to references/best_known.csv. Its sha256 matches the one in status/table-fetch.txt (fetched 2026-11-13T01:12:05Z). The table has not changed.
- Every claimed row has an integer-valued UB with no float noise, and UB >= LB. The UB of every claimed row is listed in the table in section 6 ("UB live").
- The benchmark repository's main HEAD is the pinned commit eb1d28381c34525b58736965cddbeb89e095f88a (2026-05-04). best_known.csv was last changed 2026-04-27 (fb2d06a).

## 2. Instance identity
I downloaded all 65 instance files from the pinned-commit URLs in references/benchmark-commit.txt. For 65 of 65, the sha256 matches references/instances.sha256 and also matches the copy under references/instances/. The table's 402 row names and data.csv's 402 sources match one-to-one by name (lower-casing; Behnke->behnkegeiger, BrandimarteMk->brandimarte). The file order differs, so the mapping is by name.

I also wrote my own checker (work-novelty/check.py). All 65 objects are valid, and each makespan is at most round(UB) - 1 against the live table. This repeats the reproduce check. I needed it here to validate other people's schedules.

## 3. Sources searched and what they hold for these 65 rows
| Source | What was checked | Result for our rows |
|---|---|---|
| jrc-rodec/FJSSP-W-Benchmarking | All 8 historical versions of best_known.csv (035912b, 9462fca, 22e1c02, decf461, c5d3007, e8574fb, c894f27, fb2d06a), with names normalised and UB taken as the max of the two columns because of the old header swap; full tree (no solution files); releases (none); PRs (none); issue #1 (leonlan: Behnke1 at 86/87, answered by the organisers on 2026-04-27, which led to the table fix) | No historical UB at or below ours. The closest margin is +1 (behnkegeiger10, 23, 41, 45). |
| jrc-rodec/FJSSP-W-Competition | All 15 issue threads and every attachment (15 archives; 2 release links in issue #13 return 404 and the MarkRogoQC/FJSS repo is deleted, but issue #13's own table gives values 3-7x the UB); PR #16 (GECCO 2026 results poster, "three of the prior best known results could be improved") | The 30 competition instances overlap our rows on 4 instances, matched by sha256 of content: Hurinksdata40, Hurinkrdata50, Hurinkvdata5, Fattahi20. Lowest values: sdata40 1301 (valid), rdata50 5681 reported (issue #14, schedule invalid; best valid 5697), vdata5 503 (valid), Fattahi20 1127 reported (issue #14, invalid; best valid 1153). All are above ours (1285 / 5651 / 501 / 1123). Issues #1/#2 (Haoxiang Qin) contain runs on all 402 instances (10 runs x 2 scenarios). For our 65 rows, all 1,300 schedules pass my checker, and none is at or below ours. The closest is behnkegeiger51 at 232 vs our 231. |
| jrc-rodec/FJSSPW-GA | results/condensed_ga_results.json (402 instances); results/solver_result/results_{cplex_cp,cplex_lp,hexaly,ortools}.txt; instance files compared by sha256 (65/65 identical) | Nothing at or below ours. The closest is cplex_cp, which equals the UB (+1). |
| jrc-rodec/scheduling_model (organisers' model repo, pushed 2026-07-09) | 82 result/analysis files (notebooks, txt, csv, xlsx); its benchmarks_with_workers instances are sha256-identical to ours where checked | No FJSSP-W value at or below ours. The notebook flags I checked turned out to be: (a) best_known_comparison.ipynb's "Literature" column, which equals the FJSP (no-worker) best_known table row for row (402/402) and is also mis-keyed (the code reads values in file order but assigns them to lexicographically sorted names; it carries a "TODO: double check order" comment); (b) Behnke51 220 and Behnke53 214 in fjssp_fjssp-w_comparison.ipynb and ecdf_plots_fjssp.ipynb, which come from the solver['cplex_cp']['no_worker'] (FJSP) dict, while the 'worker' dict has nothing at or below ours; (c) counts, sizes and runtimes. FJSP values are a different problem and do not count. |
| jrc-rodec/FJSSP-W-Uncertainty-GECCO-Public | Tree | Code only, no results |
| elder-plinius/V3R1T4S | TROPHY_CASE.md (no FJSSP entry); known-knowns/ on main (no FJSSP-W entry); the target file; all 1020 PRs and 43 issues by title, plus a search for fjssp / FJSSP-W / worker flexibility / behnkegeiger / hurinksdata | The only FJSSP-W PR is #868 (userblaname, open, last updated 2026-11-07). Its INDEX.csv has 91 rows, and their overlap with our 65 is zero, checked row by row by cell and by file. Its body lists 95 files but includes only 91. The other 4 (Hurinksdata61, Hurinksdata63, Hurinkedata6, Hurinkrdata50) were excluded, and no objects were published for them. Its own value for Hurinkrdata50, 5684, is above our 5651. |
| xuqqqqq/FJSSP-W (AWLS, May 2026) | experiments/layer1_competition30.csv, layer2_public402.csv (empty result columns), layer3; paper drafts (EN/ZH TeX); literature target CSVs (DFJSP, a different set) | Fattahi20 1153, Hurinksdata40 1373, Hurinkrdata50 5697, Hurinkvdata5 507. All are above ours. |
| benbekir/GECCO-2026 | results/*.json (8 algorithm sets, competition instances), results/best_known.csv (old table copy), LAHC_vs_BEST.csv | All are above ours on the 4 overlapping instances; the old table has nothing at or below ours. |
| ScheduleOpt/optalcp-benchmarks | benchmarks/flexible-jobshop-w (README, model, data; HEAD 2026-11-06) | Data and model only; no results directory |
| plaans/flexible-jobshop-benchmarks | Tree | Plain FJSP data, no FJSSP-W results |
| Other GitHub hits (search: FJSSP-W, fjsspw, FJSP-W, worker flexibility, dual resource) | leonlan repos, weinbendera, AnastasijaFed (empty), dcogithub, hagegegege (other instance sets) | No FJSSP-W results on these instances |
| arXiv 2501.16159 v1-v3 (TeX source) | Every mention of our rows | Only Fattahi20, at the best-known 1147 (= UB) |
| Web/arXiv search for 2025-2026 FJSSP-W literature (GECCO 2026 accepted competition entries, competition page) | Search results and the competition site | No per-instance values beyond the above |

## 4. Trivial edits of published objects
Published schedules exist for all 65 instances: Qin's competition archives, FJSSPW-GA solver_result (cplex_cp, ortools, hexaly), and the competition archives for the 4 shared instances. I collected 2,639 such schedules (work-novelty/collect.py). For each one, I kept its machine/worker assignment and its per-machine, per-worker and per-job order, then applied these edits:
- left-justification (re-timing by the valid propagation rule). This also repairs overlapping submissions such as issue #14's.
- iterated forward-backward double justification, using the time-reversal symmetry of the problem and then left-justifying again.

Relabelling (renaming identical machines or workers) and deletion or restriction do not lower the makespan. The best makespan any published schedule reaches under these edits is above ours on every row (section 6, "polished"). The smallest margin is +1 (behnkegeiger41, behnkegeiger51). Our objects are not a trivial edit of a published object.

Provenance: the solver accepts an optional hint file (provenance/code/solve.py, argument 6). However, provenance/rows.csv puts all 65 rows in runs that the preregistrations and run reports record as "no warm start". None of the rows comes from the warm-started run 2026-11-12-0931. No published schedule had to be named as a seed.

## 5. Ties and near-ties
None of the 65 rows is tied. The smallest gaps between a public value and ours are +1 on behnkegeiger10, 23, 41, 45 (table UB) and on behnkegeiger51 (Qin 232). Hurinkvdata63 has our makespan of 250 equal to the table's LB of 250, so it is proven optimal. No public value of 250 or less exists for it.

## 6. Per-row results (all 65 hold; no row fails)
"UB hist min" is the lowest UB in any of the 8 table versions. "Best non-table value" is the lowest value found in any source other than the table. "Polished" is the best makespan reachable by trivial edits of published schedules, with the number of schedules in parentheses.

| Row | File | UB live | UB hist min | Ours | Best non-table value (source) | Polished (n schedules) | Result |
|---|---|---:|---:|---:|---|---|---|
| behnkegeiger10 | Behnke10 | 125 | 125 | 124 | 125 (FJSSPW-GA cplex_cp) | 125 (23) | holds |
| behnkegeiger21 | Behnke21 | 81 | 81 | 78 | 81 (comp. issues #1/#2 (Qin, all 402)) | 81 (23) | holds |
| behnkegeiger23 | Behnke23 | 79 | 79 | 78 | 79 (FJSSPW-GA cplex_cp) | 79 (23) | holds |
| behnkegeiger27 | Behnke27 | 119 | 119 | 116 | 119 (FJSSPW-GA cplex_cp) | 119 (23) | holds |
| behnkegeiger28 | Behnke28 | 111 | 111 | 108 | 111 (FJSSPW-GA cplex_cp) | 111 (23) | holds |
| behnkegeiger29 | Behnke29 | 112 | 112 | 110 | 112 (FJSSPW-GA cplex_cp) | 112 (23) | holds |
| behnkegeiger3 | Behnke3 | 86 | 86 | 83 | 86 (FJSSPW-GA cplex_cp) | 86 (23) | holds |
| behnkegeiger41 | Behnke41 | 80 | 80 | 79 | 80 (FJSSPW-GA GA) | 81 (23) | holds |
| behnkegeiger44 | Behnke44 | 78 | 78 | 76 | 78 (FJSSPW-GA GA) | 79 (23) | holds |
| behnkegeiger45 | Behnke45 | 80 | 80 | 79 | 80 (FJSSPW-GA GA) | 80 (23) | holds |
| behnkegeiger47 | Behnke47 | 113 | 113 | 111 | 113 (FJSSPW-GA GA) | 115 (23) | holds |
| behnkegeiger50 | Behnke50 | 118 | 118 | 114 | 118 (FJSSPW-GA cplex_cp) | 118 (23) | holds |
| brandimarte5 | BrandimarteMk5 | 166 | 166 | 164 | 166 (FJSSPW-GA cplex_cp) | 166 (23) | holds |
| chambersbarnes15 | ChambersBarnes15 | 1163 | 1163 | 1120 | 1163 (FJSSPW-GA cplex_cp) | 1163 (23) | holds |
| chambersbarnes16 | ChambersBarnes16 | 1155 | 1155 | 1113 | 1155 (FJSSPW-GA cplex_cp) | 1155 (23) | holds |
| chambersbarnes17 | ChambersBarnes17 | 1153 | 1153 | 1118 | 1153 (FJSSPW-GA cplex_cp) | 1153 (23) | holds |
| chambersbarnes18 | ChambersBarnes18 | 1091 | 1091 | 1082 | 1091 (FJSSPW-GA cplex_cp) | 1091 (23) | holds |
| chambersbarnes19 | ChambersBarnes19 | 1060 | 1060 | 1050 | 1060 (FJSSPW-GA cplex_cp) | 1060 (23) | holds |
| chambersbarnes20 | ChambersBarnes20 | 1143 | 1143 | 1118 | 1143 (FJSSPW-GA cplex_cp) | 1143 (23) | holds |
| chambersbarnes21 | ChambersBarnes21 | 1094 | 1094 | 1055 | 1094 (FJSSPW-GA cplex_cp) | 1094 (23) | holds |
| chambersbarnes4 | ChambersBarnes4 | 845 | 845 | 834 | 845 (FJSSPW-GA hexaly) | 845 (23) | holds |
| dppaulli4 | DPpaulli4 | 2520 | 2520 | 2447 | 2520 (FJSSPW-GA cplex_cp) | 2520 (23) | holds |
| fattahi20 | Fattahi20 | 1147 | 1147 | 1123 | 1127 (comp. issue #14 (reported; schedule invalid; best valid 1153, issue #11)) | 1147 (274) | holds |
| hurinkedata15 | Hurinkedata15 | 919 | 919 | 915 | 919 (FJSSPW-GA cplex_cp) | 919 (23) | holds |
| hurinkedata24 | Hurinkedata24 | 990 | 990 | 977 | 990 (FJSSPW-GA cplex_cp) | 990 (23) | holds |
| hurinkedata27 | Hurinkedata27 | 886 | 886 | 869 | 886 (FJSSPW-GA cplex_cp) | 886 (23) | holds |
| hurinkedata28 | Hurinkedata28 | 891 | 891 | 881 | 891 (FJSSPW-GA cplex_cp) | 891 (23) | holds |
| hurinkedata29 | Hurinkedata29 | 1101 | 1101 | 1090 | 1101 (FJSSPW-GA cplex_cp) | 1101 (23) | holds |
| hurinkedata30 | Hurinkedata30 | 1174 | 1174 | 1157 | 1174 (FJSSPW-GA cplex_cp) | 1174 (23) | holds |
| hurinkedata32 | Hurinkedata32 | 1104 | 1104 | 1091 | 1104 (FJSSPW-GA cplex_cp) | 1104 (23) | holds |
| hurinkedata39 | Hurinkedata39 | 1120 | 1120 | 1115 | 1120 (FJSSPW-GA cplex_cp) | 1120 (23) | holds |
| hurinkedata40 | Hurinkedata40 | 1317 | 1317 | 1291 | 1317 (FJSSPW-GA cplex_cp) | 1317 (23) | holds |
| hurinkedata41 | Hurinkedata41 | 1138 | 1138 | 1111 | 1138 (FJSSPW-GA cplex_cp) | 1138 (23) | holds |
| hurinkedata42 | Hurinkedata42 | 1133 | 1133 | 1104 | 1133 (FJSSPW-GA cplex_cp) | 1133 (23) | holds |
| hurinkedata43 | Hurinkedata43 | 1101 | 1101 | 1069 | 1101 (FJSSPW-GA cplex_cp) | 1101 (23) | holds |
| hurinkedata9 | Hurinkedata9 | 784 | 784 | 782 | 784 (FJSSPW-GA cplex_cp) | 784 (23) | holds |
| hurinkrdata13 | Hurinkrdata13 | 767 | 767 | 762 | 767 (FJSSPW-GA cplex_cp) | 767 (23) | holds |
| hurinkrdata4 | Hurinkrdata4 | 540 | 540 | 538 | 540 (FJSSPW-GA hexaly) | 540 (23) | holds |
| hurinkrdata42 | Hurinkrdata42 | 1004 | 1004 | 979 | 1004 (FJSSPW-GA cplex_cp) | 1004 (23) | holds |
| hurinkrdata44 | Hurinkrdata44 | 908 | 908 | 892 | 908 (FJSSPW-GA cplex_cp) | 908 (23) | holds |
| hurinkrdata5 | Hurinkrdata5 | 500 | 500 | 498 | 500 (FJSSPW-GA ortools) | 500 (23) | holds |
| hurinkrdata50 | Hurinkrdata50 | 5701 | 5701 | 5651 | 5681 (comp. issue #14 (reported; schedule invalid; best valid 5697, issue #6)) | 5697 (274) | holds |
| hurinkrdata52 | Hurinkrdata52 | 6240 | 6240 | 6193 | 6240 (FJSSPW-GA cplex_cp) | 6240 (23) | holds |
| hurinkrdata6 | Hurinkrdata6 | 458 | 458 | 454 | 458 (FJSSPW-GA cplex_cp) | 458 (23) | holds |
| hurinkrdata7 | Hurinkrdata7 | 479 | 479 | 474 | 479 (FJSSPW-GA cplex_cp) | 479 (23) | holds |
| hurinkrdata9 | Hurinkrdata9 | 765 | 765 | 763 | 765 (FJSSPW-GA cplex_cp) | 765 (23) | holds |
| hurinksdata26 | Hurinksdata26 | 951 | 951 | 948 | 951 (FJSSPW-GA hexaly) | 951 (23) | holds |
| hurinksdata29 | Hurinksdata29 | 1202 | 1202 | 1132 | 1202 (FJSSPW-GA cplex_cp) | 1202 (23) | holds |
| hurinksdata30 | Hurinksdata30 | 1192 | 1192 | 1177 | 1192 (FJSSPW-GA hexaly) | 1192 (23) | holds |
| hurinksdata31 | Hurinksdata31 | 1212 | 1212 | 1148 | 1212 (FJSSPW-GA hexaly) | 1212 (23) | holds |
| hurinksdata32 | Hurinksdata32 | 1146 | 1146 | 1131 | 1146 (FJSSPW-GA cplex_cp) | 1146 (23) | holds |
| hurinksdata33 | Hurinksdata33 | 1248 | 1248 | 1240 | 1248 (FJSSPW-GA hexaly) | 1248 (23) | holds |
| hurinksdata39 | Hurinksdata39 | 1192 | 1192 | 1182 | 1192 (FJSSPW-GA cplex_cp) | 1192 (23) | holds |
| hurinksdata40 | Hurinksdata40 | 1329 | 1329 | 1285 | 1301 (comp. issue #11 (Yu Sun), valid) | 1301 (274) | holds |
| hurinksdata42 | Hurinksdata42 | 1168 | 1168 | 1159 | 1168 (FJSSPW-GA cplex_cp) | 1168 (23) | holds |
| hurinksdata43 | Hurinksdata43 | 1175 | 1175 | 1137 | 1175 (FJSSPW-GA cplex_cp) | 1175 (23) | holds |
| hurinksdata47 | Hurinksdata47 | 676 | 676 | 669 | 676 (FJSSPW-GA hexaly) | 676 (23) | holds |
| hurinkvdata49 | Hurinkvdata49 | 4740 | 4740 | 4718 | 4740 (FJSSPW-GA cplex_cp) | 4740 (23) | holds |
| hurinkvdata5 | Hurinkvdata5 | 504 | 504 | 501 | 503 (comp. issue #5 (CIAM), valid) | 503 (274) | holds |
| hurinkvdata63 | Hurinkvdata63 | 251 | 251 | 250 | 251 (FJSSPW-GA cplex_cp) | 251 (23) | holds |
| behnkegeiger51 | Behnke51 | 234 | 234 | 231 | 232 (comp. issues #1/#2 (Qin, all 402)) | 232 (23) | holds |
| behnkegeiger52 | Behnke52 | 234 | 234 | 212 | 234 (comp. issues #1/#2 (Qin, all 402)) | 234 (23) | holds |
| behnkegeiger53 | Behnke53 | 229 | 229 | 216 | 229 (FJSSPW-GA cplex_cp) | 229 (23) | holds |
| behnkegeiger54 | Behnke54 | 251 | 251 | 227 | 236 (comp. issues #1/#2 (Qin, all 402)) | 236 (23) | holds |
| behnkegeiger55 | Behnke55 | 237 | 237 | 220 | 237 (FJSSPW-GA cplex_cp) | 237 (23) | holds |

Rows that fail: none. Rows that hold: all 65 listed above.

## 7. Limits
- I could not read the MarkRogoQC release assets for issue #13 (404, repository deleted). The values in that issue's table are all far above the UB.
- Literature search covered arXiv full text for the benchmark paper, GitHub, and web search. I did not have paywalled proceedings (GECCO 2026 companion papers), so I covered them only through the competition attachments, which contain those entries' own result files.
- The working files (downloads, scripts, intermediate JSON) are in panel-v2/work-novelty/.

pass: true
