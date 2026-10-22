Real output of `sh verify-it-yourself/run_checks.sh` run from the package folder on 2026-10-18 (Python standard library only):

```
sha256 ok object/30x64.txt
== check_sc.py: 50-digit decimal arithmetic, normalise, all pairs, against the saved live rows
(30,64) c*=0.038213431431870275994 table=0.038215865917 gain=0.00000243449 star=False needs_opt=False ref=Pavlos Moros, 2026. index_cos=0.038215865917 OK
rows checked: 1 (expected 1); smallest gain 2.43e-06; largest gain 2.43e-06
assertions: PASS (every row OK, no star, label absent)
ALL CHECKS PASS
```
