Real output of `sh verify-it-yourself/run_checks.sh` run from the package folder on 2026-10-18 (Python standard library only):

```
sha256 ok object/31x65.txt
== check_sc.py: 50-digit decimal arithmetic, normalise, all pairs, against the saved live rows
(31,65) c*=0.037040509594848894968 table=0.037040536638 gain=2.70432e-8 star=False needs_opt=False ref=Pavlos Moros, 2026. index_cos=0.037040536638 OK
rows checked: 1 (expected 1); smallest gain 2.7e-08; largest gain 2.7e-08
assertions: PASS (every row OK, no star, label absent)
ALL CHECKS PASS
```
