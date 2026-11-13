# Criterion skeptic report: claim-v2 (FJSSP-W, 65 rows)

context: started cold as the CRITERION skeptic of a three-person panel, from a brief file only; read only files inside the claim folder (claim-v2/) plus the bank entry `fjssp-w-worker-flexibility-bks` in repo/bank/targets.json; fetched the live best_known.csv URL once; wrote only to panel-v2/work-criterion/ and this file; Python 3 standard library only, run with -I and PYTHONDONTWRITEBYTECODE=1.

## What was checked, and how

All scripts are in panel-v2/work-criterion/ (check.py, mapping.py, features.py, claimtable.py, prov.py, mutate.py, tinytest.py, nullgreedy.py; outputs results.json, null_greedy.json, rowtable.md, live_best_known.csv).

1. **Criterion text.** criterion.txt contains the bank's success criterion and partial wins p1, p2, p3 verbatim (string-checked against targets.json).
2. **Independent checker** (check.py), written from the bank's instance format before reading provenance/code. It parses each instance two ways (line per job, and one token stream) and requires both to agree and to consume the file exactly. All 65 headers have exactly three numbers. For each schedule it checks: six integers per op; each (job, op) present exactly once; (machine, worker) eligible for that op; duration equal to that pair's duration (no op has two durations for one pair); start >= 0; job precedence; no overlap on any machine or any worker (half-open intervals); makespan = latest end. The `instance` field must equal the file name, with no other keys.
   - Validated on a hand-built 2-job, 2-machine, 2-worker instance (work-criterion/tiny/T.fjs). A valid schedule passes with makespan 7. An ineligible pair, a machine overlap and a pure worker overlap are each rejected.
   - Also validated by mutating a real claimed schedule (Behnke21): a dropped op, a duplicated op, a duration off by 1, worker 99, a precedence violation and a machine overlap are all detected.
