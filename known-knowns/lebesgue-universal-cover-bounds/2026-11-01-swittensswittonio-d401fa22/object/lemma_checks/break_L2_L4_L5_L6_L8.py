# Random / adversarial counterexample searches for L2 (gauge, mirror, rho-period), L4 (erosion), L5 (corner movement),
# L6 (Prop 4.9: core inside every placement + beta <= A), L8 (a-priori exclusion). NUMERICAL evidence only (float64).
import numpy as np, sys, time
from common import *
rng = np.random.default_rng(20261031)
t0 = time.time()
R3, R5 = Rn(3), Rn(5)
def rot(a): c, s = np.cos(a), np.sin(a); return np.array([[c, -s], [s, c]])   # column-vector convention
def rowrot(P, a): return P @ rot(a).T

print("==== L2: gauge reduction, mirror, rho period (point-set hull areas) ====")
worst_gauge = worst_per = worst_mir = 0.0
for trial in range(300):
    # arbitrary rigid motions (some reflecting) of D, B3, B5:  x -> Q_i x + s_i, Q_i in O(2)
    mots = []
    for i in range(3):
        a = rng.uniform(0, 2*np.pi); e = rng.integers(0, 2)
        Q = rot(a) @ (np.diag([1.0, -1.0]) if e else np.eye(2)); s = rng.uniform(-0.4, 0.4, 2)
        mots.append((Q, s, a, e))
    bodies = [disc_points(1200), boundary_points(3, 0, (0, 0), 150), boundary_points(5, 0, (0, 0), 150)]
    pts = [b @ Q.T + s for b, (Q, s, a, e) in zip(bodies, mots)]
    A0 = hull_area(np.vstack(pts))
    # --- the reduction of Lemma 4.3, done numerically ---
    # 1. replace reflecting g_i by g_i o S_i where S_i = diag(1,-1) is a symmetry of body i (D, B3, B5 are all symmetric under it)
    Qs = [Q @ (np.diag([1.0, -1.0]) if e else np.eye(2)) for (Q, s, a, e) in mots]   # now rotations rot(a_i)
    ss = [m[1] for m in mots]
    # 2. translate so D's image centre ss[0] is the origin; 3. rotate by -a_2 so B3 has orientation 0
    a2, a3 = mots[1][2], mots[2][2]
    t3 = rot(-a2) @ (ss[1]-ss[0]); rho = (a3 - a2) % (2*np.pi/5); t5 = rot(-a2) @ (ss[2]-ss[0])
    # placement point sets: D at origin, B3 + t3 (orientation 0), rho-rotated B5 + t5
    P = [disc_points(1200), boundary_points(3, 0, tuple(t3), 150), boundary_points(5, rho, tuple(t5), 150)]
    A1 = hull_area(np.vstack(P))
    worst_gauge = max(worst_gauge, abs(A1-A0))
print("max |area(original arrangement) - area(reduced placement (t3,rho in [0,2pi/5),t5))| over 300 random motions incl. reflections:", worst_gauge)
for trial in range(300):
    t3 = rng.uniform(-.5, .5, 2); t5 = rng.uniform(-.5, .5, 2); rho = rng.uniform(0, 2*np.pi)
    a = A_outer(t3, rho, t5, 4000); b = A_outer(t3, rho + 2*np.pi/5, t5, 4000); c = A_outer(t3, rho - 4*np.pi/5, t5, 4000)
    worst_per = max(worst_per, abs(a-b), abs(a-c))
    S = np.array([1.0, -1.0]); m = A_outer(S*t3, -rho, S*t5, 4000)
    worst_mir = max(worst_mir, abs(a-m))
print("max |A(rho) - A(rho+2pi/5)|, |A(rho)-A(rho-4pi/5)| (support-function area, N=4000):", worst_per)
print("max |A(t3,rho,t5) - A(S t3,-rho,S t5)| (mirror):", worst_mir)
# negative control: a non-period shift must change A
t3 = np.array([.1, .05]); t5 = np.array([-.05, .1]); print("control: |A(rho)-A(rho+pi/5)| =", abs(A_outer(t3, .3, t5, 4000)-A_outer(t3, .3+np.pi/5, t5, 4000)), "(must be >> 0)")

