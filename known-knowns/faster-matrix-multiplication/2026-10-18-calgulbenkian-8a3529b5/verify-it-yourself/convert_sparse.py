#!/usr/bin/env python3
"""Lossless conversion of a scheme file between dense rows and "sparse_flat_pairs", standard library only.

Usage:
  python3 convert_sparse.py to-sparse DENSE.json SPARSE.json
  python3 convert_sparse.py to-dense  SPARSE.json DENSE.json
  python3 convert_sparse.py compare    A.json B.json      (either encoding; entry-by-entry comparison)

A scheme file holds "n": [n1, n2, n3], "m" and the lists "u", "v", "w" (one row per term). Dense rows have length
n1*n2 (u), n2*n3 (v) and n3*n1 (w). In "sparse_flat_pairs" a row is [index, value, index, value, ...] with the
indices into the dense row in increasing order and zero entries left out; "n" and "m" are kept and the key
"encoding": "sparse_flat_pairs" is added. This is the encoding that check_fmm_fast.py reads.
"""
import json
import sys


def lengths(n):
    n1, n2, n3 = n
    return {"u": n1 * n2, "v": n2 * n3, "w": n3 * n1}


def to_dense_rows(d):
    """Return {"u": [...], "v": [...], "w": [...]} as lists of dense integer rows, whatever the encoding."""
    enc = d.get("encoding")
    out = {}
    for key, length in lengths(d["n"]).items():
        rows = []
        for row in d[key]:
            if enc == "sparse_flat_pairs":
                if len(row) % 2:
                    raise ValueError(key + ": sparse row of odd length")
                dense = [0] * length
                seen = set()
                for a, x in zip(row[0::2], row[1::2]):
                    if not isinstance(a, int) or isinstance(a, bool) or not 0 <= a < length or a in seen:
                        raise ValueError(key + ": bad or repeated index %r" % (a,))
                    seen.add(a)
                    dense[a] = x
                rows.append(dense)
            elif enc is None:
                if len(row) != length:
                    raise ValueError(key + ": dense row of length %d, expected %d" % (len(row), length))
                rows.append(list(row))
            else:
                raise ValueError("unknown encoding %r" % (enc,))
        if len(rows) != d["m"]:
            raise ValueError(key + ": %d rows, m = %d" % (len(rows), d["m"]))
        out[key] = rows
    return out


def to_sparse(d):
    if d.get("encoding") is not None:
        raise ValueError("input is already encoded")
    dense = to_dense_rows(d)
    new = {}
    for k, val in d.items():
        new[k] = val
        if k == "m":
            new["encoding"] = "sparse_flat_pairs"
    for key in ("u", "v", "w"):
        new[key] = [[t for a, x in enumerate(row) if x != 0 for t in (a, x)] for row in dense[key]]
    return new


def to_dense(d):
    dense = to_dense_rows(d)
    new = {k: v for k, v in d.items() if k != "encoding"}
    for key in ("u", "v", "w"):
        new[key] = dense[key]
    return new


def compare(a, b):
    if a["n"] != b["n"] or a["m"] != b["m"]:
        return "FAIL: n or m differ"
    da, db = to_dense_rows(a), to_dense_rows(b)
    entries = 0
    for key in ("u", "v", "w"):
        for ra, rb in zip(da[key], db[key]):
            for x, y in zip(ra, rb):
                entries += 1
                if x != y:
                    return "FAIL: an entry of %s differs" % key
    return "SAME: n=%s m=%d, %d entries compared, 0 differ" % (a["n"], a["m"], entries)


def main(argv):
    if len(argv) < 4 or argv[1] not in ("to-sparse", "to-dense", "compare"):
        print(__doc__)
        return 2
    with open(argv[2]) as f:
        a = json.load(f)
    if argv[1] == "compare":
        with open(argv[3]) as f:
            b = json.load(f)
        msg = compare(a, b)
        print(msg)
        return 0 if msg.startswith("SAME") else 1
    out = to_sparse(a) if argv[1] == "to-sparse" else to_dense(a)
    with open(argv[3], "w") as f:
        f.write(json.dumps(out, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
