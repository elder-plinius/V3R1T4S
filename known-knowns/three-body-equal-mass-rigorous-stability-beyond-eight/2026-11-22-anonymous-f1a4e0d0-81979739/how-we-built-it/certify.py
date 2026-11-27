"""Interval certificate (PREREG.md C1, C3; PREREG.v2.md C2) for one row of data/ics_971_100_num.txt.

usage: certify.py ROW [r_exp] [shift_vx]
  ROW      global row number (1 = figure-eight)
  r_exp    box half-width 10^-r_exp (default 30)
  shift_vx optional shift of the box centre in vx (known-negative test)
Prints a JSON-ish report; last line "CERT ROW n: PASS" or "CERT ROW n: FAIL (...)".
"""
import sys, time, json
from flint import arb, arb_mat, ctx
from vt3b import integrate, rhs
from ic import load_row, x0_of, G_of

row = int(sys.argv[1])
r_exp = int(sys.argv[2]) if len(sys.argv) > 2 else 30
shift = sys.argv[3] if len(sys.argv) > 3 else '0'
PREC_C, N_C, PREC_B, N_B = [int(x) for x in sys.argv[4:8]] if len(sys.argv) > 7 else (320, 64, 256, 44)
t_start = time.time()
out = {'row': row, 'r': '1e-%d' % r_exp, 'shift_vx': shift, 'prec_centre': PREC_C, 'N_centre': N_C, 'prec_box': PREC_B, 'N_box': N_B}
fails = []


def log(*a):
    print(*a, flush=True)


# ---------- centre run (high precision, state only) ----------
ctx.prec = PREC_C
(vx, vy, T, Ts), raw = load_row(row)
vx = vx + arb(shift)
th = T / 2
xc = [vx, vy, th]
Xc, _, ns_c = integrate(x0_of(vx, vy), [], th, N=N_C)
Gc = G_of(Xc)
out['centre_steps'] = ns_c
out['G_centre'] = [g.str(5, radius=True) for g in Gc]
log('centre run', ns_c, 'steps', out['G_centre'], '%.0fs' % (time.time() - t_start))

# ---------- box run (state + 12 tangents) ----------
ctx.prec = PREC_B
r = arb('1e-%d' % r_exp)
box = [x + arb(0, r) for x in xc]
I12 = [[arb(1) if i == j else arb(0) for j in range(12)] for i in range(12)]
Xb, Tb, ns_b = integrate(x0_of(box[0], box[1]), I12, th, N=N_B,
                         t_end_interval=(-r, r), log=log)
out['box_steps'] = ns_b
log('box run', ns_b, 'steps %.0fs' % (time.time() - t_start))
# A[i][p] = d state_i / d initial_p
A = [[Tb[p][i] for p in range(12)] for i in range(12)]

# ---------- C1: Krawczyk ----------
Y = Xb
gradG = [[arb(0)] * 12 for _ in range(3)]
gradG[0][2] = arb(1)
gradG[1][3] = arb(1)
gradG[2][0] = Y[6] - Y[10]
gradG[2][1] = Y[7] - Y[11]
gradG[2][6] = Y[0]
gradG[2][10] = -Y[0]
gradG[2][7] = Y[1]
gradG[2][11] = -Y[1]
dx0_dvx = [0, 0, 0, 0, 0, 0, 1, 0, -2, 0, 1, 0]
dx0_dvy = [0, 0, 0, 0, 0, 0, 0, 1, 0, -2, 0, 1]
fY, _ = rhs(Y, [])
DG = [[arb(0)] * 3 for _ in range(3)]
for k in range(3):
    for col, d in enumerate([dx0_dvx, dx0_dvy]):
        s = arb(0)
        for i in range(12):
            gi = gradG[k][i]
            if gi == 0 and gi.rad() == 0:
                continue
            for p in range(12):
                if d[p]:
                    s = s + gi * A[i][p] * d[p]
        DG[k][col] = s
    DG[k][2] = sum((gradG[k][i] * fY[i] for i in range(12)), arb(0))
