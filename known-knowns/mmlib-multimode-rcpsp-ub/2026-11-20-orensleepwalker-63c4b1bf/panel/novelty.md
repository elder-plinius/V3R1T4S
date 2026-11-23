# Novelty review: 30 MMLIB+ upper-bound improvements (mmlib-multimode-rcpsp-ub)

context: fresh subagent started for this claim only

Reviewer role: NOVELTY skeptic. Inputs: claim/ only (CLAIM.md, target.md, object/schedules, evidence, data, code) plus live web. I did not modify claim/.

## Live fetches (each fetched once, plain GET, User-Agent `V3R1T4S-checker (+https://github.com/elder-plinius/V3R1T4S)`, no retries)

| UTC time | URL | HTTP | Bytes | Note |
|---|---|---|---|---|
| 2026-11-20T10:41:46Z | http://solutionsupdate.ugent.be/mrcpsp | 200 | 16738 | "Table - Best known results for MMRCPSP (September 2026)"; row "MMLIB MMplus 3240 1965 77.17% 14.7". Byte-identical to claim's data/mrcpsp.html (fetched 10:14:46Z). |
| 2026-11-20T10:41:46Z | http://solutionsupdate.ugent.be/sites/default/files/datasets/MMplus_2.csv | 200 | 531891 | Byte-identical to claim's data/MMplus_2.csv. |
| 2026-11-20T10:41:46Z | http://solutionsupdate.ugent.be/sites/default/files/datasets/MMplus_2_BKS.csv | 200 | 1034169 | Byte-identical to claim's data/MMplus_2_BKS.csv. |
| 2026-11-20T10:41:47Z | https://api.github.com/repos/MarioVanhoucke/MMLIB-Multi-Mode-Resource-Constrained-Project-Library/releases/latest | 200 | 4102 | tag v2.1, published 2026-06-23T09:34:11Z, single asset MMLIB_v2_1.zip (15742479 bytes, updated 2026-07-23T17:02:55Z); same as claim's data/release.json. UB-lit read from the claim's copy of that asset's Excel (sheet MMLIB+, column O). |
| 2026-11-20T10:43:54Z | https://zenodo.org/api/records/22261196 (Gippini, ref 6 on the dataset CSV) | 200 | - | plus its three files (README.md, MANIFEST.sha256, mmlib-deposit.zip), each 200 at 10:44:03-04Z |
| 2026-11-20T10:45:10Z | Ahmeti 2022 TU Wien dissertation PDF (repositum.tuwien.at bitstream 20.500.12708/20425) | 200 | 2078866 | |
| 2026-11-20T10:46:02Z | Etminaniesfahani 2024 UTS PhD thesis (opus.lib.uts.edu.au bitstream 10453/187477) | 200 | 3175302 | |

Blocks: one. link.springer.com/article/10.1007/s10732-024-09540-3 (Ahmeti & Musliu, J. Heuristics 31(1), 2025) answered 303 to the Springer login (idp.springer.com). I did not retry or get around it. See the residual risk below.

## Per-instance comparison

"Site UB" is UB value in MMplus_2.csv (with its UB ref; 8 = "Several authors, mmlib.eu, 2018", 7 = Shichen Tian 2026-09-03, 5 = Etminaniesfahani et al. 2024, 1 = Coelho & Vanhoucke). "BKS" is the Value in MMplus_2_BKS.csv. "UB-lit" comes from the v2.1 release Excel. The current public best is the minimum of the three. LB is the site LB (every claim is >= LB, so nothing is suspicious). Every schedule also passes the claim's checker (re-run by me: VALID at the claimed makespan). The other reviewers own the feasibility check.

