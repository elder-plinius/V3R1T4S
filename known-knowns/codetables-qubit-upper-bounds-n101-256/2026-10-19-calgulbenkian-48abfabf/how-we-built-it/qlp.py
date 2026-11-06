#!/usr/bin/env python3
"""High-precision simplex for the qubit stabilizer-code LP and exact Farkas certificate extraction.

Rows (integer coefficients, scaled by 2^(n-k)); see check_cert.py for the definitions:
  E0: A_0 = 1;  E1: sum A_i = 2^(n-k);  Q_j (1<=j<d): MacW_j(A) - 2^(n-k) A_j = 0;
  G_j (d<=j<=n): MacW_j(A) - 2^(n-k) A_j >= 0;  H_j (0<=j<=n, optional): sum (-1)^i K_j(i) A_i >= 0.
Phase-1 simplex in flint arb (ball arithmetic, midpoints used for decisions) with column scaling.
If Phase 1 ends with positive infeasibility, the row duals form a Farkas certificate; it is rationalised,
repaired exactly (shift along E1), and verified exactly in integers before being returned.
"""
import sys, json, time
from fractions import Fraction
from math import comb
import flint
from flint import arb, arb_mat, fmpq, fmpz


def kraw_table(n):
    """K[j][i] = coefficient of z^j in (1+3z)^(n-i) (1-z)^i, exact Python ints."""
    p3 = [[1]]
    for e in range(1, n + 1):  # (1+3z)^e
        prev = p3[-1]
        cur = [0] * (e + 1)
        for t, c in enumerate(prev):
            cur[t] += c
            cur[t + 1] += 3 * c
        p3.append(cur)
    K = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        poly = p3[n - i]
        for _ in range(i):  # multiply by (1 - z)
            nxt = poly + [0]
            for t in range(len(poly)):
                nxt[t + 1] -= poly[t]
            poly = nxt
        for j in range(n + 1):
            K[j][i] = poly[j]
    return K


def build_rows(n, k, d, shadow, K=None, window=None):
    """Return list of (name, coeffs[int]*(n+1), rhs int, kind) with kind 'eq' or 'ge'.
    window=w keeps only G_j and H_j with j <= d-1+w (a relaxation: any Farkas certificate of the subset is a
    certificate of the full system, because omitted rows simply get multiplier 0)."""
    if K is None:
        K = kraw_table(n)
    S = 2 ** (n - k)
    rows = []
    rows.append(("E0", [1] + [0] * n, 1, "eq"))
    rows.append(("E1", [1] * (n + 1), S, "eq"))
    for j in range(1, n + 1):
        if window is not None and j >= d and j > d - 1 + window:
            continue
        coef = list(K[j])
        coef[j] -= S
        rows.append((("Q%d" if j < d else "G%d") % j, coef, 0, "eq" if j < d else "ge"))
    if shadow:
        for j in range(n + 1):
            if window is not None and j > d - 1 + window:
                continue
            coef = [K[j][i] if i % 2 == 0 else -K[j][i] for i in range(n + 1)]
            rows.append(("H%d" % j, coef, 0, "ge"))
    return rows


def exact_verify(n, k, d, shadow, rows, y):
    """y: dict name -> Fraction multiplier. Returns (ok, value, maxcol)."""
    m = n + 1
    col = [Fraction(0)] * m
    val = Fraction(0)
    for name, coef, rhs, kind in rows:
        t = y.get(name, 0)
        if not t:
            continue
        if kind == "ge" and t < 0:
            return False, None, None
        for i in range(m):
            if coef[i]:
                col[i] += t * coef[i]
        val += t * rhs
    return (val > 0 and max(col) <= 0), val, max(col)


