"""Calibration of check_eaqecc.py on hand-derivable cases. Prints CALIBRATION PASS or FAIL."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from check_eaqecc import analyse, mind
ok = True
def rec(name, info, n, want):
    global ok
    d = mind(info, n)
    got = (info['s'], info['c'], info['k'], d)
    print(name, 's,c,k,d =', got, 'expected', want, 'OK' if got == want else 'MISMATCH')
    ok = ok and got == want
# n=2, S = {X1 X2, Z1 Z2}: <(1,1|0,0),(0,0|1,1)> = 1+1 = 2 = -1 mod 3, nonzero, so one entangled pair; by hand dual = {(a,-a|e,-e)}, min weight 2
rec('EA n=2 {X1X2, Z1Z2}', analyse([[1,1,0,0],[0,0,1,1]], 2), 2, (2,1,1,2))
rec('EA n=2 {X1, Z1}', analyse([[1,0,0,0],[0,0,1,0]], 2), 2, (2,1,1,1))
# ordinary qutrit [[5,1,3]] from cyclic shifts of x=(0,0,0,1,1), z=(1,0,1,0,0): c = 0, k = 1, d = 3
x=[0,0,0,1,1]; z=[1,0,1,0,0]
S=[list(np.roll(x,i))+list(np.roll(z,i)) for i in range(4)]
rec('cyclic [[5,1,3]]_3', analyse(S, 5), 5, (4,0,1,3))
print('CALIBRATION PASS' if ok else 'CALIBRATION FAIL')
sys.exit(0 if ok else 1)
