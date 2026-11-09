"""Standalone check of the #23 site percolation threshold claim, written from the definitions, Python standard library
only (no numpy, no compiled code).

Checks, in order:
 1. integrity: the sha256 of every archive in object/mc/ARCHIVES.sha256 and of every data file listed in the object
    JSON (the histograms are read from the archives, see how-we-built-it/pack_mc.py);
 2. the lattice: rows S S S T of unit squares (S) and unit triangles (T) built from geometry; at every vertex of a
    period the neighbours at unit distance, the angular gaps between them (60 degrees = a triangle, 90 = a square),
    hence the vertex configuration; the fractions and zbar must be those of Wikipedia's row 23:
    (1/2)(3^3,4^2) + (1/2)(4^4), z = 5, 4, zbar = 4.5;
 3. method A: the transfer-matrix root series p_c(n) are extrapolated by the frozen rule (ansatz p_c(n) = p_c +
    sum_k A_k n^-e_k, exponents 4, 6, 8, 10 when the local exponent of the three largest n is within 0.5 of an even
    integer >= 4; fits K = 1..4, j = 0, 1, 2 on windows of K+1 consecutive n ending at n_max - j and least squares on the
    K+1+j largest n, n >= 4; p_TM = median, sigma_TM = largest distance from it), here in exact rational arithmetic;
 4. method B: for every Monte Carlo torus size (L2 >= 16) the crossing p_L of the wrapping probabilities from the block
    histograms (R_0D(n) = P(n < n1): no wrapping cluster yet; R_2D(n) = P(n >= n2): a cluster wrapping both ways;
    canonical curves R(p) = sum_n Binom(M, n, p) R(n); p_L = root of R_2D(p) = R_0D(p)), its jackknife error over
    blocks, and the weighted least-squares fit p_L = p_MC + A L2^-4 (sigma from the covariance, times
    sqrt(chi2/dof) when that exceeds 1);
 5. the criterion's numeric conditions: sigma <= 2e-6; (a) |p_TM - p_MC| <= 3 sqrt(s_TM^2 + s_MC^2); (b) within 3
    combined sigma of the table's 0.5720(2); (c) the bond threshold of #23 by the same transfer-matrix code within
    1e-6 of the table's 0.45844622 with sigma <= 1e-7, the Monte Carlo bond value within 3 sigma of it with sigma <=
    2e-6, and the Monte Carlo kagome site value within 3 sigma of the exact 1 - 2 sin(pi/18) with sigma <= 2e-6;
 6. every number stated in the object JSON equals the recomputed one (to its printed precision).
The last line printed is PASS or FAIL.

usage: python check_threshold.py <object folder>
"""
import hashlib
import json
import math
import os
import re
import sys
import tarfile
from fractions import Fraction

FAILS = []
MEMBERS = {}                                  # mc/<dataset>/<file> -> bytes, read from the archives


def load_archives(obj):
    """Read every archive listed in object/mc/ARCHIVES.sha256 into MEMBERS; return the archives whose sha256 or
    members are wrong."""
    bad, mc = [], os.path.join(obj, "mc")
    for line in open(os.path.join(mc, "ARCHIVES.sha256")):
        h, name = line.split(None, 1)
        path = os.path.join(mc, name.strip())
        if not os.path.isfile(path) or hashlib.sha256(open(path, "rb").read()).hexdigest() != h:
            bad.append(name.strip())
            continue
        with tarfile.open(path, "r:xz") as t:
            for m in t.getmembers():
                if not m.isfile() or not m.name.startswith("mc/") or m.name in MEMBERS:
                    bad.append("%s: %s" % (name.strip(), m.name))
                    continue
                MEMBERS[m.name] = t.extractfile(m).read()
    return bad


def data(obj, f):
    if f in MEMBERS:
        return MEMBERS[f]
    p = os.path.join(obj, f)
    return open(p, "rb").read() if os.path.isfile(p) else None


def check(cond, msg):
    print(("ok    " if cond else "FAIL  ") + msg)
    if not cond:
        FAILS.append(msg)


# ---------- 2. lattice ----------

