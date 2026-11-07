#!/usr/bin/env python3
"""
Standalone Zero-Trust Verifier for V3R1T4S Target `tdc-dti-dg-bindingdb-patent-pcc`
(`TDC DTI Domain-Generalization: BindingDB patent-year split`, Package `2026-10-29-mizopl-d0d5d2a2`).

Verifies:
  1. `object/manifest_sha256.json`: Official TDC dataset URLs, SHA-256 commitments (`dti_dg_group.zip`,
     `train_val.csv`, `test.csv`), split row counts (`[183430, 49028, 24514, 24514]`), zero `.DS_Store` or
     `__MACOSX` entries, and official `(row_index, Drug_ID, Target_ID)` key commitments.
  2. `object/certificate.json` & `object/certificate_phase1_cpu_p1_p2.json`:
     - Claim status (`CONFIRMED_PARTIAL`, `claimed_partial_win: p1`, primary track `trackA_strict_train`),
     - Pre-test `train_val` (2013-2018) inner temporal validation progression (`step02`..`step07`:
       Split A `0.45340 -> 0.62386`, Split B `0.45172 -> 0.60613`) fixed prior to first test evaluation (`step08`),
     - Full 6-run test evaluation audit (`1` primary evaluation in `step08` + `5` exploratory Phase-2 runs),
     - Cross-consistency of all 5-seed Pearson correlations (`PCC`), subset breakdowns, and 10,000-resample
       bootstrap intervals between `certificate.json` and `certificate_phase1_cpu_p1_p2.json`.
  3. All 40 keyed prediction CSV part files (`object/seed_{1..5}_{track}_part{1,2}.csv`):
     - Reassembles `part1` (rows `0..24513`) + `part2` (rows `24514..49027`) into the 49,028-row test table,
     - Verifies exact `(row_index, Drug_ID, Target_ID)` key ordering (`test_pair_ids_sha256`),
     - Verifies per-part SHA-256 hashes, per-part L1/L2 norms, full-vector `mean`/`std`/`l1_norm`/`l2_norm`,
       and the 5x5 `cross_seed_dot_matrix` for every track (`trackA_strict_train`, `trackB_trainval_refit`,
       `erm_baseline`, `trackF1_bayes_mmse72`).
  4. Direct Ground-Truth Rescoring against Official TDC `test.csv` & `train_val.csv` (when staged in
     `TDC_DATA_DIR` or `tempfile.gettempdir() / "tdc_dti_dg_data"`):
     - Verifies SHA-256 of `train_val.csv` and `test.csv`, verifies `test_drug_target_keys_sha256` and
       exact row-by-row `(Drug_ID, Target_ID)` identity against `test.csv`, and recomputes all 5-seed
       Pearson correlations, per-year (`2019 / 2020 / 2021`) PCCs, and `Seen-Target` / `Unseen-Target` /
       `Unseen-Ligand` PCCs directly against `test.csv["Y"]`.
"""
import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import pearsonr

ROOT = Path(__file__).resolve().parent.parent
OBJ_DIR = ROOT / "object"
SPLIT_HALF = 24514
N_TEST = 49028


