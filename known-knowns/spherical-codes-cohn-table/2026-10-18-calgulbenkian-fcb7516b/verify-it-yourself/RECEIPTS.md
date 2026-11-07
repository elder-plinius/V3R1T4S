Real output of `sh verify-it-yourself/run_checks.sh` run from the package folder on 2026-11-03 (Python standard library only):

```
sha256 ok object/7x365.txt
== check_sc.py: 50-digit decimal arithmetic, normalise, all pairs, against the saved live rows
(7,365) c*=0.67046703514181086524 table=0.670467238587 gain=2.03445e-7 star=False needs_opt=False ref=Antoine Jay, 2026, using the program of A. Jay, M. Poberznik, M. Brut, A. Hemery index_cos=0.670467238587 OK
rows checked: 1 (expected 1); smallest gain 2.03e-07; largest gain 2.03e-07
assertions: PASS (every row OK, no star, label absent)
ALL CHECKS PASS
```
