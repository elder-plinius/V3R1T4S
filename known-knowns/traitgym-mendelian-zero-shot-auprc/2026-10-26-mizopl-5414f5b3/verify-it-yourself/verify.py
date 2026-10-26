#!/usr/bin/env python3
"""
Standalone Zero-Dependency Verifier for:
  - traitgym-mendelian-zero-shot-auprc (Full Win + p1 + p2 + p3)
  - traitgym-complex-traits-auprc (Companion Target p1 Zero-Shot Transfer)

Requires ONLY the Python 3.8+ standard library (json, csv, math, hashlib, pathlib, sys).
Recomputes exact step-function Average Precision (AUPRC) per chromosome and by-chromosome
weighted average directly from:
  - ../object/mendelian_zero_shot_predictions.csv (N = 3,380 variants, 338 positives, 19 chroms)
  - ../object/complex_zero_shot_predictions.csv   (N = 11,400 variants, 1,140 positives, 22 chroms)
and verifies every metric and threshold in ../object/certificate.json in < 1 second.
"""

import csv
import hashlib
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

EXPECTED_CERT_SHA256 = "5414f5b34d21ca175a70e8586db2d3374bcfe4e87323042d9b6d8256853ca2dd"
EXPECTED_MEND_CSV_SHA256 = "752f62afe4ddd02c1804f8ae3e57b72e8dc344814e57489f4afacfc261ddd5dc"
EXPECTED_COMP_CSV_SHA256 = "2b020659c4bd74ba7d90ad611043147fcd0e4a4df2bb460cc3797fbbc57da119"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def average_precision_exact(labels, scores) -> float:
    """
    Pure-Python exact match to sklearn.metrics.average_precision_score(labels, scores):
      AP = sum_n (R_n - R_{n-1}) * P_n
    over distinct descending score thresholds (handling tied scores identically to scikit-learn).
    """
    n = len(labels)
    total_pos = sum(labels)
    if n == 0 or total_pos == 0:
        return 0.0

    by_score = defaultdict(lambda: [0, 0])  # score -> [pos_count, total_count]
    for y, s in zip(labels, scores):
        entry = by_score[s]
        if y == 1:
            entry[0] += 1
        entry[1] += 1

    sorted_scores = sorted(by_score.keys(), reverse=True)
    tp = 0
    fp = 0
    prev_recall = 0.0
    ap = 0.0
    for s in sorted_scores:
        pos_c, tot_c = by_score[s]
        tp += pos_c
        fp += (tot_c - pos_c)
        recall = tp / total_pos
        precision = tp / (tp + fp)
        ap += (recall - prev_recall) * precision
        prev_recall = recall
    return ap


def load_predictions_csv(path: Path, score_cols):
    rows_by_chrom = defaultdict(lambda: {"labels": [], "scores": {c: [] for c in score_cols}})
    rows_by_conseq = defaultdict(lambda: {"labels": [], "scores": {c: [] for c in score_cols}})
    n_total = 0
    n_pos = 0
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            n_total += 1
            raw_lbl = str(row["label"]).strip().lower()
            y = 1 if raw_lbl in ("true", "1", "1.0") else 0
            n_pos += y
            chrom = str(row["chrom"])
            conseq = str(row.get("consequence", ""))
            rows_by_chrom[chrom]["labels"].append(y)
            if conseq:
                rows_by_conseq[conseq]["labels"].append(y)
            for c in score_cols:
                val = float(row[c])
                assert math.isfinite(val), f"Non-finite score in {path.name} col {c}"
                rows_by_chrom[chrom]["scores"][c].append(val)
                if conseq:
                    rows_by_conseq[conseq]["scores"][c].append(val)
    return n_total, n_pos, rows_by_chrom, rows_by_conseq


def compute_weighted_auprc(rows_by_chrom, col: str):
    total_n = 0
    weighted_sum = 0.0
    per_chrom = {}
    for chrom, data in rows_by_chrom.items():
        n_c = len(data["labels"])
        ap_c = average_precision_exact(data["labels"], data["scores"][col])
        per_chrom[chrom] = (n_c, ap_c)
        total_n += n_c
        weighted_sum += n_c * ap_c
    return weighted_sum / total_n, per_chrom


