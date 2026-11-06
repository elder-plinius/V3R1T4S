#!/usr/bin/env python3
"""Second, separately written checker (numpy, bitmask layout) for Definition 2.1/2.2 of arXiv:2604.08790.
Builds the out-neighbourhood mask of every vertex in every tournament, then for all k-subsets at once
(an array of masks) tests whether some (t, v) with v outside U has U inside its out-neighbourhood."""
import json, sys
import numpy as np
from itertools import combinations

def main(path):
    d = json.load(open(path)); m, k, n = d["m"], d["k"], d["n"]
    A = np.array([[[int(c) for c in row] for row in T] for T in d["tournaments"]], dtype=np.int64)
    assert A.shape == (m, n, n), f"shape {A.shape} != {(m, n, n)}"
    assert np.all(A.diagonal(axis1=1, axis2=2) == 0), "nonzero diagonal"
    assert np.all((A + A.transpose(0, 2, 1))[:, ~np.eye(n, dtype=bool)] == 1), "not a tournament"
    w = (1 << np.arange(n, dtype=np.int64))
    out = (A * w[None, None, :]).sum(axis=2)            # out[t, v] = bitmask of vertices beaten by v in T_t
    U = np.array([sum(1 << u for u in c) for c in combinations(range(n), k)], dtype=np.int64)
    inside = (out[:, :, None] & U[None, None, :]) == U[None, None, :]
    notin = ((U[None, :] >> np.arange(n, dtype=np.int64)[:, None]) & 1) == 0   # [v, U]: v not in U
    dominated = (inside & notin[None, :, :]).any(axis=(0, 1))
    bad = int((~dominated).sum())
    print(f"bitmask checker: m={m} k={k} n={n}: {len(U)} k-subsets, {bad} undominated -> {'PASS' if bad == 0 else 'FAIL'}")
    return bad == 0

if __name__ == "__main__":
    try: ok = main(sys.argv[1])
    except AssertionError as e: print("INVALID:", e); sys.exit(2)
    sys.exit(0 if ok else 1)