def fail(msg: str):
    print(f"VERIFY ERROR: {msg}")
    print("FAIL")
    sys.exit(1)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_and_verify_track_parts(
    track_key: str,
    track_meta: dict,
    expected_pair_ids_sha256: str,
    check_file_sha: bool = True,
) -> np.ndarray:
    """
    Loads all 5 seeds (part1 + part2) for `track_key`, verifies row_index 0..49027,
    verifies `(row_index, Drug_ID, Target_ID)` key SHA-256, and checks per-part and
    full-vector moments + 5x5 cross-seed Gram matrix.
    """
    part_files_meta = track_meta.get("part_files", {})
    seeds_meta = track_meta.get("seeds", {})
    if len(part_files_meta) != 10 or len(seeds_meta) != 5:
        fail(f"Track {track_key}: expected 10 part_files and 5 seeds, got {len(part_files_meta)} and {len(seeds_meta)}")

    seed_vecs = []
    ref_pair_ids_sha = None

    for s in range(1, 6):
        s_str = str(s)
        if s_str not in seeds_meta:
            fail(f"Track {track_key}: missing seed {s_str}")
        s_info = seeds_meta[s_str]

        p1_name = f"seed_{s}_{track_key}_part1.csv"
        p2_name = f"seed_{s}_{track_key}_part2.csv"
        p1_path = OBJ_DIR / p1_name
        p2_path = OBJ_DIR / p2_name

        if not p1_path.is_file() or not p2_path.is_file():
            fail(f"Track {track_key} seed {s}: missing {p1_name} or {p2_name}")

        p1_bytes = p1_path.read_bytes()
        p2_bytes = p2_path.read_bytes()

        if check_file_sha:
            h1 = sha256_bytes(p1_bytes)
            h2 = sha256_bytes(p2_bytes)
            if h1 != part_files_meta[p1_name]["sha256"] or h1 != s_info["part1_sha256"]:
                fail(f"{p1_name}: sha256 mismatch ({h1} != {s_info['part1_sha256']})")
            if h2 != part_files_meta[p2_name]["sha256"] or h2 != s_info["part2_sha256"]:
                fail(f"{p2_name}: sha256 mismatch ({h2} != {s_info['part2_sha256']})")

        df1 = pd.read_csv(p1_path, dtype={"Drug_ID": str, "Target_ID": str})
        df2 = pd.read_csv(p2_path, dtype={"Drug_ID": str, "Target_ID": str})

        expected_cols = ["row_index", "Drug_ID", "Target_ID", "y_pred"]
        if list(df1.columns) != expected_cols or list(df2.columns) != expected_cols:
            fail(f"Track {track_key} seed {s}: unexpected CSV columns {list(df1.columns)} / {list(df2.columns)}")

        if len(df1) != SPLIT_HALF or len(df2) != N_TEST - SPLIT_HALF:
            fail(f"Track {track_key} seed {s}: unexpected part row counts {len(df1)}, {len(df2)}")

        v1 = df1["y_pred"].values.astype(np.float64)
        v2 = df2["y_pred"].values.astype(np.float64)
        if not (np.all(np.isfinite(v1)) and np.all(np.isfinite(v2))):
            fail(f"Track {track_key} seed {s}: non-finite predictions detected")

        # Check part-level moments
        for p_label, v_part, p_meta in [("part1", v1, part_files_meta[p1_name]), ("part2", v2, part_files_meta[p2_name])]:
            l1_p = float(np.sum(np.abs(v_part)))
            l2_p = float(np.sqrt(np.sum(v_part * v_part)))
            m_p = float(np.mean(v_part))
            sd_p = float(np.std(v_part))
            if abs(l1_p - float(p_meta["l1_norm"])) > 1e-7:
                fail(f"Track {track_key} seed {s} {p_label}: l1_norm mismatch ({l1_p:.8f} vs {p_meta['l1_norm']:.8f})")
            if abs(l2_p - float(p_meta["l2_norm"])) > 1e-7:
                fail(f"Track {track_key} seed {s} {p_label}: l2_norm mismatch ({l2_p:.8f} vs {p_meta['l2_norm']:.8f})")
            if abs(m_p - float(p_meta["mean"])) > 1e-8 or abs(sd_p - float(p_meta["std"])) > 1e-8:
                fail(f"Track {track_key} seed {s} {p_label}: mean/std mismatch")

        df_full = pd.concat([df1, df2], ignore_index=True)
        row_idx = df_full["row_index"].values
        if not np.array_equal(row_idx, np.arange(N_TEST, dtype=row_idx.dtype)):
            fail(f"Track {track_key} seed {s}: row_index is not 0..{N_TEST - 1}")

        # Verify (row_index, Drug_ID, Target_ID) key hash on every seed
        pair_str = "\n".join(
            f"{i}\t{d}\t{t}"
            for i, d, t in zip(row_idx, df_full["Drug_ID"].tolist(), df_full["Target_ID"].tolist())
        )
        pair_sha = sha256_bytes(pair_str.encode("utf-8"))
        if pair_sha != expected_pair_ids_sha256:
            fail(f"Track {track_key} seed {s}: (row_index, Drug_ID, Target_ID) key hash mismatch")

        vec = np.concatenate([v1, v2])
        l1_full = float(np.sum(np.abs(vec)))
        l2_full = float(np.sqrt(np.sum(vec * vec)))
        m_full = float(np.mean(vec))
        sd_full = float(np.std(vec))
        if (
            abs(l1_full - float(s_info["l1_norm"])) > 1e-7
            or abs(l2_full - float(s_info["l2_norm"])) > 1e-7
            or abs(m_full - float(s_info["pred_mean"])) > 1e-8
            or abs(sd_full - float(s_info["pred_std"])) > 1e-8
            or abs(float(np.sum(np.abs(v1))) - float(s_info["part1_l1_norm"])) > 1e-7
            or abs(float(np.sum(np.abs(v2))) - float(s_info["part2_l1_norm"])) > 1e-7
        ):
            fail(f"Track {track_key} seed {s}: full-vector moment mismatch against certificate")

        seed_vecs.append(vec)

    mat = np.vstack(seed_vecs)  # (5, 49028)
    dot_mat = mat @ mat.T
    cert_dot = np.array(track_meta["cross_seed_dot_matrix"], dtype=np.float64)
    if cert_dot.shape != (5, 5) or np.max(np.abs(dot_mat - cert_dot)) > 1e-1:
        fail(f"Track {track_key}: 5x5 cross_seed_dot_matrix mismatch")

    return mat


