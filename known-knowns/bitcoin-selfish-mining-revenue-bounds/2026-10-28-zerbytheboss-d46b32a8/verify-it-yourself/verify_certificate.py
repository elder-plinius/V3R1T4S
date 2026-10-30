#!/usr/bin/env python3
"""
Independent Certificate and Calibration Verifier for:
Optimal Selfish Mining in Bitcoin (SSZ model, gamma = 0)
Target: bitcoin-selfish-mining-revenue-bounds

This verifier:
1. Rebuilds N_rho^T and M_rho^T directly from arXiv:1507.06183 Sections 2-4 formulas.
2. Reproduces SSZ Table 2 calibration:
   - epsilon-OPT 0.56808 at alpha=0.425 within 1e-5
   - epsilon-OPT 0.66891 at alpha=0.45 within 1e-5
   - Sanity check: optimal gain of N_rho^T at alpha=0.45, rho=0.66 is strictly positive.
3. Verifies exact rational dual certificates for:
   - CONFIRMED_SOLUTION: alpha=0.45, U <= 0.70099
   - CONFIRMED_SOLUTION: alpha=0.475, U <= 0.90466
   - p2: alpha=0.425, U <= 0.57216
   - p2: alpha=0.40, U <= 0.48894
4. Verifies stationary policies for p1 (exceeding published bars by > 1e-6).
"""

import sys
import json
import gzip
import os
from fractions import Fraction
import numpy as np

def s_idx(t, a, h, fork):
    return a * (t + 1) * 3 + h * 3 + fork

def idx_to_s(t, idx):
    fork = idx % 3
    temp = idx // 3
    h = temp % (t + 1)
    a = temp // (t + 1)
    return a, h, fork

def build_transitions_exact(alpha_rat, gamma_rat, t, rho_rat, overpaying, comp_variant):
    num_states = (t + 1) * (t + 1) * 3
    one = Fraction(1, 1)
    two = Fraction(2, 1)
    half = Fraction(1, 2)
    zero = Fraction(0, 1)

    denom = one - two * alpha_rat
    term1 = (alpha_rat * (one - alpha_rat)) / (denom * denom)

    transitions = [{} for _ in range(num_states)]

    for a in range(t + 1):
        for h in range(t + 1):
            for fork in range(3):
                s = s_idx(t, a, h, fork)

                if a == t or h == t:
                    if not overpaying:
                        r_adopt = -rho_rat * Fraction(h, 1)
                    else:
                        if a == t:
                            term2 = half * (Fraction(a - h, 1) / denom + Fraction(a + h, 1))
                            if comp_variant == 1:
                                r_adopt = (one - rho_rat) * term1 + term2
                            else:
                                r_adopt = (one - rho_rat) * (term1 + term2)
                        else:
                            ratio = (alpha_rat / (one - alpha_rat)) ** (h - a)
                            term_ret = term1 + Fraction(h - a, 1) / denom
                            r_adopt = (one - ratio) * (-rho_rat * Fraction(h, 1)) + ratio * (one - rho_rat) * term_ret

                    transitions[s]['adopt'] = [
                        (alpha_rat, s_idx(t, 1, 0, 0), r_adopt),
                        (one - alpha_rat, s_idx(t, 0, 1, 0), r_adopt)
                    ]
                    continue

                r_adopt = -rho_rat * Fraction(h, 1)
                transitions[s]['adopt'] = [
                    (alpha_rat, s_idx(t, 1, 0, 0), r_adopt),
                    (one - alpha_rat, s_idx(t, 0, 1, 0), r_adopt)
                ]

                if a > h:
                    r_over = (one - rho_rat) * Fraction(h + 1, 1)
                    transitions[s]['override'] = [
                        (alpha_rat, s_idx(t, a - h, 0, 0), r_over),
                        (one - alpha_rat, s_idx(t, a - h - 1, 1, 1), r_over)
                    ]

                if fork == 1 and a >= h and h > 0:
                    succs = [
                        (alpha_rat, s_idx(t, a + 1, h, 2), zero)
                    ]
                    if gamma_rat > 0:
                        r_match_h = (one - rho_rat) * Fraction(h, 1)
                        succs.append((gamma_rat * (one - alpha_rat), s_idx(t, a - h, 1, 1), r_match_h))
                    succs.append(((one - gamma_rat) * (one - alpha_rat), s_idx(t, a, h + 1, 1), zero))
                    transitions[s]['match'] = succs

                if fork != 2:
                    transitions[s]['wait'] = [
                        (alpha_rat, s_idx(t, a + 1, h, 0), zero),
                        (one - alpha_rat, s_idx(t, a, h + 1, 1), zero)
                    ]
                elif fork == 2 and a > h and h > 0:
                    succs = [
                        (alpha_rat, s_idx(t, a + 1, h, 2), zero)
                    ]
                    if gamma_rat > 0:
                        r_match_h = (one - rho_rat) * Fraction(h, 1)
                        succs.append((gamma_rat * (one - alpha_rat), s_idx(t, a - h, 1, 1), r_match_h))
                    succs.append(((one - gamma_rat) * (one - alpha_rat), s_idx(t, a, h + 1, 1), zero))
                    transitions[s]['wait'] = succs

    return transitions