def lattice_rows(pattern):
    """Vertices of one period (x mod 1) and the cell vector a2 for a row pattern of S and T, unit edges."""
    h = {"S": 1.0, "T": math.sqrt(3) / 2}
    lines, y, shift = [], 0.0, 0.0
    for r in pattern:
        lines.append((y, shift))
        y += h[r]
        if r == "T":
            shift = (shift + 0.5) % 1.0
    return lines, (shift, y)


def vertex_configs(pattern, reps=3):
    lines, (sx, H) = lattice_rows(pattern)
    pts = []
    for k in range(-1, reps + 1):
        for (y, s) in lines:
            for i in range(-3, 4):
                pts.append((i + s + k * sx, y + k * H))
    out = []
    for (y, s) in lines:                      # one vertex per row line per period (period 1 along x)
        p = (s + sx, y + H)                   # the copy in the second repetition (k = 1, i = 0)
        nb = [q for q in pts if abs(math.hypot(q[0] - p[0], q[1] - p[1]) - 1.0) < 1e-9]
        ang = sorted(math.degrees(math.atan2(q[1] - p[1], q[0] - p[0])) % 360 for q in nb)
        gaps = [round((ang[(i + 1) % len(ang)] - ang[i]) % 360) for i in range(len(ang))]
        faces = [3 if g == 60 else 4 if g == 90 else 0 for g in gaps]
        out.append((len(nb), faces))
    return out


def canon(faces):
    rots = [tuple(faces[i:] + faces[:i]) for i in range(len(faces))]
    rots += [tuple(reversed(r)) for r in rots]
    return min(rots)


def name(c):
    s, i = [], 0
    while i < len(c):
        j = i
        while j < len(c) and c[j] == c[i]:
            j += 1
        s.append("%d^%d" % (c[i], j - i) if j - i > 1 else "%d" % c[i])
        i = j
    return ".".join(s)


def check_lattice():
    vc = vertex_configs("SSST")
    names = [name(canon(f)) for z, f in vc]
    fr = {}
    for n in names:
        fr[n] = fr.get(n, Fraction(0)) + Fraction(1, len(names))
    zbar = sum(Fraction(z) for z, f in vc) / len(vc)
    angle_ok = all(0 not in f and sum(60 if x == 3 else 90 for x in f) == 360 for z, f in vc)
    print("lattice SSST: vertex configurations %s, fractions %s, zbar %s" % (names, {k: str(v) for k, v in fr.items()}, zbar))
    check(angle_ok, "every vertex is surrounded by unit triangles and squares filling 360 degrees")
    want = {"3^3.4^2": Fraction(1, 2), "4^4": Fraction(1, 2)}
    alt = {"4^2.3^3": Fraction(1, 2), "4^4": Fraction(1, 2)}
    check(fr in (want, alt) and zbar == Fraction(9, 2) and sorted(set(z for z, f in vc)) == [4, 5],
          "lattice is (1/2)(3^3,4^2) + (1/2)(4^4), z = 5, 4, zbar = 9/2 (Wikipedia row 23)")
    return zbar


# ---------- 3. transfer-matrix extrapolation ----------

def read_series(path):
    vals = {}
    for line in open(path):
        t = line.split()
        if len(t) > 5 and t[0] == "n":
            vals[int(t[1])] = Fraction(t[t.index("pc") + 1])
    return vals


def local_exponent(vals):
    n = max(vals)
    r = float((vals[n] - vals[n - 1]) / (vals[n - 1] - vals[n - 2]))
    g = lambda e: (n ** -e - (n - 1) ** -e) / ((n - 1) ** -e - (n - 2) ** -e) - r
    lo, hi = 0.5, 30.0
    if g(lo) * g(hi) > 0:
        return None
    for _ in range(200):
        m = (lo + hi) / 2
        if g(lo) * g(m) <= 0:
            hi = m
        else:
            lo = m
    return (lo + hi) / 2


def solve(A, b):
    n = len(A)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        piv = next(r for r in range(c, n) if M[r][c] != 0)
        M[c], M[piv] = M[piv], M[c]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c] / M[c][c]
                M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [M[i][n] / M[i][i] for i in range(n)]


