#!/usr/bin/env python3
"""constructor lens: punctured extended one-point Hermitian codes E_m with the deleted
coordinate set taken up to the automorphisms of the curve that fix P_inf.

E_m (hermitian.py): rows = monomials x^i y^j (j <= 2, 3i + 4j <= m) at the 27 affine points of y^3 + y = x^4 over
GF(9), coordinate 27 = P_inf (1 for the top monomial). Puncturing at a set P keeps dimension kappa = m - 2 while
|P| < d(E_m) = 28 - m and gives d >= 28 - m - |P|.

Automorphisms fixing P_inf: s(x, y) = (a x + b, a^4 y + a b^3 x + c), a != 0, c^3 + c = b^4 (order 216). They map
L(m P_inf) to itself, so they act on E_m as monomial maps (a permutation of the 27 affine coordinates with column
scalings; the P_inf coordinate gets a scalar). The maximum Hermitian hull over column sign patterns (scalings by
norm classes) is invariant under monomial maps, so one deletion set per orbit suffices.

Shortening (--shorten): the subcode of E_m vanishing on the set, with those coordinates removed (hermitian.shorten):
[28 - r, m - 2 - r, >= 28 - m] while r < kappa.
Usage: punct.py m r outdir [--with-inf] [--shorten]
  writes outdir/E{m}_p{r}_o{j}.code (epsbig input "K n" + K x n matrix) for one representative of every orbit of
  r-subsets of the 27 affine coordinates (with --with-inf: r-subsets of all 28 coordinates that contain P_inf), and
  prints the representatives and orbit sizes."""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gf9lib import ADD, MUL
from hermitian import pts, code, pw

def group():
    idx = {p: i for i, p in enumerate(pts)}
    perms = set()
    for a in range(1, 9):
        a4 = pw(a, 4)
        for b in range(9):
            for c in range(9):
                if ADD[pw(c, 3)][c] != pw(b, 4):
                    continue
                perm = []
                for x, y in pts:
                    X = ADD[MUL[a][x]][b]
                    Y = ADD[ADD[MUL[a4][y]][MUL[MUL[a][pw(b, 3)]][x]]][c]
                    perm.append(idx[(X, Y)])   # KeyError if not an automorphism
                perms.add(tuple(perm))
    return sorted(perms)

def orbit_reps(r, perms, with_inf):
    seen = set(); reps = []
    if with_inf:
        base = itertools.combinations(range(27), r - 1)
    else:
        base = itertools.combinations(range(27), r)
    for S in base:
        if S in seen:
            continue
        orb = {tuple(sorted(p[i] for i in S)) for p in perms}
        seen |= orb
        reps.append((S, len(orb)))
    return reps

if __name__ == "__main__":
    m, r, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    with_inf = "--with-inf" in sys.argv
    shorten = "--shorten" in sys.argv
    from hermitian import shorten as _short
    os.makedirs(out, exist_ok=True)
    perms = group()
    print("automorphisms fixing P_inf found: %d" % len(perms))
    G = code(m); K = len(G)
    reps = orbit_reps(r, perms, with_inf)
    tot = 0
    for j, (S, sz) in enumerate(reps):
        dele = list(S) + ([27] if with_inf else [])
        keep = [t for t in range(28) if t not in dele]
        Gp = _short(G, dele) if shorten else [[row[t] for t in keep] for row in G]
        fn = os.path.join(out, "E%d_%s%d%s_o%d.code" % (m, "s" if shorten else "p", r, "i" if with_inf else "", j))
        with open(fn, "w") as fh:
            fh.write("%d %d\n" % (len(Gp), len(keep)))
            for row in Gp:
                fh.write(" ".join(map(str, row)) + "\n")
        tot += sz
        print("orbit %d: deleted %s size %d -> %s" % (j, dele, sz, os.path.basename(fn)))
    print("m=%d kappa=%d r=%d with_inf=%s orbits=%d total sets=%d" % (m, K, r, with_inf, len(reps), tot))
