"""Joint route + timetable neighbourhood for TimPassLib.
For a freed event set F, the activities touching F are 'variable' (V). An OD pair is AFFECTED if its current shortest path uses a variable activity, or a path
that is cheapest when every variable activity takes its lower bound (an optimistic lower bound on any path) beats its current cost. Affected OD pairs get a
few candidate paths (current, optimistic, K-1 samples with random variable durations); CP-SAT chooses the timetable inside F and, for each affected OD pair,
which candidate path it uses (z_od >= length of the chosen path, minimised). Unaffected OD pairs keep their cost. The candidate set always contains the
current path, so the model is never worse than the incumbent; the exact total after re-routing is never worse than the model's value."""
import sys, os, random, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ptl
from ortools.sat.python import cp_model

def build_candidates(I, pi, V, K, rng):
    cur = ptl.costs_current(I, pi); opt = list(cur)
    for k in V: a = I.acts[k]; opt[k] = a[4] + (I.P if a[1] == 'change' else 0)
    samples = [opt]
    for _ in range(max(0, K - 1)):
        c = list(cur)
        for k in V: a = I.acts[k]; c[k] = rng.randint(a[4], a[5]) + (I.P if a[1] == 'change' else 0)
        samples.append(c)
    aff = []; n_unaff = 0
    for o, dests in I.od.items():
        dist, pred = ptl.tree(I, o, cur)
        trees = [ptl.tree(I, o, s) for s in samples] if K > 0 else []
        for dst, c in dests:
            b = ptl.best_arrival(I, dist, dst)
            if b is None: continue
            pc = ptl.path_arcs(I, pred, b); ccur = dist[b]
            touches = any(k in V for k in pc)
            # v2 (2026-11-16): the optimistic tree only supplies a candidate path; an OD pair is affected when its current path touches a variable
            # activity or a random-duration sample finds a strictly cheaper path (the all-lower-bound screen of v1 flagged most pairs on the R instances)
            cheaper = False
            for dd, _pp in trees[1:]:
                b3 = ptl.best_arrival(I, dd, dst)
                if b3 is not None and dd[b3] < ccur: cheaper = True; break
            if not touches and not cheaper: n_unaff += 1; continue
            paths = [pc]
            for dd, pp in trees:
                b2 = ptl.best_arrival(I, dd, dst)
                if b2 is None: continue
                p2 = ptl.path_arcs(I, pp, b2)
                if p2 not in paths: paths.append(p2)
            aff.append((c, ccur, paths))
    return aff, cur, n_unaff

def solve_joint(I, pi, F, secs, workers, seed, K, rng, max_aff=14000):
    T = I.T; V = {k for k, a in enumerate(I.acts) if a[2] in F or a[3] in F}
    Vp = {k for k in V if I.acts[k][1] in I.pax}
    aff, cur, n_unaff = build_candidates(I, pi, Vp, K, rng)
    if len(aff) > max_aff: return 'TOO_BIG', len(aff), 0, 0, None
    m = cp_model.CpModel(); t = {e: m.NewIntVar(0, T - 1, '') for e in F}; X = {}
    for k in V:
        _, typ, i, j, L, U = I.acts[k]
        ilo, ihi = (0, T - 1) if i in F else (pi[i], pi[i]); jlo, jhi = (0, T - 1) if j in F else (pi[j], pi[j])
        dmin, dmax = jlo - ihi, jhi - ilo; plo, phi = -((dmax - L) // T), (U - dmin) // T
        x = m.NewIntVar(L, U, ''); p = m.NewIntVar(plo, phi, ''); X[k] = x
        m.Add(x == (t[j] if j in F else pi[j]) - (t[i] if i in F else pi[i]) + T * p)
        d = ptl.dur(I, I.acts[k], pi); m.AddHint(x, d); m.AddHint(p, (d - (pi[j] - pi[i])) // T)
    for e in F: m.AddHint(t[e], pi[e])
    obj = []; cur_aff = 0; multi = 0; zl = []
    for c, ccur, paths in aff:
        cur_aff += c * ccur; zs = []; ys = []
        lo_hi = []
        for p in paths:
            const = sum(cur[k] for k in p if k not in Vp) + sum(I.P for k in p if k in Vp and I.acts[k][1] == 'change')
            vs = [k for k in p if k in Vp]
            lo_hi.append((const + sum(I.acts[k][4] for k in vs), const + sum(I.acts[k][5] for k in vs), const, vs))
        z = m.NewIntVar(min(x[0] for x in lo_hi), max(x[1] for x in lo_hi), ''); m.AddHint(z, ccur)
        if len(paths) == 1:
            const, vs = lo_hi[0][2], lo_hi[0][3]; m.Add(z >= const + sum(X[k] for k in vs))
        else:
            multi += 1; ys = [m.NewBoolVar('') for _ in paths]; m.AddExactlyOne(ys)
            for n, (lo, hi, const, vs) in enumerate(lo_hi):
                m.Add(z >= const + sum(X[k] for k in vs)).OnlyEnforceIf(ys[n]); m.AddHint(ys[n], 1 if n == 0 else 0)
        obj.append(c * z); zl.append((c, z))
    if not obj: return 'NO_AFFECTED', 0, 0, 0, None
    m.Minimize(sum(obj))
    sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = secs; sv.parameters.num_workers = workers; sv.parameters.random_seed = seed
    st = sv.Solve(m); name = sv.StatusName(st)
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE): return name, len(aff), cur_aff, cur_aff, None
    new = {e: sv.Value(t[e]) for e in F}
    # exact value of the model's solution: choose, for each affected OD, the cheapest candidate under the new durations
    return name, len(aff), cur_aff, sum(c * sv.Value(z) for c, z in zl), new
