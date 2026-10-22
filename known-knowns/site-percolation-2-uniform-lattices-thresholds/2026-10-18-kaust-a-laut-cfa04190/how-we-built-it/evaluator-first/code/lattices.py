"""Periodic planar lattices for percolation, built from geometry and checked from the definition.

A lattice is a dict:
  name, a1, a2 (Cartesian lattice vectors), verts (Cartesian positions of the vertices of one cell),
  edges: list of (i, j, d1, d2): vertex i of cell (c1, c2) is joined to vertex j of cell (c1+d1, c2+d2).
Edges are found as the vertex pairs at unit distance (all tilings here are edge-to-edge tilings by regular
polygons of unit edge), and check_tiling() then verifies that the result really is such a tiling: every face of
the embedding is a regular polygon with unit edges, Euler's relation V - E + F = 0 holds per cell, no two edges
cross, and the vertex configurations, their fractions, zbar and the number of vertex orbits under the
tiling's isometries are reported.
"""
import math
import itertools
from fractions import Fraction
import numpy as np

TOL = 1e-9


def _dedupe(points, a1, a2, tol=1e-7):
    """Reduce points modulo the lattice and drop duplicates."""
    A = np.array([a1, a2]).T
    Ainv = np.linalg.inv(A)
    out = []
    for p in points:
        f = Ainv @ np.asarray(p, float)
        f = f - np.floor(f + 1e-9)
        q = A @ f
        dup = False
        for r in out:
            d = Ainv @ (q - r)
            d = d - np.round(d)
            if np.linalg.norm(A @ d) < tol:
                dup = True
                break
        if not dup:
            out.append(q)
    return out


def make_lattice(name, a1, a2, points):
    a1 = np.asarray(a1, float)
    a2 = np.asarray(a2, float)
    verts = _dedupe(points, a1, a2)
    edges = []
    R = 3
    for i, p in enumerate(verts):
        for j, q in enumerate(verts):
            for d1 in range(-R, R + 1):
                for d2 in range(-R, R + 1):
                    r = q + d1 * a1 + d2 * a2
                    if abs(np.linalg.norm(r - p) - 1.0) < 1e-7:
                        # keep each undirected edge once
                        key = (i, j, d1, d2)
                        rev = (j, i, -d1, -d2)
                        if rev not in edges and key not in edges:
                            edges.append(key)
    return {"name": name, "a1": a1.tolist(), "a2": a2.tolist(),
            "verts": [v.tolist() for v in verts], "edges": edges}


# ---------------------------------------------------------------- builders

def rows(pattern):
    """Stack of rows: 'S' = row of unit squares, 'T' = row of alternating triangles.
    Lines of vertices at unit spacing; a T row shifts the next line by 1/2."""
    pts = []
    y = 0.0
    s = 0.0
    for ch in pattern:
        pts.append((s, y))
        if ch == 'S':
            y += 1.0
        elif ch == 'T':
            y += math.sqrt(3) / 2
            s = (s + 0.5) % 1.0
        else:
            raise ValueError(ch)
    a1 = (1.0, 0.0)
    a2 = (s, y)
    return make_lattice("rows-" + pattern, a1, a2, pts)


def kagome():
    r3 = math.sqrt(3)
    return make_lattice("kagome", (2, 0), (1, r3), [(0, 0), (1, 0), (0.5, r3 / 2)])


def honeycomb():
    r3 = math.sqrt(3)
    return make_lattice("honeycomb", (r3, 0), (r3 / 2, 1.5), [(0, 0), (0, 1)])


def polygon_vertices(center, k, phase):
    """Vertices of a regular k-gon with unit edge, first vertex at angle phase."""
    R = 1.0 / (2 * math.sin(math.pi / k))
    cx, cy = center
    return [(cx + R * math.cos(phase + 2 * math.pi * t / k), cy + R * math.sin(phase + 2 * math.pi * t / k))
            for t in range(k)]