| Instance | File | LB | Site UB (ref) | BKS | UB-lit | Current public best | Claimed | Seed | New? |
|---|---|---|---|---|---|---|---|---|---|
| 1238 | Jall248_3 | 40 | 51 (8) | 51 | 51 | 51 | 50 | scratch | new (-1) |
| 1767 | Jall354_2 | 30 | 32 (1) | 32 | 32 | 32 | 31 | posted | new (-1), see seeds |
| 1768 | Jall354_3 | 29 | 32 (1) | 32 | 32 | 32 | 31 | posted | new (-1), see seeds |
| 2161 | Jall433_1 | 66 | 73 (8) | 73 | 73 | 73 | 72 | scratch | new (-1) |
| 2170 | Jall434_5 | 47 | 54 (8) | 54 | 54 | 54 | 53 | scratch | new (-1) |
| 2177 | Jall436_2 | 44 | 51 (8) | 51 | 51 | 51 | 50 | scratch | new (-1) |
| 2178 | Jall436_3 | 51 | 58 (8) | 58 | 58 | 58 | 56 | scratch | new (-2) |
| 2180 | Jall436_5 | 47 | 54 (8) | 54 | 54 | 54 | 53 | scratch | new (-1) |
| 2223 | Jall445_3 | 68 | 76 (8) | 76 | 76 | 76 | 75 | scratch | new (-1) |
| 2299 | Jall460_4 | 59 | 69 (8) | 69 | 69 | 69 | 67 | scratch | new (-2) |
| 2446 | Jall490_1 | 62 | 77 (8) | 77 | 77 | 77 | 76 | scratch | new (-1) |
| 2450 | Jall490_5 | 64 | 76 (5) | 76 | 76 | 76 | 75 | posted | new (-1) |
| 2452 | Jall491_2 | 46 | 52 (8) | 52 | 52 | 52 | 51 | scratch | new (-1) |
| 2519 | Jall504_4 | 51 | 53 (8) | 53 | 53 | 53 | 52 | scratch | new (-1) |
| 2714 | Jall543_4 | 41 | 47 (8) | 47 | 47 | 47 | 46 | scratch | new (-1) |
| 2717 | Jall544_2 | 64 | 75 (7) | 75 | 76 | 75 | 74 | posted | new (-1) |
| 2774 | Jall555_4 | 42 | 51 (8) | 51 | 51 | 51 | 50 | scratch | new (-1) |
| 2841 | Jall569_1 | 79 | 92 (7) | 92 | 94 | 92 | 91 | posted | new (-1), see seeds |
| 2842 | Jall569_2 | 60 | 71 (8) | 71 | 71 | 71 | 69 | scratch | new (-2) |
| 2843 | Jall569_3 | 63 | 77 (7) | 77 | 79 | 77 | 76 | posted | new (-1), see seeds |
| 2846 | Jall570_1 | 50 | 58 (8) | 58 | 58 | 58 | 57 | scratch | new (-1) |
| 2850 | Jall570_5 | 48 | 56 (8) | 56 | 56 | 56 | 55 | scratch | new (-1) |
| 2854 | Jall571_4 | 66 | 79 (5) | 79 | 79 | 79 | 78 | posted | new (-1) |
| 2857 | Jall572_2 | 46 | 60 (8) | 60 | 60 | 60 | 59 | scratch | new (-1) |
| 2983 | Jall597_3 | 51 | 61 (8) | 61 | 61 | 61 | 60 | scratch | new (-1) |
| 2987 | Jall598_2 | 64 | 80 (8) | 80 | 80 | 80 | 78 | scratch | new (-2) |
| 2993 | Jall599_3 | 45 | 52 (8) | 52 | 52 | 52 | 51 | scratch | new (-1) |
| 3042 | Jall609_2 | 44 | 51 (8) | 51 | 51 | 51 | 50 | scratch | new (-1) |
| 3117 | Jall624_2 | 46 | 53 (7) | 53 | 54 | 53 | 52 | posted | new (-1) |
| 3122 | Jall625_2 | 72 | 84 (8) | 84 | 84 | 84 | 83 | scratch | new (-1) |

Total improvement: 34 units (26 instances by 1, 4 by 2). This matches CLAIM.md. All 30 are open on the site (LB < UB), and every claim is strictly below all three published values. None is a tie.

## Literature, code and repository search (last 24 months)

- **SolutionsUpdate record sets** in MMplus_2.csv: IDs 1-8. The newest are Gippini (2026-09-11), Shichen Tian (2026-09-03) and Etminaniesfahani et al. (submitted 2024/05). These are already in the values above.
- **Gippini Zenodo deposit 10.5281/zenodo.22261196** (v1.0, 2026-09-02/03): 81 instances. Its MMLIB+ entries are jall13, 15, 19, 20, 21, 59, 69, 168, 177 and 221. None of the 30 claimed instances is among them, and its only MMLIB+ schedule improvement is jall168_2.
- **Ahmeti 2022 dissertation (TU Wien)**: it names 64 Jall instances with new UBs (e.g. Jall64_4, Jall127_3, Jall556_2, Jall564_4, Jall619_2). None of the 30 claimed instances appears.
- **Etminaniesfahani 2024 UTS thesis**: it says it improved 614 MMLIB+ instances but gives no per-instance list. Those results are the site's ref 5 (submitted 2024/05), so they are already in the table.
- **Web searches** covered 2024-2026 MMLIB+ new upper bounds, Shichen Tian, Etminaniesfahani, Jall plus CP-SAT, and arXiv. Hits were Klein 2025 (Ann. Oper. Res., MILP formulations, reports gaps and claims no new UBs), Tian, Mei & Zhang (GP heuristics, no per-instance BKS), branch-and-price arXiv 2501.04563 (lower bounds, MMLIB50) and a 2026 IJPR RCPSP review. None reports a value at or below a claimed makespan for these instances.
- **MMLIB GitHub repository**: issues are enabled, with 0 issues ever (open or closed) and no PRs. The last push was 2026-07-23 (README only). The only release is v2.1, and its asset (updated 2026-07-23) is the one the claim uses. The repository tree has nothing newer than the release.
- **V3R1T4S repository** (elder-plinius/V3R1T4S): TROPHY_CASE.md (100 lines) has no MMLIB, MRCPSP, multi-mode, Jall or solutionsupdate entry. known-knowns/ has no MMLIB or RCPSP directory. PR and issue searches (all states) for MMLIB, MRCPSP, Jall and mmlib-multimode returned nothing. Hits for "multi-mode" are unrelated (polytopes, Voynich, Conway-99, a kit issue).

