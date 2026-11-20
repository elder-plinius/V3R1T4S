"""Writes the variable map of an encoding as JSON: which variable number stands for what. The map only gives NAMES to
variable numbers; formula_audit.py then rebuilds, from the definition of the problem and these names alone, the
complete list of clauses the base formula must consist of, and compares it with the DIMACS file. If a name were
wrong, that comparison would fail.
Usage: python dump_varmap.py module n kind K M out.json sets5.txt sets6.txt"""
import importlib, json, sys

mod_name, n, kind, K, M, out = sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
sets = [tuple(sorted(map(int, l.split()))) for p in sys.argv[7:] for l in open(p) if l.strip()]
mod = importlib.import_module(mod_name)
Enc = getattr(mod, 'Enc', None) or getattr(mod, 'Enc2')
E = Enc(n, kind, K, M, sets)
N = n * n
m = {'module': mod_name, 'n': n, 'kind': kind, 'K': K, 'M': M, 'nv': E.nv, 'sets': [list(S) for S in sets],
     'X': E.X,                                                     # X[v][c]: square v (= row*n + column) is in class c
     'ZS': E.ZS}                                                   # ZS[c][j]: class c contains every square of sets[j]
if hasattr(E, 'CNT'):                                              # encoding 1
    m['CNT'] = [[[E.CNT[c][i][mm] for mm in range(M + 1)] for i in range(N + 1)] for c in range(K)]   # 0 = no variable (constant)
    m['OCC'] = E.OCC                                               # OCC[c][l]: class c has a square on line l
    m['lines'] = E.lines                                           # the squares of line l
else:                                                              # encoding 2
    m['CNT'] = [[[0] * (M + 1)] + [[0] + [E.R[c][i][mm] for mm in range(1, M + 1)] for i in range(1, N + 1)] for c in range(K)]
    m['Q'] = E.Q                                                   # Q[c][v]: class c has a square with index < v
json.dump(m, open(out, 'w'))
print('%s: %d variables named in %s' % (mod_name, E.nv, out))
