"""Standalone checker for: under GRH (Dirichlet L-functions) and RH, Brun's constant B < 2.1257395 (per-modulus Selberg remainder).
Adapted from the e6b84d42 checker check_selberg.py. NEW for intervals whose entry ends with "rho": the error factor is
Sigma(n) = sum_q |rho_q|, rho_q = sum_{lcm(d1,d2)=q} lambda_d1 lambda_d2, n = floor(z_i) <= 20000. The checker computes the Selberg
weights lambda_d (Klyve (5.24)-(5.26)) itself in arb at the working precision, rounds L_d = round(2^40 lambda_d) with
|2^40 lambda_d - L_d| <= 1 certified by the ball, sums L_a L_b per modulus EXACTLY with its own sort-based rhocount.c, checks
sum_q P_q == (sum L)^2, lambda_1 = 1 and sum|lambda_d| <= W_up(n)/V_low(n), and uses Sigma <= (sum_q|P_q| + 2 N sum|L| + N^2)/2^80.
Reads the certificate (z_i per interval and the stated
sup of each interval term). Recomputes every term in arb from definitions: V(n), M(n), W(n) from wvcount.c (exact integer
sieve, this folder), Lambda(z) <= W_up(z)/V_low(z), W_up for z > 1e10 = min_s z/(2*0.6601618) + z^s S'(s) with S'(s) recomputed.
Checks: (0) wvcount vs a pure-Python definition for n <= 20000 (S, M and SW); (1) 1 <= z_i < m_i^(1/4);
(2) recomputed sup of each term (incl. the pi_2(z) correction 2 z_i/m_i) <= stated term * (1 + 1e-15), and stated <= recomputed * (1 + 1e-5)
    (two-sided, so a corrupted certificate is rejected; table rounding makes stated exceed recomputed by at most 5e-6 relative);
(3) A(1e10) <= 0.0107001 (own V lemma); (4) total of the RECOMPUTED sups + tail + head < 2.1257395. Last line: PASS or FAIL.
Usage: check_rho.py cert.json [precision bits, default 128]; run_checks.sh runs 128 and 256."""
import json, math, os, subprocess, sys, traceback
class Fail(Exception): pass
def fail(msg): raise Fail(msg)
def main():
    from flint import arb, fmpz, fmpq, ctx
    ctx.prec = int(sys.argv[2]) if len(sys.argv) > 2 else 128
    print('precision bits:', ctx.prec)
    HERE = os.path.dirname(os.path.abspath(__file__))
    cert = json.load(open(sys.argv[1]))
    CLAIM = arb(fmpq(21257395, 10**7)); iv = cert["intervals"]
    if len(iv) != 9906: fail("expected 9906 intervals")
    exe = os.path.join(HERE, "wvcount"); rexe = os.path.join(HERE, "rhocount")
    if subprocess.call(["cc", "-O2", "-o", exe, os.path.join(HERE, "wvcount.c"), "-lpthread"]) != 0: fail("cannot compile wvcount.c")
    if subprocess.call(["cc", "-O2", "-o", rexe, os.path.join(HERE, "rhocount.c")]) != 0: fail("cannot compile rhocount.c")
    def wvcount(points, N):
        out = subprocess.run([exe, str(N), str(max(1, min(8, os.cpu_count() or 1)))], input="\n".join(map(str, points)) + "\n",
                             capture_output=True, text=True, check=True).stdout.split("\n")
        return {int(a): (int(b), int(c), int(d)) for a, b, c, d in (l.split() for l in out if l.strip())}
    small = sorted(set(list(range(0, 20001, 7)) + [20000])); got = wvcount(small, 20000)
    def factor(n):
        f = []; d = 2
        while d * d <= n:
            while n % d == 0: f.append(d); n //= d
            d += 1
        if n > 1: f.append(n)
        return f
    S = 0; M = 0; SW = 0
    for n in range(0, 20001):
        if n >= 1 and n % 2 == 1:
            f = factor(n)
            if len(f) == len(set(f)):
                P = 1
                for p in f: P *= p - 2
                S += (1 << 64) // P; M += 1; SW += -((-(n << 40)) // P)
        if n in got and got[n] != (S, M, SW): fail("wvcount disagrees with the definition at n=%d" % n)
    print("check 0: wvcount matches the definition at %d points <= 20000" % len(small))
    L10 = arb(10).log()
    mids = [arb(4) * arb(10)**18] + [(L10 * arb(fmpq(95 + i, 5))).exp() for i in range(9906)]
    L2 = 10**10; zs = []
    for i, ent in enumerate(iv):
        if not (len(ent) == 3 or (len(ent) == 4 and ent[3] == "rho")): fail("bad entry %d" % i)
        kind, h = ent[0], ent[1]
        if kind == "z": zf = float.fromhex(h); z = arb(zf)
        elif kind == "t": zf = math.inf; z = arb(float.fromhex(h)).exp()
        else: fail("bad z kind")
        if not (z >= arb(1) and z < mids[i].root(4)): fail("z_%d not admissible" % i)
        if kind == "t" and not (z > arb(L2)): fail("t-encoded z_%d must exceed 1e10" % i)
        zs.append((zf, z))
    pts = sorted(set([L2] + [int(math.floor(zf)) for zf, z in zs if zf <= L2]))
    tab = wvcount(pts, L2); TWO64 = arb(2)**64; TWO40 = arb(2)**40
    PI = arb.pi(); li2u = arb(fmpq(10451638, 10**7)); pi2u = arb(fmpq(6601619, 10**7)); C2lo = arb(fmpq(6601618, 10**7))
    A = arb(fmpq(107001, 10**7)); VL2 = arb(fmpz(tab[L2][0])) / TWO64
    # S'(s) for the W lemma
    Pm = 10**7; sv = bytearray([1]) * (Pm + 1); sv[0] = sv[1] = 0
    for q in range(2, int(Pm**0.5) + 1):
        if sv[q]: sv[q*q::q] = bytearray(len(range(q*q, Pm + 1, q)))
    oddp = [p for p in range(3, Pm + 1, 2) if sv[p]]
    tailp = lambda b: arb(fmpq(125506, 100000)) * b * arb(Pm)**(1 - b) / ((b - 1) * arb(Pm).log())
    SP = {}
    for k in (52, 54, 56, 58, 60, 63, 66, 70, 75):
        s_ = arb(fmpq(k, 100)); lg = arb(0)
        for p in oddp: pa = arb(p); lg += (1 + 2 / (pa - 2) * pa**(-s_) + pa / (pa - 2) * pa**(-2 * s_)).log()
        lg += arb(Pm + 1) / arb(Pm - 1) * (2 * tailp(1 + s_) + tailp(2 * s_)); SP[k] = (s_, lg.exp())
    def V_low(zf, z):
        if zf > L2: return VL2 + (z.log() - arb(L2).log()) / (2 * pi2u) - A
        return arb(fmpz(tab[int(math.floor(zf))][0])) / TWO64
    def W_up(zf, z):
        if zf <= L2: return arb(fmpz(tab[int(math.floor(zf))][2])) / TWO40
        best = None
        for k, (s_, Sv) in SP.items():
            b = z / (2 * C2lo) + z**s_ * Sv
            if best is None or b.upper() < best.upper(): best = b
        return best
    import bisect
    from math import gcd
    SIG = {}; TWO80 = arb(2)**80
    def sigma_up(n, zf):
        if n in SIG: return SIG[n]
        if not (1 <= n <= 20000): fail("rho level n=%d outside [1, 20000]" % n)
        fac = {}
        for d in range(1, n + 1, 2):
            m = d; ps = []; p = 3; ok = True
            while p * p <= m:
                if m % p == 0:
                    m //= p
                    if m % p == 0: ok = False; break
                    ps.append(p)
                p += 2
            if ok:
                if m > 1: ps.append(m)
                fac[d] = ps
        ds = sorted(fac); hh = {}
        for d in ds:
            P = 1
            for p in fac[d]: P *= p - 2
            hh[d] = arb(fmpq(1, P))
        pref = [arb(0)]
        for d in ds: pref.append(pref[-1] + hh[d])
        Vn = pref[-1]; Ls = []; Lam = arb(0); lam1 = None
        for d in ds:
            y = n // d; top = bisect.bisect_right(ds, y)
            G = pref[top] if d == 1 else sum((hh[t] for t in ds[:top] if gcd(t, d) == 1), arb(0))
            kq = fmpq(1)
            for p in fac[d]: kq *= fmpq(p - 1, p - 2)
            lam = (-1)**len(fac[d]) * arb(kq) * G / Vn
            if d == 1: lam1 = lam
            Lam += abs(lam)
            x = lam * arb(2)**40; Li = int((x.mid() + arb(fmpq(1, 2))).floor().unique_fmpz())
            if not (abs(x - Li) <= 1): fail("weight rounding not certified at n=%d d=%d" % (n, d))
            Ls.append((d, Li))
        if not lam1.contains(1): fail("lambda_1 != 1 at n=%d" % n)
        if not (Lam <= arb(fmpz(tab[n][2])) / TWO40 / (arb(fmpz(tab[n][0])) / TWO64)): fail("sum |lambda| exceeds W/V at n=%d" % n)
        r = subprocess.run([rexe], input="%d %d\n" % (n, len(Ls)) + "".join("%d %d\n" % t for t in Ls), capture_output=True, text=True)
        if r.returncode != 0: fail("rhocount failed at n=%d (exit %d)" % (n, r.returncode))
        nn, N, sL, sAL, S, ok = r.stdout.split()
        if int(nn) != n or int(N) != len(Ls) or ok != "1" or int(sL) != sum(t[1] for t in Ls) or int(sAL) != sum(abs(t[1]) for t in Ls):
            fail("rhocount inconsistent at n=%d" % n)
        N = int(N); up = (arb(fmpz(int(S))) + 2 * N * arb(fmpz(int(sAL))) + N * N) / TWO80
        if not (up <= Lam**2 * (1 + arb(10)**-9)): fail("Sigma bound exceeds Lambda^2 at n=%d" % n)
        SIG[n] = up; return up
    total = arb(0); worst = -1.0; nrho = 0
    for i in range(9906):
        s, e = mids[i], mids[i + 1]; zf, z = zs[i]
        c1 = (e.log().log() - e.li() / e) - (s.log().log() - s.li() / s)
        c2 = 2 * (s.log() + 2) / s.sqrt() - 2 * (e.log() + 2) / e.sqrt()
        ls = s.log(); lam = 2 * z.log() / ls
        if not (lam < arb(fmpq(1, 2))): lam = arb(fmpq(1, 2))
        cpi = 1 / (8 * PI) + (1 / (2 * PI) + 3 / ls) * lam + 1 / (4 * PI * ls) + 6 / ls**2 + li2u / (s.sqrt() * ls)
        Vl = V_low(zf, z); Lam = W_up(zf, z) / Vl
        if len(iv[i]) == 4:
            if not (zf <= 20000): fail("rho flag on interval %d with z > 20000" % i)
            E = sigma_up(int(math.floor(zf)), zf); nrho += 1
        else: E = Lam**2
        term = 2 * (c1 / Vl + cpi * c2 * E) + 2 * z / s
        up = term.upper(); stated = arb(iv[i][2])
        if not (up <= stated * (1 + arb(10)**-15)): fail("interval %d: recomputed %s exceeds stated %s" % (i, up.str(20, radius=False), iv[i][2]))
        if stated > up * (1 + arb(10)**-5): fail("interval %d: stated %s exceeds recomputed %s by more than 1e-5 relative (corrupted certificate?)" % (i, iv[i][2], up.str(20, radius=False)))
        worst = max(worst, float(((stated - up) / stated).mid()))
        total += up
    print("check rho: %d intervals use Sigma(n) at %d levels n <= 20000 (weights certified, exact sums, identity sum_q P_q = (sum L)^2 OK)" % (nrho, len(SIG)))
    print("check 1-2: 9906 intervals admissible; recomputed sups <= stated (max relative slack %.1e)" % worst)
    tail = 32 * pi2u / mids[-1].log() + 8 / mids[-1].sqrt()
    head = arb(fmpq(1840518, 10**6)) - 2 * arb(fmpz(3023463123235320)) / (arb(4) * arb(10)**18)
    s_ = arb(fmpq(44, 100)); lg = arb(0)
    for p in oddp: pa = arb(p); lg += (1 + (2 * pa**s_ + pa**(2 * s_)) / (pa * (pa - 2))).log()
    lg += arb(Pm + 1) / arb(Pm - 1) * (2 * tailp(2 - s_) + tailp(2 - 2 * s_))
    kappa = (arb.const_euler() + arb(2).log()) / 2
    if not (kappa + 4 >= 1 / (2 * s_)): fail("Rankin max not at u = 1")
    Ab = (kappa + 12) * arb(10)**(-10 * s_) * lg.exp()
    if not (Ab <= A): fail("A(1e10) bound too large")
    print("check 3: A(1e10) <= %s <= 0.0107001" % Ab.upper().str(10, radius=False))
    Btot = total + tail + head
    print("B <= %s (sup of the ball, recomputed)" % Btot.upper().str(20, radius=False))
    if not (Btot < CLAIM): fail("total not below 2.1257395")
    print("check 4: B < 2.1257395"); print("PASS")
if __name__ == "__main__":
    try: main()
    except Fail as e: print("FAIL reason:", e); print("FAIL"); sys.exit(1)
    except Exception: traceback.print_exc(); print("FAIL reason: malformed or inconsistent input"); print("FAIL"); sys.exit(1)
