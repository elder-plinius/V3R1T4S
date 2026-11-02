#!/usr/bin/env python3
"""Independent exact checker (Python standard library only) for a bilinear matrix multiplication scheme.

Definition checked. Format <n1,n2,n3>: A is n1 x n2, B is n2 x n3, C = AB is n1 x n3. A scheme of rank r is r triples
(u_k, v_k, w_k) with
    m_k = (sum_{i,j} u_k[i*n2+j] A[i][j]) * (sum_{j,l} v_k[j*n3+l] B[j][l]),    C[i][l] = sum_k w_k[i*n3+l] m_k
for every A, B. Comparing the coefficient of A[i][j] B[j'][l] in C[i'][l'] with that of C = AB gives the Brent
equations, for all i, i' < n1, j, j' < n2, l, l' < n3:
    sum_k u_k[i*n2+j] v_k[j'*n3+l] w_k[i'*n3+l'] = [i = i'] [j = j'] [l = l'].
All (n1 n2)(n2 n3)(n1 n3) equations are checked, the zero ones included.

Arithmetic. Coefficients are read as exact rationals. Each factor matrix (U, V, W) is multiplied by its own least
common denominator (the lcm of the denominators of all its entries: Du, Dv, Dw), so all products are Python integers,
and every equation is checked as  sum_k U'[..] V'[..] W'[..] = Du Dv Dw [..]  exactly. Equations are processed one
A-index at a time, so memory stays small.

Also: three random exact evaluations C = AB (random integer A and B, exact rational arithmetic, every entry compared),
a count of terms with a zero factor (must be 0), and a report of pairs of terms that share two proportional factors
(such a pair could be merged, so its presence would mean r is not reduced; it does not make the scheme wrong).

Usage: check_brent_stdlib.py <dir with u.txt v.txt w.txt> [--trials 3] [--seed 1]
Last line: PASS or FAIL (exit status 0 or 1).
"""
import sys, os, re, random
from fractions import Fraction
from math import lcm


def die(msg):
    print("problem: " + msg)
    print("FAIL")
    sys.exit(1)


def read(path, which):
    fmt = rank = None
    rows = []
    with open(path, encoding="ascii") as fh:
        for ln, line in enumerate(fh, 1):
            s = line.strip()
            if s.startswith("#"):
                m = re.fullmatch(r"#\s*format\s+(\d+)\s+(\d+)\s+(\d+)", s)
                if m:
                    fmt = tuple(int(x) for x in m.groups())
                m = re.fullmatch(r"#\s*rank\s+(\d+)", s)
                if m:
                    rank = int(m.group(1))
                continue
            if fmt is None or rank is None:
                die("%s: data line %d before the format/rank headers" % (which, ln))
            size = {"u": fmt[0] * fmt[1], "v": fmt[1] * fmt[2], "w": fmt[0] * fmt[2]}[which]
            d = {}
            for tok in s.split():
                m = re.fullmatch(r"(\d+):(-?\d+)(?:/(\d+))?", tok)
                if not m:
                    die("%s line %d: bad token %r" % (which, ln, tok[:40]))
                idx = int(m.group(1))
                c = Fraction(int(m.group(2)), int(m.group(3)) if m.group(3) else 1)
                if idx >= size or idx in d:
                    die("%s line %d: index %d out of range or repeated" % (which, ln, idx))
                if c:
                    d[idx] = c
            rows.append(d)
    if fmt is None or rank is None:
        die("%s: missing header" % which)
    return fmt, rank, rows


def key(f):
    """Projective class of a factor: entries divided by the entry at the smallest index."""
    k0 = min(f)
    c0 = f[k0]
    return tuple(sorted((i, c / c0) for i, c in f.items()))


