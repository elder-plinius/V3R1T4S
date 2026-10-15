#!/usr/bin/env python3
"""needs_minimax_solver.py -- CONTRARIAN lens, run 2026-10-15-0312.

Exact solver for "Risk or Safety" in POINTS-NEEDED coordinates, written from the BRIEF.md definition only.

State (a, i, j): the mover has a open points and still needs i points (banked-wise); the opponent needs j.
    P(a, i, j) = 1                                   if a >= i
    P(0, i, j) = 1/2 (1 - P(0, j, i)) + 1/2 P(1, i, j)          (forced toss)
    P(a, i, j) = max(continue, stop),  1 <= a < i, with
        continue = 1/2 (1 - P(0, j, i)) + 1/2 P(a + 1, i, j)
        stop     = 1 - P(0, j, i - a)

ALGORITHM (not policy iteration, not value iteration): exact minimax over pure turn-plans.
Inside the component {i, j} the only cyclic unknowns are x = P(0, i, j) and y = P(0, j, i).  A turn of the
mover is equivalent to a plan "collect k heads, then bank" (k = 1..i; k = i means toss until the win), because
the only randomness inside a turn is a tail, which ends the turn.  With s_k = 1 - P(0, j, i - k) (k < i), s_i = 1:
    x = F(y) = max_k L_k(y),   L_k(y) = (1 - 2^-k)(1 - y) + 2^-k s_k      (strictly decreasing lines)
    y = G(x) = max_m M_m(x),   M_m(x) = (1 - 2^-m)(1 - x) + 2^-m t_m      (opponent's lines)
Since F is strictly decreasing, F(G(x)) = F(max_m M_m(x)) = min_m max_k L_k(M_m(x)), and every L_k o M_m is affine
increasing with slope (1-2^-k)(1-2^-m) < 1.  Solving x = T(x) for T = min_m max_k h_km gives (proof in NOTES.md):
    x* = min_m max_k x_km,     x_km = root of x = L_k(M_m(x)) = (A_k + B_k C_m) / (1 - B_k D_m)
and for i = j:  x* = max_k A_k / (1 - B_k).  Then y* = G(x*), and x* = F(y*) is re-verified exactly.
Afterwards the within-turn values P(a, i, j), a = i-1 .. 1, follow by the backward max, and the identity
P(0, i, j) = 1/2 (1 - y*) + 1/2 P(1, i, j) == x* is re-checked exactly for every component.

Outputs (in the attempt folder):
    code/values_n1_30.txt         lines "n num/den" with P(0, n, n), n = 1..N
    code/needs_table_N30.json     every P(a, i, j) (0 <= a < i <= N, 1 <= j <= N), action data, optimal plan sets
    code/needs_solver_output.log  (captured stdout, by the caller)
"""
import sys, json, time, os
from fractions import Fraction as Fr

ATT = "."  # (package copy: the run-folder path constant was replaced by "." for publication)
DATA = "."  # package copy: the run-folder path constant was replaced by "." for publication


def solve(N):
    P0 = {}          # (i, j) -> P(0, i, j)
    PA = {}          # (a, i, j) -> P(a, i, j), 0 <= a < i
    ACT = {}         # (a, i, j) -> (cont, stop) exact pair for a >= 1
    PLANS = {}       # (i, j) -> sorted list of optimal k (turn plans) at the on-path start (0, i, j)
    one = Fr(1)

    def lines(i, j):
        """Lines A_k + B_k * y for the mover needing i against j (y = P(0, j, i))."""
        out = []
        for k in range(1, i + 1):
            p = Fr(1, 2 ** k)
            s = one if k == i else one - P0[(j, i - k)]
            out.append((k, (one - p) + p * s, -(one - p)))
        return out

    for S in range(2, 2 * N + 1):
        for i in range(max(1, S - N), min(N, S - 1) + 1):
            j = S - i
            if j < i:
                continue          # handle the unordered pair once, with i <= j
            L = lines(i, j)
            if i == j:
                x = max(A / (one - B) for (_, A, B) in L)
                y = x
            else:
                M = lines(j, i)   # opponent's lines C_m + D_m * x
                best_over_m = []
                for (_, C, D) in M:
                    r = max((A + B * C) / (one - B * D) for (_, A, B) in L)
                    best_over_m.append(r)
                x = min(best_over_m)
                y = max(C + D * x for (_, C, D) in M)
                # symmetric formula for y as an independent consistency check
                y2 = min(max((C + D * A) / (one - D * B) for (_, C, D) in M) for (_, A, B) in L)
                assert y2 == y, ("y mismatch", i, j)
            # exact re-verification of the two fixed-point equations
            assert x == max(A + B * y for (_, A, B) in L), ("F(y) != x", i, j)
            if i != j:
                assert y == max(C + D * x for (_, C, D) in lines(j, i)), ("G(x) != y", i, j)
            P0[(i, j)] = x
            P0[(j, i)] = y
            # optimal plan sets
            for (u, v, xu, yv, LL) in ((i, j, x, y, L), (j, i, y, x, None if i == j else lines(j, i))):
                if LL is None:
                    LL = L
                PLANS[(u, v)] = [k for (k, A, B) in LL if A + B * yv == xu]
            # within-turn values for both orientations
            for (u, v) in ((i, j), (j, i)):
                yy = P0[(v, u)]
                tail = (one - yy) / 2
                V = {u: one}
                for a in range(u - 1, 0, -1):
                    cont = tail + V[a + 1] / 2
                    stop = one - P0[(v, u - a)]
                    V[a] = cont if cont >= stop else stop
                    ACT[(a, u, v)] = (cont, stop)
                    PA[(a, u, v)] = V[a]
                x0 = tail + V[1] / 2
                assert x0 == P0[(u, v)], ("forced-toss identity fails", u, v)
                PA[(0, u, v)] = x0
    return P0, PA, ACT, PLANS


