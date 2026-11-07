"""Independent p2 checker (does not import the search or build code). Input: JSON with n and edges.
Checks the properties arXiv:2602.23282 proves for A.P.-hypergraphs of (4,5)-sets, read with vertex labels as the
order: Definition 1.7 (3-uniform), Lemma 2.4 (distinct middles, never the first or last vertex; m <= n-2),
Lemma 2.5 (linear), Lemma 5.2 (F7-free; F7 = {012,034,056,135,246}) by two independent embedding searches.
alpha by CP-SAT (OPTIMAL, bound = value) and by pysat: a witness of size alpha and UNSAT for alpha+1."""
import sys, json, itertools, time
from fractions import Fraction as F

F7 = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (2, 4, 6)]

def f7_method_a(n, E):
    # star-based: F7 vertex 0 has degree 3, its three edges are completed by two transversal edges
    S = set(E); inc = [[] for _ in range(n)]
    for e in E:
        for v in e: inc[v].append(e)
    for c in range(n):
        for a, b, d in itertools.combinations(inc[c], 3):
            ra = [v for v in a if v != c]; rb = [v for v in b if v != c]; rd = [v for v in d if v != c]
            for x1, y1 in (ra, ra[::-1]):
                for x2, y2 in (rb, rb[::-1]):
                    for x3, y3 in (rd, rd[::-1]):
                        if tuple(sorted((x1, x2, x3))) in S and tuple(sorted((y1, y2, y3))) in S:
                            return (c, a, b, d)
    return None

def f7_method_b(n, E):
    # generic backtracking embedding of the 7 F7 vertices; each F7 edge must map onto an edge of H
    S = set(E); inc = [[] for _ in range(n)]
    for e in E:
        for v in e: inc[v].append(e)
    def rec(i, phi):
        if i == len(F7):
            return dict(phi)
        f = F7[i]
        mapped = [phi.get(v) for v in f]
        if all(m is not None for m in mapped):
            return rec(i + 1, phi) if tuple(sorted(mapped)) in S else None
        cands = E if all(m is None for m in mapped) else inc[next(m for m in mapped if m is not None)]
        for e in cands:
            for perm in itertools.permutations(e):
                ok = True; new = {}
                for v, h in zip(f, perm):
                    if v in phi:
                        if phi[v] != h: ok = False; break
                    else:
                        if h in phi.values() or h in new.values(): ok = False; break
                        new[v] = h
                if not ok: continue
                phi2 = dict(phi); phi2.update(new)
                r = rec(i + 1, phi2)
                if r: return r
        return None
    return rec(0, {})

def main(path):
    d = json.load(open(path)); n = d["n"]; E = [tuple(sorted(e)) for e in d["edges"]]
    res = {}
    res["three_uniform"] = all(len(set(e)) == 3 and all(0 <= v < n for v in e) for e in E) and len(set(E)) == len(E)
    pc = {}
    for e in E:
        for pr in itertools.combinations(e, 2): pc[pr] = pc.get(pr, 0) + 1
    res["linear"] = max(pc.values()) <= 1
    mids = [e[1] for e in E]
    res["middles_distinct"] = len(set(mids)) == len(mids)
    res["middles_not_ends"] = all(0 < x < n - 1 for x in mids)
    res["m_le_n_minus_2"] = len(E) <= n - 2
    t = time.time(); a = f7_method_a(n, E); res["f7_free_a"] = a is None; ta = time.time() - t
    t = time.time(); b = f7_method_b(n, E); res["f7_free_b"] = b is None; tb = time.time() - t
    from ortools.sat.python import cp_model
    md = cp_model.CpModel(); y = [md.NewBoolVar("y%d" % i) for i in range(n)]
    for e in E: md.Add(sum(y[v] for v in e) <= 2)
    md.Maximize(sum(y)); s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 600; s.parameters.num_workers = 4
    st = s.Solve(md); alpha = int(s.ObjectiveValue()); bound = int(round(s.BestObjectiveBound()))
    W = [i for i in range(n) if s.Value(y[i])]
    res["cpsat"] = (s.StatusName(st), alpha, bound)
    res["witness_independent"] = all(not all(v in set(W) for v in e) for e in E) and len(W) == alpha
    from pysat.formula import CNF
    from pysat.card import CardEnc, EncType
    from pysat.solvers import Solver
    cnf = CNF()
    for e in E: cnf.append([-(v + 1) for v in e])
    card = CardEnc.atleast(lits=list(range(1, n + 1)), bound=alpha + 1, top_id=n, encoding=EncType.seqcounter)
    cnf.extend(card.clauses)
    t = time.time()
    with Solver(name="cd19", bootstrap_with=cnf.clauses) as sv:
        sat = sv.solve()
    res["pysat_alpha_plus_1"] = "SAT" if sat else "UNSAT"; tp = time.time() - t
    r = F(alpha, n)
    res["ratio"] = str(r); res["below_5_9"] = r < F(5, 9); res["at_least_9_17"] = r >= F(9, 17); res["below_4_7"] = r < F(4, 7)
    res["alpha_dp_in_file"] = d.get("alpha_dp"); res["dp_agrees"] = d.get("alpha_dp") == alpha
    tau = n - alpha; res["henning_yeo_17tau<=5n+3m"] = 17 * tau <= 5 * n + 3 * len(E); res["I11_11tau<=3n+2m"] = 11 * tau <= 3 * n + 2 * len(E)
    print(json.dumps({"file": path, "n": n, "m": len(E), **res, "times_f7_a_b_pysat": [round(ta, 2), round(tb, 2), round(tp, 2)]}))
    ok = all(res[k] for k in ("three_uniform", "linear", "middles_distinct", "middles_not_ends", "m_le_n_minus_2", "f7_free_a", "f7_free_b",
                                "witness_independent", "below_5_9", "at_least_9_17", "dp_agrees")) and res["cpsat"][0] == "OPTIMAL" and \
        res["cpsat"][1] == res["cpsat"][2] and res["pysat_alpha_plus_1"] == "UNSAT"
    print("P2_CHECK:", "PASS" if ok else "FAIL")

main(sys.argv[1])
