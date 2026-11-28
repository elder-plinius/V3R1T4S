#!/usr/bin/env python3
"""Exact-rational dual check of an over-paying SSZ N_rho^T certificate.

Rebuilds Table 1 + Section 4.2 / eq. (7) independently (does not import the
solver). Bias entries become exact dyadic rationals via float.as_integer_ratio.
"""
from __future__ import annotations

import argparse, json, time
from fractions import Fraction
from pathlib import Path
import numpy as np

IRRELEVANT, RELEVANT, ACTIVE = 0, 1, 2
ADOPT, OVERRIDE, MATCH, WAIT = 0, 1, 2, 3


def F(x) -> Fraction:
    if isinstance(x, Fraction):
        return x
    if isinstance(x, str) and "/" in x:
        a, b = x.split("/", 1)
        return Fraction(int(a), int(b))
    if isinstance(x, (int, np.integer)):
        return Fraction(int(x))
    return Fraction(x)


def sid(a, h, f, T):
    return (a * (T + 1) + h) * 3 + f


def unsid(s, T):
    f = s % 3
    t = s // 3
    return t // (T + 1), t % (T + 1), f


def C_of(alpha: Fraction) -> Fraction:
    return alpha * (1 - alpha) / (1 - 2 * alpha) ** 2


def elast_eq7(a, h, alpha: Fraction) -> Fraction:
    return C_of(alpha) + Fraction(1, 2) * ((a - h) / (1 - 2 * alpha) + a + h)


def elast_from24(a0, h0, alpha: Fraction) -> Fraction:
    d = 1 - 2 * alpha
    Epsi = (alpha / d) * (1 + 1 / d) + (a0 - h0) / d
    return Fraction(1, 2) * (Epsi - (a0 - h0)) + a0


def overpay_w_a_ge_h(a, h, alpha: Fraction, rho: Fraction, grouping: str) -> Fraction:
    """Cap reward when T = a >= h.

    grouping='rebracketed': (1-rho)*E[last] as in appendix (26)-(27) and Lemma 13.
    grouping='literal': typeset eq. (7), where (1-rho) multiplies only the C term.
    """
    C = C_of(alpha)
    half = Fraction(1, 2) * ((a - h) / (1 - 2 * alpha) + a + h)
    if grouping == "rebracketed":
        return (1 - rho) * (C + half)
    if grouping == "literal":
        return (1 - rho) * C + half
    raise ValueError("unknown eq7 grouping: %s" % grouping)


def overpay_w_h_gt_a(a, h, alpha: Fraction, rho: Fraction, ht_comp: str) -> Fraction:
    """Cap reward when T = h > a (the 'following display' / eq. (28)).

    printed: uses E[a0|return] = (h-a)/(1-2*alpha), the expected hitting time.
    corrected: uses the attacker block count a + (h-a)*(1-alpha)/(1-2*alpha).
    max: pointwise max, a conservative over-pay (valid whenever either is).
    """
    q = (alpha / (1 - alpha)) ** (h - a)
    C = C_of(alpha)
    printed = (1 - q) * (-rho * h) + q * (1 - rho) * (C + (h - a) / (1 - 2 * alpha))
    E_a0 = a + (h - a) * (1 - alpha) / (1 - 2 * alpha)
    corrected = (1 - q) * (-rho * h) + q * (1 - rho) * (C + E_a0)
    if ht_comp == "printed":
        return printed
    if ht_comp == "corrected":
        return corrected
    if ht_comp == "max":
        return printed if printed >= corrected else corrected
    raise ValueError("unknown ht_comp: %s" % ht_comp)


def overpay_w(a, h, alpha: Fraction, rho: Fraction, grouping: str = "rebracketed",
              ht_comp: str = "printed") -> Fraction:
    if a >= h:
        return overpay_w_a_ge_h(a, h, alpha, rho, grouping)
    return overpay_w_h_gt_a(a, h, alpha, rho, ht_comp)


def w_rho(ra, rh, rho):
    return ra - rho * (ra + rh)


def allowed(a, h, f, action, T) -> bool:
    if a == T or h == T:
        return action == ADOPT
    if action == ADOPT:
        return True
    if action == OVERRIDE:
        return a > h
    if action == MATCH:
        # Table 1: match is feasible when a >= h (including h = 0).
        return f == RELEVANT and a >= h
    if action == WAIT:
        return a < T and h < T
    return False


def transitions(a, h, f, action, alpha, gamma, rho, T, paying, grouping="rebracketed", ht_comp="printed"):
    if not allowed(a, h, f, action, T):
        return []

    def x0(w):
        return [
            (alpha, 1, 0, IRRELEVANT, w),
            (1 - alpha, 0, 1, IRRELEVANT, w),
        ]

    if action == ADOPT:
        if (a == T or h == T) and paying == "over":
            w = overpay_w(a, h, alpha, rho, grouping=grouping, ht_comp=ht_comp)
        else:
            w = w_rho(0, h, rho)
        return x0(w)
    if action == OVERRIDE:
        w = w_rho(h + 1, 0, rho)
        return [
            (alpha, a - h, 0, IRRELEVANT, w),
            (1 - alpha, a - h - 1, 1, RELEVANT, w),
        ]
    if action == WAIT and f != ACTIVE:
        return [
            (alpha, a + 1, h, IRRELEVANT, Fraction(0)),
            (1 - alpha, a, h + 1, RELEVANT, Fraction(0)),
        ]
    out = [(alpha, a + 1, h, ACTIVE, Fraction(0))]
    if gamma > 0:
        out.append((gamma * (1 - alpha), a - h, 1, RELEVANT, w_rho(h, 0, rho)))
        out.append(((1 - gamma) * (1 - alpha), a, h + 1, RELEVANT, Fraction(0)))
    else:
        out.append((1 - alpha, a, h + 1, RELEVANT, Fraction(0)))
    return out


