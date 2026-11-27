# Novelty verdict
context: fresh subagent started for this claim only

Claim under review: claim/CLAIM.md, claim/rows.csv. Six ITC2021 instances, each claimed strictly below the board's Best UB: Early 9 56 -> 51, Early 12 315 -> 300, Middle 5 279 -> 278, Middle 12 358 -> 338, Middle 15 462 -> 459, Late 11 196 -> 191. I read only claim/. Working files (my scripts, live copies, scans) are in panel/work-novelty/.

## 1. Primary status source (live, one plain request per page, User-Agent "V3R1T4S-novelty-check/1.0 (read-only research)")

| page | UTC | HTTP | sha256 | vs claim/ |
|---|---|---|---|---|
| https://robinxval.ugent.be/ITC2021/instances.php | 2026-11-27T14:47:44Z | 200 | e008069e04f701038edce32190c5ecb5a978067c251bedd26f00c08740832f75 | identical to claim/data/board.html (and to claim/data/fetch.json) |
| RobinX/history.php ... ITC2021_Early_9.xml | 2026-11-27T14:48:32Z | 200 | 0be1eb4b2b527cbb5118738e8b5531102efb260720d3a7bfae9bac3369e061f6 | identical to claim/data/hist/ITC2021_Early_9.html |
| ... ITC2021_Early_12.xml | 2026-11-27T14:48:35Z | 200 | 056155701db1d78436607988e06a3b67c901b55e524321e851405289e47fcc76 | identical |
| ... ITC2021_Middle_5.xml | 2026-11-27T14:48:37Z | 200 | 2baa0e250084bf2eb18bebe236297e9c54f14016932270fa2791d90d01e91216 | identical |
| ... ITC2021_Middle_12.xml | 2026-11-27T14:48:42Z | 200 | 0cecebad677d7bc54eeb2ada875170c063b21c1cd8aeb01bdf0b3047c34443db | identical |
| ... ITC2021_Middle_15.xml | 2026-11-27T14:48:45Z | 200 | bbac4dfeaf8a24472c7e830044a4baf8e910e7684967209b2242c5d328cd7e11 | identical |
| ... ITC2021_Late_11.xml | 2026-11-27T14:48:47Z | 200 | e618938b6ec33a1f7d3251dcbf2669c8c0c3ead070c0154ab9293fd31cbf0517 | identical |

History URL form: https://robinxval.ugent.be/RobinX/history.php?instanceFileName=ITC2021/Instances/ITC2021_{instance}.xml&repositoryName=ITC2021. Disclosure: my first attempt used a wrong path (/ITC2021/history.php) and got HTTP 404 "File not found." for all six (14:47:57Z-14:48:13Z). That was my URL error, not a block; I fetched the correct path once per page afterwards.

I also fetched once each the six posted record solutions (validator/Repository/ITC2021/Solutions/<file>, 14:49:17Z-14:49:29Z, all HTTP 200). Each is byte-identical to its claim/data/records/ copy (sha256 88ff6777..., 6efdb584..., 4e37096d..., 756806ac..., a09af408..., ecfea6fa...). ITC2021/index.php (14:52:08Z, 200, 39f381ef...): latest news is 18 March 2025 (Middle 2 and 3). The 11 July 2026 Late 11 entry is in the history table but has no news item. ITC2021/downloads.php (14:57:53Z, 200, a5402e5d...): its newest publications are from 2024 (Premananda, Tjahyanto and Mukhlason, Ann. Oper. Res. 343; Van Bulck et al., EJOR 318).

Board rows (live): Early 9 UB (0, 56) Van Bulck and Goossens; Early 12 (0, 315) same; Middle 5 (0, 279) same, LB (0, 47); Middle 12 (0, 358) Clémence Van den Ostende, LB (0, 1); Middle 15 (0, 462) Krystallidis, Musliu, Saturn, LB (0, 1); Late 11 (0, 196) Premananda and Muklason. These match CLAIM.md.