print("==== L4: erosion  |W_j-V_j|<=delta  =>  cap D(V_j,1-delta) in cap D(W_j,1) ====")
worst = -9.0; nchk = 0
for trial in range(4000):
    n = rng.integers(2, 8)
    if rng.random() < .5:   # regular-ish corner sets of B3/B5 with random rotation/translation, random delta
        nn = int(rng.choice([3, 5])); V = corners(nn, rng.uniform(0, 6.3)) + rng.uniform(-.7, .7, 2)
    else:                   # arbitrary points
        V = rng.uniform(-.6, .6, (n, 2))
    delta = 10**rng.uniform(-6, np.log10(.6))
    rho = 1-delta
    cen = V.mean(0)
    # sample p in the cap by rays from several base points; find boundary by exact quadratic along rays
    base = cen
    if np.max(np.hypot(*(V-base).T)) > rho:      # try the minimax centre by crude search
        from scipy.optimize import minimize
        r = minimize(lambda p: np.max(np.hypot(*(V-p).T)), cen, method='Nelder-Mead', options=dict(xatol=1e-13, fatol=1e-13))
        base = r.x
        if r.fun > rho: continue
    ang = rng.uniform(0, 2*np.pi, 400); U = np.stack([np.cos(ang), np.sin(ang)], 1)
    smax = np.full(400, np.inf)
    for v in V:
        b = U@(base-v); c = np.sum((base-v)**2)-rho**2
        smax = np.minimum(smax, -b+np.sqrt(np.maximum(b*b-c, 0)))
    X = base + (smax*rng.choice([1.0, 1.0, 0.999999, rng.random()]))[:, None]*U      # boundary / near-boundary points
    # adversarial W: push each corner directly away from the farthest relevant point; try each point's own worst W_j
    worstd = -9
    for v in V:
        d = np.hypot(*(X-v).T)                            # |p-V_j|
        # W_j = V_j + delta * (V_j - p)/|V_j-p| maximises |p-W_j| = |p-V_j| + delta
        worstd = max(worstd, np.max(d + delta) - 1)
    # also random admissible W
    for _ in range(3):
        ph = rng.uniform(0, 2*np.pi, len(V)); W = V + delta*np.stack([np.cos(ph), np.sin(ph)], 1)*rng.random((len(V), 1))**.2
        dd = np.sqrt(((X[:, None, :]-W[None])**2).sum(-1)).max()
        worstd = max(worstd, dd-1)
    worst = max(worst, worstd); nchk += len(X)
print(f"checked {nchk} boundary/near-boundary points of random eroded sets: max over (|p-W_j|-1) = {worst:.3e}  (<=~1e-15 means no violation; tight case = 0)")

print("==== L5: corner movement bound ====")
def delta_B3(h): return np.hypot(h[0], h[1])
def delta_B5(h, hr): return np.hypot(h[0], h[1]) + 2*R5*np.sin(hr/2)
w3 = w5 = -9; ratio3 = ratio5 = 0
for trial in range(20000):
    c = rng.uniform(-.7, .7, 2); h = 10**rng.uniform(-6, -.3, 2); cr = rng.uniform(0, 2*np.pi/5); hr = 10**rng.uniform(-6, -.2)
    # placements: box vertices and random points
    for k in range(6):
        if k < 3:
            sg = rng.choice([-1, 1], 3); d = sg*np.array([h[0], h[1], hr])
        else:
            d = (rng.random(3)*2-1)*np.array([h[0], h[1], hr])
        t = c + d[:2]; rr = cr + d[2]
        V3 = corners(3) + c; W3 = corners(3) + t
        disp3 = np.max(np.hypot(*(W3-V3).T)); w3 = max(w3, disp3-delta_B3(h)); ratio3 = max(ratio3, disp3/delta_B3(h))
        V5 = corners(5, cr) + c; W5 = corners(5, rr) + t
        disp5 = np.max(np.hypot(*(W5-V5).T)); w5 = max(w5, disp5-delta_B5(h, hr)); ratio5 = max(ratio5, disp5/delta_B5(h, hr))
print(f"B3: max(actual corner movement - delta3) = {w3:.3e}, max ratio {ratio3:.15f}   B5: max(actual - delta5) = {w5:.3e}, max ratio {ratio5:.15f}   (20000 boxes x 6 placements)")
# tightness / adversarial: B5 optimum direction: translation aligned with rotation chord
hbest = 0
for trial in range(2000):
    h = np.array([.01, .01]); hr = .05; cr = rng.uniform(0, 2*np.pi)
    # choose corner k, rotate by +hr, translate along chord direction
    k = rng.integers(0, 5); V = corners(5, cr)[k]; Wr = corners(5, cr+hr)[k]
    chord = Wr-V; u = chord/np.hypot(*chord); t = np.sign(u)*h      # box vertex closest to chord direction
    hbest = max(hbest, np.hypot(*(chord+t))/delta_B5(h, hr))
