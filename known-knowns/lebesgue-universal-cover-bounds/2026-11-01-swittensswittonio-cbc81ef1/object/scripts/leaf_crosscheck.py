# Independent re-evaluation (mpmath.iv, 200 bit; different code from the C# Iv engine) of the EXACT certificate chosen by the C# checker for sampled leaves,
# plus a Monte-Carlo validity test of the polygon area bound inside the leaf box.
import json, sys, math, random
from mpmath import iv, mpf
import numpy as np
sys.path.insert(0, 'code')
import gen_tables as gt
iv.prec = 200
excl = json.load(open('code/tables/author_exclusions.json'))
cache = {}
def pts(kind, n, s, variant):
    key = (kind, n, s, variant)
    if key in cache: return cache[key]
    if kind == 'disk': P = gt.disk(s)
    else:
        P, _ = gt.reul(n, s)
        if variant == 1:
            drop = set(excl['%d,%d' % (n, s)]['drop_indices']); P = [p for i, p in enumerate(P) if i not in drop]
    cache[key] = P; return P
PI5_TXT = '0.6283185307179586'
def ivdec(t, top=None):
    v = iv.mpf(t)
    return v
def run(rec, tau=iv.mpf('0.834')):
    lo, hi = rec['lo'], rec['hi']
    box = []
    for k in range(5):
        a = iv.mpf(lo[k]); b = iv.mpf(hi[k])
        if k == 2 and hi[k] == PI5_TXT: b = iv.pi / 5
        box.append(iv.mpf([a.a, b.b]))
    X3, Y3, PSI, X5, Y5 = box
    c = [(mpf(lo[k]) + mpf(hi[k])) / 2 for k in range(5)]
    dpts = pts('disk', 0, rec['ds'], 0); p3 = pts('reul', 3, rec['r3'], rec['variant']); p5 = pts('reul', 5, rec['r5'], rec['variant'])
    nd, n3 = len(dpts), len(p3)
    CB, SB = iv.cos(PSI), iv.sin(PSI)
    cc, sc = iv.cos(iv.mpf(c[2])), iv.sin(iv.mpf(c[2]))
    def vbox(i):
        if i < nd: return dpts[i]
        i -= nd
        if i < n3: q = p3[i]; return (X3 + q[0], Y3 + q[1])
        q = p5[i - n3]; return (X5 + q[0] * CB - q[1] * SB, Y5 + q[0] * SB + q[1] * CB)
    def vcen(i):
        if i < nd: return dpts[i]
        i -= nd
        if i < n3: q = p3[i]; return (iv.mpf(c[0]) + q[0], iv.mpf(c[1]) + q[1])
        q = p5[i - n3]; return (iv.mpf(c[3]) + q[0] * cc - q[1] * sc, iv.mpf(c[4]) + q[0] * sc + q[1] * cc)
    idx = rec['cand']; m = len(idx)
    VB = [vbox(i) for i in idx]; VC = [vcen(i) for i in idx]
    def area(V):
        s = iv.mpf(0)
        for i in range(len(V)):
            a = V[i]; b = V[(i + 1) % len(V)]; s += a[0] * b[1] - b[0] * a[1]
        return s / 2
    # radii
    rad = [max(iv.mpf(hi[k]).b - c[k], c[k] - iv.mpf(lo[k]).a) for k in range(5)]
    if hi[2] == PI5_TXT: rad[2] = (iv.pi / 5).b - c[2] if (iv.pi / 5).b - c[2] > rad[2] else rad[2]
    # eps
    def eps(i):
        if i < nd: return iv.mpf(0)
        i -= nd
        if i < n3: return iv.sqrt(iv.mpf(rad[0]) ** 2 + iv.mpf(rad[1]) ** 2)
        q = p5[i - n3]; return iv.sqrt(iv.mpf(rad[3]) ** 2 + iv.mpf(rad[4]) ** 2) + iv.sqrt(q[0] ** 2 + q[1] ** 2) * rad[2]
    EP = [eps(i) for i in idx]
    Sc = area(VC); Sb = area(VB)
    E = iv.mpf(0)
    for i in range(m):
        a = VC[(i + 1) % m]; b = VC[i - 1]
        E += EP[i] * iv.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) / 2 + EP[i] * EP[(i + 1) % m] / 2
    lowP = (Sc - E).a
    D = [iv.mpf(0)] * 5
    for pos, i in enumerate(idx):
        if i < nd: continue
        nx = VB[(pos + 1) % m]; pv = VB[pos - 1]; dx = nx[0] - pv[0]; dy = nx[1] - pv[1]
        if i < nd + n3: D[0] += dy / 2; D[1] -= dx / 2
        else:
            q = p5[i - nd - n3]; D[3] += dy / 2; D[4] -= dx / 2
            ddx = -(SB * q[0]) - CB * q[1]; ddy = CB * q[0] - SB * q[1]; D[2] += (ddx * dy - ddy * dx) / 2
    var = sum((max(abs(D[k].a), abs(D[k].b)) * rad[k] for k in range(5)), iv.mpf(0))
    lowMV = (Sc - var).a; lowD = Sb.a
    lower = max(lowP, lowMV, lowD)
    return {'py_lower': float(lower), 'cs_lower': rec['lower'], 'pert': float(lowP), 'mv': float(lowMV), 'direct': float(lowD), 'm': m}
