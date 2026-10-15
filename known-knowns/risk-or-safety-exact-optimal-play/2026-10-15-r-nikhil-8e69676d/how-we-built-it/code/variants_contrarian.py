#!/usr/bin/env python3
"""variants.py -- CONTRARIAN lens: definitional variants of "Risk or Safety" for n <= 8 (angle 7).

A SECOND, independent exact solver, in banked coordinates (a, b, c), parameterised by the rule variant:
per strongly connected component {b, c} (processed in decreasing b + c) it guesses a policy by float value
iteration, then runs exact policy iteration: exact Gaussian elimination (fractions.Fraction) of the policy's
linear system, exact improvement, repeat until no action strictly improves.  The final tables are re-verified
exactly against the variant's own Bellman equations.

Variants:
  bank      (i)   the BRIEF rules: P = 1 when a + b >= n; forced toss at a = 0; stop = 1 - P(0, c, a + b)
  mustbank  (ii)  reaching n with open points is not a win: P = 1 only when b >= n; positions with a + b >= n are
                  decision positions (toss, or stop = bank and win); a runs up to n - b + 1 (cap; beyond: value 1)
  pass      (iii) a = 0 also allows "pass" (stop with nothing open): value 1 - P(0, c, b)
  choosex   (iv)  "choose x coins, all must be heads": positions (0, b, c) only, action x = 1..n-b,
                  value (1 - 2^-x)(1 - P(0, c, b)) + 2^-x * (1 if b + x >= n else 1 - P(0, c, b + x))
  typed32   (vi)  literal reading of the equations as TYPED in the paper's Section 3.2 (n = 3 list): after a
                  further head the "stop" branch banks only ONE point: stop at a >= 1 = 1 - P(0, c, b + 1)
  second    (v)   second player moves first: the starting player's win probability is 1 - P_bank(0, 0, 0) for the
                  other player, i.e. report the second player's value 1 - P(0,0,0)
"""
import sys, os
from fractions import Fraction as Fr

ATT = "."  # package copy: the run-folder path constant was replaced by "." for publication
DATA = "."  # package copy: the run-folder path constant was replaced by "." for publication
HALF = Fr(1, 2)
ONE = Fr(1)


def build(n, variant):
    """Return dict pos -> list of actions; an action is (name, const, [(coef, pos), ...]) meaning
    value = const + sum coef * P(pos)."""
    G = {}
    for b in range(n):
        for c in range(n):
            if variant == "choosex":
                acts = []
                for x in range(1, n - b + 1):
                    p = Fr(1, 2 ** x)
                    const = (1 - p) * 1                      # (1-p) * (1 - P(0,c,b)) -> const part (1-p)
                    terms = [(-(1 - p), (0, c, b))]
                    if b + x >= n:
                        const += p
                    else:
                        const += p
                        terms.append((-p, (0, c, b + x)))
                    acts.append(("x=%d" % x, const, terms))
                G[(0, b, c)] = acts
                continue
            amax = n - b - 1 if variant != "mustbank" else n - b + 1
            for a in range(0, amax + 1):
                # toss (continue): 1/2 (1 - P(0,c,b)) + 1/2 W(a+1, b, c)
                const = HALF
                terms = [(-HALF, (0, c, b))]
                if variant == "mustbank":
                    if a + 1 > amax:
                        const += HALF                         # cap: beyond the last listed a, value 1 (stop=1 there)
                    else:
                        terms.append((HALF, (a + 1, b, c)))
                else:
                    if a + 1 + b >= n:
                        const += HALF
                    else:
                        terms.append((HALF, (a + 1, b, c)))
                acts = [("toss", const, terms)]
                if a == 0:
                    if variant == "pass":
                        acts.append(("pass", ONE, [(-ONE, (0, c, b))]))
                else:
                    if variant == "typed32":
                        bb = b + 1
                    else:
                        bb = a + b
                    if bb >= n:
                        acts.append(("stop", ONE, []))
                    else:
                        acts.append(("stop", ONE, [(-ONE, (0, c, bb))]))
                G[(a, b, c)] = acts
    return G


def gauss(rows, unknowns):
    """Solve exactly: rows[u] = (dict v->coef, rhs) meaning sum coef*X_v = rhs."""
    idx = {u: k for k, u in enumerate(unknowns)}
    m = len(unknowns)
    A = [[Fr(0)] * (m + 1) for _ in range(m)]
    for u, (co, rhs) in rows.items():
        r = idx[u]
        for v, cf in co.items():
            A[r][idx[v]] += cf
        A[r][m] = rhs
    for col in range(m):
        piv = next((r for r in range(col, m) if A[r][col] != 0), None)
        if piv is None:
            raise ZeroDivisionError("singular system")
        A[col], A[piv] = A[piv], A[col]
        pv = A[col][col]
        rowc = [x / pv for x in A[col]]
        A[col] = rowc
        for r in range(m):
            if r != col and A[r][col] != 0:
                f = A[r][col]
                A[r] = [x - f * y for x, y in zip(A[r], rowc)]
    return {u: A[idx[u]][m] for u in unknowns}


