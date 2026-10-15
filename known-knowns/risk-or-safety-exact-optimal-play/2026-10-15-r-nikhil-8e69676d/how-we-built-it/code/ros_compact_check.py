#!/usr/bin/env python3
"""ros_compact_check.py -- checker for COMPACT certificates of the coin game "Risk or Safety"
(V3R1T4S target risk-or-safety-exact-optimal-play; main session, written from the definition).

Points-needed coordinates: i = points the player to move still needs, j = points the opponent needs, a = open points
(0 <= a < i). The bank's equations become
    V(a, i, j) = 1                                               for a >= i
    V(0, i, j) = (1/2)(1 - V(0, j, i)) + (1/2) V(1, i, j)        (forced toss)
    V(a, i, j) = max(continue, stop)   for 1 <= a < i, with
        continue = (1/2)(1 - V(0, j, i)) + (1/2) V(a + 1, i, j),   stop = 1 - V(0, j, i - a).
(With b = n - i, c = n - j these are exactly P(a,b,c) = max(...), stop = 1 - P(0, c, a + b), P = 1 when a + b >= n.)

A compact certificate lists only P0(i, j) = V(0, i, j) for all 1 <= i, j <= N (lines "i j num/den"; '#' comments).
For every ordered pair (i, j) this checker recomputes V(a, i, j), a = i-1 .. 1, by the max recursion from the listed
P0 values, then checks the forced-toss equation P0(i, j) == (1/2)(1 - P0(j, i)) + (1/2) V(1, i, j) EXACTLY.
If all N^2 equations hold, the full table defined by the recursion satisfies every Bellman equation, hence (unique
solution) it is the optimal-value table and A387261(n)/A387262(n) = P0(n, n).
It also derives T(i, j) = the smallest a >= 1 at which stop > continue (i if none), reports exact ties, and can compare
with a toss-count file (lines "i j k"), with OEIS b-files, with a values file ("n num/den") and with the A394776 b-file.

Usage: python3 -I ros_compact_check.py P0_FILE [--T T_FILE] [--oeis DIR] [--values VALUES_FILE]
                                      [--a394776 BFILE] [--out-values OUT] [--out-T OUT]
Exit 0 iff COMPACT_PASS (and every requested comparison agrees).
"""
import sys, os, time
from fractions import Fraction

def load_p0(path):
    P0 = {}
    N = 0
    for line in open(path):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        i, j, v = line.split()
        i, j = int(i), int(j)
        if (i, j) in P0:
            raise SystemExit("duplicate entry (%d, %d)" % (i, j))
        num, den = v.split('/') if '/' in v else (v, '1')
        num, den = int(num), int(den)
        f = Fraction(num, den)
        if f.numerator != num or f.denominator != den:
            raise SystemExit("entry (%d, %d) is not reduced: %s" % (i, j, v))
        P0[(i, j)] = f
        N = max(N, i, j)
    return P0, N

