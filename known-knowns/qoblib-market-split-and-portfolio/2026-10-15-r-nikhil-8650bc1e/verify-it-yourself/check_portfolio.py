#!/usr/bin/env python3
"""Standalone checker for QOBLIB class 06 portfolio solutions, written from the class's reference model
06-portfolio/models/binary_quadratic_programming/bqp_u3_c10.zpl + parameter_u3_c10.zpl, in exact rational arithmetic
(Python standard library only). It also pins the instance files by sha256 and prints a final PASS or FAIL.

Usage: python3 -I check_portfolio.py INSTANCE_DIR SOLUTION EXPECTED_OBJECTIVE BAR
PASS iff the instance files have the pinned sha256, the solution is feasible in every period, its exact objective
equals EXPECTED_OBJECTIVE and is strictly below BAR (the class minimises).
"""
import hashlib

import gzip
import math
import os
import sys
from fractions import Fraction as F

CASH, UNIT = F(1000000), F(100000)
DELTA, NU, RHO = F("0.001"), F("0.0001"), F("0.000025")
UB, CS1, CS2 = 3, 4, 7


def zround(q):
    """Round half away from zero, exactly."""
    a = abs(q)
    n = math.floor(a + F(1, 2))
    return n if q >= 0 else -n


def open_text(path):
    if os.path.exists(path):
        return open(path, "r", encoding="utf-8")
    return gzip.open(path + ".gz", "rt", encoding="utf-8")


def rows(path):
    with open_text(path) as f:
        for line in f:
            line = line.split("#", 1)[0].strip()
            if line:
                yield line.split()


def read_instance(d):
    raw_p, order, days = {}, [], set()
    for t, s, v in rows(os.path.join(d, "stock_prices.txt")):
        t = int(t)
        days.add(t)
        if s not in raw_p:
            raw_p[s] = {}
            order.append(s)
        raw_p[s][t] = F(v)
    cov = {}
    for t, s1, s2, v in rows(os.path.join(d, "covariance_matrices.txt")):
        cov[(s1, s2, int(t))] = F(v)
    T = sorted(days)
    if T != list(range(T[0], T[-1] + 1)):
        raise ValueError("day indices are not consecutive")
    t0 = T[0]
    p = {(s, t): raw_p[s][t] * (UNIT / raw_p[s][t0]) for s in order for t in T}
    return order, T, p, cov


def read_solution(path):
    head, pos = {}, {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.split("#", 1)[0].strip()
            if not line:
                continue
            tok = line.split()
            if len(tok) == 2:
                head[tok[0]] = tok[1]
            elif len(tok) == 4:
                key = (int(tok[0]), tok[1])
                if key in pos:
                    raise ValueError("duplicate position line for %r" % (key,))
                lo, sh = int(tok[2]), int(tok[3])
                if not (0 <= lo <= UB and 0 <= sh <= UB):
                    raise ValueError("unit count outside 0..%d at %r" % (UB, key))
                pos[key] = (lo, sh)
            else:
                raise ValueError("malformed line %r" % line)
    return head, pos


def evaluate(order, T, p, cov, pos, B, lam):
    t_beg, t_end = T[0], T[-1]
    for (t, s) in pos:
        if t not in T or s not in order:
            raise ValueError("position (%d, %s) outside the instance" % (t, s))
    u = {(s, tau, t): 0 for s in order for tau in (1, -1) for t in T}
    for (t, s), (lo, sh) in pos.items():
        u[(s, 1, t)] = lo
        u[(s, -1, t)] = sh
    feasible, log = True, []
    parts = dict(risk=0, ret=0, trans=0, cash=0, short=0, liq=0)
    for t in T:
        net = sum(tau * u[(s, tau, t)] for s in order for tau in (1, -1))
        tot = sum(u[(s, tau, t)] for s in order for tau in (1, -1))
        cslack = CASH / UNIT - net
        bslack = B - tot
        ok = 0 <= cslack <= 2 ** CS1 - 1 and 0 <= bslack <= 2 ** CS2 - 1
        feasible &= ok
        log.append("t=%2d net=%3d total=%3d cash_slack=%s count_slack=%d %s" % (t, net, tot, cslack, bslack, "ok" if ok else "VIOLATED"))
        # cash interest: y is the binary expansion of the cash slack; coefficient round(nu*unit*2^k)
        if ok:
            cs = int(cslack)
            parts["cash"] -= sum(zround(NU * UNIT * 2 ** k) for k in range(CS1) if (cs >> k) & 1)
        held = [(s, tau) for s in order for tau in (1, -1) if u[(s, tau, t)]]
        for (si, ti) in held:
            for (sj, tj) in held:
                c = zround(lam * ti * tj * cov[(si, sj, t)] * p[(si, t)] * p[(sj, t)])
                parts["risk"] += c * u[(si, ti, t)] * u[(sj, tj, t)]
        for s in order:
            parts["short"] += zround(RHO * p[(s, t)]) * u[(s, -1, t)]
            for tau in (1, -1):
                n = u[(s, tau, t)]
                if t != t_end:
                    parts["ret"] -= zround(tau * (p[(s, t + 1)] - p[(s, t)])) * n
                if t == t_beg:
                    parts["trans"] += zround(DELTA * p[(s, t)]) * n
                elif t != t_end:
                    parts["trans"] += zround(DELTA * p[(s, t)]) * abs(n - u[(s, tau, t - 1)])
                else:
                    parts["liq"] += zround(DELTA * p[(s, t)]) * n
    return feasible, sum(parts.values()), parts, log


PINNED = {
    "stock_prices.txt.gz": "189292e71736fdfb55a75d4dfe5269829668a9ac73513bedd4fc5b30bf38fee9",
    "covariance_matrices.txt.gz": "5214e9ddb522339f86485e0bdc86f519542d552cfc744fc137bd7dcabfa31167",
}


def verdict(argv):
    inst, sol, expected, bar = argv[1], argv[2], int(argv[3]), int(argv[4])
    for name, h in PINNED.items():
        got = hashlib.sha256(open(os.path.join(inst, name), "rb").read()).hexdigest()
        print("instance file %s sha256 %s %s" % (name, got, "ok" if got == h else "MISMATCH (expected %s)" % h))
        if got != h:
            return False
    try:
        order, T, p, cov = read_instance(inst)
        head, pos = read_solution(sol)
        B = int(head.get("budget"))
        lam = F(head.get("lambda"))
        feasible, obj, parts, log = evaluate(order, T, p, cov, pos, B, lam)
    except (OSError, ValueError, KeyError, TypeError) as e:
        print("MALFORMED: %s" % e)
        return False
    print("instance %s: %d assets, %d periods; B=%d lambda=%s" % (head.get("instance"), len(order), len(T), B, lam))
    print("\n".join(log))
    print("breakdown: " + ", ".join("%s=%d" % kv for kv in parts.items()))
    print("feasible: %s" % feasible)
    print("objective = %d (expected %d; bar %d)" % (obj, expected, bar))
    if (B, lam) != (50, F(1, 100)) or head.get("instance") != "po_a200_t10_s00":
        print("solution header does not name the claimed cell (po_a200_t10_s00, B = 50, lambda = 0.01)")
        return False
    return feasible and obj == expected and obj < bar


def main(argv):
    if len(argv) != 5:
        print(__doc__)
        print("FAIL")
        return 2
    ok = verdict(argv)
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
