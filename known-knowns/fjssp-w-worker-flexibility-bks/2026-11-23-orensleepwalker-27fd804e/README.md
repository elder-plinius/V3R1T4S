# FJSSP-W (flexible job shop with worker flexibility): 136 schedules below the published best makespan

## What
For each of the 136 listed FJSSP-W instances (34 Behnke, 7 Brandimarte, 16 Dauzere-Peres-Paulli, 13 Hurink edata, 30 rdata, 5 sdata and 31 vdata), the schedule in object/<file>.json passes independently written checkers against the byte-identical upstream instance file and has a makespan at least 1 below the rounded UB in the best_known.csv fetched live on 2026-11-23 (sha256 74f982d5...30cf, unchanged at 19:34:00Z), so each meets the full criterion separately and the set meets p1, p2 and p3; nothing is confirmed about optimality or about any public competition value.

136 instances of the FJSSP-W benchmark (jrc-rodec/FJSSP-W-Benchmarking): 34 Behnke, 31 Hurinkvdata, 30 Hurinkrdata, 16 DPpaulli, 13 Hurinkedata, 7 BrandimarteMk, 5 Hurinksdata. Each row meets the target's full success criterion on its own (a checker-valid schedule with makespan at least 1 below the table's rounded UB); together they meet partial wins p1, p2 and p3. Total 1367 time units below the listed UBs; 56 rows are exactly 1 below, the largest saving is 85.

The two "public" columns give the closest public result the authors found for each row: a published competition or solver schedule re-timed with the instance's own durations, and the lowest value a competition team reported (the-record-we-beat/public-results-screen.txt). Every row is below both. On six large Behnke rows a GECCO 2026 competition submission is already below the table (Behnke39, 56, 57, 58, 59: Haoxiang Qin et al.; Behnke60: Yu Sun and the HUST SMART Lab Team2), and our schedules are below those too.

