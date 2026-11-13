# FJSSP-W (flexible job shop with worker flexibility): 65 schedules below the published best makespan

## What
Against best_known.csv as re-fetched live at 2026-11-13T01:36:54Z (sha256 74f982d5..., byte-identical to the claim's copy), each of the 65 schedules in object/ is a feasible FJSSP-W schedule, under an independent checker, for its instance file in references/instances (identity matched to the repository's data.csv features; files not re-downloaded), with makespan at least 1 below the rounded listed UB of the table row mapped by data.csv name, so each row meets the bank's full success criterion and the set meets p1, p2 and p3; this says nothing about novelty against sources other than that table, about optimality, or about solver strength (five rows, behnkegeiger51 to 55, are also beaten by a trivial greedy).

65 instances of the FJSSP-W benchmark (jrc-rodec/FJSSP-W-Benchmarking): 60 found with a 300 s CP-SAT limit, 5 with 600 s (same solver otherwise). Each row meets the target's full success criterion on its own; together they also meet partial wins p1, p2 and p3. Three fresh AI-agent reviewers (reproduce, novelty, criterion) checked every row; see panel/.

| Table row | Listed UB | Ours | Saving | % | Group |
|---|---:|---:|---:|---:|---|
| behnkegeiger10 | 125 | 124 | 1 | 0.8 | 300s |
| behnkegeiger21 | 81 | 78 | 3 | 3.7 | 300s |
| behnkegeiger23 | 79 | 78 | 1 | 1.27 | 300s |
| behnkegeiger27 | 119 | 116 | 3 | 2.52 | 300s |
| behnkegeiger28 | 111 | 108 | 3 | 2.7 | 300s |
| behnkegeiger29 | 112 | 110 | 2 | 1.79 | 300s |
| behnkegeiger3 | 86 | 83 | 3 | 3.49 | 300s |
| behnkegeiger41 | 80 | 79 | 1 | 1.25 | 300s |
| behnkegeiger44 | 78 | 76 | 2 | 2.56 | 300s |
| behnkegeiger45 | 80 | 79 | 1 | 1.25 | 300s |
| behnkegeiger47 | 113 | 111 | 2 | 1.77 | 300s |
| behnkegeiger50 | 118 | 114 | 4 | 3.39 | 300s |
| brandimarte5 | 166 | 164 | 2 | 1.2 | 300s |
| chambersbarnes15 | 1163 | 1120 | 43 | 3.7 | 300s |
| chambersbarnes16 | 1155 | 1113 | 42 | 3.64 | 300s |
| chambersbarnes17 | 1153 | 1118 | 35 | 3.04 | 300s |
| chambersbarnes18 | 1091 | 1082 | 9 | 0.82 | 300s |
| chambersbarnes19 | 1060 | 1050 | 10 | 0.94 | 300s |
| chambersbarnes20 | 1143 | 1118 | 25 | 2.19 | 300s |
| chambersbarnes21 | 1094 | 1055 | 39 | 3.56 | 300s |
| chambersbarnes4 | 845 | 834 | 11 | 1.3 | 300s |
| dppaulli4 | 2520 | 2447 | 73 | 2.9 | 300s |
| fattahi20 | 1147 | 1123 | 24 | 2.09 | 300s |
| hurinkedata15 | 919 | 915 | 4 | 0.44 | 300s |
| hurinkedata24 | 990 | 977 | 13 | 1.31 | 300s |
| hurinkedata27 | 886 | 869 | 17 | 1.92 | 300s |
| hurinkedata28 | 891 | 881 | 10 | 1.12 | 300s |
| hurinkedata29 | 1101 | 1090 | 11 | 1.0 | 300s |
| hurinkedata30 | 1174 | 1157 | 17 | 1.45 | 300s |
| hurinkedata32 | 1104 | 1091 | 13 | 1.18 | 300s |
| hurinkedata39 | 1120 | 1115 | 5 | 0.45 | 300s |
| hurinkedata40 | 1317 | 1291 | 26 | 1.97 | 300s |
| hurinkedata41 | 1138 | 1111 | 27 | 2.37 | 300s |
| hurinkedata42 | 1133 | 1104 | 29 | 2.56 | 300s |
| hurinkedata43 | 1101 | 1069 | 32 | 2.91 | 300s |
| hurinkedata9 | 784 | 782 | 2 | 0.26 | 300s |
| hurinkrdata13 | 767 | 762 | 5 | 0.65 | 300s |
| hurinkrdata4 | 540 | 538 | 2 | 0.37 | 300s |
| hurinkrdata42 | 1004 | 979 | 25 | 2.49 | 300s |
| hurinkrdata44 | 908 | 892 | 16 | 1.76 | 300s |
| hurinkrdata5 | 500 | 498 | 2 | 0.4 | 300s |
| hurinkrdata50 | 5701 | 5651 | 50 | 0.88 | 300s |
| hurinkrdata52 | 6240 | 6193 | 47 | 0.75 | 300s |
| hurinkrdata6 | 458 | 454 | 4 | 0.87 | 300s |
| hurinkrdata7 | 479 | 474 | 5 | 1.04 | 300s |
| hurinkrdata9 | 765 | 763 | 2 | 0.26 | 300s |
| hurinksdata26 | 951 | 948 | 3 | 0.32 | 300s |
| hurinksdata29 | 1202 | 1132 | 70 | 5.82 | 300s |
| hurinksdata30 | 1192 | 1177 | 15 | 1.26 | 300s |
| hurinksdata31 | 1212 | 1148 | 64 | 5.28 | 300s |
| hurinksdata32 | 1146 | 1131 | 15 | 1.31 | 300s |
| hurinksdata33 | 1248 | 1240 | 8 | 0.64 | 300s |
| hurinksdata39 | 1192 | 1182 | 10 | 0.84 | 300s |
| hurinksdata40 | 1329 | 1285 | 44 | 3.31 | 300s |
| hurinksdata42 | 1168 | 1159 | 9 | 0.77 | 300s |
| hurinksdata43 | 1175 | 1137 | 38 | 3.23 | 300s |
| hurinksdata47 | 676 | 669 | 7 | 1.04 | 300s |
| hurinkvdata49 | 4740 | 4718 | 22 | 0.46 | 300s |
| hurinkvdata5 | 504 | 501 | 3 | 0.6 | 300s |
| hurinkvdata63 | 251 | 250 | 1 | 0.4 | 300s |
| behnkegeiger51 | 234 | 231 | 3 | 1.28 | 600s |
| behnkegeiger52 | 234 | 212 | 22 | 9.4 | 600s |
| behnkegeiger53 | 229 | 216 | 13 | 5.68 | 600s |
| behnkegeiger54 | 251 | 227 | 24 | 9.56 | 600s |
| behnkegeiger55 | 237 | 220 | 17 | 7.17 | 600s |