def three_twelve():
    """(3,12^2): unit-edge dodecagons centred on a triangular lattice of spacing 2 * apothem."""
    ap = 0.5 / math.tan(math.pi / 12)
    D = 2 * ap
    a1 = (D, 0.0)
    a2 = (D / 2, D * math.sqrt(3) / 2)
    pts = polygon_vertices((0, 0), 12, math.radians(15))
    return make_lattice("(3,12^2)", a1, a2, pts)


def square():
    return rows("S") | {"name": "square"}


def triangular():
    return rows("T") | {"name": "triangular"}


# ---------------------------------------------------------------- checker

def neighbours(lat):
    """For each cell vertex: list of (j, d1, d2, vector) sorted by angle (counterclockwise)."""
    a1 = np.array(lat["a1"])
    a2 = np.array(lat["a2"])
    V = [np.array(v) for v in lat["verts"]]
    nb = [[] for _ in V]
    for (i, j, d1, d2) in lat["edges"]:
        vec = V[j] + d1 * a1 + d2 * a2 - V[i]
        nb[i].append((j, d1, d2, vec))
        nb[j].append((i, -d1, -d2, -vec))
    for lst in nb:
        lst.sort(key=lambda t: math.atan2(t[3][1], t[3][0]))
    return nb


def faces(lat):
    """Trace the faces of the periodic embedding. Returns a list of faces, each a list of
    (vertex, cell offset) corners, one representative per translation class."""
    nb = neighbours(lat)
    # half-edge (i, k) = k-th neighbour of i. next half-edge around a face (face on the left):
    # arrive at j from i, take the neighbour of j that comes just before (clockwise of) the reverse edge.
    seen = set()
    out = []
    for i in range(len(nb)):
        for k in range(len(nb[i])):
            if (i, k) in seen:
                continue
            face = []
            ci, ck = i, k
            off = np.zeros(2, int)
            while True:
                if (ci, ck) in seen:
                    break
                seen.add((ci, ck))
                face.append((ci, tuple(off)))
                j, d1, d2, vec = nb[ci][ck]
                off = off + np.array([d1, d2])
                # find reverse edge index at j
                back = None
                for kk, (jj, e1, e2, w) in enumerate(nb[j]):
                    if jj == ci and e1 == -d1 and e2 == -d2:
                        back = kk
                        break
                # next edge: clockwise from the reverse edge = previous in CCW order
                nk = (back - 1) % len(nb[j])
                ci, ck = j, nk
            out.append(face)
    return out


