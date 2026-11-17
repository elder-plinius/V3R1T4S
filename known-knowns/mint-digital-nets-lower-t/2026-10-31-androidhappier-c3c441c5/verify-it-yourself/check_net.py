#!/usr/bin/env python3
"""Standalone checker (Python standard library only) for a digital (t,m,s)-net over F_2.

Definition checked: C_1..C_s in F_2^{m x m} generate a digital (t,m,s)-net over F_2 iff for EVERY composition
(d_1,...,d_s) of k = m - t into s non-negative parts, the k vectors {row r of C_i : 1 <= r <= d_i, 1 <= i <= s}
are linearly independent over F_2 (rank k). This program checks every one of the C(k+s-1, s-1) compositions.

How: depth-first over d_1, d_2, ..., d_{s-1}; the rows chosen so far are kept as an echelon basis (pivot = lowest
set bit). For a fixed prefix (d_1..d_{s-1}) the last part is forced, d_s = k - sum. A prefix whose rows are already
dependent fails for every completion, so it is reported as a failure with a witness composition. For the last
block, the first r rows of C_s stay independent modulo the span for all r up to some r_max (prefix independence is
monotone in r), so the composition passes iff d_s <= r_max. Each composition is counted once; the total must equal
C(k+s-1, s-1).

Input format: lines starting with '#' are comments; s blocks separated by blank lines; each block has the rows of
C_i (row 1 first), one row per line, m characters 0/1 (column 1 first). Blocks may have fewer than m rows if they
have at least k rows. Usage: python3 check_net.py FILE m s t   Last output line: PASS or FAIL.
"""
import sys
from math import comb


def parse(path, m, s):
    blocks, cur = [], []
    with open(path, "r", encoding="ascii") as f:
        for n, raw in enumerate(f, 1):
            line = raw.rstrip("\r\n").strip()
            if line.startswith("#"):
                continue
            if line == "":
                if cur:
                    blocks.append(cur)
                    cur = []
                continue
            if len(line) != m or any(ch not in "01" for ch in line):
                raise ValueError("line %d: expected %d characters 0/1" % (n, m))
            v = 0
            for c, ch in enumerate(line):
                if ch == "1":
                    v |= 1 << c
            cur.append(v)
    if cur:
        blocks.append(cur)
    if len(blocks) != s:
        raise ValueError("found %d blocks, expected %d" % (len(blocks), s))
    return blocks


def reduce_low(v, basis):
    """Reduce v by an echelon basis keyed by lowest set bit; return the remainder (0 = dependent)."""
    while v:
        low = v & -v
        b = basis.get(low)
        if b is None:
            return v
        v ^= b
    return 0


def check(blocks, m, s, t):
    k = m - t
    for i, b in enumerate(blocks):
        if len(b) < k:
            return False, 0, "block %d has only %d rows, need %d" % (i + 1, len(b), k)
    counted = 0
    prefix = [0] * s
    last = blocks[s - 1]

    def rec(i, rem, basis):
        nonlocal counted
        if i == s - 1:
            loc = dict(basis)
            r = 0
            while r < rem:
                v = reduce_low(last[r], loc)
                if v == 0:
                    break
                loc[v & -v] = v
                r += 1
            if r < rem:
                prefix[i] = rem
                return "rank deficient at composition %s" % (tuple(prefix),)
            counted += 1
            return None
        loc = dict(basis)
        rows = blocks[i]
        for d in range(rem + 1):
            if d:
                v = reduce_low(rows[d - 1], loc)
                if v == 0:
                    prefix[i] = d
                    for j in range(i + 1, s):
                        prefix[j] = 0
                    prefix[s - 1] = rem - d if i < s - 1 else 0
                    return "rank deficient at composition %s" % (tuple(prefix),)
                loc[v & -v] = v
            prefix[i] = d
            err = rec(i + 1, rem - d, loc)
            if err:
                return err
        prefix[i] = 0
        return None

    err = rec(0, k, {})
    total = comb(k + s - 1, s - 1)
    if err:
        return False, counted, err
    if counted != total:
        return False, counted, "counted %d compositions, expected %d" % (counted, total)
    return True, counted, "all %d compositions of k=%d into s=%d parts have rank %d" % (total, k, s, k)


def main():
    if len(sys.argv) != 5:
        print("usage: check_net.py FILE m s t")
        print("FAIL")
        return 2
    path = sys.argv[1]
    m, s, t = (int(x) for x in sys.argv[2:5])
    try:
        blocks = parse(path, m, s)
    except (OSError, ValueError) as e:
        print("parse error: %s" % e)
        print("FAIL")
        return 1
    ok, counted, msg = check(blocks, m, s, t)
    print("b=2 m=%d s=%d t=%d k=%d compositions_checked=%d expected=%d: %s"
          % (m, s, t, m - t, counted, comb(m - t + s - 1, s - 1), msg))
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
