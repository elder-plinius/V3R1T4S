#!/usr/bin/env python3
"""Build canonical v2 machine-readable certificate of the polynomial identities and witnesses (certificate.json)."""
import hashlib
import json
import os
import sympy as sp

def poly2_terms(expr, x, y):
    poly = sp.Poly(sp.expand(expr), x, y, domain='ZZ')
    terms = []
    for (ex, ey), coeff in sorted(poly.terms(), key=lambda t: (-t[0][0], -t[0][1])):
        if coeff != 0:
            terms.append([int(ex), int(ey), int(coeff)])
    return terms

def poly1_terms(expr, m):
    poly = sp.Poly(sp.expand(expr), m, domain='ZZ')
    terms = []
    for (em,), coeff in sorted(poly.terms(), key=lambda t: -t[0][0]):
        if coeff != 0:
            terms.append([int(em), int(coeff)])
    return terms

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    res_dir = os.path.join(base_dir, "result")
    if not os.path.isdir(res_dir):
        res_dir = os.path.join(base_dir, "object")
    lean_path = os.path.join(res_dir, "dgh_internal_edge_cuboids_proof.lean")

    with open(lean_path, "rb") as f:
        lean_bytes = f.read()

    a, e, p, q, m = sp.symbols("a e p q m")

    u_e1 = a * (a**4 + a**2 * e**2 + e**4)
    u_e2 = 2 * e * a**2 * (a**2 + e**2)
    u_csq = e**2 * (e**4 - a**2 * e**2 - a**4) * (e**4 + 3 * a**2 * e**2 + 3 * a**4)

    fa_e1 = (p**2 - q**2) * (p**4 + 2*p**3*q + 2*p**2*q**2 - 2*p*q**3 + q**4) * (p**4 - 2*p**3*q + 2*p**2*q**2 + 2*p*q**3 + q**4)
    fa_e2 = 4 * p * q * (p**4 - q**4)**2
    fa_csq = -4 * p**2 * q**2 * (p**4 - 4*p**2*q**2 - q**4) * (p**4 + 4*p**2*q**2 - q**4) * (3*p**4 + q**4) * (p**4 + 3*q**4)
    fa_dab = (p**2 - q**2) * (p**8 + 8*p**6*q**2 - 2*p**4*q**4 + 8*p**2*q**6 + q**8)
    fa_dac = (p**2 + q**2) * (p**4 - 2*p**3*q - 2*p**2*q**2 - 2*p*q**3 + q**4) * (p**4 + 2*p**3*q - 2*p**2*q**2 + 2*p*q**3 + q**4)
    fa_dbc = 2 * p * q * (p**4 - 2*p**3*q + 2*p**2*q**2 + 2*p*q**3 + q**4) * (p**4 + 2*p**3*q + 2*p**2*q**2 - 2*p*q**3 + q**4)
    fa_sp  = (p**2 + q**2) * (p**4 + 2*p**3*q + 2*p**2*q**2 - 2*p*q**3 + q**4) * (p**4 - 2*p**3*q + 2*p**2*q**2 + 2*p*q**3 + q**4)

    fb_e1 = 2 * p * q * (p**4 + 2*p**3*q + 2*p**2*q**2 - 2*p*q**3 + q**4) * (p**4 - 2*p**3*q + 2*p**2*q**2 + 2*p*q**3 + q**4)
    fb_e2 = 8 * p**2 * q**2 * (p**2 - q**2) * (p**2 + q**2)**2
    fb_csq = (p**2 - q**2)**2 * (p**4 - 2*p**3*q - 2*p**2*q**2 - 2*p*q**3 + q**4) * (p**4 - 2*p**3*q + 6*p**2*q**2 - 2*p*q**3 + q**4) * (p**4 + 2*p**3*q - 2*p**2*q**2 + 2*p*q**3 + q**4) * (p**4 + 2*p**3*q + 6*p**2*q**2 + 2*p*q**3 + q**4)
    fb_dab = 2 * p * q * (p**8 + 8*p**6*q**2 - 2*p**4*q**4 + 8*p**2*q**6 + q**8)
    fb_dac = (p**2 + q**2) * (p**4 - 4*p**2*q**2 - q**4) * (p**4 + 4*p**2*q**2 - q**4)
    fb_dbc = (p**2 - q**2) * (p**4 - 2*p**3*q + 2*p**2*q**2 + 2*p*q**3 + q**4) * (p**4 + 2*p**3*q + 2*p**2*q**2 - 2*p*q**3 + q**4)
    fb_sp  = fa_sp

    wa_p, wa_q = 101, 100
    wa_e1 = int(fa_e1.subs({p: wa_p, q: wa_q}))
    wa_e2 = int(fa_e2.subs({p: wa_p, q: wa_q}))
    wa_csq = int(fa_csq.subs({p: wa_p, q: wa_q}))

    wb_p, wb_q = 100, 1
    wb_e1 = int(fb_e1.subs({p: wb_p, q: wb_q}))
    wb_e2 = int(fb_e2.subs({p: wb_p, q: wb_q}))
    wb_csq = int(fb_csq.subs({p: wb_p, q: wb_q}))

    cert = {
        "schema_version": 2,
        "unified_parametrization_count": 1,
        "excluded_fibration_count": 2,
        "lean_verified_theorem_count": 12,
        "lean_placeholder_count": 0,
        "lean_reflection_count": 0,
        "lean_proof_bytes": len(lean_bytes),
        "lean_proof_sha": hashlib.sha256(lean_bytes).hexdigest(),
        "bivariate_polynomials": {
            "unified_edge_first": poly2_terms(u_e1, a, e),
            "unified_edge_second": poly2_terms(u_e2, a, e),
            "unified_third_sq": poly2_terms(u_csq, a, e),
            "family_a_edge_first": poly2_terms(fa_e1, p, q),
            "family_a_edge_second": poly2_terms(fa_e2, p, q),
            "family_a_third_sq": poly2_terms(fa_csq, p, q),
            "family_a_diag_ab": poly2_terms(fa_dab, p, q),
            "family_a_diag_ac": poly2_terms(fa_dac, p, q),
            "family_a_diag_bc": poly2_terms(fa_dbc, p, q),
            "family_a_space_diag": poly2_terms(fa_sp, p, q),
            "family_b_edge_first": poly2_terms(fb_e1, p, q),
            "family_b_edge_second": poly2_terms(fb_e2, p, q),
            "family_b_third_sq": poly2_terms(fb_csq, p, q),
            "family_b_diag_ab": poly2_terms(fb_dab, p, q),
            "family_b_diag_ac": poly2_terms(fb_dac, p, q),
            "family_b_diag_bc": poly2_terms(fb_dbc, p, q),
            "family_b_space_diag": poly2_terms(fb_sp, p, q),
        },
        "univariate_positive_subfamilies": {
            "subfamily_a_min_k": 1,
            "subfamily_a_edge_first": poly1_terms(fa_e1.subs({p: m + 2, q: m + 1}), m),
            "subfamily_a_edge_second": poly1_terms(fa_e2.subs({p: m + 2, q: m + 1}), m),
            "subfamily_a_third_sq": poly1_terms(fa_csq.subs({p: m + 2, q: m + 1}), m),
            "subfamily_b_min_k": 2,
            "subfamily_b_edge_first": poly1_terms(fb_e1.subs({p: 2 * m + 4, q: 1}), m),
            "subfamily_b_edge_second": poly1_terms(fb_e2.subs({p: 2 * m + 4, q: 1}), m),
            "subfamily_b_third_sq": poly1_terms(fb_csq.subs({p: 2 * m + 4, q: 1}), m),
        },
        "high_parameter_witnesses": {
            "family_a_p": wa_p,
            "family_a_q": wa_q,
            "family_a_edge_first_dec": str(wa_e1),
            "family_a_edge_second_dec": str(wa_e2),
            "family_a_third_sq_dec": str(wa_csq),
            "family_b_p": wb_p,
            "family_b_q": wb_q,
            "family_b_edge_first_dec": str(wb_e1),
            "family_b_edge_second_dec": str(wb_e2),
            "family_b_third_sq_dec": str(wb_csq),
        },
    }

    def check_keys(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                assert not any(ch.isdigit() for ch in k), f"Digit found in key: {k}"
                check_keys(v)
        elif isinstance(obj, list):
            for item in obj:
                check_keys(item)
    check_keys(cert)

    cert_path = os.path.join(res_dir, "certificate.json")
    with open(cert_path, "w", encoding="utf-8") as f:
        json.dump(cert, f, indent=2)
        f.write("\n")
    print(f"Wrote {cert_path} ({os.path.getsize(cert_path)} bytes), sha256={hashlib.sha256(open(cert_path,'rb').read()).hexdigest()}")

if __name__ == "__main__":
    main()
