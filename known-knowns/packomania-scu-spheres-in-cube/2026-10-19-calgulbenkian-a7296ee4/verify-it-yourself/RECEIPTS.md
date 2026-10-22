# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from the package folder by the packager on 2026-10-19 (python3 3.9.6, Darwin). Wall time about 1 seconds. Exit status 0.

```
sha256 of object/WIN_scu_739.txt matches INDEX.csv (a7296ee4e9a17d4490e65a696af8c4d64266a39af7cd383cfdd0e54d641baf76)
== packcheck.py: exact feasible radius of object/WIN_scu_739.txt
object_points N=739 dim=3 decimals_scale=20
pairs_examined=272691 pairs_expected=272691
r_pair_half_min_distance=0.058627544166645979614056673889
r_wall=0.058627544166646006210000000000
r_star=0.058627544166645979614056673889
binding=pair
table_radius=0.058531064606
gain_over_table=9.647956064597961e-5
gain_at_least_margin(1e-11)=True
RESULT PASS
== (the posted Packomania coordinate file is not shipped; see RUN_IT_YOURSELF.md for the non-isometry check)
== table_compare.py: facts against the saved table records
table rows read: 262 (N from 739 to 1000)
table row N=739: 0.05853106460600  r_star minus this = 9.647956e-5
largest table row at N' >= 739: 0.05862703675600 (at N=740)  r_star minus this = 5.074106e-7
Moki-Julio manifest N=739: 0.05860738667577  r_star minus this = 2.015749e-5
largest manifest value at N' >= 739: 0.05860738667577 (at N=739)  r_star minus this = 2.015749e-5
RESULT facts printed
== negative control: the first point is moved onto the second; the check must FAIL
negative control rejected as expected (r_star=0.000000000000000000000000000000)
ALL CHECKS PASS
```
