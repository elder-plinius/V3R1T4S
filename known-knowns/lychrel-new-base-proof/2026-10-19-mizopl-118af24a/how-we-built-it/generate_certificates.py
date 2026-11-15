#!/usr/bin/env python3
"""
Generate the exact JSON certificates for:
1) lychrel_base50_certificate.json (Base 50 = 2 * 5^2, Period 4)
2) lychrel_base98_certificate.json (Base 98 = 2 * 7^2, Period 4)
3) lychrel_base146_certificate.json (Base 146 = 2 * 73, Period 4)
4) seal_base26_baseline_certificate.json (David Seal 1996 Base 26 baseline, Period 4)
5) kuitche_2023_audit.json (Audit of Kuitche 2023 preprint rs-2659802 across bases 3..10)
"""
import json, os, hashlib
from search_engines import solve_outer_period2
from search_inner import solve_inner_period4, add_lists

CLAIM_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "claim")
os.makedirs(CLAIM_DIR, exist_ok=True)

def digits_to_int(digits, b):
    val = 0
    for d in digits:
        val = val * b + d
    return val

def make_symbolic_blocks(prefix, left_digit, mid, right_digit, suffix):
    """
    Create normalized run-length symbolic blocks.
    Each block is {"digit": d, "a": a, "c": c} representing d^(a*m + c) for integer m >= 1.
    """
    raw = []
    for d in prefix:
        raw.append((d, 0, 1))
    raw.append((left_digit, 1, 0))
    for d in mid:
        raw.append((d, 0, 1))
    raw.append((right_digit, 1, 0))
    for d in suffix:
        raw.append((d, 0, 1))
    # Merge adjacent blocks with identical digit:
    merged = []
    for d, a, c in raw:
        if merged and merged[-1][0] == d:
            prev_d, prev_a, prev_c = merged[-1]
            merged[-1] = (prev_d, prev_a + a, prev_c + c)
        else:
            merged.append((d, a, c))
    return [{"digit": d, "a": a, "c": c} for d, a, c in merged]

def build_period4_certificate(b, label):
    L0, R0 = solve_outer_period2(b, max_len=200)
    M0 = solve_inner_period4(b, max_layers=200)
    assert L0 is not None and M0 is not None, f"Failed to solve for base {b}"

    R1, cR0 = add_lists(R0, L0[::-1], b, 0)
    M1, cM0 = add_lists(M0, M0[::-1], b, 0)
    L1, cL0 = add_lists(L0, R0[::-1], b, 1)
    assert (cR0, cM0, cL0) == (0, 1, 0)

    R2_raw, cR1 = add_lists(R1, L1[::-1], b, 0)
    M2_raw, cM1 = add_lists(M1, M1[::-1], b, 1)
    L2_raw, cL1 = add_lists(L1, R1[::-1], b, 0)
    assert (cR1, cM1, cL1) == (1, 0, 1)
    assert R2_raw == R0
    assert [1] + L2_raw[:-1] == L0 and L2_raw[-1] == b - 1

    M2 = [b - 1] + M2_raw
    M3, cM2 = add_lists(M2, M2[::-1], b, 0)
    assert cM2 == 1

    M4_raw, cM3 = add_lists(M3, M3[::-1], b, 1)
    assert cM3 == 0 and M4_raw == M0 + [0]

    # Start number n = T_1(1):
    T1_m1_digits = L0 + [b - 1] + M0 + [0] + R0
    n_int = digits_to_int(T1_m1_digits, b)

    # Pre-template seed n_seed (outside {T_1..T_4} at step 0, enters T_2(1) at step 1):
    # Replace L0[0]=1 with 2 and R0[-1]=b-3 with b-4 so their sum is still b-2!
    seed_digits = list(T1_m1_digits)
    seed_digits[0] = 2
    seed_digits[-1] = R0[-1] - 1
    seed_int = digits_to_int(seed_digits, b)

    templates = [
        {
            "name": "T_1(m)",
            "phase": 0,
            "prefix": L0,
            "left_repeat_digit": b - 1,
            "middle": M0,
            "right_repeat_digit": 0,
            "suffix": R0,
            "normalized_rle_blocks": make_symbolic_blocks(L0, b - 1, M0, 0, R0),
            "next_template": "T_2(m)",
            "carries": {"c_R": 0, "c_M": 1, "c_L": 0}
        },
        {
            "name": "T_2(m)",
            "phase": 1,
            "prefix": L1,
            "left_repeat_digit": 0,
            "middle": M1,
            "right_repeat_digit": b - 1,
            "suffix": R1,
            "normalized_rle_blocks": make_symbolic_blocks(L1, 0, M1, b - 1, R1),
            "next_template": "T_3(m)",
            "carries": {"c_R": 1, "c_M": 0, "c_L": 1}
        },
        {
            "name": "T_3(m)",
            "phase": 2,
            "prefix": L0,
            "left_repeat_digit": b - 1,
            "middle": M2,
            "right_repeat_digit": 0,
            "suffix": R0,
            "normalized_rle_blocks": make_symbolic_blocks(L0, b - 1, M2, 0, R0),
            "next_template": "T_4(m)",
            "carries": {"c_R": 0, "c_M": 1, "c_L": 0}
        },
        {
            "name": "T_4(m)",
            "phase": 3,
            "prefix": L1,
            "left_repeat_digit": 0,
            "middle": M3,
            "right_repeat_digit": b - 1,
            "suffix": R1,
            "normalized_rle_blocks": make_symbolic_blocks(L1, 0, M3, b - 1, R1),
            "next_template": "T_1(m+1)",
            "carries": {"c_R": 1, "c_M": 0, "c_L": 1}
        }
    ]

    cert = {
        "base": b,
        "label": label,
        "is_power_of_two": (b & (b - 1)) == 0,
        "in_known_set_11_17_20_26": b in (11, 17, 20, 26),
        "period": 4,
        "parameter_threshold_m0": 1,
        "outer_length": len(L0),
        "inner_length_even_phases": len(M0),
        "inner_length_odd_phases": len(M2),
        "start_n_T1_m1_digits": T1_m1_digits,
        "start_n_T1_m1_base10": str(n_int),
        "start_n_T1_m1_length_in_base_b": len(T1_m1_digits),
        "pre_template_seed_digits": seed_digits,
        "pre_template_seed_base10": str(seed_int),
        "pre_template_seed_enters_at_step": 1,
        "pre_template_seed_target": "T_2(1)",
        "L0": L0,
        "R0": R0,
        "L1": L1,
        "R1": R1,
        "M0": M0,
        "M1": M1,
        "M2": M2,
        "M3": M3,
        "templates": templates
    }
    return cert

