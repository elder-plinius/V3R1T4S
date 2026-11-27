#!/usr/bin/env python3
"""
neon_global_bound_probe_r12.py (v2, fixed Lemma U optimizer!)

Tests exact/float Lemma U (scalar distortion) across omega = 9, 10, 11, 12, 13
to determine the EXACT global lower bound on L for ALL odd coverings!
"""
import time
from fractions import Fraction

ODD_PRIMES = [
    3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73,
    79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157,
    163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241
]

def scalar_B_float(primes, exps, k0, Cs):
    r = len(primes)
    prod_th = 1.0
    sum_th = 0.0
    for m in range(k0):
        p = primes[m]
        e = exps[m]
        if e is None:
            th = 1.0 / (p - 2.0)
        else:
            pe = float(p ** e)
            th = (pe - 1.0) / ((p - 2.0) * pe + 1.0)
        prod_th *= (1.0 + th)
        sum_th += th
    B = prod_th - 1.0 - sum_th

    max_K = max(primes[k0:]) + 2
    dist = {1: 1.0}
    mean = 1.0
    for m in range(r):
        p = primes[m]
        e = exps[m]
        if m >= k0:
            C = Cs[m - k0]
            rho = 1.0 / (p - 1.0) if e is None else (1.0 - p ** (-e)) / (p - 1.0)
            delta = 1.0 - 1.0 / C
            if delta < rho - 1e-12 or C > p + 1e-12 or C <= 1.0:
                return 1e9
            thresh = delta / rho
            ex = rho * mean - delta
            for k, pk in dist.items():
                if k < thresh:
                    ex += pk * (delta - rho * k)
            B += C * ex
        if m == r - 1:
            break
        if m < k0:
            if e is None:
                denom = p - 2.0
                p_ge1 = (p - 1.0) / (p * denom)
                steps = [(0, 1.0 - p_ge1)]
                for t in range(1, max_K):
                    steps.append((t, (p - 1.0)**2 / (p**(t + 1) * denom)))
                mean *= (1.0 + 1.0 / (p - 2.0))
            else:
                denom = (p - 2.0) + p**(-e)
                p_ge = [((p - 1.0) * p**(-t)) / denom for t in range(1, e + 1)]
                steps = [(0, 1.0 - p_ge[0])]
                for t in range(1, e):
                    steps.append((t, p_ge[t - 1] - p_ge[t]))
                steps.append((e, p_ge[e - 1]))
                mean *= (1.0 + sum(p_ge))
        else:
            C = Cs[m - k0]
            if e is None:
                steps = [(0, 1.0 - C / p)]
                for t in range(1, max_K):
                    steps.append((t, C * (p - 1.0) / (p**(t + 1))))
                mean *= (1.0 + C / (p - 1.0))
            else:
                steps = [(0, 1.0 - C / p)]
                for t in range(1, e):
                    steps.append((t, C * (p - 1.0) / (p**(t + 1))))
                steps.append((e, C / (p**e)))
                mean *= (1.0 + C * (1.0 - p**(-e)) / (p - 1.0))
        nd = {}
        for k, pk in dist.items():
            for t, pt in steps:
                nk = k * (t + 1)
                if nk >= max_K:
                    break
                nd[nk] = nd.get(nk, 0.0) + pk * pt
        dist = nd
    return B

def optimize_scalar(primes, exps, early_stop=0.985):
    r = len(primes)
    best_B = 1e9
    best_cfg = None
    # Note: for k0=1, p_0=3 is uniform, p_1=5 gets cap C_1 around 2.0!
    # For k0=2, p_0=3, p_1=5 are uniform (giving th3*th5 = 1/3!), p_2=7 gets cap C_2 around 1.5!
    for k0 in (1, 2):
        Cs = []
        for m in range(k0, r):
            p = primes[m]
            e = exps[m]
            rho = 1.0 / (p - 1.0) if e is None else (1.0 - p**(-e)) / (p - 1.0)
            c_min = 1.0 / (1.0 - rho) + 1e-4
            # Schroeder-like starting caps:
            if p == 5: c0 = 2.0
            elif p == 7: c0 = 1.5
            elif p == 11: c0 = 1.67
            elif p == 13: c0 = 1.5
            elif p == 17: c0 = 1.6
            elif p == 19: c0 = 1.8
            elif p == 23: c0 = 2.2
            else: c0 = min(float(p) * 0.5, 2.5 + 0.05 * (p - 23))
            Cs.append(max(c_min + 0.02, min(float(p) - 0.01, c0)))
        cur_B = scalar_B_float(primes, exps, k0, Cs)
        for step in (0.4, 0.15, 0.05, 0.015):
            improved = True
            iters = 0
            while improved and iters < 3:
                improved = False
                iters += 1
                for idx in range(r - k0):
                    m = k0 + idx
                    p = primes[m]
                    e = exps[m]
                    rho = 1.0 / (p - 1.0) if e is None else (1.0 - p**(-e)) / (p - 1.0)
                    c_min = 1.0 / (1.0 - rho) + 1e-5
                    c_max = float(p)
                    base = Cs[idx]
                    best_c = base
                    for d in (-2, -1, 1, 2):
                        cand = base + d * step
                        if cand < c_min or cand > c_max:
                            continue
                        Cs[idx] = cand
                        v = scalar_B_float(primes, exps, k0, Cs)
                        if v < cur_B - 1e-7:
                            cur_B = v
                            best_c = cand
                            improved = True
                    Cs[idx] = best_c
                if cur_B < early_stop:
                    break
            if cur_B < early_stop:
                break
        if cur_B < best_B:
            best_B = cur_B
            best_cfg = (k0, list(Cs))
        if best_B < early_stop:
            break
    return best_B, best_cfg

