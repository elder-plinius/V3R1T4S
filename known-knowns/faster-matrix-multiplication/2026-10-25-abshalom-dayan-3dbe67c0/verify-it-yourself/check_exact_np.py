#!/usr/bin/env python3
"""Exact, streamed Brent-equation checker for bilinear matrix multiplication schemes over Q (numpy + stdlib).

Same definition and same text format as verify-it-yourself/check_brent_stdlib.py of the 18x18x19 package:
  m_k = (sum u_k[i*n2+j] A[i][j]) * (sum v_k[j*n3+l] B[j][l]),   C[i][l] = sum_k w_k[i*n3+l] m_k.
Brent equations, for ALL i,i' < n1, j,j' < n2, l,l' < n3 (zero ones included):
  sum_k u_k[i*n2+j] v_k[j'*n3+l] w_k[i'*n3+l'] = [i=i'][j=j'][l=l'].

Exactness argument (all of it is checked at run time, and the run aborts rather than continue if one fails):
 1. Every coefficient is parsed as an exact rational p/q (Python ints). Each factor matrix X in {U,V,W} is multiplied by
    its own least common denominator Dx (lcm of the reduced denominators), giving integer matrices U', V', W'.
    The equations become  sum_k U'[a,k] V'[b,k] W'[c,k] = D * target[a,b,c],  D = Du*Dv*Dw  (D*0 = 0 for the zero ones).
    Scaling by a nonzero constant preserves equality, so the integer system holds iff the rational one does.
 2. For a fixed first index a, the whole (b,c) slab is T = X^T Wsel, X[k,b] = U'[a,k] V'[b,k] (float64 matrix product,
    BLAS, so the summation order is unknown). Let bound_a = sum_k |U'[a,k]| max_b|V'[b,k]| max_c|W'[c,k]| (computed
    with exact Python integers). Every product U'V'W' that enters a slab entry is an integer with absolute value
    <= its term's contribution to bound_a, and every partial sum, in whatever order or blocking BLAS uses, is a sum of a
    subset of those integers, so its absolute value is <= bound_a. All operands are integers below 2**53 in absolute
    value. IEEE double arithmetic is exact on integers whose exact result is below 2**53 (also with fused multiply-add),
    so when bound_a < 2**53 the float result is the exact integer. If bound_a >= 2**53 the terms of that slab are split
    into chunks, each with chunk bound < 2**53, and the chunk results are added as int64; the program asserts that
    bound_a < 2**62, so the int64 sum cannot overflow either. D < 2**62 is asserted.
 3. T (converted to int64, exact) is compared entry by entry with D*target, and the mismatches are counted. All
    n1 n2 * n2 n3 * n1 n3 triples are covered: slab a = 0 .. n1 n2 - 1, each with all (b,c). A slab with no terms
    is compared as T = 0.
Memory: dense V' and W' (terms x index, float64) plus one slab and its operands at a time.

Also: terms with a zero factor, mergeable pairs (two proportional factors, exact: same support and same primitive
integer vector up to sign), LCD per factor matrix, three random exact evaluations C = AB with fractions.Fraction on
random small rational matrices, sha256 of every input file.

Usage: check_exact_np.py <dir with u,v,w (.txt or .partN.txt)> [--trials 3] [--seed 1] [--json out.json]
Last line: PASS or FAIL.
"""
import sys, os, re, glob, json, time, random, hashlib
from array import array
from fractions import Fraction
from math import lcm, gcd
import numpy as np

LINE = re.compile(r"(?:\d+:-?\d+(?:/\d+)?(?: \d+:-?\d+(?:/\d+)?)*)?")
LIM53 = int(os.environ.get("CHECK_LIM53_TEST", 1 << 53))  # env override only for testing the chunked path
LIM62 = 1 << 62


def die(msg):
    print("problem: " + msg)
    print("FAIL")
    sys.exit(1)


def part_files(base, which):
    one = os.path.join(base, which + ".txt")
    if os.path.exists(one):
        return [one]
    parts = glob.glob(os.path.join(base, which + ".part*.txt"))
    parts.sort(key=lambda p: int(re.search(r"\.part(\d+)\.txt$", p).group(1)))
    if not parts:
        die("no %s.txt or %s.partN.txt in %s" % (which, which, base))
    return parts