def build_kuitche_audit():
    """
    Audit of Rostand S. Kuitche (2023), 'On the Construction of Some Lychrel Numbers',
    Research Square rs-2659802/v1 (DOI: 10.21203/rs.3.rs-2659802/v1).
    Section 4 Case 1 defines the template family in base b (written for b=4 with digit b-1=3, b-2=2):
      x_0 = [b-1, b-2, b-1]
      y_0 = [1, 0] + x_0 + [0, 0]
      For p >= 1:
        y_{2p-1} = [1, 0] + [b-1]^p + [b-1, b-2, b-1] + [0]^p + [0, 0]
        y_{2p}   = [1, 0] + [b-1]^p + [b-1, b-2, b-1] + [0]^{p+1} + [0, 0]
      Claimed closure in base 4: phi^3(y_{2p-1}) = y_{2p} and phi^3(y_{2p}) = y_{2p+1}.
    We test this exact template family and start seed a = [b-1, b-1, b-1, b-1]_b = b^4 - 1
    across all bases b in {3, 4, 5, 6, 7, 8, 9, 10}.
    """
    def rev_add(d, b):
        out, c = add_lists(d, d[::-1], b, 0)
        if c: out = [c] + out
        return out

    results = []
    for b in range(3, 11):
        # 1) Test Kuitche's y_1 (p=1): [1, 0, b-1, b-1, b-2, b-1, 0, 0, 0]
        y1 = [1, 0, b - 1, b - 1, b - 2, b - 1, 0, 0, 0]
        y2_paper = [1, 0, b - 1, b - 1, b - 2, b - 1, 0, 0, 0, 0]
        y2_corrected = [1, 0, b - 1, b - 1, b - 1, b - 2, b - 1, 0, 0, 0]
        y3_expected = [1, 0, b - 1, b - 1, b - 1, b - 2, b - 1, 0, 0, 0, 0]
        cur = list(y1)
        iterates_y1 = [cur]
        palindrome_step_y1 = None
        for s in range(1, 25):
            cur = rev_add(cur, b)
            iterates_y1.append(cur)
            if cur == cur[::-1] and palindrome_step_y1 is None:
                palindrome_step_y1 = s
        phi3_y1 = iterates_y1[3]
        phi6_y1 = iterates_y1[6]
        closure_phi3_paper = (phi3_y1 == y2_paper)
        closure_phi3_corrected = (phi3_y1 == y2_corrected)
        closure_phi6 = (phi6_y1 == y3_expected)

        # 2) Test seed a = [b-1, b-1, b-1, b-1]_b (in base 4, 3333_4 = 255)
        seed = [b - 1, b - 1, b - 1, b - 1]
        cur_s = list(seed)
        pal_step_seed = None
        pal_digits_seed = None
        for s in range(1, 50):
            cur_s = rev_add(cur_s, b)
            if cur_s == cur_s[::-1]:
                pal_step_seed = s
                pal_digits_seed = cur_s
                break

        results.append({
            "base": b,
            "is_power_of_two": (b & (b - 1)) == 0,
            "y1_digits": y1,
            "phi1_y1_digits": iterates_y1[1],
            "phi2_y1_digits": iterates_y1[2],
            "phi3_y1_digits": phi3_y1,
            "phi6_y1_digits": phi6_y1,
            "y2_paper_digits": y2_paper,
            "y2_corrected_digits": y2_corrected,
            "y3_expected_digits": y3_expected,
            "template_closure_phi3_y1_eq_y2_paper": closure_phi3_paper,
            "template_closure_phi3_y1_eq_y2_corrected": closure_phi3_corrected,
            "template_closure_phi6_y1_eq_y3": closure_phi6,
            "y1_reaches_palindrome_at_step": palindrome_step_y1,
            "y1_palindrome_digits": iterates_y1[palindrome_step_y1] if palindrome_step_y1 else None,
            "seed_b4_minus_1_digits": seed,
            "seed_reaches_palindrome_at_step": pal_step_seed,
            "seed_palindrome_digits": pal_digits_seed
        })

    return {
        "paper_title": "On the Construction of Some Lychrel Numbers",
        "author": "Rostand S. Kuitche",
        "year": 2023,
        "doi": "10.21203/rs.3.rs-2659802/v1",
        "summary_of_paper_contents": (
            "Sections 2-3 prove four 1-step/2-step preimage equivalence relations (Propositions 3.1-3.4) "
            "in bases 3 <= b <= 10 showing phi(a) = phi(x) or phi^2(a) = phi^2(x) when adding b^(l-1)-1, "
            "(b-1)*b^(l/2-1), or sum_{k=1}^{l-3} (b-1)*b^k. Section 4 Case 1 gives an explicit template cycle "
            "only in base b = 4 (a power of 2, already known) for a = 3333_4 = 255. Section 4 Case 2 and Section 5 "
            "apply Propositions 3.1-3.4 in base b = 10 to unproved Lychrel candidates (196, 879, 1997, 7059) to "
            "generate sibling candidates (e.g. 4994, 8778, 19723, 89760, 58883, 43593) tested numerically to "
            "530,914 iterations without any template-closure proof."
        ),
        "base_3_to_10_mechanical_audit": results
    }

