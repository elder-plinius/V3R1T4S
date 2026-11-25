# Reproduce review (skeptic: reproduce)

context: started fresh with only a brief and read-only access to claim-v2/ (CLAIM.md, REPRODUCE.md, criterion.txt, object/, references/, provenance/rows.csv, status/table-fetch.txt); the authors' code, notes and other workspace folders were not read; python3 -I, standard library only, own checker written from REPRODUCE.md section 1-5 before anything else.

## Method
Checker: work-reproduce/chk.py (own parser and checker). Definition applied (REPRODUCE.md item 3, quoted): "every operation exactly once; (machine, worker) allowed for that operation and the duration equal to that pair's; starts >= 0; within a job, operation i starts at or after operation i-1 ends; no two operations overlap on a machine, nor on a worker (half-open intervals); makespan = latest end." Instance parser: one integer stream, 3 header numbers (4 tried if not exactly consumed), per job ops, per op k machine choices, each machine id + w worker/duration pairs. Row pass rule: valid and makespan <= round(UB) - 1.

For all 65 rows the script: parses the instance, validates object/<file>.json (also the "instance" field and that all schedule fields are integers), recomputes makespan, reads UB by header name from references/best_known.csv (semicolon separated; max deviation of the 65 UBs from an integer was 0.0), confirms row_to_file.json against references/data.csv (source column) and the file names (family names lower-cased, behnke -> behnkegeiger, Mk removed, number equal), checks that rows, objects, instance files, sha lines and provenance rows are the same 65-element set, checks references/instances.sha256 against the instance files, and compares makespan, UB, saving, pct, object_sha256, instance_sha256 and file in provenance/rows.csv, and the file, UB, makespan, saving columns of the CLAIM.md table (65 table rows parsed), with its own values.
(The table sha256 line in status/table-fetch.txt was also compared with the copy of best_known.csv; see below.)

