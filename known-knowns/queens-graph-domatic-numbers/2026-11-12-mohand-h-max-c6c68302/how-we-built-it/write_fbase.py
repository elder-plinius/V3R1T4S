"""Write the base formula of one encoding as a DIMACS file, in a few seconds and without any solver: the encoder's
formula without the clauses of its implied counting constraint (the clauses that mention a variable belonging to no
class), in the encoder's order, with the encoder's variable count in the header. It is the file called Fbase.cnf
elsewhere (stage_b2.py writes the same file before its long final step); its sha256 is printed so that it can be
compared with the certificate. Standard library only (the encoders import nothing else).
Usage: python write_fbase.py module n kind K M out.cnf sets5.txt sets6.txt"""
import hashlib, importlib, sys

mod, n, kind, K, M, out = sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
sets = [tuple(sorted(map(int, l.split()))) for p in sys.argv[7:] for l in open(p) if l.strip()]
_m = importlib.import_module(mod)
Enc = getattr(_m, 'Enc', None) or getattr(_m, 'Enc2')
E = Enc(n, kind, K, M, sets)
N = n * n
all_class = set()
for c in range(K):
    if hasattr(E, 'class_vars'):
        V = list(E.class_vars(c))
    else:
        V = [E.X[v][c] for v in range(N)] + [E.CNT[c][i][m] for i in range(1, N + 1) for m in range(1, M + 1) if E.CNT[c][i][m]] + list(E.ZS[c]) + list(E.OCC[c])
    all_class |= set(V)
base = [cl for cl in E.clauses if all(abs(l) in all_class for l in cl)]
text = 'p cnf %d %d\n' % (E.nv, len(base)) + ''.join(' '.join(map(str, cl)) + ' 0\n' for cl in base)
with open(out, 'x', newline='\n') as f:          # 'x': refuses to overwrite an existing file
    f.write(text)
print('%s: encoder %d clauses, base formula %d clauses written to %s' % (mod, len(E.clauses), len(base), out))
print('sha256 %s' % hashlib.sha256(text.encode()).hexdigest())
