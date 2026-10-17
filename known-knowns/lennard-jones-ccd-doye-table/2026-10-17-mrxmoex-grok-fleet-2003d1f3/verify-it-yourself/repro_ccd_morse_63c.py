#!/usr/bin/env python3
"""Repro for the CCD Morse table erratum 63C (rho0 = 3 cell: sign typo).
Python 3 standard library only. Downloads the live table page and the 63C points file at run time; nothing is bundled.
Energy: E = sum_{i<j} exp(rho (1 - r)) (exp(rho (1 - r)) - 2), pair well depth = 1, equilibrium pair distance = 1, as the CCD page states.
Steps: (1) parse the table row 63C and its rho0 column headers; (2) check the posted file at its own header rho0 (= 6) against the
table's rho0 = 6 cell (calibration); (3) relax the posted file at rho0 = 3 (L-BFGS, then Newton with the 6 rigid-body modes shifted out)
to a stationary point, count negative Hessian eigenvalues (Sylvester inertia of an LDL^T factorisation), and compare with the table cell."""
import csv, hashlib, html, math, os, re, sys, time, urllib.request
MORSE = "https://www-wales.ch.cam.ac.uk/~jon/structures/Morse"
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = {r["url"]: r for r in csv.DictReader(open(os.path.join(HERE, "..", "SOURCES.csv")))}
fails = []
def get(url):
    for k in range(3):  # small retry: some mirrors drop TLS handshakes intermittently
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "ccd-errata-repro"}), timeout=180) as r:
                b = r.read(); lm = r.headers.get("Last-Modified", ""); break
        except OSError as e:
            if k == 2: raise
            print(f"    retry {url}: {e}"); time.sleep(5)
    h = hashlib.sha256(b).hexdigest(); exp = SRC.get(url, {}).get("sha256", "")
    note = "" if not exp else ("sha256 matches SOURCES.csv" if h == exp else "NOTE: sha256 differs from SOURCES.csv (file updated since 2026-10-17?)")
    print(f"  {url}\n    {len(b)} B  sha256 {h}  Last-Modified {lm or '-'}  {note}")
    return b
def check(label, cond):
    print(f"  [{'ok' if cond else 'FAIL'}] {label}")
    if not cond: fails.append(label)
def dot(a, b): return sum(p * q for p, q in zip(a, b))
def morse(x, rho):
    n = len(x) // 3; E = 0.0; g = [0.0] * len(x)
    for i in range(n):
        xi, yi, zi = x[3 * i], x[3 * i + 1], x[3 * i + 2]
        for j in range(i + 1, n):
            dx = xi - x[3 * j]; dy = yi - x[3 * j + 1]; dz = zi - x[3 * j + 2]
            r = math.sqrt(dx * dx + dy * dy + dz * dz); ex = math.exp(rho * (1 - r)); E += ex * (ex - 2); f = -2 * rho * ex * (ex - 1) / r
            g[3 * i] += f * dx; g[3 * i + 1] += f * dy; g[3 * i + 2] += f * dz; g[3 * j] -= f * dx; g[3 * j + 1] -= f * dy; g[3 * j + 2] -= f * dz
    return E, g
def lbfgs(x, rho, m=10, gtol=1e-4, maxit=2000):
    E, g = morse(x, rho); S, Y = [], []
    for it in range(maxit):
        if max(map(abs, g)) < gtol: break
        q = g[:]; al = []
        for s, y in reversed(list(zip(S, Y))):
            a = dot(s, q) / dot(y, s); al.append(a); q = [qi - a * yi for qi, yi in zip(q, y)]
        gam = dot(S[-1], Y[-1]) / dot(Y[-1], Y[-1]) if S else 1e-3
        d = [gam * v for v in q]
        for (s, y), a in zip(zip(S, Y), reversed(al)):
            b = dot(y, d) / dot(y, s); d = [di + (a - b) * si for di, si in zip(d, s)]
        d = [-v for v in d]; gd = dot(g, d)
        if gd >= 0: d = [-v for v in g]; gd = dot(g, d); S, Y = [], []
        t = min(1.0, 0.1 / max(map(abs, d)))
        while True:
            xn = [a + t * b for a, b in zip(x, d)]; En, gn = morse(xn, rho)
            if En <= E + 1e-4 * t * gd or t < 1e-12: break
            t *= 0.5
        if t < 1e-12: break  # line search stalled (flat to machine precision): hand over to Newton
        s = [a - b for a, b in zip(xn, x)]; y = [a - b for a, b in zip(gn, g)]
        if dot(s, y) > 1e-12: S.append(s); Y.append(y)
        if len(S) > m: S.pop(0); Y.pop(0)
        x, E, g = xn, En, gn
    return x
