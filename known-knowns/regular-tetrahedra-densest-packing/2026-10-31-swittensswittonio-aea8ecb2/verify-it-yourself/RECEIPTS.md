# Receipts

Real output of `sh verify-it-yourself/run_checks.sh` (Windows, Git Bash, Python 3.14, python-flint 0.9.0), 2026-10-31.

```
step 1: sha256 of every file in object/
object/ hashes: 11 files, 0 mismatches
step 2: python-flint (Arb)
step 3: exact-integer branch-and-bound for K4 (eps = 1/1000)
boxes processed 28959 stats {'dom': 1964, 'in': 2343, 'ok': 9999, 'vtx': 174} unresolved 0
SHELL boxes 228811 {'core': 488, 'in': 28087, 'ok': 85831} unresolved 0
RESULT: PROVED (all boxes certified)
step 4: re-certification with Arb
scheme (Q=40, k=30, u=0.01140, K4' eps=1/1000): gamma_Q=0.788335 r_v=0.030707 d=0.16940 q=6 (multiplicity) q_v=7 (area count; K2-count would be 44) m_v=3 good/tet=96
checks: {'d>2*r_v': True, 'd>=2u': True, '1/sqrt2>=2u': True, 'R0<=sqrt(2/3)d': True, 'R1>0': True, "0<R''<sqrt(2/3)": True, "r_v/R''<0.98": True, 'ok': True}
rho(0,Q) used = 5.342391e-12 ; b >= 4.501166e-15
CERTIFIED (Arb, modulo the Residual trust list) density <= 1 - 4.501166e-15
PASS
```
