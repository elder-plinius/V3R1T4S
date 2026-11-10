"""Independent checks of window.py.

1. Random explicit exploration trees embedded in Z^2 (actual coordinates, eps-adjacency from the paper's definition
   with min = smaller coordinate sum), around a selected vertex b2 with parent c. The posterior of eps(b2) given all
   tree-edge observations is computed by brute-force enumeration over the eps of every tree vertex (no message
   passing, no orientation labels). For each tree the domination margin at p is computed directly; it must be
   >= the worst-case margin that window.py's cone check reports at the same p and a depth covering the tree.
2. The root step: the root has four children; the law of their eta given eps(0) open must dominate pi_{1-p}^4.

usage: python validate.py <p as a fraction> <n_trees> <seed>
"""
import random
import sys
from fractions import Fraction as F
from itertools import product

sys.path.insert(0, __import__("os").path.dirname(__file__))
import window as W  # noqa: E402

ALL = W.ALL
OPEN = W.OPEN
NB = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def eta(sv, sw, v, w):
    if sum(v) < sum(w):
        return W.adj(sv, sw)
    return W.adj(sw, sv)


def random_tree(rng, depth):
    """Explicit tree: c at (0,0), b2 at a random neighbour, parent chain and side subtrees grown randomly without
    reusing sites. Returns (nodes: coord -> parent coord or None, obs: coord -> eta to parent, b2)."""
    used = {}
    obs = {}
    c = (0, 0)
    b2 = rng.choice(NB)
    used[c] = None
    used[b2] = c
    obs[b2] = 1
    frontier = []  # processed vertices whose free neighbours may become children

    # parent chain above c
    cur = c
    for _ in range(rng.randint(0, depth)):
        cand = [(cur[0] + dx, cur[1] + dy) for dx, dy in NB if (cur[0] + dx, cur[1] + dy) not in used]
        if not cand:
            break
        par = rng.choice(cand)
        used[par] = None
        used[cur] = par
        obs[cur] = 1
        frontier.append(par)
        cur = par
    # c and chain vertices are processed: give their free neighbours random outcomes; recurse a little
    todo = [c] + frontier
    budget = 14
    while todo and budget > 0:
        v = todo.pop(0)
        for dx, dy in NB:
            u = (v[0] + dx, v[1] + dy)
            if u in used or (u[0] - b2[0], u[1] - b2[1]) in [(0, 0)]:
                continue
            r = rng.random()
            if r < 0.25:
                continue  # absent (left unexplored for this check; it plays no role)
            used[u] = v
            budget -= 1
            if r < 0.55:
                obs[u] = 0
            else:
                obs[u] = 1
                if rng.random() < 0.5 and budget > 0:
                    todo.append(u)
    return used, obs, b2


def posterior_b2(p, used, obs, b2):
    pi = {s: (p if s[0] else 1 - p) * (p if s[1] else 1 - p) for s in ALL}
    verts = list(used)
    idx = {v: i for i, v in enumerate(verts)}
    edges = [(v, used[v], obs[v]) for v in verts if used[v] is not None]
    w = {s: F(0) for s in OPEN}
    for states in product(ALL, repeat=len(verts)):
        ok = True
        for v, u, e in edges:
            if eta(states[idx[v]], states[idx[u]], v, u) != bool(e):
                ok = False
                break
        if not ok:
            continue
        t = F(1)
        for s in states:
            t *= pi[s]
        w[states[idx[b2]]] += t
    return w


def posterior_bp(p, used, obs, b2):
    """Same posterior by message passing with window.py's orientation-labelled adjacency W.A (child orientation
    'max' if the child's coordinate sum is larger than the parent's)."""
    pi = {s: (p if s[0] else 1 - p) * (p if s[1] else 1 - p) for s in ALL}
    nbrs = {v: [] for v in used}
    for v, u in used.items():
        if u is not None:
            nbrs[v].append(u)
            nbrs[u].append(v)

    def edge_ok(sa, va, sb, vb):
        # the observed eta on the tree edge {va, vb}, via orientation labels
        child, par = (va, vb) if used.get(va) == vb else (vb, va)
        schild, spar = (sa, sb) if child == va else (sb, sa)
        o = "max" if sum(child) > sum(par) else "min"
        return W.A(spar, schild, o) == bool(obs[child])

    def msg(frm, to):
        out = {}
        for st in ALL:
            tot = F(0)
            for sf in ALL:
                if not edge_ok(sf, frm, st, to):
                    continue
                t = pi[sf]
                for z in nbrs[frm]:
                    if z != to:
                        t *= msg(z, frm)[sf]
                tot += t
            out[st] = tot
        return out

    w = {}
    for s in OPEN:
        t = pi[s]
        for z in nbrs[b2]:
            t *= msg(z, b2)[s]
        w[s] = t
    return w