if __name__ == "__main__":
    cert50 = build_period4_certificate(50, "Primary new base b = 50 (Period-4 template cycle)")
    cert98 = build_period4_certificate(98, "Secondary new base b = 98 (Period-4 template cycle)")
    cert146 = build_period4_certificate(146, "Tertiary new base b = 146 (Period-4 template cycle)")
    cert26 = build_period4_certificate(26, "David Seal 1996 baseline b = 26 (Period-4 template cycle)")
    audit = build_kuitche_audit()

    files = [
        ("lychrel_base50_certificate.json", cert50),
        ("lychrel_base98_certificate.json", cert98),
        ("lychrel_base146_certificate.json", cert146),
        ("seal_base26_baseline_certificate.json", cert26),
        ("kuitche_2023_audit.json", audit),
    ]
    for fname, obj in files:
        p = os.path.join(CLAIM_DIR, fname)
        with open(p, "w", encoding="utf-8") as f:
            json.dump(obj, f, indent=2)
            f.write("\n")
        raw = open(p, "rb").read()
        h = hashlib.sha256(raw).hexdigest()
        print(f"{fname:38s}: {len(raw):6d} bytes, sha256={h}")

    for r in audit["base_3_to_10_mechanical_audit"]:
        print(f"Kuitche audit b={r['base']:2d}: phi3_paper={r['template_closure_phi3_y1_eq_y2_paper']}, "
              f"phi6={r['template_closure_phi6_y1_eq_y3']}, "
              f"y1_pal_step={r['y1_reaches_palindrome_at_step']}, seed_pal_step={r['seed_reaches_palindrome_at_step']}")