def check_tiling(lat, verbose=True):
    a1 = np.array(lat["a1"])
    a2 = np.array(lat["a2"])
    V = [np.array(v) for v in lat["verts"]]
    nV = len(V)
    nE = len(lat["edges"])
    problems = []
    for (i, j, d1, d2) in lat["edges"]:
        L = np.linalg.norm(V[j] + d1 * a1 + d2 * a2 - V[i])
        if abs(L - 1) > 1e-7:
            problems.append("edge length %.9f" % L)
    F = faces(lat)
    sizes = []
    area_total = 0.0
    for f in F:
        pts = [V[v] + o[0] * a1 + o[1] * a2 for (v, o) in f]
        k = len(pts)
        sizes.append(k)
        area = 0.5 * sum(pts[t][0] * pts[(t + 1) % k][1] - pts[(t + 1) % k][0] * pts[t][1] for t in range(k))
        area_total += area
        # regular polygon test: unit edges and equal turning angles
        want = math.pi * (k - 2) / k
        for t in range(k):
            p0, p1, p2 = pts[t - 1], pts[t], pts[(t + 1) % k]
            u = p0 - p1
            w = p2 - p1
            ang = math.atan2(u[0] * w[1] - u[1] * w[0], u @ w)
            ang = abs(ang)
            if abs(ang - want) > 1e-6:
                problems.append("face of %d sides has angle %.6f, want %.6f" % (k, ang, want))
                break
        if area <= 0:
            problems.append("face with non-positive area %.6f (orientation)" % area)
    cell_area = abs(a1[0] * a2[1] - a1[1] * a2[0])
    if abs(area_total - cell_area) > 1e-6:
        problems.append("face areas sum to %.9f, cell area %.9f" % (area_total, cell_area))
    if nV - nE + len(F) != 0:
        problems.append("Euler V-E+F = %d" % (nV - nE + len(F)))
    # vertex configurations: label every half-edge with the size of the face on its left
    nb = neighbours(lat)
    seen = {}
    for i in range(nV):
        for k in range(len(nb[i])):
            if (i, k) in seen:
                continue
            path = []
            ci, ck = i, k
            while (ci, ck) not in seen:
                seen[(ci, ck)] = None
                path.append((ci, ck))
                j, d1, d2, vec = nb[ci][ck]
                back = [kk for kk, (jj, e1, e2, w) in enumerate(nb[j]) if jj == ci and e1 == -d1 and e2 == -d2][0]
                ci, ck = j, (back - 1) % len(nb[j])
            for he in path:
                seen[he] = len(path)
    confs = []
    for i in range(nV):
        if len(nb[i]) < 3:
            problems.append("vertex %d has degree %d" % (i, len(nb[i])))
        # the face to the left of half-edge (i,k) lies between edge k and the previous edge in CCW order;
        # going once around the vertex visits each face once, in angular order
        seq = [seen[(i, k)] for k in range(len(nb[i]))]
        confs.append(canon(seq))
    counts = {}
    for c in confs:
        counts[c] = counts.get(c, 0) + 1
    fr = {c: Fraction(n, nV) for c, n in counts.items()}
    zbar = Fraction(2 * nE, nV)
    # angle sum at each vertex
    for i, c in enumerate(confs):
        s = sum(math.pi * (k - 2) / k for k in c)
        if abs(s - 2 * math.pi) > 1e-9:
            problems.append("vertex %d angle sum %.9f" % (i, s))
    crossings = edge_crossings(lat)
    if crossings:
        problems.append("%d edge crossings" % crossings)
    orbits = vertex_orbits(lat)
    res = {"name": lat["name"], "V": nV, "E": nE, "F": len(F), "face_sizes": sorted(sizes),
           "configs": confs, "fractions": fr, "zbar": zbar, "orbits": orbits, "problems": problems}
    if verbose:
        print_check(res)
    return res


def canon(seq):
    """Canonical form of a cyclic face-size sequence up to rotation and reflection."""
    n = len(seq)
    if n == 0:
        return ()
    cands = []
    for s in (list(seq), list(reversed(seq))):
        for r in range(n):
            cands.append(tuple(s[r:] + s[:r]))
    return min(cands)


def conf_str(c):
    # compress runs: (3,3,3,4,4) -> 3^3.4^2
    out = []
    i = 0
    while i < len(c):
        j = i
        while j < len(c) and c[j] == c[i]:
            j += 1
        out.append(str(c[i]) + ("^%d" % (j - i) if j - i > 1 else ""))
        i = j
    return ".".join(out)


def print_check(res):
    print("lattice %s: V=%d E=%d F=%d per cell; zbar=%s; faces %s" % (
        res["name"], res["V"], res["E"], res["F"], res["zbar"], res["face_sizes"]))
    for c, f in sorted(res["fractions"].items(), key=lambda t: -t[1]):
        print("   (%s) %s" % (f, conf_str(c)))
    print("   vertex orbits under isometries: %d" % res["orbits"])
    print("   problems: %s" % (res["problems"] or "none"))


def edge_crossings(lat):
    a1 = np.array(lat["a1"])
    a2 = np.array(lat["a2"])
    V = [np.array(v) for v in lat["verts"]]
    segs = []
    for (i, j, d1, d2) in lat["edges"]:
        p = V[i]
        q = V[j] + d1 * a1 + d2 * a2
        for t1 in range(-1, 2):
            for t2 in range(-1, 2):
                sh = t1 * a1 + t2 * a2
                segs.append((p + sh, q + sh))
    base = segs[4::9]  # t1 = t2 = 0 copies
    n = 0
    for (p, q) in base:
        for (r, s) in segs:
            if seg_cross(p, q, r, s):
                n += 1
    return n