def main(argv):
    args = list(argv)
    p0file = args.pop(0)
    opt = {}
    while args:
        k = args.pop(0)
        opt[k] = args.pop(0)
    t0 = time.time()
    P0, N = load_p0(p0file)
    errors = []
    missing = [(i, j) for i in range(1, N + 1) for j in range(1, N + 1) if (i, j) not in P0]
    if missing:
        errors.append("%d entries missing, first %s" % (len(missing), missing[:5]))
    if len(P0) != N * N:
        errors.append("table has %d entries, expected N^2 = %d" % (len(P0), N * N))
    if errors:
        print("\n".join(errors)); print("COMPACT_FAIL"); return 1
    half = Fraction(1, 2)
    one = Fraction(1)
    T = {}
    ties = []
    checked = 0
    bad = 0
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            x = P0[(i, j)]
            y = P0[(j, i)]
            if not (0 <= x <= 1):
                errors.append("P0(%d,%d) outside [0,1]" % (i, j)); bad += 1; continue
            tail = half * (one - y)
            V = one                      # V(i, i, j) = 1 (a = i reaches the goal)
            t_ij = i                     # toss count if no stop is ever better
            for a in range(i - 1, 0, -1):
                cont = tail + half * V
                stop = one - P0[(j, i - a)]
                if stop > cont:
                    V = stop
                    t_ij = a             # overwritten downward; final value = smallest a with stop > cont
                else:
                    if stop == cont:
                        ties.append((a, i, j))
                    V = cont
            forced = tail + half * V     # V(1, i, j) is V after the loop (or 1 when i = 1)
            if forced != x:
                bad += 1
                if bad <= 10:
                    errors.append("forced-toss equation fails at (i=%d, j=%d): listed %s, recomputed %s" % (i, j, x, forced))
            T[(i, j)] = t_ij
            checked += 1
    elapsed = time.time() - t0
    print("N=%d ordered_pairs_checked=%d failures=%d exact_ties=%d time=%.1fs" % (N, checked, bad, len(ties), elapsed))
    if ties[:10]:
        print("ties (a,i,j):", ties[:10])
    for e in errors[:10]:
        print("  - " + e)
    ok = (bad == 0 and not errors)
    # comparisons
    if '--values' in opt:
        vals = {}
        for line in open(opt['--values']):
            p = line.split()
            if len(p) == 2 and '/' in p[1]:
                vals[int(p[0])] = Fraction(p[1])
        mism = [n for n in vals if n <= N and P0[(n, n)] != vals[n]]
        print("values_file_compare: %d terms compared, %d mismatches %s" % (len([n for n in vals if n <= N]), len(mism), mism[:5]))
        ok &= not mism
    if '--oeis' in opt:
        d = opt['--oeis']
        num, den = {}, {}
        for fn, dst in (("b387261.txt", num), ("b387262.txt", den)):
            for line in open(os.path.join(d, fn)):
                line = line.strip()
                if line and not line.startswith('#'):
                    k, v = line.split(); dst[int(k)] = int(v)
        mism = [n for n in num if n <= N and P0[(n, n)] != Fraction(num[n], den[n])]
        print("oeis_compare: %d published terms, %d mismatches %s -> oeis_match=%s" % (len([n for n in num if n <= N]), len(mism), mism, "yes" if not mism else "NO"))
        ok &= not mism
    if '--T' in opt:
        Tf = {}
        for line in open(opt['--T']):
            p = line.split()
            if len(p) == 3 and not line.startswith('#'):
                Tf[(int(p[0]), int(p[1]))] = int(p[2])
        mism = [(k, Tf[k], T.get(k)) for k in Tf if T.get(k) != Tf[k]]
        print("T_file_compare: %d entries, %d mismatches %s" % (len(Tf), len(mism), mism[:5]))
        ok &= not mism
    if '--a394776' in opt:
        b = {}
        for line in open(opt['--a394776']):
            p = line.split()
            if len(p) == 2 and not line.startswith('#'):
                b[int(p[0])] = int(p[1])
        mism = []
        cnt = 0
        for i in range(1, min(N, 20) + 1):
            for j in range(1, min(N, 20) + 1):
                idx = (j - 1) ** 2 + i if i < j else i * i - j + 1
                if idx in b:
                    cnt += 1
                    if b[idx] != T[(i, j)]:
                        mism.append((i, j, b[idx], T[(i, j)]))
        print("a394776_compare: %d published terms compared, %d mismatches %s" % (cnt, len(mism), mism[:5]))
        ok &= not mism
    if '--out-values' in opt:
        with open(opt['--out-values'], 'w') as f:
            for n in range(1, N + 1):
                f.write("%d %d/%d\n" % (n, P0[(n, n)].numerator, P0[(n, n)].denominator))
        print("wrote values n=1..%d to %s" % (N, opt['--out-values']))
    if '--out-T' in opt:
        with open(opt['--out-T'], 'w') as f:
            for i in range(1, N + 1):
                for j in range(1, N + 1):
                    f.write("%d %d %d\n" % (i, j, T[(i, j)]))
        print("wrote T table to %s" % opt['--out-T'])
    print("COMPACT_PASS" if ok else "COMPACT_FAIL")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
