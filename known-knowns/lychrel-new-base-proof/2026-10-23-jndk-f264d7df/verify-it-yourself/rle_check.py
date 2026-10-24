#!/usr/bin/env python3
"""Exact reverse-and-add template-closure checker (written from the definition, this run).

Numbers are digit lists, most significant first. A template is a run list [(digit, (a, k))]: a run of `digit`
repeated a + k*m times, m >= 0 the template parameter.

Symbolic step. Digit i from the left pairs with digit i from the right, so the pair sums are constant on the segments
cut by the run boundaries of x and of reversed(x). On a segment with constant pair sum s, carries settle after one
digit: c1 = [s + c >= b]; then [s + c1 >= b] = c1 in all three cases s >= b, s <= b-2, s = b-1. So a segment of
length L emits one digit (s+c) mod b followed by L-1 copies of (s+c1) mod b, with outgoing carry c1 (and if
L could be 0 the segment is absent). This is exact for every m at which the boundary order used is valid.
"""
import sys, json
from fractions import Fraction

def to_digits(n, b):
    if n == 0:
        return [0]
    out = []
    while n:
        n, r = divmod(n, b)
        out.append(r)
    return out[::-1]

def ra(d, b):
    """Concrete reverse-and-add on a digit list (MSB first)."""
    L = len(d); out = []; c = 0
    for i in range(L - 1, -1, -1):
        v = d[i] + d[L - 1 - i] + c
        out.append(v % b); c = v // b
    if c:
        out.append(c)
    return out[::-1]

def is_pal(d):
    return d == d[::-1]

def rle(d):
    runs = []
    for x in d:
        if runs and runs[-1][0] == x:
            runs[-1][1] += 1
        else:
            runs.append([x, 1])
    return [(x, n) for x, n in runs]

def expand(t, m):
    out = []
    for dg, (a, k) in t:
        n = a + k * m
        if n < 0:
            raise ValueError('negative run length')
        out.extend([dg] * n)
    return out

def aff_add(f, g):
    return (f[0] + g[0], f[1] + g[1])

def aff_sub(f, g):
    return (f[0] - g[0], f[1] - g[1])

def stable_from(f):
    """Smallest integer M >= 0 such that sign of f(m) is constant (and equal to the asymptotic sign) for m >= M."""
    a, k = f
    if k == 0:
        return 0
    # root at m = -a/k; sign constant for m > root
    r = Fraction(-a, k)
    M = int(r) + 1 if r >= 0 else 0
    return max(M, 0)

def asym_sign(f):
    a, k = f
    if k != 0:
        return 1 if k > 0 else -1
    return (a > 0) - (a < 0)

def normalize(runs):
    """Merge equal adjacent digits; drop identically-zero runs."""
    out = []
    for dg, f in runs:
        if f == (0, 0):
            continue
        if out and out[-1][0] == dg:
            out[-1] = (dg, aff_add(out[-1][1], f))
        else:
            out.append((dg, f))
    return out

def sym_ra(t, b):
    """Symbolic reverse-and-add. Returns (result runs normalized, M0) valid for all m >= M0."""
    M0 = 0
    for dg, f in t:
        if f[1] < 0:
            raise ValueError('negative slope')
        # need length >= 1 for canonical form: a + k m >= 1
        M0 = max(M0, stable_from(aff_sub(f, (1, 0))) if f[1] > 0 else 0)
        if f[1] == 0 and f[0] < 1:
            raise ValueError('nonpositive constant run')
    total = (0, 0)
    bx = [(0, 0)]
    for dg, f in t:
        total = aff_add(total, f); bx.append(total)
    # boundaries of reversed: total - bx
    pts = set(bx) | set(aff_sub(total, p) for p in bx)
    pts = list(pts)
    # order points for large m; record threshold where all pairwise orders are stable
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            M0 = max(M0, stable_from(aff_sub(pts[i], pts[j])))
    import functools
    def cmp(p, q):
        return asym_sign(aff_sub(p, q))
    pts.sort(key=functools.cmp_to_key(cmp))
    # digit at MSB-index position in [p, q): find run of x containing it, and run of reversed x
    def run_at(bounds, runs_, p):
        # bounds increasing affine; find run r with bounds[r] <= p < bounds[r+1] (asymptotically)
        for r in range(len(runs_)):
            if asym_sign(aff_sub(bounds[r], p)) <= 0 and asym_sign(aff_sub(bounds[r + 1], p)) > 0:
                return runs_[r][0]
        raise RuntimeError('no run')
    rev = t[::-1]
    brev = [(0, 0)]; acc = (0, 0)
    for dg, f in rev:
        acc = aff_add(acc, f); brev.append(acc)
    segs = []  # MSB order: (pair sum, length)
    for i in range(len(pts) - 1):
        p, q = pts[i], pts[i + 1]
        ln = aff_sub(q, p)
        if ln == (0, 0):
            continue
        if asym_sign(ln) <= 0:
            raise RuntimeError('bad order')
        s = run_at(bx, t, p) + run_at(brev, rev, p)
        if ln[1] > 0:
            M0 = max(M0, stable_from(aff_sub(ln, (1, 0))))
        segs.append((s, ln))
    # add from LSB
    out = []; c = 0
    for s, ln in reversed(segs):
        if ln[1] == 0:
            for _ in range(ln[0]):
                v = s + c; out.append((v % b, (1, 0))); c = v // b
        else:
            v = s + c; out.append((v % b, (1, 0))); c1 = v // b
            out.append(((s + c1) % b, aff_sub(ln, (1, 0)))); c = c1
    if c:
        out.append((c, (1, 0)))
    res = normalize(out[::-1])
    for dg, f in res:
        if f[1] > 0:
            M0 = max(M0, stable_from(aff_sub(f, (1, 0))))
    return res, M0

