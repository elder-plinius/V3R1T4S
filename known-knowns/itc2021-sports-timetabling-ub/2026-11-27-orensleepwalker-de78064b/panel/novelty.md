# Novelty verdict
context: fresh subagent started for this claim only

Claim under review: the lower bounds in claim/CLAIM.md and claim/rows.csv: Early 14 >= 4, Early 9 >= 40, Middle 6 >= 60, Middle 9 >= 20, Late 9 >= 20. Inputs read: claim/ only (CLAIM.md, PREREG.md, REPRODUCE.md, target.md, rows.csv, data/fetch.json, data/board.html, data/hist/*, data/inst/*, the two PROOF.md files, code/break_floor_stdlib.py). I wrote only in panel/work-novelty/ and this file. Downloads were treated as data, and no downloaded program was run. My own stdlib text extractors (stored in a scratch directory outside the run) read the PDFs.

Short answer: no published lower bound on any of the five instances is at or above the claimed value. However, the board and the history pages do not show the highest published bounds on two rows. Team MODAL's bound files from 2023-02-01 give Middle 6 >= 39 and Late 9 >= 5. Both are in the RobinX GitHub repository and are served by the board site, but neither appears in the instances table or on the history pages. Both are still far below the claimed 60 and 20. The claim text should cite them (disclosure below).

## Sources (fetched 2026-11-27, UTC)

### Board site (robinxval.ugent.be). One plain GET per page, User-Agent "V3R1T4S-novelty-check/1.0". Every page returned HTTP 200, with no challenge.

| page | time (UTC) | sha256 | vs claim/data |
|---|---|---|---|
| ITC2021/instances.php | 14:54:28Z | e008069e04f701038edce32190c5ecb5a978067c251bedd26f00c08740832f75 | byte-identical to data/board.html |
| history Early 14 | 14:54:46Z | 0b993e9e663e8b4db2b332f6d84a4f3a0959c6a006aa452f9215b897a766237a | identical |
| history Early 9 | 14:54:49Z | 0be1eb4b2b527cbb5118738e8b5531102efb260720d3a7bfae9bac3369e061f6 | identical |
| history Middle 6 | 14:54:51Z | ec19f942aa447004322e8af3ef88903a4471c5c00ad61ffbb32eee333c046327 | identical |
| history Middle 9 | 14:54:53Z | 0ad1e2358ae62b098168f2969c0a2fdd3a4aede35da957488513aff85c52fbe0 | identical |
| history Late 9 | 14:54:55Z | 1cac5c3eeb2fa00c33e0934a0319520b90bc2fa1ae8013ba36a41c7838701ee0 | identical |
| Bounds/ITC2021_Early_14_Bound_1.xml | 14:55:17Z | bc5222f6...4f50939f | (the posted LB file) |
| Bounds/ITC2021_Early_9_Bound.xml | 14:55:18Z | 9c3e83ae...69a968d | |
| Bounds/ITC2021_Middle_6_Bound_24.xml | 14:55:19Z | 4054259c...28297 | |
| Bounds/ITC2021_Middle_9_Bound.xml | 14:55:21Z | e157142d...e1306e50 | |
| Bounds/ITC2021_Late_9_Bound_3.xml | 14:55:22Z | ef7b833b...fe | |
| ITC2021/index.php (news) | 15:03:45Z | 39f381ef5b9eba0cd47473852aa39b145661eb03e57ca9051feffd7ac5ed9d51 | |
| ITC2021/downloads.php (publication list) | 15:07:03Z | a5402e5d098ab41ffbda5246fe6324f6d815fc2af20975d93ab63f56fedf11f7 | |
| Bounds/ITC2021_Middle_6_Bound_39.xml (not linked from the board) | 15:10:59Z | 69e567d1eaa97f2618b5b88e41747353bfc5d0a0b96754e5e4b6bdc37835c67a | |
| Bounds/ITC2021_Late_9_Bound_5.xml (not linked from the board) | 15:11:00Z | a27cf0de4012a6bc0a68922303199c7c4ba598e98eff93c73062a2eef4fd7602 | |

Saved copies are in panel/work-novelty/fetch/.

### Bounds posted on the board and the history pages (task 1)

| instance | board Best LB (link) | history "Overview bounds" (date, contributor, value) | board Best UB |
|---|---|---|---|
| Early 14 | (0, 1) Bound_1 | 29-10-2020 David Van Bulck (0,0); 10-11-2021 Fonseca & Toffolo (0,1) | (0, 4) Team Gionar |
| Early 9 | (0, 0) Bound | 29-10-2020 David Van Bulck (0,0) | (0, 56) Van Bulck & Goossens (FBHS) |
| Middle 6 | (0, 24) Bound_24 | 30-1-2021 Van Bulck (0,0); 10-11-2021 Fonseca & Toffolo (0,2); 11-11-2021 Team Udine (0,24) | (0, 1090) Krystallidis, Musliu, Saturn |
| Middle 9 | (0, 0) Bound | 30-1-2021 Van Bulck (0,0) | (0, 415) Van Bulck & Goossens |
| Late 9 | (0, 3) Bound_3 | 15-4-2021 Van Bulck (0,0); 10-11-2021 Fonseca & Toffolo (0,3) | (0, 498) Van Bulck & Goossens |

Remarks inside the bound files: the Fonseca & Toffolo values come from "an integer programming model running single-thread on Gurobi solver for 1 hour". The Udine value comes from CPLEX with two threads for 8 days ("Best bound found after 17386 seconds"). The Van Bulck values are "Feasibility guarantee". All five rows are still marked open (bg-danger). Each claimed bound is strictly above every bound on the board and on the history pages, and at or below the posted Best UB (4<=4, 40<=56, 60<=1090, 20<=415, 20<=498).

### Bounds missing from the board: RobinX GitHub repository (Robin-X/RobinX, read with gh, about 15:08Z)
- Repository/ITC2021/Bounds/ holds 138 files. For the five instances it holds: Early_14_Bound (0) and Bound_1 (1); Early_9_Bound (0); Middle_6_Bound (0), _2 (2), _24 (24) and **_39 (39, Team Modal, 01-02-2023)**; Middle_9_Bound (0); Late_9_Bound (0), _3 (3) and **_5 (5, Team Modal, 01-02-2023)**. Commit 7fb020cc6e (2023-02-01, "Repository update") added MODAL's 28 bounds. These match the site news item "February 1, 2023. A total of 28 new lower bounds have been added ... by team MODAL". Their Remarks field is a table: "M06 Best_LB_root 22, Best_LB_end 39" and "L09 3 -> 5". MODAL filed no bound for Early 14, Early 9 or Middle 9. The 28 files cover Early 3/5/6/7/8/10/11/15, Middle 1/2/3/5/6/7/10/11/12/15 and Late 1/2/3/5/6/7/8/9/13/14.
- The board's instances table does not use these files. For example it shows Middle 3 3378 against MODAL's 3532 and Early 7 1296 against MODAL's 1358, and on our rows Middle 6 24 against 39 and Late 9 3 against 5. The board site still serves both files (HTTP 200, fetched above).
- Highest published bound is therefore 39 for Middle 6 and 5 for Late 9. Both are below the claim.

### Literature (task 2)
| source | how obtained (sha256 of the file read) | bounds reported on our rows | verdict |
|---|---|---|---|
| Rosati, Petris, Di Gaspero, Schaerf, J. Sched. 25:301-319 (2022), Table 8, column "CPLEX best bound" (Team Udine) | Springer OA PDF, 36394677...bc78331 | E9 0.0, E14 1.0, M6 23.0, M9 0.0, L9 2.9 | all below the claim |
| van Doornmalen, Hojny, Lambers, Spieksma (Team TU/e), PATAT 2021 vol. II, table of MIP results with a 24-hour limit, "Dual" column (Early instances only) | patatconference.org paper2, 5a393285...893a1 | E9 0.00, E14 1.00 | below |
| Berthold, Koch, Shinano (Team MODAL), "MILP. Try. Repeat.", PATAT 2021 | paper1, 8f2da204...eaff1c1 | Table 1 lists solutions only (E9 122, E14 25, M6 2270, M9 810, L9 790). The text says only "positive LB proven" for 36 instances. Later bounds are in the RobinX files above (M6 39, L9 5) | below |
| Fonseca & Toffolo (Team GOAL), PATAT 2021 version | paper5, 7b86cb39...f3e793 | Table 1 lists solutions only. Their LBs are the board files (E14 1, M6 2, L9 3) | below |
| Fonseca & Toffolo, J. Sched. 25:273-286 (2022) | Springer paywall (HTML only, ee69970a...) | full text not read. Their bound files on the board say "Gurobi 1 hour" (E14 1, M6 2, L9 3) | below (residual limit) |
| GOAL repo github.com/georgehgfonseca/itc2021sportsScheduling, data/ITC2021_*Log.txt | gh API | the "lb" column reads E9 490-538, M6 1740, M9 1050-1130 | **not global bounds**: these are fix-and-optimize subproblem values with most variables fixed. They exceed known feasible penalties (E9 56, M6 1090, M9 415), so they cannot be valid global lower bounds |
| Van Bulck & Goossens, "First-break-heuristically-schedule", Oper. Res. Lett. 51(3):326-331 (2023) (the HAP decomposition with pattern costs) | ScienceDirect returned 403 and no OA copy was found | full text not read. The method fixes a HAP set with a Benders master and then schedules heuristically. Any value it reports is the cost of the selected or relaxed patterns, not a proven global bound unless the paper says so. Its authors run the board, and the board posts only their FBHS solutions (E9 56, M9 415, L9 498) and no FBHS lower bound on these rows | no global bound known (residual limit) |
| Van Bulck & Goossens, "A traditional Benders' approach to sports timetabling" (EJOR 2023) | UGent backoffice PDF, ce59dc5a...b740e | LB tables cover TTP, travel and rest-difference instances only, not ITC2021 | not applicable |
| Van Bulck & Goossens, ITC2021 overview, EJOR 308 (2023) | UGent preprint, 97c1b93b...59194 | no per-instance LB table. It says later bounds are tracked on the website | none |
| Van Bulck, Goossens et al., "Which algorithm to select in sports timetabling?", EJOR 318 (2024) | arXiv 2309.03229, e18a5442...e68 | no per-instance bounds. It says only two instances were solved to optimality | none |
| Krystallidis, TU Wien diploma thesis (2023), ALNS (advisor Musliu) | repositum PDF, 9f39ab1e...733bf | no lower bounds. It says 3 of 45 instances are proven optimal (the closed ones: Middle 4, Late 4, Late 15) | none. Early 14 is not closed there |
| Lester (Reprobate), J. Sched. 25:287-299 (2022) and PATAT 2021 | PDFs 6f524fa8..., 58014104... | no per-instance bounds | none |
| Sumin & Rodin (Saturn), PATAT 2021 | 7e53a4e0... | cites the 3n-6 break bound for *mirrored* DRR only. No instance bounds | none |
| Phillips, O'Sullivan, Walker, PATAT 2021; Lamas-Fernandez, Martinez-Sykora, Potts (UoS), PATAT 2021; Dimitsas et al., PATAT 2022; Van Bulck et al., MathSport 2021; organisation rules V7; PATAT 2022 paper 26; van Doornmalen et al., arXiv 2210.08292 | PDFs hashed in panel/work-novelty/lit/ | no lower bounds on these instances | none |
| Lamorgese | web search found no ITC2021 work under this name | none found | none |
| GitHub search "itc2021" and "sports timetabling" (about 15:05Z): robertomrosati/sa4stt, amine-athmani/ITC2021 (Gurobi MILP, 2026-10), nassoskranidiotis/CP-PSO_Results (its README LB column copies the board: 0, 1, 24, 0, 3), mnn31/qoblib-solvers (QOBLIB problem 05 is feasibility only, with no objective), yash18uniapp-code, rawunder/STASP_HonoursProject (a copy of the RobinX bounds), others | gh API | none above the board or MODAL values | none |

Sources I could not read: Fonseca & Toffolo (J. Sched. 2022, paywall); the FBHS ORL paper (403 and paywall); Rosati's PhD thesis (2024) and his ESWA 2024 paper (air.uniud.it returned 403, and I did not retry); Premananda et al. (Ann. OR 2024), Jaradat (2022), Alsmadi et al. (2022) and Lester's SAT Competition 2022 note. The unread papers are heuristic or feasibility work, so no lower bounds are expected from them.

### V3R1T4S (task 3), gh read-only, about 15:03Z
- `gh pr list --state all` returned 1201 PRs (#1 to #1256). No title or branch mentions ITC2021, sports or RobinX. The only timetabling PRs are #1094 (ITC-2007 exam) and #1122 (TimPassLib).
- `gh search prs` and `gh search issues` for ITC2021, itc2021, "sports timetabling", itc2021-lower-bound-certificate, Early_14, robinx, Middle_6/Late_9/Gionar returned nothing. The same search for FJSSP did return hits, so the search works. The issue list (55 issues) has no ITC2021 issue.
- Code search finds ITC2021 only in the bank card known-unknowns/optimization-benchmarks/itc2021-sports-timetabling-ub.md and in README.md.

## Per-row result (highest published bound found vs claimed)

| row | highest published global LB found | source | claimed | strictly higher? |
|---|---:|---|---:|---|
| Early 14 | 1 | Fonseca & Toffolo, board, 2021. Also Rosati CPLEX 1.0 and TU/e dual 1.00 | 4 | yes (equals posted UB 4, so it would close the instance. No source closes it) |
| Early 9 | 0 | board (Van Bulck 2020). TU/e dual 0.00, Rosati 0.0 | 40 | yes |
| Middle 6 | **39** | Team MODAL 2023-02-01 (RobinX GitHub and a site file not shown on the board). Board 24 (Udine) | 60 | yes |
| Middle 9 | 0 | board. Rosati 0.0 | 20 | yes |
| Late 9 | **5** | Team MODAL 2023-02-01 (same). Board 3 (Fonseca & Toffolo) | 20 | yes |

## Is the argument so standard that the bounds carry no new information? (task 4)
The ingredients are textbook: the de Werra n-2 break floor, the rule that at most two teams can be break-free and must use complementary patterns, per-slot home/away balance (home-home breaks equal away-away breaks, so the total is even), and per-team enumeration of venue patterns under that team's hard CA1/BR1/forced-GA1 venue rules. That enumeration is the first step of first-break-then-schedule. The Early 9 odd-index parity step is a short extra argument. On its own the plain de Werra floor gives nothing here: on all five instances BR2 has intp = n-2 (18 for 20 teams, 16 for 18 teams), so it yields penalty 0. The gain comes entirely from the team-specific hard venue rules.

Still, the resulting numbers were not public information. Gurobi for 1 hour (GOAL), CPLEX for up to 8 days (Udine), 24-hour MIP runs (TU/e) and MODAL's massively parallel MILP reached only 1/0/39/0/5. The organisers, who wrote the HAP and Benders papers, have not posted any break-based bound. No source treats Early 14 as solved to optimality. The bank's partial win asks only for a strictly higher lower bound given as a replayable model file plus log and seed, and it does not ask for a new method. So an elementary method does not count against novelty here. Whether the argument is correct is for REPRODUCE to judge, not this report.

## Residual limits and disclosure
1. Disclosure the claim should add: CLAIM.md says each bound is strictly above the posted Best LB and every history bound. That is true, but it leaves out the higher MODAL bounds that the board does not show: Middle 6 39 and Late 9 5 (RobinX commit 7fb020cc6e, site files Bound_39 and Bound_5). The claim still holds against them. I recommend citing them so that no reader thinks 24 and 3 are the highest known bounds.
2. Not read (paywall or 403): the full Fonseca & Toffolo J. Sched. paper, the FBHS ORL paper, Rosati's thesis and his ESWA 2024 paper. If FBHS reported a proven global HAP-master bound of at least 40, 20 or 20 on Early 9, Middle 9 or Late 9, this verdict would change. Against that: its authors run the board and posted no such bound, and no later source cites one.
3. The board site may hold bound files that neither the board table nor GitHub lists. I cannot list that directory.
4. The search was in English and covered web, arXiv, PATAT, UGent biblio and GitHub. Unpublished theses or emails sent to the organisers cannot be ruled out.
5. In the GOAL repository logs, the "lb" values (490-1740) are subproblem objectives, not global bounds (they exceed known feasible penalties). Nobody should cite them as prior bounds above ours.

pass: true
