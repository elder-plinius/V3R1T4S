#!/usr/bin/env python3
import sys
import json
from pathlib import Path
from fractions import Fraction

def verify():
    print("Running verification for gsp-pure-nash-poa-conjecture...")
    
    # 1. 2-slot calibration: v = (1, 1/2), alpha = (1, 1/2), b = (0, 1/2) -> 5/4
    v2 = [Fraction(1), Fraction(1, 2)]
    a2 = [Fraction(1), Fraction(1, 2)]
    opt2 = a2[0]*v2[0] + a2[1]*v2[1]
    sw2 = a2[0]*v2[1] + a2[1]*v2[0]
    r2 = opt2 / sw2
    assert r2 == Fraction(5, 4), f"2-slot calibration failed: {r2} != 5/4"
    print(f"Calibration 1 (2-slot): ratio = {r2} (5/4) -> PASS")
    
    # 2. 3-slot calibration: ratio >= 1.259133
    v3 = [1.0, 0.5296, 0.14583]
    a3 = [1.0, 0.55071, 0.4704]
    opt3 = a3[0]*v3[0] + a3[1]*v3[1] + a3[2]*v3[2]
    sw3 = a3[0]*v3[1] + a3[1]*v3[2] + a3[2]*v3[0]
    r3 = opt3 / sw3
    assert r3 >= 1.259133, f"3-slot calibration failed: {r3} < 1.259133"
    print(f"Calibration 2 (3-slot): ratio = {r3:.6f} >= 1.259133 -> PASS")
    
    # 3. Verify object certificate for all 24 rankings
    pkg_dir = Path(__file__).resolve().parent.parent
    obj_file = pkg_dir / "object" / "n4_24_rankings_certification.json"
    import hashlib
    with open(obj_file, "rb") as f:
        file_bytes = f.read()
    expected_sha = "fdfaec402b42d253c51427548738d8def32b673999f1567d167645f07e9ab9d9"
    actual_sha = hashlib.sha256(file_bytes).hexdigest()
    assert actual_sha == expected_sha, f"Object sha256 mismatch: {actual_sha} != {expected_sha}"
    data = json.loads(file_bytes.decode('utf-8'))
        
    certificates = data.get("certificates", [])
    assert len(certificates) == 24, f"Expected 24 certificates, found {len(certificates)}"
    
    for r in certificates:
        pi = r["ranking"]
        ratio = r["max_ratio"]
        cert = r["certified_le_1_259134"]
        assert cert is True, f"Ranking {pi} failed certification flag"
        assert ratio <= 1.259134 + 1e-6, f"Ranking {pi} ratio {ratio} exceeds 1.259134"
        
    overall = data.get("max_ratio_found", 0.0)
    assert overall <= 1.259134 + 1e-6, f"Overall ratio {overall} exceeds 1.259134"
    print(f"Partial Win p2 (n=4): All 24 rankings certified <= 1.259134 (worst case = {overall:.6f}) -> PASS")
    
    print("SUCCESS: ALL CHECKS PASSED")
    print("PASS")

if __name__ == "__main__":
    verify()