def hessian_shifted(x, rho):
    """Analytic Hessian plus the projector onto the 6 rigid-body modes (shifts the 6 zero eigenvalues to +1)."""
    n = len(x) // 3; N = 3 * n; H = [[0.0] * N for _ in range(N)]
    for i in range(n):
        for j in range(i + 1, n):
            d = [x[3 * i + k] - x[3 * j + k] for k in range(3)]; r = math.sqrt(dot(d, d)); u = [v / r for v in d]
            e = math.exp(rho * (1 - r)); V1 = -2 * rho * e * (e - 1); V2 = 2 * rho * rho * e * (2 * e - 1)
            for a in range(3):
                for b in range(3):
                    h = (V2 - V1 / r) * u[a] * u[b] + (V1 / r if a == b else 0.0)
                    H[3 * i + a][3 * j + b] -= h; H[3 * j + a][3 * i + b] -= h; H[3 * i + a][3 * i + b] += h; H[3 * j + a][3 * j + b] += h
    c = [sum(x[3 * i + k] for i in range(n)) / n for k in range(3)]; modes = []
    for k in range(3):
        v = [0.0] * N
        for i in range(n): v[3 * i + k] = 1.0
        modes.append(v)
    for k in range(3):
        v = [0.0] * N; a, b = (k + 1) % 3, (k + 2) % 3
        for i in range(n): v[3 * i + a] = -(x[3 * i + b] - c[b]); v[3 * i + b] = x[3 * i + a] - c[a]
        modes.append(v)
    Z = []
    for v in modes:  # Gram-Schmidt
        for w in Z: f = dot(v, w); v = [p - f * q for p, q in zip(v, w)]
        nv = math.sqrt(dot(v, v)); Z.append([p / nv for p in v])
    for z in Z:
        for a in range(N):
            if z[a]:
                row = H[a]
                for b in range(N): row[b] += z[a] * z[b]
    return H
def solve(A, rhs):
    N = len(rhs); M = [A[i][:] + [rhs[i]] for i in range(N)]
    for k in range(N):
        p = max(range(k, N), key=lambda i: abs(M[i][k])); M[k], M[p] = M[p], M[k]; rk = M[k]
        for i in range(k + 1, N):
            f = M[i][k] / rk[k]
            if f:
                ri = M[i]
                for j in range(k, N + 1): ri[j] -= f * rk[j]
    out = [0.0] * N
    for i in range(N - 1, -1, -1): out[i] = (M[i][N] - sum(M[i][j] * out[j] for j in range(i + 1, N))) / M[i][i]
    return out
def inertia(A):
    """Number of negative pivots of a symmetric LDL^T (no pivoting) = number of negative eigenvalues (Sylvester)."""
    N = len(A); M = [r[:] for r in A]; neg = 0; small = float("inf")
    for k in range(N):
        piv = M[k][k]; small = min(small, abs(piv)); neg += piv < 0; rk = M[k]
        for i in range(k + 1, N):
            f = M[i][k] / piv
            if f:
                ri = M[i]
                for j in range(k, N): ri[j] -= f * rk[j]
    return neg, small
