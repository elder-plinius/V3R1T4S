#!/usr/bin/env python3
# Calibration script: reproduces JLTX (SODA 2019 / arXiv:1804.00480) 3-buyer and 4-buyer instances.
import math
import sys

def calibrate_3buyer():
    print("=== 1. JLTX 3-Buyer Calibration ===")
    # v0 = inf, F0(p) = p/(p+1)
    # v1 approx 1.5699, q1 = 1 / v1^2
    # v2 is root of: v2 + v1/(1 + v1 - v1^2) * ln[ (v1+1)/(v1^3) * ((v1^2 - 1)*v2 + v1)/(v2+1) ] = 1
    v1 = 1.569926
    q1 = 1.0 / (v1 * v1)
    
    def ar_v2(v2):
        term = (v1 / (1.0 + v1 - v1**2)) * math.log( ((v1 + 1.0) / (v1**3)) * ((v1**2 - 1.0)*v2 + v1) / (v2 + 1.0) )
        return v2 + term

    low, high = 0.5, 0.99
    for _ in range(80):
        mid = (low + high) / 2.0
        if ar_v2(mid) < 1.0:
            low = mid
        else:
            high = mid
    v2 = (low + high) / 2.0
    opt = 1.0 + 1.0 / v1 + v2 * (1.0 - 1.0 / (v1**2))
    print(f"JLTX 3-buyer: v1 = {v1:.4f}, v2 = {v2:.4f}, OPT = {opt:.4f}")
    assert abs(v1 - 1.5699) < 0.001, "v1 mismatch"
    assert abs(v2 - 0.8399) < 0.001, "v2 mismatch"
    assert abs(opt - 2.1361) < 0.001, "OPT mismatch"
    print("PASS: 3-buyer calibration matches JLTX 2.1361 exactly.\n")
    return v1, v2, opt

def calibrate_4buyer():
    print("=== 2. JLTX 4-Buyer Printed Instance Calibration ===")
    # Printed parameters in JLTX Theorem 3:
    # v1 = 1.8512, q1 = 0.2918
    # v2 = 0.9700, q2 = 0.6138
    # v3 = 0.7231, q3 = 1.0000
    v = [float('inf'), 1.8512, 0.9700, 0.7231]
    q = [0.0, 0.2918, 0.6138, 1.0000]
    
    # Analytical piece integral using partial fractions:
    # c_0 = 1.0, c_j = v_j * q_j / (1 - q_j)
    c = [1.0, v[1]*q[1]/(1.0 - q[1]), v[2]*q[2]/(1.0 - q[2])]
    
    def piece_integral(m, lower, upper):
        cm = c[:m+1]
        C_m = sum(cm)
        A = []
        for j in range(m + 1):
            cj = cm[j]
            num_val = - ((-cj)**m) * (-cj + C_m)
            denom_val = 1.0
            for i in range(m + 1):
                if i != j:
                    denom_val *= (cm[i] - cj)
            A.append(num_val / denom_val)
        return sum(A[j] * math.log((upper + cm[j]) / (lower + cm[j])) for j in range(m + 1))

    # AR(v1)
    ar1 = v[1] * (1.0 - (1.0 - q[1]) * (v[1] / (v[1] + 1.0)))
    
    # AR(v2)
    int_2_1 = piece_integral(1, v[2], v[1])
    F0_v2 = v[2] / (v[2] + 1.0)
    F1_v2 = v[2] / (v[2] + c[1])
    ap2 = v[2] * (1.0 - F0_v2 * F1_v2 * (1.0 - q[2]))
    ar2 = ap2 + int_2_1
    
    # AR(v3)
    int_3_2 = piece_integral(2, v[3], v[2])
    ap3 = v[3]
    ar3 = ap3 + int_3_2 + int_2_1
    
    # OPT
    opt = 1.0 + v[1]*q[1] + v[2]*q[2]*(1.0 - q[1]) + v[3]*q[3]*(1.0 - q[1])*(1.0 - q[2])
    
    print(f"JLTX 4-buyer: AR(v1) = {ar1:.6f}")
    print(f"JLTX 4-buyer: AR(v2) = {ar2:.6f}")
    print(f"JLTX 4-buyer: AR(v3) = {ar3:.6f}")
    print(f"JLTX 4-buyer: OPT    = {opt:.6f}")
    ratio = opt / max(ar1, ar2, ar3)
    print(f"JLTX 4-buyer: OPT/AR = {ratio:.6f}")
    
    assert abs(ar1 - 1.0) < 0.001, "AR(v1) mismatch"
    assert abs(ar2 - 1.0) < 0.001, "AR(v2) mismatch"
    assert abs(ar3 - 1.0) < 0.001, "AR(v3) mismatch"
    assert abs(opt - 2.1596) < 0.001, "OPT mismatch"
    print("PASS: 4-buyer calibration matches JLTX 2.1596 exactly.\n")
    return opt, (ar1, ar2, ar3), ratio

if __name__ == "__main__":
    calibrate_3buyer()
    calibrate_4buyer()
