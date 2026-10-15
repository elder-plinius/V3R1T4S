#!/usr/bin/env python3
"""mix_opt.py (adversary lens): continuous optimisation of an adversary mixture of K conditionally independent
two-state environments sharing R report values (so that report pairs collide exactly), unknown-state CI cell of
arXiv:2604.24517. Objective: LB(D) = min_f E_D L(f|env) (floats here; the claim path is the exact checker
../../code/lb_check.py on the rationalised JSON this script writes).

Parametrisation (all constraints satisfied by construction):
  shared reports r_1 < ... < r_R in (0,1)   (sorted from R free numbers in (0,1))
  env k: pattern ((a1,b1),(a2,b2)) with a<b indices into r; theta1 = u1 * r_min_used, theta2 = r_max_used + u2*(1-r_max_used),
         mu = lo + u3*(hi-lo) with lo = max(r_a1, r_a2), hi = min(r_b1, r_b2); u in [0,1] (clipped)
  weights: softmax of K free numbers.
Expert report distribution in env k: P(x_H) = (mu - x_L)/(x_H - x_L) (Bayes plausibility); binary signals.
Optimiser: random restarts over patterns + Nelder-Mead (own implementation) + final coordinate polishing.
"""
import sys, json, time, argparse, random, itertools
import numpy as np
from fractions import Fraction as Fr

ap = argparse.ArgumentParser()
ap.add_argument("--K", type=int, default=2); ap.add_argument("--R", type=int, default=2)
ap.add_argument("--restarts", type=int, default=200); ap.add_argument("--nm_iters", type=int, default=4000)
ap.add_argument("--time_cap", type=float, default=600); ap.add_argument("--seed", type=int, default=1)
ap.add_argument("--out", default="output/mix"); ap.add_argument("--symmetric", type=int, default=0, help="1: both experts use the same pair in every env")
ap.add_argument("--from_table3", type=int, default=0)
ap.add_argument("--patterns", default=None, help="explicit pattern list as JSON, e.g. [[[0,1],[0,1]],[[0,1],[0,1]]]")
ap.add_argument("--den", type=int, default=10**6, help="denominator for rationalising the result")
ap.add_argument("--init", default=None, help="npy file with a starting parameter vector (with --patterns)")
args = ap.parse_args()
random.seed(args.seed); np.random.seed(args.seed)
K, R = args.K, args.R; BAR = 31 / 1326; t0 = time.time()

def lb_of(params, patterns):
    """params: R report params, then per env (u1,u2,u3), then K weight params. Returns LB (float) or -1 if invalid."""
    r = np.sort(np.clip(params[:R], 1e-6, 1 - 1e-6))
    if np.any(np.diff(r) < 1e-9): return -1.0
    u = np.clip(params[R:R + 3 * K], 0.0, 1.0).reshape(K, 3)
    wl = params[R + 3 * K:]; w = np.exp(wl - wl.max()); w /= w.sum()
    M0, M1, M2 = {}, {}, {}
    for k in range(K):
        (a1, b1), (a2, b2) = patterns[k]
        xl1, xh1, xl2, xh2 = r[a1], r[b1], r[a2], r[b2]
        rmin = min(xl1, xl2); rmax = max(xh1, xh2)
        th1 = u[k, 0] * rmin; th2 = rmax + u[k, 1] * (1 - rmax)
        lo = max(xl1, xl2); hi = min(xh1, xh2)
        if hi < lo: return -1.0
        mu = lo + u[k, 2] * (hi - lo)
        d = th2 - th1
        if d <= 1e-12: return -1.0
        lam2 = (mu - th1) / d; lam1 = 1 - lam2
        if lam1 <= 1e-12 or lam2 <= 1e-12: return -1.0
        q1 = (mu - xl1) / (xh1 - xl1); q2 = (mu - xl2) / (xh2 - xl2)
        for (ia, xa, pa) in ((a1, xl1, 1 - q1), (b1, xh1, q1)):
            for (ib, xb, pb) in ((a2, xl2, 1 - q2), (b2, xh2, q2)):
                p1 = (xa - th1) / d; p2 = (xb - th1) / d
                z = (1 - p1) * (1 - p2) / lam1 + p1 * p2 / lam2
                prob = w[k] * pa * pb * z
                if prob <= 0: continue
                fb = th1 + d * (p1 * p2 / lam2) / z
                key = (ia, ib)
                M0[key] = M0.get(key, 0.0) + prob; M1[key] = M1.get(key, 0.0) + prob * fb; M2[key] = M2.get(key, 0.0) + prob * fb * fb
    return sum(M2[k] - M1[k] ** 2 / M0[k] for k in M0)

def nelder_mead(f, x0, step=0.1, iters=2000, tol=1e-12):
    n = len(x0); pts = [np.array(x0, float)]
    for i in range(n):
        y = np.array(x0, float); y[i] += step * (1 if np.random.rand() < 0.5 else -1); pts.append(y)
    vals = [f(p) for p in pts]
    for it in range(iters):
        order = np.argsort(vals)[::-1]; pts = [pts[i] for i in order]; vals = [vals[i] for i in order]   # maximise
        if vals[0] - vals[-1] < tol and it > 50: break
        c = np.mean(pts[:-1], axis=0); xr = c + (c - pts[-1]); fr = f(xr)
        if fr > vals[0]:
            xe = c + 2 * (c - pts[-1]); fe = f(xe)
            if fe > fr: pts[-1], vals[-1] = xe, fe
            else: pts[-1], vals[-1] = xr, fr
        elif fr > vals[-2]: pts[-1], vals[-1] = xr, fr
        else:
            xc = c + 0.5 * (pts[-1] - c); fc = f(xc)
            if fc > vals[-1]: pts[-1], vals[-1] = xc, fc
            else:
                for i in range(1, len(pts)):
                    pts[i] = pts[0] + 0.5 * (pts[i] - pts[0]); vals[i] = f(pts[i])
    i = int(np.argmax(vals)); return pts[i], vals[i]

