#!/usr/bin/env python3
"""Generalised class construction [[n,1,n-1-t;c]]_3 with X-type radical (lens small-cases, run 2026-10-17-1119).
Classes Z_1..Z_T (T <= 4), Z-code column P_t on Z_t, radical piece Y_t (dim e_t, supported in Z_t, orthogonal to all-ones);
the X partner x0_t of the Z-codeword vanishing on Z_t is chosen so that every vector of x0_t + Y_t has <= t zeros on Z_t.
Every word of C \\ R then has <= t zeros: d >= n - t.  dim R = sum e_t, c = n - 1 - dim R.
Class spec: list of (size, [y vectors as tuples of length size])."""
import random, itertools
P = [(1, 0), (0, 1), (1, 1), (1, 2)]
A = [(0, 1), (1, 0), (1, 2), (1, 1)]
inv = {1: 1, 2: 2}

def build(spec, tz, seed=0):
    rnd = random.Random(seed)
    n = sum(s for s, ys in spec)
    g1 = [0] * n; g2 = [0] * n; R0 = []; classes = []; pos = 0
    for t, (s, ys) in enumerate(spec):
        Z = list(range(pos, pos + s)); pos += s
        for i in Z: g1[i], g2[i] = P[t]
        loc = []
        for y in ys:
            assert len(y) == s and sum(y) % 3 == 0
            v = [0] * n
            for a, i in enumerate(Z): v[i] = y[a] % 3
            R0.append(v); loc.append(y)
        # all vectors of the local span
        span = {tuple((sum(cf[j] * loc[j][a] for j in range(len(loc)))) % 3 for a in range(s))
                for cf in itertools.product(range(3), repeat=len(loc))} if loc else {tuple([0] * s)}
        classes.append((Z, span))
    for attempt in range(200000):
        target = {}
        for t, (Z, span) in enumerate(classes):
            for _ in range(100000):
                x0 = [rnd.randrange(3) if any(v[a] for v in span) else rnd.randrange(1, 3) for a in range(len(Z))]
                if all(sum(1 for a in range(len(Z)) if (x0[a] + v[a]) % 3 == 0) <= tz for v in span):
                    break
            else:
                raise SystemExit('local problem infeasible for class %d' % t)
            target[t] = dict(zip(Z, x0))
        ux = [0] * n; vx = [0] * n
        for t, (Z, span) in enumerate(classes):
            a1, a2 = A[t]
            for i in Z:
                if a1:
                    vx[i] = rnd.randrange(3); ux[i] = ((target[t][i] - a2 * vx[i]) * inv[a1]) % 3
                else:
                    ux[i] = rnd.randrange(3); vx[i] = (target[t][i] * inv[a2]) % 3
        form = (sum(ux[i] * g2[i] for i in range(n)) - sum(g1[i] * vx[i] for i in range(n))) % 3
        if form: break
    else:
        raise SystemExit('no nondegenerate choice')
    rows = [v + [0] * n for v in R0] + [ux + g1, vx + g2]
    return n, len(R0), rows
