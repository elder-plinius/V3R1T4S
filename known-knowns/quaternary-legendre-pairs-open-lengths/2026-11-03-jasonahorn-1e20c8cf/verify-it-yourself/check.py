#!/usr/bin/env python3
"""Exhaust the two groups named in object/groups.txt. Last line PASS or FAIL."""
import sys
from pathlib import Path

N = 70
CANON = {
    (1, 3, 9, 11, 13, 17, 27, 29, 33, 39, 47, 51),
    (1, 9, 11, 23, 29, 37, 39, 43, 51, 53, 57, 67),
}


def fail(msg):
    print(msg)
    print("FAIL")
    sys.exit(1)


def orbits(group):
    seen = [False] * N
    out = []
    for start in range(N):
        if seen[start]:
            continue
        orb = []
        stack = [start]
        seen[start] = True
        while stack:
            x = stack.pop()
            orb.append(x)
            for g in group:
                y = (g * x) % N
                if not seen[y]:
                    seen[y] = True
                    stack.append(y)
        out.append(orb)
    return out


def paf_key(seq):
    ext = seq + seq
    key = []
    for k in range(1, N):
        c0 = c1 = c2 = c3 = 0
        for j in range(N):
            d = (ext[j] - ext[j + k]) & 3
            if d == 0:
                c0 += 1
            elif d == 1:
                c1 += 1
            elif d == 2:
                c2 += 1
            else:
                c3 += 1
        key.append(c0 - c2)
        key.append(c1 - c3)
    return tuple(key)


def needed(key):
    out = []
    for i in range(0, len(key), 2):
        out.append(-2 - key[i])
        out.append(-key[i + 1])
    return tuple(out)


def search(group):
    orbs = orbits(group)
    sizes = [len(o) for o in orbs]
    total = 4 ** len(orbs)
    bucket0 = {}
    bucket2 = {}
    n0 = n2 = 0
    for idx in range(total):
        re = im = 0
        x = idx
        assign = []
        for s in sizes:
            d = x & 3
            x >>= 2
            assign.append(d)
            if d == 0:
                re += s
            elif d == 1:
                im += s
            elif d == 2:
                re -= s
            else:
                im -= s
        nrm = re * re + im * im
        if nrm == 0:
            n0 += 1
        elif nrm == 2:
            n2 += 1
        else:
            continue
        seq = [0] * N
        for val, orb in zip(assign, orbs):
            for p in orb:
                seq[p] = val
        key = paf_key(seq)
        (bucket0 if nrm == 0 else bucket2).setdefault(key, 1)
    hits = sum(1 for key in bucket2 if needed(key) in bucket0)
    return n0, n2, hits, total


def main():
    root = Path(__file__).resolve().parents[1]
    text = (root / "object" / "groups.txt").read_text()
    lines = [ln.split() for ln in text.splitlines() if ln.strip()]
    groups = []
    expect = {}
    for parts in lines:
        if parts[0] in ("H1", "H2"):
            groups.append(tuple(int(x) for x in parts[1:]))
        else:
            expect[parts[0]] = int(parts[1])
    if set(groups) != CANON:
        fail("groups are not the two named order-12 subgroups")
    if any(69 in g for g in groups):
        fail("a group contains -1")
    total_hits = 0
    for i, group in enumerate(groups, start=1):
        n0, n2, hits, space = search(group)
        tag = "H1" if group == (1, 3, 9, 11, 13, 17, 27, 29, 33, 39, 47, 51) else "H2"
        if n0 != expect["expected_norm0_" + tag] or n2 != expect["expected_norm2_" + tag]:
            fail("count mismatch for %s: got %s %s" % (tag, n0, n2))
        if space not in (1048576, 16777216):
            fail("unexpected space")
        total_hits += hits
        print(tag, "norm0", n0, "norm2", n2, "hits", hits, "space", space)
    if total_hits != expect["expected_hits"]:
        fail("hits %s" % total_hits)
    print("PASS")


if __name__ == "__main__":
    main()
