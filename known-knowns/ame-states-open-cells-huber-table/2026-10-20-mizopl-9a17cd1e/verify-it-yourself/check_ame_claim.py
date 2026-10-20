#!/usr/bin/env python3
"""Standalone self-contained verifier for outbox/2026-10-20-mizopl-9a17cd1e."""
import importlib.util
import json
import os
import sys

PKG_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OBJ_DIR = os.path.join(PKG_DIR, "object")
HWB_DIR = os.path.join(PKG_DIR, "how-we-built-it")


def fail(msg):
    print("ERROR: " + str(msg))
    print("FAIL")
    sys.exit(1)


def main():
    try:
        from itertools import combinations
        spec = importlib.util.spec_from_file_location("author_checker_ame", os.path.join(HWB_DIR, "author_checker_ame.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        # Verify AME(9, 10), AME(11, 10), and null controls directly on object/
        mod.verify_ame_9_10(OBJ_DIR, full_dense=False)
        mod.verify_ame_11_10(OBJ_DIR)
        mod.verify_null_and_perturbation_controls(OBJ_DIR)

        with open(os.path.join(OBJ_DIR, "ame_9_10_certificate.json")) as f:
            c9 = json.load(f)
        assert c9["cell"] == [9, 10] and c9["n"] == 9 and c9["D"] == 10 and c9["k"] == 4
        for idx, S in enumerate(combinations(range(9), 4)):
            Sc = [i for i in range(9) if i not in S]
            row = c9["quinary_graph_mds_code"]["cuts_determinants"][idx]
            assert row["S"] == list(S) and row["Sc"] == Sc

        with open(os.path.join(OBJ_DIR, "ame_11_10_certificate.json")) as f:
            c11 = json.load(f)
        assert c11["cell"] == [11, 10] and c11["n"] == 11 and c11["D"] == 10 and c11["k"] == 5
        for idx, S in enumerate(combinations(range(11), 5)):
            Sc = [i for i in range(11) if i not in S]
            row = c11["quinary_graph_mds_code"]["cuts_determinants"][idx]
            assert row["S"] == list(S) and row["Sc"] == Sc

        with open(os.path.join(OBJ_DIR, "huber_wyderka_settled_blanks_audit.json")) as f:
            aud = json.load(f)
        assert aud["settled_positive_blank_cells_count"] == 22
        assert len(aud["settled_positive_blank_cells"]) == 22
        assert aud["impure_codetables_false_positives_count"] == 2
        imp = aud["impure_codetables_false_positives"]
        assert imp[0]["symplectic_weight"] == 7 and imp[0]["rank_deficient_7party_cuts"] == 190
        assert imp[1]["symplectic_weight"] == 1 and imp[1]["rank_deficient_7party_cuts"] == 3003
    except Exception as e:
        fail(e)

    print("Verified exact AME(9, 10) (126/126 cuts), AME(11, 10) & pure [[11, 1, 6]]_5 (462/462 cuts), and 1,008-cell audit.")
    print("PASS")


if __name__ == "__main__":
    main()
