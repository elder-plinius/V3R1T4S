#!/usr/bin/env python3
"""SSZ MDP from Table 1 and Section 4.2 of arXiv:1507.06183 (PDF page 8 / Table 1,
page 11 eq. (7) and the following display). gamma may be 0.

Adopt goes to X0 = (1,0,irr) / (0,1,irr), one transition = one new block.
Override is two-way (next block already created).
Wait (irr or rel): (a+1,h,irr) w.p. alpha, (a,h+1,rel) w.p. 1-alpha.
Match (rel, a>=h) and wait (active) share:
  (a+1,h,active) w.p. alpha, reward (0,0)
  (a-h,1,rel)    w.p. gamma*(1-alpha), reward (h,0)
  (a,h+1,rel)    w.p. (1-gamma)*(1-alpha), reward (0,0)
At max(a,h)=T only adopt is legal (Sec. 4.2).
Under-pay cap/ordinary adopt: w_rho = -rho * h, next X0.
Over-pay cap adopt: w_rho from eq. (7) / following display, next X0.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import numpy as np

IRRELEVANT, RELEVANT, ACTIVE = 0, 1, 2
ADOPT, OVERRIDE, MATCH, WAIT = 0, 1, 2, 3
ACTION_NAMES = {ADOPT: "adopt", OVERRIDE: "override", MATCH: "match", WAIT: "wait"}


def n_states(T: int) -> int:
    return (T + 1) * (T + 1) * 3


def sid(a, h, f, T):
    return (a * (T + 1) + h) * 3 + f


def unsid(s, T):
    f = s % 3
    t = s // 3
    return t // (T + 1), t % (T + 1), f


def C_of(alpha):
    return alpha * (1.0 - alpha) / (1.0 - 2.0 * alpha) ** 2


def elast_eq7(a, h, alpha):
    C = C_of(alpha)
    return C + 0.5 * ((a - h) / (1.0 - 2.0 * alpha) + a + h)


def overpay_w(a, h, alpha, rho):
    if a >= h:
        return (1.0 - rho) * elast_eq7(a, h, alpha)
    q = (alpha / (1.0 - alpha)) ** (h - a)
    return (1.0 - q) * (-rho * h) + q * (1.0 - rho) * (C_of(alpha) + (h - a) / (1.0 - 2.0 * alpha))


def allowed(a, h, f, action, T):
    if a == T or h == T:
        return action == ADOPT
    if action == ADOPT:
        return True
    if action == OVERRIDE:
        return a > h
    if action == MATCH:
        return f == RELEVANT and a >= h and h >= 1
    if action == WAIT:
        return a < T and h < T
    return False


def w_rho(ra, rh, rho):
    return ra - rho * (ra + rh)


def transitions(a, h, f, action, alpha, gamma, rho, T, paying):
    """List of (p, a2, h2, f2, w_rho). Empty if illegal."""
    if not allowed(a, h, f, action, T):
        return []

    def x0(w):
        # official adopt (and cap adopt): next state ~ X0
        return [
            (alpha, 1, 0, IRRELEVANT, w),
            (1.0 - alpha, 0, 1, IRRELEVANT, w),
        ]

    if action == ADOPT:
        if (a == T or h == T) and paying == "over":
            w = overpay_w(a, h, alpha, rho)
        else:
            w = w_rho(0.0, float(h), rho)
        return x0(w)

    if action == OVERRIDE:
        w = w_rho(float(h + 1), 0.0, rho)
        return [
            (alpha, a - h, 0, IRRELEVANT, w),
            (1.0 - alpha, a - h - 1, 1, RELEVANT, w),
        ]

    if action == WAIT and f != ACTIVE:
        return [
            (alpha, a + 1, h, IRRELEVANT, 0.0),
            (1.0 - alpha, a, h + 1, RELEVANT, 0.0),
        ]

    # (a,h,active) wait, or (a,h,relevant) match
    out = [(alpha, a + 1, h, ACTIVE, 0.0)]
    if gamma > 0:
        out.append((gamma * (1.0 - alpha), a - h, 1, RELEVANT, w_rho(float(h), 0.0, rho)))
        out.append(((1.0 - gamma) * (1.0 - alpha), a, h + 1, RELEVANT, 0.0))
    else:
        out.append((1.0 - alpha, a, h + 1, RELEVANT, 0.0))
    return out


def build_action_tables(T, alpha, rho, paying, gamma=0.0):
    ns = n_states(T)
    tables = []
    for s in range(ns):
        a, h, f = unsid(s, T)
        acts = []
        for action in (ADOPT, OVERRIDE, MATCH, WAIT):
            if not allowed(a, h, f, action, T):
                continue
            tr = transitions(a, h, f, action, alpha, gamma, rho, T, paying)
            if not tr:
                continue
            for p, a2, h2, f2, w in tr:
                if a2 < 0 or h2 < 0 or a2 > T or h2 > T:
                    raise RuntimeError(
                        "off-board successor from (%d,%d,%d) action %d -> (%d,%d,%d)"
                        % (a, h, f, action, a2, h2, f2)
                    )
            packed = [(p, sid(a2, h2, f2, T), w) for p, a2, h2, f2, w in tr]
            acts.append((action, packed))
        if not acts:
            # unused corner (e.g. (0,0,*) or a dead fork label at the cap):
            # treat as adopt with ordinary/overpay reward, next X0 (clipped).
            w = overpay_w(a, h, alpha, rho) if paying == "over" else w_rho(0.0, float(h), rho)
            acts.append((ADOPT, [(alpha, sid(1, 0, IRRELEVANT, T), w),
                                 (1.0 - alpha, sid(0, 1, IRRELEVANT, T), w)]))
        tables.append(acts)
    return tables


@dataclass
class SolveResult:
    gain: float
    bias: np.ndarray
    policy: np.ndarray
    iters: int
    paying: str
    alpha: float
    rho: float
    T: int
    ev_iters: int = 0


def _policy_arrays(tables, policy):
    ns = len(policy)
    r = np.zeros(ns)
    p0 = np.zeros(ns); p1 = np.zeros(ns); p2 = np.zeros(ns)
    i0 = np.zeros(ns, dtype=np.int32)
    i1 = np.zeros(ns, dtype=np.int32)
    i2 = np.zeros(ns, dtype=np.int32)
    for s, acts in enumerate(tables):
        action = int(policy[s])
        packed = None
        for act, pk in acts:
            if act == action:
                packed = pk
                break
        if packed is None:
            packed = acts[0][1]
            policy[s] = acts[0][0]
        rows = list(packed) + [(0.0, 0, 0.0)] * 3
        for k, (p, s2, w) in enumerate(rows[:3]):
            r[s] += p * w
            if k == 0:
                p0[s], i0[s] = p, s2
            elif k == 1:
                p1[s], i1[s] = p, s2
            else:
                p2[s], i2[s] = p, s2
    return r, p0, p1, p2, i0, i1, i2


def _T_of(ns):
    t1 = int(round((ns / 3) ** 0.5))
    if t1 * t1 * 3 != ns:
        raise ValueError("cannot recover T from ns=%d" % ns)
    return t1 - 1


def rvi_gain(r, p0, p1, p2, i0, i1, i2, T, tol=1e-10, max_iter=80000, pin=None):
    """Lazy relative value iteration. Returns (gain_at_pin, bias, iters, residual)."""
    ns = len(r)
    if pin is None:
        pin = sid(1, 0, IRRELEVANT, T)
    h = np.zeros(ns)
    it = 0
    for it in range(1, max_iter + 1):
        raw = r + p0 * h[i0] + p1 * h[i1] + p2 * h[i2]
        h_new = 0.5 * h + 0.5 * raw
        h_new -= h_new[pin]
        if float(np.max(np.abs(h_new - h))) < tol:
            h = h_new
            break
        h = h_new
    residual = r + p0 * h[i0] + p1 * h[i1] + p2 * h[i2] - h
    return float(residual[pin]), h, it, residual


def policy_evaluation(tables, policy, tol=1e-10, max_iter=80000):
    r, p0, p1, p2, i0, i1, i2 = _policy_arrays(tables, policy)
    T = _T_of(len(policy))
    gain, h, it, residual = rvi_gain(r, p0, p1, p2, i0, i1, i2, T, tol=tol, max_iter=max_iter)
    return gain, h, it


def greedy_policy(tables, h):
    pref = {OVERRIDE: 3, MATCH: 2, WAIT: 1, ADOPT: 0}
    pol = np.zeros(len(tables), dtype=np.int8)
    for s, acts in enumerate(tables):
        best_a, best_q = acts[0][0], -1e300
        for act, packed in acts:
            q = sum(p * (w + h[s2]) for p, s2, w in packed)
            if q > best_q + 1e-12 or (abs(q - best_q) <= 1e-12 and pref.get(act, 0) > pref.get(best_a, 0)):
                best_q, best_a = q, act
        pol[s] = best_a
    return pol


def honest_like_policy(tables, T):
    """Publish immediately: override if a>h, else wait if a>=h and h<T, else adopt."""
    pol = np.zeros(len(tables), dtype=np.int8)
    for s, acts in enumerate(tables):
        a, h, f = unsid(s, T)
        legal = {act for act, _ in acts}
        if OVERRIDE in legal and a > h:
            pol[s] = OVERRIDE
        elif WAIT in legal and a >= h:
            pol[s] = WAIT
        elif ADOPT in legal:
            pol[s] = ADOPT
        else:
            pol[s] = acts[0][0]
    return pol


def policy_iteration_tables(tables, T, alpha, rho, paying, ev_tol=1e-10, max_pi=40):
    policy = honest_like_policy(tables, T)
    last = None
    for it in range(1, max_pi + 1):
        gain, bias, ev = policy_evaluation(tables, policy, tol=ev_tol)
        new = greedy_policy(tables, bias)
        last = SolveResult(gain, bias, policy, it, paying, alpha, rho, T, ev)
        if np.array_equal(new, policy):
            # re-evaluate for a consistent residual[reference]
            residual_gain, bias, ev = policy_evaluation(tables, policy, tol=ev_tol)
            # better gain: mean residual on policy (should be nearly constant)
            r, p0, p1, p2, i0, i1, i2 = _policy_arrays(tables, policy)
            resid = r + p0 * bias[i0] + p1 * bias[i1] + p2 * bias[i2] - bias
            last = SolveResult(float(resid[sid(1, 0, 0, T)]), bias, policy, it, paying, alpha, rho, T, ev)
            return last
        policy = new
    r, p0, p1, p2, i0, i1, i2 = _policy_arrays(tables, policy)
    resid = r + p0 * last.bias[i0] + p1 * last.bias[i1] + p2 * last.bias[i2] - last.bias
    return SolveResult(float(resid[sid(1, 0, 0, T)]), last.bias, policy, last.iters, paying, alpha, rho, T, last.ev_iters)


def reward_rates_blocks(tables, policy, T, alpha, paying, rho, gamma=0.0, tol=1e-10, max_iter=80000):
    """Mean (ra, tot) per step under the policy, via lazy evaluation of two reward streams.

    Reconstruct ra, rh from w and the known action structure by walking transitions
    with the (ra,rh) attached. We rebuild from the same Table 1 rules.
    """
    ns = len(policy)
    ra = np.zeros(ns); tot = np.zeros(ns)
    p0 = np.zeros(ns); p1 = np.zeros(ns); p2 = np.zeros(ns)
    i0 = np.zeros(ns, dtype=np.int32)
    i1 = np.zeros(ns, dtype=np.int32)
    i2 = np.zeros(ns, dtype=np.int32)

    def pack_from(a, h, f, action):
        tr = transitions(a, h, f, action, alpha, gamma, rho, T, paying)
        if not tr:
            # fallback adopt
            tr = transitions(a, h, f, ADOPT, alpha, gamma, rho, T, paying)
        # We need (ra,rh) not just w. Re-derive:
        out = []
        if action == ADOPT or not tr:
            # cap overpay is a scalar, not a block pair; do not use for REV of over-pay.
            # For under-pay adopt: (0,h)
            for p, a2, h2, f2, w in tr:
                out.append((p, sid(a2, h2, f2, T), 0.0, float(h)))
        elif action == OVERRIDE:
            for p, a2, h2, f2, w in tr:
                out.append((p, sid(a2, h2, f2, T), float(h + 1), 0.0))
        elif action == MATCH or (action == WAIT and f == ACTIVE):
            for p, a2, h2, f2, w in tr:
                if abs(p - (gamma * (1.0 - alpha))) < 1e-15 and gamma > 0 and a2 == a - h:
                    out.append((p, sid(a2, h2, f2, T), float(h), 0.0))
                else:
                    out.append((p, sid(a2, h2, f2, T), 0.0, 0.0))
        else:
            for p, a2, h2, f2, w in tr:
                out.append((p, sid(a2, h2, f2, T), 0.0, 0.0))
        return out

    for s in range(ns):
        a, h, f = unsid(s, T)
        action = int(policy[s])
        if not allowed(a, h, f, action, T):
            action = ADOPT
        rows = pack_from(a, h, f, action) + [(0.0, 0, 0.0, 0.0)] * 3
        for k, (p, s2, r1, r2) in enumerate(rows[:3]):
            ra[s] += p * r1
            tot[s] += p * (r1 + r2)
            if k == 0:
                p0[s], i0[s] = p, s2
            elif k == 1:
                p1[s], i1[s] = p, s2
            else:
                p2[s], i2[s] = p, s2

    def mean_of(r):
        gain, v, it, resid = rvi_gain(r, p0, p1, p2, i0, i1, i2, T, tol=tol, max_iter=max_iter)
        return gain, it

    ga, ita = mean_of(ra)
    gt, itt = mean_of(tot)
    rev = (ga / gt) if abs(gt) > 1e-18 else float("nan")
    return {"mean_ra": ga, "mean_tot": gt, "rev": rev, "iters": (ita, itt)}


def optimal_under_rev(T, alpha, gamma=0.0, max_outer=16, ev_tol=1e-10):
    rho = float(alpha)
    hist = []
    sol = rates = tables = None
    for i in range(max_outer):
        tables = build_action_tables(T, alpha, rho, "under", gamma=gamma)
        sol = policy_iteration_tables(tables, T, alpha, rho, "under", ev_tol=ev_tol)
        rates = reward_rates_blocks(tables, sol.policy, T, alpha, "under", rho, gamma=gamma, tol=ev_tol)
        hist.append({"i": i, "rho": rho, "rev": rates["rev"], "gain": sol.gain,
                     "pi_iters": sol.iters, "ev": sol.ev_iters, "rates": rates})
        new = rates["rev"]
        if new != new or abs(new - rho) < 1e-10 or abs(sol.gain) < 1e-12:
            if new == new:
                rho = new
            break
        rho = new
    return rho, sol, tables, rates, hist


def check_dual(tables, h, g, outward_eps=0.0):
    max_viol = -1e300
    n = 0
    worst = None
    for s, acts in enumerate(tables):
        for act, packed in acts:
            q = sum(p * (w + h[s2]) for p, s2, w in packed)
            viol = q - h[s] - g
            n += 1
            if viol > max_viol:
                max_viol = viol
                worst = (s, int(act), float(viol))
    return float(max_viol) <= outward_eps, float(max_viol), n, worst
