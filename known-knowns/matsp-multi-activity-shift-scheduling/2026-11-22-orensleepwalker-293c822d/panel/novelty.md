# Novelty review: matsp-optimality-certificate (94 instances, counting bound W - M)

context: fresh subagent started for this claim only

Reviewer role: NOVELTY skeptic. Inputs: claim/ (CLAIM.md, target.md, object/certificates.csv) plus the web. Nothing else in the workspace was read. claim/ was not modified.
Question: does any published source already state the optimal value, or a lower bound equal to the best known value, for any of the 94 claimed instances?

## Live fetches (each URL fetched once, plain request, UA "V3R1T4S-checker (+https://github.com/elder-plinius/V3R1T4S)", no retries)

| time (UTC) | URL | HTTP | bytes |
|---|---|---|---|
| 2026-11-22T08:56:16Z | https://www.schedulingbenchmarks.org/matsp/ | 200 | 75849 |
| 2026-11-22T08:56:17Z | https://www.schedulingbenchmarks.org/changes.html | 200 | 23627 |
| 2026-11-22T08:56:37Z | https://link.springer.com/article/10.1007/s10951-026-00886-z (article HTML) | 200 | 391177 |
| 2026-11-22T08:56:39Z | https://link.springer.com/content/pdf/10.1007/s10951-026-00886-z.pdf | 200 | 372149 |
| 2026-11-22T08:57:07Z | .../s10951-026-00886-z/tables/5 | 200 | 219203 |
| 2026-11-22T08:57:08Z | .../s10951-026-00886-z/tables/7 | 200 | 227172 |
| 2026-11-22T08:57:09Z | .../s10951-026-00886-z/tables/8 | 200 | 226851 |
| 2026-11-22T08:58:08Z | PATAT 2024 proceedings PDF (patatconference2024.dtu.dk) | 200 | 15959169 |
| 2026-11-22T09:01:52Z | https://www.schedulingbenchmarks.org/papers/VNS_for_MASSP.pdf | 200 | 438967 |

No fetch was blocked (no 403 or 429).

### Status table (matsp/)
- Columns: Instance, Days, Staff, Tasks, Best known, Reference. There is no lower-bound column, and the words "optimal" and "lower bound" do not appear anywhere on the page.
- Example rows: `1 7 10 1 383 TRA26`, `2 7 10 1 132 TRA26`, `8 7 20 2 763 TRA26`, `9 7 20 2 318 TRA26`, `10 7 20 3 59 TRA26`, `80 ... 6 TRA26`, `155 ... 24 TRA26`, `220 ... 10810 TRA26`, `225 ... 10866 TRA26`.
- I parsed all 225 rows; every one credits TRA26. For all 94 rows of object/certificates.csv, the live Best known equals the claimed `best_known` and `bound`, and `min_work_intervals - max_cover_total = bound`. Mismatches: 0.

### Changes page
- Newest entry is 29-Oct-2026 (nurse rostering history). The other entries after 01-Sep-2026 are 27-Oct, 21-Oct and 15-Oct (nurse rostering), 07-Oct (multi-activity command-line verifier) and 12-Sep (nurse Instance24 LB/UB).
- The only multi-activity results entry is 01-Sep-2026 (new solutions by Trautsch and Kovari). It contains no lower bounds or optimality statements.
- The page has no lower bounds for any multi-activity instance.

## TRA26 article (Trautsch and Kovari, J. Sched. 2026), checked row by row
- **Text, optimality statements:** "as was proven for problem instances 4, 77, and 78" and "SA was able to produce proven optimal solutions for instance 1 (with a cost of 383) and instance 5 (with a cost of 0)".
- **Table 5 (23 test instances):** gives CP LB/UB and IP LB/UB (1 h limits).
  - CP LB = UB, so proven optimal: inst 3 (274), 4 (304), 77 (775), 78 (581).
  - The proven set {1, 3, 4, 5, 77, 78} matches CLAIM.md, and none of these is among the 94.
- **Claimed instances that appear in Table 5:**
  - 9: CP LB 93, IP LB "-", best known 318
  - 50: CP LB 2, IP "-", best known 2100
  - 60: no LB, best known 2440
  - 89: CP LB 73, IP LB 1, best known 2136
  - 125, 194, 210, 215: no LB ("-"), best known 3998, 12584, 11076, 11408
  - In every case the published LB is absent or far below the claimed bound. The SA minima in Table 5 equal the claimed best known values.
