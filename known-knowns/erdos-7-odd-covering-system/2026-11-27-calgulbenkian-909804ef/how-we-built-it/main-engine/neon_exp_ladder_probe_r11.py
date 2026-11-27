#!/usr/bin/env python3
"""
neon_exp_ladder_probe_r11.py

Exact rational Schroeder anchored-distortion evaluator for ARBITRARY finite or infinite
exponent vectors (v3, v5, v7, v11, v13, v17, v19, v23, v29) (None = infinity),
using the exact int64 16-state DP kernel libgeom135_r11.dylib (built from geom135_r11.c).

Evaluates the hardest canonical State A1 (and other critical anchor states) with:
  - exact ordinary stage bounds
  - exact padded stage 7 + direct positive-sum first-hit stages 11..29 (pure3 terminal)
  - exact fixed-165 at stage 11 (closing terminal)
  - optional threshold/cap optimization (including C7 != 3/2!)
"""
import os
import sys
import time
import ctypes
from fractions import Fraction
from functools import lru_cache

HERE = os.path.dirname(os.path.abspath(__file__))
LIB_PATH = os.path.join(HERE, "libgeom135_r11.dylib")

_lib = ctypes.CDLL(LIB_PATH)
_lib.geom135_batch.argtypes = [
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_int),
    ctypes.POINTER(ctypes.c_int64),
    ctypes.POINTER(ctypes.c_int64),
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_int64),
    ctypes.POINTER(ctypes.c_int64),
]
_lib.geom135_batch.restype = None


def geom_batch(xs, a_w, off, queries):
    n = len(xs)
    nq = len(queries)
    c_xs = (ctypes.c_int * n)(*xs)
    c_aw = (ctypes.c_int64 * n)(*a_w)
    c_off = (ctypes.c_int64 * n)(*off)
    flat_q = []
    for q in queries:
        flat_q.extend(q)
    c_q = (ctypes.c_int64 * (8 * nq))(*flat_q)
    c_out = (ctypes.c_int64 * nq)()
    _lib.geom135_batch(n, c_xs, c_aw, c_off, nq, c_q, c_out)
    return [int(c_out[i]) for i in range(nq)]


PRIMES_LATER = (7, 11, 13, 17, 19, 23, 29)


@lru_cache(None)
def core_cells(a, b, r):
    return tuple(
        x for x in range(135)
        if x % 3 != 0 and x % 9 != 1 and x % 27 != b
        and x % 5 != 0 and x % 15 != a
        and (r < 0 or x % 45 != r)
    )


def s_counts(xs, xi):
    x3, x5, x9, x15 = xi
    return tuple((x % 3 == x3) + (x % 5 == x5) + (x % 9 == x9) + (x % 15 == x15) for x in xs)