**Residual risk:** I could not read the full text of Ahmeti & Musliu, J. Heuristics 2025 (blocked by the Springer login). Its abstract mentions improved single-project multi-mode results. It follows on from the 2022 dissertation, whose MMLIB+ list contains none of these instances. I count it as not contradicting the claim, but I did not confirm this.

## Seeded objects (8 schedules warm-started from the posted BKS schedule)

The posted schedule comes from the BKS CSV row of the same instance (UB refs 1, 5 or 7). Each claim names its seed through `warm_start_from_posted_schedule` and CLAIM.md. Mode changes are versus the posted modes; the posted schedules re-check VALID at the posted value. The question is whether a trivial edit (re-timing the posted modes, a local polish) of the posted object already gives the claimed value.

I ran my own independent check: posted modes fixed, a pure single-mode RCPSP *decision* model (horizon equal to the claimed makespan, CP-SAT, 8 workers, 600 s).

| Instance | Modes changed | Author re-timing (best / bound) | My decision run at the claimed makespan | Verdict |
|---|---|---|---|---|
| 2450 Jall490_5 | 38/100 | 76 / 76 OPTIMAL | INFEASIBLE (proved, 0 s) | not a polish; new |
| 2717 Jall544_2 | 46/100 | 75 / 75 OPTIMAL | INFEASIBLE (proved) | not a polish; new |
| 2854 Jall571_4 | 41/100 | 79 / 79 OPTIMAL | INFEASIBLE (proved) | not a polish; new |
| 3117 Jall624_2 | 29/100 | 53 / 53 OPTIMAL | INFEASIBLE (proved) | not a polish; new |
| 1767 Jall354_2 | 18/100 | 32 / 26 (300 s) | UNKNOWN after 600 s | new, see note |
| 1768 Jall354_3 | 19/100 | 32 / 22 (300 s) | UNKNOWN after 600 s | new, see note |
| 2841 Jall569_1 | 37/100 | 92 / 90 (300 s) | UNKNOWN after 600 s | new, see note |
| 2843 Jall569_3 | 34/100 | 77 / 76 (300 s) | UNKNOWN after 600 s | new, see note |

**Note on the 4 undecided seeds.** None of the claimed objects is a trivial edit of its seed. Each re-assigns 18-37% of the activities' modes, which is a combinatorial change under the non-renewable budgets. That is not a deletion, restriction, propagation, relabelling, symmetry or local numerical polish. What re-timing the posted modes alone demonstrably gives is the posted value: the author's 60 s and 300 s runs and my independent 600 s decision run found no schedule at the claimed makespan. So the claimed value beats everything the trivial edits are known to give. It is not proved that re-timing alone can never reach it (no infeasibility proof for these four). If the lead requires a proof, these four, and only these four, would move to "not established".

For the 22 schedules built from scratch, the BKS CSV posts no schedule for any of them (their rows carry no Solution field; all are UB ref 8, the 2018 mmlib.eu import). So no published object exists to be edited. Their mode assignments cannot be compared to a posted one.

## Verdict

For all 30 instances, each claimed makespan is strictly below the current public best: dataset CSV UB, BKS CSV value and release UB-lit, re-fetched live at 2026-11-20T10:41:46Z. No 2024-2026 literature, deposit, repository issue, PR, TROPHY_CASE or known-knowns entry I found reports an equal or better value for any of them. No claimed schedule is a trivial edit of a published schedule. 4 of the 8 seeded claims are proved beyond posted-mode re-timing. The other 4 are not reached by re-timing under 900+ s of combined search, though this is not proved. Instances failing novelty: none.

novelty: PASS (30/30)

pass: true
