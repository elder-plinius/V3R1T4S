#!/usr/bin/env python
"""Run B: TRANSPOSED-SWEEP broken-profile DP for A028420 (monomer-dimer matchings).

Different decomposition from Run A (runs/2026-10-27-0735): the grid is scanned
COLUMN-major — the frontier tracks rows, bit k = row k — which is the bank's own listed
example of a different decomposition ("row vs column sweep"), implemented as separate
code (this file) with its own transition derivation, plus a DISJOINT proven prime set.

State at cut before cell (j, i) in column-major order (column j, row i): n-bit mask;
bit k means cell (k, j) is covered for k >= i (by a vertical from (i-1, k) — only
k == i — or a horizontal from (k, j-1)), and cell (k, j+1) is covered for k < i
(horizontal from (k, j)).
Transitions at cell (j, i):
  bit i set   -> forced  T = S & ~(1 << i)
  bit i clear -> monomer T = S | vertical T = S | (1 << i) (not in the last column)
              -> horizontal T = S | (1 << (i+1)) (not in the last row; bit i+1 clear)
Answer = dp[0] after the last cell.

Usage:
  python mdp_dp_col.py exact <n>   exact big-integer a(n) (object dtype)
  python mdp_dp_col.py mod <n> <p> a(n) mod p (int64)
  python mdp_dp_col.py gate        exact gate n = 0..20 vs data/b028420.txt
"""
import sys
import time
import numpy as np


def run_dp_col(n, dtype, mod):
    size = 1 << n
    dp = np.zeros(size, dtype=dtype)
    dp[0] = 1
    for j in range(n):
        last_col = j == n - 1
        for i in range(n):
            v = dp.reshape(-1, 2, 1 << i)
            bs = v[:, 1, :]
            bc = v[:, 0, :]
            new = np.empty_like(v)
            new[:, 0, :] = bs
            new[:, 0, :] += bc
            if last_col:
                new[:, 1, :] = 0
            else:
                new[:, 1, :] = bc
            if i < n - 1:
                w = new.reshape(-1, 2, 2, 1 << i)
                sw = bc.reshape(-1, 2, 1 << i)
                w[:, 1, 0, :] += sw[:, 0, :]
            dp = new.reshape(-1)
            if mod:
                np.remainder(dp, mod, out=dp)
            del bs, bc, v
    return int(dp[0])


def main():
    t0 = time.time()
    mode = sys.argv[1]
    if mode == "exact":
        print(run_dp_col(int(sys.argv[2]), object, 0), flush=True)
        print(f"[{time.time()-t0:.0f}s]", file=sys.stderr)
    elif mode == "mod":
        print(run_dp_col(int(sys.argv[2]), np.int64, int(sys.argv[3])), flush=True)
        print(f"[{time.time()-t0:.0f}s]", file=sys.stderr)
    elif mode == "gate":
        pub = {}
        for line in open("data/b028420.txt"):
            s = line.split()
            if len(s) == 2:
                pub[int(s[0])] = int(s[1])
        ok = True
        for n in range(0, 21):
            v = run_dp_col(n, object, 0)
            good = v == pub.get(n)
            print(f"n={n}: {'OK' if good else 'FAIL ' + str(v) + ' vs ' + str(pub.get(n))}",
                  flush=True)
            ok = ok and good
            if not good:
                print("GATE FAIL")
                return 1
        print("GATE PASS (n=0..20)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