- **Tables 7 and 8 (202 tuning instances):** columns are only VNS and SA long-run Min/Avg/Dev/t. They contain no lower bounds and no optimality marks.
- **Other claimed instances in Table 5's neighbourhood:** 7, 11, 17, 42, 47, 57, 68, 81, 143, 163 and 191 are not claimed. Their published LBs (e.g. 7: 669/727, 81: 1272/1510) are not tight.
- **Future work:** "experiment with alternative mathematical models to prove optimality for a larger number of problem instances". So the authors themselves treat the other instances as unproven.

## Other sources searched
- **PATAT 2024 version** ("A Simulated Annealing Approach to the Multi-Activity Multi-Day Shift Scheduling Problem", Trautsch and Kovari, proceedings pp. 125-138): I extracted the text. It has VNS vs SA tables only. The only use of "optimal" is a remark that a block-count parameter below 10 may make the optimum unreachable. It has no lower bounds.
- **Qu and Curtois, ICORES 2020** (VNS_for_MASSP.pdf; scitepress HTML version read via a web fetch): it reports no lower bounds and no proven optima. It says only that "at least three of the instances have zero cost solutions", without naming them, and no claimed instance has best known 0 (the minimum claimed best known is 59).
- **Status page link to "an initial set of results and an integer programming model":** it is commented out in the page source and points to the nurse-rostering paper and solutions (instances1_24solutions). It is not a multi-activity result.
- **TRA26 code, github.com/trautschlaci/massp_sa** (via gh API):
  - Last push 2025-09-10. It has no releases, no tags and one branch (main).
  - The tree holds sources (SA, CP-SAT and Gurobi model code), README and best_solutions/*.xml. There is no lower-bound or certificate file, and the README does not mention bounds or optimality.
- **Citing works (OpenAlex):**
  - TRA26 has 0 citations.
  - Works citing Qu-Curtois 2020: Shariat and Huang, J. Heuristics 2024 (LNS for multi-activity tour scheduling; industrial and random instances, heuristic). A 2026 Polytechnique Montreal thesis on ML for personnel scheduling (own retail instances). A 2020 nurse-rostering paper and an unrelated transport paper.
  - None gives bounds for the Curtois-Qu instances.
- **OpenAlex search** "multi-activity shift scheduling" since 2024-11: the only hit on this benchmark is TRA26.
- **Web searches** (standard and extended) for lower bounds or optimal values on the Curtois-Qu / schedulingbenchmarks MATSP instances in 2024-2026: nothing beyond TRA26.
- **GitHub repo search** ("multi-activity shift scheduling", matsp, massp, schedulingbenchmarks): two unrelated heuristic repos (an LNS for tour scheduling from 2024 and a 2023 SA thesis project). Neither has bounds for these instances.
- **V3R1T4S repository (elder-plinius/V3R1T4S):**
  - TROPHY_CASE.md: no entry for matsp, shift scheduling or multi-activity.
  - known-knowns/ (7404 paths): nothing for matsp or shift scheduling. The only matsp file in the tree is the known-unknowns target.
  - Open and closed PRs and issues, searched for matsp, shift, multi-activity, curtois, TRA26, schedulingbenchmarks and optimality-certificate: only #1215 (instance 80, roster penalty 0) and #1216 (instance 155, roster penalty 0). These are this team's upper-bound claims, not lower bounds, and neither instance is among the 94.

## Comparison against the trivial-edit rule
- The claimed object is a lower bound equal to the best known value. The strongest published lower bounds for these cells are the TRA26 CP/IP bounds, which exist for at most 4 of the 94 (9, 50, 89, plus 60/125/194/210/215 with none). The claimed bounds strictly beat them, e.g. 318 vs 93, 2100 vs 2, 2136 vs 73.
- No published object for these 94 cells (relabelled, restricted or otherwise) gives a matching bound, and no source states their optimality.
- The six instances that are already proven optimal (1, 3, 4, 5, 77, 78) are correctly excluded.

## Already proven optimal elsewhere among the 94
None. I found no published source that proves any of the 94 claimed instances optimal.

## Scope note
This review covers novelty only. I did not check whether the W - M argument is valid or whether the instance arithmetic is correct; those belong to the other panel members.

novelty: CONFIRMED (no published optimal value or matching lower bound for any of the 94; status source read live, HTTP 200)
pass: true
