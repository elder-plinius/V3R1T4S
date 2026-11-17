#!/usr/bin/env python
"""Broken-profile DP for monomer-dimer matchings on the n x n grid (OEIS A028420).

State at cut before cell (i, j): n-bit mask; bit k means cell (i, k) is covered for
k >= j (by a horizontal from (i, k-1), only k == j, or a vertical from (i-1, k)), and
cell (i+1, k) is covered for k < j (vertical from (i, k)).
Transitions at cell (i, j):
  bit j set   -> forced  T = S & ~(1 << j)
  bit j clear -> monomer T = S | vertical T = S | (1 << j) (not on the last row)
              -> horizontal T = S | (1 << (j+1)) (not in the last column; source bit j+1
                 must be clear, which the target view enforces)
Answer = dp[0] after the last cell.
Vectorized with reshape views (axis 1 = bit j; finer 4-D view for the horizontal term) —
no gathers, no mask arrays.

Usage:
  python mdp_dp.py exact <n>   exact big-integer a(n) (object dtype; n <= ~20 practical)
  python mdp_dp.py mod <n> <p> a(n) mod p (int64 numpy)
  python mdp_dp.py gate        exact gate n = 0..20 against data/b028420.txt
"""
import sys
import time
import numpy as np


def run_dp(n, dtype, fill_last_row_zero):
    size = 1 << n
    dp = np.zeros(size, dtype=dtype)
    dp[0] = 1
    for i in range(n):
        last_row = i == n - 1
        for j in range(n):
            v = dp.reshape(-1, 2, 1 << j)
            bs = v[:, 1, :]          # sources: bit j set    -> forced to bit-clear target
            bc = v[:, 0, :]          # sources: bit j clear  -> monomer/vertical/horizontal
            new = np.empty_like(v)
            new[:, 0, :] = bs                        # forced
            new[:, 0, :] += bc                       # + monomer (in-place, no temp)
            if last_row:
                new[:, 1, :] = 0
            else:
                new[:, 1, :] = bc                    # vertical (no .copy: bc is a view of dp)
            if j < n - 1:
                # horizontal: source bit j clear AND bit j+1 clear; target bit j clear,
                # bit j+1 set. 4-D view: (higher, bit j+1, bit j, low j bits).
                w = new.reshape(-1, 2, 2, 1 << j)
                sw = bc.reshape(-1, 2, 1 << j)
                w[:, 1, 0, :] += sw[:, 0, :]
            dp = new.reshape(-1)
            if fill_last_row_zero:
                np.remainder(dp, fill_last_row_zero, out=dp)  # in-place mod
            del bs, bc, v
    return int(dp[0])


def main():
    t0 = time.time()
    mode = sys.argv[1]
    if mode == "exact":
        n = int(sys.argv[2])
        print(run_dp(n, object, 0), flush=True)
        print(f"[{time.time()-t0:.0f}s]", file=sys.stderr)
    elif mode == "mod":
        n, p = int(sys.argv[2]), int(sys.argv[3])
        print(run_dp(n, np.int64, p), flush=True)
        print(f"[{time.time()-t0:.0f}s]", file=sys.stderr)
    elif mode == "gate":
        pub = {}
        for line in open("data/b028420.txt"):
            s = line.split()
            if len(s) == 2:
                pub[int(s[0])] = int(s[1])
        ok = True
        for n in range(0, 21):
            v = run_dp(n, object, 0)
            good = v == pub.get(n)
            print(f"n={n}: {v} {'OK' if good else 'FAIL vs ' + str(pub.get(n))}", flush=True)
            ok = ok and good
            if not good:
                print("GATE FAIL")
                return 1
        print("GATE PASS (n=0..20)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
