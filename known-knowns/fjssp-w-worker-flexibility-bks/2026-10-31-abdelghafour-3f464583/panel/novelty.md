# Novelty review: fjssp-w-worker-flexibility-bks, partial win p2 (95 claimed instances)

context: subagent (Claude Code Agent tool, fresh context)
role: novelty skeptic. Input read: claim/ only (CLAIM.md, name_map.csv, best_known.csv, instances/, fjsspw_check.py).

## 1. Status table, fetched once
- URL: https://raw.githubusercontent.com/jrc-rodec/FJSSP-W-Benchmarking/main/instances/InstanceData/FJSSP-W/best_known.csv
- Command: `curl -sS -A 'V3R1T4S-research-agent (+https://github.com/elder-plinius/V3R1T4S)' -w '%{http_code}'` (one fetch, no retries)
- Fetch time (`date -u`): 2026-10-31T12:36:55Z. HTTP status: 200.
- sha256 of the fetched bytes: 74f982d5fdbdd7ebf6b889b0a57106474f9dd677a3813cf5762fc54afdfe30cf. This is identical to the scout's copy (claim/best_known.csv) and the scout's 10:24:20Z record, so the table had not changed.
- Procedure note: another process in the shared scratch area deleted the downloaded file before I parsed it. I did not re-fetch, because the rules allow no retries. The rows were read from claim/best_known.csv, which has the same sha256, so it is byte-for-byte the live response.
- Result: all 95 claimed makespans are strictly below round(UB) of their row (rows mapped through name_map.csv, columns read by header `Instance;UB;LB`). Each UB equals the "UB (rounded)" column in CLAIM.md, and no claimed value is below its LB. Live-table check: 95/95.

## 2. Sources checked for known values at or below a claimed makespan
| source | what was checked | finding |
|---|---|---|
| jrc-rodec/FJSSP-W-Benchmarking | all 8 historical versions of best_known.csv (035912b, 9462fca, 22e1c02, decf461, c5d3007, e8574fb, c894f27, fb2d06a; UB = max of the two columns, because of the pre-2026-04-27 header swap); repo tree (no results folder); releases (none); HEAD eb1d283 | no historical UB at or below any claim |
| arXiv:2501.16159 v1 (2025-01-27), v2 (2025-04-14), v3 (2026-05-05) | TeX sources of all versions, every table | only aggregate tables (collection statistics, solver averages, MiniZinc scores). No per-instance makespans |
| jrc-rodec/FJSSPW-GA (2025) | results/condensed_ga_results.json, solver_result/results_{cplex_cp,cplex_lp,hexaly,ortools}.txt (all 402 instances matched) | none at or below any claim |
| jrc-rodec/scheduling_model, FJSSP-W-Uncertainty-GECCO-Public | trees, result directories, best_known notebooks | no FJSSP-W per-instance values beyond the above |
| jrc-rodec/FJSSP-W-Competition (CEC/GECCO 2026) | 30 instances (5 identical by sha256 to claimed instances: ChambersBarnes10, Hurinkedata6, Hurinkrdata50, Hurinksdata61, Hurinksdata63); all 16 issues and their 13 submission archives (results CSV/JSON parsed only, no code run); PR #16 GECCO results poster (it says three prior best-knowns were improved) | see section 3 |
| ScheduleOpt/optalcp-benchmarks flexible-jobshop-w | README, model files, history to 2026-01-24 | data and model only, no results |
| Web search for other 2025-2026 FJSSP-W papers | two searches | no per-instance FJSSP-W results found beyond the above |
| elder-plinius/V3R1T4S | TROPHY_CASE.md (no FJSSP entry); known-knowns/ (no FJSSP entry); the target file in known-unknowns/ (no values); all 836 open and closed PR titles and bodies; PR search for fjssp, FJSSP-W, worker flexibility, hurink, jrc-rodec, makespan; file lists of the 145 PRs opened since 2026-10-25 (the target was added 2026-10-30) | no prior FJSSP-W claim |