def seg_cross(p, q, r, s):
    def orient(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    # proper crossings only (shared endpoints are not crossings)
    for a in (p, q):
        for b in (r, s):
            if np.linalg.norm(a - b) < 1e-7:
                return False
    o1, o2, o3, o4 = orient(p, q, r), orient(p, q, s), orient(r, s, p), orient(r, s, q)
    return (o1 * o2 < -1e-12) and (o3 * o4 < -1e-12)


def vertex_orbits(lat):
    """Number of orbits of the cell's vertices under the isometries of the tiling (translations included).
    Candidate isometries: x -> M x + t with M a rotation by a multiple of 30 degrees or a reflection, sending a cell
    vertex src to a cell vertex dst; kept if they map a 5 x 5-cell patch of vertices into the vertex set. Since edges
    are exactly the unit-distance vertex pairs, an isometry that preserves the vertex set preserves the edges."""
    a1 = np.array(lat["a1"])
    a2 = np.array(lat["a2"])
    V = [np.array(v) for v in lat["verts"]]
    A = np.array([a1, a2]).T
    Ainv = np.linalg.inv(A)
    Q = 10 ** 6

    def key(p):
        f = Ainv @ p
        f = f - np.floor(f)
        return (int(round(f[0] * Q)) % Q, int(round(f[1] * Q)) % Q)
    index = {}
    for k, v in enumerate(V):
        index[key(v)] = k

    def cell_index(p):
        return index.get(key(p))

    mats = []
    for t in range(12):
        c, s = math.cos(t * math.pi / 6), math.sin(t * math.pi / 6)
        mats.append(np.array([[c, -s], [s, c]]))
        mats.append(np.array([[c, s], [s, -c]]))
    patch = [v + t1 * a1 + t2 * a2 for v in V for t1 in range(-2, 3) for t2 in range(-2, 3)]
    parent = list(range(len(V)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for M in mats:
        for src in range(len(V)):
            for dst in range(len(V)):
                t = V[dst] - M @ V[src]
                if not all(cell_index(M @ p + t) is not None for p in patch):
                    continue
                for k in range(len(V)):
                    img = cell_index(M @ V[k] + t)
                    ra, rb = find(k), find(img)
                    if ra != rb:
                        parent[ra] = rb
    return len({find(k) for k in range(len(V))})


ARCHIMEDEAN = {"square": square, "triangular": triangular, "kagome": kagome, "honeycomb": honeycomb,
               "(3,12^2)": three_twelve,
               # elongated triangular (3^3,4^2) = alternating rows of squares and triangles; calibration lattice
               # for the row geometry (run 2026-10-16-1714)
               "(3^3,4^2)": lambda: rows("ST") | {"name": "(3^3,4^2) rows ST"}}

# Wikipedia "2-uniform lattices" rows built so far, keyed by the table's '#'.
TWO_UNIFORM = {
    "20": lambda: rows("STTT") | {"name": "#20 rows STTT"},
    "21": lambda: rows("STT") | {"name": "#21 rows STT"},
    "22": lambda: rows("SST") | {"name": "#22 rows SST"},
    "23": lambda: rows("SSST") | {"name": "#23 rows SSST"},
    # triangular lattice with hexagonal holes, reduced basis, a1 = shortest period vector (oldest-entry lens,
    # run 2026-10-16-1714, PREREG.v3 addition E)
    "15": lambda: _tri_holes("15"),
}


def _tri_holes(num):
    import os
    import sys
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "oldest-entry", "code")
    if d not in sys.path:
        sys.path.insert(0, d)
    import new_lattices
    return new_lattices.build(num)


def get(name):
    if name in ARCHIMEDEAN:
        return ARCHIMEDEAN[name]()
    return TWO_UNIFORM[name.lstrip("#")]()


def write_latfile(lat, path):
    """Plain format read by nzwrap.c: 'K <verts> E <edges>' then one 'i j d1 d2' line per edge."""
    with open(path, "w", newline="\n") as f:
        f.write("K %d E %d\n" % (len(lat["verts"]), len(lat["edges"])))
        for (i, j, d1, d2) in lat["edges"]:
            f.write("%d %d %d %d\n" % (i, j, d1, d2))


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "export":
        write_latfile(get(sys.argv[2]), sys.argv[3])
    else:
        for k, f in list(ARCHIMEDEAN.items()) + list(TWO_UNIFORM.items()):
            check_tiling(f())