3. **Table.** references/best_known.csv has header `Instance;UB;LB` and 402 rows; columns were read by header. UB >= LB on every row. UB was rounded to the nearest integer. None of the 65 claimed rows has float noise on its UB (three have noise on LB only: brandimarte5, hurinkedata24, hurinksdata31). A row passes only if makespan <= round(UB) - 1.
4. **Live re-fetch.** I fetched https://raw.githubusercontent.com/jrc-rodec/FJSSP-W-Benchmarking/main/instances/InstanceData/FJSSP-W/best_known.csv once, at 2026-11-13T01:36:54Z: HTTP 200, sha256 74f982d5fdbdd7ebf6b889b0a57106474f9dd677a3813cf5762fc54afdfe30cf. It is byte-identical to references/best_known.csv and to the hash in status/table-fetch.txt (fetched 2026-11-13T01:12:05Z). The "re-fetched live immediately before claiming" clause holds.
5. **Instance membership and row mapping.** references/data.csv has 402 rows with 402 unique `source` names, and all 65 files are among them. Lower-casing plus two renames (Behnke -> behnkegeiger, BrandimarteMk -> brandimarte) gives an exact bijection between the 402 data.csv names and the 402 table names. Family counts agree (60 Behnke, 15 Brandimarte, 21 ChambersBarnes, 18 DPpaulli, 20 Fattahi, 4 x 66 Hurink, 4 Kacem). references/row_to_file.json agrees with this mapping on all 65 rows. The two files are not in the same row order, so mapping by position would be wrong; the claim does not do that.
6. **Instance identity.** All 65 instance files match references/instances.sha256 and the instance_sha256 column of provenance/rows.csv. Independently, each file's n_jobs, n_machines, n_worker, n_operations, d_max, d_min and d_distinct match its data.csv row exactly, and d_average matches to 1e-6 (65 of 65). This shows the files are the repository's instances, not regenerated ones (the bank's first pitfall). Limitation: I did not re-download the instance files or data.csv from GitHub; identity rests on the local copies and this feature match.
7. **CLAIM.md table.** All 65 rows match my recomputation: file, rounded UB, makespan, saving and percentage. No makespan is below the table's LB.
8. **Partial wins** (by family of the 65 passing rows): 17 behnkegeiger, 1 brandimarte, 8 chambersbarnes, 1 dppaulli, 1 fattahi, 37 Hurink (13 e, 10 r, 11 s, 3 v). Every claimed row has round(UB) > round(LB).
   - p1 holds (18 Behnke/Brandimarte rows with UB > LB).
   - p2 holds (65 distinct instances, at least 10 needed).
   - p3 holds (37 Hurink rows, 1 DPpaulli and 8 ChambersBarnes rows).
   - The full criterion is met separately for each row, and it subsumes p1 to p3. So the full criterion is the operative level, not a partial win.
9. **Hidden quantifiers and definitions.**
   - "Strictly below" is read as at least 1 below the rounded UB. Five rows win by exactly 1 (behnkegeiger10, 23, 41, 45, hurinkvdata63); makespans are integers, so these are strict.
   - hurinkvdata63's makespan of 250 equals the listed LB, which is consistent and makes it optimal.
   - behnkegeiger21 has LB 0 (a trivial bound); this does not matter, because only the UB counts.
   - The criterion says "for one of the 402 instances"; the claim asserts it separately per row and does not pool rows.
   - "Nothing is submitted by the agent": nothing in the claim folder says anything was submitted. PR #868 is only referenced as an exclusion list, and the competition issue threads only as a novelty source.

## Per-row results (all 65 hold; none fail)

| Table row | File | UB raw | UB rounded | LB raw | Ops | Checker | Makespan | Saving | UB>LB | Row passes |
|---|---|---:|---:|---:|---:|---|---:|---:|---|---|
| behnkegeiger10 | Behnke10 | 125.0 | 125 | 75.0 | 100 | valid | 124 | 1 | yes | yes |
| behnkegeiger21 | Behnke21 | 81.0 | 81 | 0.0 | 50 | valid | 78 | 3 | yes | yes |
| behnkegeiger23 | Behnke23 | 79.0 | 79 | 66.0 | 50 | valid | 78 | 1 | yes | yes |
| behnkegeiger27 | Behnke27 | 119.0 | 119 | 74.0 | 100 | valid | 116 | 3 | yes | yes |
| behnkegeiger28 | Behnke28 | 111.0 | 111 | 66.0 | 100 | valid | 108 | 3 | yes | yes |
| behnkegeiger29 | Behnke29 | 112.0 | 112 | 67.0 | 100 | valid | 110 | 2 | yes | yes |
| behnkegeiger3 | Behnke3 | 86.0 | 86 | 72.0 | 50 | valid | 83 | 3 | yes | yes |
| behnkegeiger41 | Behnke41 | 80.0 | 80 | 62.0 | 50 | valid | 79 | 1 | yes | yes |
| behnkegeiger44 | Behnke44 | 78.0 | 78 | 61.0 | 50 | valid | 76 | 2 | yes | yes |
| behnkegeiger45 | Behnke45 | 80.0 | 80 | 62.0 | 50 | valid | 79 | 1 | yes | yes |
| behnkegeiger47 | Behnke47 | 113.0 | 113 | 68.0 | 100 | valid | 111 | 2 | yes | yes |
| behnkegeiger50 | Behnke50 | 118.0 | 118 | 66.0 | 100 | valid | 114 | 4 | yes | yes |
| brandimarte5 | BrandimarteMk5 | 166.0 | 166 | 57.99999999999886 | 106 | valid | 164 | 2 | yes | yes |
| chambersbarnes15 | ChambersBarnes15 | 1163.0 | 1163 | 885.0 | 225 | valid | 1120 | 43 | yes | yes |
| chambersbarnes16 | ChambersBarnes16 | 1155.0 | 1155 | 879.0 | 225 | valid | 1113 | 42 | yes | yes |
| chambersbarnes17 | ChambersBarnes17 | 1153.0 | 1153 | 873.0 | 225 | valid | 1118 | 35 | yes | yes |
| chambersbarnes18 | ChambersBarnes18 | 1091.0 | 1091 | 879.0 | 225 | valid | 1082 | 9 | yes | yes |
| chambersbarnes19 | ChambersBarnes19 | 1060.0 | 1060 | 881.0 | 225 | valid | 1050 | 10 | yes | yes |
| chambersbarnes20 | ChambersBarnes20 | 1143.0 | 1143 | 892.0 | 225 | valid | 1118 | 25 | yes | yes |
| chambersbarnes21 | ChambersBarnes21 | 1094.0 | 1094 | 882.0 | 225 | valid | 1055 | 39 | yes | yes |
| chambersbarnes4 | ChambersBarnes4 | 845.0 | 845 | 617.0 | 100 | valid | 834 | 11 | yes | yes |
| dppaulli4 | DPpaulli4 | 2520.0 | 2520 | 1289.0 | 196 | valid | 2447 | 73 | yes | yes |
| fattahi20 | Fattahi20 | 1147.0 | 1147 | 880.0 | 48 | valid | 1123 | 24 | yes | yes |
| hurinkedata15 | Hurinkedata15 | 919.0 | 919 | 397.0 | 100 | valid | 915 | 4 | yes | yes |
| hurinkedata24 | Hurinkedata24 | 990.0 | 990 | 664.9999999999982 | 150 | valid | 977 | 13 | yes | yes |
| hurinkedata27 | Hurinkedata27 | 886.0 | 886 | 663.0 | 150 | valid | 869 | 17 | yes | yes |
| hurinkedata28 | Hurinkedata28 | 891.0 | 891 | 676.0 | 150 | valid | 881 | 10 | yes | yes |
| hurinkedata29 | Hurinkedata29 | 1101.0 | 1101 | 653.0 | 200 | valid | 1090 | 11 | yes | yes |
| hurinkedata30 | Hurinkedata30 | 1174.0 | 1174 | 630.0 | 200 | valid | 1157 | 17 | yes | yes |
| hurinkedata32 | Hurinkedata32 | 1104.0 | 1104 | 675.0 | 200 | valid | 1091 | 13 | yes | yes |
| hurinkedata39 | Hurinkedata39 | 1120.0 | 1120 | 878.0 | 225 | valid | 1115 | 5 | yes | yes |
| hurinkedata40 | Hurinkedata40 | 1317.0 | 1317 | 902.0 | 225 | valid | 1291 | 26 | yes | yes |
| hurinkedata41 | Hurinkedata41 | 1138.0 | 1138 | 872.0 | 225 | valid | 1111 | 27 | yes | yes |
| hurinkedata42 | Hurinkedata42 | 1133.0 | 1133 | 847.0 | 225 | valid | 1104 | 29 | yes | yes |
| hurinkedata43 | Hurinkedata43 | 1101.0 | 1101 | 872.0 | 225 | valid | 1069 | 32 | yes | yes |
| hurinkedata9 | Hurinkedata9 | 784.0 | 784 | 431.0 | 75 | valid | 782 | 2 | yes | yes |
| hurinkrdata13 | Hurinkrdata13 | 767.0 | 767 | 415.0 | 75 | valid | 762 | 5 | yes | yes |
| hurinkrdata4 | Hurinkrdata4 | 540.0 | 540 | 378.0 | 50 | valid | 538 | 2 | yes | yes |
| hurinkrdata42 | Hurinkrdata42 | 1004.0 | 1004 | 842.0 | 225 | valid | 979 | 25 | yes | yes |
| hurinkrdata44 | Hurinkrdata44 | 908.0 | 908 | 780.0 | 100 | valid | 892 | 16 | yes | yes |
| hurinkrdata5 | Hurinkrdata5 | 500.0 | 500 | 367.0 | 50 | valid | 498 | 2 | yes | yes |
| hurinkrdata50 | Hurinkrdata50 | 5701.0 | 5701 | 2828.0 | 52 | valid | 5651 | 50 | yes | yes |
| hurinkrdata52 | Hurinkrdata52 | 6240.0 | 6240 | 2824.0 | 56 | valid | 6193 | 47 | yes | yes |
| hurinkrdata6 | Hurinkrdata6 | 458.0 | 458 | 326.0 | 50 | valid | 454 | 4 | yes | yes |
| hurinkrdata7 | Hurinkrdata7 | 479.0 | 479 | 339.0 | 50 | valid | 474 | 5 | yes | yes |
| hurinkrdata9 | Hurinkrdata9 | 765.0 | 765 | 391.0 | 75 | valid | 763 | 2 | yes | yes |
| hurinksdata26 | Hurinksdata26 | 951.0 | 951 | 595.0 | 150 | valid | 948 | 3 | yes | yes |
| hurinksdata29 | Hurinksdata29 | 1202.0 | 1202 | 670.0 | 200 | valid | 1132 | 70 | yes | yes |
| hurinksdata30 | Hurinksdata30 | 1192.0 | 1192 | 628.0 | 200 | valid | 1177 | 15 | yes | yes |
| hurinksdata31 | Hurinksdata31 | 1212.0 | 1212 | 706.999999999 | 200 | valid | 1148 | 64 | yes | yes |
| hurinksdata32 | Hurinksdata32 | 1146.0 | 1146 | 686.0 | 200 | valid | 1131 | 15 | yes | yes |
| hurinksdata33 | Hurinksdata33 | 1248.0 | 1248 | 665.0 | 200 | valid | 1240 | 8 | yes | yes |
| hurinksdata39 | Hurinksdata39 | 1192.0 | 1192 | 871.0 | 225 | valid | 1182 | 10 | yes | yes |
| hurinksdata40 | Hurinksdata40 | 1329.0 | 1329 | 914.0 | 225 | valid | 1285 | 44 | yes | yes |
| hurinksdata42 | Hurinksdata42 | 1168.0 | 1168 | 870.0 | 225 | valid | 1159 | 9 | yes | yes |
| hurinksdata43 | Hurinksdata43 | 1175.0 | 1175 | 875.0 | 225 | valid | 1137 | 38 | yes | yes |
| hurinksdata47 | Hurinksdata47 | 676.0 | 676 | 412.0 | 300 | valid | 669 | 7 | yes | yes |
| hurinkvdata49 | Hurinkvdata49 | 4740.0 | 4740 | 2814.0 | 55 | valid | 4718 | 22 | yes | yes |
| hurinkvdata5 | Hurinkvdata5 | 504.0 | 504 | 372.0 | 50 | valid | 501 | 3 | yes | yes |
| hurinkvdata63 | Hurinkvdata63 | 251.0 | 251 | 250.0 | 99 | valid | 250 | 1 | yes | yes |
| behnkegeiger51 | Behnke51 | 234.0 | 234 | 69.0 | 250 | valid | 231 | 3 | yes | yes |
| behnkegeiger52 | Behnke52 | 234.0 | 234 | 69.0 | 250 | valid | 212 | 22 | yes | yes |
| behnkegeiger53 | Behnke53 | 229.0 | 229 | 67.0 | 250 | valid | 216 | 13 | yes | yes |
| behnkegeiger54 | Behnke54 | 251.0 | 251 | 68.0 | 250 | valid | 227 | 24 | yes | yes |
| behnkegeiger55 | Behnke55 | 237.0 | 237 | 69.0 | 250 | valid | 220 | 17 | yes | yes |

## Null model (randomized greedy)

nullgreedy.py is a naive randomized greedy list scheduler: at each step it appends the (job, pair) with the earliest finish time plus noise. It ran 30 restarts per instance, seed 1, taking seconds per instance, and every schedule it produced is valid under my checker.
- **60 rows:** greedy ends well above the listed UB (for example hurinkedata28: greedy 1381, UB 891, claim 881). The claimed improvement is not something a trivial heuristic gives.
- **5 rows** (the whole "600s" group): greedy beats the listed UB, and it also beats the claimed schedule:

| Row | UB | Claim | Greedy |
|---|---:|---:|---:|
| behnkegeiger51 | 234 | 231 | 219 |
| behnkegeiger52 | 234 | 212 | 209 |
| behnkegeiger53 | 229 | 216 | 213 |
| behnkegeiger54 | 251 | 227 | 221 |
| behnkegeiger55 | 237 | 220 | 212 |

These five rows still meet the criterion literally, because it asks only for a feasible schedule strictly below the listed UB. But their listed UBs are weak: a trivial greedy undercuts them, and the claimed CP-SAT schedules are not even as good as that greedy. Any statement that these rows show solver strength would be unsupported. CLAIM.md makes no such statement: it says "Not claimed: optimality ... any statement about the solver as a method beyond provenance". So this is a caveat, not a failure.

## Wording and misleading content

- CLAIM.md's one-sentence claim is scoped to "the rounded upper bound (UB) the table lists" and to the stated table fetch. It disclaims optimality and the LB column, and names the six rows removed since version 1 and why.
- The panel brief paraphrases the claim as beating "the published best makespan". CLAIM.md itself claims only the table UB. Version 1 showed that better public values exist outside the table for some rows (FJSSP-W-Competition issue threads, PR #868). Whether any of the 65 remaining rows is matched or beaten by such sources is a novelty question outside the literal criterion. I did not check it (outside my read scope); the novelty skeptic should.
- Minor, not misleading: provenance/README.md still says "How the 71 schedules were produced" (version 1 count), but its last bullet explains version 2.
- Minor, disclosed: the null-test line in provenance/preregistrations/2026-11-12-1955.md was added after the run as a dated amendment.
- Minor, disclosed: run 2026-11-12-1335 had two post-deadline reruns (behnkegeiger31, behnkegeiger40); neither is a claimed row.

## Provenance (cherry-picking check)

- The run reports plus run-2026-11-12-0020-all-attempts.csv list 280 distinct attempted rows. These are all open rows (UB > LB) not in PR #868: 10 + 135 + 28 + 27 + 66 + 9 + 5, plus the stopped stage-2 run.
- They report 71 wins. The 65 claimed rows are exactly those 71 minus the six removed rows named in CLAIM.md. Every claimed row appears as a win in a report, with the same UB and makespan.
- The 0020 attempts CSV has 135 rows, of which 32 improved. The improved flag is consistent with the live table for every row, and no UB changed between the runs and the live table.
- provenance/rows.csv has the same 65 rows; object sha256, instance sha256, makespan and UB all match. For OPTIMAL rows the solver bound equals the makespan, and no bound exceeds the makespan.
- Misses and ties are reported. Because each row is an explicit, checkable schedule, selection among rows cannot inflate any single row's result. Nothing in provenance/ undermines the claim.

## Verdict

- Every clause of the bank's success criterion holds for every one of the 65 rows: the instance is among the 402, the mapping is confirmed from data.csv names, the schedule is feasible under an independent checker, its makespan is at least 1 below the rounded UB, and the table is unchanged on a live re-fetch.
- p1, p2 and p3 follow.
- Caveats:
  - The five "600s" rows (behnkegeiger51 to 55) have listed UBs that a trivial greedy also beats, by more than the claim does.
  - Novelty against sources other than best_known.csv was not checked here.
  - Instance files and data.csv were not re-downloaded.
- No row fails.

confirmed_scope: Against best_known.csv as re-fetched live at 2026-11-13T01:36:54Z (sha256 74f982d5..., byte-identical to the claim's copy), each of the 65 schedules in object/ is a feasible FJSSP-W schedule, under an independent checker, for its instance file in references/instances (identity matched to the repository's data.csv features; files not re-downloaded), with makespan at least 1 below the rounded listed UB of the table row mapped by data.csv name, so each row meets the bank's full success criterion and the set meets p1, p2 and p3; this says nothing about novelty against sources other than that table, about optimality, or about solver strength (five rows, behnkegeiger51 to 55, are also beaten by a trivial greedy).

pass: true
