#!/usr/bin/env python3
"""Exact checker for a bilinear matrix multiplication scheme stored as three factor files (Python standard library).

Definition. A bilinear scheme of rank r for <n1,n2,n3> (A is n1 x n2, B is n2 x n3, C = AB is n1 x n3) is a list of
r products m_k = (sum_{i,j} u_k[i*n2+j] A[i][j]) * (sum_{j,l} v_k[j*n3+l] B[j][l]) with C[i][l] = sum_k w_k[i*n3+l] m_k
for all A, B over the ring (here Q). Equivalently (Brent equations), for all i, i' < n1, j, j' < n2, l, l' < n3:
    sum_k u_k[i*n2+j] * v_k[j'*n3+l] * w_k[i'*n3+l'] = 1 if (i, j, l) == (i', j', l') else 0.
Files: <dir>/u.txt, v.txt, w.txt; header lines '# format n1 n2 n3' and '# rank r'; then exactly r data lines, line k
listing the nonzero entries of factor k as 'index:coefficient' (integer or p/q). Every coefficient is cleared to an
integer with one common denominator D and every term is expanded exactly; all n1 n2 n2 n3 n1 n3 equations are checked.
Also required: every term has three nonzero factors (so the number of multiplications is exactly r).
Usage: check_scheme.py <dir>        Last line: PASS or FAIL. Exit status 0 or 1.
"""
import sys, os, re
from fractions import Fraction
from math import lcm

def fail(msg):
    print("problem: " + msg)
    print("FAIL")
    sys.exit(1)

def read_factor(path, size_of):
    fmt = rank = None
    rows = []
    with open(path, encoding="ascii") as fh:
        for ln, line in enumerate(fh, 1):
            line = line.strip()
            if line.startswith("#"):
                m = re.match(r"#\s*format\s+(\d+)\s+(\d+)\s+(\d+)\s*$", line)
                if m:
                    fmt = tuple(int(x) for x in m.groups())
                m = re.match(r"#\s*rank\s+(\d+)\s*$", line)
                if m:
                    rank = int(m.group(1))
                continue
            if fmt is None or rank is None:
                fail("%s: data before the format and rank headers" % os.path.basename(path))
            size = size_of(fmt)
            d = {}
            for tok in line.split():
                m = re.fullmatch(r"(\d+):(-?\d+(?:/\d+)?)", tok)
                if not m:
                    fail("%s line %d: bad token %r" % (os.path.basename(path), ln, tok[:30]))
                idx, c = int(m.group(1)), Fraction(m.group(2))
                if idx >= size:
                    fail("%s line %d: index %d out of range (size %d)" % (os.path.basename(path), ln, idx, size))
                if idx in d:
                    fail("%s line %d: index %d repeated" % (os.path.basename(path), ln, idx))
                if c != 0:
                    d[idx] = c
            rows.append(d)
    if fmt is None or rank is None:
        fail("%s: missing '# format' or '# rank' header" % os.path.basename(path))
    return fmt, rank, rows

def main():
    if len(sys.argv) != 2:
        fail("usage: check_scheme.py <dir with u.txt v.txt w.txt>")
    base = sys.argv[1]
    sizes = {"u": lambda f: f[0] * f[1], "v": lambda f: f[1] * f[2], "w": lambda f: f[0] * f[2]}
    got = {ax: read_factor(os.path.join(base, ax + ".txt"), sizes[ax]) for ax in "uvw"}
    fmts = {got[ax][0] for ax in "uvw"}
    ranks = {got[ax][1] for ax in "uvw"}
    if len(fmts) != 1 or len(ranks) != 1:
        fail("the three files disagree on format or rank: %s %s" % (sorted(fmts), sorted(ranks)))
    (n1, n2, n3), r = fmts.pop(), ranks.pop()
    U, V, W = got["u"][2], got["v"][2], got["w"][2]
    if not (len(U) == len(V) == len(W) == r):
        fail("data lines u %d, v %d, w %d, but the header says rank %d" % (len(U), len(V), len(W), r))
    zero = [k for k in range(r) if not (U[k] and V[k] and W[k])]
    if zero:
        fail("%d term(s) have a zero factor (first: term %d), so the scheme does not use exactly %d products" % (len(zero), zero[0], r))
    D = 1
    terms = []
    for k in range(r):
        dens, ints = [], []
        for f in (U[k], V[k], W[k]):
            df = 1
            for c in f.values():
                df = lcm(df, c.denominator)
            dens.append(df)
            ints.append([(i, c.numerator * (df // c.denominator)) for i, c in f.items()])
        p = dens[0] * dens[1] * dens[2]
        D = lcm(D, p)
        terms.append((p, ints))
    acc = {}
    for p, (fu, fv, fw) in terms:
        s = D // p
        for iu, cu in fu:
            for iv, cv in fv:
                cuv = s * cu * cv
                for iw, cw in fw:
                    key = (iu, iv, iw)
                    acc[key] = acc.get(key, 0) + cuv * cw
    bad = 0
    for (iu, iv, iw), val in acc.items():
        i, j = divmod(iu, n2); jj, l = divmod(iv, n3); ii, ll = divmod(iw, n3)
        want = D if (i == ii and j == jj and l == ll) else 0
        if val != want:
            bad += 1
    for i in range(n1):
        for j in range(n2):
            for l in range(n3):
                if (i * n2 + j, j * n3 + l, i * n3 + l) not in acc:
                    bad += 1
    print("format <%d,%d,%d>, %d terms, every term with three nonzero factors, common denominator %d, "
          "%d Brent equations checked, %d wrong" % (n1, n2, n3, r, D, n1 * n2 * n2 * n3 * n1 * n3, bad))
    if bad:
        print("FAIL")
        sys.exit(1)
    print("rank %d scheme for <%d,%d,%d> over Q verified exactly" % (r, n1, n2, n3))
    print("PASS")

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:  # malformed input of any kind is a failure, never a crash
        print("problem: %s: %s" % (type(e).__name__, str(e)[:200]))
        print("FAIL")
        sys.exit(1)
