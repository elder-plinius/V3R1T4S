"""Independent checks of the canonical-geodesic rules, written from the definitions (complete paths, no incremental
state; different structure from the Go enumerators).

Part A (ground truth): random site configurations in a box (outside closed). For the open cluster of the centre,
compute intrinsic distances by BFS and parents by the rule "neighbour at distance d-1 with the smallest direction
index" (+x,-x,+y,-y,+z,-z), as seen from the child. For every vertex up to distance NMAX, take its tree path and
check: (1) it is a neighbour-avoiding walk; (2) every site of F (shortcut sites and wrong-rank turn corners) is
closed; (3) no detour pair candidate (as in canon2) has both sites open; (4) every child of the endpoint is a valid
extension (off the path, adjacent to no other path vertex, not in F).

Part B (independent enumeration): all N-step NAWs from the origin, generated as complete tuples; F and ext computed
from each complete path; prints the ext histogram as "EXT N f:count ..." for comparison with the Go output.

usage: python groundtruth.py A [configs] | python groundtruth.py B N
"""
import random
import sys
from collections import deque

DIRS = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]


def add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def nbrs(x):
    return [add(x, d) for d in DIRS]


def dir_index(frm, to):
    return DIRS.index(sub(to, frm))


def is_naw(path):
    idx = {v: i for i, v in enumerate(path)}
    if len(idx) != len(path):
        return False
    for i, v in enumerate(path):
        for w in nbrs(v):
            j = idx.get(w)
            if j is not None and abs(i - j) != 1:
                return False
    return True


def forced_closed(path):
    """F from the definition: shortcut sites and wrong-rank turn corners."""
    on = set(path)
    F = set()
    adjidx = {}
    for i, v in enumerate(path):
        for w in nbrs(v):
            if w not in on:
                adjidx.setdefault(w, []).append(i)
    for w, ids in adjidx.items():
        if max(ids) - min(ids) >= 3:
            F.add(w)
    for k in range(1, len(path) - 1):
        a, b, c = path[k - 1], path[k], path[k + 1]
        if sub(c, b) != sub(b, a):
            u = add(a, sub(c, b))
            if dir_index(c, u) < dir_index(c, b):
                F.add(u)
    return F, adjidx


def pair_candidates(path, F, adjidx):
    """All (t, z) detour-pair candidates of canon2's rules (before the greedy disjoint choice)."""
    on = set(path)
    out = []
    for j in range(1, len(path)):
        y = path[j]
        back = dir_index(y, path[j - 1])
        for ez, d in enumerate(DIRS):
            z = add(y, d)
            if z in on or z in F:
                continue
            for t in nbrs(z):
                if t == y or t in on or t in F or t not in adjidx:
                    continue
                ids = adjidx[t]
                # adjacency to path vertices with index < j only (the rule is applied when v_j is added)
                early = [i for i in ids if i < j]
                if not early:
                    continue
                shortcut = min(early) <= j - 5
                competitor = j >= 3 and (j - 3) in early and ez < back
                if shortcut or competitor:
                    out.append((t, z))
    return out


def part_a(configs, L=15, NMAX=10, seed=1):
    rng = random.Random(seed)
    c = (L // 2, L // 2, L // 2)
    stats = dict(paths=0, Fsites=0, pairs=0, children=0)
    for it in range(configs):
        p = rng.choice([0.3, 0.4, 0.5, 0.6])
        opn = {(x, y, z) for x in range(L) for y in range(L) for z in range(L) if rng.random() < p}
        opn.add(c)
        dist = {c: 0}
        q = deque([c])
        while q:
            v = q.popleft()
            for w in nbrs(v):
                if w in opn and w not in dist:
                    dist[w] = dist[v] + 1
                    q.append(w)
        parent = {}
        for v, d in dist.items():
            if d == 0:
                continue
            for di in range(6):  # smallest direction index from the child
                w = add(v, DIRS[di])
                if dist.get(w) == d - 1:
                    parent[v] = w
                    break
        children = {}
        for v, w in parent.items():
            children.setdefault(w, []).append(v)
        for x, d in dist.items():
            if d > NMAX:
                continue
            path = [x]
            while path[-1] != c:
                path.append(parent[path[-1]])
            path.reverse()
            stats["paths"] += 1
            assert is_naw(path), ("not NAW", path)
            F, adjidx = forced_closed(path)
            for s in F:
                assert s not in opn, ("open forced-closed site", path, s)
            stats["Fsites"] += len(F)
            for t, z in pair_candidates(path, F, adjidx):
                assert not (t in opn and z in opn), ("pair both open", path, t, z)
                stats["pairs"] += 1
            on = set(path)
            for y in children.get(x, []):
                assert y not in on and y not in F, ("bad child", path, y)
                assert sum(1 for w in nbrs(y) if w in on) == 1, ("child adjacent to path", path, y)
                stats["children"] += 1
    print("PART A PASS: %d configs, %d tree paths, %d forced-closed sites, %d pair candidates, %d children checked"
          % (configs, stats["paths"], stats["Fsites"], stats["pairs"], stats["children"]))


def part_b(N):
    hist = {}
    total = 0
    stack = [[(0, 0, 0)]]
    while stack:
        path = stack.pop()
        if len(path) == N + 1:
            if not is_naw(path):
                continue
            total += 1
            F, _ = forced_closed(path)
            on = set(path)
            e = 0
            for y in nbrs(path[-1]):
                if y in on or y in F:
                    continue
                if sum(1 for w in nbrs(y) if w in on) == 1:
                    e += 1
            hist[len(F)] = hist.get(len(F), 0) + e
            continue
        for d in DIRS:
            nxt = add(path[-1], d)
            cand = path + [nxt]
            if is_naw(cand):  # prefix of a NAW is a NAW: prune early
                stack.append(cand)
    print("TOTAL %d %d" % (N, total))
    print("EXT %d %s" % (N, " ".join("%d:%d" % (f, hist[f]) for f in sorted(hist))))


def part_c(N, prefix):
    """Like part_b, but only walks whose step sequence starts with `prefix` (direction indices); unweighted."""
    path = [(0, 0, 0)]
    for di in prefix:
        path.append(add(path[-1], DIRS[di]))
    assert is_naw(path), "prefix is not a NAW"
    hist = {}
    total = 0
    stack = [path]
    while stack:
        path = stack.pop()
        if len(path) == N + 1:
            total += 1
            F, _ = forced_closed(path)
            on = set(path)
            e = sum(1 for y in nbrs(path[-1])
                    if y not in on and y not in F and sum(1 for w in nbrs(y) if w in on) == 1)
            hist[len(F)] = hist.get(len(F), 0) + e
            continue
        for d in DIRS:
            cand = path + [add(path[-1], d)]
            if is_naw(cand):
                stack.append(cand)
    return total, hist


if __name__ == "__main__":
    if sys.argv[1] == "A":
        part_a(int(sys.argv[2]) if len(sys.argv) > 2 else 200)
    elif sys.argv[1] == "C":
        total, hist = part_c(int(sys.argv[2]), [int(ch) for ch in sys.argv[3]])
        print("TOTAL %s %d" % (sys.argv[2], total))
        print("EXT %s %s" % (sys.argv[2], " ".join("%d:%d" % (f, hist[f]) for f in sorted(hist))))
    else:
        part_b(int(sys.argv[2]))