class ExponentModel:
    """
    Exact Schroeder anchored model for exps = (v3, v5, v7, v11, v13, v17, v19, v23, v29),
    where each entry is an int >= 1 (v3 >= 3, v5 >= 2, v7 >= 1) or None (for infinity).
    """
    def __init__(self, exps, C7=Fraction(3, 2), taus_later=(4, 4, 6, 8, 12, 16), U_cut=10, V_cut=8):
        assert len(exps) == 9
        self.exps = tuple(exps)
        v3, v5, v7 = exps[0], exps[1], exps[2]
        assert v3 is None or v3 >= 3
        assert v5 is None or v5 >= 2
        assert v7 is None or v7 >= 1

        self.v3, self.v5, self.v7 = v3, v5, v7
        self.v_later = exps[2:]  # for 7, 11, 13, 17, 19, 23, 29

        self.P3 = Fraction(1, 2) if v3 is None else Fraction(3**v3 - 1, 2 * 3**v3)
        self.P5 = Fraction(1, 4) if v5 is None else Fraction(5**v5 - 1, 4 * 5**v5)
        self.P7 = Fraction(1, 6) if v7 is None else Fraction(7**v7 - 1, 6 * 7**v7)
        self.R0 = 135 * (1 - self.P3 - self.P5)

        self.Z_budget = Fraction(1, 2) if v3 is None else Fraction(3**(v3 - 3) - 1, 2 * 3**(v3 - 3))
        self.T_budget = Fraction(1, 20) if v5 is None else Fraction(5**(v5 - 2) - 1, 20 * 5**(v5 - 2))

        # Exact (u, v) positive atoms + exact infinite remainder mass/mean if None
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

        # Stage 7
        self.C7 = Fraction(C7)
        self.N7 = 1 / self.P7
        assert self.C7 * (1 - self.P7) >= 1 and self.C7 <= 7
        self.TAU7 = self.N7 * (1 - 1 / self.C7)
        self.BETA7 = self.N7 - self.TAU7
        self.W7_ext = self.N7 / 7
        self.W7_rem = 1 - self.W7_ext

        # Charged 7-fibre live mass S_s = min(1, C7*(6-s)/7), Case-2 safe for all v7 >= 1
        self.S_s = tuple(min(Fraction(1), self.C7 * Fraction(6 - s, 7)) for s in range(5))
        assert all(S >= self.C7 / 7 for S in self.S_s), f"C7={self.C7} violates S_4 >= C7/7"
        self.pi7_0_s = tuple(S - self.C7 / 7 for S in self.S_s)

        # Normalize pi7_0_s to common integer denominator
        den_k = 1
        for x in self.pi7_0_s:
            from math import lcm
            den_k = lcm(den_k, x.denominator)
        self.kappa_den = den_k
        self.kappa_int = tuple(int(x * den_k) for x in self.pi7_0_s)

        # Positive J7 atoms (exact up to j_cut, plus tail for v7 = None)
        self.pi7_pos = []
        if v7 is None:
            for j in range(1, 20):
                self.pi7_pos.append((j, self.C7 * Fraction(6, 7**(j + 1))))
            self.mean_1pJ7 = Fraction(1) + self.C7 / 6
        else:
            for j in range(1, v7):
                self.pi7_pos.append((j, self.C7 * Fraction(6, 7**(j + 1))))
            self.pi7_pos.append((v7, self.C7 * Fraction(1, 7**v7)))
            self.mean_1pJ7 = Fraction(1) + self.C7 * self.P7
        self.pi7_pos = tuple(self.pi7_pos)

        # Later stages 7, 11, 13, 17, 19, 23, 29
        norms = [self.N7]
        for p, vp in zip(PRIMES_LATER[1:], self.v_later[1:]):
            Pp = Fraction(1, p - 1) if vp is None else Fraction(p**vp - 1, (p - 1) * p**vp)
            norms.append(1 / Pp)
        self.norms = tuple(norms)
        self.taus = (self.TAU7,) + tuple(Fraction(t) for t in taus_later)
        self.betas = tuple(n - t for n, t in zip(self.norms, self.taus))
        self.caps = tuple(n / b for n, b in zip(self.norms, self.betas))
        for p, t, n, C in zip(PRIMES_LATER, self.taus, self.norms, self.caps):
            assert t >= 1 and t < n and C <= p, f"Invalid cap at p={p}: t={t}, n={n}, C={C}"

        # Build exact distributions of M_q (full and post-7) up to M_CUT > max(taus)
        M_CUT = int(max(self.taus)) + 2
        self.M_CUT = M_CUT

        def build_dist(include_7):
            out = []
            dist = {1: Fraction(1)}
            mean = Fraction(1)
            for idx, (p, vp, C, n_p) in enumerate(zip(PRIMES_LATER, self.v_later, self.caps, self.norms)):
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

    def exact_reserve(self, state):
        a, b, c, r, j, d, k, i_e, z = state
        zz = self.Z_budget if z >= 0 else Fraction(0)

        def D(h):
            return (Fraction(1, 5) if h == c else Fraction(0)) + (self.T_budget if h == j else Fraction(0))

        g15 = 3 * (a == 1) + (b % 3 == a % 3) + (zz if (z >= 0 and z % 3 == a % 3) else Fraction(0))
        R = self.R0 + g15 + (9 - g15) * D(a)
        if r >= 0:
            g45 = Fraction(1 if b % 9 == r % 9 else 0) + (zz if (z >= 0 and z % 9 == r % 9) else Fraction(0))
            R += g45 + (3 - g45) * D(r % 5)
        if d != 0:
            cs = core_cells(a, b, r)
            B_mass = sum(
                (1 - (zz if x % 27 == z else Fraction(0)))
                for x in cs if x % 3 == d and x % 5 == k
            )
            R += Fraction(9, 5) - B_mass * (Fraction(1, 5) - i_e * self.T_budget)
        return R

    def cell_weight_blocks(self, state):
        from math import lcm
        a, b, c, r, j, d, k, i_e, z = state
        xs = core_cells(a, b, r)
        # w3_0(x) = (1 - z_x) if not u_has_pos else (2/3 - z_x)
        w3_fr = [
            (Fraction(1) if not self.u_has_pos else Fraction(2, 3))
            - (self.Z_budget if (z >= 0 and x % 27 == z) else Fraction(0))
            for x in xs
        ]
        w5_fr = [
            Fraction(4, 5)
            - (Fraction(1, 5) if x % 5 == c else Fraction(0))
            - (self.T_budget if x % 5 == j else Fraction(0))
            - ((Fraction(1, 5) - i_e * self.T_budget) if (d != 0 and x % 3 == d and x % 5 == k) else Fraction(0))
            for x in xs
        ]
        assert all(w > 0 for w in w3_fr) and all(w > 0 for w in w5_fr)
        d3 = 1
        for w in w3_fr:
            d3 = lcm(d3, w.denominator)
        d5 = 1
        for w in w5_fr:
            d5 = lcm(d5, w.denominator)
        w3_int = [int(w * d3) for w in w3_fr]
        w5_int = [int(w * d5) for w in w5_fr]
        blocks = {
            (False, False): ([w3_int[i] * w5_int[i] for i in range(len(xs))], d3 * d5),
            (False, True):  (w3_int, d3),
            (True, False):  (w5_int, d5),
            (True, True):   ([1] * len(xs), 1),
        }
        return xs, blocks

    def eval_ord_envelope(self, state, xi=None, use_kappa=False):
        xs, blocks = self.cell_weight_blocks(state)
        sc = s_counts(xs, xi) if use_kappa else None
        n = len(xs)
        zeros = [0] * n
        M_tot = Fraction(0)
        W_tot = Fraction(0)
        F_vals = {t: Fraction(0) for t in self.rat_ts}

        # Exact positive-atom combinations + exact linear tail if u or v infinite
        u_modes = (False, True) if self.u_has_pos else (False,)
        v_modes = (False, True)

        # Precompute block stats (tot_w, h_g, mx_w)
        blk_stats = {}
        for upos in u_modes:
            for vpos in v_modes:
                aw_base, den_blk = blocks[(upos, vpos)]
                if use_kappa:
                    aw = [aw_base[i] * self.kappa_int[sc[i]] for i in range(n)]
                    den_tot = den_blk * self.kappa_den
                else:
                    aw = aw_base
                    den_tot = den_blk
                tot_w = sum(aw)
                mx_w = max(aw)
                h_g = []
                for g in (3, 9, 27, 5, 15, 45):
                    acc = {}
                    for x, w in zip(xs, aw):
                        acc[x % g] = acc.get(x % g, 0) + w
                    h_g.append(max(acc.values()))
                blk_stats[(upos, vpos)] = (aw, den_tot, tot_w, mx_w, h_g)

                u_atoms = self.u_pos if upos else ((0, Fraction(1)),)
                v_atoms = self.v_pos if vpos else ((0, Fraction(1)),)
                queries = []
                q_meta = []
                for u, pu in u_atoms:
                    for v, pv in v_atoms:
                        w_uv = pu * pv
                        M_tot += w_uv * Fraction(tot_w, den_tot)
                        lin_uv = (
                            tot_w
                            + h_g[0] + h_g[1] + (1 + u) * h_g[2]
                            + (1 + v) * (h_g[3] + h_g[4] + h_g[5])
                            + (1 + u) * (1 + v) * mx_w
                        )
                        W_tot += w_uv * Fraction(lin_uv, den_tot)
                        for t in self.rat_ts:
                            qt, pt = t.denominator, t.numerator
                            queries.append((
                                qt - pt, qt, qt, qt * (1 + u),
                                qt * (1 + v), qt * (1 + v), qt * (1 + v),
                                qt * (1 + u) * (1 + v),
                            ))
                            q_meta.append((t, w_uv, qt))
                if queries:
                    res = geom_batch(xs, aw, zeros, queries)
                    for (t, w_uv, qt), val in zip(q_meta, res):
                        F_vals[t] += w_uv * Fraction(val, qt * den_tot)

        # Exact linear tail contribution outside [0, U_cut) x [0, V_cut) (only nonzero if v3 or v5 is None)
        def add_linear_tail(upos, vpos, p_u, m_u, p_v, m_v):
            nonlocal M_tot, W_tot
            if p_u == 0 or p_v == 0:
                return
            _, den_tot, tot_w, mx_w, h_g = blk_stats[(upos, vpos)]
            p_uv = p_u * p_v
            # E[1+u] = p_u + m_u, E[1+v] = p_v + m_v
            eu1 = p_u + m_u
            ev1 = p_v + m_v
            M_add = p_uv * Fraction(tot_w, den_tot)
            W_add = (
                p_uv * (tot_w + h_g[0] + h_g[1])
                + eu1 * p_v * h_g[2]
                + p_u * ev1 * (h_g[3] + h_g[4] + h_g[5])
                + eu1 * ev1 * mx_w
            ) / den_tot
            M_tot += M_add
            W_tot += W_add
            for t in self.rat_ts:
                # Conservative exact upper bound (1 - t + s)_+ <= 1 + s outside box!
                F_vals[t] += W_add

        if self.u_tail_p > 0:
            # u in tail, v = 0
            add_linear_tail(True, False, self.u_tail_p, self.u_tail_m, Fraction(1), Fraction(0))
            # u in tail, v in v_pos
            vp_sum = sum(pv for _, pv in self.v_pos)
            vm_sum = sum(v * pv for v, pv in self.v_pos)
            add_linear_tail(True, True, self.u_tail_p, self.u_tail_m, vp_sum, vm_sum)
            # u in tail, v in tail
            if self.v_tail_p > 0:
                add_linear_tail(True, True, self.u_tail_p, self.u_tail_m, self.v_tail_p, self.v_tail_m)
        if self.v_tail_p > 0:
            # u = 0, v in tail
            add_linear_tail(False, True, Fraction(1), Fraction(0), self.v_tail_p, self.v_tail_m)
            # u in u_pos, v in tail
            if self.u_has_pos:
                up_sum = sum(pu for _, pu in self.u_pos)
                um_sum = sum(u * pu for u, pu in self.u_pos)
                add_linear_tail(True, True, up_sum, um_sum, self.v_tail_p, self.v_tail_m)

        return M_tot, W_tot, F_vals

    def stage_expectation(self, env, dist, mean, tau, mult_scale=1):
        M_tot, W_tot, F_vals = env
        low_sum = Fraction(0)
        low_p = Fraction(0)
        low_m = Fraction(0)
        for m, pr in dist.items():
            mm = mult_scale * m
            if mm < tau:
                low_sum += pr * mm * F_vals[tau / mm]
                low_p += pr
                low_m += pr * mm
        rem_mean = mult_scale * mean - low_m
        rem_p = 1 - low_p
        return low_sum + rem_mean * W_tot - tau * rem_p * M_tot

    def eval_stage7_padded(self, state, xi):
        from math import lcm
        xs, blocks = self.cell_weight_blocks(state)
        sc = s_counts(xs, xi)
        # (R_7 + W7_ext * s - (TAU7 - 1))_+ / BETA7
        D = lcm(self.W7_ext.denominator, self.W7_rem.denominator, (self.TAU7 - 1).denominator)
        w_ext_i = int(self.W7_ext * D)
        w_rem_i = int(self.W7_rem * D)
        sh_i = -int((self.TAU7 - 1) * D)
        off = [w_ext_i * s for s in sc]

        u_modes = (False, True) if self.u_has_pos else (False,)
        tot = Fraction(0)
        blk_stats = {}
        for upos in u_modes:
            u_atoms = self.u_pos if upos else ((0, Fraction(1)),)
            for vpos in (False, True):
                v_atoms = self.v_pos if vpos else ((0, Fraction(1)),)
                aw, den_blk = blocks[(upos, vpos)]
                queries = []
                weights = []
                for u, pu in u_atoms:
                    for v, pv in v_atoms:
                        queries.append((
                            sh_i,
                            w_rem_i, w_rem_i, D * (1 + u),
                            D * v + w_rem_i, D * v + w_rem_i, D * (1 + v),
                            D * (1 + u) * (1 + v),
                        ))
                        weights.append(pu * pv)
                if queries:
                    res = geom_batch(xs, aw, off, queries)
                    for w_uv, val in zip(weights, res):
                        tot += w_uv * Fraction(val, D * den_blk)
                if self.u_tail_p > 0 or self.v_tail_p > 0:
                    # precompute linear upper bound for tail: (R_7 + W7_ext*s - (TAU7-1))_+ <= R_7 + W7_ext*s
                    s_w = sum(aw[i] * sc[i] for i in range(len(xs)))
                    mx_w = max(aw)
                    h_g = []
                    for g in (3, 9, 27, 5, 15, 45):
                        acc = {}
                        for x, w in zip(xs, aw):
                            acc[x % g] = acc.get(x % g, 0) + w
                        h_g.append(max(acc.values()))
                    blk_stats[(upos, vpos)] = (den_blk, s_w, mx_w, h_g)

        def add_pad_tail(upos, vpos, p_u, m_u, p_v, m_v):
            nonlocal tot
            if p_u == 0 or p_v == 0:
                return
            den_blk, s_w, mx_w, h_g = blk_stats[(upos, vpos)]
            p_uv = p_u * p_v
            eu1 = p_u + m_u
            ev1 = p_v + m_v
            # R_7 <= W7_rem*(h3+h9) + (1+u)*h27 + (v+W7_rem)*(h5+h15) + (1+v)*h45 + (1+u)(1+v)*mx + W7_ext*s_w
            val = (
                p_uv * (self.W7_ext * s_w + self.W7_rem * (h_g[0] + h_g[1] + h_g[3] + h_g[4]))
                + eu1 * p_v * h_g[2]
                + p_u * m_v * (h_g[3] + h_g[4])
                + p_u * ev1 * h_g[5]
                + eu1 * ev1 * mx_w
            ) / den_blk
            tot += val

        if self.u_tail_p > 0:
            add_pad_tail(True, False, self.u_tail_p, self.u_tail_m, Fraction(1), Fraction(0))
            vp_sum = sum(pv for _, pv in self.v_pos)
            vm_sum = sum(v * pv for v, pv in self.v_pos)
            add_pad_tail(True, True, self.u_tail_p, self.u_tail_m, vp_sum, vm_sum)
            if self.v_tail_p > 0:
                add_pad_tail(True, True, self.u_tail_p, self.u_tail_m, self.v_tail_p, self.v_tail_m)
        if self.v_tail_p > 0:
            add_pad_tail(False, True, Fraction(1), Fraction(0), self.v_tail_p, self.v_tail_m)
            if self.u_has_pos:
                up_sum = sum(pu for _, pu in self.u_pos)
                um_sum = sum(u * pu for u, pu in self.u_pos)
                add_pad_tail(True, True, up_sum, um_sum, self.v_tail_p, self.v_tail_m)

        return tot / self.BETA7

    def eval_fixed165(self, state, xi, eta):
        from math import lcm
        xs, blocks = self.cell_weight_blocks(state)
        sc = s_counts(xs, xi)
        tau11 = self.taus[1]
        beta11 = self.betas[1]
        w165 = self.norms[1] / 11  # normalized weight of 165-class at stage 11!
        D = lcm(w165.denominator, tau11.denominator)
        w165_i = int(w165 * D)
        tau11_i = int(tau11 * D)
        off = [w165_i if x % 15 == eta else 0 for x in xs]

        # Build exact m = 1 + J7 distribution (m=1 with kappa, m>=2 up to < tau11 exact, rest linear)
        env_unpad = self.eval_ord_envelope(state, xi=None, use_kappa=False)
        M_tot, W_tot, _ = env_unpad

        u_modes = (False, True) if self.u_has_pos else (False,)
        tot = Fraction(0)

        # Terms with m < tau11
        low_p = self.pi7_0_s[0]  # placeholder, we track exact tail separately!
        # Actually easier: sum m = 1 (kappa) + all (j, pj) in pi7_pos with 1+j < tau11;
        # for m >= tau11, use linear unpadded bound (m * W_tot - tau11 * M_tot) (strictly valid since
        # 165 is inside c15 and m >= tau11 makes hinge linear)!
        used_pos_p = Fraction(0)
        used_pos_m = Fraction(0)
        m_list = [(1, True, Fraction(1))]
        for j, pj in self.pi7_pos:
            m = 1 + j
            if m < tau11:
                m_list.append((m, False, pj))
                used_pos_p += pj
                used_pos_m += m * pj

        for m, use_kap, m_wt in m_list:
            shift = D * m - tau11_i
            mD = D * m
            blk_stats = {}
            for upos in u_modes:
                u_atoms = self.u_pos if upos else ((0, Fraction(1)),)
                for vpos in (False, True):
                    v_atoms = self.v_pos if vpos else ((0, Fraction(1)),)
                    aw_base, den_blk = blocks[(upos, vpos)]
                    if use_kap:
                        aw = [aw_base[i] * self.kappa_int[sc[i]] for i in range(len(xs))]
                        den_tot = den_blk * self.kappa_den
                    else:
                        aw = aw_base
                        den_tot = den_blk
                    queries = []
                    weights = []
                    for u, pu in u_atoms:
                        for v, pv in v_atoms:
                            c15 = mD * (1 + v) - w165_i
                            assert c15 >= 0
                            queries.append((
                                shift,
                                mD, mD, mD * (1 + u),
                                mD * (1 + v), c15, mD * (1 + v),
                                mD * (1 + u) * (1 + v),
                            ))
                            weights.append(pu * pv)
                    if queries:
                        res = geom_batch(xs, aw, off, queries)
                        for w_uv, val in zip(weights, res):
                            tot += m_wt * w_uv * Fraction(val, D * den_tot)
                    if self.u_tail_p > 0 or self.v_tail_p > 0:
                        tot_w = sum(aw)
                        mx_w = max(aw)
                        h_g = []
                        for g in (3, 9, 27, 5, 15, 45):
                            acc = {}
                            for x, w in zip(xs, aw):
                                acc[x % g] = acc.get(x % g, 0) + w
                            h_g.append(max(acc.values()))
                        blk_stats[(upos, vpos)] = (den_tot, tot_w, mx_w, h_g)

            if self.u_tail_p > 0 or self.v_tail_p > 0:
                def add_165_tail(upos, vpos, p_u, m_u, p_v, m_v):
                    nonlocal tot
                    if p_u == 0 or p_v == 0:
                        return
                    den_tot, tot_w, mx_w, h_g = blk_stats[(upos, vpos)]
                    p_uv = p_u * p_v
                    eu1 = p_u + m_u
                    ev1 = p_v + m_v
                    W_add = (
                        p_uv * (tot_w + h_g[0] + h_g[1])
                        + eu1 * p_v * h_g[2]
                        + p_u * ev1 * (h_g[3] + h_g[4] + h_g[5])
                        + eu1 * ev1 * mx_w
                    ) / den_tot
                    tot += m_wt * m * W_add
                if self.u_tail_p > 0:
                    add_165_tail(True, False, self.u_tail_p, self.u_tail_m, Fraction(1), Fraction(0))
                    vp_sum = sum(pv for _, pv in self.v_pos)
                    vm_sum = sum(v * pv for v, pv in self.v_pos)
                    add_165_tail(True, True, self.u_tail_p, self.u_tail_m, vp_sum, vm_sum)
                    if self.v_tail_p > 0:
                        add_165_tail(True, True, self.u_tail_p, self.u_tail_m, self.v_tail_p, self.v_tail_m)
                if self.v_tail_p > 0:
                    add_165_tail(False, True, Fraction(1), Fraction(0), self.v_tail_p, self.v_tail_m)
                    if self.u_has_pos:
                        up_sum = sum(pu for _, pu in self.u_pos)
                        um_sum = sum(u * pu for u, pu in self.u_pos)
                        add_165_tail(True, True, up_sum, um_sum, self.v_tail_p, self.v_tail_m)

        # Remaining m >= tau11 tail of (1 + J_7):
        # Total positive J7 probability is C7 / 7; total mean of (1+J7) on J7>=1 is mean_1pJ7 - (1 - C7/7)
        rem_p = self.C7 / 7 - used_pos_p
        rem_m = (self.mean_1pJ7 - (1 - self.C7 / 7)) - used_pos_m
        if rem_p > 0:
            tot += rem_m * W_tot - tau11 * rem_p * M_tot

        return tot / beta11

    def eval_A1(self, state=(2, 4, 1, 8, 1, 2, 1, 0, 13), xi=(1, 4, 7, 14), eta=14):
        R = self.exact_reserve(state)
        env_unpad = self.eval_ord_envelope(state, xi=None, use_kappa=False)
        env_kap = self.eval_ord_envelope(state, xi=xi, use_kappa=True)
        l7 = self.eval_stage7_padded(state, xi)

        # Positive J7 tail for stages 11..29
        Ls = [l7]
        for q in range(1, len(PRIMES_LATER)):
            dist_p7, mean_p7 = self.post7[q]
            t_q, b_q = self.taus[q], self.betas[q]
            j0 = self.stage_expectation(env_kap, dist_p7, mean_p7, t_q, mult_scale=1)
            jpos = Fraction(0)
            used_p = Fraction(0)
            used_m = Fraction(0)
            for j, pj in self.pi7_pos:
                mm = 1 + j
                if mm < t_q:
                    jpos += pj * self.stage_expectation(env_unpad, dist_p7, mean_p7, t_q, mult_scale=mm)
                    used_p += pj
                    used_m += mm * pj
            rem_p = self.C7 / 7 - used_p
            rem_m = (self.mean_1pJ7 - (1 - self.C7 / 7)) - used_m
            if rem_p > 0:
                M_tot, W_tot, _ = env_unpad
                jpos += rem_m * mean_p7 * W_tot - t_q * rem_p * M_tot
            Ls.append((j0 + jpos) / b_q)

        l11_165 = self.eval_fixed165(state, xi, eta)
        Ls_165 = [Ls[0], l11_165] + Ls[2:]
        return R, Ls, Ls_165