DGm = arb_mat(DG)
C = arb_mat([[x.mid() for x in rr] for rr in DGm.mid().inv().tolist()])
Gcv = arb_mat([[g] for g in Gc])
xhat = arb_mat([[x] for x in xc])
dX = arb_mat([[arb(0, r)] for _ in range(3)])
K = xhat - C * Gcv + (arb_mat([[arb(int(i == j)) for j in range(3)] for i in range(3)]) - C * DGm) * dX
inside = True
kr = []
for i in range(3):
    dev = (K[i, 0] - xc[i]).abs_upper()
    kr.append(float(dev / r))
    if not (dev < r):
        inside = False
out['krawczyk_dev_over_r'] = kr
out['C1_krawczyk_inside'] = inside
if not inside:
    fails.append('C1')
log('C1', inside, kr)

# ---------- C2: trivial block ----------
x0b = x0_of(box[0], box[1])
f0, _ = rhs(x0b, [])
cols = []
cols.append([arb(1), 0, arb(1), 0, arb(1), 0] + [0] * 6)      # e_x
cols.append([0, arb(1), 0, arb(1), 0, arb(1)] + [0] * 6)      # e_y
cols.append([0] * 6 + [arb(1), 0, arb(1), 0, arb(1), 0])      # b_x
cols.append([0] * 6 + [0, arb(1), 0, arb(1), 0, arb(1)])      # b_y
cols.append(list(f0))                                          # f(x0)
rot = []
for c in range(0, 12, 2):
    rot += [-x0b[c + 1], x0b[c]]                               # J (x, y) = (-y, x)
cols.append(rot)
U = [[arb(cols[j][i]) for j in range(6)] for i in range(12)]
best = None
import itertools
for rows in itertools.combinations(range(12), 6):
    d = arb_mat([U[i] for i in rows]).det()
    if not d.contains(0):
        best = (rows, d.str(10, radius=True))
        break
out['C2_minor'] = best
if best is None:
    fails.append('C2')
log('C2', best)

# ---------- C3: reduced monodromy ----------
Am = arb_mat(A)
Jm = arb_mat([[arb(1) if (j == i + 6) else (arb(-1) if (i == j + 6) else arb(0)) for j in range(12)] for i in range(12)])
Ainv = -(Jm * Am.transpose() * Jm)
perm = {0: 4, 1: 5, 2: 2, 3: 3, 4: 0, 5: 1, 6: 10, 7: 11, 8: 8, 9: 9, 10: 6, 11: 7}
Sm = [[arb(0)] * 12 for _ in range(12)]
for i in range(12):
    # S: q1 -> -q3, q2 -> -q2, q3 -> -q1, v1 -> v3, v2 -> v2, v3 -> v1  (new_i = sign * old_perm[i])
    Sm[i][perm[i]] = arb(-1) if i < 6 else arb(1)
Sm = arb_mat(Sm)
M = Sm * Ainv * Sm * Am
out['symplectic_check_maxrad_AinvA_minus_I'] = float(max((Ainv * Am - arb_mat([[arb(int(i == j)) for j in range(12)] for i in range(12)]))[i, j].abs_upper() for i in range(12) for j in range(12)))
p = M.charpoly()
pc = [p[k] for k in range(13)]
from math import comb
c = [sum((pc[k] * comb(k, j) for k in range(j, 13)), arb(0)) for j in range(13)]
out['c0_c7_contain_0'] = all(c[j].contains(0) for j in range(8))
out['c0_c7_maxabs'] = float(max(c[j].abs_upper() for j in range(8)))
# q(lambda) = sum_i c[8+i] (lambda - 1)^i
qc = [arb(0)] * 5
for i in range(5):
    for k in range(i + 1):
        qc[k] = qc[k] + c[8 + i] * comb(i, k) * (-1) ** (i - k)
