#!/usr/bin/env python3
"""PREREG negative controls N2-N4 for the arb certificate (N1 replay lives in attempts/replay, N5 in attempts/checker)."""
import io, contextlib
from cert_arb import certify
from mpmath import mp, mpf, log, exp, sqrt
def run(*a, **k):
    with contextlib.redirect_stdout(io.StringIO()):
        return certify(*a, verbose=False, **k)
res = []
# N2 ablation (Bellotti density off, KLN to 1-nu), c=57.54: must not certify any Y < 32.8
ok, _ = run('32.799', '57.54', 'kln', 128); res.append(('N2 ablation kln c=57.54 at Y=32.799 must FAIL', not ok))
ok, _ = run('32.892', '57.54', 'kln', 128); res.append(('N2 info: kln c=57.54 certifies 32.892 (= Cully-Hugill JNT 2023)', ok))
# N3 tamper: Y_cert-0.01 must fail; C' x e^50 at Y_cert must fail
ok, _ = run('29.725', '51.34', 'thm11', 256); res.append(('N3a main at Y=29.725 (Y_cert-0.01) must FAIL', not ok))
ok, _ = run('29.735', '51.34', 'thm11', 256, Cscale='5.184705528587072464087453322933485384827469756e21'); res.append(('N3b main with C1*5.1847e21 (~e^50) at 29.735 must FAIL', not ok))
ok, _ = run('29.735', '51.34', 'thm11', 256); res.append(('N3c main at 29.735 PASS (prec 256)', ok))
# N4 float vs arb at X0 (main)
_, out = run('29.735', '51.34', 'thm11', 256)
mp.dps = 50
a = mpf(1)/3 + mpf('1e-9'); X = 3*exp(mpf('29.735')); L = a*X; nu = 1/(mpf('51.34')*L**(mpf(2)/3)*log(L)**(mpf(1)/3))
f = 0
for C,B,e in [('9.77e21','57.8875',mpf(19703)/1800),('7.65e10','33.08',mpf(503)/45),('0.27','0',mpf(14)/10)]:
    C=mpf(C);B=mpf(B); f += C*L**e*exp(-X*(nu-B*a*nu**1.5))/(1-1.5*B*a*sqrt(mpf('1e-6')))
f = 2*log(L)*f
arbmid = mpf(out['Phi'].mid().str(40, radius=False))
rel = abs(f-arbmid)/arbmid
res.append((f'N4 float Phi={mp.nstr(f,15)} vs arb mid={mp.nstr(arbmid,15)} rel diff {mp.nstr(rel,3)} < 1e-9', rel < mpf('1e-9')))
for k, v in res: print(('ok  ' if v else 'BAD ') + k)
print('ALL_CONTROLS_BEHAVE' if all(v for _, v in res) else 'CONTROL_FAILURE')
