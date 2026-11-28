#!/usr/bin/env python3
"""Exact checker (Python standard library only) for average-reward dual certificates on SSZ's
over-paying MDP N_rho^T (arXiv 1507.06183, gamma = 0), rebuilt here from the paper's formulas.

MDP (SSZ Table 1, gamma = 0).  State (a, h, f), 0 <= a, h <= T, f in {0 irrelevant, 1 relevant, 2 active}.
Reward pair (x, y) is mapped to w_rho(x, y) = (1 - rho) x - rho y.
  adopt    : -> (1,0,0) w.p. alpha, (0,1,0) w.p. 1-alpha; reward (0, h)
  override : only if a > h; -> (a-h,0,0) alpha, (a-h-1,1,1) 1-alpha; reward (h+1, 0)
  wait     : f in {0,1}: -> (a+1,h,0) alpha, (a,h+1,1) 1-alpha; reward (0,0)
  wait (f=2) and match (only if f=1 and a >= h):
             -> (a+1,h,2) alpha, (a-h,1,1) gamma(1-alpha) = 0, (a,h+1,1) (1-gamma)(1-alpha); reward 0
             (the (h,0) reward sits on the gamma branch, probability 0)
  truncating states max(a,h) = T: adopt only, and its reward is replaced by the compensation
    a = T >= h :  (1-rho) * ( KK + ((a-h)/(1-2 alpha) + a + h) / 2 ),   K = alpha(1-alpha)/(1-2alpha)^2   [eq. (7)]
    h = T > a  :  (1 - q^d)(-rho h) + q^d (1-rho) (KK + E0),  q = alpha/(1-alpha), d = h - a, with
      variant 'printed'  : KK = K,  E0 = d/(1-2 alpha)              (exactly as printed: eq. (7) and (28))
      variant 'corrected': KK = 2K, E0 = h + alpha d/(1-2 alpha)    (both errata fixed, derivation in CLAIM.md:
                           Lemma 13 / eq. (22) E[last] = 2K + ...; eq. (28) E[a0 | return] = h + alpha d/(1-2alpha))
Certificate: bias h(a,h,f) = H[a][h] / 2^s (label-invariant), integers H read from the file.
For EVERY state and EVERY allowed action the checker computes the exact residual
  r_rho(s,a) + sum_s' P(s'|s,a) h(s') - h(s)
and reports the exact maximum g.  CERT_OK iff g < 0 (then every policy of N has gain <= g < 0).
Usage: python3 check_cert.py CERT.txt.gz [printed|corrected|both]
"""
import gzip, json, sys
from fractions import Fraction as F

def load(path):
    op = gzip.open if path.endswith('.gz') else open
    with op(path, 'rt') as fh:
        hdr = json.loads(fh.readline())
        H = [list(map(int, fh.readline().split())) for _ in range(hdr['T'] + 1)]
    T = hdr['T']
    assert len(H) == T + 1 and all(len(r) == T + 1 for r in H), 'bad H shape'
    return hdr, H

def compensation(alpha, rho, T, a, h, variant):
    K = alpha * (1 - alpha) / (1 - 2 * alpha) ** 2
    if a == T:                                       # T = a >= h : eq. (7)
        KK = K if variant == 'printed' else 2 * K      # corrected Lemma 13: E[last] = 2K + ...
        return (1 - rho) * (KK + F(1, 2) * (F(a - h) / (1 - 2 * alpha) + a + h))
    assert h == T and a < h
    d = h - a
    qd = (alpha / (1 - alpha)) ** d
    if variant == 'printed':
        KK, E0 = K, F(d) / (1 - 2 * alpha)
    elif variant == 'corrected':
        KK, E0 = 2 * K, h + alpha * d / (1 - 2 * alpha)
    else:
        raise ValueError(variant)
    return (1 - qd) * (-rho * h) + qd * (1 - rho) * (KK + E0)

def check(hdr, H, variant):
    alpha, rho, T, s = F(hdr['alpha']), F(hdr['rho']), hdr['T'], hdr['scale_log2']
    assert 0 < alpha < F(1, 2) and 0 < rho < 1
    an, ad = alpha.numerator, alpha.denominator
    rn, rd = rho.numerator, rho.denominator
    S = 1 << s
    bn = ad - an                                     # (1-alpha) = bn/ad
    Z = an * H[1][0] + bn * H[0][1]                  # ad * (sum_s' P_adopt h(s')) * S
    # integer residual R means residual = R / (ad*rd*S)
    best_int, best_where = None, None
    pairs = 0
    for a in range(T + 1):
        Ha, Ha1 = H[a], (H[a + 1] if a < T else None)
        for h in range(T + 1):
            if a == T or h == T:
                continue
            Hs = ad * Ha[h]
            cand = []
            waitv = rd * (an * Ha1[h] + bn * Ha[h + 1] - Hs)
            adoptv = ad * S * (-h * rn) + rd * (Z - Hs)
            ovv = None
            if a > h:
                ovv = ad * S * ((h + 1) * (rd - rn)) + rd * (an * H[a - h][0] + bn * H[a - h - 1][1] - Hs)
            for f in (0, 1, 2):
                # f=0,1 wait; f=2 wait uses match transitions; both -> same h values (label-invariant)
                cand.append((waitv, (a, h, f, 'wait')))
                cand.append((adoptv, (a, h, f, 'adopt')))
                if ovv is not None:
                    cand.append((ovv, (a, h, f, 'override')))
                if f == 1 and a >= h:
                    cand.append((waitv, (a, h, f, 'match')))
            pairs += len(cand)
            for v, w in cand:
                if best_int is None or v > best_int:
                    best_int, best_where = v, w
    best = F(best_int, ad * rd * S)
    # truncating states: adopt only, compensation reward
    for a in range(T + 1):
        for h in range(T + 1):
            if not (a == T or h == T):
                continue
            C = compensation(alpha, rho, T, a, h, variant)
            res = C + F(Z - ad * H[a][h], ad * S)
            for f in (0, 1, 2):
                pairs += 1
                if res > best:
                    best, best_where = res, (a, h, f, 'adopt(truncating)')
    return best, best_where, pairs

def main():
    path = sys.argv[1]
    variants = sys.argv[2] if len(sys.argv) > 2 else 'both'
    variants = ['printed', 'corrected'] if variants == 'both' else [variants]
    hdr, H = load(path)
    print('cert', path, 'alpha', hdr['alpha'], 'rho', hdr['rho'], 'T', hdr['T'], 'scale 2^%d' % hdr['scale_log2'])
    allok = True
    for v in variants:
        g, where, pairs = check(hdr, H, v)
        ok = g < 0
        allok &= ok
        print('variant %-9s pairs %d  max residual g = %s  (~%.9e) at %s  %s'
              % (v, pairs, g, float(g), where, 'CERT_OK' if ok else 'CERT_FAIL'))
    print('CERT_OK' if allok else 'CERT_FAIL')

if __name__ == '__main__':
    main()