Every solution listed in the history pages (solutions table, not the bounds table):
- Early 9: Team UoS 108 (24-6-2021); first milestone 178; Van Bulck and Goossens 56 (04-2023, Early9_0_56_FBHS.xml).
- Early 12: Saturn 380; milestone 555; Van Bulck and Goossens 315 (04-2023).
- Middle 5: Team MODAL 413; Van Bulck and Goossens 279 (01-2021, FBHS).
- Middle 12: Krystallidis, Musliu, Van Bulck, Goossens 597; Van Bulck 599 (10-2022); Van Bulck and Goossens 674; Team DES 911; Clémence Van den Ostende 358 (undated).
- Middle 15: Team DES 485 (12-7-2021); Saturn 495; Krystallidis, Musliu, Saturn 462 (undated).
- Late 11: Krystallidis and Musliu 201 (2-2024); Team DES 202; Team Udine 207; Premananda and Muklason 196 (11-7-2026).

The minimum listed value for each instance equals the Best UB in CLAIM.md. None is at or below the claimed value.

## 2. Literature, web and code search (results at or below the claimed values)

- RobinX GitHub repository (github.com/Robin-X/RobinX, HEAD 878bf2db7b25b43cc3022bc08c00be938b997b6a, last commit 2026-10-22). This is the same commit as the claim's validator. I made a sparse clone of Repository/ITC2021/Solutions (166 files) as data and parsed every file's InstanceName and ObjectiveValue (panel/work-novelty/robinx_six_scan.txt). The repo holds solution files that the history pages do not list: Early9_56.xml (56), Early9_67.xml (67), Early12_0_315.xml (315), Early12_320.xml (320), Middle5_0_279.xml (279), Middle5_295.xml, Middle5_299.xml, Middle12_704.xml, Middle_12_893.xml. Minimum stated objective per instance: Early 9 56, Early 12 315, Middle 5 279, Middle 12 597 (358 exists only on the website), Middle 15 462, Late 11 196. Nothing is at or below the claimed values. The 26 files with unrecognised names are all Test, Demo or TC_BM instances.
- Krystallidis, A. (2023), TU Wien diploma thesis, "Adaptive large neighbourhood search for double-round-robin sports tournament problem" (repositum.tuwien.at handle 20.500.12708/189318; PDF sha256 9f39ab1e..., read through text extraction). Tables 4.17 and 4.18 (ALNS best values and best-known values at that time) give: Early 9 best-known 56, own 452 and then 367 after 24 h; Early 12 best-known 320, own 765 and then 710; Middle 5 295, own 472 and then 469; Middle 12 599, own 954 and then 914; Middle 15 495, own 1266 and then 1202; Late 11 207, own 236 and then 226. All are above our values.
- github.com/ankranidiotis/cppso (also published as nassoskranidiotis/CP-PSO_Results, last push 2024-09-28). Its README table: Early 9 best 56, Dimitsas et al. 2022 448, Rosati et al. 2022 132, CP-PSO 1613; Early 12 315 / 1025 / 1010 / 1445; Middle 5 279 / 732 / 510 / 1029; Middle 12 597 / 1596 / 950 / 3291; Middle 15 462 / 1833 / 985 / 6290; Late 11 201 / 511 / 207 / 796. All above.
- Rosati, Petris, Di Gaspero and Schaerf, multi-neighbourhood SA (PATAT ITC2021 paper 7; J. Sched. 2022). Values from search snippets and the cppso table: Early 12 1010, Middle 15 985, Late 11 207 (their best), and Early 9 132. All above. I did not read the paper's full table myself. The robertomrosati/sa4stt repository holds code and instances only, with no result files.
- Team UoS (Lamas-Fernandez, Martinez-Sykora, Potts; PATAT ITC2021 paper 6), Team DES / Phillips et al. ALNS matheuristic (PATAT ITC2021 paper 4), and the competition overviews (MathSport 2021 paper; Van Bulck and Goossens, EJOR 308, 2023). The official 2021 results reported in snippets are Late 11 207, Early 12 380 and Middle 15 495. Their later improvements are the DES and UoS entries on the board. All are above.
- Van Bulck and Goossens, "First-break-heuristically-schedule", ORL 51 (2023). Its records 56, 315 and 279 are the board's (Remarks field in the posted XML). I did not read the full text because it is paywalled.
- Van Bulck et al., "Which algorithm to select in sports timetabling?" (arXiv 2309.03229v2, EJOR 318, 2024). It reports no per-instance objective values, only aggregate tables.
- Premananda, Tjahyanto and Mukhlason, Ann. Oper. Res. 343:411-427 (2024). I could not read the full text: Springer redirected to an authorisation and cookie page, which I did not follow. Their later records (Middle 2 and 3 in 2025, Late 11 196 in 2026) are on the board. I found no 2025 or 2026 paper by them.
- Fonseca and Toffolo, J. Sched. 2022 (fix-and-optimize) and the georgehgfonseca/itc2021 repository (last push 2024-02-27, code only). On the board for these instances they hold only lower bounds (Middle 5 LB 45, Middle 15 LB 1).
- Neumann (2023), TU Wien CP/SA thesis: snippets say it is far from the best known values. Jaradat (2022) Elitist-Ant and the DAPSO-SD PSO paper: described as poor compared with the best. Not read in full.
- arXiv API (export.arxiv.org, 2026-11-27T14:56:02Z and 14:56:06Z, HTTP 200). "ITC2021" returns only 2309.03229. "sports timetabling" also returns 2609.03612 (a TTP overview, 2026-09) and 2011.09135. Neither has ITC2021 per-instance values.
- GitHub repository search ("ITC2021", "sports timetabling") and code search (instance names, record filenames such as "Middle_15_462", "ITC2021_Late_11_196", "Middle12_358", "Early9_0_56", "Early12_0_315_FBHS"):
  - mnn31/qoblib-solvers (QOBLIB problem 05, pushed 2026-11-24). Feasibility only, soft constraints ignored. Its RobinX penalties are Middle 5 7782, Middle 12 4609 and Middle 15 8251; Early 9, Early 12 and Late 11 are feasible but have no penalty recorded. All are far above.
  - amine-athmani/ITC2021 (2026-10): Gurobi MILP code, no results.
  - joaosoaressantos22/solve_itc2021: empty repository.
  - yash18uniapp-code/calendar-aware-sports-scheduling (2026-11-25): a modified calendar-aware problem, so its scores are not ITC2021 objectives.
  - No other result files were found.
