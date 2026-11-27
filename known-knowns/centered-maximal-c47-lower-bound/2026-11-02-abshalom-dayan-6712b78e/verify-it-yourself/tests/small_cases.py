#!/usr/bin/env python3
# Hand-computed small cases for the checkers. Run from the claim folder. Prints PASS or FAIL.
# One atom of mass m, far from its images: box {p} gives a square of area m, nothing else reaches, value exactly 1.
# Two atoms of equal mass m at distance t <= sqrt(2m) in x: squares Q(p, sqrt(m)/2) and the box of both, with rho = sqrt(2m)/2,
# whose rectangle is [x2-rho, x1+rho] x [y-rho, y+rho]. By hand, for bits = 4, m = 1 (16/16), t = 1: rho = sqrt(2)/2 is not dyadic;
# the checker rounds rho down, so the exact expected value is computed here from the checker's own grid R = 40 by the same rule.
import json, subprocess, sys, os, tempfile, math
from fractions import Fraction as F
d = tempfile.mkdtemp()
def run(c, reach):
    p = os.path.join(d, 'c.json'); json.dump(c, open(p, 'w'))
    o = subprocess.run([sys.executable, '-I', 'verify-it-yourself/check_a.py', p, str(reach)], capture_output=True, text=True).stdout
    return o
ok = True
# case 1: one atom, mass 1, period 8: square of side 1, area 1, mass 1, value 1 exactly
o = run(dict(bits=4, Lx=128, Ly=128, atoms=[[0, 0, 16]]), 2); print(o.strip().splitlines()[-1]); ok &= 'value=1.000000000000' in o
# case 2: one atom, mass 4, period 8: side 2 square, area 4, value 1 exactly
o = run(dict(bits=4, Lx=128, Ly=128, atoms=[[0, 0, 64]]), 2); print(o.strip().splitlines()[-1]); ok &= 'value=1.000000000000' in o
# case 3: two atoms of mass 1 at distance 1 in x, period 8. Squares: [-1/2,1/2]^2 and [1/2,3/2]x[-1/2,1/2].
# Box of both: mass 2, rho = sqrt(2)/2, rectangle [1-rho, rho] x [-rho, rho], width 2 rho - 1, height 2 rho.
# Union area = 2 + (2 rho - 1)(2 rho - 1) = 2 + (sqrt 2 - 1)^2 = 2 + 3 - 2 sqrt 2 = 5 - 2 sqrt 2 = 2.17157287...; value = that / 2 = 1.08578643...
o = run(dict(bits=4, Lx=128, Ly=128, atoms=[[0, 0, 16], [16, 0, 16]]), 3); line = o.strip().splitlines()[-1]; print(line)
v = float(line.split('=')[1]); ok &= abs(v - (5 - 2*math.sqrt(2))/2) < 1e-9
print('PASS' if ok else 'FAIL')
