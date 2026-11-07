#!/usr/bin/env python3
"""Third, pure-Python exhaustive reproduction of a(1..8) (all 2^n rules, all starts) from geng -cq n."""
import sys, subprocess, os
sys.path.insert(0, os.path.dirname(__file__)); import stepper
geng = sys.argv[1]
for n in range(1, int(sys.argv[2]) + 1):
    gs = subprocess.run([geng, '-cq', str(n)], capture_output=True, text=True).stdout.split()
    best = (0,)
    for g in gs:
        nn, adj = stepper.g6(g); m = stepper.permax(nn, adj)
        if m[0] > best[0]: best = (m[0], g, m[1], m[2])
    print(f'n={n} graphs={len(gs)} a(n)={best[0]} witness={best[1:]}', flush=True)
