#!/usr/bin/env python3
import os
import sys
import gzip
import json
import struct
import hashlib

def main():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    obj_dir = os.path.join(base, "object")

    # 0. Verify summary object
    summary_p = os.path.join(obj_dir, "summary.json")
    assert os.path.isfile(summary_p), "Missing summary.json"
    with open(summary_p, "rb") as f:
        sh = hashlib.sha256(f.read()).hexdigest()
    if sh != "2e08e5c3084603004b8d8ff53ca3c6e8418e4b4d81be0fd61fba9feae526bf84":
        print("Summary object hash mismatch: corrupted object rejected.")
        return 1

    with open(summary_p, "r", encoding="utf-8") as f:
        sdata = json.load(f)
    assert sdata["num_states"] == 946
    assert sdata["convention_ii_exploitability"] <= 0.0488
    assert sdata["convention_i_exploitability"] <= 0.0488

    # 1. Verify preflop 2-way equity table
    eq_path = os.path.join(obj_dir, "equity_2way.bin")
    assert os.path.isfile(eq_path), "Missing equity_2way.bin"
    eq_size = os.path.getsize(eq_path)
    assert eq_size == 685464, f"Unexpected equity table size: {eq_size}"

    # Verify AA vs KK equity in binary table
    with open(eq_path, "rb") as f:
        f.seek((0 * 169 + 1) * 24)
        win, loss, tie = struct.unpack("<ddd", f.read(24))
        # AA win equity is approx 0.824
        assert 0.81 <= win <= 0.84, f"AA vs KK equity unexpected: {win}, {loss}, {tie}"

    print("Preflop 2-way equity table validated (685,464 bytes).")

    # 2. Verify Convention (ii) Strategy Profile
    prof_ii_path = os.path.join(obj_dir, "strategy_profile_conv_ii.json.gz")
    assert os.path.isfile(prof_ii_path), "Missing strategy_profile_conv_ii.json.gz"
    with gzip.open(prof_ii_path, "rt", encoding="utf-8") as f:
        prof_ii = json.load(f)

    assert len(prof_ii["strategies"]) == 946, f"Expected 946 strategies, got {len(prof_ii['strategies'])}"
    assert len(prof_ii["values"]) == 2838, f"Expected 2838 values, got {len(prof_ii['values'])}"
    assert prof_ii["exploitability"] <= 0.0488, "Certified epsilon exceeds claimed bound"
    print(f"Convention (ii) strategy profile verified: 946 states, epsilon = ${prof_ii['exploitability']:.6f}.")

    # 3. Verify Convention (i) Strategy Profile
    prof_i_path = os.path.join(obj_dir, "strategy_profile_conv_i.json.gz")
    assert os.path.isfile(prof_i_path), "Missing strategy_profile_conv_i.json.gz"
    with gzip.open(prof_i_path, "rt", encoding="utf-8") as f:
        prof_i = json.load(f)

    assert len(prof_i["strategies"]) == 946
    assert len(prof_i["values"]) == 2838
    assert prof_i["exploitability"] <= 0.0488
    print(f"Convention (i) strategy profile verified: 946 states, epsilon = ${prof_i['exploitability']:.6f}.")

    print("ALL THREE-PLAYER JAM/FOLD ARTIFACTS VERIFIED: PASS")
    return 0

if __name__ == "__main__":
    try:
        rc = main()
        sys.exit(rc)
    except Exception as e:
        print(f"VERIFICATION FAILED: {e}", file=sys.stderr)
        sys.exit(1)
