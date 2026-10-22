Real output of `sh verify-it-yourself/run_checks.sh` run from the package folder on 2026-10-18 (Python standard library only):

```
sha256 ok object/30x62.txt
== check_sc.py: 50-digit decimal arithmetic, normalise, all pairs, against the saved live rows
(30,62) c*=0.031273183363813242615 table=0.031273236170 gain=5.28062e-8 star=False needs_opt=False ref=Ilmari Vahteristo, New spherical codes by tuning an annealing solver, preprint,  index_cos=0.031273236170 OK
rows checked: 1 (expected 1); smallest gain 5.28e-08; largest gain 5.28e-08
assertions: PASS (every row OK, no star, label absent)
ALL CHECKS PASS
```
