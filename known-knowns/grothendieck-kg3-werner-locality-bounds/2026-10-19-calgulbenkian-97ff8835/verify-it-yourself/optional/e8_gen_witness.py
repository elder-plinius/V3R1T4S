#!/usr/bin/env python3
"""Builder-side generator (needs pulp with CBC): an explicit sign vector b with ||A b||_1 = 6104 for the
matrix in the MATLAB file, found by integer programming at a dominant vector w whose dual bound is 6104.
usage: e8_gen_witness.py MATFILE OUTFILE c1 c2 c3 c4 c5 c6 c7 c8
Output: 120 lines 'n1 .. n8 b' (positive-root coordinates in the simple-root basis, b in {-1,1})."""
import sys, pulp
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import e8_check as E
mat, out = sys.argv[1], sys.argv[2]
c = [int(x) for x in sys.argv[3:11]]
A, _ = E.load_matrix(mat)
P, S, G, C, Ci, base = E.identify(A)
nw = [2 * sum(Ci[a][b] * c[b] for b in range(8)) for a in range(8)]
xs = [2 * sum(p[k] * c[k] for k in range(8)) for p in P]
prob = pulp.LpProblem('w', pulp.LpMaximize)
y = [pulp.LpVariable('y%d' % i, cat='Binary') for i in range(120)]     # b_i = 2 y_i - 1
fp = [abs(3 * x - 13) for x in xs]
fm = [abs(3 * x + 13) for x in xs]
prob += pulp.lpSum(fm[i] + (fp[i] - fm[i]) * y[i] for i in range(120))
for k in range(8):
    prob += pulp.lpSum(P[i][k] * (2 * y[i] - 1) for i in range(120)) == nw[k]
prob.solve(pulp.PULP_CBC_CMD(msg=0))
print(pulp.LpStatus[prob.status])
b = [2 * round(y[i].value()) - 1 for i in range(120)]
# check on the object matrix itself (raw signs S)
braw = [S[j] * b[j] for j in range(120)]
Ab = [sum(A[i][j] * braw[j] for j in range(120)) for i in range(120)]
print('||A b||_1 =', sum(abs(v) for v in Ab))
open(out, 'w').write("\n".join(" ".join(str(x) for x in P[j]) + " " + str(b[j]) for j in range(120)) + "\n")
