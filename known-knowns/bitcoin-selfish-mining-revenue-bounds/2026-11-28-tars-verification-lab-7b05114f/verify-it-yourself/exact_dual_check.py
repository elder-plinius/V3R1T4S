#!/usr/bin/env python3
"""Standalone exact-rational dual checker (Python standard library only).

Rebuilds SSZ Table 1 + Section 4.2 with eq. (7) read as (1-rho)*E[last]
per appendix (26)-(27) and Lemma 13. Includes match at (a,0,relevant).
"""
from __future__ import annotations

import ast, json, struct, sys
from fractions import Fraction
from pathlib import Path

IRRELEVANT, RELEVANT, ACTIVE = 0, 1, 2
ADOPT, OVERRIDE, MATCH, WAIT = 0, 1, 2, 3
CLAIMED_G = Fraction(-51696398727, 351843720888320)
T, ALPHA, RHO, GAMMA = 95, Fraction(9, 20), Fraction(169, 250), Fraction(0)
EXPECTED_N = 72678


def load_npy(path: Path):
    b = path.read_bytes()
    if b[:6] != b"\x93NUMPY":
        raise ValueError("not a .npy file: %s" % path)
    major, minor = b[6], b[7]
    if (major, minor) == (1, 0):
        hlen = struct.unpack_from("<H", b, 8)[0]
        header = b[10:10 + hlen]
        data = b[10 + hlen:]
    elif (major, minor) == (2, 0):
        hlen = struct.unpack_from("<I", b, 8)[0]
        header = b[12:12 + hlen]
        data = b[12 + hlen:]
    else:
        raise ValueError("unsupported npy version %s.%s" % (major, minor))
    meta = ast.literal_eval(header.decode("latin1").strip())
    shape = meta["shape"]
    descr = meta["descr"]
    if meta.get("fortran_order"):
        raise ValueError("fortran_order arrays are not supported")
    n = 1
    for d in shape:
        n *= d
    if descr == "<f8":
        vals = struct.unpack("<" + "d" * n, data)
    elif descr in ("|i1", "i1", "<i1"):
        vals = struct.unpack("b" * n, data)
    else:
        raise ValueError("unsupported descr %r" % descr)
    return shape, vals


def sid(a, h, f, T=T):
    return (a * (T + 1) + h) * 3 + f


def unsid(s, T=T):
    f = s % 3
    t = s // 3
    return t // (T + 1), t % (T + 1), f


def C_of(alpha: Fraction) -> Fraction:
    return alpha * (1 - alpha) / (1 - 2 * alpha) ** 2


def elast(a, h, alpha: Fraction) -> Fraction:
    return C_of(alpha) + Fraction(1, 2) * ((a - h) / (1 - 2 * alpha) + a + h)


def overpay_w(a, h, alpha: Fraction, rho: Fraction) -> Fraction:
    if a >= h:
        return (1 - rho) * elast(a, h, alpha)
    q = (alpha / (1 - alpha)) ** (h - a)
    return (1 - q) * (-rho * h) + q * (1 - rho) * (C_of(alpha) + (h - a) / (1 - 2 * alpha))


def w_rho(ra, rh, rho):
    return ra - rho * (ra + rh)


def allowed(a, h, f, action, T=T) -> bool:
    if a == T or h == T:
        return action == ADOPT
    if action == ADOPT:
        return True
    if action == OVERRIDE:
        return a > h
    if action == MATCH:
        return f == RELEVANT and a >= h
    if action == WAIT:
        return a < T and h < T
    return False


def transitions(a, h, f, action, alpha, gamma, rho, T=T):
    if not allowed(a, h, f, action, T):
        return []

    def x0(w):
        return [(alpha, 1, 0, IRRELEVANT, w), (1 - alpha, 0, 1, IRRELEVANT, w)]

    if action == ADOPT:
        if a == T or h == T:
            w = overpay_w(a, h, alpha, rho)
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


def main():
    # Resolve files relative to the package root (cwd) or next to this script's package.
    here = Path(__file__).resolve().parent
    root = here.parent if (here / "exact_dual_check.py").exists() and (here.parent / "object").is_dir() else Path.cwd()
    bias_path = root / "object" / "over_bias.npy"
    claim_path = root / "object" / "exact_dual_rho169_250.json"
    if len(sys.argv) >= 3:
        bias_path, claim_path = Path(sys.argv[1]), Path(sys.argv[2])
    shape, bias = load_npy(bias_path)
    n_states = (T + 1) * (T + 1) * 3
    if shape != (n_states,):
        print("bias shape %s != (%d,)" % (shape, n_states), file=sys.stderr)
        return 1
    H = [Fraction(*float(x).as_integer_ratio()) for x in bias]
    claimed = json.loads(claim_path.read_text())
    claimed_g = Fraction(int(claimed["max_residual_g_bar"]["num"]), int(claimed["max_residual_g_bar"]["den"]))

    min_r = max_r = None
    n = 0
    offboard = 0
    for s in range(n_states):
        a, h, f = unsid(s)
        for action in (ADOPT, OVERRIDE, MATCH, WAIT):
            tr = transitions(a, h, f, action, ALPHA, GAMMA, RHO)
            if not tr:
                continue
            q = Fraction(0)
            for p, a2, h2, f2, w in tr:
                if a2 < 0 or h2 < 0 or a2 > T or h2 > T:
                    offboard += 1
                    continue
                q += p * (w + H[sid(a2, h2, f2)])
            r = q - H[s]
            n += 1
            if min_r is None or r < min_r:
                min_r = r
            if max_r is None or r > max_r:
                max_r = r
    g_bar = max_r
    print("n_inequalities", n)
    print("offboard", offboard)
    print("g_bar", str(g_bar))
    print("claimed_g", str(claimed_g))
    print("hardcoded_g", str(CLAIMED_G))
    ok = (
        n == EXPECTED_N
        and offboard == 0
        and g_bar == claimed_g == CLAIMED_G
        and g_bar < 0
        and bool(claimed.get("certified_REV_lt_rho"))
        and claimed.get("eq7_grouping") == "rebracketed"
    )
    print("match", ok)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