def margin(p, w, c, b2):
    """Direct domination margin for the free neighbours of b2 (all three non-parent neighbours as children)."""
    lam = 1 - p
    pi = {s: (p if s[0] else 1 - p) * (p if s[1] else 1 - p) for s in ALL}
    kids = [(b2[0] + dx, b2[1] + dy) for dx, dy in NB if (b2[0] + dx, b2[1] + dy) != c]
    Pk = {b: [sum(pi[a] for a in ALL if eta(b, a, b2, k)) for k in kids] for b in OPEN}
    sw = sum(w.values())
    worst = None
    for Aset in W.UPSETS:
        piA = sum((lam if x[0] else 1 - lam) * (lam if x[1] else 1 - lam) * (lam if x[2] else 1 - lam) for x in Aset)
        tot = F(0)
        for b in OPEN:
            nuA = F(0)
            for x in Aset:
                t = F(1)
                for xi, pp in zip(x, Pk[b]):
                    t *= pp if xi else 1 - pp
                nuA += t
            tot += w[b] * nuA
        m = tot / sw - piA
        worst = m if worst is None else min(worst, m)
    return worst


def root_step(p):
    lam = 1 - p
    pi = {s: (p if s[0] else 1 - p) * (p if s[1] else 1 - p) for s in ALL}
    kids = NB
    Pk = {b: [sum(pi[a] for a in ALL if eta(b, a, (0, 0), k)) for k in kids] for b in OPEN}
    pts4 = list(product((0, 1), repeat=4))
    ups = []
    for mask in range(1, 2 ** 16 - 1):
        S = {pts4[i] for i in range(16) if mask >> i & 1}
        if all(y in S for x in S for y in pts4 if all(b >= a for a, b in zip(x, y))):
            ups.append(S)
    sw = sum(pi[b] for b in OPEN)
    worst = None
    for Aset in ups:
        piA = F(0)
        nuA = F(0)
        for x in Aset:
            t = F(1)
            for xi in x:
                t *= lam if xi else 1 - lam
            piA += t
            for b in OPEN:
                u = pi[b] / sw
                for xi, pp in zip(x, Pk[b]):
                    u *= pp if xi else 1 - pp
                nuA += u
        m = nuA - piA
        worst = m if worst is None else min(worst, m)
    return len(ups), worst, (1 - (1 - p) ** 2) - lam


def main():
    p = F(sys.argv[1])
    n = int(sys.argv[2])
    rng = random.Random(int(sys.argv[3]))
    nup, rw, r0 = root_step(p)
    print("root step at p = %s: %d increasing events of {0,1}^4, worst margin %.6e; root open %.6e above 1-p"
          % (p, nup, float(rw), float(r0)))
    k = 3
    cw = W.margin_at(p, k)[0][0]
    print("window.py depth %d worst-case margin at p: %.6e" % (k, float(cw)))
    worst = None
    for i in range(n):
        used, obs, b2 = random_tree(rng, 2)
        if len(used) > 9:
            continue
        w = posterior_b2(p, used, obs, b2)
        wb = posterior_bp(p, used, obs, b2)
        sw, sb = sum(w.values()), sum(wb.values())
        assert all(w[s] / sw == wb[s] / sb for s in OPEN), ("BP mismatch", used, obs)
        m = margin(p, w, (0, 0), b2)
        assert m >= cw - F(1, 10 ** 12), ("violation", m, cw, used, obs)
        worst = m if worst is None else min(worst, m)
    print("random explicit trees: worst direct margin %.6e >= cone margin %.6e: OK" % (float(worst), float(cw)))


if __name__ == "__main__":
    main()
