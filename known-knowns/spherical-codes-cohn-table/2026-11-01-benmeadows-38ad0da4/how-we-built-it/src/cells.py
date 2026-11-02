"""List the slice: d in 25..32, three-field rows of /plain, d+2 <= N <= 3d,
minus every (d, N) named in the claims file (any state)."""
import json, re, os
ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data")


def table():
    T = {}
    for line in open(os.path.join(ROOT, "spherical-codes.org_plain")):
        p = line.strip().split(",")
        if len(p) >= 3 and p[0].isdigit():
            T[(int(p[0]), int(p[1]))] = p
    return T


def claimed():
    C = set()
    for x in json.load(open(os.path.join(ROOT, "claims_spherical-codes-cohn-table.json"))):
        if "spherical" not in x["title"]:
            continue
        for a, b in re.findall(r"\((\d+),\s*(\d+)\)", x["title"]):
            C.add((int(a), int(b)))
    return C


def cells():
    T, C = table(), claimed()
    out = []
    for (d, N), p in sorted(T.items()):
        if 25 <= d <= 32 and len(p) == 3 and d + 2 <= N <= 3 * d and (d, N) not in C:
            out.append((d, N, p[2]))
    return out


if __name__ == "__main__":
    c = cells()
    print(len(c), sorted(claimed()))
    for x in c:
        print(*x)
