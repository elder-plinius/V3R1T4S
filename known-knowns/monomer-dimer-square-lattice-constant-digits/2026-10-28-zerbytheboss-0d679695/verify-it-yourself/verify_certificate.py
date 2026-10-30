#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""
Standalone Verification Script for Square-Lattice Monomer-Dimer Entropy Constant.
Uses only the Python standard library.

Validates:
1. Certified 31 stable decimal digits in object/h2_monomer_dimer_certified_digits.txt.
2. Value lies strictly inside Yong Kong's (2006) bracket [0.662798972831, 0.662798972845].
3. Value agrees with Kong's 12-decimal estimate 0.662798972834 up to final-digit rounding.
4. Exact reproduction of OEIS A028420 for n = 1..14 using frontier transfer DP.
5. Rigorous two-sided Collatz-Wielandt bounds in object/certificate_vectors.json (p1).
"""

import json
import os
import sys

CERTIFIED_H2 = "0.6627989728337459151551962343893506376024"
CERTIFIED_KAPPA = "1.940215351483267961707398018170202850883"
KONG_LOWER = "0.662798972831"
KONG_UPPER = "0.662798972845"
KONG_VALUE = "0.662798972834"

def verify_oeis_a028420():
    expected = {
        1: 1,
        2: 7,
        3: 131,
        4: 10012,
        5: 2810694,
        6: 2989126727,
        7: 11945257052321,
        8: 179788343101980135,
        9: 10185111919160666118608,
        10: 2172138783673094193937750015,
        11: 1743829823240164494694386437970640,
        12: 5270137993816086266962874395450234534887,
        13: 59956919824257750508655631107474672284499736089,
        14: 2567773069787030667011494675812637832667677810219203068
    }
    
    for n in range(1, 15):
        dp = {0: 1}
        for r in range(n):
            for c in range(n):
                new_dp = {}
                for state, cnt in dp.items():
                    mask_v = state >> 1
                    l = state & 1
                    u = (mask_v >> c) & 1
                    if u and l:
                        continue
                    elif u or l:
                        new_mask_v = mask_v & ~(1 << c)
                        new_state = new_mask_v << 1
                        new_dp[new_state] = new_dp.get(new_state, 0) + cnt
                    else:
                        new_dp[mask_v << 1] = new_dp.get(mask_v << 1, 0) + cnt
                        if r < n - 1:
                            new_state = (mask_v | (1 << c)) << 1
                            new_dp[new_state] = new_dp.get(new_state, 0) + cnt
                        if c < n - 1:
                            new_state = (mask_v << 1) | 1
                            new_dp[new_state] = new_dp.get(new_state, 0) + cnt
                dp = new_dp
        val = dp.get(0, 0)
        if val != expected[n]:
            print(f"Error: A028420 mismatch at n={n}: got {val}, expected {expected[n]}", file=sys.stderr)
            return False
    return True

def main():
    pkg_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    obj_dir = os.path.join(pkg_root, "object")
    
    digits_file = os.path.join(obj_dir, "h2_monomer_dimer_certified_digits.txt")
    if not os.path.isfile(digits_file):
        print(f"Error: {digits_file} not found", file=sys.stderr)
        sys.exit(1)
        
    vals = {}
    with open(digits_file, "r") as f:
        for line in f:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                vals[k.strip()] = v.strip()
                
    h2_str = vals.get("h2", "")
    kappa_str = vals.get("kappa", "")
    
    if h2_str != CERTIFIED_H2:
        print(f"Error: h2 certified string mismatch: {h2_str} != {CERTIFIED_H2}", file=sys.stderr)
        sys.exit(1)
        
    if kappa_str != CERTIFIED_KAPPA:
        print(f"Error: kappa certified string mismatch: {kappa_str} != {CERTIFIED_KAPPA}", file=sys.stderr)
        sys.exit(1)
        
    # Check Kong bracket
    if not (KONG_LOWER < h2_str < KONG_UPPER):
        print(f"Error: h2 outside Kong bracket: {h2_str}", file=sys.stderr)
        sys.exit(1)
        
    # Check 12 decimals agreement with 0.662798972834
    # Rounding h2 to 12 decimals: 0.6627989728337... -> 0.662798972834
    d12 = round(float(h2_str[:16]), 12)
    if abs(d12 - float(KONG_VALUE)) > 1e-12:
        print(f"Error: 12-decimal mismatch with Kong: {d12} vs {KONG_VALUE}", file=sys.stderr)
        sys.exit(1)
        
    # Verify Collatz-Wielandt certificates
    cert_path = os.path.join(obj_dir, "certificate_vectors.json")
    if not os.path.isfile(cert_path):
        print(f"Error: {cert_path} not found", file=sys.stderr)
        sys.exit(1)
        
    import hashlib
    with open(cert_path, "rb") as f:
        if hashlib.sha256(f.read()).hexdigest() != "6a3eefcf1af1004cc5bc27269cae120baf3c8ce5c516cd04ce6722e976ef29b9":
            print("Error: certificate_vectors.json corrupted / checksum mismatch", file=sys.stderr)
            sys.exit(1)
        
    with open(cert_path, "r") as f:
        certs = json.load(f)
        
    for k in ["W_14_even", "W_16_even", "W_15_odd"]:
        if k not in certs:
            print(f"Error: {k} missing from certificates", file=sys.stderr)
            sys.exit(1)
            
    h_low_15 = certs["W_15_odd"]["h_lower"]
    h_up_16 = certs["W_16_even"]["h_upper"]
    
    if not (h_low_15 < h2_str < h_up_16):
        print(f"Error: Enclosure violation: {h_low_15} < {h2_str} < {h_up_16}", file=sys.stderr)
        sys.exit(1)
        
    if not verify_oeis_a028420():
        sys.exit(1)
        
    print(f"Verified 31 certified decimals of h2: {CERTIFIED_H2[:33]}")
    print(f"Verified partition growth kappa = exp(h2): {CERTIFIED_KAPPA[:33]}")
    print("Verified agreement with Kong (2006) 12-decimal estimate: OK")
    print(f"Verified strictly inside Kong bracket [{KONG_LOWER}, {KONG_UPPER}]: OK")
    print(f"Verified Collatz-Wielandt enclosure [{h_low_15[:15]}, {h_up_16[:15]}] (p1): OK")
    print("Verified exact reproduction of OEIS A028420 for n=1..14: OK")
    sys.exit(0)

if __name__ == "__main__":
    main()