def random_pattern():
    def pair():
        a, b = sorted(random.sample(range(R), 2)); return (a, b)
    pats = []
    for k in range(K):
        p1 = pair(); p2 = p1 if args.symmetric else pair(); pats.append((p1, p2))
    return pats

if args.patterns: fixed_patterns = [tuple(tuple(tuple(p) for p in env) for env in json.loads(args.patterns))]
else: fixed_patterns = None
best = (-1.0, None, None)
log = open(args.out + ".log", "a")
for rs in range(args.restarts):
    pats = fixed_patterns[0] if fixed_patterns else random_pattern()
    if args.from_table3 and K == 2 and R == 2:
        pats = (((0, 1), (0, 1)), ((0, 1), (0, 1)))
        x0 = np.array([1 / 6, 5 / 6, 0.0, 0.0, 0.5, 1.0 / 5, 1.0, 0.5, 0.0, 0.0])   # Table 3 exactly
        # env A: theta1 = 0 (u1=0), theta2 = 5/6 (u2=0), mu = 1/6 + 0.5*(4/6) = 1/2? Table 3 has mu_A = 5/12 -> u3 = (5/12-1/6)/(4/6) = 0.375
        x0[4] = 0.375
        # env B: theta1 = 1/6 (u1 = 1), theta2 = 1 (u2 = 1), mu_B = 7/12 -> u3 = (7/12-1/6)/(4/6) = 0.625
        x0[5] = 1.0; x0[6] = 1.0; x0[7] = 0.625
    elif args.init and rs == 0:
        x0 = np.load(args.init)
    else:
        x0 = np.concatenate([np.random.rand(R), np.random.rand(3 * K), np.random.randn(K) * 0.3])
    f = lambda p: lb_of(p, pats)
    v0 = f(x0)
    x, v = nelder_mead(f, x0, step=0.15, iters=args.nm_iters)
    # second NM round from the found point with a smaller step
    x, v = nelder_mead(f, x, step=0.02, iters=args.nm_iters)
    msg = "restart %3d | patterns %s | start %.6f -> best %.9f | %.0fs" % (rs, pats, v0, v, time.time() - t0)
    print(msg, flush=True); log.write(msg + "\n"); log.flush()
    if v > best[0]: best = (v, x.copy(), pats)
    if time.time() - t0 > args.time_cap: print("time cap", flush=True); break
v, x, pats = best
print("BEST LB (float) %.9f  bar %.9f  diff %.3e  patterns %s" % (v, BAR, v - BAR, pats), flush=True)
log.write("BEST LB (float) %.9f  bar %.9f  diff %.3e  patterns %s\n" % (v, BAR, v - BAR, pats))
# ---- rationalise and write the mixture JSON (exact check by lb_check.py) ----
r = np.sort(np.clip(x[:R], 1e-6, 1 - 1e-6)); u = np.clip(x[R:R + 3 * K], 0, 1).reshape(K, 3)
wl = x[R + 3 * K:]; w = np.exp(wl - wl.max()); w /= w.sum()
DEN = args.den
rq = [Fr(int(round(float(v) * DEN)), DEN) for v in r]
envs = []
wq = [Fr(int(round(float(v) * DEN)), DEN) for v in w]; wq[int(np.argmax(w))] += 1 - sum(wq)
for k in range(K):
    (a1, b1), (a2, b2) = pats[k]
    xl1, xh1, xl2, xh2 = rq[a1], rq[b1], rq[a2], rq[b2]
    rmin = min(xl1, xl2); rmax = max(xh1, xh2)
    th1 = Fr(int(round(float(u[k, 0] * rmin) * DEN)), DEN); th2 = Fr(int(round(float(rmax + u[k, 1] * (1 - rmax)) * DEN)), DEN)
    th1 = min(th1, rmin); th2 = max(th2, rmax)
    lo = max(xl1, xl2); hi = min(xh1, xh2)
    mu = Fr(int(round(float(lo + u[k, 2] * (hi - lo)) * DEN)), DEN); mu = min(max(mu, lo), hi)
    d = th2 - th1; lam2 = (mu - th1) / d; lam1 = 1 - lam2
    if lam1 <= 0 or lam2 <= 0: print("env %d degenerate after rounding (lambda); skipping JSON" % k); envs = None; break
    def lik(xl, xh):
        q = (mu - xl) / (xh - xl); pl = (xl - th1) / d; ph = (xh - th1) / d
        return [[str((1 - pl) * (1 - q) / lam1), str((1 - ph) * q / lam1)], [str(pl * (1 - q) / lam2), str(ph * q / lam2)]]
    envs.append({"weight": str(wq[k]), "theta": [str(th1), str(th2)], "prior": [str(lam1), str(lam2)],
                 "experts": [{"likelihoods": lik(xl1, xh1)}, {"likelihoods": lik(xl2, xh2)}],
                 "reports": [[str(xl1), str(xh1)], [str(xl2), str(xh2)]], "mu": str(mu)})
if envs:
    json.dump({"lb_float": v, "patterns": [list(map(list, p)) for p in pats], "environments": envs}, open(args.out + "_mixture.json", "w"), indent=1)
    print("wrote %s_mixture.json" % args.out, flush=True)
np.save(args.out + "_x.npy", x)
