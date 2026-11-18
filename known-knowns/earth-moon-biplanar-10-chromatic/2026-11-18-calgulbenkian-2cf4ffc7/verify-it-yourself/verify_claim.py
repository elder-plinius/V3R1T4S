#!/usr/bin/env python3
"""
Standalone, zero-dependency verifier for the 19-vertex, 92-edge 9-critical biplanar graph claim (p2).
Uses only the Python 3 standard library; if networkx is also installed, runs Boyer-Myrvold check_planarity
as a third independent planarity verification.
"""
import os, sys, json, hashlib, random
from collections import deque

def orient2d(ax, ay, bx, by, cx, cy):
    return (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)

def on_closed_segment(ax, ay, bx, by, px, py):
    if orient2d(ax, ay, bx, by, px, py) != 0:
        return False
    return min(ax, bx) <= px <= max(ax, bx) and min(ay, by) <= py <= max(ay, by)

def segments_disjoint_closed(ax, ay, bx, by, cx, cy, dx, dy):
    o1 = orient2d(ax, ay, bx, by, cx, cy)
    o2 = orient2d(ax, ay, bx, by, dx, dy)
    o3 = orient2d(cx, cy, dx, dy, ax, ay)
    o4 = orient2d(cx, cy, dx, dy, bx, by)
    if (o1 > 0 and o2 < 0 or o1 < 0 and o2 > 0) and (o3 > 0 and o4 < 0 or o3 < 0 and o4 > 0):
        return False
    if o1 == 0 and on_closed_segment(ax, ay, bx, by, cx, cy): return False
    if o2 == 0 and on_closed_segment(ax, ay, bx, by, dx, dy): return False
    if o3 == 0 and on_closed_segment(cx, cy, dx, dy, ax, ay): return False
    if o4 == 0 and on_closed_segment(cx, cy, dx, dy, bx, by): return False
    return True

def verify_fary_straight_line(n, edges, coords):
    if len(coords) != n:
        return False, "coords length != n"
    pts = []
    seen = set()
    for p in coords:
        if not isinstance(p, list) or len(p) != 2 or not isinstance(p[0], int) or not isinstance(p[1], int):
            return False, "non-integer coordinate"
        t = (p[0], p[1])
        if t in seen:
            return False, f"duplicate vertex coordinate {t}"
        seen.add(t)
        pts.append(t)
    elist = [(min(u, v), max(u, v)) for u, v in edges]
    for u, v in elist:
        ax, ay = pts[u]; bx, by = pts[v]
        for w in range(n):
            if w != u and w != v and on_closed_segment(ax, ay, bx, by, pts[w][0], pts[w][1]):
                return False, f"vertex {w} lies on segment ({u},{v})"
    m = len(elist)
    for i in range(m):
        u1, v1 = elist[i]; ax, ay = pts[u1]; bx, by = pts[v1]
        for j in range(i + 1, m):
            u2, v2 = elist[j]; cx, cy = pts[u2]; dx, dy = pts[v2]
            shared = {u1, v1} & {u2, v2}
            if not shared:
                if not segments_disjoint_closed(ax, ay, bx, by, cx, cy, dx, dy):
                    return False, f"crossing between disjoint edges ({u1},{v1}) and ({u2},{v2})"
            elif len(shared) == 1:
                s = next(iter(shared))
                o1 = v1 if u1 == s else u1
                o2 = v2 if u2 == s else u2
                sx, sy = pts[s]
                x1, y1 = pts[o1][0] - sx, pts[o1][1] - sy
                x2, y2 = pts[o2][0] - sx, pts[o2][1] - sy
                if x1 * y2 - y1 * x2 == 0 and (x1 * x2 + y1 * y2) > 0:
                    return False, f"collinear overlapping incident edges ({s},{o1}) and ({s},{o2})"
            else:
                return False, f"duplicate edge ({u1},{v1})"
    return True, "OK"

