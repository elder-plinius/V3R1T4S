#!/usr/bin/env python3
"""Independent pure-stdlib Python 3 verifier for perfect-cuboid p1 (v2).
Zero shared code with verify_c99.c and zero external dependencies beyond Python 3 stdlib.
"""
import hashlib
import json
import math
import os
import re
import sys

def fail(msg: str) -> None:
    sys.stderr.write(f"PYTHON_REJECT: {msg}\n")
    sys.exit(1)

def p2_clean(d):
    return {k: v for k, v in d.items() if v != 0}

def p2_add(a, b, scale_b=1):
    out = dict(a)
    for k, v in b.items():
        out[k] = out.get(k, 0) + scale_b * v
    return p2_clean(out)

def p2_mul(a, b):
    out = {}
    for (i1, j1), v1 in a.items():
        for (i2, j2), v2 in b.items():
            key = (i1 + i2, j1 + j2)
            out[key] = out.get(key, 0) + v1 * v2
    return p2_clean(out)

def p2_pow(base, exp):
    acc = {(0, 0): 1}
    for _ in range(exp):
        acc = p2_mul(acc, base)
    return acc

def p2_sub(u, sx, sy):
    out = {}
    for (ix, iy), cf in u.items():
        term = p2_mul(p2_pow(sx, ix), p2_pow(sy, iy))
        out = p2_add(out, term, cf)
    return out

def p2_eval_int(poly, x_val: int, y_val: int) -> int:
    return sum(cf * (x_val ** ix) * (y_val ** iy) for (ix, iy), cf in poly.items())

def p1_mul(a, b):
    out = {}
    for i1, v1 in a.items():
        for i2, v2 in b.items():
            out[i1 + i2] = out.get(i1 + i2, 0) + v1 * v2
    return {k: v for k, v in out.items() if v != 0}

def p1_pow(base, exp):
    acc = {0: 1}
    for _ in range(exp):
        acc = p1_mul(acc, base)
    return acc

def p2_to_p1(poly, mx, my):
    out = {}
    for (ix, iy), cf in poly.items():
        prod = p1_mul(p1_pow(mx, ix), p1_pow(my, iy))
        for deg, v in prod.items():
            out[deg] = out.get(deg, 0) + cf * v
    return {k: v for k, v in out.items() if v != 0}

def parse_p2_json(rows):
    if not isinstance(rows, list) or not rows:
        fail("empty or non-list bivariate polynomial")
    prev = None
    out = {}
    for row in rows:
        if not isinstance(row, list) or len(row) != 3 or not all(isinstance(x, int) and not isinstance(x, bool) for x in row):
            fail("malformed bivariate monomial")
        ex, ey, cf = row
        if ex < 0 or ey < 0 or cf == 0:
            fail("invalid exponent or zero coeff in bivariate polynomial")
        cur = (ex, ey)
        if prev is not None and cur >= prev:
            fail("bivariate polynomial not strictly descending")
        prev = cur
        out[cur] = cf
    return out

def parse_p1_json(rows):
    if not isinstance(rows, list) or not rows:
        fail("empty or non-list univariate polynomial")
    prev = None
    out = {}
    for row in rows:
        if not isinstance(row, list) or len(row) != 2 or not all(isinstance(x, int) and not isinstance(x, bool) for x in row):
            fail("malformed univariate monomial")
        em, cf = row
        if em < 0 or cf == 0:
            fail("invalid univariate monomial")
        if prev is not None and em >= prev:
            fail("univariate polynomial not strictly descending")
        prev = em
        out[em] = cf
    return out

def is_exact_sq(n: int) -> bool:
    if n < 0:
        return False
    r = math.isqrt(n)
    return r * r == n

