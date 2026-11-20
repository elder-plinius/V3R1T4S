#!/usr/bin/env python3
"""dpcount.py: exact size of D(A), the set of ALL linear orders of 1..N that obey a never-condition assignment A
(V3R1T4S package checker, Python standard library only).

Definition (Karpov, Markstrom, Riis and Zhou, arXiv:2601.07336v1, Section 2, quoting Sen): a set of linear orders is a
Condorcet domain if its restriction to every triple of alternatives satisfies a never condition (some alternative of
the triple is never first, never second or never last within the triple). A line "a b c iNj" (a < b < c) says that
the i-th smallest alternative of the triple {a, b, c} is never at position j within the triple (1 top, 2 middle,
3 bottom). If A has exactly one line for every one of the C(N,3) triples, every subset of D(A) - D(A) itself
included - is a Condorcet domain.

Method: build an order from the top. When x is placed after the set S of alternatives already placed, its position
inside the triple {x, y, z} is 1 + |S intersect {y, z}|, so every line about x is decided at that moment. The count
of valid completions of S is memoised (exact Python integers).

Usage: python3 dpcount.py N ASSIGNMENT EXPECTED_COUNT MIN_COUNT
Last output line: PASS if A is well formed (one line per triple, nothing else), |D(A)| == EXPECTED_COUNT and
|D(A)| >= MIN_COUNT; otherwise FAIL.
"""
import sys


def main(argv):
    if len(argv) != 5:
        print(__doc__.strip().splitlines()[-3])
        print("FAIL")
        return 2
    n, path, expected, minimum = int(argv[1]), argv[2], int(argv[3]), int(argv[4])
    cons = {x: [] for x in range(1, n + 1)}
    seen, bad, lines = set(), 0, 0
    with open(path, "rb") as fh:
        raw = fh.read()
    for ln in raw.split(b"\n")[:-1] if raw.endswith(b"\n") else raw.split(b"\n"):
        lines += 1
        try:
            text = ln.decode("ascii")
        except UnicodeDecodeError:
            bad += 1
            continue
        parts = text.split(" ")
        if len(parts) != 4 or any(not p for p in parts):
            bad += 1
            continue
        a, b, c, cond = parts
        if not (a.isdigit() and b.isdigit() and c.isdigit()) or any(p[0] == "0" for p in (a, b, c)):
            bad += 1
            continue
        a, b, c = int(a), int(b), int(c)
        if not (1 <= a < b < c <= n) or len(cond) != 3 or cond[1] != "N" or cond[0] not in "123" or cond[2] not in "123":
            bad += 1
            continue
        if (a, b, c) in seen:
            bad += 1
            continue
        seen.add((a, b, c))
        t = (a, b, c)
        x = t[int(cond[0]) - 1]
        y, z = [v for v in t if v != x]
        cons[x].append(((1 << (y - 1)) | (1 << (z - 1)), int(cond[2])))
    want = n * (n - 1) * (n - 2) // 6
    if not raw.endswith(b"\n"):
        bad += 1
    print("assignment: %d lines, %d distinct triples (C(%d,3) = %d), %d malformed or repeated" % (lines, len(seen), n, want, bad))
    if bad or len(seen) != want:
        print("the assignment does not have exactly one well-formed line per triple")
        print("FAIL")
        return 1
    full = (1 << n) - 1
    memo = {}

    def count(S):
        if S == full:
            return 1
        v = memo.get(S)
        if v is not None:
            return v
        tot = 0
        for x in range(1, n + 1):
            bit = 1 << (x - 1)
            if S & bit:
                continue
            for mask, j in cons[x]:
                if 1 + bin(S & mask).count("1") == j:
                    break
            else:
                tot += count(S | bit)
        memo[S] = tot
        return tot

    total = count(0)
    print("n %d |D(A)| %d (memoised prefix sets: %d)" % (n, total, len(memo)))
    ok = total == expected and total >= minimum
    print("expected %d: %s; at least %d: %s" % (expected, "yes" if total == expected else "NO",
                                                 minimum, "yes" if total >= minimum else "NO"))
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