out['q_coeffs'] = [x.str(12, radius=True) for x in qc]
ok3 = True
res = {}
for name, a in (('a_l3', qc[3]), ('a_l1', qc[1])):
    b = qc[2]
    disc = a * a - 4 * (b - 2)
    if not (disc > 0):
        ok3 = False
        res[name] = 'disc not certified > 0: ' + disc.str(8, radius=True)
        continue
    sq = disc.sqrt()
    s1 = (-a - sq) / 2
    s2 = (-a + sq) / 2
    good = (s1 > -2) and (s2 < 2)
    ok3 = ok3 and bool(good)
    pi2 = 2 * arb.pi()
    w = sorted([(s / 2).acos() / pi2 for s in (s1, s2)], key=lambda z: float(z.mid()))
    res[name] = {'disc': disc.str(10, radius=True), 's': [s1.str(15, radius=True), s2.str(15, radius=True)],
                 'in_(-2,2)': bool(good), 'omega': [x.str(25, radius=True) for x in w]}
out['C3'] = res
out['C3_elliptic_distinct'] = ok3
if not ok3:
    fails.append('C3')
log('C3', json.dumps(res, indent=1))

# ---------- C3': reduced monodromy on U^omega / span(f, R x0) (PREREG.v3) ----------
def vec(lst):
    return arb_mat([[arb(x)] for x in lst])
fx0 = [arb(x) for x in f0]
dH = [-fx0[6 + k] for k in range(6)] + [fx0[k] for k in range(6)]
dL = [arb(0)] * 12
for b_ in range(3):
    xq, yq, ux, uy = x0b[2 * b_], x0b[2 * b_ + 1], x0b[6 + 2 * b_], x0b[7 + 2 * b_]
    dL[2 * b_], dL[2 * b_ + 1], dL[6 + 2 * b_], dL[7 + 2 * b_] = uy, -ux, -yq, xq
dot = lambda a_, b_: sum((arb(x) * arb(y) for x, y in zip(a_, b_)), arb(0))
cf = []   # 8 fixed COM-free vectors: d1 = body1 - body3, d2 = body1 + body3 - 2 body2, in q and v, x and y
for off in (0, 6):
    for ax in (0, 1):
        v1 = [0] * 12; v1[off + ax] = 1; v1[off + 4 + ax] = -1
        v2 = [0] * 12; v2[off + ax] = 1; v2[off + 4 + ax] = 1; v2[off + 2 + ax] = -2
        cf += [v1, v2]
import itertools as _it
bestc = None
for gi, gj in _it.combinations(range(8), 2):
    d_ = dot(dH, cf[gi]) * dot(dL, cf[gj]) - dot(dH, cf[gj]) * dot(dL, cf[gi])
    if bestc is None or abs(float(d_.mid())) > bestc[0]:
        bestc = (abs(float(d_.mid())), gi, gj)
_, gi, gj = bestc
g1, g2 = cf[gi], cf[gj]
W2 = arb_mat([[dot(dH, g1), dot(dH, g2)], [dot(dL, g1), dot(dL, g2)]])
W2inv = W2.inv()
zs = []
for k in range(8):
    if k in (gi, gj):
        continue
    rhs2 = arb_mat([[dot(dH, cf[k])], [dot(dL, cf[k])]])
    ab = W2inv * rhs2
    zs.append([arb(cf[k][i]) - ab[0, 0] * g1[i] - ab[1, 0] * g2[i] for i in range(12)])
cols_fixed = [fx0, rot, cols[0], cols[1], cols[2], cols[3], [arb(x) for x in g1], [arb(x) for x in g2]]
bestz = None
for combo in _it.combinations(range(6), 4):
    Bm = arb_mat([[c_[i] for c_ in ([zs[j] for j in combo] + cols_fixed)] for i in range(12)])
    dm = abs(float(Bm.mid().det().mid()))
    if bestz is None or dm > bestz[0]:
        bestz = (dm, combo)