def main() -> None:
    if len(sys.argv) != 2:
        fail("usage: verify_py.py <object_dir>")
    obj_dir = sys.argv[1]
    cert_path = os.path.join(obj_dir, "certificate.json")
    lean_path = os.path.join(obj_dir, "dgh_internal_edge_cuboids_proof.lean")

    for p in (cert_path, lean_path):
        if not os.path.isfile(p):
            fail(f"missing object file: {p}")

    with open(cert_path, "rb") as f:
        raw_cert = f.read()
    try:
        cert = json.loads(raw_cert.decode("utf-8"))
    except Exception as exc:
        fail(f"JSON parse error: {exc}")

    expected_top_keys = [
        "schema_version",
        "unified_parametrization_count",
        "excluded_fibration_count",
        "lean_verified_theorem_count",
        "lean_placeholder_count",
        "lean_reflection_count",
        "lean_proof_bytes",
        "lean_proof_sha",
        "bivariate_polynomials",
        "univariate_positive_subfamilies",
        "high_parameter_witnesses",
    ]
    if list(cert.keys()) != expected_top_keys:
        fail("top-level certificate keys mismatch")

    if (cert["schema_version"], cert["unified_parametrization_count"], cert["excluded_fibration_count"],
            cert["lean_verified_theorem_count"], cert["lean_placeholder_count"], cert["lean_reflection_count"]) != (2, 1, 2, 12, 0, 0):
        fail("header metadata constants mismatch")

    with open(lean_path, "rb") as f:
        lean_bytes = f.read()

    if cert["lean_proof_bytes"] != len(lean_bytes) or cert["lean_proof_sha"] != hashlib.sha256(lean_bytes).hexdigest():
        fail("lean_proof_bytes or lean_proof_sha mismatch")

    # Audit raw Lean source directly (even inside comments)
    lean_raw = lean_bytes.decode("utf-8")
    for forbidden in ("sorry", "native_decide", "admit", "ofReduceBool", "trustCompiler"):
        if forbidden in lean_raw:
            fail(f"forbidden substring '{forbidden}' found in Lean file")
    if re.search(r"(?m)^\s*axiom\b", lean_raw):
        fail("custom axiom declaration found in Lean file")
    print_axioms = re.findall(r"#print\s+axioms\s+PerfectCuboidDGH\.[A-Za-z0-9_]+", lean_raw)
    if len(print_axioms) != 12:
        fail(f"expected 12 #print axioms commands, found {len(print_axioms)}")

    # Parse and verify all 17 bivariate polynomials
    bp = cert["bivariate_polynomials"]
    biv_keys = [
        "unified_edge_first", "unified_edge_second", "unified_third_sq",
        "family_a_edge_first", "family_a_edge_second", "family_a_third_sq",
        "family_a_diag_ab", "family_a_diag_ac", "family_a_diag_bc", "family_a_space_diag",
        "family_b_edge_first", "family_b_edge_second", "family_b_third_sq",
        "family_b_diag_ab", "family_b_diag_ac", "family_b_diag_bc", "family_b_space_diag",
    ]
    if list(bp.keys()) != biv_keys:
        fail("bivariate_polynomials key order mismatch")
    polys = {k: parse_p2_json(bp[k]) for k in biv_keys}

    a_var, e_var = {(1, 0): 1}, {(0, 1): 1}
    a2, e2 = p2_pow(a_var, 2), p2_pow(e_var, 2)
    a4, e4 = p2_pow(a_var, 4), p2_pow(e_var, 4)
    def_u_e1 = p2_mul(a_var, p2_add(p2_add(a4, p2_mul(a2, e2)), e4))
    def_u_e2 = p2_mul({(0, 0): 2}, p2_mul(e_var, p2_mul(a2, p2_add(a2, e2))))
    f1 = p2_add(p2_add(e4, p2_mul(a2, e2), -1), a4, -1)
    f2 = p2_add(p2_add(e4, p2_mul(a2, e2), 3), a4, 3)
    def_u_csq = p2_mul(e2, p2_mul(f1, f2))

    if polys["unified_edge_first"] != def_u_e1 or polys["unified_edge_second"] != def_u_e2 or polys["unified_third_sq"] != def_u_csq:
        fail("unified defining polynomials mismatch")

    deg_u_e1 = max(i + j for (i, j) in def_u_e1)
    deg_u_csq = max(i + j for (i, j) in def_u_csq)

    p2_minus_q2 = {(2, 0): 1, (0, 2): -1}
    two_pq = {(1, 1): 2}
    if (p2_sub(def_u_e1, p2_minus_q2, two_pq) != polys["family_a_edge_first"] or
            p2_sub(def_u_e2, p2_minus_q2, two_pq) != polys["family_a_edge_second"] or
            p2_sub(def_u_csq, p2_minus_q2, two_pq) != polys["family_a_third_sq"]):
        fail("Family A unification mismatch")
    if (p2_sub(def_u_e1, two_pq, p2_minus_q2) != polys["family_b_edge_first"] or
            p2_sub(def_u_e2, two_pq, p2_minus_q2) != polys["family_b_edge_second"] or
            p2_sub(def_u_csq, two_pq, p2_minus_q2) != polys["family_b_third_sq"]):
        fail("Family B unification mismatch")

    for pref in ("family_a", "family_b"):
        pe1, pe2, pcsq = polys[f"{pref}_edge_first"], polys[f"{pref}_edge_second"], polys[f"{pref}_third_sq"]
        pdab, pdac, pdbc, psp = polys[f"{pref}_diag_ab"], polys[f"{pref}_diag_ac"], polys[f"{pref}_diag_bc"], polys[f"{pref}_space_diag"]
        pe1_2, pe2_2 = p2_mul(pe1, pe1), p2_mul(pe2, pe2)
        if p2_add(pe1_2, pe2_2) != p2_mul(pdab, pdab):
            fail(f"{pref} diag_ab^2 mismatch")
        if p2_add(pe1_2, pcsq) != p2_mul(pdac, pdac):
            fail(f"{pref} diag_ac^2 mismatch")
        if p2_add(pe2_2, pcsq) != p2_mul(pdbc, pdbc):
            fail(f"{pref} diag_bc^2 mismatch")
        if p2_add(p2_add(pe1_2, pe2_2), pcsq) != p2_mul(psp, psp):
            fail(f"{pref} space_diag^2 mismatch")
        for dpoly in (pdab, pdac, pdbc, psp):
            if p2_eval_int(dpoly, 4, 1) <= 0:
                fail(f"{pref} diagonal orientation not positive")

    # Univariate positive subfamilies
    up = cert["univariate_positive_subfamilies"]
    up_keys = [
        "subfamily_a_min_k", "subfamily_a_edge_first", "subfamily_a_edge_second", "subfamily_a_third_sq",
        "subfamily_b_min_k", "subfamily_b_edge_first", "subfamily_b_edge_second", "subfamily_b_third_sq",
    ]
    if list(up.keys()) != up_keys or up["subfamily_a_min_k"] != 1 or up["subfamily_b_min_k"] != 2:
        fail("univariate_positive_subfamilies metadata mismatch")
    for kname, bpoly, mx, my in [
        ("subfamily_a_edge_first", polys["family_a_edge_first"], {1: 1, 0: 2}, {1: 1, 0: 1}),
        ("subfamily_a_edge_second", polys["family_a_edge_second"], {1: 1, 0: 2}, {1: 1, 0: 1}),
        ("subfamily_a_third_sq", polys["family_a_third_sq"], {1: 1, 0: 2}, {1: 1, 0: 1}),
        ("subfamily_b_edge_first", polys["family_b_edge_first"], {1: 2, 0: 4}, {0: 1}),
        ("subfamily_b_edge_second", polys["family_b_edge_second"], {1: 2, 0: 4}, {0: 1}),
        ("subfamily_b_third_sq", polys["family_b_third_sq"], {1: 2, 0: 4}, {0: 1}),
    ]:
        got = parse_p1_json(up[kname])
        if got != p2_to_p1(bpoly, mx, my) or got.get(0, 0) <= 0 or any(v <= 0 for v in got.values()):
            fail(f"{kname} univariate positive verification failed")

    # High-parameter witnesses + 500 explicit math.isqrt checks
    hpw = cert["high_parameter_witnesses"]
    hpw_keys = [
        "family_a_p", "family_a_q", "family_a_edge_first_dec", "family_a_edge_second_dec", "family_a_third_sq_dec",
        "family_b_p", "family_b_q", "family_b_edge_first_dec", "family_b_edge_second_dec", "family_b_third_sq_dec",
    ]
    if list(hpw.keys()) != hpw_keys:
        fail("high_parameter_witnesses keys mismatch")
    wap, waq, wbp, wbq = hpw["family_a_p"], hpw["family_a_q"], hpw["family_b_p"], hpw["family_b_q"]
    if (wap, waq) != (101, 100) or (wbp, wbq) != (100, 1):
        fail("witness coordinates mismatch")

    wa_e1 = p2_eval_int(polys["family_a_edge_first"], wap, waq)
    wa_e2 = p2_eval_int(polys["family_a_edge_second"], wap, waq)
    wa_csq = p2_eval_int(polys["family_a_third_sq"], wap, waq)
    wb_e1 = p2_eval_int(polys["family_b_edge_first"], wbp, wbq)
    wb_e2 = p2_eval_int(polys["family_b_edge_second"], wbp, wbq)
    wb_csq = p2_eval_int(polys["family_b_third_sq"], wbp, wbq)
    if (hpw["family_a_edge_first_dec"], hpw["family_a_edge_second_dec"], hpw["family_a_third_sq_dec"]) != (str(wa_e1), str(wa_e2), str(wa_csq)):
        fail("Family A witness decimal mismatch")
    if (hpw["family_b_edge_first_dec"], hpw["family_b_edge_second_dec"], hpw["family_b_third_sq_dec"]) != (str(wb_e1), str(wb_e2), str(wb_csq)):
        fail("Family B witness decimal mismatch")

    checked_a = 0
    for k in range(1, 251):
        e1 = p2_eval_int(polys["family_a_edge_first"], k + 1, k)
        e2 = p2_eval_int(polys["family_a_edge_second"], k + 1, k)
        csq = p2_eval_int(polys["family_a_third_sq"], k + 1, k)
        if e1 <= 0 or e2 <= 0 or csq <= 0:
            fail("Family A non-positive")
        if not (is_exact_sq(e1 * e1 + e2 * e2) and is_exact_sq(e1 * e1 + csq) and is_exact_sq(e2 * e2 + csq) and is_exact_sq(e1 * e1 + e2 * e2 + csq)):
            fail("Family A diagonal not square")
        if is_exact_sq(csq):
            fail("Counterexample in Family A")
        checked_a += 1

    checked_b = 0
    for k in range(2, 252):
        e1 = p2_eval_int(polys["family_b_edge_first"], 2 * k, 1)
        e2 = p2_eval_int(polys["family_b_edge_second"], 2 * k, 1)
        csq = p2_eval_int(polys["family_b_third_sq"], 2 * k, 1)
        if e1 <= 0 or e2 <= 0 or csq <= 0:
            fail("Family B non-positive")
        if not (is_exact_sq(e1 * e1 + e2 * e2) and is_exact_sq(e1 * e1 + csq) and is_exact_sq(e2 * e2 + csq) and is_exact_sq(e1 * e1 + e2 * e2 + csq)):
            fail("Family B diagonal not square")
        if is_exact_sq(csq):
            fail("Counterexample in Family B")
        checked_b += 1

    print(f"PROVED_SUMMARY: unified_parametrizations={cert['unified_parametrization_count']} excluded_fibrations={cert['excluded_fibration_count']} lean_theorems={cert['lean_verified_theorem_count']} placeholder_count={cert['lean_placeholder_count']} reflection_count={cert['lean_reflection_count']}")
    print(f"PROVED_DEGREES: unified_edge_deg={deg_u_e1} unified_csq_deg={deg_u_csq}")
    print(f"PROVED_FIBERS_CHECKED: total={checked_a + checked_b} family_a={checked_a} family_b={checked_b} min_k_a=1 min_k_b=2 perfect_cuboids_found=0")
    print(f"PROVED_WITNESS_A: p={wap} q={waq} e1={wa_e1} e2={wa_e2} c_sq={wa_csq}")
    print(f"PROVED_WITNESS_B: p={wbp} q={wbq} e1={wb_e1} e2={wb_e2} c_sq={wb_csq}")
    print("PYTHON_VERIFIER: PASS")

if __name__ == "__main__":
    main()