| Table row | Listed UB | Closest public schedule (re-timed) | Lowest public reported value | Ours | Below UB by |
|---|---:|---:|---:|---:|---:|
| behnkegeiger11 | 228 | 228 | 228 | 224 | 4 |
| behnkegeiger12 | 223 | 223 | 223 | 221 | 2 |
| behnkegeiger13 | 234 | 234 | 234 | 233 | 1 |
| behnkegeiger14 | 238 | 238 | 238 | 237 | 1 |
| behnkegeiger15 | 233 | 233 | 233 | 230 | 3 |
| behnkegeiger16 | 416 | 416 | 416 | 406 | 10 |
| behnkegeiger17 | 402 | 402 | 402 | 400 | 2 |
| behnkegeiger18 | 399 | 399 | 399 | 390 | 9 |
| behnkegeiger19 | 397 | 397 | 397 | 390 | 7 |
| behnkegeiger20 | 403 | 403 | 403 | 389 | 14 |
| behnkegeiger26 | 107 | 107 | 107 | 106 | 1 |
| behnkegeiger30 | 114 | 114 | 114 | 113 | 1 |
| behnkegeiger31 | 226 | 226 | 226 | 225 | 1 |
| behnkegeiger32 | 218 | 218 | 218 | 217 | 1 |
| behnkegeiger33 | 219 | 219 | 219 | 213 | 6 |
| behnkegeiger34 | 213 | 213 | 213 | 210 | 3 |
| behnkegeiger35 | 208 | 208 | 208 | 204 | 4 |
| behnkegeiger36 | 423 | 423 | 423 | 395 | 28 |
| behnkegeiger37 | 419 | 419 | 419 | 393 | 26 |
| behnkegeiger38 | 419 | 419 | 419 | 392 | 27 |
| behnkegeiger39 | 435 | 426 | 426 | 403 | 32 |
| behnkegeiger40 | 441 | 441 | 441 | 420 | 21 |
| behnkegeiger46 | 108 | 107 | 107 | 106 | 2 |
| behnkegeiger48 | 117 | 117 | 117 | 116 | 1 |
| behnkegeiger49 | 107 | 107 | 107 | 106 | 1 |
| behnkegeiger56 | 474 | 408 | 408 | 395 | 79 |
| behnkegeiger57 | 476 | 425 | 425 | 391 | 85 |
| behnkegeiger58 | 445 | 416 | 416 | 401 | 44 |
| behnkegeiger59 | 429 | 414 | 414 | 392 | 37 |
| behnkegeiger6 | 117 | 117 | 117 | 116 | 1 |
| behnkegeiger60 | 431 | 370 | 370 | 369 | 62 |
| behnkegeiger7 | 119 | 119 | 119 | 118 | 1 |
| behnkegeiger8 | 119 | 119 | 119 | 118 | 1 |
| behnkegeiger9 | 121 | 121 | 121 | 120 | 1 |
| brandimarte10 | 199 | 199 | 199 | 194 | 5 |
| brandimarte11 | 586 | 586 | 586 | 584 | 2 |
| brandimarte13 | 402 | 402 | 402 | 374 | 28 |
| brandimarte15 | 328 | 328 | 328 | 320 | 8 |
| brandimarte2 | 26 | 26 | 26 | 25 | 1 |
| brandimarte6 | 58 | 58 | 58 | 57 | 1 |
| brandimarte7 | 137 | 137 | 137 | 136 | 1 |
| dppaulli10 | 2343 | 2343 | 2343 | 2334 | 9 |
| dppaulli11 | 1991 | 1991 | 1991 | 1980 | 11 |
| dppaulli12 | 1971 | 1971 | 1971 | 1947 | 24 |
| dppaulli13 | 2302 | 2302 | 2302 | 2229 | 73 |
| dppaulli14 | 2084 | 2084 | 2084 | 2076 | 8 |
| dppaulli15 | 2071 | 2050 | 2050 | 2036 | 35 |
| dppaulli16 | 2325 | 2325 | 2325 | 2314 | 11 |
| dppaulli17 | 2084 | 2084 | 2084 | 2044 | 40 |
| dppaulli18 | 2069 | 2035 | 2035 | 2028 | 41 |
| dppaulli2 | 2224 | 2224 | 2224 | 2216 | 8 |
| dppaulli3 | 2148 | 2148 | 2148 | 2131 | 17 |
| dppaulli5 | 2194 | 2194 | 2194 | 2178 | 16 |
| dppaulli6 | 2141 | 2141 | 2141 | 2123 | 18 |
| dppaulli7 | 2350 | 2350 | 2350 | 2349 | 1 |
| dppaulli8 | 2003 | 2003 | 2003 | 1990 | 13 |
| dppaulli9 | 1968 | 1968 | 1968 | 1959 | 9 |
| hurinkedata14 | 1058 | 1058 | 1058 | 1057 | 1 |
| hurinkedata18 | 1065 | 1065 | 1065 | 1064 | 1 |
| hurinkedata3 | 1055 | 1055 | 1055 | 1054 | 1 |
| hurinkedata31 | 1128 | 1128 | 1128 | 1127 | 1 |
| hurinkedata33 | 1191 | 1191 | 1191 | 1190 | 1 |
| hurinkedata34 | 1528 | 1528 | 1528 | 1527 | 1 |
| hurinkedata35 | 1644 | 1644 | 1644 | 1628 | 16 |
| hurinkedata36 | 1498 | 1498 | 1498 | 1497 | 1 |
| hurinkedata37 | 1580 | 1580 | 1580 | 1579 | 1 |
| hurinkedata38 | 1665 | 1665 | 1665 | 1613 | 52 |
| hurinkedata46 | 623 | 623 | 623 | 621 | 2 |
| hurinkedata47 | 635 | 635 | 635 | 634 | 1 |
| hurinkedata48 | 627 | 627 | 627 | 626 | 1 |
| hurinkrdata10 | 711 | 711 | 711 | 710 | 1 |
| hurinkrdata11 | 726 | 726 | 726 | 725 | 1 |
| hurinkrdata12 | 809 | 809 | 809 | 808 | 1 |
| hurinkrdata14 | 1018 | 1018 | 1018 | 1017 | 1 |
| hurinkrdata15 | 887 | 887 | 887 | 886 | 1 |
| hurinkrdata16 | 981 | 981 | 981 | 980 | 1 |
| hurinkrdata17 | 1021 | 1021 | 1021 | 1020 | 1 |
| hurinkrdata18 | 1033 | 1033 | 1033 | 1032 | 1 |
| hurinkrdata24 | 819 | 819 | 819 | 805 | 14 |
| hurinkrdata25 | 741 | 741 | 741 | 735 | 6 |
| hurinkrdata26 | 825 | 825 | 825 | 800 | 25 |
| hurinkrdata27 | 772 | 772 | 772 | 771 | 1 |
| hurinkrdata29 | 1024 | 1024 | 1024 | 1023 | 1 |
| hurinkrdata3 | 985 | 985 | 985 | 984 | 1 |
| hurinkrdata30 | 1062 | 1062 | 1062 | 1043 | 19 |
| hurinkrdata31 | 1051 | 1051 | 1051 | 1032 | 19 |
| hurinkrdata32 | 978 | 978 | 978 | 963 | 15 |
| hurinkrdata33 | 1047 | 1047 | 1047 | 1046 | 1 |
| hurinkrdata34 | 1463 | 1463 | 1463 | 1446 | 17 |
| hurinkrdata35 | 1575 | 1575 | 1575 | 1557 | 18 |
| hurinkrdata36 | 1418 | 1418 | 1418 | 1416 | 2 |
| hurinkrdata37 | 1459 | 1459 | 1459 | 1457 | 2 |
| hurinkrdata38 | 1471 | 1471 | 1471 | 1469 | 2 |
| hurinkrdata39 | 985 | 985 | 985 | 965 | 20 |
| hurinkrdata40 | 1039 | 1039 | 1039 | 1024 | 15 |
| hurinkrdata41 | 925 | 925 | 925 | 922 | 3 |
| hurinkrdata43 | 943 | 943 | 943 | 936 | 7 |
| hurinkrdata46 | 538 | 538 | 538 | 520 | 18 |
| hurinkrdata47 | 531 | 531 | 531 | 530 | 1 |
| hurinkrdata48 | 544 | 544 | 544 | 523 | 21 |
| hurinksdata3 | 1106 | 1106 | 1106 | 1105 | 1 |
| hurinksdata37 | 1600 | 1600 | 1600 | 1599 | 1 |
| hurinksdata41 | 1156 | 1156 | 1156 | 1152 | 4 |
| hurinksdata46 | 646 | 646 | 646 | 644 | 2 |
| hurinksdata48 | 689 | 689 | 689 | 687 | 2 |
| hurinkvdata10 | 712 | 712 | 712 | 709 | 3 |
| hurinkvdata11 | 720 | 720 | 720 | 719 | 1 |
| hurinkvdata12 | 805 | 805 | 805 | 804 | 1 |
| hurinkvdata13 | 756 | 756 | 756 | 755 | 1 |
| hurinkvdata14 | 1004 | 1004 | 1004 | 1003 | 1 |
| hurinkvdata15 | 880 | 880 | 880 | 879 | 1 |
| hurinkvdata16 | 978 | 978 | 978 | 977 | 1 |
| hurinkvdata17 | 1011 | 1011 | 1011 | 1010 | 1 |
| hurinkvdata24 | 764 | 764 | 764 | 763 | 1 |
| hurinkvdata25 | 701 | 701 | 701 | 697 | 4 |
| hurinkvdata26 | 777 | 777 | 777 | 772 | 5 |
| hurinkvdata27 | 746 | 746 | 746 | 734 | 12 |
| hurinkvdata28 | 721 | 721 | 721 | 713 | 8 |
| hurinkvdata29 | 994 | 994 | 994 | 991 | 3 |
| hurinkvdata3 | 962 | 962 | 962 | 961 | 1 |
| hurinkvdata30 | 1018 | 1018 | 1018 | 1010 | 8 |
| hurinkvdata31 | 1010 | 1010 | 1010 | 1008 | 2 |
| hurinkvdata32 | 947 | 947 | 947 | 937 | 10 |
| hurinkvdata33 | 1010 | 1010 | 1010 | 1006 | 4 |
| hurinkvdata34 | 1430 | 1430 | 1430 | 1424 | 6 |
| hurinkvdata35 | 1578 | 1578 | 1578 | 1553 | 25 |
| hurinkvdata36 | 1409 | 1409 | 1409 | 1408 | 1 |
| hurinkvdata37 | 1446 | 1446 | 1446 | 1445 | 1 |
| hurinkvdata38 | 1465 | 1465 | 1465 | 1457 | 8 |
| hurinkvdata44 | 785 | 785 | 785 | 784 | 1 |
| hurinkvdata46 | 477 | 477 | 477 | 471 | 6 |
| hurinkvdata47 | 498 | 498 | 498 | 486 | 12 |
| hurinkvdata48 | 488 | 488 | 488 | 477 | 11 |
| hurinkvdata52 | 6149 | 6149 | 6149 | 6148 | 1 |
| hurinkvdata53 | 4635 | 4635 | 4635 | 4634 | 1 |
| hurinkvdata9 | 763 | 763 | 763 | 762 | 1 |