if __name__ == '__main__':
    recs = [json.loads(l) for l in open(sys.argv[1])]
    nmc = int(sys.argv[2]) if len(sys.argv) > 2 else 400
    worst = 9; bad = 0; rows = []
    for rec in recs:
        r = run(rec)
        # Monte Carlo: polygon area (float, exact sample points from mp at 50 digits) over random z in box must be >= cs_lower (bound validity)
        lo = [float(x) for x in rec['lo']]; hi = [float(x) for x in rec['hi']]
        nd = len(pts('disk', 0, rec['ds'], 0)); p3 = pts('reul', 3, rec['r3'], rec['variant']); p5 = pts('reul', 5, rec['r5'], rec['variant'])
        mid = lambda p: (float(p[0].mid), float(p[1].mid))
        D = np.array([mid(p) for p in pts('disk', 0, rec['ds'], 0)]); A3 = np.array([mid(p) for p in p3]); A5 = np.array([mid(p) for p in p5])
        allp = np.vstack([D, A3, A5]); idx = rec['cand']; mc_min = 9
        for _ in range(nmc):
            z = [random.uniform(lo[k], hi[k]) for k in range(5)]
            P = np.vstack([D, A3 + [z[0], z[1]], A5 @ np.array([[math.cos(z[2]), math.sin(z[2])], [-math.sin(z[2]), math.cos(z[2])]]) + [z[3], z[4]]])
            poly = P[idx]; x, y = poly[:, 0], poly[:, 1]
            S = 0.5 * float(np.sum(x * np.roll(y, -1) - np.roll(x, -1) * y)); mc_min = min(mc_min, S)
        ok = r['py_lower'] > 0.834 and mc_min >= rec['lower'] - 1e-12 and r['py_lower'] >= rec['lower'] - 1e-10
        bad += (not ok); worst = min(worst, r['py_lower'] - 0.834)
        rows.append({**r, 'leaf': rec['leaf'], 'kind': rec['kind'], 'mc_min_area': mc_min, 'ok': ok})
        print('%-60s m=%3d cs=%.12f py=%.12f mcmin=%.12f %s %s' % (rec['leaf'][-34:], r['m'], rec['lower'], r['py_lower'], mc_min, rec['kind'], 'OK' if ok else 'MISMATCH'), flush=True)
    print('leaves', len(recs), 'mismatches', bad, 'worst py slack over 0.834: %.3e' % worst)
    json.dump(rows, open(sys.argv[3] if len(sys.argv) > 3 else 'out/leaf_crosscheck.json', 'w'), indent=0)
