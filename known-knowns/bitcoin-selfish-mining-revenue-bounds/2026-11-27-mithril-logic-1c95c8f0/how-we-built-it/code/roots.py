"""Bisection for the root rho* of the optimal gain (sign of Z_rho(0)) of the chosen MDP variant."""
import sys, time
from ssp import SSP
def root(al, T, mode, lo, hi, tol=2e-7):
    s = SSP(al, T, mode)
    while hi - lo > tol:
        mid = (lo+hi)/2
        Z = s.solve(mid, 0.0)[0]
        if Z > 0: lo = mid
        else: hi = mid
    return lo, hi
if __name__ == '__main__':
    al, T, mode = float(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    lo, hi = float(sys.argv[4]), float(sys.argv[5])
    t = time.time()
    lo, hi = root(al, T, mode, lo, hi, float(sys.argv[6]) if len(sys.argv) > 6 else 2e-7)
    print('alpha=%s T=%d mode=%s root in [%.10f, %.10f]  (%.0fs)' % (al, T, mode, lo, hi, time.time()-t), flush=True)