## 3. Instances beaten or tied by a known value
- hurinksdata61, claimed 826: TIED by Yu Sun, TS-restart (Competition issue #11, 2026-05-10), makespan 826. The schedule passes the claim's checker. A tie is not a record.
- hurinksdata63, claimed 373: TIED by Yu Sun, TS-restart (issue #11), makespan 373. The schedule passes the checker. A tie is not a record. HUST OR team (#14) also reports 373, but that schedule fails the checker.
- hurinkedata6, claimed 537: HUST Operations Research and Optimization team (issue #14, 2026-05-30) REPORTS 533. Their schedule fails the claim's checker: worker no-overlap is broken 11 times. The conversion was confirmed on Yu Sun's schedules, which pass. Re-timing it while keeping its assignments gives 738. The reported value is not a valid published schedule, but I exclude the instance anyway.
- hurinkrdata50, claimed 5684: same team (#14) REPORTS 5681. The schedule fails the checker (11 worker overlaps), and re-timing gives 8000. Excluded on the same basis.
- ChambersBarnes10, claimed 855: best valid competition value is 856 (Yu Sun). The claim still beats it, by 1.
- All other instances: the best value found anywhere equals the live UB, or is worse. For example, the Haoxiang Qin competition run covers every claimed instance and none of its values is lower.

On trivial edits: the claim states its schedules came from CP-SAT from scratch, not seeded from a published schedule. The 91 survivors have no published schedule at or below them, so there is no published object whose deletion, relabelling, symmetry or polish could give these values.

## 4. Surviving set
Survivors: 91, counting only instances strictly below everything found and dropping the 2 ties and the 2 instances with lower reported values. It would be 93 if the two invalid HUST reports were ignored. Either count is at least the 10 that p2 requires.

hurinksdata6=573, hurinksdata55=6174, hurinkedata50=6067, hurinksdata51=7043, hurinkedata49=5956, hurinksdata53=7337, hurinkedata10=738, hurinkedata12=851, hurinkedata51=6494, hurinkedata11=813, hurinkrdata8=438, hurinkedata17=1071, hurinksdata56=7895, hurinkvdata7=480, hurinkvdata6=456, hurinkrdata49=4840, hurinkvdata50=5608, hurinkvdata8=437, hurinkvdata4=546, hurinkrdata51=5408, hurinkrdata53=5410, hurinkvdata51=5406, fattahi19=994, hurinksdata59=954, hurinksdata64=842, hurinksdata23=842, hurinksdata2=870, hurinksdata58=822, hurinksdata19=883, hurinksdata62=939, hurinksdata45=874, hurinksdata65=874, hurinksdata22=793, hurinksdata44=1132, hurinkedata58=810, hurinksdata60=935, hurinksdata57=1000, hurinksdata66=874, hurinkedata63=364, hurinkedata65=875, hurinkedata60=917, hurinkedata45=862, hurinkedata57=916, hurinkedata66=864, hurinkedata62=897, hurinkedata61=794, hurinkedata64=825, hurinkrdata56=5350, chambersbarnes6=863, hurinkedata59=889, chambersbarnes1=863, hurinkedata2=812, hurinkedata44=1086, brandimarte4=55, hurinkrdata54=5859, chambersbarnes7=840, chambersbarnes2=852, hurinksdata25=861, hurinksdata27=904, hurinksdata28=908, hurinksdata24=1000, chambersbarnes3=857, hurinkedata26=937, chambersbarnes5=789, chambersbarnes13=864, hurinkedata25=819, hurinkrdata20=592, chambersbarnes8=875, hurinkrdata60=692, hurinkrdata21=618, hurinkrdata64=590, hurinkrdata22=649, hurinkrdata65=657, hurinkrdata59=664, hurinkrdata2=640, hurinkrdata23=706, hurinkrdata57=704, hurinkrdata62=704, hurinkrdata66=701, chambersbarnes11=846, hurinkrdata63=281, chambersbarnes14=848, chambersbarnes9=860, hurinkvdata56=4223, chambersbarnes12=853, chambersbarnes10=855, hurinkvdata58=560, behnkegeiger5=84, behnkegeiger1=83, behnkegeiger4=88, behnkegeiger2=85

Not surviving: hurinksdata61 (tie), hurinksdata63 (tie), hurinkedata6 and hurinkrdata50 (lower values reported, schedules invalid, excluded to be safe).
Scope: novelty only. I did not re-run the 95 claimed schedules through the checker; that belongs to the reproduce panelist.

novelty: p2 holds with 91 surviving strict improvements (10 required).
pass: true
