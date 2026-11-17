# Receipts

Output of `sh verify-it-yourself/run_checks.sh` (run 2026-11-13T18:15:20Z, Python 3.11, standard library only):

```
S14 lag -5 samples NCC [0.4936, 0.6211] mean 0.5573 | S16 lag -3 samples NCC [0.6196, -0.0235] mean 0.2981 | Dt 0.2981
R7 best single channel S14 0.6211, S16 0.6196: True
null: 401 controls, best 0.19062, Dt above all: True
R8 S16 - S14 0.715 s, reference median 0.815 s (n 6): True
R9 phase 161.49 deg, 95% interval of 62 events [46.70, 318.34]: True
thermal: solar elevation S14 -65.6, S16 -32.4 deg
R6 (saved): nearest catalogue row -85.9 min (levent 73-303 0100 T2=A N2=1)
PASS
```
