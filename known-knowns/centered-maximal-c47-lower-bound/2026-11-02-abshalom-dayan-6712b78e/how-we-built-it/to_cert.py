#!/usr/bin/env python3
# Round a float atom list to dyadic rationals with BITS fractional bits. Usage: to_cert.py IN.cfg OUT.json [BITS]
# Output integers are numerators over 2^BITS. Atoms are reduced into the cell. Atoms at equal positions are merged.
import sys, json
bits = int(sys.argv[3]) if len(sys.argv) > 3 else 30
S = 1 << bits
L = [l.split() for l in open(sys.argv[1]) if l.strip() and not l.startswith('#')]
Lx, Ly = round(float(L[0][0])*S), round(float(L[0][1])*S)
at = {}
for x, y, m in L[1:]:
    k = (round(float(x)*S) % Lx, round(float(y)*S) % Ly); at[k] = at.get(k, 0) + round(float(m)*S)
json.dump(dict(bits=bits, Lx=Lx, Ly=Ly, atoms=[[a, b, m] for (a, b), m in sorted(at.items())]), open(sys.argv[2], 'w'))
print("atoms", len(at))