def verify_rotation_system_genus0(n, edges, rot):
    adj = [set() for _ in range(n)]
    for u, v in edges:
        if not (isinstance(u, int) and isinstance(v, int) and 0 <= u < n and 0 <= v < n) or u == v:
            return False, f"invalid edge ({u},{v})"
        if v in adj[u]:
            return False, f"parallel edge ({u},{v})"
        adj[u].add(v); adj[v].add(u)
    if len(rot) != n:
        return False, "rotation table size != n"
    nxt_around = {}
    for u in range(n):
        cyc = rot[u]
        if len(cyc) != len(adj[u]) or set(cyc) != adj[u]:
            return False, f"rotation list at vertex {u} does not match neighborhood"
        d = len(cyc)
        for idx, v in enumerate(cyc):
            nxt_around[(u, v)] = (u, cyc[(idx + 1) % d])
    vis_v = [False] * n
    used_darts = set()
    for start in range(n):
        if vis_v[start]:
            continue
        comp_v = []
        q = deque([start]); vis_v[start] = True
        while q:
            x = q.popleft(); comp_v.append(x)
            for y in adj[x]:
                if not vis_v[y]:
                    vis_v[y] = True; q.append(y)
        vc = len(comp_v)
        ec = sum(len(adj[x]) for x in comp_v) // 2
        if ec == 0:
            continue
        comp_darts = {(x, y) for x in comp_v for y in adj[x]}
        fc = 0
        for d0 in comp_darts:
            if d0 in used_darts:
                continue
            fc += 1
            cur = d0
            while cur not in used_darts:
                used_darts.add(cur)
                u, v = cur
                cur = nxt_around[(v, u)]
            if cur != d0:
                return False, "face permutation not a cycle"
        euler = vc - ec + fc
        if euler != 2:
            return False, f"component V={vc}, E={ec}, F={fc}, Euler={euler} != 2"
    return True, "OK"

def verify_drat(num_vars, clauses, drat_lines):
    active = []
    clause_multiset = {}
    for c in clauses:
        t = tuple(sorted(set(c)))
        idx = len(active); active.append(t)
        clause_multiset.setdefault(t, []).append(idx)
    alive = [True] * len(active)
    lit_occ = {l: [] for l in range(-num_vars, num_vars + 1) if l != 0}
    for idx, t in enumerate(active):
        for l in t:
            lit_occ[l].append(idx)

    val = [0] * (num_vars + 1)
    def lit_val(l):
        v = val[abs(l)]
        return v if l > 0 else -v
    def assign_lit(l, trail):
        var = abs(l)
        val[var] = 1 if l > 0 else -1
        trail.append(var)

    unit_indices = [idx for idx, c in enumerate(active) if len(c) <= 1]

    def is_rup(cand):
        trail = []
        q = deque()
        for l in cand:
            lv = lit_val(l)
            if lv == -1: continue
            if lv == 1:
                for v in trail: val[v] = 0
                return True
            assign_lit(-l, trail); q.append(-l)
        for idx in unit_indices:
            if not alive[idx]: continue
            c = active[idx]
            if len(c) == 0:
                for v in trail: val[v] = 0
                return True
            l0 = c[0]; lv0 = lit_val(l0)
            if lv0 == -1:
                for v in trail: val[v] = 0
                return True
            elif lv0 == 0:
                assign_lit(l0, trail); q.append(l0)
        conflict = False
        while q and not conflict:
            true_lit = q.popleft()
            for idx in lit_occ[-true_lit]:
                if not alive[idx]: continue
                c = active[idx]
                unassigned = 0; last_u = 0; sat = False
                for l in c:
                    lv = lit_val(l)
                    if lv == 1: sat = True; break
                    if lv == 0:
                        unassigned += 1; last_u = l
                        if unassigned > 1: break
                if sat: continue
                if unassigned == 0: conflict = True; break
                if unassigned == 1:
                    assign_lit(last_u, trail); q.append(last_u)
        for v in trail: val[v] = 0
        return conflict

    for raw in drat_lines:
        toks = raw.strip().split()
        if not toks: continue
        if toks[0] == "d":
            lits = [int(x) for x in toks[1:] if x != "0"]
            t = tuple(sorted(set(lits)))
            lst = clause_multiset.get(t)
            if lst:
                alive[lst.pop()] = False
        else:
            lits = [int(x) for x in toks if x != "0"]
            if len(lits) == 0:
                if is_rup(()):
                    return True, "VERIFIED EMPTY CLAUSE"
                return False, "empty clause failed RUP"
            if not is_rup(lits):
                pivot = lits[0]
                for idx in list(lit_occ[-pivot]):
                    if not alive[idx]: continue
                    resolvent = list(lits) + [x for x in active[idx] if x != -pivot]
                    sres = set(resolvent)
                    if any(-x in sres for x in sres): continue
                    if not is_rup(resolvent):
                        return False, f"DRAT step failed RUP and RAT: {lits}"
            t = tuple(sorted(set(lits)))
            idx = len(active); active.append(t); alive.append(True)
            clause_multiset.setdefault(t, []).append(idx)
            if len(t) <= 1: unit_indices.append(idx)
            for l in t: lit_occ[l].append(idx)
    return False, "DRAT ended without empty clause"

