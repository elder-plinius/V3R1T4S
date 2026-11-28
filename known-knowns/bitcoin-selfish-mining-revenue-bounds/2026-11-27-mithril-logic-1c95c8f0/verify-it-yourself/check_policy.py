#!/usr/bin/env python3
"""Exact LOWER certificate for one stationary policy (Python standard library only).

Given a stationary policy pi (one action per (a,h), the same for every fork label f) and a bias vector
h(a,h,f) = H[a][h]/2^s, compute exactly   g_lo = min over ALL states s of  r(s,pi(s)) + sum P(s'|s,pi(s)) h(s') - h(s).
Then the long-run average reward of pi from any start state is >= g_lo (telescoping), so
  variant 'under'    (SSZ M_rho^T: truncating states adopt with reward -rho*h, identical to the untruncated
                      model M_rho for this policy): g_lo > 0  =>  REV(pi) > rho in the untruncated gamma=0 model,
                      so max REV > rho and no upper bound U <= rho can ever be certified, for any T.
  variant 'printed' / 'corrected' (N_rho^T): g_lo > 0 => optimal gain of N_rho^T is > 0 => no dual
                      certificate with g < 0 exists for N_rho^T at this rho and T.
Transitions/rewards as in check_cert.py.  Policy file: gzip text, T+1 lines of T+1 chars from {a,w,o}
(adopt, wait, override).  Usage: python3 check_policy.py CERT.txt.gz POLICY.txt.gz under|printed|corrected
"""
import sys, gzip
from fractions import Fraction as F
from check_cert import load, compensation

def main():
    hdr, H = load(sys.argv[1])
    with gzip.open(sys.argv[2], 'rt') as fh:
        P = [fh.readline().strip() for _ in range(hdr['T'] + 1)]
    variant = sys.argv[3]
    alpha, rho, T, s = F(hdr['alpha']), F(hdr['rho']), hdr['T'], hdr['scale_log2']
    an, ad = alpha.numerator, alpha.denominator; bn = ad - an
    rn, rd = rho.numerator, rho.denominator; S = 1 << s
    assert len(P) == T + 1 and all(len(r) == T + 1 for r in P)
    Z = an * H[1][0] + bn * H[0][1]
    lo, where, n = None, None, 0
    for a in range(T + 1):
        for h in range(T + 1):
            act = P[a][h]
            trunc = (a == T or h == T)
            if trunc:
                assert act == 'a', 'policy must adopt at truncating state %s' % ((a, h),)
                C = -rho * h if variant == 'under' else compensation(alpha, rho, T, a, h, variant)
                res = C + F(Z - ad * H[a][h], ad * S)
            else:
                if act == 'w':
                    R = rd * (an * H[a + 1][h] + bn * H[a][h + 1] - ad * H[a][h])
                elif act == 'a':
                    R = ad * S * (-h * rn) + rd * (Z - ad * H[a][h])
                elif act == 'o':
                    assert a > h, 'override infeasible at %s' % ((a, h),)
                    R = ad * S * ((h + 1) * (rd - rn)) + rd * (an * H[a - h][0] + bn * H[a - h - 1][1] - ad * H[a][h])
                else:
                    raise ValueError(act)
                res = F(R, ad * rd * S)
            n += 3          # same residual for f = 0, 1, 2 (wait at f=2 uses match transitions, same targets' h)
            if lo is None or res < lo:
                lo, where = res, (a, h, act)
    print('policy cert', sys.argv[1], 'variant', variant, 'alpha', alpha, 'rho', rho, 'T', T, 'states', n)
    print('exact min residual g_lo = %s (~%.9e) at %s' % (lo, float(lo), where))
    print('POLICY_GAIN_POSITIVE' if lo > 0 else 'POLICY_GAIN_NOT_POSITIVE')

if __name__ == '__main__':
    main()