def read_factor(paths, which):
    fmt = rank = None
    indptr = array("q", [0])
    idx = array("q")
    num = array("q")
    den = array("q")
    nrow = 0
    for path in paths:
        with open(path, "r", encoding="ascii", newline="") as fh:
            data = fh.read()
        for ln, s in enumerate(data.split("\n")):
            if s.endswith("\r"):
                die("%s: CR in line" % path)
            if s.startswith("#"):
                m = re.fullmatch(r"#\s*format\s+(\d+)\s+(\d+)\s+(\d+)", s)
                if m:
                    fmt = tuple(int(x) for x in m.groups())
                m = re.fullmatch(r"#\s*rank\s+(\d+)", s)
                if m:
                    rank = int(m.group(1))
                continue
            if s == "" and ln == data.count("\n"):
                continue  # final newline
            if fmt is None or rank is None:
                die("%s: data line before format/rank headers" % which)
            if not LINE.fullmatch(s):
                die("%s line %d: malformed" % (which, ln + 1))
            for tok in s.split():
                a, _, c = tok.partition(":")
                n, _, d = c.partition("/")
                n = int(n)
                d = int(d) if d else 1
                if d == 0:
                    die("%s: zero denominator" % which)
                if n:
                    g = gcd(abs(n), d)
                    idx.append(int(a)); num.append(n // g); den.append(d // g)
            nrow += 1
            indptr.append(len(idx))
    if fmt is None or rank is None:
        die("%s: missing header" % which)
    n1, n2, n3 = fmt
    size = {"u": n1 * n2, "v": n2 * n3, "w": n1 * n3}[which]
    ip = np.frombuffer(indptr, dtype=np.int64).copy()
    ix = np.frombuffer(idx, dtype=np.int64).copy()
    nu = np.frombuffer(num, dtype=np.int64).copy()
    de = np.frombuffer(den, dtype=np.int64).copy()
    if ix.size and (ix.min() < 0 or ix.max() >= size):
        die("%s: index out of range" % which)
    row = np.repeat(np.arange(nrow, dtype=np.int64), np.diff(ip))
    # sort within rows, reject repeats
    order = np.lexsort((ix, row))
    ix, nu, de, row = ix[order], nu[order], de[order], row[order]
    key = row * size + ix
    if key.size > 1 and np.any(key[1:] == key[:-1]):
        die("%s: repeated index within a term" % which)
    # nonzero coefficients were kept, so zero entries were dropped (a term with all-zero entries has empty row)
    ip = np.concatenate([[0], np.cumsum(np.bincount(row, minlength=nrow))]).astype(np.int64)
    return fmt, rank, nrow, size, ip, ix, nu, de, row


def lcd_of(de):
    d = 1
    for x in np.unique(de).tolist():
        d = lcm(d, int(x))
    return d


def scale_to_int(nu, de, D):
    """exact integer nu * D / de, with an overflow guard."""
    if nu.size == 0:
        return nu.copy()
    assert D < LIM62
    mx = int(np.abs(nu).max())
    assert mx * D < LIM62, "scaled coefficient could overflow int64"
    q = np.empty_like(nu)
    for x in np.unique(de).tolist():
        m = de == x
        assert D % int(x) == 0
        q[m] = nu[m] * (D // int(x))
    return q


def primitive_keys(row, ix, val, nrow):
    """per term: hashable key of the projective class (support + primitive integer vector, sign-normalised)."""
    keys = []
    starts = np.searchsorted(row, np.arange(nrow + 1))
    for k in range(nrow):
        s, e = starts[k], starts[k + 1]
        v = val[s:e]
        g = int(np.gcd.reduce(np.abs(v))) if v.size else 1
        v = v // g
        if v.size and v[0] < 0:
            v = -v
        keys.append((ix[s:e].tobytes(), v.tobytes()))
    ids = {}
    return [ids.setdefault(k, len(ids)) for k in keys]


def main():
    args = sys.argv[1:]
    if not args:
        die("usage: check_exact_np.py <dir> [--trials N] [--seed S] [--json out]")
    base = args[0]
    trials = int(args[args.index("--trials") + 1]) if "--trials" in args else 3
    seed = int(args[args.index("--seed") + 1]) if "--seed" in args else 1
    jout = args[args.index("--json") + 1] if "--json" in args else None
    t0 = time.time()
    res = {"dir": base}
    shas = {}
    for w in "uvw":
        for p in part_files(base, w):
            shas[os.path.basename(p)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    res["file_sha256"] = shas
    fac = {}
    for w in "uvw":
        fac[w] = read_factor(part_files(base, w), w)
    (fu, ru, nu_, szu, ipu, ixu, numu, denu, rowu) = fac["u"]
    (fv, rv, nv_, szv, ipv, ixv, numv, denv, rowv) = fac["v"]
    (fw, rw, nw_, szw, ipw, ixw, numw, denw, roww) = fac["w"]
    if not (fu == fv == fw and ru == rv == rw):
        die("files disagree on format or rank")
    n1, n2, n3 = fu
    r = ru
    if not (nu_ == nv_ == nw_ == r):
        die("data lines %d/%d/%d but rank header %d" % (nu_, nv_, nw_, r))
    res.update(format=[n1, n2, n3], rank=r)
    # zero factors
    cu, cv, cw = (np.diff(ip) for ip in (ipu, ipv, ipw))
    zero_terms = int(np.sum((cu == 0) | (cv == 0) | (cw == 0)))
    res["terms_with_zero_factor"] = zero_terms
    print("format <%d,%d,%d> (A %dx%d, B %dx%d), %d terms, terms with a zero factor: %d" % (n1, n2, n3, n1, n2, n2, n3, r, zero_terms))
    if zero_terms:
        die("a term has a zero factor")
    res["nonzeros"] = {"u": int(ixu.size), "v": int(ixv.size), "w": int(ixw.size)}
    res["denominators_occurring_gt1"] = sorted({int(x) for x in np.unique(np.concatenate([denu, denv, denw])) if x != 1})
    Du, Dv, Dw = lcd_of(denu), lcd_of(denv), lcd_of(denw)
    res["lcd"] = {"u": Du, "v": Dv, "w": Dw}
    print("nonzeros u %d, v %d, w %d; LCD per factor matrix: U %d, V %d, W %d" % (ixu.size, ixv.size, ixw.size, Du, Dv, Dw))
    D = Du * Dv * Dw
    assert D < LIM62, "D too large for int64"
    Ui, Vi, Wi = scale_to_int(numu, denu, Du), scale_to_int(numv, denv, Dv), scale_to_int(numw, denw, Dw)
    res["max_abs_scaled"] = {"u": int(np.abs(Ui).max()), "v": int(np.abs(Vi).max()), "w": int(np.abs(Wi).max())}

    # mergeable pairs
    ku = primitive_keys(rowu, ixu, Ui, r)
    kv = primitive_keys(rowv, ixv, Vi, r)
    kw = primitive_keys(roww, ixw, Wi, r)
    merge = {}
    for name, (a, b) in (("uv", (ku, kv)), ("uw", (ku, kw)), ("vw", (kv, kw))):
        seen = set()
        c = 0
        for p in zip(a, b):
            if p in seen:
                c += 1
            else:
                seen.add(p)
        merge[name] = c
    res["mergeable_pairs"] = merge
    res["duplicate_factors"] = {"u": r - len(set(ku)), "v": r - len(set(kv)), "w": r - len(set(kw))}
    print("pairs of terms sharing two proportional factors (mergeable): uv %d, uw %d, vw %d" % (merge["uv"], merge["uw"], merge["vw"]))

    # ---- Brent equations, streamed per A-index
    Vd = np.zeros((r, szv), dtype=np.float64)
    Wd = np.zeros((r, szw), dtype=np.float64)
    assert int(np.abs(Vi).max()) < LIM53 and int(np.abs(Wi).max()) < LIM53 and int(np.abs(Ui).max()) < LIM53
    Vd[rowv, ixv] = Vi.astype(np.float64)
    Wd[roww, ixw] = Wi.astype(np.float64)
    assert np.array_equal(Vd[rowv, ixv].astype(np.int64), Vi) and np.array_equal(Wd[roww, ixw].astype(np.int64), Wi)
    maxV = [int(x) for x in np.abs(Vd).max(axis=1)]
    maxW = [int(x) for x in np.abs(Wd).max(axis=1)]
    cost = [maxV[k] * maxW[k] for k in range(r)]
    order = np.argsort(ixu, kind="stable")
    a_sorted = ixu[order]
    k_sorted = rowu[order]
    u_sorted = Ui[order]
    a_ptr = np.searchsorted(a_sorted, np.arange(n1 * n2 + 1))
    tgt = np.zeros((szv, szw), dtype=np.int64)
    wrong = 0
    max_bound = 0
    nchunk_slabs = 0
    for a in range(n1 * n2):
        i, j = divmod(a, n2)
        s, e = a_ptr[a], a_ptr[a + 1]
        ks = k_sorted[s:e]
        us = u_sorted[s:e]
        # exact bounds
        contrib = [abs(int(u)) * cost[int(k)] for u, k in zip(us.tolist(), ks.tolist())]
        bound = sum(contrib)
        max_bound = max(max_bound, bound)
        assert bound < LIM62, "int64 accumulation could overflow"
        assert all(c < LIM53 for c in contrib)
        T = np.zeros((szv, szw), dtype=np.int64)
        if len(ks):
            if bound < LIM53:
                chunks = [(0, len(ks))]
            else:
                nchunk_slabs += 1
                chunks = []
                st, acc = 0, 0
                for q, c in enumerate(contrib):
                    if acc + c >= LIM53:
                        chunks.append((st, q)); st, acc = q, 0
                    acc += c
                chunks.append((st, len(ks)))
            for (x0, x1) in chunks:
                kk = ks[x0:x1]
                X = Vd[kk] * us[x0:x1].astype(np.float64)[:, None]
                Tf = X.T @ Wd[kk]
                T += Tf.astype(np.int64)
        l = np.arange(n3)
        tgt[j * n3 + l, i * n3 + l] = D
        wrong += int(np.count_nonzero(T != tgt))
        tgt[j * n3 + l, i * n3 + l] = 0
        if a % 100 == 0:
            print("  slab %d/%d, wrong so far %d, %.0fs" % (a, n1 * n2, wrong, time.time() - t0), flush=True)
    total = (n1 * n2) * (n2 * n3) * (n1 * n3)
    res.update(brent_equations_checked=total, brent_wrong=wrong, D=D, max_slab_bound=max_bound,
               max_slab_bound_bits=max_bound.bit_length(), slabs_needing_chunks=nchunk_slabs)
    print("Brent equations: %d checked (all index triples), %d wrong; D = Du*Dv*Dw = %d; max slab bound %d (< 2^%d)"
          % (total, wrong, D, max_bound, max_bound.bit_length()))
    del Vd, Wd

    # ---- random exact evaluations with Fractions
    def terms_of(ip, ix, nu, de):
        return ip, ix.tolist(), nu.tolist(), de.tolist()
    UP, UI, UN, UD = terms_of(ipu, ixu, numu, denu)
    VP, VI, VN, VD = terms_of(ipv, ixv, numv, denv)
    WP, WI, WN, WD = terms_of(ipw, ixw, numw, denw)
    rnd = random.Random(seed)
    evals = []
    rand_bad = 0
    for t in range(trials):
        A = [Fraction(rnd.randint(-20, 20), rnd.randint(1, 12)) for _ in range(n1 * n2)]
        B = [Fraction(rnd.randint(-20, 20), rnd.randint(1, 12)) for _ in range(n2 * n3)]
        C = [Fraction(0)] * (n1 * n3)
        for k in range(r):
            sa = sum((Fraction(UN[p], UD[p]) * A[UI[p]] for p in range(UP[k], UP[k + 1])), Fraction(0))
            sb = sum((Fraction(VN[p], VD[p]) * B[VI[p]] for p in range(VP[k], VP[k + 1])), Fraction(0))
            m = sa * sb
            if m:
                for p in range(WP[k], WP[k + 1]):
                    C[WI[p]] += Fraction(WN[p], WD[p]) * m
        AB = [sum((A[i * n2 + j] * B[j * n3 + l] for j in range(n2)), Fraction(0)) for i in range(n1) for l in range(n3)]
        bad = sum(1 for x, y in zip(C, AB) if x != y)
        evals.append({"seed": seed, "trial": t + 1, "entries": n1 * n3, "differ": bad})
        print("random exact evaluation %d (seed %d, rational entries p/q, |p|<=20, q<=12): %d of %d entries of C differ from AB"
              % (t + 1, seed, bad, n1 * n3), flush=True)
        rand_bad += bad
    res["random_evaluations"] = evals
    res["seconds"] = round(time.time() - t0, 1)
    res["pass"] = (wrong == 0 and rand_bad == 0)
    if jout:
        json.dump(res, open(jout, "w"), indent=1)
    if wrong or rand_bad:
        die("%d Brent equations fail, %d random-evaluation entries differ" % (wrong, rand_bad))
    print("rank-%d scheme for <%d,%d,%d> over Q: all Brent equations hold exactly" % (r, n1, n2, n3))
    print("PASS")


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("problem: %s: %s" % (type(e).__name__, str(e)[:200]))
        print("FAIL")
        sys.exit(1)
