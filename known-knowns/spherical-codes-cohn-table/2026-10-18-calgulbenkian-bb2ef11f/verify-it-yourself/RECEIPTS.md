Real output of `sh verify-it-yourself/run_checks.sh` run from the package folder on 2026-10-18 (Python standard library only):

```
sha256 ok object/27x56.txt
== check_sc.py: 50-digit decimal arithmetic, normalise, all pairs, against the saved live rows
(27,56) c*=0.034509959006364448779 table=0.034509985004 gain=2.59976e-8 star=False needs_opt=False ref=Ilmari Vahteristo, New spherical codes by tuning an annealing solver, preprint,  index_cos=0.034509985004 OK
rows checked: 1 (expected 1); smallest gain 2.6e-08; largest gain 2.6e-08
assertions: PASS (every row OK, no star, label absent)
ALL CHECKS PASS
```