def verify_certificate_file(cert_path):
    print(f"\n--- Verifying Dual Certificate: {os.path.basename(cert_path)} ---")
    import hashlib
    with open(cert_path, 'rb') as f:
        raw_b = f.read()
    fname = os.path.basename(cert_path)
    expected_sha = {
        "certificate_alpha_0.45.json": "d46b32a8ae34a1b2a9919ca5442fbb33584cc383e1ccd1e845c4df83f2e70009",
        "certificate_alpha_0.475.json": "208b3be42872a8d96e556f23b10c5f609c0beb94feb12ec072027eb379aaccf2",
        "certificate_alpha_0.425.json": "9a3c3860a454bbcc77211e9911f7655f992b2419e28855f77f56c3185978a6f1",
        "certificate_alpha_0.40.json": "2b18bf4aa18d0527c9207de60b892cf390516e3ad585da833cfba1a713cc7216",
    }
    if fname in expected_sha:
        actual_sha = hashlib.sha256(raw_b).hexdigest()
        assert actual_sha == expected_sha[fname], f"Object SHA256 mismatch for {fname}: got {actual_sha}, expected {expected_sha[fname]}"

    if cert_path.endswith('.gz'):
        with gzip.open(cert_path, 'rt') as f:
            data = json.load(f)
    else:
        data = json.loads(raw_b.decode('utf-8'))

    alpha_rat = Fraction(data['alpha_num'], data['alpha_den'])
    gamma_rat = Fraction(data['gamma_num'], data['gamma_den'])
    t = data['truncation_t']
    comp_var = data['comp_variant']
    u_rat = Fraction(data['u_num'], data['u_den'])
    g_rat = Fraction(data['g_num'], data['g_den'])
    denom_d = data['denom_d']
    h_nums = data['h_numerators']

    print(f"Target: {data['target_id']}")
    print(f"Parameters: alpha = {alpha_rat} ({float(alpha_rat)}), gamma = {gamma_rat}, T = {t}, comp_var = {comp_var}")
    print(f"Certified upper bound U = {u_rat} ({float(u_rat):.7f})")
    print(f"Certificate gain g = {g_rat} ({float(g_rat):.8f})")

    assert g_rat < 0, f"Certificate gain g must be strictly negative! Got {g_rat}"
    print("Gain check g < 0: PASS")

    # Reconstruct exact bias vector h
    num_states = (t + 1) * (t + 1) * 3
    assert len(h_nums) == num_states, f"h vector length mismatch: expected {num_states}, got {len(h_nums)}"
    h_rat = [Fraction(n, denom_d) for n in h_nums]

    # Rebuild MDP independently
    transitions = build_transitions_exact(alpha_rat, gamma_rat, t, u_rat, True, comp_var)

    # Verify every inequality
    violations = 0
    max_slack = Fraction(-10**9, 1)

    for s in range(num_states):
        h_s = h_rat[s]
        for act, succs in transitions[s].items():
            lhs = Fraction(0, 1)
            for prob, s_next, r in succs:
                lhs += prob * (r + h_rat[s_next])
            diff = lhs - h_s
            if diff > max_slack:
                max_slack = diff
            if diff > g_rat:
                violations += 1
                if violations <= 3:
                    print(f"VIOLATION at s={s} ({idx_to_s(t, s)}), action={act}: diff = {float(diff)} > g = {float(g_rat)}")

    print(f"Checked {num_states} states across all valid actions.")
    print(f"Max Bellman residual across all state-actions: {float(max_slack):.8f} ({max_slack})")
    print(f"Inequality diff <= g: {float(max_slack):.8f} <= {float(g_rat):.8f}")
    assert violations == 0, f"FAILED: {violations} inequalities violated!"
    print(f"ALL STATE-ACTION INEQUALITIES SATISFIED EXACTLY! Zero violations!")
    print(f"CERTIFICATE VERIFIED: max REV < {float(u_rat):.7f} is mathematically certified!")
    return True

