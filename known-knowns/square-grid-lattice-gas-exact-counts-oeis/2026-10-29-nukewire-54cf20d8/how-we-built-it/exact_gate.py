#!/usr/bin/env python
"""The full EXACT n = 21..27 gate the criterion panelist required: for each n, compute
a(n) by full multi-prime CRT with Run B's column-sweep code and compare EXACTLY with
the published b-file value. Checkpoints per (n, prime) to code/exact_gate_residues.txt.

Usage: python exact_gate.py            (sequential; hours — checkpoints make it resumable)
       python exact_gate.py <n>       (single n)
"""
import os
import sys
import time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mdp_dp_col import run_dp_col  # noqa: E402
from sympy.ntheory.modular import crt  # noqa: E402


def primes_for(n_value, used):
    """~ceil(bits(3^(n^2))/61)+1 proven primes disjoint from both runs' sets."""
    from sympy import nextprime
    import math
    need = int(math.ceil(n_value * n_value * math.log2(3))) + 62
    out = []
    p = 2305843009213695600
    while sum(x.bit_length() for x in out) < need:
        p = nextprime(p)
        if p not in used:
            out.append(p)
    return out


def main():
    pub = {}
    for line in open("data/b028420_live.txt"):
        s = line.split()
        if len(s) == 2:
            pub[int(s[0])] = int(s[1])
    used = set()
    for f in ("../2026-10-28-0734/code/primesB.txt",):
        used.update(int(x) for x in open(f).read().split())
    # Run A's primes too (from its residues file via the sibling's output)
    used.update(int(x) for x in """2305843009213693967 2305843009213693973 2305843009213694009 2305843009213694017
2305843009213694087 2305843009213694149 2305843009213694173 2305843009213694207
2305843009213694257 2305843009213694317 2305843009213694323 2305843009213694381
2305843009213694411 2305843009213694429 2305843009213694443 2305843009213694491
2305843009213694497 2305843009213694569 2305843009213694597 2305843009213694683
2305843009213694791""".split())
    ck = "code/exact_gate_residues.txt"
    ns = [int(sys.argv[1])] if len(sys.argv) > 1 else list(range(21, 28))
    for n in ns:
        primes = primes_for(n, used)
        res = {}
        # resume from checkpoint
        if os.path.exists(ck):
            for line in open(ck):
                s = line.split()
                if len(s) == 3 and s[0] == str(n):
                    res[int(s[1])] = int(s[2])
        for p in primes:
            if p in res:
                continue
            t0 = time.time()
            r = run_dp_col(n, np.int64, p)
            with open(ck, "a", newline="\n") as f:
                f.write(f"{n} {p} {r}\n")
            res[p] = r
            print(f"n={n} p={p}: {r} [{time.time()-t0:.0f}s]", flush=True)
        val, _ = crt(sorted(res), [res[p] for p in sorted(res)])
        ok = int(val) == pub[n]
        print(f"n={n}: CRT {'=' if ok else '!='} published ({len(res)} primes) "
              f"{'OK' if ok else 'FAIL'}", flush=True)
        if not ok:
            print("EXACT GATE FAIL at n =", n)
            return 1
    print("EXACT GATE PASS (n=21..27, full CRT, exact equality)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