print("adversarial (box vertex aligned with the rotation chord) max ratio actual/delta5 =", hbest, " (<=1 required)")

print("==== L6: core inside every placed body + beta <= A ====")
def core_pts(Vc, rho_, nang=720):
    base = Vc.mean(0)
    ang = np.linspace(0, 2*np.pi, nang, endpoint=False); U = np.stack([np.cos(ang), np.sin(ang)], 1)
    smax = np.full(nang, np.inf)
    for v in Vc:
        b = U@(base-v); c = np.sum((base-v)**2)-rho_**2
        smax = np.minimum(smax, -b+np.sqrt(np.maximum(b*b-c, 0)))
    return base + smax[:, None]*U
ring = disc_points(2048)
maxcont = -9; maxgap = -9; ncase = 0; nempty = 0
for trial in range(600):
    c3 = rng.uniform(-.4, .4, 2); c5 = rng.uniform(-.4, .4, 2); cr = rng.uniform(0, 2*np.pi/5)
    sc = 10**rng.uniform(-4, -0.7)
    h3 = sc*rng.uniform(.2, 1, 2); h5 = sc*rng.uniform(.2, 1, 2); hr = sc*rng.uniform(.2, 1)
    d3 = np.hypot(*h3); d5 = np.hypot(*h5)+2*R5*np.sin(hr/2)
    V3c = corners(3)+c3; V5c = corners(5, cr)+c5
    pieces = [ring]
    cores = []
    for (Vc, dl, nn) in ((V3c, d3, 3), (V5c, d5, 5)):
        if 1-dl < Rn(nn): nempty += 1; cores.append(None); continue
        cp = core_pts(Vc, 1-dl); cores.append(cp); pieces.append(cp)
    beta_in = hull_area(np.vstack(pieces))
    for k in range(8):
        sg = rng.choice([-1, 1], 3) if k < 4 else (rng.random(3)*2-1)
        t3 = c3 + sg[0]*h3*np.array([1, 1]) * (1 if k < 4 else 1); 
        t3 = c3 + (rng.choice([-1, 1], 2)*h3 if k < 4 else (rng.random(2)*2-1)*h3)
        t5 = c5 + (rng.choice([-1, 1], 2)*h5 if k < 4 else (rng.random(2)*2-1)*h5)
        rr = cr + (rng.choice([-1, 1])*hr if k < 4 else (rng.random()*2-1)*hr)
        W3 = corners(3)+t3; W5 = corners(5, rr)+t5
        for cp, W in ((cores[0], W3), (cores[1], W5)):
            if cp is None: continue
            dist = np.sqrt(((cp[:, None, :]-W[None])**2).sum(-1)).max()
            maxcont = max(maxcont, dist-1)
        Aout = A_outer(t3, rr, t5, 8000)
        maxgap = max(maxgap, beta_in - Aout); ncase += 1
print(f"{ncase} (box,placement) cases ({nempty} empty cores skipped): max over core points of (dist to placed corner - 1) = {maxcont:.3e}; max(beta_inner - A_outer) = {maxgap:.3e} (must be < 0; beta_inner is inner (polygonal) so this is a conservative test)")

print("==== L8: a-priori exclusion: |t3|>0.7 or |t5|>0.7 => A >= f(0.7) ====")
fmin = 9; viol = 0
for trial in range(3000):
    far = rng.choice([3, 5]); r_ = 0.7+10**rng.uniform(-9, 0); ang = rng.uniform(0, 2*np.pi)
    tfar = r_*np.array([np.cos(ang), np.sin(ang)]); tnear = rng.uniform(-.7, .7, 2)
    rho = rng.uniform(0, 2*np.pi/5)
    t3, t5 = (tfar, tnear) if far == 3 else (tnear, tfar)
    A = A_outer(t3, rho, t5, 3000)
    fmin = min(fmin, A - float(f(r_))); 
    if A < float(f(0.7)): viol += 1
print("min (A_outer - f(|t|)) over 3000 far placements =", fmin, "; #A_outer < f(0.7):", viol, " (A_outer >= A so A_outer<f would be a violation)")
print("elapsed s:", time.time()-t0)
