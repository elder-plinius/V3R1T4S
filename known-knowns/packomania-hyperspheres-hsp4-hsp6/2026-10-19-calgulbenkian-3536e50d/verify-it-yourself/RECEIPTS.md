# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from the package folder by the packager on 2026-10-19 (python3 3.9.6, Darwin). Wall time about 1 seconds. Exit status 0.

```
sha256 of object/WIN_hsp4_170.txt matches INDEX.csv (3536e50dd047d04f09605dabb6bf33b5c17a9bfaf502147c2cc43c9da215bb65)
== packcheck.py: exact feasible radius of object/WIN_hsp4_170.txt
object_points N=170 dim=4 decimals_scale=17
pairs_examined=14365 pairs_expected=14365
object_header_radius=0.21564505946838996575
r_pair_half_min_distance=0.215645064369925650688523058284
r_wall=0.215645059468390008128190279493
r_star=0.215645059468390008128190279493
binding=wall
table_radius=0.215589695168
gain_over_table=5.536430039000813e-5
gain_at_least_margin(1e-10)=True
RESULT PASS
== (the posted Packomania coordinate file is not shipped; see RUN_IT_YOURSELF.md for the non-isometry check)
== table_compare.py: facts against the saved table records
table rows read: 131 (N from 170 to 300)
table row N=170: 0.21558969516800  r_star minus this = 5.536430e-5
largest table row at N' >= 170: 0.21558969516800 (at N=170)  r_star minus this = 5.536430e-5
Moki-Julio manifest N=170: 0.21559175301350  r_star minus this = 5.330645e-5
largest manifest value at N' >= 170: 0.21559175301350 (at N=170)  r_star minus this = 5.330645e-5
Cohn table converted, N=170: 0.20853075981595  r_star minus this = 7.114300e-3
largest converted Cohn value at N' >= 170: 0.20853075981595 (at N=170)  r_star minus this = 7.114300e-3
RESULT facts printed
== negative control: the first point is moved onto the second; the check must FAIL
negative control rejected as expected (r_star=0.000000000000000000000000000000)
ALL CHECKS PASS
```