def main():
    corrupt_mode = "--corrupt" in sys.argv
    single_obj = os.environ.get("ZERO_TRUST_SINGLE_OBJECT", "").strip()

    manifest_path = OBJ_DIR / "manifest_sha256.json"
    cert_path = OBJ_DIR / "certificate.json"
    phase1_path = OBJ_DIR / "certificate_phase1_cpu_p1_p2.json"

    for req_p in (manifest_path, cert_path, phase1_path):
        if not req_p.is_file():
            fail(f"Missing required certificate file: {req_p.name}")

    # Verify object/ files against SHA256SUMS (catches any 1-byte/1-digit unhashed corruption)
    sha256sums_path = ROOT / "SHA256SUMS"
    if sha256sums_path.is_file():
        for line in sha256sums_path.read_text(encoding="utf-8").splitlines():
            parts = line.strip().split(None, 1)
            if len(parts) == 2 and parts[1].startswith("object/"):
                exp_h, rel_p = parts[0], parts[1]
                fp = ROOT / rel_p
                if not fp.is_file() or sha256_file(fp) != exp_h:
                    fail(f"{rel_p}: SHA-256 mismatch against SHA256SUMS")

    # Ensure banned files from review are absent
    for banned_name in ("test_labels_and_strata.csv", "skeptic_audit_certificate_fullwin.json"):
        if (OBJ_DIR / banned_name).exists():
            fail(f"Forbidden file present in object/: {banned_name}")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    cert = json.loads(cert_path.read_text(encoding="utf-8"))
    phase1 = json.loads(phase1_path.read_text(encoding="utf-8"))

    if corrupt_mode:
        # Simulate adversarial tampering of the primary prediction vector
        cert["tracks"]["trackA_strict_train"]["mean_5seed_pcc"] = 0.41000

    # 1. Verify `object/manifest_sha256.json`
    if manifest.get("benchmark_group") != "DTI_DG_Group" or manifest.get("benchmark_name") != "bindingdb_patent":
        fail("manifest_sha256.json: invalid benchmark_group or benchmark_name")
    if manifest.get("split_row_counts") != [183430, 49028, 24514, 24514]:
        fail(f"manifest_sha256.json: unexpected split_row_counts {manifest.get('split_row_counts')}")

    m_files = manifest.get("files", {})
    for k in m_files:
        if ".DS_Store" in k or "__MACOSX" in k:
            fail(f"manifest_sha256.json contains forbidden OS metadata entry: {k}")

    expected_zip_sha = "4708233b8536d856a9ee6522623e4d44bbf7d2efc1c8496e69f6cd2c6482457a"
    expected_tv_sha = "1cb713579f1a9f6f5fe0374e8939da8ae0e6b187fd24c0b0197b54c81ec486b6"
    expected_te_sha = "3124f012b92c8c00de39a82ae0ef9d3dd5cc135732bd8bfd420629e1a13dec31"
    expected_keys_sha = "b28e09b01f7990c55ede2facbe7b9831c6dc9203d140dc575814361ae649b674"

    if (
        m_files.get("data/dti_dg_group.zip", {}).get("sha256") != expected_zip_sha
        or m_files.get("data/dti_dg_group.zip", {}).get("size_bytes") != 9515670
        or m_files.get("data/dti_dg_group/bindingdb_patent/train_val.csv", {}).get("sha256") != expected_tv_sha
        or m_files.get("data/dti_dg_group/bindingdb_patent/train_val.csv", {}).get("size_bytes") != 167715236
        or m_files.get("data/dti_dg_group/bindingdb_patent/test.csv", {}).get("sha256") != expected_te_sha
        or m_files.get("data/dti_dg_group/bindingdb_patent/test.csv", {}).get("size_bytes") != 44933376
    ):
        fail("manifest_sha256.json: official TDC file sha256 or size_bytes mismatch")

    if manifest.get("test_drug_target_keys_sha256") != expected_keys_sha:
        fail("manifest_sha256.json: test_drug_target_keys_sha256 mismatch")

    eda = manifest.get("eda", {})
    if (
        eda.get("train_val_rows") != 183430
        or eda.get("test_rows") != 49028
        or eda.get("test_rows_seen_target") != 45031
        or eda.get("test_rows_unseen_target") != 3997
        or eda.get("test_rows_unseen_drug") != 30959
        or eda.get("test_years") != {"2019": 42009, "2020": 6947, "2021": 72}
    ):
        fail("manifest_sha256.json: EDA row/stratum counts mismatch")

    expected_pair_ids_sha = manifest.get("test_pair_ids_sha256", "")
    if len(expected_pair_ids_sha) != 64:
        fail("manifest_sha256.json: missing test_pair_ids_sha256")

    # 2. Verify `object/certificate.json` and `object/certificate_phase1_cpu_p1_p2.json`
    for cname, cobj in [("certificate.json", cert), ("certificate_phase1_cpu_p1_p2.json", phase1)]:
        if cobj.get("target_id") != "tdc-dti-dg-bindingdb-patent-pcc":
            fail(f"{cname}: invalid target_id")
        if cobj.get("status") != "CONFIRMED_PARTIAL" or cobj.get("claimed_partial_win") != "p1":
            fail(f"{cname}: expected status=CONFIRMED_PARTIAL and claimed_partial_win=p1")
        tdc_data = cobj.get("official_tdc_data", {})
        if (
            tdc_data.get("dti_dg_group_zip_sha256") != expected_zip_sha
            or tdc_data.get("train_val_csv_sha256") != expected_tv_sha
            or tdc_data.get("test_csv_sha256") != expected_te_sha
            or tdc_data.get("test_drug_target_keys_sha256") != expected_keys_sha
            or tdc_data.get("test_pair_ids_sha256") != expected_pair_ids_sha
        ):
            fail(f"{cname}: official_tdc_data sha256 mismatch")

        pre_val = cobj.get("pre_test_inner_temporal_validation", {})
        if pre_val.get("inner_split_progression_A") != [0.45340, 0.50615, 0.57503, 0.57548, 0.60856, 0.62386]:
            fail(f"{cname}: inner_split_progression_A tampered")
        if pre_val.get("inner_split_progression_B") != [0.45172, 0.50157, 0.55863, 0.56207, 0.58805, 0.60613]:
            fail(f"{cname}: inner_split_progression_B tampered")

    audit = cert.get("test_evaluation_audit", {})
    if (
        audit.get("total_test_evaluations_across_campaign") != 6
        or audit.get("claimed_primary_track_test_evaluation_index") != 1
        or len(audit.get("chronological_test_runs", [])) != 6
    ):
        fail("certificate.json: test_evaluation_audit tampered")

    # Verify cross-consistency between certificate.json and certificate_phase1_cpu_p1_p2.json
    track_map_phase1 = {
        "trackA_strict_train": "track_a_strict_train_s",
        "trackB_trainval_refit": "track_b_train_val_refit",
        "erm_baseline": "erm_baseline",
    }
    expected_track_summaries = {
        "trackA_strict_train": (
            0.57942175,
            0.00298974,
            [0.57855558, 0.58064482, 0.58093959, 0.58286534, 0.57410342],
            0.58250360,
            "claimed_primary",
        ),
        "trackB_trainval_refit": (
            0.57105900,
            0.00259652,
            [0.57186805, 0.57245591, 0.56799687, 0.57475515, 0.56821903],
            0.57170656,
            "exploratory_ablation",
        ),
        "erm_baseline": (
            0.51309713,
            0.00271205,
            [0.51182770, 0.51470468, 0.51220629, 0.51735054, 0.50939642],
            0.51635680,
            "reproduced_baseline",
        ),
        "trackF1_bayes_mmse72": (
            0.59996069,
            0.00265531,
            [0.59972456, 0.60142321, 0.60338044, 0.59993663, 0.59533864],
            0.60394441,
            "exploratory_ablation",
        ),
    }

    for t_key, (exp_m, exp_sd, exp_seeds, exp_ens, exp_role) in expected_track_summaries.items():
        if t_key not in cert.get("tracks", {}):
            fail(f"certificate.json: missing track {t_key}")
        tm = cert["tracks"][t_key]
        if tm.get("role") != exp_role:
            fail(f"certificate.json/{t_key}: role mismatch ({tm.get('role')} != {exp_role})")
        s_pccs = tm.get("seed_pccs", [])
        if len(s_pccs) != 5 or any(abs(float(a) - b) > 1e-6 for a, b in zip(s_pccs, exp_seeds)):
            fail(f"certificate.json/{t_key}: seed_pccs mismatch")
        if abs(float(tm["mean_5seed_pcc"]) - exp_m) > 1e-6 or abs(float(tm["std_5seed_pcc"]) - exp_sd) > 1e-6:
            fail(f"certificate.json/{t_key}: mean/std 5-seed PCC mismatch")
        if abs(float(tm["ensemble_5seed_avg_pcc"]) - exp_ens) > 1e-5:
            fail(f"certificate.json/{t_key}: ensemble_5seed_avg_pcc mismatch")

        if t_key in track_map_phase1:
            p1_key = track_map_phase1[t_key]
            if p1_key not in phase1.get("tracks", {}):
                fail(f"certificate_phase1_cpu_p1_p2.json: missing track {p1_key}")
            tm_p1 = phase1["tracks"][p1_key]
            if tm_p1.get("seed_pccs") != s_pccs or abs(float(tm_p1["mean_5seed_pcc"]) - exp_m) > 1e-6:
                fail(f"certificate_phase1_cpu_p1_p2.json/{p1_key}: mismatch vs certificate.json")
            if tm_p1.get("cross_seed_dot_matrix") != tm.get("cross_seed_dot_matrix"):
                fail(f"certificate_phase1_cpu_p1_p2.json/{p1_key}: cross_seed_dot_matrix mismatch")

    # Check bootstrap intervals
    boot_a = cert.get("bootstrap_10000_resamples", {}).get("trackA_strict_train", {})
    boot_a_p1 = phase1.get("bootstrap_10000_resamples", {}).get("track_a_strict_train_s", {})
    if (
        boot_a != boot_a_p1
        or boot_a.get("n_resamples") != 10000
        or abs(float(boot_a.get("boot_mean_pcc", 0.0)) - 0.58252792) > 1e-5
        or float(boot_a.get("win_rate_vs_0.538", 0.0)) != 1.0
    ):
        fail("Bootstrap 10,000-resample certificate for Track A tampered")

    # 3. Load and verify the keyed CSV part files
    # If ZERO_TRUST_SINGLE_OBJECT targets a single CSV part file, verify that track's parts;
    # otherwise verify all 40 CSV part files across all 4 tracks.
    if single_obj.endswith(".csv"):
        matched_tracks = [tk for tk in expected_track_summaries if f"_{tk}_" in single_obj]
        if not matched_tracks:
            fail(f"Unknown single object CSV target: {single_obj}")
        tracks_to_check = matched_tracks
        check_sha_flag = True
    elif single_obj.endswith(".json"):
        tracks_to_check = ["trackA_strict_train"]
        check_sha_flag = True
    else:
        tracks_to_check = list(expected_track_summaries.keys())
        check_sha_flag = True

    loaded_mats = {}
    for tk in tracks_to_check:
        loaded_mats[tk] = load_and_verify_track_parts(
            tk,
            cert["tracks"][tk],
            expected_pair_ids_sha,
            check_file_sha=check_sha_flag,
        )

    # 4. If official TDC `test.csv` & `train_val.csv` are available locally (and not in single-object fast mode),
    # run full ground-truth rescoring directly against `test.csv["Y"]`!
    if not single_obj:
        cand_dirs = []
        if os.environ.get("TDC_DATA_DIR"):
            cand_dirs.append(Path(os.environ["TDC_DATA_DIR"]))
        cand_dirs.append(Path(tempfile.gettempdir()) / "tdc_dti_dg_data")
        cand_dirs.append(ROOT / "how-we-built-it" / "data" / "dti_dg_group" / "bindingdb_patent")

        tdc_dir = None
        for d in cand_dirs:
            if (d / "test.csv").is_file() and (d / "train_val.csv").is_file():
                tdc_dir = d
                break

        if tdc_dir is not None:
            tv_csv = tdc_dir / "train_val.csv"
            te_csv = tdc_dir / "test.csv"
            if sha256_file(tv_csv) != expected_tv_sha or sha256_file(te_csv) != expected_te_sha:
                fail(f"Staged TDC data in {tdc_dir} failed official SHA-256 check")

            tv_df = pd.read_csv(tv_csv)
            te_df = pd.read_csv(te_csv)
            y_true = te_df["Y"].values.astype(np.float64)
            years = te_df["Year"].values.astype(np.int32)
            seen_t = te_df["Target"].isin(set(tv_df["Target"])).values
            unseen_t = ~seen_t
            seen_d = te_df["Drug"].isin(set(tv_df["Drug"])).values
            unseen_d = ~seen_d

            for tk, mat in loaded_mats.items():
                tm = cert["tracks"][tk]
                for s in range(1, 6):
                    vec = mat[s - 1]
                    s_info = tm["seeds"][str(s)]
                    p_all = float(pearsonr(vec, y_true)[0])
                    p_st = float(pearsonr(vec[seen_t], y_true[seen_t])[0])
                    p_ut = float(pearsonr(vec[unseen_t], y_true[unseen_t])[0])
                    p_sd = float(pearsonr(vec[seen_d], y_true[seen_d])[0])
                    p_ud = float(pearsonr(vec[unseen_d], y_true[unseen_d])[0])
                    if (
                        abs(p_all - float(s_info["pcc_all"])) > 1e-6
                        or abs(p_st - float(s_info["pcc_seen_target"])) > 1e-6
                        or abs(p_ut - float(s_info["pcc_unseen_target"])) > 1e-6
                        or abs(p_sd - float(s_info["pcc_seen_drug"])) > 1e-6
                        or abs(p_ud - float(s_info["pcc_unseen_drug"])) > 1e-6
                    ):
                        fail(f"Ground-truth rescoring mismatch on {tk} seed {s}")
                    for yr in (2019, 2020, 2021):
                        p_yr = float(pearsonr(vec[years == yr], y_true[years == yr])[0])
                        if abs(p_yr - float(s_info["pcc_by_year"][str(yr)])) > 1e-6:
                            fail(f"Ground-truth year {yr} rescoring mismatch on {tk} seed {s}")

            print(
                f"Ground-truth rescoring against official TDC test.csv ({N_TEST} rows) & train_val.csv (183,430 rows) verified."
            )

    # Confirm Partial Win p1 margin >= +0.010 over Rank #2 OrangeBalls-ProtBertMorgan (0.538)
    track_a_mean = float(cert["tracks"]["trackA_strict_train"]["mean_5seed_pcc"])
    margin_vs_rank2 = track_a_mean - 0.538
    if margin_vs_rank2 < 0.010:
        fail(f"Track A 5-seed mean PCC ({track_a_mean:.5f}) does not beat 0.538 by >= 0.010")

    print(
        f"Verified TDC DTI_DG BindingDB_Patent package (status=CONFIRMED_PARTIAL, partial_win=p1): "
        f"Claimed CPU-Only Track A = {track_a_mean:.5f} ± {cert['tracks']['trackA_strict_train']['std_5seed_pcc']:.5f} "
        f"(+{margin_vs_rank2:.5f} vs Rank #2 0.538; +0.06632 vs Reproduced ERM 0.51310)."
    )
    print("PASS")


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:
        fail(f"Unhandled exception: {exc}")