## Check it yourself
    sh verify-it-yourself/run_checks.sh
Expected last line: PASS. It checks each schedule's sha256, downloads each instance file from the organisers' repository at commit eb1d28381c34 (not redistributed here), checks its sha256, validates the schedule with an independent checker and requires makespan = the value in INDEX.csv and at most UB - 1. A few minutes on a laptop (Python 3 standard library, curl, sha256sum).

## Compared to
best_known.csv of jrc-rodec/FJSSP-W-Benchmarking (https://raw.githubusercontent.com/jrc-rodec/FJSSP-W-Benchmarking/main/instances/InstanceData/FJSSP-W/best_known.csv), fetched 2026-11-23T19:06:35Z, sha256 74f982d5fdbdd7ebf6b889b0a57106474f9dd677a3813cf5762fc54afdfe30cf (the-record-we-beat/); its values have been unchanged since the repository's first table (2025-03-27). Also screened against the public submissions of the GECCO 2026 FJSSP-W competition (jrc-rodec/FJSSP-W-Competition, 15 submission threads and their archives), the benchmark authors' solver result files and all historical versions of the table; three rows where a public result is at or below ours were dropped before the claim was frozen (DPpaulli1, Hurinkrdata28, Hurinkvdata18). Cells claimed by open PR #868, by our draft PR #1081 or by 32 further cells of ours prepared earlier are excluded (the-record-we-beat/other-claims.txt).

## Not claimed
Optimality of any schedule; anything about instances not listed; the lower bounds; that the public competition values are valid (they are only used to screen the rows); anything about the search method beyond provenance. The search was an exploratory campaign without preregistration; the plan that fixes the object list, the screen and the counting rule was frozen after it (how-we-built-it/PREREG.md). Results are against the table as fetched at the time above.

## Credits
Benchmark and table: Hutter, Steinberger and Hellwig (Josef Ressel Centre; jrc-rodec/FJSSP-W-Benchmarking; arXiv:2501.16159); the underlying instance families: Behnke and Geiger, Brandimarte, Dauzere-Peres and Paulli, Hurink et al. GECCO 2026 FJSSP-W competition organisers and participants, whose public submissions we compared against, in particular Haoxiang Qin, Shixuan Zhou, Hainan Zhang, Kaichen Chen and Yi Xiang (South China University of Technology), Yu Sun, and the HUST SMART Lab Team2. Tools: OR-Tools CP-SAT, NumPy, Numba. Run by the V3R1T4S kit: Antigravity (search campaign) and Claude Code (lead agent, screen and claim), with three fresh reviewer subagents.
