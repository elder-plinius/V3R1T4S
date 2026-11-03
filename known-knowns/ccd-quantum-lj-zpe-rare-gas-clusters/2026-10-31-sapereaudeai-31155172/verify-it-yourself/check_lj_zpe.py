#!/usr/bin/env python3
"""Checker for bank target ccd-quantum-lj-zpe-rare-gas-clusters (V3R1T4S), written from the bank definition.

Definition (bank/targets.json, success_criterion, abridged here; target.md holds it verbatim):
  * coordinates (>= 12 digits) of N atoms forming a certified local minimum of the classical
    E_LJ = 4 sum_{i<j} (r^-12 - r^-6): gradient norm < 1e-9, analytic Hessian of that E_LJ with exactly
    6 eigenvalues of magnitude < 1e-6 and none below -1e-6;
  * E_sp = E_LJ + (q/2) sum sqrt(lambda_i) over the 3N-6 nonzero eigenvalues (unit masses),
    q = 0.01 (Xe), 0.03 (Ar), 0.095 (Ne);
  * a record needs E_sp STRICTLY LOWER by at least 5e-4 than the lowest tabulated value for that N and species;
  * the checker must first reproduce table rows from their posted point files to 5e-5 with the same code.

Pair sums run over i < j once (the bank's "factor-of-sqrt-2 trap" is a double-counted pair sum).
E_LJ and the gradient are evaluated in 50-digit decimal arithmetic straight from the coordinate strings
(both need only r^2); the Hessian and its eigenvalues are double precision (numpy).

Usage
  check_lj_zpe.py COORDS [--polish] [--write-polished OUT] [--expect SP=VALUE ...] [--tol 5e-5]
                         [--bar SP=VALUE ...] [--margin 5e-4] [--min-digits 12]
  check_lj_zpe.py --selftest
COORDS: one atom per line, "x y z" (Fortran D exponents accepted); an xyz header (count, comment) and a
leading element symbol are skipped. --polish (calibration only, never for a claim) Newton-polishes on the
classical surface first and reports how far the atoms moved. Exit code 0 iff every requested check passes.
"""
import argparse
import decimal
import math
import re
import sys

import numpy as np

Q = {"Xe": 0.01, "Ar": 0.03, "Ne": 0.095}
D = decimal.Decimal
CTX = decimal.Context(prec=50)
NUM_RE = re.compile(r"^[+-]?(\d+\.?\d*|\.\d+)([eEdD][+-]?\d+)?$")


# ---------- input ----------

def sig_digits(tok):
    """Significant digits as written; for an exact zero, the number of decimals written."""
    mant = re.split(r"[eEdD]", tok)[0].lstrip("+-")
    digits = mant.replace(".", "")
    if digits.strip("0"):
        return len(digits.lstrip("0"))
    return len(mant.partition(".")[2])


def parse_coords(path):
    toks = []
    with open(path, encoding="latin-1") as f:
        lines = [l.split() for l in f if l.strip()]
    if lines and len(lines[0]) == 1 and lines[0][0].isdigit():      # xyz header: count + comment line
        lines = lines[2:]
    for parts in lines:
        if len(parts) == 4 and not NUM_RE.match(parts[0]):
            parts = parts[1:]
        if len(parts) != 3 or not all(NUM_RE.match(p) for p in parts):
            raise ValueError("not an 'x y z' line: %r" % " ".join(parts))
        toks.append(parts)
    if len(toks) < 2:
        raise ValueError("fewer than 2 atoms")
    return toks


def to_decimal(tok):
    return CTX.create_decimal(tok.replace("D", "E").replace("d", "e"))


# ---------- evaluator ----------

def energy_grad_decimal(dec):
    """E_LJ and its gradient in 50-digit decimal arithmetic, pair sum over i < j."""
    n = len(dec)
    e = D(0)
    g = [[D(0)] * 3 for _ in range(n)]
    four, c48, c24 = D(4), D(48), D(24)
    with decimal.localcontext(CTX):
        for i in range(n):
            xi = dec[i]
            for j in range(i + 1, n):
                d = [xi[k] - dec[j][k] for k in range(3)]
                s = d[0] * d[0] + d[1] * d[1] + d[2] * d[2]
                s3 = s * s * s
                inv6 = 1 / s3
                inv12 = inv6 * inv6
                e += four * (inv12 - inv6)
                f = -c48 * inv12 / s + c24 * inv6 / s          # phi'(r)/r
                for k in range(3):
                    g[i][k] += f * d[k]
                    g[j][k] -= f * d[k]
    return e, g


