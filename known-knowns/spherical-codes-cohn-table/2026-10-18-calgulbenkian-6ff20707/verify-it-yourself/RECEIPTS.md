Real output of `sh verify-it-yourself/run_checks.sh` run from the package folder on 2026-10-18 (Python standard library only):

```
sha256 ok object/28x59.txt
== check_sc.py: 50-digit decimal arithmetic, normalise, all pairs, against the saved live rows
(28,59) c*=0.039154189772679138677 table=0.039154654978 gain=4.65205e-7 star=False needs_opt=False ref=Pavlos Moros, 2026. index_cos=0.039154654978 OK
rows checked: 1 (expected 1); smallest gain 4.65e-07; largest gain 4.65e-07
assertions: PASS (every row OK, no star, label absent)
ALL CHECKS PASS
```