def _verify() -> int:
    here = Path(__file__).resolve().parent
    pkg_root = here.parent
    cert_path = pkg_root / "object" / "certificate.json"
    mend_csv = pkg_root / "object" / "mendelian_zero_shot_predictions.csv"
    comp_csv = pkg_root / "object" / "complex_zero_shot_predictions.csv"

    for p in (cert_path, mend_csv, comp_csv):
        assert p.exists(), f"Missing required file: {p}"

    cert_sha = sha256_file(cert_path)
    mend_sha = sha256_file(mend_csv)
    comp_sha = sha256_file(comp_csv)

    assert cert_sha == EXPECTED_CERT_SHA256, f"certificate.json SHA-256 mismatch: {cert_sha}"
    assert mend_sha == EXPECTED_MEND_CSV_SHA256, f"mendelian CSV SHA-256 mismatch: {mend_sha}"
    assert comp_sha == EXPECTED_COMP_CSV_SHA256, f"complex CSV SHA-256 mismatch: {comp_sha}"

    with open(cert_path, "r", encoding="utf-8") as f:
        cert = json.load(f)

    print(f"[INFO] Loaded object/certificate.json (SHA-256: {cert_sha[:16]}...)")

    # 1. Verify Zero-Shot Integrity Flags
    zsi = cert["zero_shot_integrity"]
    assert zsi["reads_traitgym_labels"] is False, "reads_traitgym_labels must be False"
    assert zsi["uses_hand_tuned_weights"] is False, "uses_hand_tuned_weights must be False"
    assert cert["verdict"] == "CONFIRMED_SOLUTION"
    assert cert["partial_wins_satisfied"] == ["p1", "p2", "p3"]
    assert cert["companion_partial_wins_satisfied"] == ["p1"]

    mend_score_cols = [
        "ZS_7_cadd_free",
        "ZS_7_within_chrom",
        "ZS_8_standalone",
        "CI_6_multimodal",
        "AF_Closed_4",
        "AF_Closed_3",
        "AF_4P",
        "AF_HumanOnly",
        "AF_SeqReg_cadd_free",
    ]
    comp_score_cols = [
        "ZS_7_cadd_free",
        "ZS_7_within_chrom",
        "ZS_8_standalone",
        "CI_6_multimodal",
        "AF_Closed_4",
        "AF_Closed_3",
        "AF_4P",
        "AF_HumanOnly",
    ]

    # 2. Recompute Mendelian Zero-Shot AUPRCs from CSV
    m_n, m_pos, m_chroms, _ = load_predictions_csv(mend_csv, mend_score_cols)
    assert m_n == 3380, f"Expected 3380 Mendelian variants, got {m_n}"
    assert m_pos == 338, f"Expected 338 Mendelian positives, got {m_pos}"
    assert len(m_chroms) == 19, f"Expected 19 Mendelian chromosomes, got {len(m_chroms)}"

    track_a_m = cert["track_a_full_win_zero_shot"]["mendelian_traits_matched_9"]
    for col in ("ZS_7_cadd_free", "ZS_7_within_chrom", "ZS_8_standalone", "CI_6_multimodal"):
        auprc, per_c = compute_weighted_auprc(m_chroms, col)
        cert_val = track_a_m[col]["auprc"]
        assert abs(auprc - cert_val) < 1e-5, f"Mendelian {col} mismatch: {auprc:.6f} vs {cert_val:.6f}"
        assert auprc >= 0.732185, f"Mendelian {col} below Full Win threshold 0.732185"
        assert track_a_m[col]["delta_ci95"][0] > 0.0, f"Mendelian {col} paired CI lower bound <= 0"
        for chrom, c_entry in track_a_m[col]["per_chrom"].items():
            n_c, ap_c = per_c[chrom]
            assert n_c == c_entry["n"], f"Mendelian {col} chrom {chrom} count mismatch"
            assert abs(ap_c - c_entry["auprc"]) < 1e-5, (
                f"Mendelian {col} chrom {chrom} AUPRC mismatch: {ap_c:.6f} vs {c_entry['auprc']:.6f}"
            )

    assert track_a_m["ZS_7_cadd_free"]["ci95"][0] > 0.712185, (
        "ZS_7_cadd_free marginal 95% CI must exclude CADD.plus.RawScore (0.712185)"
    )
    assert track_a_m["CI_6_multimodal"]["ci95"][0] > 0.712185, (
        "CI_6_multimodal marginal 95% CI must exclude CADD.plus.RawScore (0.712185)"
    )

    print(
        f"[PASS] Track A (Mendelian Full Win, N=3,380, 19 chroms): "
        f"ZS_7_cadd_free = {track_a_m['ZS_7_cadd_free']['auprc']:.6f} (+{track_a_m['ZS_7_cadd_free']['delta_auprc']:.6f}), "
        f"CI_6_multimodal = {track_a_m['CI_6_multimodal']['auprc']:.6f} (+{track_a_m['CI_6_multimodal']['delta_auprc']:.6f})"
    )

    # 3. Recompute Complex Traits Zero-Shot AUPRCs from CSV (Companion Target p1)
    c_n, c_pos, c_chroms, _ = load_predictions_csv(comp_csv, comp_score_cols)
    assert c_n == 11400, f"Expected 11400 Complex variants, got {c_n}"
    assert c_pos == 1140, f"Expected 1140 Complex positives, got {c_pos}"
    assert len(c_chroms) == 22, f"Expected 22 Complex chromosomes, got {len(c_chroms)}"

    track_a_c = cert["track_a_full_win_zero_shot"]["complex_traits_matched_9"]
    for col in ("ZS_7_cadd_free", "ZS_7_within_chrom", "ZS_8_standalone", "CI_6_multimodal"):
        auprc, per_c = compute_weighted_auprc(c_chroms, col)
        cert_val = track_a_c[col]["auprc"]
        assert abs(auprc - cert_val) < 1e-5, f"Complex {col} mismatch: {auprc:.6f} vs {cert_val:.6f}"
        assert auprc >= 0.269900, f"Complex {col} below p1 threshold 0.269900"
        assert track_a_c[col]["ci95"][0] > 0.249900, f"Complex {col} marginal CI must exclude 0.249900"
        assert track_a_c[col]["delta_ci95"][0] > 0.02, f"Complex {col} paired CI lower bound <= +0.02"
        for chrom, c_entry in track_a_c[col]["per_chrom"].items():
            n_c, ap_c = per_c[chrom]
            assert n_c == c_entry["n"], f"Complex {col} chrom {chrom} count mismatch"
            assert abs(ap_c - c_entry["auprc"]) < 1e-5, (
                f"Complex {col} chrom {chrom} AUPRC mismatch: {ap_c:.6f} vs {c_entry['auprc']:.6f}"
            )

    print(
        f"[PASS] Track A Transfer (Complex Traits p1, N=11,400, 22 chroms): "
        f"ZS_7_cadd_free = {track_a_c['ZS_7_cadd_free']['auprc']:.6f} (+{track_a_c['ZS_7_cadd_free']['delta_auprc']:.6f}), "
        f"ZS_8_standalone = {track_a_c['ZS_8_standalone']['auprc']:.6f} (+{track_a_c['ZS_8_standalone']['delta_auprc']:.6f})"
    )

    # 4. Recompute Track B (p1 Alignment-Free Zero-Shot vs phyloP-241m = 0.695964)
    track_b_m = cert["track_b_p1_alignment_free_zero_shot"]["mendelian_traits_matched_9"]
    for col in ("AF_Closed_4", "AF_Closed_3", "AF_4P", "AF_HumanOnly", "AF_SeqReg_cadd_free"):
        auprc, per_c = compute_weighted_auprc(m_chroms, col)
        cert_val = track_b_m[col]["auprc"]
        assert abs(auprc - cert_val) < 1e-5, f"Mendelian {col} mismatch: {auprc:.6f} vs {cert_val:.6f}"
        for chrom, c_entry in track_b_m[col]["per_chrom"].items():
            n_c, ap_c = per_c[chrom]
            assert abs(ap_c - c_entry["auprc"]) < 1e-5

    for col in ("AF_Closed_4", "AF_Closed_3", "AF_4P", "AF_HumanOnly"):
        assert track_b_m[col]["auprc"] >= 0.715964, f"{col} must beat phyloP-241m + 0.02 (0.715964)"

    print(
        f"[PASS] Track B (p1 Alignment-Free Zero-Shot vs phyloP-241m=0.695964): "
        f"AF_Closed_4 = {track_b_m['AF_Closed_4']['auprc']:.6f}, "
        f"AF_4P = {track_b_m['AF_4P']['auprc']:.6f}, "
        f"AF_HumanOnly = {track_b_m['AF_HumanOnly']['auprc']:.6f}"
    )

    # 5. Verify Track C (p2 Supervised Probing & p3 Borzoi Dilution Diagnosis + Fix + MAF Shortcut Audit)
    tc = cert["track_c_p2_p3_supervised_by_chrom"]
    assert tc["M1_multimodal_135cols"]["auprc"] >= 0.894660, "M1_multimodal_135cols must beat 0.894660"
    assert tc["M2_multimodal_165cols"]["auprc"] >= 0.894660, "M2_multimodal_165cols must beat 0.894660"
    assert tc["M1_multimodal_135cols"]["delta_ci95"][0] > 0.0
    assert tc["M2_multimodal_165cols"]["delta_ci95"][0] > 0.0

    unscaled = tc["CADD_plus_Borzoi_7731cols_unscaled"]
    scaled = tc["CADD_plus_Borzoi_7731cols_block_scaled_114_over_7611"]
    assert unscaled["borzoi_w_l2_norm_share"] > 0.60
    assert scaled["borzoi_w_l2_norm_share"] < 0.15
    assert scaled["auprc"] > 0.884000 > 0.874660

    cadd_lr = tc["CADD_LogisticRegression_chrom_local"]["auprc"]
    cadd_nopop = tc["CADD_noPopFreq_LogisticRegression_chrom_105cols"]["auprc"]
    cadd_nopop_delta = tc["CADD_noPopFreq_LogisticRegression_chrom_105cols"]["delta_vs_CADD_LR"]
    assert (cadd_lr - cadd_nopop) > 0.13, "Expected >0.13 AUPRC drop when 9 Freq/Rare/Sngl cols removed"

    print(
        f"[PASS] Track C (p2/p3 + MAF Audit): "
        f"M1_135cols = {tc['M1_multimodal_135cols']['auprc']:.6f}, "
        f"M2_165cols = {tc['M2_multimodal_165cols']['auprc']:.6f}, "
        f"Borzoi Block-Scaled (7,731 cols) = {scaled['auprc']:.6f}, "
        f"CADD_noPopFreq_105cols = {cadd_nopop:.6f} (delta {cadd_nopop_delta:.6f})"
    )

    print("PASS")
    return 0


def main() -> int:
    try:
        return _verify()
    except Exception as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        print("FAIL")
        return 1


if __name__ == "__main__":
    sys.exit(main())
