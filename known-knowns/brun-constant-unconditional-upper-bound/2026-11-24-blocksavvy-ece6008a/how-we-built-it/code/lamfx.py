"""Exact rational Selberg weights (Klyve (5.24)-(5.26)) and a rigorous upper bound for Sigma(n) = sum_q |rho_q|.
lambda_d = mu(d) prod_{p|d}(p-1)/(p-2) * G_d(n/d) / V(n),  G_d(y) = sum_{t<=y, t odd squarefree, (t,d)=1} h(t),  h(t) = prod_{p|t} 1/(p-2),
V(n) = G_1(n), for d odd squarefree <= n (n = floor(z)). All in exact rationals (flint fmpq).
L_d = round(2^40 lambda_d) exactly (|2^40 lambda_d - L_d| <= 1/2). rhofx (C, exact int128) returns S = sum_q |P_q|,
P_q = sum_{lcm(a,b)=q} L_a L_b over ordered pairs. Then 2^80 Sigma <= S + sum_{(a,b)} (|L_a| + |L_b| + 1) = S + 2 N sum|L| + N^2
(each |2^80 lambda_a lambda_b - L_a L_b| <= |L_a|/2 + |L_b|/2 + 1/4; we use the coarser bound). Returns exact fmpq upper bound.
Also returns Lambda(n) = sum |lambda_d| and W(n) = sum_{d<=n odd sqfree} prod p/(p-2) exactly, for the identity Lambda = W/V."""
import subprocess, os
from flint import fmpq, fmpz
SCALE = 40
def odd_sqfree(n):
    spf = list(range(n + 1))
    for i in range(2, int(n**0.5) + 1):
        if spf[i] == i:
            for m in range(i * i, n + 1, i):
                if spf[m] == m: spf[m] = i
    out = {}
    for d in range(1, n + 1, 2):
        m = d; ps = []; ok = True
        while m > 1:
            p = spf[m]; m //= p
            if m % p == 0: ok = False; break
            ps.append(p)
        if ok: out[d] = ps
    return out
def weights(n):
    ds = odd_sqfree(n)
    h = {}; kk = {}
    for d, ps in ds.items():
        num = 1; den = 1; kn = 1
        for p in ps: den *= (p - 2); kn *= (p - 1)
        h[d] = fmpq(1, den); kk[d] = fmpq(kn, den)
    keys = sorted(ds)
    V = sum((h[d] for d in keys), fmpq(0))
    from math import gcd
    lam = {}
    for d in keys:
        y = n // d
        G = sum((h[t] for t in keys if t <= y and gcd(t, d) == 1), fmpq(0)) if d > 1 else V
        lam[d] = (-1 if len(ds[d]) % 2 else 1) * kk[d] * G / V
    return keys, lam, V, h
def rounded(lam, keys):
    L = {}
    for d in keys:
        x = lam[d] * (fmpz(2) ** SCALE)
        L[d] = int((x + fmpq(1, 2)).floor())
        assert abs(x - L[d]) <= fmpq(1, 2)
    return L
def sigma_upper(n, exe):
    keys, lam, V, h = weights(n)
    L = rounded(lam, keys)
    inp = "%d %d\n" % (n, len(keys)) + "".join("%d %d\n" % (d, L[d]) for d in keys)
    r = subprocess.run([exe], input=inp, capture_output=True, text=True)
    if r.returncode != 0: raise RuntimeError("rhofx failed (%d): %s" % (r.returncode, r.stderr))
    nn, N, sL, sAL, S = r.stdout.split(); N = int(N); assert int(nn) == n and N == len(keys)
    assert int(sL) == sum(L.values()) and int(sAL) == sum(abs(v) for v in L.values())
    up = fmpq(int(S) + 2 * N * int(sAL) + N * N, 2 ** (2 * SCALE))
    Lam = sum((abs(lam[d]) for d in keys), fmpq(0))
    Wn = sum((fmpq(d) * h[d] for d in keys), fmpq(0))   # prod p/(p-2) = d * h(d)
    return dict(n=n, N=N, sigma_up=up, S=int(S), sumAbsL=int(sAL), sumL=int(sL), Lambda=Lam, V=V, W=Wn, lam1=lam[1],
                sumlam=sum((lam[d] for d in keys), fmpq(0)))
if __name__ == "__main__":
    import sys, time
    exe = sys.argv[1]
    for a in sys.argv[2:]:
        t = time.time(); r = sigma_upper(int(a), exe)
        print(r["n"], r["N"], float(r["sigma_up"]), float(r["Lambda"]**2), float(r["sigma_up"] / r["Lambda"]**2),
              "Lambda==W/V" if r["Lambda"] == r["W"] / r["V"] else "IDENTITY-FAIL", "lam1=1" if r["lam1"] == 1 else "LAM1-FAIL",
              "%.1fs" % (time.time() - t), flush=True)
