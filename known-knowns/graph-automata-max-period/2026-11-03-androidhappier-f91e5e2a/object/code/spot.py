#!/usr/bin/env python3
"""Spot check (not exhaustive): for each graph6 in a file, Python permax (ALL 2^n rules, no degree pruning, all 2^n
starts) vs Program A (totF) and Program B (totBgo) run on that single graph. Usage: spot.py <totF> <totBgo> <g6file>"""
import sys, subprocess, re
sys.path.insert(0, __import__('os').path.dirname(__file__)); import stepper
A, B, F = sys.argv[1:4]; k = mism = 0
def run(cmd, g):
    o = subprocess.run(cmd, input=g + '\n', capture_output=True, text=True).stdout
    return int(re.search(r'maxperiod=(\d+)', o).group(1))
for g in open(F).read().split():
    n, adj = stepper.g6(g); p = stepper.permax(n, adj)[0]
    a = run([A, '0'], g); b = run([B, 'nbr', '0'], g); k += 1
    print(g, 'A', a, 'B', b, 'python', p, '' if a == b == p else 'MISMATCH'); mism += not (a == b == p)
print('graphs', k, 'mismatches', mism)
