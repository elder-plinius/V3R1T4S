#!/usr/bin/env python3
"""
neon_global_anchored_probe_r12.py

General r-prime exact Schroeder anchored engine (r = 9, 10, 11, ...),
testing the 17 surviving omega=10 vectors and 1 surviving omega=11 vector below
6,557,114,959,770,375 (and omega=9 vectors above 6.557e15!) to see how high we
can certify the NEW GLOBAL LOWER BOUND ON L for EVERY odd covering!
"""
import os
import sys
import time
from math import lcm
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import neon_exp_ladder_probe_r11 as ep

class GeneralExponentModel(ep.ExponentModel):
    """Same exact Schroeder model as ExponentModel, supporting ANY r >= 3 primes!"""
    def __init__(self, primes_later, exps, C7=Fraction(3, 2), taus_later=None, U_cut=8, V_cut=6):
        self.primes_later = tuple(primes_later)
        assert len(exps) == 2 + len(self.primes_later)
        assert len(taus_later) == len(self.primes_later) - 1
        self.exps = tuple(exps)
        v3, v5, v7 = exps[0], exps[1], exps[2]
        assert v3 is None or v3 >= 3
        assert v5 is None or v5 >= 2
        assert v7 is None or v7 >= 1

        self.v3, self.v5, self.v7 = v3, v5, v7
        self.v_later = exps[2:]

        self.P3 = Fraction(1, 2) if v3 is None else Fraction(3**v3 - 1, 2 * 3**v3)
        self.P5 = Fraction(1, 4) if v5 is None else Fraction(5**v5 - 1, 4 * 5**v5)
        self.P7 = Fraction(1, 6) if v7 is None else Fraction(7**v7 - 1, 6 * 7**v7)
        self.R0 = 135 * (1 - self.P3 - self.P5)

        self.Z_budget = Fraction(1, 2) if v3 is None else Fraction(3**(v3 - 3) - 1, 2 * 3**(v3 - 3))
        self.T_budget = Fraction(1, 20) if v5 is None else Fraction(5**(v5 - 2) - 1, 20 * 5**(v5 - 2))

        if v3 is None:
            self.u_pos = tuple((u, Fraction(2, 3**(u + 1))) for u in range(1, U_cut))
            self.u_tail_p = Fraction(1, 3**U_cut)
            self.u_tail_m = self.u_tail_p * (U_cut + Fraction(1, 2))
            self.u_has_pos = True
        elif v3 == 3:
            self.u_pos = ()
            self.u_tail_p = Fraction(0)
            self.u_tail_m = Fraction(0)
            self.u_has_pos = False
        else:
            umax = v3 - 3
            self.u_pos = tuple((u, Fraction(2, 3**(u + 1))) for u in range(1, umax)) + ((umax, Fraction(1, 3**umax)),)
            self.u_tail_p = Fraction(0)
            self.u_tail_m = Fraction(0)
            self.u_has_pos = True

        if v5 is None:
            self.v_pos = tuple((v, Fraction(4, 5**(v + 1))) for v in range(1, V_cut))
            self.v_tail_p = Fraction(1, 5**V_cut)
            self.v_tail_m = self.v_tail_p * (V_cut + Fraction(1, 4))
            self.v_has_pos = True
        else:
            vmax = v5 - 1
            self.v_pos = tuple((v, Fraction(4, 5**(v + 1))) for v in range(1, vmax)) + ((vmax, Fraction(1, 5**vmax)),)
            self.v_tail_p = Fraction(0)
            self.v_tail_m = Fraction(0)
            self.v_has_pos = True

        self.C7 = Fraction(C7)
        self.N7 = 1 / self.P7
        assert self.C7 * (1 - self.P7) >= 1 and self.C7 <= 7
        self.TAU7 = self.N7 * (1 - 1 / self.C7)
        self.BETA7 = self.N7 - self.TAU7
        self.W7_ext = self.N7 / 7
        self.W7_rem = 1 - self.W7_ext

        self.S_s = tuple(min(Fraction(1), self.C7 * Fraction(6 - s, 7)) for s in range(5))
        self.pi7_0_s = tuple(S - self.C7 / 7 for S in self.S_s)
        den_k = 1
        for x in self.pi7_0_s:
            den_k = lcm(den_k, x.denominator)
        self.kappa_den = den_k
        self.kappa_int = tuple(int(x * den_k) for x in self.pi7_0_s)

        norms = [self.N7]
        for p, vp in zip(self.primes_later[1:], self.v_later[1:]):
            Pp = Fraction(1, p - 1) if vp is None else Fraction(p**vp - 1, (p - 1) * p**vp)
            norms.append(1 / Pp)
        self.norms = tuple(norms)
        self.taus = (self.TAU7,) + tuple(Fraction(t) for t in taus_later)
        self.betas = tuple(n - t for n, t in zip(self.norms, self.taus))
        self.caps = tuple(n / b for n, b in zip(self.norms, self.betas))
        for p, t, n, C in zip(self.primes_later, self.taus, self.norms, self.caps):
            assert t >= 1 and t < n and C <= p, f"Invalid cap at p={p}: t={t}, n={n}, C={C}"

        M_CUT = int(max(self.taus)) + 2
        self.M_CUT = M_CUT

        self.pi7_pos = []
        if v7 is None:
            for j in range(1, M_CUT + 2):
                self.pi7_pos.append((j, self.C7 * Fraction(6, 7**(j + 1))))
            self.mean_1pJ7 = Fraction(1) + self.C7 / 6
        else:
            for j in range(1, v7):
                self.pi7_pos.append((j, self.C7 * Fraction(6, 7**(j + 1))))
            self.pi7_pos.append((v7, self.C7 * Fraction(1, 7**v7)))
            self.mean_1pJ7 = Fraction(1) + self.C7 * self.P7
        self.pi7_pos = tuple(self.pi7_pos)

        def build_dist(include_7):
            out = []
            dist = {1: Fraction(1)}
            mean = Fraction(1)
            for idx, (p, vp, C, n_p) in enumerate(zip(self.primes_later, self.v_later, self.caps, self.norms)):
                out.append((dict(dist), mean))
                if p == 7 and not include_7:
                    continue
                if vp is None:
                    steps = [(0, 1 - C / p)] + [(e, C * Fraction(p - 1, p**(e + 1))) for e in range(1, M_CUT)]
                else:
                    steps = (
                        [(0, 1 - C / p)]
                        + [(e, C * Fraction(p - 1, p**(e + 1))) for e in range(1, vp)]
                        + [(vp, C * Fraction(1, p**vp))]
                    )
                mean = mean * (1 + C / n_p)
                nd = {}
                for m_val, pr_m in dist.items():
                    for e, pr_e in steps:
                        nm = m_val * (e + 1)
                        if nm >= M_CUT:
                            break
                        nd[nm] = nd.get(nm, Fraction(0)) + pr_m * pr_e
                dist = nd
            return out

        self.full = build_dist(True)
        self.post7 = build_dist(False)
        self.rat_ts = tuple(sorted({t / m for t in self.taus for m in range(1, M_CUT) if m < t}))

    def check_all_32_basic(self):
        worst = None
        for a in (1, 2):
            for b in (2, 4):
                for c in (a, 3 - a):
                    for j in range(1, 5):
                        st = (a, b, c, -1, j, 0, 0, 0, -1)
                        R = self.exact_reserve(st)
                        env = self.eval_ord_envelope(st, xi=None, use_kappa=False)
                        S = sum(
                            self.stage_expectation(env, dist, mean, t, mult_scale=1) / bt
                            for (dist, mean), t, bt in zip(self.full, self.taus, self.betas)
                        )
                        m = R - S
                        if worst is None or m < worst[0]:
                            worst = (m, st, R, S)
        return worst