def to_cert(n, k, d, shadow, y):
    """Scale rational multipliers to integers and emit the JSON certificate."""
    from math import lcm
    L = 1
    for t in y.values():
        L = lcm(L, Fraction(t).denominator)
    cert = {"n": n, "k": k, "d": d, "shadow": shadow, "u_E0": "0", "u_E1": "0", "u_Q": {}, "v_G": {}, "v_H": {}}
    for name, t in y.items():
        z = Fraction(t) * L
        assert z.denominator == 1
        z = int(z)
        if z == 0:
            continue
        if name == "E0":
            cert["u_E0"] = str(z)
        elif name == "E1":
            cert["u_E1"] = str(z)
        else:
            cert[{"Q": "u_Q", "G": "v_G", "H": "v_H"}[name[0]]][name[1:]] = str(z)
    from math import gcd
    g = 0
    for key in ("u_E0", "u_E1"):
        g = gcd(g, int(cert[key]))
    for key in ("u_Q", "v_G", "v_H"):
        for v in cert[key].values():
            g = gcd(g, int(v))
    if g > 1:
        cert["u_E0"], cert["u_E1"] = str(int(cert["u_E0"]) // g), str(int(cert["u_E1"]) // g)
        for key in ("u_Q", "v_G", "v_H"):
            cert[key] = {j: str(int(v) // g) for j, v in cert[key].items()}
    return cert


def rationalize(x, bits=400):
    """Round an arb midpoint to a dyadic rational with `bits` bits after the leading bit."""
    f = x.mid()
    if f == 0:
        return Fraction(0)
    man, exp = f.man_exp()
    man, exp = int(man), int(exp)
    sh = man.bit_length() - bits
    if sh > 0:
        man = (man + (1 << (sh - 1))) >> sh
        exp += sh
    return Fraction(man) * (Fraction(2) ** exp)


def solve_phase1(n, k, d, shadow, prec=1536, K=None, max_iter=20000, log=None, tol_exp=-400, perturb_bits=120, window=None):
    """Phase-1 simplex. Returns dict(status='infeasible', cert=...) or dict(status='feasible') or other."""
    flint.ctx.prec = prec
    rows = build_rows(n, k, d, shadow, K, window)
    m = len(rows)
    nv = n + 1
    # column scaling: s_i ~ size of A_i in a random-like code, so scaled variables are O(1)
    S = 2 ** (n - k)
    # Standard form rows:  eq rows: coef.x + art = rhs (art basic);  ge rows: -coef.x + slack = 0 (slack basic)
    eq_idx = [r for r in range(m) if rows[r][3] == "eq"]
    ge_idx = [r for r in range(m) if rows[r][3] == "ge"]
    # columns: x (nv), slack for ge rows, art for eq rows
    ncol = nv + len(ge_idx) + len(eq_idx)
    colscale = []
    for i in range(nv):
        mx = max(abs(rows[r][1][i]) for r in range(m))
        colscale.append(mx)
    T = []
    rhs = []
    rowscale = []
    for r in range(m):
        name, coef, b, kind = rows[r]
        sgn = 1 if kind == "eq" else -1
        vals = [Fraction(sgn * coef[i], colscale[i]) for i in range(nv)]
        mx = max(abs(v) for v in vals)
        if b:
            mx = max(mx, abs(Fraction(b)))
        rowscale.append(mx)
        T.append([v / mx for v in vals])
        rhs.append(Fraction(b) / mx)
    # anti-degeneracy: tiny deterministic pseudo-random perturbation of every rhs (exactness is restored
    # by the final integer verification of the unperturbed system)
    import random
    rng = random.Random(12345 + 7 * n + 13 * k + d)
    for r in range(m):
        rhs[r] += Fraction(rng.randint(1 << 20, 1 << 21), 1 << (20 + perturb_bits))
    # make rhs >= 0
    for r in range(m):
        if rhs[r] < 0:
            T[r] = [-v for v in T[r]]
            rhs[r] = -rhs[r]
            rowscale[r] = -rowscale[r]
    # dense tableau in arb: m rows x (ncol + 1) cols (last = rhs)
    W = ncol + 1
    data = []
    gpos = {r: nv + t for t, r in enumerate(ge_idx)}
    apos = {r: nv + len(ge_idx) + t for t, r in enumerate(eq_idx)}
    basis = [0] * m
    for r in range(m):
        line = [arb(fmpq(v.numerator, v.denominator)) for v in T[r]] + [arb(0)] * (ncol - nv) + [
            arb(fmpq(rhs[r].numerator, rhs[r].denominator))]
        if r in gpos:
            # row was negated if rowscale<0; slack coefficient follows the same sign as constructed (+1 before flip)
            line[gpos[r]] = arb(1 if rowscale[r] > 0 else -1)
            basis[r] = gpos[r]
        else:
            line[apos[r]] = arb(1 if rowscale[r] > 0 else -1)
            basis[r] = apos[r]
        data.extend(line)
    # rows where the basic slack has coefficient -1 (only possible if rhs was 0 and we flipped) -> unflip
    M = arb_mat(m, W, data)
    for r in range(m):
        if float(M[r, basis[r]].mid()) < 0:
            for c in range(W):
                M[r, c] = -M[r, c]
            rowscale[r] = -rowscale[r]
    # Phase-1 cost: 1 on artificial columns. reduced cost row z_c = c_c - sum_{art rows} M[r,c]
    cost = [0] * ncol
    for r in eq_idx:
        cost[apos[r]] = 1
    zrow = arb_mat(1, W, [arb(cost[c]) if c < ncol else arb(0) for c in range(W)])
    for r in eq_idx:
        zrow = zrow - arb_mat(1, W, [M[r, c] for c in range(W)])
    tol = arb(2) ** tol_exp
    it = 0
    degenerate_run = 0
    bland = False
    t0 = time.time()
    while it < max_iter:
        it += 1
        zl = [float(zrow[0, c].mid()) if True else 0 for c in range(ncol)]
        # entering column: most negative reduced cost (Dantzig) or first negative (Bland)
        cand = [c for c in range(ncol) if zl[c] < 0 and zrow[0, c].mid() < -tol]
        cand = [c for c in cand if not (c >= nv + len(ge_idx))]  # never re-enter artificials
        if not cand:
            break
        e = cand[0] if bland else min(cand, key=lambda c: zl[c])
        colv = [M[r, e] for r in range(m)]
        best = None
        for r in range(m):
            a = colv[r]
            if a.mid() > tol:
                ratio = M[r, ncol] / a
                key = (float(ratio.mid()) if ratio.mid() > tol else 0.0, basis[r] if bland else -float(a.mid()))
                if best is None or key < best[0]:
                    best = (key, r)
        if best is None:
            return {"status": "unbounded?", "iters": it}
        p = best[1]
        if best[0][0] == 0.0:
            degenerate_run += 1
            if degenerate_run > 50:
                bland = True
        else:
            degenerate_run = 0
            bland = False
        piv = M[p, e]
        prow = arb_mat(1, W, [M[p, c] / piv for c in range(W)])
        ccol = arb_mat(m, 1, colv)
        M = M - ccol * prow
        for c in range(W):
            M[p, c] = prow[0, c]
        zrow = zrow - arb_mat(1, 1, [zrow[0, e]]) * prow
        M = M.mid()          # drop ball radii: plain multiprecision floating point
        zrow = zrow.mid()
        basis[p] = e
        if log and it % 50 == 0:
            log("  it %d obj %.3e bland=%s %.1fs" % (it, -float(zrow[0, ncol].mid()), bland, time.time() - t0))
    obj = -zrow[0, ncol]  # phase-1 objective value (sum of scaled artificials)
    objf = float(obj.mid())
    info = {"iters": it, "phase1_obj": objf, "secs": round(time.time() - t0, 1)}
    if obj.mid() <= tol:
        info["status"] = "feasible"
        return info
    # Duals of stored rows: for a column whose original tableau column was +-e_r with cost c: z = c - y_r*(+-1)
    y = {}
    for r in range(m):
        if r in gpos:
            colid, c0 = gpos[r], 0
        else:
            colid, c0 = apos[r], 1
        yr = arb(c0) - zrow[0, colid]   # dual of the (possibly sign-flipped) stored row
        # stored row r = (sign) * (original row)/|rowscale| with column scaling; constraint form:
        #   eq: coef.x = b  -> stored = coef.x/rowscale
        #   ge: -coef.x + slack = 0 -> stored = -coef.x/rowscale + slack
        name = rows[r][0]
        yq = rationalize(yr)
        sc = rowscale[r]
        if rows[r][3] == "eq":
            y[name] = yq / sc
        else:
            y[name] = -yq / sc
    for nm in list(y):
        if nm[0] in "GH" and y[nm] < 0:
            y[nm] = Fraction(0)
    # exact repair: shift along E1 so every column coefficient is <= 0
    ok, val, mc = exact_verify(n, k, d, shadow, rows, y)
    if mc is not None and mc > 0:
        y["E1"] = y.get("E1", 0) - mc
        ok, val, mc = exact_verify(n, k, d, shadow, rows, y)
    info["status"] = "infeasible" if ok else "infeasible_unverified"
    if ok:
        info["cert"] = to_cert(n, k, d, shadow, y)
    return info


if __name__ == "__main__":
    n, k, d = map(int, sys.argv[1:4])
    shadow = len(sys.argv) > 4 and sys.argv[4] == "shadow"
    r = solve_phase1(n, k, d, shadow, log=lambda s: print(s, flush=True))
    cert = r.pop("cert", None)
    print(json.dumps(r))
    if cert:
        fn = "cert_%d_%d_%d_%s.json" % (n, k, d, "sh" if shadow else "ns")
        json.dump(cert, open(fn, "w"))
        print("wrote", fn)
