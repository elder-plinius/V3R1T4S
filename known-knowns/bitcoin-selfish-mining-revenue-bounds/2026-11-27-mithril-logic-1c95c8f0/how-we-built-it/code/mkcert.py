"""Make a certificate file: solve the SSP for the given variant at rho, at g slightly above g*
(so Z(g) < 0), round W*2^s to integers, write gzip text (header JSON + T+1 rows).
Also optionally write the greedy policy (for policy lower certificates).
usage: mkcert.py alpha_frac T rho_frac mode out.txt.gz [gfactor] [policy_out.txt.gz]"""
import sys, json, gzip, numpy as np
from fractions import Fraction as F
from ssp import SSP
alpha, T, rho, mode, out = F(sys.argv[1]), int(sys.argv[2]), F(sys.argv[3]), sys.argv[4], sys.argv[5]
gf = float(sys.argv[6]) if len(sys.argv) > 6 else 0.98
s = SSP(float(alpha), T, mode)
gstar, Zs = s.gain(float(rho))
# g = g* * gf.  Dual (upper) certificate needs g > g* (Z(g) < 0): gf < 1 when g* < 0, gf > 1 when g* > 0.
# Policy (lower) certificate needs g < g* (Z(g) > 0): gf < 1 when g* > 0.
g = gstar*gf
Z, sw, de = s.solve(float(rho), g)
print('alpha %s T %d rho %s mode %s: g* = %.12e, using g = %.12e, Z(g) = %.3e, sweeps %d, delta %.1e'
      % (alpha, T, rho, mode, gstar, g, Z, sw, de))
SC = 40
H = np.rint(s.W*2.0**SC).astype(np.int64)
assert np.abs(s.W).max()*2**SC < 2**62
with gzip.open(out, 'wt') as fh:
    fh.write(json.dumps({'format': 'ssz-dual-cert-v1', 'alpha': str(alpha), 'rho': str(rho), 'T': T,
                         'scale_log2': SC, 'label_invariant': True, 'built_with_mode': mode}) + '\n')
    for a in range(T+1):
        fh.write(' '.join(map(str, H[a].tolist())) + '\n')
print('wrote', out)
if len(sys.argv) > 7:
    pol = s.policy(float(rho), g)
    with gzip.open(sys.argv[7], 'wt') as fh:
        for a in range(T+1):
            fh.write(''.join(pol[a]) + '\n')
    print('wrote policy', sys.argv[7])
