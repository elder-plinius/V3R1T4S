"""Standalone checker for: under GRH (Dirichlet L-functions) and RH, Brun's constant B < 2.126988 (Selberg-weight version).
Adapted from runs/2026-11-23-1618/claim_v2/verify/check.py. Reads cert_selberg_p128.json (z_i per interval and the stated
sup of each interval term). Recomputes every term in arb from definitions: V(n), M(n), W(n) from wvcount.c (exact integer
sieve, this folder), Lambda(z) <= W_up(z)/V_low(z), W_up for z > 1e10 = min_s z/(2*0.6601618) + z^s S'(s) with S'(s) recomputed.
Checks: (0) wvcount vs a pure-Python definition for n <= 20000 (S, M and SW); (1) 1 <= z_i < m_i^(1/4);
(2) recomputed sup of each term (incl. the pi_2(z) correction 2 z_i/m_i) <= stated term * (1 + 1e-15), and stated <= recomputed * (1 + 1e-5)
    (two-sided, so a corrupted certificate is rejected; table rounding makes stated exceed recomputed by at most 5e-6 relative);
(3) A(1e10) <= 0.0107001 (own V lemma); (4) total of the RECOMPUTED sups + tail + head < 2.126988. Last line: PASS or FAIL.
Usage: check_selberg.py [cert.json] [precision bits, default 128]; run_checks.sh runs 128 and 256."""
import json, math, os, subprocess, sys, traceback
class Fail(Exception): pass
def fail(msg): raise Fail(msg)
def main():
    from flint import arb, fmpz, fmpq, ctx
    ctx.prec = int(sys.argv[2]) if len(sys.argv) > 2 else 128
    print('precision bits:', ctx.prec)
    HERE = os.path.dirname(os.path.abspath(__file__))
    cert = json.load(open(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "cert_selberg_p128.json")))
    CLAIM = arb(fmpq(2126988, 10**6)); iv = cert["intervals"]
    if len(iv) != 9906: fail("expected 9906 intervals")
    exe = os.path.join(HERE, "wvcount")
    if subprocess.call(["cc", "-O2", "-o", exe, os.path.join(HERE, "wvcount.c"), "-lpthread"]) != 0: fail("cannot compile wvcount.c")
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
    for i, (kind, h, _) in enumerate(iv):
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
    total = arb(0); worst = -1.0
    for i in range(9906):
        s, e = mids[i], mids[i + 1]; zf, z = zs[i]
        c1 = (e.log().log() - e.li() / e) - (s.log().log() - s.li() / s)
        c2 = 2 * (s.log() + 2) / s.sqrt() - 2 * (e.log() + 2) / e.sqrt()
        ls = s.log(); lam = 2 * z.log() / ls
        if not (lam < arb(fmpq(1, 2))): lam = arb(fmpq(1, 2))
        cpi = 1 / (8 * PI) + (1 / (2 * PI) + 3 / ls) * lam + 1 / (4 * PI * ls) + 6 / ls**2 + li2u / (s.sqrt() * ls)
        Vl = V_low(zf, z); Lam = W_up(zf, z) / Vl
        term = 2 * (c1 / Vl + cpi * c2 * Lam**2) + 2 * z / s
        up = term.upper(); stated = arb(iv[i][2])
        if not (up <= stated * (1 + arb(10)**-15)): fail("interval %d: recomputed %s exceeds stated %s" % (i, up.str(20, radius=False), iv[i][2]))
        if stated > up * (1 + arb(10)**-5): fail("interval %d: stated %s exceeds recomputed %s by more than 1e-5 relative (corrupted certificate?)" % (i, iv[i][2], up.str(20, radius=False)))
        worst = max(worst, float(((stated - up) / stated).mid()))
        total += up
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
    if not (Btot < CLAIM): fail("total not below 2.126988")
    print("check 4: B < 2.126988"); print("PASS")
if __name__ == "__main__":
    try: main()
    except Fail as e: print("FAIL reason:", e); print("FAIL"); sys.exit(1)
    except Exception: traceback.print_exc(); print("FAIL reason: malformed or inconsistent input"); print("FAIL"); sys.exit(1)