combo = bestz[1]
Z = [zs[j] for j in combo]
Bm = arb_mat([[c_[i] for c_ in (Z + cols_fixed)] for i in range(12)])
c3p = {'g_pair': [gi, gj], 'z_combo': list(combo)}
try:
    m4 = [[None] * 4 for _ in range(4)]
    for j in range(4):
        y = Bm.solve(M * vec(Z[j]))
        for i in range(4):
            m4[i][j] = y[i, 0]
        c3p.setdefault('other_coords_contain_0', []).append(all(y[i, 0].contains(0) for i in range(6, 12)))
    m4 = arb_mat(m4)
    cp = m4.charpoly()
    a0, a1, a2, a3 = cp[0], cp[1], cp[2], cp[3]
    c3p['q_red'] = [x.str(15, radius=True) for x in (a0, a1, a2, a3)]
    okp = True
    for name, a in (('a3', a3), ('a1', a1)):
        disc = a * a - 4 * (a2 - 2)
        if not (disc > 0):
            okp = False
            c3p[name] = 'disc not certified > 0: ' + disc.str(8, radius=True)
            continue
        sq = disc.sqrt()
        s1, s2 = (-a - sq) / 2, (-a + sq) / 2
        good = bool((s1 > -2) and (s2 < 2))
        okp = okp and good
        w = sorted([(s_ / 2).acos() / (2 * arb.pi()) for s_ in (s1, s2)], key=lambda z_: float(z_.mid()))
        c3p[name] = {'disc': disc.str(10, radius=True), 's': [s1.str(20, radius=True), s2.str(20, radius=True)],
                     'in_(-2,2)': good, 'omega': [x.str(25, radius=True) for x in w]}
except Exception as e:
    okp = False
    c3p['error'] = repr(e)
out["C3prime"] = c3p
out["C3prime_elliptic_distinct"] = okp
if ok3 or okp:
    if 'C3' in fails:
        fails.remove('C3')
        out['C3_note'] = 'C3 (12x12 route) failed on width; C3prime certified (PREREG.v3: either route)'
log("C3'", json.dumps(c3p, indent=1))
# save the monodromy-half enclosure A for the record
json.dump({'A': [[A[i][j].str(30, radius=True) for j in range(12)] for i in range(12)]}, open('A_row%d_r%d_rerun.json' % (row, r_exp), 'w'))

# ---------- consistency with the source's 40-digit frequencies ----------
import os
srcfile = os.environ.get('ANGLES_FILE', '../object/res_eig_angles_row2.txt')
parts = open(srcfile).read().split('i.c. %d\n' % row) if os.path.exists(srcfile) else []
blk = parts[1].split('i.c.')[0] if len(parts) > 1 else 'stability angles: 0 0'
angs = blk.split('stability angles:')[1].split()[:2]
src = sorted([arb(x) for x in angs], key=lambda z: float(z.mid()))
omsrc = out['C3prime']['a3']['omega'] if (okp and isinstance(out['C3prime'].get('a3'), dict)) else (res['a_l3']['omega'] if isinstance(res.get('a_l3'), dict) else None)
if omsrc is not None:
    out['source_omegas'] = angs
    cons = []
    for o_str, s_ in zip(omsrc, src):
        mid = o_str.strip('[]').split('+/-')
        o = arb(mid[0].strip(), mid[1].strip() if len(mid) > 1 else 0)
        cons.append(bool(o.overlaps(s_)) or float(abs(o.mid() - s_.mid())) < 1e-35)
    out['omega_consistent_with_source'] = cons
out['seconds'] = round(time.time() - t_start, 1)
print(json.dumps(out, indent=1))
print('CERT ROW %d: %s' % (row, 'PASS' if not fails else 'FAIL (%s)' % ','.join(fails)))
