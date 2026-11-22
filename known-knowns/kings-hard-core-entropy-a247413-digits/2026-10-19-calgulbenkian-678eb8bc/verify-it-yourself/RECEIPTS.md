# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder with the system python3 (3.9.6, standard library only) on 2026-10-19T02:02Z. The checker is the panel claim folder checker with two changes (table excerpts read from `the-record-we-beat/README.md`; part 0 checks object hashes against `SHA256SUMS` and the one-row INDEX.csv). The panel claim folder's own receipts, from its original checker, are not repeated here.

```
== part 0: INDEX.csv row and SHA256SUMS hashes of every object file
ok    INDEX.csv header
ok    INDEX.csv has one data row
ok    sha256 of object/KINGS_VALUE.txt
ok    SHA256SUMS hash of object/KINGS_VALUE.txt
ok    SHA256SUMS hash of object/domg_100.log
ok    SHA256SUMS hash of object/domg_110.log
ok    SHA256SUMS hash of object/domg_120.log
ok    SHA256SUMS hash of object/domg_130.log
ok    SHA256SUMS hash of object/final_tables.txt
ok    SHA256SUMS hash of object/lam_open.txt
ok    SHA256SUMS hash of object/lam_open_lean.txt
ok    SHA256SUMS hash of object/prereg_b_output.txt
ok    SHA256SUMS hash of object/sitef_100.log
ok    SHA256SUMS hash of object/sitef_70.log
ok    SHA256SUMS hash of object/sitef_80.log
ok    SHA256SUMS hash of object/sitef_90.log
ok    object/ holds 13 files
== part 1: parse the object tables
ok    lam_open.txt holds widths 2..28 (70 digits each)
ok    lam_open_lean.txt holds widths 24, 28 and 29..40
ok    lean vs old lambda_24: relative difference 1.4e-56
ok    lean vs old lambda_28: relative difference 2.0e-56
ok    sitef_70.log last line agrees with Table A in final_tables.txt (52 decimals)
ok    sitef_80.log last line agrees with Table A in final_tables.txt (52 decimals)
ok    sitef_90.log last line agrees with Table A in final_tables.txt (52 decimals)
ok    sitef_100.log last line agrees with Table A in final_tables.txt (52 decimals)
== part 2: own Wynn epsilon at 80 digits on r_m = lambda_m / lambda_(m-1), m = 3..mmax
ok    E(mmax) for mmax = 22..40 matches prereg_b_output.txt (order and 44 printed decimals)
ok    window counts (four successive mmax) for windows ending 25..40 match the file
      method B: decimals common to E(37), E(38), E(39), E(40): 33
      method B: window ending 34 (the original target width): 27
ok    method B stable decimal count over mmax = 37..40 is 33
== part 3: agreement counts
ok    A247413 DATA excerpt has 18 terms
ok    first term is the integer part 1; 17 published decimals follow
      method A: decimals common to chi = 70, 80, 90, 100: 36
      method A: decimals common to chi = 80, 90, 100: 38
ok    method A stable decimal count over chi = 70..100 is 36
      A (chi = 100) vs B (E(40)): 35 common decimals
ok    A and B share at least 33 leading decimals (35)
ok    A and B both begin with the 17 published decimals
ok    KINGS_VALUE.txt carries the 33-decimal value
ok    the 33 decimals equal the first 33 decimals of A (chi = 100) and of B (E(40))
ok    decimals 34-35 of A and of B are 39 (truncation and rounding give the same 33 decimals)
      method C (domino CTM, supporting): decimals common to chi = 100, 110, 120, 130 last lines: 29; with A (chi = 100): 100:29, 110:31, 120:30, 130:31
      published bracket (Liang) low 1.342643951124601297851 high 1.342643951124601298092; method A value inside it: True
== part 4: checks from the definition
ok    independent sets of the king graph on the 1x1 grid = 2 = A063443(2)
ok    independent sets of the king graph on the 2x2 grid = 5 = A063443(3)
ok    independent sets of the king graph on the 3x3 grid = 35 = A063443(4)
ok    independent sets of the king graph on the 4x4 grid = 314 = A063443(5)
ok    independent sets of the king graph on the 5x5 grid = 6427 = A063443(6)
ok    independent sets of the king graph on the 6x6 grid = 202841 = A063443(7)
ok    independent sets of the king graph on the 7x7 grid = 12727570 = A063443(8)
ok    Z(3,5) = Z(5,3) (grid symmetry)
ok    open strip m = 1: exact power iteration gives 1.6180339887498948482045868343656381177203, golden ratio 1.6180339887498948482045868343656381177203 (rel diff 0.0e+00)
ok    open strip m = 2: exact power iteration 2.000000000000000000000000000000 vs listed lambda_m 2.000000000000000000000000000000 (rel diff 0.0e+00)
ok    open strip m = 3: exact power iteration 2.813606502648330815441227562361 vs listed lambda_m 2.813606502648330815441227562361 (rel diff 1.8e-62)
ok    open strip m = 4: exact power iteration 3.690306445883315985901487546207 vs listed lambda_m 3.690306445883315985901487546207 (rel diff 7.6e-62)
ok    open strip m = 5: exact power iteration 5.017597223373379638213172510825 vs listed lambda_m 5.017597223373379638213172510825 (rel diff 1.7e-61)
ok    open strip m = 6: exact power iteration 6.692999365873237507488900062385 vs listed lambda_m 6.692999365873237507488900062385 (rel diff 9.0e-61)

failed checks: 0
PASS
```
