"""Fast exact check of an r-colouring file (circulant or matrix, mcheck.py format), two methods per colour:
 (A) alpha.c (C bitset B&B) on the complement of colour c: an independent k-set there = K_k in colour c.
     circulant files: 'sym' mode (alpha.c verifies in-code that the expanded matrix is circulant, then fixes
     vertex 0); matrix files: 'nosym'.
 (B) SAT (pysat CaDiCaL 1.9.5, a different solver build from mcheck.py's 1.5.3): K_k in colour c.
     circulant: vertex-transitive, so K_k exists iff a K_{k-1} exists in the colour-c neighbourhood of 0;
     the SAT instance is on that neighbourhood (expanded from the matrix). matrix: full graph.
usage: check_fast.py <file> k_1 ... k_r [alpha_cap_seconds]
Exit 0 iff for every colour both methods say "no K_{k_c}"."""
import sys, os, subprocess, hashlib, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)  # package copy: mcheck.py sits next to this file
from mcheck import load, validate  # parsing/validation only; the clique tests below are independent


def sat_clique(A, verts, k):
    from pysat.solvers import Cadical195
    from pysat.card import CardEnc, EncType
    n = len(verts)
    if k <= 0:
        return True
    if k > n:
        return False
    idx = {v: i + 1 for i, v in enumerate(verts)}
    cl = [[-idx[verts[i]], -idx[verts[j]]] for i in range(n) for j in range(i + 1, n) if not A[verts[i]][verts[j]]]
    card = CardEnc.atleast(lits=list(range(1, n + 1)), bound=k, top_id=n, encoding=EncType.seqcounter)
    with Cadical195(bootstrap_with=cl + card.clauses) as s:
        return s.solve()


def main():
    path = sys.argv[1]
    lines = [l.strip() for l in open(path) if l.strip() and not l.lstrip().startswith('#')]
    kind = lines[0].split()[0]
    C, r = load(path)
    ks = [int(x) for x in sys.argv[2:2 + r]]
    cap = sys.argv[2 + r] if len(sys.argv) > 2 + r else '3000'
    validate(C, r)
    N = len(C)
    canon = "\n".join("".join(map(str, row)) for row in C).encode()
    print('file', path, 'kind', kind, 'N', N, 'colours', r, 'matrix sha256', hashlib.sha256(canon).hexdigest(), flush=True)
    ok = True
    tmp = os.path.join(HERE, '..', 'work')
    os.makedirs(tmp, exist_ok=True)
    for c in range(1, r + 1):
        k = ks[c - 1]
        adj = os.path.join(tmp, 'chk_%s_c%d.adj' % (os.path.basename(path), c))
        with open(adj, 'w') as f:
            for i in range(N):
                f.write(''.join('0' if i == j or C[i][j] == c else '1' for j in range(N)) + '\n')
        t0 = time.time()
        res = subprocess.run([os.path.join(HERE, 'alpha'), adj, str(k), 'sym' if kind == 'circulant' else 'nosym', '-t', cap],
                             capture_output=True, text=True).stdout
        ra = [l for l in res.splitlines() if l.startswith('RESULT')][0]
        A = [[1 if (i != j and C[i][j] == c) else 0 for j in range(N)] for i in range(N)]
        deg = sorted(set(sum(row) for row in A))
        t1 = time.time()
        if kind == 'circulant':
            nb0 = [j for j in range(N) if A[0][j]]
            rb = sat_clique(A, nb0, k - 1)
        else:
            rb = sat_clique(A, list(range(N)), k)
        t2 = time.time()
        a_found = ra.startswith('RESULT FOUND')
        a_none = ra.startswith('RESULT NONE')
        print('colour %d: edges %d degrees %s | K_%d alpha.c: %s (%.1fs) | SAT: %s (%.1fs)' % (
            c, sum(map(sum, A)) // 2, deg if len(deg) <= 6 else (deg[0], '..', deg[-1]), k, ra, t1 - t0,
            'K found' if rb else 'UNSAT (no K)', t2 - t1), flush=True)
        if not (a_none and not rb):
            ok = False
            if a_found != rb:
                print('METHODS DISAGREE or UNDECIDED on colour', c)
    print('VERDICT:', 'valid (%s)-colouring of K_%d' % (','.join(map(str, ks)), N) if ok else 'NOT verified')
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
