"""Exhaust two named multiplier families at length 70.

Both sequences are constant on the orbits of H, for each listed H.
A hit is a pair whose periodic autocorrelations sum to -2 at every nonzero shift.
"""

N = 70
ROOTS = ((1, 0), (0, 1), (-1, 0), (0, -1))
GROUPS = (
    (1, 3, 9, 11, 13, 17, 27, 29, 33, 39, 47, 51),
    (1, 9, 11, 23, 29, 37, 39, 43, 51, 53, 57, 67),
)


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


def expand(assign, orbs):
    seq = [0] * N
    for val, orb in zip(assign, orbs):
        for p in orb:
            seq[p] = val
    return seq


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
    n0 = n1 = n2 = 0
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
        elif nrm == 1:
            n1 += 1
        elif nrm == 2:
            n2 += 1
        else:
            continue
        key = paf_key(expand(assign, orbs))
        (bucket0 if nrm == 0 else bucket2).setdefault(key, assign)
    hits = 0
    for key in bucket2:
        if needed(key) in bucket0:
            hits += 1
    print("H", group, "order", len(group), "contains_-1", 69 in group)
    print("n_orbits", len(orbs), "space", total)
    print("norm0", n0, "norm1", n1, "norm2", n2)
    print("unique_paf0", len(bucket0), "unique_paf2", len(bucket2), "hits", hits)
    return hits


def main():
    total_hits = 0
    for group in GROUPS:
        total_hits += search(group)
    print("TOTAL_HITS", total_hits)


if __name__ == "__main__":
    main()
