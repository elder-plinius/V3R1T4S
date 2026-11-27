#!/usr/bin/env python
"""Driver: compute a(28) mod p for a list of proven primes, in parallel worker
processes; then CRT. Run A: normal (row-major) sweep. Usage:
  python run_n28.py <primes_file> <outfile> [max_workers]
Each worker writes "<p> <residue>" lines to <outfile> as they complete (checkpoint).
"""
import os
import sys
import time
from multiprocessing import Process
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mdp_dp_col import run_dp_col as run_dp  # noqa: E402
import numpy as np  # noqa: E402


def worker(p, outfile):
    t0 = time.time()
    r = run_dp(28, np.int64, p)
    with open(outfile, "a") as f:
        f.write(f"{p} {r} {time.time()-t0:.0f}s\n")
    print(f"p={p} done in {time.time()-t0:.0f}s: {r}", flush=True)


def main():
    primes = [int(x) for x in open(sys.argv[1]).read().split()]
    outfile = sys.argv[2]
    maxw = int(sys.argv[3]) if len(sys.argv) > 3 else 7
    pass  # never truncate: this is a checkpoint file (resume-safe)
    procs = []
    for p in primes:
        while len([q for q in procs if q.is_alive()]) >= maxw:
            time.sleep(2)
        pr = Process(target=worker, args=(p, outfile))
        pr.start()
        procs.append(pr)
        print(f"launched p={p}", flush=True)
    for pr in procs:
        pr.join()
    print("ALL DONE", flush=True)


if __name__ == "__main__":
    main()
