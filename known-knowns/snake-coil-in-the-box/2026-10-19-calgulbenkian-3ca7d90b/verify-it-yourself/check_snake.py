#!/usr/bin/env python3
"""Snake / coil checker for the hypercube Q_n (standard library only).

Usage: python3 check_snake.py OBJECT N KIND PUBLISHED_JSON [--neg]
  KIND is snake or coil. OBJECT is a transition sequence, one base-36 digit per step
  (digits 0-9, a-z; the coordinate flipped at each step), starting at the vertex 0.
  PUBLISHED_JSON (the-record-we-beat/published.json) holds the table value, calibration records
  (published sequences of this table, with their table lengths) and published class hashes.

Checks (two independent methods):
  A. vertices distinct; each vertex has exactly the path neighbours it should (at most 2, 1 at
     the ends of a snake) among the n single-bit neighbours (induced path / cycle).
  B. the literal definition: distinct vertices and popcount(v_i xor v_j) >= 2 for every pair
     that is not consecutive (cyclically consecutive for a coil).
Length convention: edges = number of transitions (for a coil also the number of vertices).
Also reported: the table page's own symmetry test (first half of the sequence equals the
second half, for even length), the canonical class hash, calibration of this checker on
the published records, and the comparison with the table value.
The negative control (--neg) changes one transition; the result must be valid false.
The last output line is a JSON object.
"""
import sys, json, hashlib


def to_ts(s):
    return [int(c, 36) for c in "".join(s.split())]


def check(ts, n, kind):
    if any(not (0 <= t < n) for t in ts):
        return dict(valid=False, why="coordinate out of range")
    v = [0]
    for t in ts:
        v.append(v[-1] ^ (1 << t))
    if kind == "coil":
        if v[-1] != 0:
            return dict(valid=False, why="coil does not close")
        v = v[:-1]
    m = len(v)
    if len(set(v)) != m:
        return dict(valid=False, why="repeated vertex")
    pos = {x: i for i, x in enumerate(v)}
    for i, x in enumerate(v):
        nb = {pos[x ^ (1 << b)] for b in range(n) if (x ^ (1 << b)) in pos}
        exp = {(i - 1) % m, (i + 1) % m} if kind == "coil" else {j for j in (i - 1, i + 1) if 0 <= j < m}
        if nb != exp:
            return dict(valid=False, why="method A: chord at vertex index %d" % i)
    bad = 0
    for i in range(m):
        vi = v[i]
        for j in range(i + 1, m):
            if kind == "coil" and (j == i + 1 or (i == 0 and j == m - 1)):
                continue
            if kind == "snake" and j == i + 1:
                continue
            if bin(vi ^ v[j]).count("1") < 2:
                bad += 1
    if bad:
        return dict(valid=False, why="method B: %d violating pairs" % bad)
    return dict(valid=True, length=len(ts), vertices=m)


def half_symmetric(ts):
    L = len(ts)
    h = L // 2
    return L % 2 == 0 and all(ts[i] == ts[i + h] for i in range(h))


def canon(ts, kind):
    """First-appearance coordinate relabelling, minimised over reversal (and rotation for coils)."""
    def relabel(s):
        mp = {}
        out = []
        for t in s:
            if t not in mp:
                mp[t] = len(mp)
            out.append(mp[t])
        return tuple(out)
    best = None
    for s in (ts, ts[::-1]):
        if kind == "coil":
            for r in range(len(s)):
                c = relabel(s[r:] + s[:r])
                if best is None or c < best:
                    best = c
        else:
            c = relabel(s)
            if best is None or c < best:
                best = c
    return hashlib.sha256(bytes(best)).hexdigest()[:16]


def main():
    path, n, kind, pub = sys.argv[1], int(sys.argv[2]), sys.argv[3], json.load(open(sys.argv[4]))
    ts = to_ts(open(path).read())
    res = {"file": path.split("/")[-1], "n": n, "kind": kind}
    if "--neg" in sys.argv:
        k = len(ts) // 3
        ts[k] = (ts[k] + 1) % n
        res["negative_control"] = "transition %d changed" % k
        r = check(ts, n, kind)
        res.update(r)
        print(json.dumps(res))
        return 0
    r = check(ts, n, kind)
    res.update(r)
    if not r["valid"]:
        print(json.dumps(res)); return 0
    res["half_period_symmetric_per_table_page_test"] = half_symmetric(ts)
    res["table_value"] = pub["table_value"]
    res["table_value_source"] = pub["table_value_source"]
    if pub["table_value"] is not None:
        res["length_minus_table_value"] = r["length"] - pub["table_value"]
    if pub.get("other_published_values"):
        res["other_published_values"] = pub["other_published_values"]
    # calibration: the same checker on published records of the same table
    cal = []
    for rec in pub["calibration"]:
        rr = check(to_ts(rec["ts"]), rec["n"], rec["kind"])
        cal.append({"id": rec["id"], "n": rec["n"], "kind": rec["kind"], "table_length": rec["table_length"],
                    "valid": rr["valid"], "length": rr.get("length"),
                    "reproduces_table_length": bool(rr["valid"] and rr["length"] == rec["table_length"]),
                    "half_period_symmetric": half_symmetric(to_ts(rec["ts"]))})
    res["calibration"] = cal
    res["calibration_all_reproduce"] = all(c["reproduces_table_length"] for c in cal) and bool(cal)
    if pub.get("published_classes"):
        c = canon(ts, kind)
        res["canonical_class_hash"] = c
        same = [p for p in pub["published_classes"] if p["canon"] == c]
        res["published_classes_compared"] = len(pub["published_classes"])
        res["published_classes_with_same_canonical_hash"] = [p["source"] for p in same]
    print(json.dumps(res))
    return 0


sys.exit(main())
