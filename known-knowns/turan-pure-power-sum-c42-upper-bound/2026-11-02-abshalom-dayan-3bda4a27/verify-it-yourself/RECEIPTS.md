# Receipts

See the lines below, copied from the runs named.

## check_hjb.py rows 0..300

```
row 0 worst 0.000001 at (0, 1, 1, 2167, 0.7044817811865476) refined 8268486 t=5
row 100 worst 0.000001 at (44, 0, 1, 1083, 0.7062317811865476) refined 806684988 t=762
row 200 worst 0.000001 at (122, 0, 0, 854, 0.7044817811865476) refined 1516443121 t=1509
HJB rows 0..300: worst certified G = 0.00000100 at (214, 1, 0, 1648, 0.7062317811865476), refined 2009448649, t=1907
INIT slack 1.0000000000287557e-06
TERM min -0.04486957, V(0,0) -0.05947169, m=0.01460213, C'=13.33333, eta=m/C'=0.00109516, mu_max=0.00072866, mu*L=0.005829, 2b=0.007
Lip V_tau,V_phi 0.9722685765883643 0.7533851309849549
PASS
done0

```

## check_hjb.py rows 300..1600

```
row 1000 worst 0.000001 at (987, 0, 1, 2492, 0.7079817811865475) refined 1122319145 t=1199
row 1100 worst 0.000001 at (987, 0, 1, 2492, 0.7079817811865475) refined 1172602658 t=1255
row 1200 worst 0.000001 at (987, 0, 1, 2492, 0.7079817811865475) refined 1219070554 t=1301
row 1300 worst 0.000001 at (987, 0, 1, 2492, 0.7079817811865475) refined 1263453083 t=1364
row 1400 worst 0.000001 at (987, 0, 1, 2492, 0.7079817811865475) refined 1306804994 t=1409
row 1500 worst 0.000001 at (1498, 1, 1, 1768, 0.7106067811865475) refined 1350677629 t=1487
HJB rows 300..1600: worst certified G = 0.00000100 at (1498, 1, 1, 1768, 0.7106067811865475), refined 1399887545, t=1544
INIT slack 1.0000000000287557e-06
TERM min -0.04486957, V(0,0) -0.05947169, m=0.01460213, C'=13.33333, eta=m/C'=0.00109516, mu_max=0.00072866, mu*L=0.005829, 2b=0.007
Lip V_tau,V_phi 0.9722685765883643 0.7533851309849549
PASS
done1

```

## late_gap.py

```
b [1.721994179 +/- 4.58e-10] mu_max [0.000728659038448 +/- 1.69e-16] mu(rho_+) [0.000721651865722 +/- 3.39e-16] mu(rho_-) [0.000728659038448 +/- 1.69e-16] eb [2.0733114 +/- 3.51e-8]
C0 [61.39601020 +/- 2.26e-9] eps1 [0.0001278922733 +/- 1.27e-14] C' [13.33333333 +/- 3.34e-9] varpi [1.21161e-6 +/- 3.22e-12] 2b' [0.00699999927835 +/- 1.87e-15]
TERM min in Arb >= [-0.0448485627485 +/- 1.38e-15] at rho,psi (0.7106067811865475, 5.5921269622371055) chord [1.744e-6 +/- 1.76e-10] [1.510e-6 +/- 3.84e-10] time 2.0
m = TERM - V(0,0) >= [0.0146231295129 +/- 6.20e-15]
eta' = [0.00108714279297 +/- 4.87e-16]
GAP1 eta'-(1+varpi)mu_max = [0.0003584828717 +/- 2.66e-14]    True
GAP2 2b'-mu_max(L+1/J0) = [0.001170726242 +/- 1.07e-13]    True
smallest m that passes GAP1 with these constants: [0.009843357891 +/- 4.07e-13]
GAP OK (given HJB and INIT from the certifier)
INIT slack [1.000000000e-6 +/- 5.52e-17]

```

## check2 coverage, all rows

```
check2 coverage, parsed from the row lines of the seven logs
rows 0-397: cells 1000572, finished line no (stopped by process id after row 397)
rows 398-399: cells 5028, finished line yes
rows 400-449: cells 125700, finished line yes
rows 450-499: cells 125700, finished line yes
rows 500-799: cells 754200, finished line yes
rows 800-1199: cells 1005600, finished line yes
rows 1200-1599: cells 1005600, finished line yes
rows covered 1600 missing [] duplicated []
total cells 4022400 fails plus unresolved 0

```

## check2 last log, final lines

```
-06 at (i=1232,j=80) fails 0 unresolved 0 t=184s
row 1596 done: cells 2514, row_worst_lb 1.11774377e-06 at j=1636, row_fails 0, row_boxes 143022 | rows_done 397/400 worst_so_far 1.0002223e-06 at (i=1232,j=80) fails 0 unresolved 0 t=184s
row 1597 done: cells 2514, row_worst_lb 1.0179478e-06 at j=443, row_fails 0, row_boxes 143182 | rows_done 398/400 worst_so_far 1.0002223e-06 at (i=1232,j=80) fails 0 unresolved 0 t=185s
row 1598 done: cells 2514, row_worst_lb 1.19924368e-06 at j=1839, row_fails 0, row_boxes 143334 | rows_done 399/400 worst_so_far 1.0002223e-06 at (i=1232,j=80) fails 0 unresolved 0 t=185s
row 1599 done: cells 2514, row_worst_lb 1.11538599e-06 at j=1711, row_fails 0, row_boxes 143532 | rows_done 400/400 worst_so_far 1.0002223e-06 at (i=1232,j=80) fails 0 unresolved 0 t=185s
finished: cells 1005600 smallest_lb 1.0002222953641065e-06 at (1232,80) witness_fails 0 unresolved 0

```