def fit(vals, ns, exps):
    A = [[Fraction(1)] + [Fraction(1, n ** e) for e in exps] for n in ns]
    b = [vals[n] for n in ns]
    if len(ns) == len(exps) + 1:
        return solve(A, b)[0]
    At = list(zip(*A))
    AtA = [[sum(x * y for x, y in zip(ri, rj)) for rj in At] for ri in At]
    Atb = [sum(x * y for x, y in zip(ri, b)) for ri in At]
    return solve(AtA, Atb)[0]


def extrapolate(vals):
    ns_all = sorted(n for n in vals if n >= 4)
    nmax = ns_all[-1]
    e = local_exponent(vals)
    near = round(e / 2) * 2 if e is not None else 0
    if e is None or (near >= 4 and abs(e - near) <= 0.5):
        exps4 = [4, 6, 8, 10]
    else:
        exps4 = [int(round(e)) + k for k in range(4)]
    ests = []
    for K in range(1, 5):
        exps = exps4[:K]
        for j in range(3):
            win = list(range(nmax - j - K, nmax - j + 1))
            if all(n in vals and n >= 4 for n in win):
                ests.append(fit(vals, win, exps))
            st = ns_all[-(K + 1 + j):]
            if len(st) == K + 1 + j and st[0] >= 4:
                ests.append(fit(vals, st, exps))
    ests.sort()
    m = len(ests)
    med = ests[m // 2] if m % 2 else (ests[m // 2 - 1] + ests[m // 2]) / 2
    sig = max(abs(v - med) for v in ests)
    return float(med), float(sig), nmax, e, m


# ---------- 4. Monte Carlo crossing and fit ----------

def read_hist(name):
    lines = MEMBERS[name].decode("ascii").splitlines()
    head = lines[0].split()
    meta = dict(zip(head[0::2], head[1::2]))
    rows = [tuple(int(x) for x in line.split()) for line in lines[1:] if line.strip()]
    return meta, rows


class Curve:
    def __init__(self, M):
        self.M = M
        self.lgM = math.lgamma(M + 1)

    def weights(self, p):
        M = self.M
        sd = math.sqrt(M * p * (1 - p))
        lo = max(0, int(M * p - 14 * sd) - 2)
        hi = min(M, int(M * p + 14 * sd) + 2)
        lp, lq = math.log(p), math.log1p(-p)
        lw = [self.lgM - math.lgamma(n + 1) - math.lgamma(M - n + 1) + n * lp + (M - n) * lq for n in range(lo, hi + 1)]
        mx = max(lw)
        w = [math.exp(x - mx) for x in lw]
        s = sum(w)
        return lo, [x / s for x in w]


def diff_curve(h1, h2, lo, hi):
    """D(n) = R_2D(n) - R_0D(n) for n = lo..hi from the counts of n1 and n2 (dicts n -> count), where
    R_0D(n) = 1 - #(n1 <= n)/S and R_2D(n) = #(n2 <= n)/S."""
    S = sum(h1.values())
    c1 = sum(c for n, c in h1.items() if n < lo)
    c2 = sum(c for n, c in h2.items() if n < lo)
    D = []
    for n in range(lo, hi + 1):
        c1 += h1.get(n, 0)
        c2 += h2.get(n, 0)
        D.append(c2 / S - (1.0 - c1 / S))
    return lo, D


def root(cv, curve, a, b, cache):
    off, D = curve

    def f(p):
        if p not in cache:
            cache[p] = cv.weights(p)
        lo, w = cache[p]
        if lo < off or lo + len(w) > off + len(D):
            raise ValueError("canonical window outside the tabulated range")
        return sum(x * D[lo - off + i] for i, x in enumerate(w))
    fa, fb = f(a), f(b)
    if not fa < 0 < fb:
        raise ValueError("crossing not bracketed")
    side = 0
    for _ in range(200):                      # Illinois regula falsi
        c = (a * fb - b * fa) / (fb - fa)
        fc = f(c)
        if fc < 0:
            a, fa = c, fc
            if side == -1:
                fb /= 2
            side = -1
        else:
            b, fb = c, fc
            if side == 1:
                fa /= 2
            side = 1
        if b - a < 1e-13 or fc == 0:
            break
    return c


def crossing(paths):
    blocks, M = [], None
    for p in paths:
        meta, rows = read_hist(p)
        M = int(meta["M"])
        blocks.append(({n: a for n, a, b in rows}, {n: b for n, a, b in rows}))
    H1, H2 = {}, {}
    for h1, h2 in blocks:
        for n, a in h1.items():
            H1[n] = H1.get(n, 0) + a
        for n, b in h2.items():
            H2[n] = H2.get(n, 0) + b
    cv, cache = Curve(M), {}
    p_all = root(cv, diff_curve(H1, H2, 0, M), 0.05, 0.95, cache)
    sd = math.sqrt(M * 0.25)
    lo = max(0, int(M * (p_all - 0.01) - 15 * sd) - 5)
    hi = min(M, int(M * (p_all + 0.01) + 15 * sd) + 5)
    jk = []
    for h1, h2 in blocks:
        r1 = {n: H1[n] - h1.get(n, 0) for n in H1}
        r2 = {n: H2[n] - h2.get(n, 0) for n in H2}
        jk.append(root(cv, diff_curve(r1, r2, lo, hi), p_all - 0.01, p_all + 0.01, {}))
    nb = len(jk)
    mj = sum(jk) / nb
    err = math.sqrt((nb - 1) / nb * sum((x - mj) ** 2 for x in jk))
    return int(meta["L1"]), int(meta["L2"]), nb, p_all, err


def mc_fit(folder):
    groups = {}
    for p in sorted(n for n in MEMBERS if n.startswith(folder + "/") and n.endswith(".hist")):
        m = re.search(r"_L(\d+)x(\d+)_s\d+_b\d+\.hist$", p)
        groups.setdefault((int(m.group(1)), int(m.group(2))), []).append(p)
    rows = []
    for (L1, L2), paths in sorted(groups.items(), key=lambda t: t[0][1]):
        if L2 < 16:
            continue
        r = crossing(paths)
        print("  %s L%dx%d blocks %d  p_L %.9f +- %.2e" % (os.path.basename(folder), r[0], r[1], r[2], r[3], r[4]))
        rows.append(r)
    # weighted least squares p_L = p + A L2^-4
    W = [1 / r[4] ** 2 for r in rows]
    X = [r[1] ** -4.0 for r in rows]
    Y = [r[3] for r in rows]
    s0, s1, s2 = sum(W), sum(w * x for w, x in zip(W, X)), sum(w * x * x for w, x in zip(W, X))
    t0, t1 = sum(w * y for w, y in zip(W, Y)), sum(w * x * y for w, x, y in zip(W, X, Y))
    det = s0 * s2 - s1 * s1
    p = (s2 * t0 - s1 * t1) / det
    A = (s0 * t1 - s1 * t0) / det
    chi2 = sum(w * (y - p - A * x) ** 2 for w, x, y in zip(W, X, Y))
    dof = len(rows) - 2
    s = math.sqrt(s2 / det)
    if dof > 0 and chi2 / dof > 1:
        s *= math.sqrt(chi2 / dof)
    print("  fit L2 >= 16: p_MC %.9f +- %.2e  chi2/dof %.2f/%d" % (p, s, chi2, dof))
    return p, s, [r[1] for r in rows], [r[2] for r in rows]


# ---------- main ----------

def main():
    obj = sys.argv[1]
    J = json.load(open(os.path.join(obj, "threshold_23_site.json")))
    print("== 1 integrity")
    bad = load_archives(obj)
    check(not bad, "sha256 of the archives in object/mc/ARCHIVES.sha256 (%d problems)" % len(bad))
    listed = set(f for f in J["files"] if f.startswith("mc/"))
    check(set(MEMBERS) == listed, "the archives hold exactly the %d histogram files listed in the object (%d held)" % (
        len(listed), len(MEMBERS)))
    bad = [f for f, h in J["files"].items() if data(obj, f) is None or hashlib.sha256(data(obj, f)).hexdigest() != h]
    check(not bad, "sha256 of %d data files listed in the object (%d mismatches)" % (len(J["files"]), len(bad)))
    if FAILS:
        print("FAIL")
        sys.exit(1)
    print("== 2 lattice")
    zbar = check_lattice()
    check(float(zbar) == J["lattice"]["zbar"], "stated zbar %s" % J["lattice"]["zbar"])
    print("== 3 transfer matrix (frozen extrapolation rule, exact rational arithmetic)")
    tm = {}
    for key, f in (("site", "tm/r23_site_series.txt"), ("bond", "tm/r23_bond_series.txt")):
        p, s, nmax, e, m = extrapolate(read_series(os.path.join(obj, f)))
        tm[key] = (p, s)
        print("  #23 %s: n_max %d, local exponent %.3f, %d estimates: p_TM %.14f sigma_TM %.3e" % (key, nmax, e, m, p, s))
        st = J["tm"][key]
        check(nmax == st["n_max"] and abs(p - st["p"]) < 1e-13 and abs(s - st["sigma"]) <= 0.006 * st["sigma"],
              "#23 %s TM recomputed equals the stated %.14f +- %.3g (n_max %d)" % (key, st["p"], st["sigma"], st["n_max"]))
    print("== 4 Monte Carlo (crossing of the wrapping probabilities, jackknife, L2^-4 fit over L2 >= 16)")
    mc = {}
    for key, folder in (("site", "mc/r23_site"), ("bond", "mc/r23_bond"), ("kagome", "mc/kagome_site")):
        p, s, sizes, blocks = mc_fit(folder)
        mc[key] = (p, s)
        st = J["mc"][key]
        check(abs(p - st["p"]) <= 1e-9 and abs(s - st["sigma"]) <= 0.006 * st["sigma"] and sizes == st["L2"]
              and blocks == st["blocks"], "%s MC recomputed equals the stated %.9f +- %.4g (sizes %s, blocks %s)" % (
                  key, st["p"], st["sigma"], st["L2"], st["blocks"]))
    print("== 5 criterion (numeric parts)")
    pT, sT = tm["site"]
    pM, sM = mc["site"]
    comb = math.hypot(sT, sM)
    T = J["table"]
    check(sT <= 2e-6, "stated one-sigma uncertainty %.3g <= 2e-6" % sT)
    check(abs(pT - pM) <= 3 * comb, "(a) |TM - MC| = %.3e <= 3 combined sigma %.3e (%.2f sigma)" % (
        abs(pT - pM), 3 * comb, abs(pT - pM) / comb))
    check(abs(pT - T["site"]) <= 3 * math.hypot(sT, T["site_sigma"]),
          "(b) |TM - table %.4f| = %.3e <= 3 combined sigma" % (T["site"], abs(pT - T["site"])))
    pb, sb = tm["bond"]
    check(abs(pb - T["bond"]) < 1e-6 and sb <= 1e-7, "(c) TM bond %.10f within 1e-6 of the table %.8f (sigma %.2g <= 1e-7)" % (
        pb, T["bond"], sb))
    pmb, smb = mc["bond"]
    check(abs(pmb - T["bond"]) <= 3 * smb and smb <= 2e-6, "(c) MC bond %.9f within 3 sigma of the table (sigma %.3g <= 2e-6)" % (
        pmb, smb))
    K = 1 - 2 * math.sin(math.pi / 18)
    pk, sk = mc["kagome"]
    check(abs(pk - K) <= 3 * sk and sk <= 2e-6, "(c) MC kagome site %.9f within 3 sigma of 1 - 2 sin(pi/18) = %.9f (%.2f sigma)" % (
        pk, K, (pk - K) / sk))
    print("== 6 claimed value")
    cv = J["claimed"]
    check(abs(cv["p_c"] - pT) < 5e-9 and abs(cv["sigma"] - sT) < 5e-9,
          "claimed %.8f +- %.8f equals the TM value rounded" % (cv["p_c"], cv["sigma"]))
    print("FAIL" if FAILS else "PASS")
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