def canonical_certificate(n, edges):
    adj = [0] * n
    for u, v in edges:
        adj[u] |= (1 << v); adj[v] |= (1 << u)
    closed_adj = [adj[v] | (1 << v) for v in range(n)]

    def refine(cells):
        changed = True
        while changed:
            changed = False; new_cells = []
            cell_masks = []
            for cell in cells:
                m = 0
                for v in cell: m |= (1 << v)
                cell_masks.append(m)
            for cell in cells:
                if len(cell) <= 1:
                    new_cells.append(cell); continue
                sigs = {}
                for v in cell:
                    av = adj[v]
                    sig = tuple(bin(av & cm).count("1") for cm in cell_masks)
                    sigs.setdefault(sig, []).append(v)
                if len(sigs) == 1:
                    new_cells.append(cell)
                else:
                    changed = True
                    for sig in sorted(sigs.keys()):
                        new_cells.append(tuple(sigs[sig]))
            cells = tuple(new_cells)
        return cells

    def perm_key(perm):
        bits = []
        for i in range(n):
            ai = adj[perm[i]]
            for j in range(i + 1, n):
                bits.append("1" if (ai & (1 << perm[j])) else "0")
        return "".join(bits)

    init_cells = refine((tuple(range(n)),))
    best_key = [None]

    def search(cells):
        target_idx = -1; target_len = n + 1
        for idx, cell in enumerate(cells):
            if 1 < len(cell) < target_len:
                target_len = len(cell); target_idx = idx
        if target_idx == -1:
            k = perm_key([cell[0] for cell in cells])
            if best_key[0] is None or k < best_key[0]:
                best_key[0] = k
            return
        cell = cells[target_idx]
        prefix = cells[:target_idx]; suffix = cells[target_idx + 1:]
        reps = []
        for v in cell:
            if not any(adj[v] == adj[r] or closed_adj[v] == closed_adj[r] for r in reps):
                reps.append(v)
        for v in reps:
            rest = tuple(x for x in cell if x != v)
            search(refine(prefix + ((v,), rest) + suffix))

    search(init_cells)
    return hashlib.sha256(f"{n}:{best_key[0]}".encode("ascii")).hexdigest()

def exact_vertex_connectivity(n, adj_sets):
    # Menger's theorem via node-splitting unit-capacity Edmonds-Karp max flow
    best = n - 1
    for s in range(n):
        for t in range(s + 1, n):
            if t in adj_sets[s]:
                continue
            # Node u in {0..n-1} splits into 2*u (in) -> 2*u+1 (out) of capacity 1 (except s, t)
            N = 2 * n
            cap = {}
            nb = [[] for _ in range(N)]
            def add_dir(a, b, c):
                if (a, b) not in cap:
                    cap[(a, b)] = 0; cap[(b, a)] = 0
                    nb[a].append(b); nb[b].append(a)
                cap[(a, b)] += c
            for u in range(n):
                add_dir(2 * u, 2 * u + 1, n if u in (s, t) else 1)
                for v in adj_sets[u]:
                    add_dir(2 * u + 1, 2 * v, n)
            flow = 0
            src = 2 * s + 1; snk = 2 * t
            while True:
                parent = {src: -1}
                q = deque([src])
                while q and snk not in parent:
                    x = q.popleft()
                    for y in nb[x]:
                        if y not in parent and cap[(x, y)] > 0:
                            parent[y] = x; q.append(y)
                if snk not in parent:
                    break
                flow += 1
                cur = snk
                while cur != src:
                    p = parent[cur]
                    cap[(p, cur)] -= 1; cap[(cur, p)] += 1
                    cur = p
            if flow < best:
                best = flow
    return best

