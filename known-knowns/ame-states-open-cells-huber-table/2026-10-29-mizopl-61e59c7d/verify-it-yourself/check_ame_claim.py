#!/usr/bin/env python3
"""Standalone self-contained verifier for known-knowns/ame-states-open-cells-huber-table/2026-10-29-mizopl-61e59c7d."""
import importlib.util
import json
import os
import re
import sys

PKG_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OBJ_PATH = os.path.join(PKG_DIR, "object", "huber_wyderka_settled_blanks_audit.json")
HWB_PATH = os.path.join(PKG_DIR, "how-we-built-it", "audit_huber_wyderka.py")


def fail(msg):
    print("ERROR: " + str(msg))
    print("FAIL")
    sys.exit(1)


def main():
    try:
        if not os.path.isfile(OBJ_PATH):
            fail("Missing object/huber_wyderka_settled_blanks_audit.json")
        with open(OBJ_PATH, "r", encoding="utf-8") as f:
            loaded = json.load(f)

        spec = importlib.util.spec_from_file_location("audit_huber_wyderka", HWB_PATH)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        computed = mod.verify_and_build_audit()
        if loaded != computed:
            fail("object/huber_wyderka_settled_blanks_audit.json does not match exact recomputation")

        assert loaded["target_id"] == "ame-states-open-cells-huber-table"
        assert loaded["claim_scope"] == "p2_only_table_maintenance_cell_audit_and_15_0_8_purity_erratum"

        refs = loaded["referenced_source_pages_urls_and_sha256"]
        assert len(refs) == 17
        for r in refs:
            assert r["url"].startswith("https://")
            assert re.fullmatch(r"[0-9a-f]{64}", r["sha256"])

        lts = loaded["live_table_summary"]
        assert lts["populated_cells"] == 485 and lts["blank_cells"] == 523
        assert lts["populated_cells"] + lts["blank_cells"] == 1008
        assert lts["unrecorded_shadow_or_scott_violations_among_blanks"] == 0

        assert loaded["settled_positive_blank_cells_pre_2026_10_21_count"] == 22
        assert loaded["settled_positive_blank_cells_count"] == 23
        assert len(loaded["settled_positive_blank_cells"]) == 23

        imp = loaded["impure_codetables_false_positives"]
        assert len(imp) == 2
        assert imp[0]["n"] == 15 and imp[0]["D"] == 5
        assert imp[0]["symplectic_weight"] == 7 and imp[0]["rank_deficient_7party_cuts"] == 190
        assert imp[0]["cut_rank_histogram"] == {"14": 190, "15": 6245}
        assert imp[1]["n"] == 15 and imp[1]["D"] == 7
        assert imp[1]["symplectic_weight"] == 1 and imp[1]["rank_deficient_7party_cuts"] == 3003
        assert imp[1]["post_2026_10_21_replacement_bad_cuts"] == 0
        assert imp[1]["post_2026_10_21_replacement_pure_distance"] == 8

        prior = loaded["prior_public_lean4_and_literature_resolutions"]
        assert prior["AME_9_10"]["prior_lean4_repo"] == "https://github.com/niketp03/atlas-fc-verified"
        assert prior["AME_11_10"]["prior_lean4_repo"] == "https://github.com/KitaKen1/ame-11-10-lean"

        nulls = loaded["null_and_perturbation_controls"]
        assert nulls["zero_shift_c9_survival_on_72_affected_cuts"] == 0
        assert nulls["zero_shift_c11_survival_on_129_affected_cuts"] == 0
        assert nulls["random_vectors_passing_all_72_cuts"] == 0
    except Exception as e:
        fail(e)

    print(
        "Verified p2 1,008-cell Huber-Wyderka audit, 17 URL+SHA256 source records, "
        "[[15,0,8]]_5 (w_pure=7, 190/6,435 bad cuts) & [[15,0,8]]_7 (pre-2026-10-21 w_pure=1, 3,003/6,435 bad cuts -> "
        "2026-10-21 cyclic w_pure=8, 0/6,435 bad cuts) purity erratum, and prior Lean 4 / literature cross-checks."
    )
    print("PASS")


if __name__ == "__main__":
    main()
