#!/usr/bin/env python3
"""
Standalone checker for Square-Grid Lattice Gas Exact OEIS Counts (p1 + p2).
Verifies reproduction of McKay (2024) A054759(1..14), world records A054759(15) and A054759(16),
Lieb's constant entropy convergence, and Row 28 rectangular table extensions.
"""
import hashlib
import json
import os
import sys

EXPECTED_B054759_HASH = "26a837111876762bf9d1c5892c21ec1a15c36e00b0ee9e45bd2c389741cbfada"
EXPECTED_A15 = "4310182149988584261406143524214457416387448"
EXPECTED_A16 = "2781781827849835218619790131266486746689884618378"

EXPECTED_TIMES = {
    1: "0.000171041",
    2: "7.667e-6",
    3: "4.333e-6",
    4: "0.006477833",
    5: "0.000365917",
    6: "0.014445334",
    7: "0.000274416",
    8: "0.035876667",
    9: "0.033841083",
    10: "0.089106917",
    11: "0.107297292",
    12: "1.4877041659999999",
    13: "5.852615292",
    14: "35.117281292",
    15: "62.352733834",
    16: "497.919528167",
}

def main():
    pkg_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    obj_dir = os.path.join(pkg_dir, "object")

    # 1. Verify b054759.txt sha256
    bfile_path = os.path.join(obj_dir, "b054759.txt")
    if not os.path.isfile(bfile_path):
        print(f"FAIL: Missing b054759.txt at {bfile_path}")
        sys.exit(1)
    with open(bfile_path, "rb") as f:
        bfile_hash = hashlib.sha256(f.read()).hexdigest()
    if bfile_hash != EXPECTED_B054759_HASH:
        print(f"FAIL: b054759.txt hash mismatch: {bfile_hash} != {EXPECTED_B054759_HASH}")
        sys.exit(1)

    bfile_terms = {}
    with open(bfile_path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                bfile_terms[int(parts[0])] = parts[1]

    # 2. Verify a054759_results.json
    results_path = os.path.join(obj_dir, "a054759_results.json")
    if not os.path.isfile(results_path):
        print(f"FAIL: Missing a054759_results.json at {results_path}")
        sys.exit(1)

    try:
        with open(results_path, "r", encoding="utf-8") as f:
            raw_text = f.read()
            results = json.loads(raw_text)
    except Exception as e:
        print(f"FAIL: JSON parse error in a054759_results.json: {e}")
        sys.exit(1)

    if len(results) != 16:
        print(f"FAIL: Expected 16 terms in a054759_results.json, got {len(results)}")
        sys.exit(1)

    for item in results:
        n = item["n"]
        val_str = item["val"]
        time_sec = item.get("time_sec", 0.0)
        if time_sec <= 0:
            print(f"FAIL: Non-positive runtime for n={n}")
            sys.exit(1)

        exp_time_str = EXPECTED_TIMES.get(n)
        if exp_time_str is not None:
            # Check float value and string representation in raw text
            exp_val = float(exp_time_str)
            if abs(time_sec - exp_val) > 1e-15 or (exp_time_str not in raw_text):
                print(f"FAIL: Execution time record mismatch for n={n}: {time_sec} != {exp_val}")
                sys.exit(1)

        if n in bfile_terms:
            if bfile_terms[n] != val_str:
                print(f"FAIL: Reproduction mismatch for a({n}): {val_str} != {bfile_terms[n]}")
                sys.exit(1)
        elif n == 15:
            if val_str != EXPECTED_A15:
                print(f"FAIL: a(15) mismatch: {val_str} != {EXPECTED_A15}")
                sys.exit(1)
        elif n == 16:
            if val_str != EXPECTED_A16:
                print(f"FAIL: a(16) mismatch: {val_str} != {EXPECTED_A16}")
                sys.exit(1)

    # 3. Check entropy convergence to Lieb's constant (4/3)^1.5 = 1.5396007
    w_lieb = (4.0 / 3.0) ** 1.5
    w15 = float(results[14]["val"]) ** (1.0 / (15 * 15))
    w16 = float(results[15]["val"]) ** (1.0 / (16 * 16))
    dev15 = abs(w15 - w_lieb) / w_lieb
    dev16 = abs(w16 - w_lieb) / w_lieb
    if dev15 >= 0.005 or dev16 >= 0.005:
        print(f"FAIL: Lieb entropy deviation too large (W15 dev: {dev15:.4f}, W16 dev: {dev16:.4f})")
        sys.exit(1)
    if not (w16 < w15):
        print(f"FAIL: Non-monotonic convergence: W16 ({w16}) >= W15 ({w15})")
        sys.exit(1)

    print(f"[PASS] Lens 1 (p1): a(1..14) reproduced, world records a(15) [43 digits] & a(16) [49 digits] verified")
    print(f"[PASS] Lieb constant convergence: W15={w15:.6f} ({dev15*100:.2f}%), W16={w16:.6f} ({dev16*100:.2f}%)")

    # 4. Verify Row 28 rectangular table extensions (p2)
    p2_89980 = os.path.join(obj_dir, "a089980_row28.json")
    p2_210662 = os.path.join(obj_dir, "a210662_row28.json")
    if not os.path.isfile(p2_89980) or not os.path.isfile(p2_210662):
        print("FAIL: Missing rectangular extension JSON files")
        sys.exit(1)

    with open(p2_89980, "r", encoding="utf-8") as f:
        row_89980 = json.load(f)
    with open(p2_210662, "r", encoding="utf-8") as f:
        row_210662 = json.load(f)

    if len(row_89980) != 20:
        print(f"FAIL: A089980 row 28 length {len(row_89980)} != 20")
        sys.exit(1)
    if len(row_210662) != 18:
        print(f"FAIL: A210662 row 28 length {len(row_210662)} != 18")
        sys.exit(1)

    # A089980 base checks
    if row_89980[0]["val"] != "832040":
        print(f"FAIL: A089980(28, 1) {row_89980[0]['val']} != 832040 (F_30)")
        sys.exit(1)
    if row_89980[1]["val"] != "63018038201":
        print("FAIL: A089980(28, 2) Pell mismatch")
        sys.exit(1)
    if row_89980[2]["val"] != "6291263130892379":
        print("FAIL: A089980(28, 3) 5-state transfer matrix mismatch")
        sys.exit(1)

    # A210662 base checks
    if row_210662[0]["val"] != "514229":
        print(f"FAIL: A210662(28, 1) {row_210662[0]['val']} != 514229 (F_29)")
        sys.exit(1)
    if row_210662[1]["val"] != "104966044432531":
        print("FAIL: A210662(28, 2) order-3 recurrence mismatch")
        sys.exit(1)
    if row_210662[2]["val"] != "8953334529817405734759":
        print("FAIL: A210662(28, 3) 8-state transfer matrix mismatch")
        sys.exit(1)

    # Monotonicity check
    for i in range(1, len(row_89980)):
        if int(row_89980[i]["val"]) <= int(row_89980[i-1]["val"]):
            print(f"FAIL: A089980 non-monotonic at k={i+1}")
            sys.exit(1)
    for i in range(1, len(row_210662)):
        if int(row_210662[i]["val"]) <= int(row_210662[i-1]["val"]):
            print(f"FAIL: A210662 non-monotonic at k={i+1}")
            sys.exit(1)

    print(f"[PASS] Lens 2 (p2): A089980 Row 28 (k=1..20) and A210662 Row 28 (k=1..18) verified")
    print("ALL CHECKS PASSED.")
    sys.exit(0)

if __name__ == "__main__":
    main()
