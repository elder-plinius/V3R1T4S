# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from the package folder by the packager on 2026-10-19 (python3 3.9.6, Darwin). Wall time about 1 seconds. Exit status 0.

```
sha256 of object/WIN_scu_733.txt matches INDEX.csv (14cbb77e014f41d2dd0cb795eed3095d31591a76985ab0a9b57e04db7e63082d)
== packcheck.py: exact feasible radius of object/WIN_scu_733.txt
object_points N=733 dim=3 decimals_scale=20
pairs_examined=268278 pairs_expected=268278
r_pair_half_min_distance=0.058943752954827944802477801688
r_wall=0.058943752954827954850000000000
r_star=0.058943752954827944802477801688
binding=pair
table_radius=0.058531064607
gain_over_table=4.126883478279448e-4
gain_at_least_margin(1e-11)=True
RESULT PASS
== (the posted Packomania coordinate file is not shipped; see RUN_IT_YOURSELF.md for the non-isometry check)
== table_compare.py: facts against the saved table records
table rows read: 268 (N from 733 to 1000)
table row N=733: 0.05853106460700  r_star minus this = 4.126883e-4
largest table row at N' >= 733: 0.05894367586600 (at N=734)  r_star minus this = 7.708883e-8
Moki-Julio manifest N=733: 0.05882186938148  r_star minus this = 1.218836e-4
largest manifest value at N' >= 733: 0.05882186938148 (at N=733)  r_star minus this = 1.218836e-4
RESULT facts printed
== negative control: the first point is moved onto the second; the check must FAIL
negative control rejected as expected (r_star=0.000000000000000000000000000000)
ALL CHECKS PASS
```