## Results
- 65 of 65 rows PASS (valid schedule, makespan <= round(UB)-1). Zero mismatches against CLAIM.md table (65 rows) and provenance/rows.csv (all five compared fields plus pct). 65/65 instance sha256 match references/instances.sha256. Row-to-file mapping consistent with data.csv and names for all 65.
- Failing rows: none.
- Determinism: chk.py run twice, outputs byte-identical (work-reproduce/r1.txt, r2.txt).
- Negative tests (work-reproduce/corr.py, corrupted copies of object/ in work-reproduce/corrupt_*): each corruption made the checker report ALL_PASS=False with the expected reason: negative start, wrong duration, dropped op, duplicated op, worker not allowed, precedence violation, wrong instance field, makespan +1000, last op delayed by 2 (not better, rows.csv mismatch), missing object file, machine overlap (overlap on machine), worker overlap attempt (rejected, on precedence because the shifted op broke job order). 12/12 rejected.
- Not independently verifiable from the folder: that best_known.csv equals the live upstream file (no network used; the copy's hash was compared only to the hash recorded in status/table-fetch.txt) and that the instance files equal the upstream commit; only the recorded hashes are checked.

## Per-row results (all PASS; UB rounded, saving = UB - makespan)
| row | file | UB | makespan | saving | result |
|---|---|---:|---:|---:|---|
| behnkegeiger10 | Behnke10 | 125 | 124 | 1 | PASS |
| behnkegeiger21 | Behnke21 | 81 | 78 | 3 | PASS |
| behnkegeiger23 | Behnke23 | 79 | 78 | 1 | PASS |
| behnkegeiger27 | Behnke27 | 119 | 116 | 3 | PASS |
| behnkegeiger28 | Behnke28 | 111 | 108 | 3 | PASS |
| behnkegeiger29 | Behnke29 | 112 | 110 | 2 | PASS |
| behnkegeiger3 | Behnke3 | 86 | 83 | 3 | PASS |
| behnkegeiger41 | Behnke41 | 80 | 79 | 1 | PASS |
| behnkegeiger44 | Behnke44 | 78 | 76 | 2 | PASS |
| behnkegeiger45 | Behnke45 | 80 | 79 | 1 | PASS |
| behnkegeiger47 | Behnke47 | 113 | 111 | 2 | PASS |
| behnkegeiger50 | Behnke50 | 118 | 114 | 4 | PASS |
| behnkegeiger51 | Behnke51 | 234 | 231 | 3 | PASS |
| behnkegeiger52 | Behnke52 | 234 | 212 | 22 | PASS |
| behnkegeiger53 | Behnke53 | 229 | 216 | 13 | PASS |
| behnkegeiger54 | Behnke54 | 251 | 227 | 24 | PASS |
| behnkegeiger55 | Behnke55 | 237 | 220 | 17 | PASS |
| brandimarte5 | BrandimarteMk5 | 166 | 164 | 2 | PASS |
| chambersbarnes15 | ChambersBarnes15 | 1163 | 1120 | 43 | PASS |
| chambersbarnes16 | ChambersBarnes16 | 1155 | 1113 | 42 | PASS |
| chambersbarnes17 | ChambersBarnes17 | 1153 | 1118 | 35 | PASS |
| chambersbarnes18 | ChambersBarnes18 | 1091 | 1082 | 9 | PASS |
| chambersbarnes19 | ChambersBarnes19 | 1060 | 1050 | 10 | PASS |
| chambersbarnes20 | ChambersBarnes20 | 1143 | 1118 | 25 | PASS |
| chambersbarnes21 | ChambersBarnes21 | 1094 | 1055 | 39 | PASS |
| chambersbarnes4 | ChambersBarnes4 | 845 | 834 | 11 | PASS |
| dppaulli4 | DPpaulli4 | 2520 | 2447 | 73 | PASS |
| fattahi20 | Fattahi20 | 1147 | 1123 | 24 | PASS |
| hurinkedata15 | Hurinkedata15 | 919 | 915 | 4 | PASS |
| hurinkedata24 | Hurinkedata24 | 990 | 977 | 13 | PASS |
| hurinkedata27 | Hurinkedata27 | 886 | 869 | 17 | PASS |
| hurinkedata28 | Hurinkedata28 | 891 | 881 | 10 | PASS |
| hurinkedata29 | Hurinkedata29 | 1101 | 1090 | 11 | PASS |
| hurinkedata30 | Hurinkedata30 | 1174 | 1157 | 17 | PASS |
| hurinkedata32 | Hurinkedata32 | 1104 | 1091 | 13 | PASS |
| hurinkedata39 | Hurinkedata39 | 1120 | 1115 | 5 | PASS |
| hurinkedata40 | Hurinkedata40 | 1317 | 1291 | 26 | PASS |
| hurinkedata41 | Hurinkedata41 | 1138 | 1111 | 27 | PASS |
| hurinkedata42 | Hurinkedata42 | 1133 | 1104 | 29 | PASS |
| hurinkedata43 | Hurinkedata43 | 1101 | 1069 | 32 | PASS |
| hurinkedata9 | Hurinkedata9 | 784 | 782 | 2 | PASS |
| hurinkrdata13 | Hurinkrdata13 | 767 | 762 | 5 | PASS |
| hurinkrdata4 | Hurinkrdata4 | 540 | 538 | 2 | PASS |
| hurinkrdata42 | Hurinkrdata42 | 1004 | 979 | 25 | PASS |
| hurinkrdata44 | Hurinkrdata44 | 908 | 892 | 16 | PASS |
| hurinkrdata5 | Hurinkrdata5 | 500 | 498 | 2 | PASS |
| hurinkrdata50 | Hurinkrdata50 | 5701 | 5651 | 50 | PASS |
| hurinkrdata52 | Hurinkrdata52 | 6240 | 6193 | 47 | PASS |
| hurinkrdata6 | Hurinkrdata6 | 458 | 454 | 4 | PASS |
| hurinkrdata7 | Hurinkrdata7 | 479 | 474 | 5 | PASS |
| hurinkrdata9 | Hurinkrdata9 | 765 | 763 | 2 | PASS |
| hurinksdata26 | Hurinksdata26 | 951 | 948 | 3 | PASS |
| hurinksdata29 | Hurinksdata29 | 1202 | 1132 | 70 | PASS |
| hurinksdata30 | Hurinksdata30 | 1192 | 1177 | 15 | PASS |
| hurinksdata31 | Hurinksdata31 | 1212 | 1148 | 64 | PASS |
| hurinksdata32 | Hurinksdata32 | 1146 | 1131 | 15 | PASS |
| hurinksdata33 | Hurinksdata33 | 1248 | 1240 | 8 | PASS |
| hurinksdata39 | Hurinksdata39 | 1192 | 1182 | 10 | PASS |
| hurinksdata40 | Hurinksdata40 | 1329 | 1285 | 44 | PASS |
| hurinksdata42 | Hurinksdata42 | 1168 | 1159 | 9 | PASS |
| hurinksdata43 | Hurinksdata43 | 1175 | 1137 | 38 | PASS |
| hurinksdata47 | Hurinksdata47 | 676 | 669 | 7 | PASS |
| hurinkvdata49 | Hurinkvdata49 | 4740 | 4718 | 22 | PASS |
| hurinkvdata5 | Hurinkvdata5 | 504 | 501 | 3 | PASS |
| hurinkvdata63 | Hurinkvdata63 | 251 | 250 | 1 | PASS |

pass: true