def main():
    t0 = time.time()
    P10 = (7, 11, 13, 17, 19, 23, 29, 31)
    P11 = (7, 11, 13, 17, 19, 23, 29, 31, 37)
    P9  = (7, 11, 13, 17, 19, 23, 29)

    print("=== TESTING 32-ROW BASIC CLOSURE FOR ALL SURVIVING omega=10, 11 (and omega=9) VECTORS ===")
    tests = [
        # omega = 11: the ONLY surviving vector below 6.557e15!
        ("11p (4,2,2,1^8) [ONLY surv]",      P11, (4,2,2,1,1,1,1,1,1,1,1), (4,4,6,8,12,16,18,22)),
        ("11p (5,2,2,1^8) [stronger!]",      P11, (5,2,2,1,1,1,1,1,1,1,1), (4,4,6,8,12,16,18,22)),
        ("11p (inf,2,2,1^8) [ALL v3!]",      P11, (None,2,2,1,1,1,1,1,1,1,1), (4,4,6,8,12,16,18,22)),
        ("11p (4,3,2,1^8) [17.5e15]",        P11, (4,3,2,1,1,1,1,1,1,1,1), (4,4,6,8,12,16,18,22)),
        # omega = 10: Pareto-maximal covers for ALL 17 surviving vectors below 6.557e15!
        ("10p (inf,inf,inf; 1^7) [ALL 3,5,7!]", P10, (None,None,None,1,1,1,1,1,1,1), (4,4,6,8,12,16,18)),
        ("10p (4,3,2,2,1^6) [5.21e15]",      P10, (4,3,2,2,1,1,1,1,1,1), (4,4,6,8,12,16,18)),
        ("10p (inf,2,inf,2,1^6)",            P10, (None,2,None,2,1,1,1,1,1,1), (4,4,6,8,12,16,18)),
        ("10p (inf,2,2,inf,1^6)",            P10, (None,2,2,None,1,1,1,1,1,1), (4,4,6,8,12,16,18)),
        ("10p (5,2,2,2,2,2,2,2,1,1)",        P10, (5,2,2,2,2,2,2,2,1,1), (4,4,6,8,12,16,18)),
        ("10p (6,4,3,1^7)",                  P10, (6,4,3,1,1,1,1,1,1,1), (4,4,6,8,12,16,18)),
        ("10p (3,inf^9) [81|L at w=10!]",    P10, (3,)+(None,)*9, (4,4,6,8,12,16,18)),
        # omega = 9: CAN WE KILL (5,3,2,2,2,1^4) = 6.557e15 itself?!
        ("9p (5,3,2,2,2,1^4) [6.557e15]",    P9,  (5,3,2,2,2,1,1,1,1), (4,4,6,8,12,16)),
        ("9p (inf,inf,inf,2,2,1^4)",         P9,  (None,None,None,2,2,1,1,1,1), (4,4,6,8,12,16)),
        ("9p (inf,inf,inf,inf,inf,1^4)",     P9,  (None,None,None,None,None,1,1,1,1), (4,4,6,8,12,16)),
    ]
    for name, ps, es, taus in tests:
        t1 = time.time()
        mod = GeneralExponentModel(ps, es, C7=Fraction(3, 2), taus_later=taus, U_cut=8, V_cut=6)
        m, st, R, S = mod.check_all_32_basic()
        tag = "BASIC-32 PASS!" if m > 0 else "needs tree"
        print(f"  {name:<36s} | min_basic={float(m):+9.5f} (R={float(R):.3f}) [{time.time()-t1:4.1f}s] {tag}")
        sys.stdout.flush()

    print(f"\nElapsed: {time.time()-t0:.1f}s")

if __name__ == "__main__":
    main()
