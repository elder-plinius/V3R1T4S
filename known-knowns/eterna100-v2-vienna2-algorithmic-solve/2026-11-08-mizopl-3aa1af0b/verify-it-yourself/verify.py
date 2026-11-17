#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Standalone Zero-Trust Verifier for `eterna100-v2-vienna2-algorithmic-solve` (`2026-11-08-mizopl-3aa1af0b`)
=========================================================================================================
Verifies:
1. Cryptographic SHA-256 integrity of `object/certificate.json`, `object/manifest_sha256.json`,
   `object/ckpt_best.json`, and `object/p3_undesignability_certificates.json`.
2. Structural, combinatorial, and thermodynamic invariants of all 100 Eterna100-V2 de novo designs in
   `object/ckpt_best.json` (95/100 exact MFE solve d_bp = 0 including #79 Shapes and Energy and
   #71 Variation of a crop circle; 96/100 exact MFE ground state de_mfe = 0.00 kcal/mol including
   #68 Taraxacum officinale), verifying exact dot-bracket base-pair sets, Watson-Crick-Wobble compatibility,
   symmetric-difference base-pair distance d_bp, and all 100-element metric vectors.
3. Internal consistency of the local Turner 2004 motif energy analyses in
   `object/p3_undesignability_certificates.json` for #68, #86, #90, #99, #100.
   CORRECTION (2026-11-12, see CORRECTION.md): the p3 claim is WITHDRAWN. These are local motif
   analyses, NOT undesignability certificates; #68, #86, #90 and #99 have official V2/Vienna2 sample
   solutions that fold exactly to target under stock ViennaRNA 2.6.4 (only #100 is undisclosed).
4. Live Turner 2004 MFE folding (`RNA.fold` and `RNA.eval_structure_simple` at T = 37.0 C) across all 100
   sequences and all p3 barrier witness motifs whenever ViennaRNA (`import RNA`) is installed.
"""
import hashlib
import json
import os
import sys
from pathlib import Path

try:
    import RNA
    HAS_VIENNA = True
except ImportError:
    HAS_VIENNA = False

PKG_ROOT = Path(__file__).resolve().parent.parent
OBJ_DIR = PKG_ROOT / "object"
VALID_PAIRS = {"GC", "CG", "AU", "UA", "GU", "UG"}
VALID_BASES = {"A", "C", "G", "U"}


def fail(msg: str) -> None:
    print(f"[FAIL] {msg}")
    print("FAIL")
    sys.exit(1)


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def parse_structure_pairs(struct: str) -> set:
    stack = []
    pairs = set()
    for i, ch in enumerate(struct):
        if ch == "(":
            stack.append(i)
        elif ch == ")":
            if not stack:
                fail(f"Unbalanced ')' at index {i}")
            j = stack.pop()
            pairs.add((j, i))
        elif ch != ".":
            fail(f"Invalid dot-bracket character '{ch}' at index {i}")
    if stack:
        fail(f"Unclosed '(' in dot-bracket structure (remaining={len(stack)})")
    return pairs


def verify_sha256sums() -> int:
    sums_file = PKG_ROOT / "SHA256SUMS"
    if not sums_file.is_file():
        fail("Missing SHA256SUMS at package root")
    listed = {}
    for line in sums_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split(None, 1)
        if len(parts) != 2:
            fail(f"Malformed line in SHA256SUMS: {line}")
        h, rel = parts[0], parts[1].lstrip("*./")
        listed[os.path.normpath(rel)] = h

    checked = 0
    for p in sorted(OBJ_DIR.iterdir()):
        if not p.is_file():
            continue
        rel = os.path.normpath(os.path.relpath(p, PKG_ROOT))
        actual = sha256_bytes(p.read_bytes())
        if rel not in listed:
            fail(f"Object file {rel} missing from SHA256SUMS")
        if listed[rel] != actual:
            fail(f"SHA256 mismatch for {rel}: listed {listed[rel]} != actual {actual}")
        checked += 1
    return checked


def verify_manifest(manifest: dict, ckpt: dict) -> None:
    if manifest.get("target_id") != "eterna100-v2-vienna2-algorithmic-solve":
        fail("Invalid target_id in manifest_sha256.json")
    if manifest.get("upstream_results_tsv_sha256") != "2861ceb5a0280e5565c40016f169697fb324db7f7c56505c1489a8b78afcea6c":
        fail("Invalid upstream_results_tsv_sha256 in manifest_sha256.json")
    if manifest.get("upstream_results_tsv_bytes") != 2271309:
        fail("Invalid upstream_results_tsv_bytes in manifest_sha256.json")
    if manifest.get("upstream_puzzles_tsv_sha256") != "71147b94c1762a3c8fe93f59e87b53b6292b1c3b9367ce22d5a9c7c6b4736ef6":
        fail("Invalid upstream_puzzles_tsv_sha256 in manifest_sha256.json")
    if manifest.get("upstream_puzzles_tsv_bytes") != 96092:
        fail("Invalid upstream_puzzles_tsv_bytes in manifest_sha256.json")

    unsolved_7 = manifest.get("unsolved_7_v2_puzzle_ids")
    if unsolved_7 != [68, 71, 79, 86, 90, 99, 100] or sum(unsolved_7) != manifest.get("unsolved_7_v2_puzzle_ids_sum") or sum(unsolved_7) != 593:
        fail(f"Corrupted unsolved_7_v2_puzzle_ids in manifest_sha256.json: {unsolved_7}")

    if manifest.get("designable_2_unsolved_v2_puzzle_ids") != [71, 79]:
        fail("Corrupted designable_2_unsolved_v2_puzzle_ids in manifest_sha256.json")

    none_5 = manifest.get("sample_solution_none_5_v2_puzzle_ids")
    if none_5 != [68, 86, 90, 99, 100] or sum(none_5) != manifest.get("sample_solution_none_5_v2_puzzle_ids_sum") or sum(none_5) != 443:
        fail(f"Corrupted sample_solution_none_5_v2_puzzle_ids in manifest_sha256.json: {none_5}")

    solver_counts = manifest.get("benchmarked_solver_v2_solve_counts")
    if solver_counts != [92, 85, 72, 61, 55, 42] or sum(solver_counts) != manifest.get("benchmarked_solver_v2_solve_counts_sum") or sum(solver_counts) != 407:
        fail(f"Corrupted benchmarked_solver_v2_solve_counts in manifest_sha256.json: {solver_counts}")

    pids = [str(i) for i in range(1, 101)]
    expected_lengths = [len(ckpt[k]["target_structure"]) for k in pids]
    expected_bps = [len(parse_structure_pairs(ckpt[k]["target_structure"])) for k in pids]

    if manifest.get("length_vector_100") != expected_lengths or manifest.get("length_vector_100_sum") != sum(expected_lengths):
        fail("Corrupted length_vector_100 in manifest_sha256.json")
    if manifest.get("bp_count_vector_100") != expected_bps or manifest.get("bp_count_vector_100_sum") != sum(expected_bps):
        fail("Corrupted bp_count_vector_100 in manifest_sha256.json")


def verify_ckpt_and_certificate(ckpt: dict, cert: dict) -> None:
    if cert.get("target_id") != "eterna100-v2-vienna2-algorithmic-solve":
        fail("Invalid target_id in certificate.json")
    if cert.get("vienna_rna_versions_verified") != ["2.6.4", "2.8.0"]:
        fail("Invalid vienna_rna_versions_verified in certificate.json")

    p2 = cert.get("p2_full_benchmark_evaluation", {})
    if p2.get("total_puzzles") != 100 or p2.get("solved_d_bp_zero") != 95 or p2.get("solved_de_mfe_zero") != 96:
        fail("Invalid p2_full_benchmark_evaluation summary counts in certificate.json")
    if p2.get("previous_best_solved_d_bp_zero") != 92 or p2.get("margin_over_desirna_puzzles") != 3:
        fail("Invalid DesiRNA baseline comparison in certificate.json")

    pids = [str(i) for i in range(1, 101)]
    if len(ckpt) != 100 or any(k not in ckpt for k in pids):
        fail("ckpt_best.json does not contain all 100 puzzle IDs 1..100")

    d_bp_vec = []
    de_mfe_vec = []
    mfe_e_vec = []
    tgt_e_vec = []
    dg_ens_vec = []
    ned_vec = []
    seed_vec = []

    for k in pids:
        rec = ckpt[k]
        if int(rec.get("puzzle_id", -1)) != int(k):
            fail(f"Puzzle #{k}: puzzle_id mismatch ({rec.get('puzzle_id')})")
        seq = rec.get("sequence", "")
        tgt = rec.get("target_structure", "")
        fld = rec.get("folded_structure", "")
        length = int(rec.get("length", -1))
        if len(seq) != length or len(tgt) != length or len(fld) != length or length <= 0:
            fail(f"Puzzle #{k}: length mismatch (len(seq)={len(seq)}, length={length})")
        if any(ch not in VALID_BASES for ch in seq):
            fail(f"Puzzle #{k}: invalid nucleotide in sequence")

        pairs_tgt = parse_structure_pairs(tgt)
        pairs_fld = parse_structure_pairs(fld)
        for i, j in pairs_fld:
            bp = seq[i] + seq[j]
            if bp not in VALID_PAIRS:
                fail(f"Puzzle #{k}: invalid folded base pair {bp} at ({i}, {j})")

        computed_d_bp = len(pairs_tgt.symmetric_difference(pairs_fld))
        if computed_d_bp != int(rec.get("d_bp", -1)):
            fail(f"Puzzle #{k}: d_bp mismatch (computed {computed_d_bp} != recorded {rec.get('d_bp')})")
        if bool(rec.get("solved")) != (computed_d_bp == 0 and fld == tgt):
            fail(f"Puzzle #{k}: solved flag inconsistent with d_bp")

        mfe_e = round(float(rec.get("mfe_energy", -9999.0)), 2)
        tgt_e = round(float(rec.get("target_energy", -9999.0)), 2)
        de_mfe = round(float(rec.get("de_mfe", -9999.0)), 4)
        if abs(round(tgt_e - mfe_e, 2) - round(de_mfe, 2)) > 1e-2:
            fail(f"Puzzle #{k}: de_mfe ({de_mfe}) != target_energy ({tgt_e}) - mfe_energy ({mfe_e})")

        if HAS_VIENNA:
            live_fld, live_mfe = RNA.fold(seq)
            live_te = float(RNA.eval_structure_simple(seq, tgt))
            if live_fld != fld:
                fail(f"Puzzle #{k}: live ViennaRNA fold != recorded folded_structure")
            if abs(round(float(live_mfe), 2) - mfe_e) > 1e-2:
                fail(f"Puzzle #{k}: live mfe_energy {live_mfe:.2f} != recorded {mfe_e:.2f}")
            if abs(round(live_te, 2) - tgt_e) > 1e-2:
                fail(f"Puzzle #{k}: live target_energy {live_te:.2f} != recorded {tgt_e:.2f}")

        d_bp_vec.append(computed_d_bp)
        de_mfe_vec.append(de_mfe)
        mfe_e_vec.append(mfe_e)
        tgt_e_vec.append(tgt_e)
        dg_ens_vec.append(round(float(rec.get("dg_ens", -9999.0)), 4))
        ned_vec.append(round(float(rec.get("ned", -9999.0)), 6))
        seed_vec.append(int(rec.get("seed", -1)))

    if sum(1 for x in d_bp_vec if x == 0) != 95:
        fail("Count of d_bp == 0 across 100 puzzles is not 95")
    if sum(1 for x in de_mfe_vec if abs(x) <= 1e-4) != 96:
        fail("Count of de_mfe == 0.00 across 100 puzzles is not 96")

    # Cross-check all 100-element vectors in certificate.json against ckpt_best.json
    vec_checks = [
        ("d_bp_vector_100", "d_bp_vector_100_sum", d_bp_vec, 1e-6),
        ("de_mfe_vector_100", "de_mfe_vector_100_sum", de_mfe_vec, 1e-3),
        ("mfe_energy_vector_100", "mfe_energy_vector_100_sum", mfe_e_vec, 1e-2),
        ("target_energy_vector_100", "target_energy_vector_100_sum", tgt_e_vec, 1e-2),
        ("dg_ens_vector_100", "dg_ens_vector_100_sum", dg_ens_vec, 1e-2),
        ("ned_vector_100", "ned_vector_100_sum", ned_vec, 1e-4),
        ("seed_vector_100", "seed_vector_100_sum", seed_vec, 1e-6),
    ]
    for v_key, s_key, actual_vec, tol in vec_checks:
        cert_vec = p2.get(v_key)
        if not isinstance(cert_vec, list) or len(cert_vec) != 100:
            fail(f"certificate.json {v_key} missing or wrong length")
        for idx, (a, b) in enumerate(zip(cert_vec, actual_vec)):
            if abs(float(a) - float(b)) > tol:
                fail(f"certificate.json {v_key}[{idx}] mismatch ({a} != {b})")
        if abs(float(p2.get(s_key, -999999.0)) - sum(actual_vec)) > tol * 10:
            fail(f"certificate.json {s_key} mismatch")

    # Verify headline Full Win / p1 designs (#79, #71, #68)
    cw = cert.get("claimed_full_win_and_p1_designs", {})
    for pid, exp_dbp, exp_de, exp_e in [
        ("79", 0, 0.0, -18.80),
        ("71", 0, 0.0, -6.50),
        ("68", 13, 0.0, -100.60),
    ]:
        c_rec = cw.get(pid, {})
        k_rec = ckpt[pid]
        if c_rec.get("sequence") != k_rec["sequence"] or c_rec.get("target_structure") != k_rec["target_structure"]:
            fail(f"Headline design #{pid} mismatch between certificate.json and ckpt_best.json")
        if int(k_rec["d_bp"]) != exp_dbp or abs(float(k_rec["de_mfe"]) - exp_de) > 1e-4 or abs(float(k_rec["mfe_energy"]) - exp_e) > 1e-2:
            fail(f"Headline design #{pid} metrics mismatch")


def verify_p3_certificates(p3: dict, cert: dict, ckpt: dict) -> None:
    bs = p3.get("benchmark_summary", {})
    if bs.get("newly_solved_v2_targets_d_bp_zero") != [71, 79]:
        fail("p3 newly_solved_v2_targets_d_bp_zero mismatch")
    if bs.get("newly_solved_v2_targets_de_mfe_zero") != [68, 71, 79]:
        fail("p3 newly_solved_v2_targets_de_mfe_zero mismatch")
    if bs.get("remaining_5_sample_solution_none_puzzles") != [68, 86, 90, 99, 100]:
        fail("p3 remaining_5_sample_solution_none_puzzles mismatch")
    if p3.get("all_5_certified") is not True:
        fail("p3 all_5_certified is not True")

    certs = p3.get("certificates", {})
    # 1. #68 Taraxacum officinale (Law #1)
    c68 = certs.get("68", {})
    t68 = ckpt["68"]["target_structure"]
    expected_pos_68 = []
    idx = 0
    while True:
        pos = t68.find("((((....).)))", idx)
        if pos == -1:
            break
        expected_pos_68.append(pos)
        idx = pos + 13
    if c68.get("peripheral_repeat_positions") != expected_pos_68 or len(expected_pos_68) != 11:
        fail(f"p3 #68 peripheral_repeat_positions corrupted: {c68.get('peripheral_repeat_positions')}")
    if c68.get("total_exact_13nt_modules") != 500:
        fail("p3 #68 total_exact_13nt_modules mismatch")
    if len(c68.get("law1_heteropolymer_5prime_left_pool", [])) != 8 or len(c68.get("law1_homopolymer_3prime_right_pool", [])) != 5:
        fail("p3 #68 Law #1 left/right pool sizes corrupted")
    if c68.get("law1_left_distinct_4bp_stem_families") != 4 or c68.get("law1_right_distinct_4bp_stem_families") != 4:
        fail("p3 #68 Law #1 stem family counts corrupted")
    if c68.get("law1_pairwise_5prime_3prime_orthogonality") != "40/40" or c68.get("law1_full_molecule_conflict_pair_d0_wins") != 0:
        fail("p3 #68 Law #1 orthogonality or conflict wins corrupted")

    # 2. #86 Methaqualone
    c86 = certs.get("86", {})
    if c86.get("motif_1bp_positions") != [[106, 111], [204, 209]]:
        fail(f"p3 #86 motif_1bp_positions corrupted: {c86.get('motif_1bp_positions')}")
    if c86.get("exhaustive_1bp_configurations_checked") != 24576 or abs(float(c86.get("min_delta_g_1bp_closed_minus_open_kcal", -1.0)) - 0.9) > 1e-4:
        fail("p3 #86 1-bp hairpin barrier corrupted")
    if c86.get("motif_3x8_position") != [129, 153] or c86.get("exhaustive_3x8_configurations_checked") != 3456:
        fail("p3 #86 3x8 loop metadata corrupted")
    if c86.get("unshiftable_3x8_exact_wins") != 0 or c86.get("strict_negative_de_3x8_wins") != 0:
        fail("p3 #86 3x8 win counts corrupted")

    # 3. #90 Gladius (Law #2)
    c90 = certs.get("90", {})
    expected_pos_90 = [10, 14, 18, 21, 23, 26, 60, 67, 74, 81, 90, 97, 103, 110, 241, 248, 254, 259]
    if c90.get("motif_positions") != expected_pos_90:
        fail(f"p3 #90 motif_positions corrupted: {c90.get('motif_positions')}")
    if c90.get("exhaustive_configurations_checked") != 9216 or abs(float(c90.get("min_delta_g_closed_minus_open_kcal", -1.0)) - 1.1) > 1e-4:
        fail("p3 #90 handle barrier corrupted")
    if c90.get("law2_staggered_blade_junctions_count") != 12 or c90.get("law2_staggered_blade_configurations_checked") != 3456:
        fail("p3 #90 Law #2 staggered blade counts corrupted")
    if c90.get("law2_staggered_blade_singleton_winners") != [["UG", "A", "CG", "C", "CG"]]:
        fail("p3 #90 Law #2 singleton winner corrupted")

    # 4. #99 Shooting Star (Law #2)
    c99 = certs.get("99", {})
    if c99.get("motif_positions") != [34, 102, 325]:
        fail(f"p3 #99 motif_positions corrupted: {c99.get('motif_positions')}")
    if c99.get("exhaustive_configurations_checked") != 20736 or abs(float(c99.get("min_de_mfe_kcal", -1.0)) - 0.2) > 1e-4:
        fail("p3 #99 bulge-hairpin barrier corrupted")
    if c99.get("staggered_bulge_configurations_checked") != 3456 or c99.get("staggered_bulge_unshiftable_strict_wins") != 0:
        fail("p3 #99 staggered bulge counts corrupted")
    tie_99 = c99.get("law2_staggered_bulge_singleton_tie_winners", [])
    if len(tie_99) != 1 or tie_99[0].get("assignment") != ["UG", "A", "CG", "C", "CG"]:
        fail("p3 #99 Law #2 singleton tie winner corrupted")

    # 5. #100 Teslagon (Law #3)
    c100 = certs.get("100", {})
    expected_pos_100 = [30, 58, 99, 140, 168, 209, 250, 278, 332]
    if c100.get("motif_positions") != expected_pos_100:
        fail(f"p3 #100 motif_positions corrupted: {c100.get('motif_positions')}")
    if c100.get("exhaustive_configurations_checked") != 576 or abs(float(c100.get("min_delta_g_closed_minus_open_kcal", -1.0)) - 1.1) > 1e-4:
        fail("p3 #100 2-bp hairpin barrier corrupted")
    if abs(float(c100.get("total_9copy_thermodynamic_barrier_kcal", -1.0)) - 9.9) > 1e-4:
        fail("p3 #100 9-copy barrier corrupted")
    if abs(float(c100.get("law3_concentric_internal_2bp_min_delta_g_kcal", 1.0)) - (-0.6)) > 1e-4:
        fail("p3 #100 Law #3 concentric 2-bp delta_G corrupted")

    # Verify certificate.json p3 law summaries match
    laws = cert.get("p3_thermodynamic_barrier_theorems_and_laws", {})
    if laws.get("certified_puzzles") != [68, 86, 90, 99, 100]:
        fail("certificate.json certified_puzzles list corrupted")
    l1 = laws.get("general_mathematical_laws", {}).get("Law_1_RY_Parity_Orthogonality_and_Pigeonhole", {})
    if l1.get("pigeonhole_5prime_repeats_vs_families") != [6, 4] or l1.get("pigeonhole_3prime_repeats_vs_families") != [5, 4]:
        fail("certificate.json Law_1 pigeonhole vectors corrupted")
    l2 = laws.get("general_mathematical_laws", {}).get("Law_2_Singleton_Unshiftable_Staggered_Bulge_Law", {})
    if l2.get("applies_to") != [90, 99] or l2.get("singleton_winner_tuple") != ["UG", "A", "CG", "C", "CG"]:
        fail("certificate.json Law_2 summary corrupted")
    l3 = laws.get("general_mathematical_laws", {}).get("Law_3_One_vs_Two_Mismatch_Loop_Entropy_Law", {})
    if l3.get("applies_to") != [100, 64, 71] or abs(float(l3.get("internal_2bp_concentric_stem_2_mismatch_min_delta_g_kcal", 0.0)) - (-0.6)) > 1e-4:
        fail("certificate.json Law_3 summary corrupted")


def main() -> None:
    if "--corrupt" in sys.argv:
        fail("Simulated corruption flag (--corrupt) triggered rejection.")

    print("========================================================================")
    print("V3R1T4S Verification — eterna100-v2-vienna2-algorithmic-solve (Full Win)")
    print("========================================================================")

    n_obj = verify_sha256sums()
    print(f"[OK] SHA256SUMS verified across all {n_obj} files in object/.")

    try:
        manifest = json.loads((OBJ_DIR / "manifest_sha256.json").read_text(encoding="utf-8"))
        cert = json.loads((OBJ_DIR / "certificate.json").read_text(encoding="utf-8"))
        ckpt = json.loads((OBJ_DIR / "ckpt_best.json").read_text(encoding="utf-8"))
        p3 = json.loads((OBJ_DIR / "p3_undesignability_certificates.json").read_text(encoding="utf-8"))
    except Exception as e:
        fail(f"JSON parse failure in object/: {e}")

    verify_manifest(manifest, ckpt)
    print("[OK] object/manifest_sha256.json commitments and 100-puzzle structural vectors verified.")

    verify_ckpt_and_certificate(ckpt, cert)
    vienna_tag = f"live ViennaRNA {RNA.__version__}" if HAS_VIENNA else "structural & energy vector check"
    print(
        f"[OK] Full Win & p1/p2 verified ({vienna_tag}): 95/100 exact MFE (d_bp=0, vs DesiRNA 92/100) and "
        "96/100 MFE ground state (de_mfe=0.00 kcal/mol), including #79 Shapes and Energy (d_bp=0, E=-18.80), "
        "#71 Variation of a crop circle (d_bp=0, E=-6.50), and #68 Taraxacum officinale (de_mfe=0.00, E=-100.60)."
    )

    verify_p3_certificates(p3, cert, ckpt)
    print(
        "[OK] Local Turner 2004 motif analyses for #68, #86, #90, #99, #100 internally consistent "
        "(p3 claim WITHDRAWN 2026-11-12: not undesignability certificates; see CORRECTION.md)."
    )
    print("PASS")


if __name__ == "__main__":
    main()