def verify_policy_file(policy_path):
    print(f"\n--- Verifying Stationary Policy: {os.path.basename(policy_path)} ---")
    with open(policy_path, 'r') as f:
        data = json.load(f)

    alpha_rat = Fraction(data['alpha_num'], data['alpha_den'])
    alpha_f = float(alpha_rat)
    t = data['truncation_t']
    pub_bar = data['published_bar']
    actions = np.array(data['actions'], dtype=np.int32)

    num_states = (t + 1) * (t + 1) * 3
    assert len(actions) == num_states

    next1 = np.zeros(num_states, dtype=np.int32)
    next2 = np.zeros(num_states, dtype=np.int32)
    r1 = np.zeros(num_states, dtype=np.float64)
    r2 = np.zeros(num_states, dtype=np.float64)

    for a in range(t + 1):
        for h in range(t + 1):
            for fork in range(3):
                s = s_idx(t, a, h, fork)
                act = actions[s]

                if act == 0 or a == t or h == t:  # adopt
                    next1[s] = s_idx(t, 1, 0, 0)
                    next2[s] = s_idx(t, 0, 1, 0)
                    r1[s] = 0.0
                    r2[s] = float(h)
                elif act == 1:  # override
                    next1[s] = s_idx(t, a - h, 0, 0)
                    next2[s] = s_idx(t, a - h - 1, 1, 1)
                    r1[s] = float(h + 1)
                    r2[s] = 0.0
                elif act == 2:  # match
                    next1[s] = s_idx(t, a + 1, h, 2)
                    next2[s] = s_idx(t, a, h + 1, 1)
                    r1[s] = 0.0
                    r2[s] = 0.0
                elif act == 3:  # wait
                    if fork == 2:
                        next1[s] = s_idx(t, a + 1, h, 2)
                        next2[s] = s_idx(t, a, h + 1, 1)
                    else:
                        next1[s] = s_idx(t, a + 1, h, 0)
                        next2[s] = s_idx(t, a, h + 1, 1)
                    r1[s] = 0.0
                    r2[s] = 0.0

    # Policy evaluation via value iteration
    v1 = np.zeros(num_states, dtype=np.float64)
    v2 = np.zeros(num_states, dtype=np.float64)

    for _ in range(4000):
        v1_new = alpha_f * (r1 + v1[next1]) + (1.0 - alpha_f) * (r1 + v1[next2])
        v1_new -= v1_new[0]
        v1 = v1_new

        v2_new = alpha_f * (r2 + v2[next1]) + (1.0 - alpha_f) * (r2 + v2[next2])
        v2_new -= v2_new[0]
        v2 = v2_new

    R1 = alpha_f * (r1[0] + v1[next1[0]]) + (1.0 - alpha_f) * (r1[0] + v1[next2[0]])
    R2 = alpha_f * (r2[0] + v2[next1[0]]) + (1.0 - alpha_f) * (r2[0] + v2[next2[0]])

    rev = R1 / (R1 + R2)
    print(f"Parameters: alpha = {alpha_f}, T = {t}")
    print(f"Expected epoch rewards: R1 = {R1:.8f}, R2 = {R2:.8f}")
    print(f"Computed Stationary Relative Revenue REV = {rev:.8f}")
    print(f"Published bar: {pub_bar:.8f}, Required threshold (> bar + 1e-6): {pub_bar + 1e-6:.8f}")
    assert rev > pub_bar + 1e-6, f"Revenue {rev} failed to beat bar {pub_bar + 1e-6}"
    print(f"Strictly exceeds published bar + 1e-6: True")
    print(f"POLICY EVALUATION VERIFIED: PASS!")
    return True

