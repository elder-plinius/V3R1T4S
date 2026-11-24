"""Standalone checker for: under GRH (Dirichlet L-functions) and RH, Brun's constant B < 2.156967.
Re-evaluates every term of the bound in arb ball arithmetic (python-flint) from object/a_bound_certificate.json, which fixes
the sieve parameter z_i of each interval [m_i, m_{i+1}]; V(z) and M(z) come from vcount.c (exact integer sieve, this folder).
Checks: (0) vcount against a pure-Python definition for n <= 20000; (1) every z_i is admissible (1 <= z_i < m_i^(1/4));
(2) every stated term equals the recomputed rigorous upper bound to 1e-18 relative; (3) the V-lemma constant A(1e10) <= 0.0107001;
(4) the total (own recomputed sups + tail + head + pi_2(z) correction) is < 2.156967. Last line: PASS or FAIL."""
import json, math, os, subprocess, sys, traceback

class Fail(Exception): pass
def fail(msg): raise Fail(msg)

def main():
    from fractions import Fraction
    from flint import arb, fmpz, fmpq, ctx
    ctx.prec = 128
    HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
    cert = json.load(open(os.path.join(ROOT, "object", "a_bound_certificate.json")))
    CLAIM = arb(fmpq(2156967, 10**6)); assert cert["claimed_upper_bound"] == "2.156967"
    iv = cert["intervals"]
    if len(iv) != 9906: fail("expected 9906 intervals")
    # ---- vcount ----
    exe = os.path.join(HERE, "vcount")
    if subprocess.call(["cc", "-O2", "-o", exe, os.path.join(HERE, "vcount.c"), "-lpthread"]) != 0: fail("cannot compile vcount.c")
    def vcount(points, N):
        out = subprocess.run([exe, str(N), str(max(1, min(8, os.cpu_count() or 1)))], input="\n".join(map(str, points)) + "\n",
                             capture_output=True, text=True, check=True).stdout.split("\n")
        return {int(a): (int(b), int(c)) for a, b, c in (l.split() for l in out if l.strip())}
    # (0) definition check for n <= 20000
    small = list(range(0, 20001, 7)) + [20000]; small = sorted(set(small)); got = vcount(small, 20000)
    S = 0; M = 0; want = {}; j = 0
    def factor(n):
        f = []; d = 2
        while d * d <= n:
            while n % d == 0: f.append(d); n //= d
            d += 1
        if n > 1: f.append(n)
        return f
    for n in range(0, 20001):
        if n >= 1 and n % 2 == 1:
            f = factor(n)
            if len(f) == len(set(f)):
                P = 1
                for p in f: P *= p - 2
                S += (1 << 64) // P; M += 1
        if n in got and got[n] != (S, M): fail("vcount disagrees with the definition at n=%d" % n)
    print("check 0: vcount matches the definition at %d points <= 20000" % len(small))
    # ---- intervals ----
    L10 = arb(10).log()
    mids = [arb(4) * arb(10)**18] + [(L10 * arb(fmpq(95 + i, 5))).exp() for i in range(9906)]
    L1, L2, L3, STEP = 10**8, 10**10, 10**7, 10**4
    zs = []
    for i, (kind, h, _) in enumerate(iv):
        if kind == "z": zf = float.fromhex(h); z = arb(zf)
        elif kind == "t": zf = math.inf; z = arb(float.fromhex(h)).exp()
        else: fail("bad z kind")
        if not (z >= arb(1) and z < mids[i].root(4)): fail("z_%d not admissible" % i)
        if kind == "t" and not (z > arb(L2)): fail("t-encoded z_%d must exceed 1e10" % i)
        zs.append((zf, z))
    pts = set([L2])
    for zf, z in zs:
        if zf <= L2:
            n = int(math.floor(zf)); pts.add(n if n <= L1 else (n // STEP) * STEP)
    pts = sorted(pts); tab = vcount(pts, L2)
    TWO64 = arb(2)**64
    def Vexact(n): return arb(fmpz(tab[n][0])) / TWO64
    def Vdense(n):  # V lower bound as a double rounded down (what the contributor's dense table stores), exactly representable
        x = tab[n][0] >> 11; v = float(x)
        if int(v) > x: v = math.nextafter(v, 0.0)
        return arb(v) / arb(2)**53
    PI = arb.pi(); li2u = arb(fmpq(10451638, 10**7)); pi2u = arb(fmpq(6601619, 10**7)); A = arb(fmpq(107001, 10**7))
    VL2 = Vexact(L2)
    def V_low(zf, z):
        if zf > L2: return VL2 + (z.log() - arb(L2).log()) / (2 * pi2u) - A
        n = int(math.floor(zf))
        return Vexact((n // STEP) * STEP) if n > L1 else Vdense(n)
    def r_up(zf, z):
        if zf < L3: return arb(tab[int(math.floor(zf))][1])
        return 4 / PI**2 * z + arb(fmpq(3038, 1000)) * z.sqrt() + arb(fmpq(5744, 1000)) * z.sqrt().sqrt()
    total = arb(0); extra = arb(0); worst = 0.0
    for i in range(9906):
        s, e = mids[i], mids[i + 1]; zf, z = zs[i]
        c1 = (e.log().log() - e.li() / e) - (s.log().log() - s.li() / s)
        c2 = 2 * (s.log() + 2) / s.sqrt() - 2 * (e.log() + 2) / e.sqrt()
        ls = s.log(); lam = 2 * z.log() / ls
        if not (lam < arb(fmpq(1, 2))): lam = arb(fmpq(1, 2))
        cpi = 1 / (8 * PI) + (1 / (2 * PI) + 3 / ls) * lam + 1 / (4 * PI * ls) + 6 / ls**2 + li2u / (s.sqrt() * ls)
        term = 2 * (c1 / V_low(zf, z) + cpi * c2 * r_up(zf, z)**2)
        up = term.upper(); stated = arb(iv[i][2])
        rel = abs(float(((up - stated) / stated).mid()))
        worst = max(worst, rel)
        if rel > 1e-18: fail("interval %d: stated term %s != recomputed %s" % (i, iv[i][2], up.str(20, radius=False)))
        total += up; extra += 2 * z / s            # pi_2(x) <= S(A,P,z) + pi_2(z), pi_2(z) <= z: adds <= 2 z_i / m_i
    print("check 1-2: 9906 intervals admissible; stated terms match recomputation (max rel diff %.1e)" % worst)
    tail = 32 * pi2u / mids[-1].log() + 8 / mids[-1].sqrt()
    head = arb(fmpq(1840518, 10**6)) - 2 * arb(fmpz(3023463123235320)) / (arb(4) * arb(10)**18)
    Btot = total + tail + head + extra
    print("sum of interval bounds <= %s; pi_2(z) correction <= %s" % (total.upper().str(15, radius=False), extra.upper().str(3, radius=False)))
    # (3) V-lemma constant
    Pm = 10**7; sv = bytearray([1]) * (Pm + 1); sv[0] = sv[1] = 0
    for q in range(2, int(Pm**0.5) + 1):
        if sv[q]: sv[q*q::q] = bytearray(len(range(q*q, Pm + 1, q)))
    s_ = arb(fmpq(44, 100)); logS = arb(0)
    for p in range(3, Pm + 1, 2):
        if sv[p]: pa = arb(p); logS += (1 + (2 * pa**s_ + pa**(2 * s_)) / (pa * (pa - 2))).log()
    tailp = lambda b: arb(fmpq(125506, 100000)) * b * arb(Pm)**(1 - b) / ((b - 1) * arb(Pm).log())
    logS += arb(Pm + 1) / arb(Pm - 1) * (2 * tailp(2 - s_) + tailp(2 - 2 * s_))
    kappa = (arb.const_euler() + arb(2).log()) / 2
    if not (kappa + 4 >= 1 / (2 * s_)): fail("Rankin max not at u = 1")
    Abound = (kappa + 12) * arb(10)**(-10 * s_) * logS.exp()
    if not (Abound <= A): fail("A(1e10) bound %s exceeds 0.0107001" % Abound.upper().str(10, radius=False))
    print("check 3: A(1e10) <= %s <= 0.0107001" % Abound.upper().str(10, radius=False))
    print("B <= %s (sup of the ball)" % Btot.upper().str(20, radius=False))
    if not (Btot < CLAIM): fail("total not below 2.156967")
    print("check 4: B < 2.156967")
    print("PASS")


if __name__ == "__main__":
    try:
        main()
    except Fail as e:
        print("FAIL reason:", e); print("FAIL"); sys.exit(1)
    except Exception:
        traceback.print_exc(); print("FAIL reason: malformed or inconsistent input"); print("FAIL"); sys.exit(1)
