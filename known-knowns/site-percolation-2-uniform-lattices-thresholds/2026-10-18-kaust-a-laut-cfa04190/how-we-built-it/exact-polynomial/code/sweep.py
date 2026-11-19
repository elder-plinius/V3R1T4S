"""Turn a periodic lattice into a frontier 'sweep program' for one period of a semi-infinite cylinder.

The cylinder has circumference n cells along a1 and is infinite along a2. Vertices are (c, t, v): cell c in
0..n-1 along a1, layer t along a2, cell vertex v. The sweep adds vertices one at a time in a fixed periodic order;
the frontier is the list of added vertices that still have unadded neighbours, kept in insertion order.

Each step of the program (one added vertex x) is written as one line:
    nb <k> s_1 w_1 ... s_k w_k  self <m> w_1 ... w_m  rem <r> i_1 ... i_r
  s_j: frontier slot (index before x is appended) of an earlier neighbour, w_j: winding so that
       lift(x) = lift(slot) + w_j, where a lift counts crossings of the seam between cell n-1 and cell 0;
  self: windings of edges from x to itself (only for very small n);
  rem: slots removed after x is appended at the end (indices into the frontier including x), ascending.
The header gives n, the number of steps in a period and the frontier size at period boundaries.
"""
import sys
import os
import itertools

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "evaluator-first", "code"))
import lattices  # noqa: E402


def adjacency(lat):
    """Directed neighbour list per cell vertex: (j, d1, d2) for every edge, both directions."""
    adj = [[] for _ in lat["verts"]]
    for (i, j, d1, d2) in lat["edges"]:
        adj[i].append((j, d1, d2))
        adj[j].append((i, -d1, -d2))
    return adj


def order_key_factory(lat, mode):
    # sub-layer of each cell vertex: rank of its coordinate along the a2 direction's normal
    import numpy as np
    a1 = np.array(lat["a1"])
    a2 = np.array(lat["a2"])
    nrm = np.array([-a1[1], a1[0]])
    nrm = nrm / np.linalg.norm(nrm)
    if nrm @ a2 < 0:
        nrm = -nrm
    h = [float(np.array(v) @ nrm) for v in lat["verts"]]
    if mode == "tcv":
        return lambda t, c, v: (t, c, v)
    if mode == "tvc":
        return lambda t, c, v: (t, h[v], v, c)
    raise ValueError(mode)


def build_program(lat, n, mode=None, periods=6, verbose=False):
    adj = adjacency(lat)
    nv = len(lat["verts"])
    modes = [mode] if mode else ["tvc", "tcv"]
    best = None
    for md in modes:
        key = order_key_factory(lat, md)
        verts = [(t, c, v) for t in range(periods) for c in range(n) for v in range(nv)]
        verts.sort(key=lambda x: key(*x))
        pos = {x: k for k, x in enumerate(verts)}

        def nbrs(x):
            t, c, v = x
            out = []
            for (j, d1, d2) in adj[v]:
                cu = c + d1
                w = cu // n          # crossings of the seam going from x to the neighbour
                out.append(((t + d2, cu % n, j), w))
            return out
        # check: within a period, each vertex's earlier neighbours are at most one layer back
        frontier = []
        steps = []
        maxf = 0
        ok = True
        bsizes = []
        for k, x in enumerate(verts):
            t, c, v = x
            nb = []
            selfw = []
            for (y, w) in nbrs(x):
                if y == x:
                    if w != 0:
                        selfw.append(w)
                    continue
                if y not in pos:
                    continue  # outside the simulated window (t < 0 or t >= periods)
                if pos[y] < k:
                    if y not in frontier:
                        ok = False  # an earlier neighbour was already dropped: order is invalid
                        break
                    # lift(y) = lift(x) + w  =>  lift(x) = lift(y) - w
                    nb.append((frontier.index(y), -w))
            if not ok:
                break
            # self loops are listed once per direction in adj; keep each undirected loop once
            selfw = sorted(selfw)
            selfw = selfw[: len(selfw) // 2] if selfw else []
            frontier.append(x)
            rem = []
            for idx, y in enumerate(frontier):
                done = True
                for (z, w) in nbrs(y):
                    if z == y:
                        continue
                    if z in pos and pos[z] > k:
                        done = False
                        break
                    if z not in pos and z[0] >= periods:
                        done = False
                        break
                if done:
                    rem.append(idx)
            steps.append((x, nb, selfw, rem, len(frontier)))
            frontier = [y for idx, y in enumerate(frontier) if idx not in rem]
            maxf = max(maxf, len(frontier) + 1)
            if c == n - 1 and v == max(range(nv), key=lambda vv: key(t, n - 1, vv)):
                pass
        if not ok:
            continue
        cand = (maxf, md, steps)
        if best is None or cand[0] < best[0]:
            best = cand
    if best is None:
        raise RuntimeError("no valid sweep order")
    maxf, md, steps = best
    # pick the steady-state period: steps of layer t = periods // 2
    tsel = periods // 2
    P = n * nv
    idx = [k for k, s in enumerate(steps) if s[0][0] == tsel]
    # the period starts where the first vertex of layer tsel is added; verify that the next period repeats it
    k0 = idx[0]
    per = steps[k0:k0 + P]
    nxt = steps[k0 + P:k0 + 2 * P]
    assert len(per) == P and len(nxt) == P
    for a, b in zip(per, nxt):
        assert a[1:] == b[1:], "sweep is not periodic"
        assert a[0][1:] == b[0][1:]
    # frontier size at the period boundary = size before the first step of the period
    bsize = per[0][4] - 1  # frontier length including x minus x
    if verbose:
        print("order %s, max frontier %d, boundary %d" % (md, maxf, bsize), file=sys.stderr)
    return {"n": n, "P": P, "B": bsize, "mode": md, "steps": [(s[1], s[2], s[3]) for s in per],
            "maxf": maxf, "labels": [s[0] for s in per]}


def write_program(prog, path):
    with open(path, "w", newline="\n") as f:
        f.write("n %d P %d B %d\n" % (prog["n"], prog["P"], prog["B"]))
        for (nb, selfw, rem) in prog["steps"]:
            parts = ["nb", str(len(nb))]
            for (s, w) in nb:
                parts += [str(s), str(w)]
            parts += ["self", str(len(selfw))] + [str(w) for w in selfw]
            parts += ["rem", str(len(rem))] + [str(i) for i in rem]
            f.write(" ".join(parts) + "\n")


LATTICES = dict(lattices.ARCHIMEDEAN)
LATTICES.update({"#" + k: v for k, v in lattices.TWO_UNIFORM.items()})


if __name__ == "__main__":
    name, n, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    lat = LATTICES[name]()
    prog = build_program(lat, n, verbose=True)
    write_program(prog, out)