def main():
    t0 = time.time()
    print("=== EXACT EXPONENT LADDER PROBE AT HARDEST STATE A1 ===")
    print("State A1 = (2,4,1,8,1,2,1,0,13), xi=(1,4,7,14), eta=14\n")

    # Sanity check against known (4,3,2) exact values!
    m432 = ExponentModel((4, 3, 2, None, None, None, None, None, None))
    R, Ls, Ls165 = m432.eval_A1()
    print(f"[SANITY (4,3,2)] R={float(R):.10f}, pure3_margin={float(R-sum(Ls)):+.10f} (exp +0.1502277970), 165_margin={float(R-sum(Ls165)):+.10f} (exp +0.4291888360)")
    assert abs(float(R - sum(Ls)) - 0.1502277970) < 1e-9
    assert abs(float(R - sum(Ls165)) - 0.4291888360) < 1e-9

    # Sanity check against (inf, inf, inf)
    minf = ExponentModel((None, None, None, None, None, None, None, None, None), taus_later=(4, 4, 8, 8, 12, 16))
    R_i, Ls_i, Ls165_i = minf.eval_A1()
    print(f"[SANITY (inf,inf,inf)] R={float(R_i):.6f}, pure3_sum={float(sum(Ls_i)):.6f}, 165_sum={float(sum(Ls165_i)):.6f} (exp ~36.5524)\n")

    cases = [
        ("(4,3,2) [baseline]",       (4, 3, 2, None, None, None, None, None, None)),
        ("(4,4,2) [step v5: 3->4]",  (4, 4, 2, None, None, None, None, None, None)),
        ("(4,5,2) [v5=5]",           (4, 5, 2, None, None, None, None, None, None)),
        ("(4,inf,2) [v5=inf]",       (4, None, 2, None, None, None, None, None, None)),
        ("(4,3,3) [step v7: 2->3]",  (4, 3, 3, None, None, None, None, None, None)),
        ("(4,3,inf) [v7=inf]",       (4, 3, None, None, None, None, None, None, None)),
        ("(4,4,3) [v5=4,v7=3]",      (4, 4, 3, None, None, None, None, None, None)),
        ("(4,inf,inf) [force 3^5]",  (4, None, None, None, None, None, None, None, None)),
        ("(5,3,2) [step v3: 4->5]",  (5, 3, 2, None, None, None, None, None, None)),
        ("(5,4,2) [v3=5,v5=4]",      (5, 4, 2, None, None, None, None, None, None)),
        ("(5,3,3) [v3=5,v7=3]",      (5, 3, 3, None, None, None, None, None, None)),
        ("(inf,3,2) [v3=inf]",       (None, 3, 2, None, None, None, None, None, None)),
        ("(inf,3,inf) [force 5^4]",  (None, 3, None, None, None, None, None, None, None)),
        ("(inf,inf,2) [force 7^3]",  (None, None, 2, None, None, None, None, None, None)),
        ("(inf,inf,inf; v11=1)",     (None, None, None, 1, None, None, None, None, None)),
        ("(4,3,2; v11=1)",           (4, 3, 2, 1, None, None, None, None, None)),
        ("(5,3,2; v11=1)",           (5, 3, 2, 1, None, None, None, None, None)),
        ("(inf,inf,2; v11=1)",       (None, None, 2, 1, None, None, None, None, None)),
        ("(4,inf,inf; v11=1)",       (4, None, None, 1, None, None, None, None, None)),
        ("(inf,3,inf; v11=1)",       (None, 3, None, 1, None, None, None, None, None)),
        ("(inf,inf,inf; v11..29=1)", (None, None, None, 1, 1, 1, 1, 1, 1)),
        ("(4,inf,inf; v11..29=1)",   (4, None, None, 1, 1, 1, 1, 1, 1)),
        ("(5,4,3; v11..29=1)",       (5, 4, 3, 1, 1, 1, 1, 1, 1)),
    ]

    print(f"{'Case':<28s} | {'R':>8s} | {'pure3 mgn':>10s} | {'165 mgn':>10s} | {'Stage sums (165)':<45s}")
    print("-" * 112)
    for name, exps in cases:
        mod = ExponentModel(exps, C7=Fraction(3, 2), taus_later=(4, 4, 6, 8, 12, 16))
        R, Ls, Ls165 = mod.eval_A1()
        m_p3 = float(R - sum(Ls))
        m_165 = float(R - sum(Ls165))
        s_str = " ".join(f"{float(x):.2f}" for x in Ls165)
        tag = "PASS" if m_165 > 0 else "FAIL"
        print(f"{name:<28s} | {float(R):8.4f} | {m_p3:+10.5f} | {m_165:+10.5f} | {tag}  [{s_str}]")

    print(f"\nDone in {time.time()-t0:.2f}s.")


if __name__ == "__main__":
    main()