def energy_grad_hess(x):
    """Double precision E_LJ, gradient (3N) and analytic Hessian (3N x 3N); pair sum over i < j."""
    n = len(x)
    iu, ju = np.triu_indices(n, 1)
    d = x[iu] - x[ju]
    s = np.einsum("ij,ij->i", d, d)
    inv6 = s ** -3
    e = float(np.sum(4.0 * (inv6 * inv6 - inv6)))
    f = -48.0 * inv6 * inv6 / s + 24.0 * inv6 / s                 # phi'/r
    g = np.zeros((n, 3))
    np.add.at(g, iu, f[:, None] * d)
    np.add.at(g, ju, -f[:, None] * d)
    a = 672.0 * s ** -8 - 192.0 * s ** -5                          # phi''/r^2 - phi'/r^3
    blocks = a[:, None, None] * d[:, :, None] * d[:, None, :] + f[:, None, None] * np.eye(3)[None]
    h = np.zeros((n, 3, n, 3))
    for p, (i, j) in enumerate(zip(iu, ju)):
        k = blocks[p]
        h[i, :, i, :] += k
        h[j, :, j, :] += k
        h[i, :, j, :] -= k
        h[j, :, i, :] -= k
    return e, g.reshape(-1), h.reshape(3 * n, 3 * n)


def polish(x, max_iter=60, tol=1e-13, max_step=0.05):
    """Newton polish on the classical surface; the 6 smallest-|lambda| (rigid-body) modes are projected out and
    |lambda| is used so a step never climbs. Calibration only."""
    x = x.copy()
    for it in range(max_iter):
        _, g, h = energy_grad_hess(x)
        if np.linalg.norm(g) < tol:
            return x, it
        lam, v = np.linalg.eigh(h)
        order = np.argsort(np.abs(lam))
        keep = order[6:]
        gc = v[:, keep].T @ g
        step = -(v[:, keep] @ (gc / np.abs(lam[keep])))
        m = np.max(np.abs(step))
        if m > max_step:
            step *= max_step / m
        x = x + step.reshape(-1, 3)
    return x, max_iter


# ---------- checks ----------

def certify(tokens, x_override=None, min_digits=12):
    """Return a dict of every quantity the criterion names, from the coordinates as given (or polished)."""
    out = {}
    if x_override is None:
        out["min_sig_digits"] = min(sig_digits(t) for row in tokens for t in row)
        out["digits_ok"] = out["min_sig_digits"] >= min_digits
        dec = [[to_decimal(t) for t in row] for row in tokens]
    else:
        out["min_sig_digits"] = 17
        out["digits_ok"] = True
        dec = [[CTX.create_decimal("%.17e" % float(c)) for c in row] for row in x_override]
    x = np.array([[float(c) for c in row] for row in dec])
    n = len(x)
    e_dec, g_dec = energy_grad_decimal(dec)
    gnorm = math.sqrt(float(sum(c * c for row in g_dec for c in row)))
    e_dbl, g_dbl, h = energy_grad_hess(x)
    lam = np.linalg.eigvalsh(h)
    small = np.abs(lam) < 1e-6
    out.update(N=n, E_LJ=float(e_dec), E_LJ_double=e_dbl, grad_norm=gnorm,
               grad_norm_double=float(np.linalg.norm(g_dbl)),
               n_zero_modes=int(small.sum()), lambda_min=float(lam[0]),
               zero_mode_max_abs=float(np.max(np.abs(lam[small]))) if small.any() else float("nan"),
               lambda_min_nonzero=float(np.min(lam[~small])) if (~small).any() else float("nan"))
    out["grad_ok"] = gnorm < 1e-9
    out["hess_ok"] = out["n_zero_modes"] == 6 and not np.any(lam < -1e-6)
    out["certified_minimum"] = out["digits_ok"] and out["grad_ok"] and out["hess_ok"]
    nz = lam[~small]
    root_sum = float(np.sum(np.sqrt(np.clip(nz, 0.0, None)))) if out["hess_ok"] else float("nan")
    out["sum_sqrt_lambda"] = root_sum
    for sp, q in Q.items():
        out["E_" + sp] = out["E_LJ"] + 0.5 * q * root_sum
    return out, x


def selftest():
    """Analytic gradient and Hessian against central finite differences on a random 6-atom cluster."""
    rng = np.random.default_rng(20261031)
    x = rng.uniform(-1.2, 1.2, (6, 3))
    while True:   # keep atoms apart so the finite differences are well conditioned
        dmin = min(np.linalg.norm(x[i] - x[j]) for i in range(6) for j in range(i))
        if dmin > 0.9:
            break
        x = rng.uniform(-1.4, 1.4, (6, 3))
    e, g, h = energy_grad_hess(x)
    hstep = 1e-5
    gf = np.zeros_like(g)
    hf = np.zeros_like(h)
    flat = x.reshape(-1)
    for k in range(flat.size):
        xp, xm = flat.copy(), flat.copy()
        xp[k] += hstep
        xm[k] -= hstep
        ep, gp, _ = energy_grad_hess(xp.reshape(-1, 3))
        em, gm, _ = energy_grad_hess(xm.reshape(-1, 3))
        gf[k] = (ep - em) / (2 * hstep)
        hf[:, k] = (gp - gm) / (2 * hstep)
    dec = [[CTX.create_decimal(repr(float(c))) for c in row] for row in x]
    e_dec, g_dec = energy_grad_decimal(dec)
    gd = np.array([float(c) for row in g_dec for c in row])
    rg = np.max(np.abs(g - gf)) / max(1.0, np.max(np.abs(g)))
    rh = np.max(np.abs(h - hf)) / max(1.0, np.max(np.abs(h)))
    rs = np.max(np.abs(h - h.T))
    print("selftest: E_double=%.15f E_decimal=%.15f" % (e, float(e_dec)))
    print("selftest: max rel |grad - finite diff| = %.3e" % rg)
    print("selftest: max rel |hess - finite diff| = %.3e" % rh)
    print("selftest: max |hess - hess^T| = %.3e" % rs)
    print("selftest: max |grad_double - grad_decimal| = %.3e" % np.max(np.abs(g - gd)))
    ok = rg < 1e-6 and rh < 1e-6 and rs < 1e-12 and abs(e - float(e_dec)) < 1e-10
    print("SELFTEST:", "PASS" if ok else "FAIL")
    return ok