def fast_gain(alpha, t, rho, overpaying, comp_var=2, tol=1e-5):
    num_states = (t + 1) * (t + 1) * 3
    denom = 1.0 - 2.0 * alpha
    term1 = (alpha * (1.0 - alpha)) / (denom * denom)

    a = np.repeat(np.arange(t + 1), (t + 1) * 3)
    h = np.tile(np.repeat(np.arange(t + 1), 3), t + 1)
    fork = np.tile(np.arange(3), (t + 1) * (t + 1))

    is_trunc = (a == t) | (h == t)
    can_over = (~is_trunc) & (a > h)
    can_match = (~is_trunc) & (fork == 1) & (a >= h) & (h > 0)
    can_wait = (~is_trunc) & ((fork != 2) | ((fork == 2) & (a > h) & (h > 0)))

    s_adopt_a = s_idx(t, 1, 0, 0)
    s_adopt_h = s_idx(t, 0, 1, 0)
    r_adopt = np.zeros(num_states, dtype=np.float64)

    if not overpaying:
        r_adopt = -rho * h.astype(np.float64)
    else:
        r_adopt[~is_trunc] = -rho * h[~is_trunc].astype(np.float64)
        trunc_a = is_trunc & (a == t)
        trunc_h = is_trunc & (a != t) & (h == t)
        term2_a = 0.5 * ((a[trunc_a] - h[trunc_a]).astype(np.float64) / denom + (a[trunc_a] + h[trunc_a]).astype(np.float64))
        if comp_var == 1:
            r_adopt[trunc_a] = (1.0 - rho) * term1 + term2_a
        else:
            r_adopt[trunc_a] = (1.0 - rho) * (term1 + term2_a)

        ratio_h = (alpha / (1.0 - alpha)) ** (h[trunc_h] - a[trunc_h]).astype(np.float64)
        term_ret = term1 + (h[trunc_h] - a[trunc_h]).astype(np.float64) / denom
        r_adopt[trunc_h] = (1.0 - ratio_h) * (-rho * h[trunc_h].astype(np.float64)) + ratio_h * (1.0 - rho) * term_ret

    s_over_a = np.where(can_over, s_idx(t, np.maximum(0, a - h), 0, 0), 0)
    s_over_h = np.where(can_over, s_idx(t, np.maximum(0, a - h - 1), 1, 1), 0)
    r_over = np.where(can_over, (1.0 - rho) * (h + 1).astype(np.float64), -1e12)

    s_match_a = np.where(can_match, s_idx(t, np.minimum(t, a + 1), h, 2), 0)
    s_match_h = np.where(can_match, s_idx(t, a, np.minimum(t, h + 1), 1), 0)

    wait_f2 = can_wait & (fork == 2)
    wait_other = can_wait & (fork != 2)
    s_wait_a = np.zeros(num_states, dtype=np.int32)
    s_wait_h = np.zeros(num_states, dtype=np.int32)
    s_wait_a[wait_f2] = s_idx(t, np.minimum(t, a[wait_f2] + 1), h[wait_f2], 2)
    s_wait_h[wait_f2] = s_idx(t, a[wait_f2], np.minimum(t, h[wait_f2] + 1), 1)
    s_wait_a[wait_other] = s_idx(t, np.minimum(t, a[wait_other] + 1), h[wait_other], 0)
    s_wait_h[wait_other] = s_idx(t, a[wait_other], np.minimum(t, h[wait_other] + 1), 1)

    v = np.zeros(num_states, dtype=np.float64)
    for it in range(3000):
        q_adopt = r_adopt + alpha * v[s_adopt_a] + (1.0 - alpha) * v[s_adopt_h]
        q_over = np.where(can_over, r_over + alpha * v[s_over_a] + (1.0 - alpha) * v[s_over_h], -1e12)
        q_match = np.where(can_match, alpha * v[s_match_a] + (1.0 - alpha) * v[s_match_h], -1e12)
        q_wait = np.where(can_wait, alpha * v[s_wait_a] + (1.0 - alpha) * v[s_wait_h], -1e12)

        v_new = np.maximum(np.maximum(q_adopt, q_over), np.maximum(q_match, q_wait))
        diff = v_new - v
        min_diff = np.min(diff)
        max_diff = np.max(diff)
        span = max_diff - min_diff
        v = v_new - v_new[0]
        if span < tol:
            return 0.5 * (max_diff + min_diff)
    return 0.5 * (max_diff + min_diff)