def identity_ok(alpha):
    for a, h in ((0, 0), (1, 0), (5, 3), (40, 40), (95, 95), (95, 90), (10, 3)):
        if elast_eq7(a, h, alpha) != elast_from24(a, h, alpha):
            return False
    return True


def frac_json(x):
    if x is None:
        return None
    return {"num": str(x.numerator), "den": str(x.denominator), "float": float(x)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--T", type=int, required=True)
    ap.add_argument("--alpha", required=True)
    ap.add_argument("--rho", required=True)
    ap.add_argument("--bias", required=True)
    ap.add_argument("--policy", default=None)
    ap.add_argument("--paying", default="over")
    ap.add_argument("--gamma", default="0")
    ap.add_argument("--out", required=True)
    ap.add_argument("--eq7-grouping", choices=("rebracketed", "literal"), default="rebracketed",
                    help="rebracketed = (1-rho)*E[last] per (26)-(27); literal = typeset (7)")
    ap.add_argument("--ht-comp", choices=("printed", "corrected", "max"), default="printed",
                    help="h=T>a compensation: printed display, corrected E[a0], or their max")
    args = ap.parse_args()

    t0 = time.time()
    T = args.T
    alpha, rho, gamma = F(args.alpha), F(args.rho), F(args.gamma)
    paying = args.paying
    n_states = (T + 1) * (T + 1) * 3
    bias = np.load(args.bias)
    if bias.shape != (n_states,):
        raise SystemExit("bias shape %s != (%d,)" % (bias.shape, n_states))
    H = [Fraction(*float(x).as_integer_ratio()) for x in bias]
    policy = np.load(args.policy) if args.policy else None

    min_r = max_r = None
    min_w = max_w = None
    n = 0
    n_illegal_pol = 0
    offboard = 0
    for s in range(n_states):
        a, h, f = unsid(s, T)
        for action in (ADOPT, OVERRIDE, MATCH, WAIT):
            tr = transitions(a, h, f, action, alpha, gamma, rho, T, paying,
                             grouping=args.eq7_grouping, ht_comp=args.ht_comp)
            if not tr:
                if policy is not None and int(policy[s]) == action:
                    # fallback adopt used by builder for empty action sets
                    if not allowed(a, h, f, action, T):
                        n_illegal_pol += 1
                continue
            q = Fraction(0)
            for p, a2, h2, f2, w in tr:
                if a2 < 0 or h2 < 0 or a2 > T or h2 > T:
                    offboard += 1
                    continue
                q += p * (w + H[sid(a2, h2, f2, T)])
            r = q - H[s]
            n += 1
            if min_r is None or r < min_r:
                min_r, min_w = r, (s, a, h, f, action)
            if max_r is None or r > max_r:
                max_r, max_w = r, (s, a, h, f, action)

    g_bar = max_r
    cert_ok = (g_bar is not None and g_bar < 0 and offboard == 0 and identity_ok(alpha)
               and paying == "over")
    out = {
        "T": T,
        "alpha": frac_json(alpha),
        "rho": frac_json(rho),
        "gamma": frac_json(gamma),
        "paying": paying,
        "eq7_grouping": args.eq7_grouping,
        "ht_comp": args.ht_comp,
        "match_includes_h0": True,
        "published_table2_upper_alpha_0_45": "0.70109",
        "bank_bar_alpha_0_45": "0.70099",

        "n_states": n_states,
        "n_inequalities": n,
        "offboard": offboard,
        "identity_eq7_eq24": identity_ok(alpha),
        "min_residual": frac_json(min_r),
        "max_residual_g_bar": frac_json(g_bar),
        "min_where": None if not min_w else {"s": min_w[0], "a": min_w[1], "h": min_w[2], "fork": min_w[3], "action": min_w[4]},
        "max_where": None if not max_w else {"s": max_w[0], "a": max_w[1], "h": max_w[2], "fork": max_w[3], "action": max_w[4]},
        "g_bar_strictly_negative": bool(g_bar is not None and g_bar < 0),
        "certified_REV_lt_rho": bool(cert_ok),
        "bank_bar": {"num": "70099", "den": "100000"},
        "rho_leq_bank_bar": bool(rho <= Fraction(70099, 100000)),
        "meets_bank_format_if_g_bar_neg": bool(cert_ok and rho <= Fraction(70099, 100000)),
        "seconds": time.time() - t0,
    }
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({
        "n": n,
        "eq7_grouping": args.eq7_grouping,
        "ht_comp": args.ht_comp,
        "offboard": offboard,
        "g_bar": str(g_bar),
        "g_bar_float": float(g_bar) if g_bar is not None else None,
        "g_bar_neg": out["g_bar_strictly_negative"],
        "certified_REV_lt_rho": cert_ok,
        "rho_leq_bar": out["rho_leq_bank_bar"],
        "seconds": out["seconds"],
    }, indent=2))


if __name__ == "__main__":
    main()