def parse_pairs(items, what):
    out = {}
    for it in items or []:
        sp, _, val = it.partition("=")
        if sp not in Q:
            raise SystemExit("%s: species must be Xe, Ar or Ne, got %r" % (what, sp))
        out[sp] = float(val)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("coords", nargs="?")
    ap.add_argument("--polish", action="store_true", help="calibration only: Newton-polish before certifying")
    ap.add_argument("--write-polished")
    ap.add_argument("--expect", action="append", help="SP=VALUE: tabulated value to reproduce (calibration)")
    ap.add_argument("--tol", type=float, default=5e-5)
    ap.add_argument("--bar", action="append", help="SP=VALUE: lowest tabulated value for N (record test)")
    ap.add_argument("--margin", type=float, default=5e-4)
    ap.add_argument("--min-digits", type=int, default=12)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return 0 if selftest() else 1
    if not a.coords:
        ap.error("COORDS required")
    tokens = parse_coords(a.coords)
    expect, bar = parse_pairs(a.expect, "--expect"), parse_pairs(a.bar, "--bar")
    x0 = np.array([[float(to_decimal(t)) for t in row] for row in tokens])
    xp = None
    if a.polish:
        xp, iters = polish(x0)
        print("polish: %d Newton steps, max atom displacement %.3e" % (iters, float(np.max(np.linalg.norm(xp - x0, axis=1)))))
        if a.write_polished:
            with open(a.write_polished, "w", newline="\n") as f:
                for row in xp:
                    f.write("%.17e %.17e %.17e\n" % tuple(float(c) for c in row))
            print("polish: wrote", a.write_polished)
    if a.polish:
        print("input digits: min %d significant digits per coordinate" % min(sig_digits(t) for row in tokens for t in row))
    r, _ = certify(tokens, xp, a.min_digits)
    print("N = %d" % r["N"])
    print("min significant digits = %d (need >= %d): %s" % (r["min_sig_digits"], a.min_digits, "ok" if r["digits_ok"] else "FAIL"))
    print("E_LJ (50-digit decimal) = %.12f   (double: %.12f)" % (r["E_LJ"], r["E_LJ_double"]))
    print("gradient norm (decimal) = %.3e   (double: %.3e)  need < 1e-9: %s" % (r["grad_norm"], r["grad_norm_double"], "ok" if r["grad_ok"] else "FAIL"))
    print("Hessian: %d eigenvalues with |lambda| < 1e-6 (need exactly 6), lowest eigenvalue %.6e (need >= -1e-6), "
          "max |zero mode| %.3e, lowest nonzero %.6e: %s" % (r["n_zero_modes"], r["lambda_min"], r["zero_mode_max_abs"],
                                                          r["lambda_min_nonzero"], "ok" if r["hess_ok"] else "FAIL"))
    print("certified classical minimum: %s" % ("YES" if r["certified_minimum"] else "NO"))
    ok = r["certified_minimum"]
    if r["hess_ok"]:
        for sp in Q:
            print("E_%s = E_LJ + (%g/2) * sum sqrt(lambda) = %.6f" % (sp, Q[sp], r["E_" + sp]))
    for sp, v in expect.items():
        dv = r["E_" + sp] - v if r["hess_ok"] else float("nan")
        good = r["hess_ok"] and abs(dv) <= a.tol
        ok = ok and good
        print("calibration %s: computed %.6f vs tabulated %.5f, diff %.2e (tol %.0e): %s" % (sp, r["E_" + sp], v, dv, a.tol, "PASS" if good else "FAIL"))
    for sp, v in bar.items():
        gap = v - r["E_" + sp] if r["hess_ok"] else float("nan")
        win = r["certified_minimum"] and gap >= a.margin
        ok = ok and win
        print("record test %s: bar %.5f, E_sp %.6f, bar - E_sp = %.6f (need >= %.0e on a certified minimum): %s"
              % (sp, v, r["E_" + sp], gap, a.margin, "BEATS BAR" if win else "does not beat bar"))
    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