def main():
    args = sys.argv[1:]
    if not args:
        die("usage: check_brent_stdlib.py <dir> [--trials N] [--seed S]")
    base = args[0]
    trials = int(args[args.index("--trials") + 1]) if "--trials" in args else 3
    seed = int(args[args.index("--seed") + 1]) if "--seed" in args else 1
    (fu, ru, U), (fv, rv, V), (fw, rw, W) = (read(os.path.join(base, x + ".txt"), x) for x in "uvw")
    if not (fu == fv == fw and ru == rv == rw):
        die("files disagree on format or rank")
    n1, n2, n3 = fu
    r = ru
    if not (len(U) == len(V) == len(W) == r):
        die("data lines %d/%d/%d but rank header %d" % (len(U), len(V), len(W), r))
    zero = [k for k in range(r) if not (U[k] and V[k] and W[k])]
    print("format <%d,%d,%d> (A %dx%d, B %dx%d), %d terms, terms with a zero factor: %d"
          % (n1, n2, n3, n1, n2, n2, n3, r, len(zero)))
    if zero:
        die("term %d has a zero factor" % zero[0])
    nnz = [sum(len(F[k]) for k in range(r)) for F in (U, V, W)]
    lcds = []
    for F in (U, V, W):
        d = 1
        for f in F:
            for c in f.values():
                d = lcm(d, c.denominator)
        lcds.append(d)
    dens = sorted({c.denominator for F in (U, V, W) for f in F for c in f.values()} - {1})
    print("nonzeros u %d, v %d, w %d; denominators occurring %s" % (nnz[0], nnz[1], nnz[2], dens))
    print("least common denominator of each factor matrix: U %d, V %d, W %d" % tuple(lcds))

    # two-factor proportionality (mergeable pairs)
    merge = 0
    for a, b in ((0, 1), (0, 2), (1, 2)):
        seen = {}
        F = (U, V, W)
        for k in range(r):
            kk = (key(F[a][k]), key(F[b][k]))
            if kk in seen:
                merge += 1
            else:
                seen[kk] = k
    print("pairs of terms sharing two proportional factors (mergeable): %d" % merge)

    # integer factors
    Du, Dv, Dw = lcds
    Ui = [{i: int(c * Du) for i, c in f.items()} for f in U]
    Vi = [{i: int(c * Dv) for i, c in f.items()} for f in V]
    Wi = [{i: int(c * Dw) for i, c in f.items()} for f in W]
    D = Du * Dv * Dw
    szv, szw = n2 * n3, n1 * n3
    # outer product v_k x w_k, flattened key b*szw + c
    VW = []
    for k in range(r):
        VW.append([(b * szw + c, x * y) for b, x in Vi[k].items() for c, y in Wi[k].items()])
    by_a = {}
    for k in range(r):
        for a, x in Ui[k].items():
            by_a.setdefault(a, []).append((k, x))
    wrong = 0
    checked_nonzero_slots = 0
    for a in range(n1 * n2):
        i, j = divmod(a, n2)
        acc = {}
        for k, x in by_a.get(a, ()):
            for bc, y in VW[k]:
                acc[bc] = acc.get(bc, 0) + x * y
        want = {(j * n3 + l) * szw + (i * n3 + l): D for l in range(n3)}
        for bc, val in acc.items():
            if val != want.get(bc, 0):
                wrong += 1
        for bc in want:
            if bc not in acc:
                wrong += 1
        checked_nonzero_slots += len(acc)
    total = (n1 * n2) * (n2 * n3) * (n1 * n3)
    print("Brent equations: %d checked (all index triples), %d wrong; scaling Du*Dv*Dw = %d" % (total, wrong, D))
    if wrong:
        die("%d Brent equations fail" % wrong)

    rnd = random.Random(seed)
    for t in range(trials):
        A = [rnd.randint(-1000, 1000) for _ in range(n1 * n2)]
        B = [rnd.randint(-1000, 1000) for _ in range(n2 * n3)]
        C = [Fraction(0)] * (n1 * n3)
        for k in range(r):
            m = sum(c * A[i] for i, c in U[k].items()) * sum(c * B[i] for i, c in V[k].items())
            if m:
                for i, c in W[k].items():
                    C[i] += c * m
        AB = [sum(A[i * n2 + j] * B[j * n3 + l] for j in range(n2)) for i in range(n1) for l in range(n3)]
        bad = sum(1 for x, y in zip(C, AB) if x != y)
        print("random exact evaluation %d (seed %d): %d of %d entries of C differ from AB" % (t + 1, seed, bad, n1 * n3))
        if bad:
            die("random evaluation %d fails" % (t + 1))
    print("rank-%d scheme for <%d,%d,%d> over Q: all Brent equations hold exactly" % (r, n1, n2, n3))
    print("PASS")


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:
        print("problem: %s: %s" % (type(e).__name__, str(e)[:200]))
        print("FAIL")
        sys.exit(1)
