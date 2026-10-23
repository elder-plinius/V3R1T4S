#!/usr/bin/env python3
"""Method used to derive object/scu_files_with_N-1_rows.csv (stdlib only).
Input: a directory holding the extracted https://packomania.com/scu/txt/scu_coords.tar.gz
(not shipped; download it yourself; sha256/Last-Modified in SOURCES.csv).
A coordinate row is a line whose first token is an integer index followed by >= 3 numbers;
header lines start with '#'. Files with exactly N-1 such rows are listed; the remaining index
line (always N) is blank in every case.  Usage: sweep_rowcount.py <coords_dir>"""
import os, sys
d = sys.argv[1]; print("N,coordinate_rows,blank_index"); odd = []
for N in range(1, 1001):
    rows = [l.split() for l in open(os.path.join(d, "scu%d.txt" % N))]
    rows = [r for r in rows if r and r[0].isdigit()]
    full = [r for r in rows if len(r) >= 4]; blank = [r[0] for r in rows if len(r) == 1]
    if len(full) == N - 1: print("%d,%d,%s" % (N, N - 1, " ".join(blank)))
    elif len(full) != N: odd.append((N, len(full)))
print("other row-count anomalies:", odd, file=sys.stderr)