def newton(x, rho, maxit=20, tol=1e-9):
    for _ in range(maxit):
        E, g = morse(x, rho); gm = max(map(abs, g))
        if gm < tol: break
        dx = solve(hessian_shifted(x, rho), [-v for v in g]); s = max(map(abs, dx))
        if s > 0.1: dx = [v * 0.1 / s for v in dx]
        x = [a + b for a, b in zip(x, dx)]
    E, g = morse(x, rho); return x, E, max(map(abs, g))
print("1. CCD Morse table")
t = get(f"{MORSE}/tables.html").decode("latin-1")
hdr = [float(v) for v in re.findall(r'ALT="\$\\rho_0=(\d+(?:\.\d+)?)\$"', t)]
print(f"  rho0 column headers (ALT text, in page order): {hdr}")
cells, positive = None, []
for tr in re.findall(r"<tr.*?</tr>", t, re.S | re.I):
    m = re.search(r'href="points/([^"]+)"', tr, re.I)
    if not m: continue
    c = [html.unescape(re.sub(r"<[^>]*>", "", x)).replace("\xa0", " ").strip() for x in re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S | re.I)]
    positive += [(m.group(1), v) for v in c[4:8] if re.fullmatch(r"\+?\d+\.\d+(\[\d+\])?", v)]
    if m.group(1) == "63C": cells = c
row = dict(zip(hdr[:4], cells[4:8])); print(f"  row 63C (cells for rho0 = 3, 6, 10, 14): {cells[4:8]}")
mm = re.fullmatch(r"([-+]?\d+\.\d+)\s*(?:\[(\d+)\])?", row[3.0]); E3_table = float(mm.group(1)); idx_table = int(mm.group(2)) if mm.group(2) else 0
E6_table = float(re.sub(r"\[.*", "", row[6.0]))
check("column headers are rho0 = 3, 6, 10, 14", hdr[:4] == [3.0, 6.0, 10.0, 14.0])
check(f"63C rho0=3 cell reads '{row[3.0]}': positive value, saddle index bracket [1]", E3_table > 0 and idx_table == 1)
print(f"  positive energy cells in the whole table: {positive}")
check("63C rho0=3 is the only positive energy cell in the table", positive == [("63C", row[3.0])])
print("2. posted points file 63C at its own header rho0 (calibration)")
txt = get(f"{MORSE}/points/63C").decode("latin-1").split()
rho_hdr = float(txt[0]); x0 = [float(v) for v in txt[1:]]; n = len(x0) // 3
E6, g6 = morse(x0, rho_hdr); print(f"  header rho0 = {rho_hdr}, {n} atoms, E = {E6:.9f}, max|grad| = {max(map(abs, g6)):.1e}  (table rho0=6 cell {E6_table})")
check("file: header rho0 = 6, 63 atoms, stationary, E matches the rho0=6 cell to 1e-6", rho_hdr == 6.0 and n == 63 and len(x0) == 189 and max(map(abs, g6)) < 1e-6 and abs(E6 - E6_table) < 1e-6)
print("3. posted file relaxed at rho0 = 3")
x3, E3, gm3 = newton(lbfgs(x0, 3.0), 3.0); neg, small = inertia(hessian_shifted(x3, 3.0))
print(f"  stationary point: E = {E3:.9f}, max|grad| = {gm3:.1e}, Hessian index = {neg} (smallest |LDL pivot| {small:.3g})")
print(f"  table cell {row[3.0]}  ->  E_file + E_table = {E3 + E3_table:+.2e}  (same magnitude, opposite sign)")
check("stationary to 1e-8", gm3 < 1e-8)
check("E_file = -(table value) to 1e-6, i.e. the table's sign is wrong", E3 < 0 and abs(E3 + E3_table) < 1e-6)
check("Hessian index of that stationary point = 1 = the table's own [1] bracket", neg == idx_table == 1)
print("PASS" if not fails else f"FAIL ({len(fails)}): " + "; ".join(fails))
sys.exit(1 if fails else 0)
