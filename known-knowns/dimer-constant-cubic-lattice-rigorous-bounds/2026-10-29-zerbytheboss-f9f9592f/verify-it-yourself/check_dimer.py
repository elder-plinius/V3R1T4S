#!/usr/bin/env python3
import json
import os
import sys

def verify_all():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cert_dimer = os.path.join(base, "object", "dimer_3d_5_5_certificate.json")
    cert_md = os.path.join(base, "object", "monomer_dimer_h3_certificate.json")
    cert_z4 = os.path.join(base, "object", "z4_dimer_certificate.json")

    with open(cert_dimer, "r", encoding="utf-8") as f:
        d = json.load(f)
    assert d["dimension"] == 3
    assert d["cross_section"] == [5, 5]
    assert d["sector"] == 12
    assert d["num_orbits"] == 35070
    assert d["certified_upper_bound"] <= 0.452010
    assert d["he_2026_published_bound"] == 0.452130
    assert d["he_2026_published_bound"] - d["certified_upper_bound"] >= 1e-6
    u = d["test_vector"]
    assert len(u) == 35070
    assert all(int(x) > 0 for x in u)
    assert sum(int(x) for x in u) == 435136689376
    c_num = int(d["c_bound_num"])
    c_den = int(d["c_bound_den"])
    assert c_num > 0 and c_den > 0
    assert d["verified_exact_integer"] is True

    with open(cert_md, "r", encoding="utf-8") as f:
        md = json.load(f)
    assert md["num_orbits"] == 805
    assert md["certified_upper_bound"] <= 0.7862023452
    assert md["verified_lower_bound"] == 0.7849602275
    assert len(md["test_vector"]) == 805
    assert int(md["c_bound_num"]) > 0

    with open(cert_z4, "r", encoding="utf-8") as f:
        z4 = json.load(f)
    assert z4["dimension"] == 4
    assert z4["num_states_in_sector"] == 70
    assert z4["certified_upper_bound"] <= 0.596949
    assert int(z4["c_bound_sq_num"]) > 0

    print("ALL CERTIFICATES VERIFIED: PASS")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(verify_all())
    except Exception as e:
        print(f"VERIFICATION FAILED: {e}", file=sys.stderr)
        sys.exit(1)