## Check it yourself
    sh verify-it-yourself/run_checks.sh
Expected last line: PASS. It checks each schedule's sha256, downloads each instance file from the organisers' repository at commit eb1d28381c34 (about 15 MB; not redistributed here), checks its sha256, validates the schedule (every operation once, allowed machine-worker pair with its duration, job order, machine and worker no-overlap) and compares the makespan with the listed UB. RUN_IT_YOURSELF.md has details; verify-it-yourself/RECEIPTS.md holds a real run.

## Compared to
best_known.csv of jrc-rodec/FJSSP-W-Benchmarking (https://raw.githubusercontent.com/jrc-rodec/FJSSP-W-Benchmarking/main/instances/InstanceData/FJSSP-W/best_known.csv), fetched 2026-11-13T01:12:05Z, sha256 74f982d5fdbdd7ebf6b889b0a57106474f9dd677a3813cf5762fc54afdfe30cf (the-record-we-beat/). Open pull request #868 (another contributor) covers 91 other rows; none of ours. An earlier 71-row version of this claim was narrowed to these rows because public results in the issue threads of jrc-rodec/FJSSP-W-Competition tie or beat ours on six other rows (behnkegeiger43, 56, 57, hurinksdata61, 63, hurinkedata6); those six are not claimed. The novelty reviewer's search of other public results and the literature is in panel/novelty.md.

## Not claimed
Optimality of any schedule; anything about instances not listed; the lower bounds; any claim about the solver as a new method (it is plain CP-SAT; how-we-built-it/ is provenance). Results are against the table as fetched; the table can move.

## Credits
Benchmark and table: Hutter, Steinberger and Hellwig (Josef Ressel Centre; jrc-rodec/FJSSP-W-Benchmarking; arXiv:2501.16159); the underlying FJSP instance families: Behnke and Geiger, Brandimarte, Chambers and Barnes, Dauzere-Peres and Paulli, Fattahi et al., Hurink et al., Kacem et al. Solver: Google OR-Tools CP-SAT. Search, claim and packaging: OrenSleepwalker with AI agents (Claude Code, Antigravity).
