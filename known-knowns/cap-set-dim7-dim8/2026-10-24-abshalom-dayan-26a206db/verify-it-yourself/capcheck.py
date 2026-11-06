#!/usr/bin/env python3
"""Two independent exact cap-set checkers for F_3^n (bank target cap-set-dim7-dim8).

Input file: one vector per line, n digits from {0,1,2} (spaces/commas allowed).
Checker A (pairs, the bank's method): for every pair x != y, -(x+y) mod 3 must not be in S.
Checker B (lines): enumerate every affine line {a, a+r, a+2r} (r != 0) of F_3^n that meets S in
two points and count lines fully inside S; the set is a cap iff that count is 0.
Both also check distinctness, coordinate range and dimension. Exit 0 = cap, 1 = not a cap, 2 = malformed.
"""
import sys, itertools

def parse(path, n):
    vecs = []
    for ln, line in enumerate(open(path), 1):
        s = line.split('#')[0].replace(',', ' ').split()
        if not s:
            continue
        digits = list(''.join(s))
        if len(digits) != n:
            raise ValueError("line %d: dimension %d, expected %d" % (ln, len(digits), n))
        if any(d not in '012' for d in digits):
            raise ValueError("line %d: coordinate outside {0,1,2}" % ln)
        vecs.append(tuple(int(d) for d in digits))
    return vecs

def checker_a(vecs, n):
    enc = lambda v: sum(c * 3 ** i for i, c in enumerate(v))
    codes = [enc(v) for v in vecs]
    if len(set(codes)) != len(codes):
        return False, "duplicate vectors"
    S = set(codes)
    for i in range(len(vecs)):
        x = vecs[i]
        for j in range(i + 1, len(vecs)):
            y = vecs[j]
            z = enc(tuple((-(a + b)) % 3 for a, b in zip(x, y)))
            if z in S:
                return False, "line: %s %s and third point code %d" % (x, y, z)
    return True, "cap of size %d (pairs checked: %d)" % (len(vecs), len(vecs) * (len(vecs) - 1) // 2)

def checker_b(vecs, n):
    # Independent route: tuples as keys, direction-based line enumeration, no base-3 encoding.
    if len(set(vecs)) != len(vecs):
        return False, "duplicate vectors"
    S = set(vecs)
    full = 0
    seen = set()
    for a in vecs:
        for b in vecs:
            if a == b:
                continue
            r = tuple((bb - aa) % 3 for aa, bb in zip(a, b))
            line = frozenset(tuple((aa + k * rr) % 3 for aa, rr in zip(a, r)) for k in range(3))
            if line in seen:
                continue
            seen.add(line)
            if line <= S:
                full += 1
    return full == 0, "%d lines inside S (lines meeting S twice or more: %d)" % (full, len(seen))

def main():
    if len(sys.argv) != 3:
        print("usage: capcheck.py <file> <n>"); sys.exit(2)
    n = int(sys.argv[2])
    try:
        vecs = parse(sys.argv[1], n)
    except ValueError as e:
        print("MALFORMED:", e); sys.exit(2)
    ra, ma = checker_a(vecs, n)
    rb, mb = checker_b(vecs, n)
    print("checker A:", "CAP" if ra else "NOT A CAP", "-", ma)
    print("checker B:", "CAP" if rb else "NOT A CAP", "-", mb)
    if ra != rb:
        print("DISAGREE"); sys.exit(3)
    if n == 7 and ra and len(vecs) > 288:
        print("BUG: exceeds Thackeray's bound 288 for n=7"); sys.exit(3)
    print("VERDICT:", "CAP" if ra else "NOT A CAP", "size", len(vecs), "n", n)
    sys.exit(0 if ra else 1)

if __name__ == "__main__":
    main()