def plan_from_actions(ACT, i, j):
    """On-path toss counts derived from the per-position actions: all k such that continue is optimal at every
    a < k and stop is optimal at k (or k = i)."""
    ks = []
    for k in range(1, i + 1):
        ok = True
        for a in range(1, k):
            c, s = ACT[(a, i, j)]
            if c < s:
                ok = False
                break
        if not ok:
            break
        if k == i:
            ks.append(k)
        else:
            c, s = ACT[(k, i, j)]
            if s >= c:
                ks.append(k)
    return ks


def load_bfile(path):
    d = {}
    for line in open(path):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        k, v = line.split()
        d[int(k)] = int(v)
    return d


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    t0 = time.time()
    P0, PA, ACT, PLANS = solve(N)
    t1 = time.time()
    print("solve N=%d done in %.2f s; components=%d positions(a,i,j)=%d" % (N, t1 - t0, N * (N + 1) // 2, len(PA)))
    # cross-check plan sets two ways
    bad = 0
    for (i, j), ks in PLANS.items():
        if plan_from_actions(ACT, i, j) != ks:
            bad += 1
            print("PLAN MISMATCH", i, j, ks, plan_from_actions(ACT, i, j))
    print("plan sets (line formula vs per-position actions) disagree at %d pairs" % bad)
    # values
    with open(os.path.join(ATT, "code", "values_n1_30.txt"), "w") as f:
        for n in range(1, N + 1):
            v = P0[(n, n)]
            f.write("%d %d/%d\n" % (n, v.numerator, v.denominator))
    num = load_bfile(os.path.join(DATA, "b387261.txt"))
    den = load_bfile(os.path.join(DATA, "b387262.txt"))
    allok = True
    for n in range(1, N + 1):
        v = P0[(n, n)]
        if n in num:
            pub = Fr(num[n], den[n])
            exact_pair = (v.numerator == num[n] and v.denominator == den[n])
            allok &= exact_pair
            print("n=%2d P=%s/%s  OEIS num/den %s  (digits num=%d den=%d)" % (
                n, v.numerator, v.denominator, "MATCH" if exact_pair else "MISMATCH (pub %s)" % pub,
                len(str(v.numerator)), len(str(v.denominator))))
        else:
            print("n=%2d P=%s/%s  (new; digits num=%d den=%d; float %.15f)" % (
                n, v.numerator, v.denominator, len(str(v.numerator)), len(str(v.denominator)), float(v)))
    print("OEIS n=1..15 exact numerator AND denominator match:", allok)
    # ties anywhere in the table
    ties = [(a, i, j) for (a, i, j), (c, s) in ACT.items() if c == s]
    print("exact ties continue==stop anywhere in the N=%d needs table: %d %s" % (N, len(ties), ties[:20]))
    multi = {k: v for k, v in PLANS.items() if len(v) != 1}
    print("pairs (i,j) with a non-unique optimal plan set: %d %s" % (len(multi), sorted(multi.items())[:20]))
    # dump the table
    out = {"N": N,
           "P": {"%d,%d,%d" % k: "%d/%d" % (v.numerator, v.denominator) for k, v in PA.items()},
           "act": {"%d,%d,%d" % k: ("%d/%d" % (c.numerator, c.denominator), "%d/%d" % (s.numerator, s.denominator))
                   for k, (c, s) in ACT.items()},
           "plans": {"%d,%d" % k: v for k, v in PLANS.items()}}
    with open(os.path.join(ATT, "code", "needs_table_N%d.json" % N), "w") as f:
        json.dump(out, f)
    print("wrote needs_table_N%d.json; total time %.2f s" % (N, time.time() - t0))


if __name__ == "__main__":
    main()