- Search for Clémence Van den Ostende's thesis or paper (the Middle 12 358 holder): nothing found. The scriptiebank.be listing of a 2026 Ghent badminton thesis had no visible author. Not read.

## 3. V3R1T4S repository (elder-plinius/V3R1T4S, main at 1897a461aa23cf442dfaba78be0f85dc9e747b62)

- PR and issue searches, all states: "ITC2021", "ITC 2021", "itc2021-sports-timetabling-ub", "sports timetabling", "timetabling", "robinx", "Van Bulck", "Late_11", "Middle_15". The search API query "repo:elder-plinius/V3R1T4S itc2021" returned total_count 0. The only timetabling hits are ITC-2007 exam (#1094, #1092) and TimPassLib (#1122), which are unrelated.
- The repository tree has exactly one ITC2021 file, known-unknowns/optimization-benchmarks/itc2021-sports-timetabling-ub.md. There is no known-knowns entry and no ITC, timetabling or sports entry in TROPHY_CASE.md.
- No prior ITC2021 claim exists.

## 4. Trivial-edit question

Bank rule (kit/RUN.md, NOVELTY): "one that trivial edits of a published object give (deletion, restriction, a valid propagation rule, relabelling, symmetry, a local numerical polish, alone or combined) is not new, and one seeded from a published object must name it and beat what those edits alone give."

Comparison of each object with its record (claim/data/records/), by (home, away, slot) triples. Each timetable has 306 games (18 teams) or 380 games (20 teams). Script: panel/work-novelty/scripts/compare.py and diffdetail.py; output in panel/work-novelty/compare.txt.

| instance | games differing from record | identical slots | home/away cells changed | slots touched / teams touched | fewest differing games vs any published solution |
|---|---:|---:|---:|---|---|
| Early 9 | 179 / 306 (58%) | 2 / 34 | 0 / 612 | 32 / 18 | 179 (record) |
| Early 12 | 244 / 380 (64%) | 0 / 38 | 0 / 760 | 38 / 20 | 244 (record and Early12_0_315.xml) |
| Middle 5 | 141 / 306 (46%) | 2 / 34 | 0 / 612 | 32 / 18 | 141 (record and Middle5_0_279.xml) |
| Middle 12 | 35 / 380 (9.2%) | 26 / 38 | 0 / 760 | 12 / 13 | 35 (record); at least 357 vs every other |
| Middle 15 | 131 / 380 (34%) | 7 / 38 | 0 / 760 | 31 / 20 | 131 (record) |
| Late 11 | 15 / 380 (3.9%) | 32 / 38 | 6 / 760 | 6 / 10 | 15 (record); 32 vs Late_11_201.xml |

This confirms the provenance statement. Five objects keep the record's home/away pattern exactly (0 cells changed) and reassign opponents. Late 11 changes 6 home/away cells. No object equals a slot permutation of its record: the slots that match some record round are exactly the identical slots.

Judgment: none of the six is a trivial edit in the bank's sense.
- Relabelling or symmetry: ITC2021 constraints name specific teams and slots. No object is a team or slot relabelling of a published one (the slot-matching check above), and every penalty strictly decreases.
- Deletion or restriction: these do not apply, because every object is a complete double round robin.
- Local numerical polish: the objective is integer, and each object lowers it by an integer amount.
- Seed and margin: every row is seeded from the record, which the claim names (rows.csv method, provenance/README.md "warm start from the record", claim/data/records/). Edits of the allowed trivial kinds can at most reproduce the record's value. Each object beats that strictly (by 5, 15, 1, 20, 3 and 5).
- Small-edit rows: Middle 12 (35 games, 12 slots) and Late 11 (15 games over 6 slots, 6 home/away flips) are small local re-optimisations of the record. Late 11's change spans 6 slots and 10 teams, so it is not one classical swap move (a partial round swap touches 2 slots). I judge them local-search improvements of a discrete objective, which is what the target's own "Ideas" section recommends ("Start from the posted best solutions ... long polishing runs"), not trivial edits. The gate should read this as a judgment, with these numbers disclosed.

## 5. Per row: closest published value found

| instance | ours | closest published (at or above ours) | source | at or below ours? | row |
|---|---:|---:|---|---|---|
| Early 9 | 51 | 56 | board and history (Van Bulck and Goossens 04-2023); also Early9_56.xml in the RobinX repo | no | pass |
| Early 12 | 300 | 315 | board and history; also Early12_0_315.xml in the repo | no | pass |
| Middle 5 | 278 | 279 | board and history (FBHS); also Middle5_0_279.xml in the repo | no (margin 1) | pass |
| Middle 12 | 338 | 358 | board and history (Van den Ostende) | no | pass |
| Middle 15 | 459 | 462 | board and history (Krystallidis, Musliu, Saturn) | no (margin 3) | pass |
| Late 11 | 191 | 196 | board and history (Premananda and Muklason, 11-7-2026) | no | pass |

No equal or lower value was found for any row, so no row fails.

## 6. Residual limits

- Full texts I could not read: Premananda et al. 2024 (Springer redirected to an authorisation and cookie page, not followed), FBHS ORL 2023 (paywalled), the EJOR 2023 overview and Rosati et al. J. Sched. 2022 tables (seen only through snippets and third-party tables), PATAT 2024 proceedings (PDF over the fetch size limit), Van den Ostende's work (not found), and ResearchGate (not tried). All of these date from 2024 or earlier, and their authors' best values are on the board. The exception is the undated Van den Ostende entry, which is also on the board.
- The board is updated only from e-mail submissions. A result sent to the organisers but not yet posted, or a private result, cannot be seen. Web search coverage of 2025-2026 is incomplete: I found no 2025-2026 ITC2021 per-instance paper at all.
- I did not run any validator. Penalty correctness is the REPRODUCE skeptic's job. I compared values as stated and game sets as posted.
- The trivial-edit judgment for Middle 12 and Late 11 is an interpretation of "local numerical polish" for a discrete objective, as explained in section 4.

pass: true