def shift(t, g=1):
    return [(dg, (a + k * g, k)) for dg, (a, k) in t]

def infer_templates(xs, p):
    """xs: concrete iterates x_{t0}..x_{t0+2p}. Returns templates T_0..T_{p-1} or None."""
    T = []
    for i in range(p):
        r0, r1, r2 = rle(xs[i]), rle(xs[i + p]), rle(xs[i + 2 * p])
        if [d for d, _ in r0] != [d for d, _ in r1] or [d for d, _ in r1] != [d for d, _ in r2]:
            return None
        t = []
        for (d, n0), (_, n1), (_, n2) in zip(r0, r1, r2):
            k = n1 - n0
            if k < 0 or n2 - n1 != k:
                return None
            t.append((d, (n0, k)))
        T.append(t)
    if all(k == 0 for t in T for _, (_, k) in t):
        return None
    return T

def sym_nonpal(t):
    """Returns (ok, set of m to check concretely). ok False means palindromic for all large m."""
    t = normalize(t)
    ds = [d for d, _ in t]
    if ds != ds[::-1]:
        return True, set()
    special = set(); always = True
    for i in range(len(t)):
        f, g = t[i][1], t[-1 - i][1]
        if f != g:
            always = False
            dk = f[1] - g[1]; da = g[0] - f[0]
            if dk != 0 and da % dk == 0 and da // dk >= 0:
                special.add(da // dk)
    if always:
        return False, set()
    return True, special

def prove(b, x0, t0, p, max_brute=None, log=None):
    rep = dict(base=b, seed=x0 if isinstance(x0, int) else None, t0=t0, p=p)
    d = to_digits(x0, b) if isinstance(x0, int) else list(x0)
    xs = [d]
    for _ in range(t0 + 3 * p):
        xs.append(ra(xs[-1], b))
    pre_pal = [i for i in range(1, t0 + 1) if is_pal(xs[i])]
    rep['palindrome_before_entry'] = pre_pal
    T = infer_templates(xs[t0:], p)
    if T is None:
        rep['status'] = 'no-template'; return rep
    rep['templates'] = T
    M0 = 0; ok = True; details = []
    for i in range(p):
        res, M = sym_ra(T[i], b)
        target = T[i + 1] if i + 1 < p else shift(T[0])
        target = normalize(target)
        _, Mt = sym_ra(target, b)  # only for the canonical-length threshold of the target
        eq = (res == target)
        details.append(dict(i=i, symbolic_equal=eq, M=M))
        if not eq:
            ok = False
        M0 = max(M0, M, Mt)
    rep['M0'] = M0; rep['steps'] = details
    if not ok:
        rep['status'] = 'symbolic-closure-fails'; return rep
    # brute force m < M0 (closure) and non-palindromicity
    special = set()
    for i in range(p):
        okp, sp = sym_nonpal(T[i])
        if not okp:
            rep['status'] = 'palindromic-template'; return rep
        special |= sp
    lim = M0 + 1
    for m in range(0, lim):
        for i in range(p):
            x = expand(T[i], m)
            y = ra(x, b)
            z = expand(T[i + 1], m) if i + 1 < p else expand(T[0], m + 1)
            if y != z:
                rep['status'] = 'brute-closure-fails'; rep['fail'] = dict(m=m, i=i); return rep
            if is_pal(x):
                rep['status'] = 'palindrome-in-family'; rep['fail'] = dict(m=m, i=i); return rep
    for m in sorted(special):
        for i in range(p):
            if is_pal(expand(T[i], m)):
                rep['status'] = 'palindrome-in-family'; rep['fail'] = dict(m=m, i=i); return rep
    rep['brute_checked_m_upto'] = lim - 1
    rep['special_m_checked'] = sorted(special)
    rep['status'] = 'PROVED' if not pre_pal else 'closure-proved-but-palindrome-before-entry'
    return rep

def find_and_prove(b, x0, tmax=400, pmax=12):
    d = to_digits(x0, b) if isinstance(x0, int) else list(x0)
    xs = [d]
    for _ in range(tmax + 3 * pmax):
        if len(xs) > 1 and is_pal(xs[-1]):
            return dict(base=b, status='palindrome', step=len(xs) - 1)
        xs.append(ra(xs[-1], b))
    for t0 in range(0, tmax):
        for p in range(1, pmax + 1):
            T = infer_templates(xs[t0:t0 + 3 * p], p)
            if T is not None:
                r = prove(b, x0, t0, p)
                if r['status'] in ('PROVED', 'closure-proved-but-palindrome-before-entry'):
                    return r
    return dict(base=b, status='not-found', tmax=tmax, pmax=pmax)

if __name__ == '__main__':
    pass