def solve(n, variant, log):
    G = build(n, variant)
    comps = {}
    for (a, b, c) in G:
        comps.setdefault((min(b, c), max(b, c)), []).append((a, b, c))
    order = sorted(comps, key=lambda k: -(k[0] + k[1]))
    V = {}           # exact values of solved positions
    POL = {}
    iters_total = 0
    for key in order:
        U = sorted(comps[key])
        Uset = set(U)

        def aval(act, cur):
            name, const, terms = act
            s = const
            for cf, pos in terms:
                s += cf * (cur[pos] if pos in Uset else V[pos])
            return s
        # float value-iteration guess
        fv = {u: 0.5 for u in U}
        fV = {}
        for it in range(20000):
            delta = 0.0
            for u in U:
                best = None
                for (name, const, terms) in G[u]:
                    s = float(const)
                    for cf, pos in terms:
                        s += float(cf) * (fv[pos] if pos in Uset else float(V[pos]))
                    if best is None or s > best:
                        best = s
                delta = max(delta, abs(best - fv[u]))
                fv[u] = best
            if delta < 1e-15:
                break
        pol = {}
        for u in U:
            vals = []
            for k, (name, const, terms) in enumerate(G[u]):
                s = float(const)
                for cf, pos in terms:
                    s += float(cf) * (fv[pos] if pos in Uset else float(V[pos]))
                vals.append((s, -k))
            pol[u] = -max(vals)[1]
        # exact policy iteration
        for it in range(200):
            iters_total += 1
            rows = {}
            for u in U:
                name, const, terms = G[u][pol[u]]
                co = {u: ONE}
                rhs = const
                for cf, pos in terms:
                    if pos in Uset:
                        co[pos] = co.get(pos, Fr(0)) - cf
                    else:
                        rhs += cf * V[pos]
                rows[u] = (co, rhs)
            cur = gauss(rows, U)
            changed = False
            for u in U:
                here = aval(G[u][pol[u]], cur)
                bestk, bestv = pol[u], here
                for k, act in enumerate(G[u]):
                    v = aval(act, cur)
                    if v > bestv:
                        bestk, bestv = k, v
                if bestk != pol[u]:
                    pol[u] = bestk
                    changed = True
            if not changed:
                break
        else:
            raise RuntimeError("policy iteration did not converge in component %r" % (key,))
        for u in U:
            V[u] = cur[u]
            POL[u] = G[u][pol[u]][0]
    # exact re-verification of the variant's Bellman equations on the final table
    bad = 0
    ties = 0
    for u, acts in G.items():
        vals = []
        for (name, const, terms) in acts:
            s = const
            for cf, pos in terms:
                s += cf * V[pos]
            vals.append(s)
        if V[u] != max(vals):
            bad += 1
        if len(vals) > 1 and sorted(vals)[-1] == sorted(vals)[-2]:
            ties += 1
    return V, POL, bad, ties, iters_total


def main():
    num, den = {}, {}
    for fn, dst in (("b387261.txt", num), ("b387262.txt", den)):
        for line in open(os.path.join(DATA, fn)):
            line = line.strip()
            if line and not line.startswith("#"):
                k, v = line.split()
                dst[int(k)] = int(v)
    oeis = {k: Fr(num[k], den[k]) for k in num}
    import json
    T = json.load(open(os.path.join(ATT, "code", "needs_table_N30.json")))
    NEED = {tuple(map(int, k.split(","))): Fr(*map(int, v.split("/"))) for k, v in T["P"].items()}
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    summary = {}
    for variant in ("bank", "mustbank", "pass", "choosex", "typed32"):
        for n in range(1, nmax + 1):
            V, POL, bad, ties, its = solve(n, variant, None)
            p = V[(0, 0, 0)]
            match = (p == oeis[n])
            extra = ""
            if variant == "bank":
                # cross-check every position against the points-needed minimax table (independent algorithm)
                diff = sum(1 for (a, b, c), v in V.items() if NEED[(a, n - b, n - c)] != v)
                extra = " | vs needs-minimax table: %d/%d positions differ" % (diff, len(V))
            if variant in ("pass",):
                npass = sum(1 for u, nm in POL.items() if nm == "pass")
                extra = " | positions choosing pass: %d" % npass
            if variant == "mustbank":
                extra = " | P at a+b>=n positions all 1: %s" % all(v == 1 for (a, b, c), v in V.items() if a + b >= n)
            print("%-8s n=%d P000=%s  OEIS %s  (bellman violations %d, exact ties %d, PI iterations %d)%s" % (
                variant, n, p, "MATCH" if match else "DIFFER (pub %s; diff %.3e)" % (oeis[n], float(p - oeis[n])),
                bad, ties, its, extra))
            summary.setdefault(variant, []).append(match)
            sys.stdout.flush()
    for n in range(1, nmax + 1):
        V, POL, bad, ties, its = solve(n, "bank", None)
        q = 1 - V[(0, 0, 0)]
        print("second   n=%d second-player value 1-P000=%s  OEIS %s" % (n, q, "MATCH" if q == oeis[n] else "DIFFER"))
        summary.setdefault("second", []).append(q == oeis[n])
    print("SUMMARY (variant: reproduces OEIS for n=1..%d?)" % nmax)
    for k, v in summary.items():
        print("  %-8s %s  %s" % (k, "ALL MATCH" if all(v) else "no (matches at n=%s)" % [i + 1 for i, t in enumerate(v) if t], ""))


if __name__ == "__main__":
    main()
