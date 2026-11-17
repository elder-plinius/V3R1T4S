# Verification Receipts: `eulerian-synchronizing-szykula-vorel-bound`

Command executed from the package root:

```sh
sh verify-it-yourself/run_checks.sh
```

Exit code: `0`

Captured standard output:

```text
[PY-CALIB] Szykula-Vorel A_1 (n=5, k=4): eulerian=True, rt=11 == 11
[PY-CALIB] Szykula-Vorel A_2 (n=9, k=4): eulerian=True, rt=39 == 39
[PY-CALIB] Szykula-Vorel A_3 (n=13, k=4): eulerian=True, rt=83 == 83
[PY-CALIB] Cerny C_5 (n=5, k=2): eulerian=False (expected False), rt=16 == 16
[PY-CHECK] Verified complete Eulerian synchronizing DFA: n=7, k=5, rt=24 > floor((7^2-3)/2)=23, shortest_reset_word=034023402304234230342430 (len=24)
PY_VERIFY_OK
[C-CALIB] Szykula-Vorel A_1 (n=5, k=4): eulerian=1, rt=11 == 11
[C-CALIB] Szykula-Vorel A_2 (n=9, k=4): eulerian=1, rt=39 == 39
[C-CALIB] Szykula-Vorel A_3 (n=13, k=4): eulerian=1, rt=83 == 83
[C-CALIB] Cerny C_5 (n=5, k=2): eulerian=0 (expected 0), rt=16 == 16
[C-CHECK] Verified complete Eulerian synchronizing DFA: n=7, k=5, rt=24 > floor((7^2-3)/2)=23
C_VERIFY_OK
PASS
```
