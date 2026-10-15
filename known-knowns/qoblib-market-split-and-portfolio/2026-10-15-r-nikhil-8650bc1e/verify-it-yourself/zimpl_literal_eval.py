#!/usr/bin/env python3
"""Self-check evaluator (step 5), written literally from QOBLIB 06-portfolio bqp_u3_c10.zpl + parameter_u3_c10.zpl.

It expands a count-format solution into the model's binary variables and evaluates the ZIMPL objective term by term:
  x[i,m,tau,t] = 1 for copies m = 1..count (the alignment the class's count format uses);
  y[c,t] (c = 0..3) = bits of the cash slack C - sum tau*x, which must be an integer in 0..15 (constraint c2);
  s2[c,t] (c = 0..6) = bits of the count slack B - sum x, which must be an integer in 0..127 (constraint c3).
Objective (upscale = 1), every coefficient rounded half away from zero on exact rationals:
  sum_t [ sum_{(i,m,ti),(j,n,tj)} round(lambda*ti*tj*cov[i,j,t]*p[i,t]*p[j,t]) x x
          - sum_k round(nu*unit*2^k) y[k,t] + sum_{i,m} round(rho*p[i,t]) x[i,m,-1,t] ]
  + sum_{t in TX minus {t_beg,t_end}} - sum_{i,m,tau} ( round(tau*(p[i,t+1]-p[i,t])) x[i,m,tau,t]
          - round(delta*p[i,t]) (x[..,t-1] + x[..,t] - 2 x[..,t-1] x[..,t]) )
  - sum_{i,m,tau} ( round(tau*(p[i,t_beg+1]-p[i,t_beg])) - round(delta*p[i,t_beg]) ) x[i,m,tau,t_beg]
  + sum_{i,m,tau} round(delta*p[i,t_end]) x[i,m,tau,t_end]
Usage: python3 -I zimpl_literal_eval.py INSTANCE_DIR SOLUTION BUDGET LAMBDA
"""
import gzip
import os
import sys
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction

UNIT, CASH = Fraction(100000), Fraction(1000000)
DELTA, NU, RHO, UB = Fraction("0.001"), Fraction("0.0001"), Fraction("0.000025"), 3


def rnd(q):
    # round half away from zero via Decimal on the exact rational (independent of pf_eval's floor-based zround)
    num, den = Decimal(q.numerator), Decimal(q.denominator)
    import decimal
    with decimal.localcontext() as ctx:
        ctx.prec = 200
        v = num / den
        return int(v.quantize(Decimal(1), rounding=ROUND_HALF_UP))


def lines(path):
    op = gzip.open if path.endswith(".gz") else open
    with op(path, "rt", encoding="utf-8") as f:
        for ln in f:
            ln = ln.strip()
            if ln and not ln.startswith("#"):
                yield ln.split()


def main():
    inst, sol, B, lam = sys.argv[1], sys.argv[2], int(sys.argv[3]), Fraction(sys.argv[4])
    pp = os.path.join(inst, "stock_prices.txt.gz")
    cp = os.path.join(inst, "covariance_matrices.txt.gz")
    raw = {}
    for t, s, v in lines(pp):
        raw[(s, int(t))] = Fraction(v)
    S = sorted({s for s, _ in raw})
    TX = sorted({t for _, t in raw})
    t_beg, t_end = TX[0], TX[-1]
    p = {(s, t): raw[(s, t)] * (UNIT / raw[(s, t_beg)]) for s in S for t in TX}
    x = {}  # (i, m, tau, t) -> 1
    for tok in lines(sol):
        if len(tok) == 4:
            t, s, lo, sh = int(tok[0]), tok[1], int(tok[2]), int(tok[3])
            assert s in S and t in TX and 0 <= lo <= UB and 0 <= sh <= UB, tok
            for m in range(1, lo + 1):
                x[(s, m, 1, t)] = 1
            for m in range(1, sh + 1):
                x[(s, m, -1, t)] = 1
    held = {t: [(i, m, tau) for (i, m, tau, tt) in x if tt == t] for t in TX}
    need = {(i, j, t) for t in TX for (i, _, _) in held[t] for (j, _, _) in held[t]}
    cov = {}
    for t, a, b, v in lines(cp):
        key = (a, b, int(t))
        if key in need:
            cov[key] = Fraction(v)
    C = CASH / UNIT
    ok = True
    obj = 0
    X = lambda i, m, tau, t: x.get((i, m, tau, t), 0)  # noqa: E731
    for t in TX:
        cash_slack = C - sum(tau for (i, m, tau) in held[t])
        cnt_slack = B - len(held[t])
        if not (cash_slack.denominator == 1 and 0 <= cash_slack <= 15 and 0 <= cnt_slack <= 127):
            print("t=%d constraint violated: cash slack %s, count slack %s" % (t, cash_slack, cnt_slack))
            ok = False
            continue
        y = [(int(cash_slack) >> k) & 1 for k in range(4)]
        risk = sum(rnd(lam * ti * tj * cov[(i, j, t)] * p[(i, t)] * p[(j, t)])
                   for (i, _, ti) in held[t] for (j, _, tj) in held[t])
        cash = -sum(rnd(NU * UNIT * 2 ** k) * y[k] for k in range(4))
        short = sum(rnd(RHO * p[(i, t)]) for (i, _, tau) in held[t] if tau == -1)
        obj += risk + cash + short
    for t in TX:
        if t in (t_beg, t_end):
            continue
        for i in S:
            for m in range(1, UB + 1):
                for tau in (1, -1):
                    a, b = X(i, m, tau, t - 1), X(i, m, tau, t)
                    obj -= rnd(tau * (p[(i, t + 1)] - p[(i, t)])) * b - rnd(DELTA * p[(i, t)]) * (a + b - 2 * a * b)
    for (i, m, tau, t) in x:
        if t == t_beg:
            obj -= rnd(tau * (p[(i, t_beg + 1)] - p[(i, t_beg)])) - rnd(DELTA * p[(i, t_beg)])
        if t == t_end:
            obj += rnd(DELTA * p[(i, t_end)])
    print("binary x variables set: %d" % len(x))
    print("constraints c2/c3 hold in every period: %s" % ok)
    print("objective (literal ZIMPL evaluation) = %d" % obj)
    sys.exit(0 if ok else 21)


if __name__ == "__main__":
    main()