def main():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    obj_file = os.path.join(base, "object", "biplanar_9crit_n19_e92.json")
    drat_file = os.path.join(base, "object", "uncolorable_8.drat")
    bgs_file = os.path.join(base, "the-record-we-beat", "bgs_published_canonical_hashes.json")

    data = json.load(open(obj_file))
    n = data["num_vertices"]
    if n != 19:
        print("FAIL: num_vertices != 19"); sys.exit(1)

    E1 = [(min(u, v), max(u, v)) for u, v in data["edges_layer1"]]
    E2 = [(min(u, v), max(u, v)) for u, v in data["edges_layer2"]]
    s1, s2 = set(E1), set(E2)
    if len(s1) != len(E1) or len(s2) != len(E2):
        print("FAIL: duplicate edge inside a layer"); sys.exit(1)
    if s1 & s2:
        print("FAIL: layers E1 and E2 are not edge-disjoint"); sys.exit(1)
    E_all = sorted(s1 | s2)
    if len(E_all) != data["num_edges"] or len(E_all) != 92:
        print("FAIL: edge count mismatch"); sys.exit(1)

    adj = [set() for _ in range(n)]
    for u, v in E_all:
        if not (0 <= u < n and 0 <= v < n) or u == v:
            print("FAIL: invalid vertex or self-loop"); sys.exit(1)
        adj[u].add(v); adj[v].add(u)
    if min(len(adj[v]) for v in range(n)) < 8:
        print("FAIL: minimum degree < 8 (isolated or low-degree vertex)"); sys.exit(1)
    print(f"[1/7] Simple graph & partition verified: n={n}, |E1|={len(E1)}, |E2|={len(E2)}, |E|={len(E_all)}, deg in [{min(len(x) for x in adj)}..{max(len(x) for x in adj)}]")

    # Planarity Check #1 (Topological rotation system + Euler characteristic) & #2 (Straight-line Z^2 Fary)
    for idx, (elist, rot, coords) in enumerate([
        (E1, data["layer1_rotation_system"], data["layer1_integer_fary_coords"]),
        (E2, data["layer2_rotation_system"], data["layer2_integer_fary_coords"]),
    ], 1):
        ok_r, msg_r = verify_rotation_system_genus0(n, elist, rot)
        if not ok_r:
            print(f"FAIL: Layer {idx} rotation system genus-0 check failed: {msg_r}"); sys.exit(1)
        ok_f, msg_f = verify_fary_straight_line(n, elist, coords)
        if not ok_f:
            print(f"FAIL: Layer {idx} straight-line Z^2 Fary check failed: {msg_f}"); sys.exit(1)
    nx_note = "not installed (two stdlib planarity verifiers passed)"
    try:
        import networkx as nx
        for idx, elist in enumerate([E1, E2], 1):
            Gi = nx.Graph(); Gi.add_nodes_from(range(n)); Gi.add_edges_from(elist)
            ok_nx, _ = nx.check_planarity(Gi)
            if not ok_nx:
                print(f"FAIL: networkx check_planarity rejected Layer {idx}"); sys.exit(1)
        nx_note = "networkx Boyer-Myrvold check_planarity ALSO passed on both layers"
    except ImportError:
        pass
    print(f"[2/7] Biplanarity verified by independent topological + geometric verifiers ({nx_note})")

    # Proper 9-coloring check
    col9 = data["proper_9_coloring"]
    if len(col9) != n or any(not (isinstance(c, int) and 0 <= c < 9) for c in col9):
        print("FAIL: invalid 9-coloring vector"); sys.exit(1)
    for u, v in E_all:
        if col9[u] == col9[v]:
            print(f"FAIL: improper 9-coloring on edge ({u},{v})"); sys.exit(1)
    print("[3/7] Proper 9-coloring verified (chi <= 9)")

    # Regenerate 8-coloring CNF from scratch and verify DRAT UNSAT proof
    clq8 = data["symmetry_breaking_8_clique"]
    if len(clq8) != 8 or len(set(clq8)) != 8:
        print("FAIL: symmetry_breaking_8_clique does not have 8 distinct vertices"); sys.exit(1)
    for i in range(8):
        for j in range(i + 1, 8):
            if clq8[j] not in adj[clq8[i]]:
                print(f"FAIL: symmetry_breaking_8_clique pair ({clq8[i]},{clq8[j]}) is not an edge!"); sys.exit(1)
    k = 8
    clauses = []
    for ci, v in enumerate(clq8):
        clauses.append([v * k + ci + 1])
    for v in range(n):
        clauses.append([v * k + c + 1 for c in range(k)])
    for u, v in E_all:
        for c in range(k):
            clauses.append([-(u * k + c + 1), -(v * k + c + 1)])
    drat_lines = open(drat_file).read().splitlines()
    ok_d, msg_d = verify_drat(n * k, clauses, drat_lines)
    if not ok_d:
        print(f"FAIL: 8-coloring UNSAT DRAT proof rejected: {msg_d}"); sys.exit(1)
    print(f"[4/7] 8-coloring UNSAT DRAT proof verified on regenerated CNF ({len(clauses)} clauses, {len(drat_lines)} proof lines -> {msg_d}; chi == 9)")

    # Verify all 92 edge-deletion 8-colorings (exact 9-criticality!)
    ed_cols = data["edge_deletion_8_colorings"]
    if len(ed_cols) != len(E_all):
        print("FAIL: edge_deletion_8_colorings count mismatch"); sys.exit(1)
    for u, v in E_all:
        key = f"{u}-{v}"
        if key not in ed_cols:
            print(f"FAIL: missing 8-coloring for deleted edge {key}"); sys.exit(1)
        cm = ed_cols[key]
        if len(cm) != n or any(not (isinstance(c, int) and 0 <= c < 8) for c in cm):
            print(f"FAIL: invalid color range in {key}"); sys.exit(1)
        for a, b in E_all:
            if (a, b) == (u, v):
                continue
            if cm[a] == cm[b]:
                print(f"FAIL: improper 8-coloring on edge ({a},{b}) when deleting {key}"); sys.exit(1)
    print(f"[5/7] Exact 9-criticality verified: all {len(E_all)} edge-deleted subgraphs G - e have valid proper 8-colorings")

    # Structural indecomposability: connected complement, 5-connected, no clique cutsets, non-Hajos order
    comp_vis = {0}; q = deque([0])
    while q:
        x = q.popleft()
        for y in range(n):
            if y != x and y not in adj[x] and y not in comp_vis:
                comp_vis.add(y); q.append(y)
    if len(comp_vis) != n:
        print("FAIL: complement of G is disconnected (G is a join)"); sys.exit(1)
    kappa = exact_vertex_connectivity(n, adj)
    if kappa < 5:
        print(f"FAIL: vertex connectivity {kappa} < 5"); sys.exit(1)
    print(f"[6/7] Structural indecomposability verified: complement connected (non-join), vertex connectivity kappa={kappa}, n=19 < 21 (cannot be a Hajos sum)")

    # Canonical labelling & non-isomorphism against Boutin-Gethner-Sulanke published list
    chash = canonical_certificate(n, E_all)
    if chash != data["canonical_sha256"]:
        print(f"FAIL: canonical SHA256 mismatch: computed {chash} != {data['canonical_sha256']}"); sys.exit(1)
    rng = random.Random(314159)
    for _ in range(5):
        perm = list(range(n)); rng.shuffle(perm)
        pe = [(perm[u], perm[v]) for u, v in E_all]
        if canonical_certificate(n, pe) != chash:
            print("FAIL: canonical labeller failed permutation invariance"); sys.exit(1)
    bgs = json.load(open(bgs_file))["graphs"]
    bgs_hashes = {g["canonical_sha256"] for g in bgs}
    if chash in bgs_hashes:
        print("FAIL: graph is isomorphic to a published Boutin-Gethner-Sulanke graph!"); sys.exit(1)
    print(f"[7/7] Canonical SHA256 verified ({chash[:16]}...), non-isomorphic to all {len(bgs)} Sulanke + Boutin-Gethner-Sulanke published graphs")
    print("PASS")

if __name__ == "__main__":
    main()