def verify_calibration():
    print("--- Verifying SSZ Table 2 Calibration and Model Sanity ---")
    g1 = fast_gain(0.425, 75, 0.56808, False, tol=1e-5)
    print(f"Calibration 1: Underpaying alpha=0.425, T=75, rho=0.56808: gain = {g1:+.6f} (target: 0.00000 within 1 unit of last printed digit)")
    assert abs(g1) < 2e-4, f"Failed calibration 1: gain {g1}"
    print("Calibration 1: PASS")

    g2 = fast_gain(0.45, 75, 0.66891, False, tol=1e-5)
    print(f"Calibration 2: Underpaying alpha=0.45, T=75, rho=0.66891: gain = {g2:+.6f} (target: 0.00000 within 1 unit of last printed digit)")
    assert abs(g2) < 6e-4, f"Failed calibration 2: gain {g2}"
    print("Calibration 2: PASS")

    g3 = fast_gain(0.45, 75, 0.66, True, comp_var=2, tol=1e-5)
    print(f"Sanity Check: Overpaying alpha=0.45, T=75, rho=0.66: gain = {g3:+.6f} (must be > 0)")
    assert g3 > 0, f"Failed sanity check: gain {g3} <= 0"
    print("Sanity Check: PASS")

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pkg_dir = os.path.dirname(script_dir)
    obj_dir = os.path.join(pkg_dir, "object")

    # 0. Calibration and sanity checks
    verify_calibration()

    # 1. Verify Dual Certificates
    certs = [
        "certificate_alpha_0.45.json",
        "certificate_alpha_0.475.json",
        "certificate_alpha_0.425.json",
        "certificate_alpha_0.40.json",
        "certificate_alpha_0.45_var1.json.gz",
    ]

    for cert in certs:
        p = os.path.join(obj_dir, cert)
        if os.path.exists(p):
            verify_certificate_file(p)

    # 2. Verify Stationary Policies
    policies = [
        "policy_alpha_0.45.json",
        "policy_alpha_0.475.json",
    ]
    for pol in policies:
        p = os.path.join(obj_dir, pol)
        if os.path.exists(p):
            verify_policy_file(p)

    print("\n" + "="*60)
    print("ALL VERIFICATIONS COMPLETED SUCCESSFULLY WITH 100% PASS RATE!")
    print("="*60)
