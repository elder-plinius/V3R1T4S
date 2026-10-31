# REPRODUCE (Windows, Python 3.14; python-flint 0.9.0 = Arb; numpy, scipy for the sanity scripts)

All commands are run from THIS folder (the one that contains `REDUCTION_FULL.md` and `code/`) in a fresh shell.  Nothing outside this folder is read.
Each step is a single process.

```
python -m venv venv
venv\Scripts\python.exe -m pip install python-flint==0.9.0 numpy scipy

REM --- 1. exact integer branch-and-bound for K4' (stdlib only; ~15 s each)
python code\k4_bb.py 1 1000    > code\k4_bb_eps_1_1000.out
python code\k4_bb.py -1 100    > code\k4_bb_negative_control_eps_-1_100.out

REM --- 2. certified Arb chain with the K4' constant (3/sqrt2)(1+1/1000)
venv\Scripts\python.exe code\fullchain.py build  1000 40  > code\build_eps1000.out       REM  table rho(c,w), ~10 s, writes code\rho_cert.json
venv\Scripts\python.exe code\fullchain.py scheme 1000 40  > code\scheme_eps1000_Q40.out  REM  scan of (k,u), ~45 s, writes code\scheme_best_40.json
venv\Scripts\python.exe code\verify_final.py 40 1000      > code\verify_final.out        REM  independent re-certification; the LAST line is the result

REM --- 3. sanity checks (NUMERICAL, not proof inputs)
venv\Scripts\python.exe code\k1_check.py       > code\k1_check.out          REM  ~1 min (Arb quadrature of the defining integral, Monte Carlo)
python code\k1_random.py                       > code\k1_random.out         REM  seconds
venv\Scripts\python.exe code\v2_check.py       > code\v2_check.out          REM  ~1 min
python code\k3_check.py                        > code\k3_check.out          REM  ~8 min (randomised test of the K3 construction)
python code\k4_necessity_check.py              > code\k4_necessity_check.out
python code\k4_relax.py                        > code\k4_relax.out
python code\k4_num.py                          > code\k4_num.out
python code\edge_dist_counter.py               > code\edge_dist_counter.out
```
(`python` for the sanity scripts means any Python with numpy and scipy; the venv works as well.  If `fullchain.py scheme` is re-run it overwrites `scheme_best_40.json`; the stored copy is identical when the run is identical.)

## Expected last lines

`code\k4_bb_eps_1_1000.out`:
```
boxes processed 28959 stats {'dom': 1964, 'in': 2343, 'ok': 9999, 'vtx': 174} unresolved 0
SHELL boxes 228811 {'core': 488, 'in': 28087, 'ok': 85831} unresolved 0
RESULT: PROVED (all boxes certified)
```
`code\k4_bb_negative_control_eps_-1_100.out` ends with `RESULT: NOT PROVED` (as it must, the constant 3/sqrt2 is tight).

`code\build_eps1000.out` ends with
```
state (0, 40) CERTIFIED 5.342391e-12
rho_cert(0,5) = 1.273845e-11   rho_cert(0,41) = 5.342391e-12
```
`code\verify_final.out` ends with
```
rho(0,Q) used = 5.342391e-12 ; b >= 4.501166e-15
CERTIFIED (Arb, modulo the Residual trust list) density <= 1 - 4.501166e-15
```
`code\k3_check.out` ends with `violations (new overlap > original overlap + 3e-05): 0 ; families with uncovered original volume: 0 ; max (new-orig) overlap fraction 0.00e+00` (the line before reports 150 families, 72 nested deletions).

The reduction that matches these programs function by function is `REDUCTION_FULL.md` (section 12 has the file map; section 10 is the "Residual trust" list).
