# Receipts

Output of `sh verify-it-yourself/run_checks.sh` (run 2026-11-13T11:15:12Z, Python 3.11, standard library only):

```
S14 lag +5 samples NCC [0.4264, 0.5621] mean 0.4942 | S16 lag +7 samples NCC [0.6994, -0.0128] mean 0.3433 | Dt 0.3433
R7 best single channel S14 0.5621, S16 0.6994: True
null: 401 controls, best 0.19062, Dt above all: True
R8 S16 - S14 0.927 s, reference median 0.815 s (n 6): True
R9 phase 157.15 deg, 95% interval of 62 events [46.70, 318.34]: True
thermal: solar elevation S14 -84.6, S16 -59.8 deg
R6 (saved): nearest catalogue row -70.5 min (levent 73-330 0636 T2=A N2=203)
PASS
```