def main():
    t0 = time.time()
    L_NEW9 = 3**5 * 5**3 * 7**2 * 11**2 * 13**2 * 17 * 19 * 23 * 29
    L_PUB = 168131152814625

    print("=== 1. SANITY CHECKS ON KNOWN SCALAR BENCHMARKS ===")
    p9 = (3,5,7,11,13,17,19,23,29)
    p10 = (3,5,7,11,13,17,19,23,29,31)
    p11 = (3,5,7,11,13,17,19,23,29,31,37)
    p12 = (3,5,7,11,13,17,19,23,29,31,37,41)
    p13 = (3,5,7,11,13,17,19,23,29,31,37,41,43)

    tests = [
        ("9p all-inf (exp ~1.1507)", p9, (None,)*9),
        ("9p e3<=2 (exp 0.8763)",    p9, (2,) + (None,)*8),
        ("9p (4,3,2,2,1^5) [PUB]",   p9, (4,3,2,2,1,1,1,1,1)),
        ("9p (4,3,2,1^6)",           p9, (4,3,2,1,1,1,1,1,1)),
        ("9p (5,3,2,1^6)",           p9, (5,3,2,1,1,1,1,1,1)),
        ("9p (4,4,2,1^6)",           p9, (4,4,2,1,1,1,1,1,1)),
        ("9p (4,3,3,1^6)",           p9, (4,3,3,1,1,1,1,1,1)),
        ("9p (5,3,2,2,2,1^4) [NEW9]",p9, (5,3,2,2,2,1,1,1,1)),
        ("10p (3,2,2,1^7)",          p10,(3,2,2,1,1,1,1,1,1,1)),
        ("10p (4,2,2,1^7)",          p10,(4,2,2,1,1,1,1,1,1,1)),
        ("10p (3,3,2,1^7)",          p10,(3,3,2,1,1,1,1,1,1,1)),
        ("10p (4,3,2,1^7)",          p10,(4,3,2,1,1,1,1,1,1,1)),
        ("10p (4,3,2,2,1^6)",        p10,(4,3,2,2,1,1,1,1,1,1)),
        ("10p (5,3,2,1^7)",          p10,(5,3,2,1,1,1,1,1,1,1)),
        ("10p (4,4,2,1^7)",          p10,(4,4,2,1,1,1,1,1,1,1)),
        ("10p (4,3,3,1^7)",          p10,(4,3,3,1,1,1,1,1,1,1)),
        ("10p (3,inf^9)",            p10,(3,) + (None,)*9),
        ("10p (inf,2,inf^8)",        p10,(None,2) + (None,)*8),
        ("11p (3,2,1^9)",            p11,(3,2,1,1,1,1,1,1,1,1,1)),
        ("11p (4,2,1^9)",            p11,(4,2,1,1,1,1,1,1,1,1,1)),
        ("11p (3,3,1^9)",            p11,(3,3,1,1,1,1,1,1,1,1,1)),
        ("11p (3,2,2,1^8)",          p11,(3,2,2,1,1,1,1,1,1,1,1)),
        ("11p (4,2,2,1^8)",          p11,(4,2,2,1,1,1,1,1,1,1,1)),
        ("11p (3,3,2,1^8)",          p11,(3,3,2,1,1,1,1,1,1,1,1)),
        ("11p (4,3,2,1^8)",          p11,(4,3,2,1,1,1,1,1,1,1,1)),
        ("11p (inf,inf,1,inf^8)",    p11,(None,None,1)+(None,)*8),
        ("12p (3,1^11)",             p12,(3,)+(1,)*11),
        ("12p (4,1^11)",             p12,(4,)+(1,)*11),
        ("12p (3,2,1^10)",           p12,(3,2)+(1,)*10),
        ("12p (inf,1,inf^10)",       p12,(None,1)+(None,)*10),
        ("12p (4,1,inf^10)",         p12,(4,1)+(None,)*10),
        ("12p (5,1,1,1^9)",          p12,(5,)+(1,)*11),
        ("13p (2,1^12)",             p13,(2,)+(1,)*12),
        ("13p (3,1^12)",             p13,(3,)+(1,)*12),
    ]
    for name, ps, es in tests:
        B, cfg = optimize_scalar(ps, es, early_stop=0.0)
        L_str = "-"
        if all(x is not None for x in es):
            L = 1
            for p, e in zip(ps, es): L *= p**e
            L_str = f"{L:>21,}"
        tag = "KILL" if B < 1.0 else "SURV"
        print(f"  {name:<28s} | L={L_str} | B={B:.6f} (k0={cfg[0]}) {tag}")

    print(f"\nDone in {time.time()-t0:.2f}s")

if __name__ == "__main__":
    main()
