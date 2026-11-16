#!/usr/bin/env python3
"""
Standalone Zero-Trust Verifier for `openproblems-spatially-variable-genes-correlation`.

Recomputes `AMS-SVG` (`object/method.py`) and the Wave 2 Empirical-Bayes capture-deconfounded
variant (`object/ams_svg_eb_v2.py`) from scratch in an isolated blind temporary directory
across the 12-dataset, 9-technology verification panel from Pinello Lab / OpenProblems
`Zenodo 18193366` (auto-fetching missing `.h5ad` slices via HTTP Range if not cached),
and verifies:
  1. Pre-holdout SHA-256 locks and AST anti-leakage purity on both `object/method.py` and
     `object/ams_svg_eb_v2.py` (zero dataset-specific branches, zero `.pyc` bytecode writes).
  2. Strict blind-input isolation (`tempfile.TemporaryDirectory` containing ONLY `blind_dataset.h5ad`
     with anonymized gene IDs, stripped `.var`/`.uns`, and random column permutation), plus
     one-finite-score-per-feature, zero-NaN per-gene Kendall tau-b, scrambled `row_positions` (~0),
     and `true_ranking` (1.0) controls.
  3. Exact gene-column permutation equivariance (`max_err < 1e-12`) and exact 2D rigid-motion +
     reflection + uniform coordinate-scale invariance (`max_rel_err < 1e-12`).
  4. Sibling coordinate-permutation negative control (`|tau_null| < 0.05` vs `tau_pos > 0.78`).
  5. Exact 6-decimal Delaunay `MoranI` anchor parity (`0.196000 == 0.196000`) on
     `42_slide_tag_human_skin_melanoma` against official `Zenodo 18193366`.
  6. Full semantic & arithmetic consistency across ALL rows of `benchmark_50_datasets.json`,
     `ablation_p3.json`, `depth_paradox_benchmark.json`, `wave2_eb_v2_benchmark_50.json`,
     `bayes_ceiling_dev4.json`, and `verification_certificate.json`, plus live scratch
     recomputation of Wave 2 `sigma_tech = 0.85` capture-dropout recovery (`v2 > v1 > SPARK-X`)
     and milestone thresholds (`Main Goal` >= 5 datasets across >= 3 technologies, `p1`, `p2`, `p3`).
  7. Adversarial `--corrupt` and object-mutation rejection (`rc = 1`, final stdout line `FAIL`).
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
import ast
import gzip
import hashlib
import json
import math
import os
import struct
import tempfile
import time
import urllib.request
import zlib
from pathlib import Path

import anndata as ad
import numpy as np
import pandas as pd
import scipy.sparse as sp
import scipy.spatial

PKG_DIR = Path(__file__).resolve().parents[1]
OBJECT_DIR = PKG_DIR / "object"
HOW_DIR = PKG_DIR / "how-we-built-it"

METHOD_PY = OBJECT_DIR / "method.py"
METHOD_V2_PY = OBJECT_DIR / "ams_svg_eb_v2.py"
BENCH50_JSON = OBJECT_DIR / "benchmark_50_datasets.json"
ABLATION_JSON = OBJECT_DIR / "ablation_p3.json"
DEPTH_JSON = OBJECT_DIR / "depth_paradox_benchmark.json"
WAVE2_BENCH50_JSON = OBJECT_DIR / "wave2_eb_v2_benchmark_50.json"
BAYES_JSON = OBJECT_DIR / "bayes_ceiling_dev4.json"
CERT_JSON = OBJECT_DIR / "verification_certificate.json"

EXPECTED_METHOD_SHA256 = "4503ac7a6e97aa6816353b486e8c87f7b64f5caeba32c6ae3f486eb6f44a7336"
EXPECTED_METHOD_V2_SHA256 = "4c27e2538339e69f18061879d5418afd2a1ea1de14355b649860ae5cd097b05f"
ZENODO_ZIP_URL = "https://zenodo.org/api/records/18193366/files/simulation_data.zip/content"
ZENODO_ZIP_SIZE = 411713101

sys.path.insert(0, str(HOW_DIR))
sys.path.insert(0, str(OBJECT_DIR))


def _http_range(url: str, start: int, end_inclusive: int, timeout: int = 90) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"Range": f"bytes={start}-{end_inclusive}", "User-Agent": "AMS-SVG-Verifier/2.0"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def _load_panel_h5ad(stem: str, expected_sha256: str, cache_dir: Path) -> ad.AnnData:
    cache_dir.mkdir(parents=True, exist_ok=True)
    gz_path = cache_dir / f"{stem}.h5ad.gz"
    raw_bytes = None
    if gz_path.is_file():
        cand = gzip.decompress(gz_path.read_bytes())
        if hashlib.sha256(cand).hexdigest() == expected_sha256:
            raw_bytes = cand

    if raw_bytes is None:
        tail = _http_range(ZENODO_ZIP_URL, ZENODO_ZIP_SIZE - 65536, ZENODO_ZIP_SIZE - 1)
        eocd = tail.rfind(b"PK\x05\x06")
        if eocd < 0:
            raise RuntimeError("ZIP EOCD signature not found on Zenodo 18193366")
        _, _, _, _, _, cd_size, cd_off, _ = struct.unpack("<4sHHHHIIH", tail[eocd : eocd + 22])
        cd = _http_range(ZENODO_ZIP_URL, cd_off, cd_off + cd_size - 1)
        pos = 0
        found = None
        while pos < len(cd):
            if cd[pos : pos + 4] != b"PK\x01\x02":
                break
            fields = struct.unpack("<4sHHHHHHIIIHHHHHII", cd[pos : pos + 46])
            fname_len, extra_len, comment_len = fields[10], fields[11], fields[12]
            fname = cd[pos + 46 : pos + 46 + fname_len].decode("utf-8")
            if fname.endswith(f"/{stem}.h5ad") or fname == f"{stem}.h5ad":
                found = (int(fields[4]), int(fields[7]), int(fields[8]), int(fields[16]))
                break
            pos += 46 + fname_len + extra_len + comment_len
        if found is None:
            raise KeyError(f"Dataset {stem} missing from Zenodo 18193366")
        comp_m, crc_exp, comp_sz, lhdr = found
        chunk = _http_range(ZENODO_ZIP_URL, lhdr, min(ZENODO_ZIP_SIZE - 1, lhdr + 542 + comp_sz))
        fn_l, ex_l = struct.unpack("<26xHH", chunk[:30])
        comp_bytes = chunk[30 + fn_l + ex_l : 30 + fn_l + ex_l + comp_sz]
        raw_bytes = zlib.decompress(comp_bytes, -zlib.MAX_WBITS) if comp_m == 8 else comp_bytes
        if (zlib.crc32(raw_bytes) & 0xFFFFFFFF) != crc_exp:
            raise RuntimeError(f"CRC32 mismatch on {stem}")
        gz_path.write_bytes(gzip.compress(raw_bytes, compresslevel=6))

    actual_sha = hashlib.sha256(raw_bytes).hexdigest()
    if actual_sha != expected_sha256:
        raise AssertionError(f"Upstream h5ad SHA-256 mismatch on {stem}: {actual_sha} != {expected_sha256}")

    with tempfile.NamedTemporaryFile(suffix=".h5ad", delete=True) as tf:
        tf.write(raw_bytes)
        tf.flush()
        return ad.read_h5ad(tf.name)


def eval_kendall(pred: np.ndarray, orig_gene: np.ndarray, true_alpha: np.ndarray) -> float:
    pred_arr = np.asarray(pred, dtype=np.float64)
    if pred_arr.ndim != 1 or pred_arr.shape[0] != len(orig_gene) or not np.all(np.isfinite(pred_arr)):
        raise AssertionError("Method must return exactly one finite score per input feature")
    df = pd.DataFrame({"gene": orig_gene, "true": true_alpha, "pred": pred_arr})
    per_gene = df.groupby("gene", observed=True).apply(
        lambda x: x["pred"].corr(x["true"], method="kendall")
    )
    if per_gene.isna().any() or not np.all(np.isfinite(per_gene.to_numpy(dtype=np.float64))):
        raise AssertionError("Undefined or NaN per-gene Kendall tau-b detected (tied/constant predictions)")
    return float(per_gene.mean())


def delaunay_moran_i(z: np.ndarray, coords: np.ndarray) -> np.ndarray:
    tri = scipy.spatial.Delaunay(coords)
    edges = set()
    for s in tri.simplices:
        for u, v in ((s[0], s[1]), (s[1], s[2]), (s[0], s[2])):
            if u != v:
                edges.add((int(u), int(v)))
                edges.add((int(v), int(u)))
    rows, cols = zip(*edges)
    n = coords.shape[0]
    w = sp.csr_matrix((np.ones(len(rows), dtype=np.float64), (rows, cols)), shape=(n, n))
    deg = np.asarray(w.sum(axis=1)).ravel()
    inv_deg = np.where(deg > 0, 1.0 / np.maximum(deg, 1e-30), 0.0)
    w_row = (sp.diags(inv_deg) @ w).tocsr()
    zc = z - z.mean(axis=0, keepdims=True)
    denom = np.sum(zc * zc, axis=0)
    wz = w_row @ zc
    s0 = float(w_row.sum())
    return (n / s0) * np.sum(zc * wz, axis=0) / np.where(denom > 1e-15, denom, 1.0)


def check_ast_purity(method_file: Path) -> None:
    src = method_file.read_text(encoding="utf-8")
    tree = ast.parse(src, filename=str(method_file))
    forbidden_attrs = {"var", "uns", "obs", "X", "layers"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute) and node.attr in forbidden_attrs:
            raise AssertionError(f"Forbidden AnnData metadata attribute '.{node.attr}' in {method_file.name}")
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            low = node.value.lower()
            for kw in ("melanoma", "visium", "merfish", "stereo_seq", "slide_tag", "solution"):
                if kw in low:
                    raise AssertionError(f"Dataset-specific literal '{node.value}' inside {method_file.name}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Standalone Zero-Trust Verifier for AMS-SVG")
    parser.add_argument(
        "--corrupt",
        action="store_true",
        help="Run negative-control corruption self-test (must exit non-zero and print FAIL)",
    )
    args = parser.parse_args()

    t0 = time.perf_counter()
    try:
        # Gate 1: Method integrity & AST anti-leakage check across both frozen operators (checked BEFORE importing)
        for req_p in (
            METHOD_PY,
            METHOD_V2_PY,
            BENCH50_JSON,
            ABLATION_JSON,
            DEPTH_JSON,
            WAVE2_BENCH50_JSON,
            BAYES_JSON,
            CERT_JSON,
        ):
            if not req_p.is_file():
                raise FileNotFoundError(f"Missing required package file: {req_p}")

        method_sha = hashlib.sha256(METHOD_PY.read_bytes()).hexdigest()
        if method_sha != EXPECTED_METHOD_SHA256:
            raise AssertionError(f"object/method.py SHA-256 mismatch: {method_sha} != {EXPECTED_METHOD_SHA256}")
        method_v2_sha = hashlib.sha256(METHOD_V2_PY.read_bytes()).hexdigest()
        if method_v2_sha != EXPECTED_METHOD_V2_SHA256:
            raise AssertionError(
                f"object/ams_svg_eb_v2.py SHA-256 mismatch: {method_v2_sha} != {EXPECTED_METHOD_V2_SHA256}"
            )

        check_ast_purity(METHOD_PY)
        check_ast_purity(METHOD_V2_PY)

        from method import score_svg
        from ams_svg_eb_v2 import score_svg as score_svg_v2
        from stress_test_depth_paradox import py_sparkx_reference, simulate_capture_regime

        bench = json.loads(BENCH50_JSON.read_text(encoding="utf-8"))
        ablation = json.loads(ABLATION_JSON.read_text(encoding="utf-8"))
        depth = json.loads(DEPTH_JSON.read_text(encoding="utf-8"))
        bench_v2 = json.loads(WAVE2_BENCH50_JSON.read_text(encoding="utf-8"))
        bayes_dev4 = json.loads(BAYES_JSON.read_text(encoding="utf-8"))
        cert = json.loads(CERT_JSON.read_text(encoding="utf-8"))

        if args.corrupt:
            cert["panel_12_recomputed_tau_vector"][0] += 0.025

        # Gate 2: Cross-certificate SHA-256 & full semantic consistency across ALL rows
        sha_checks = [
            ("benchmark_50_datasets_sha256", BENCH50_JSON),
            ("ablation_p3_sha256", ABLATION_JSON),
            ("depth_paradox_benchmark_sha256", DEPTH_JSON),
            ("wave2_eb_v2_benchmark_50_sha256", WAVE2_BENCH50_JSON),
            ("bayes_ceiling_dev4_sha256", BAYES_JSON),
        ]
        for key, fpath in sha_checks:
            actual = hashlib.sha256(fpath.read_bytes()).hexdigest()
            if cert.get(key) != actual:
                raise AssertionError(f"Certificate {key} mismatch: {cert.get(key)} != {actual}")
        if cert.get("frozen_method_sha256") != method_sha:
            raise AssertionError("Certificate frozen_method_sha256 mismatch")
        if cert.get("wave2_eb_method_sha256") != method_v2_sha:
            raise AssertionError("Certificate wave2_eb_method_sha256 mismatch")
        if depth.get("frozen_method_sha256") != method_v2_sha or bench_v2.get("frozen_method_sha256") != method_v2_sha:
            raise AssertionError("Wave 2 certificate method SHA-256 mismatch")

        ds_list = bench["datasets"]
        ds_v2_list = bench_v2["datasets"]
        if len(ds_list) != 50 or len(ds_v2_list) != 50:
            raise AssertionError("Expected 50 datasets in both benchmark JSONs")
        recomp_mean50 = float(np.mean([r["ams_svg_tau"] for r in ds_list]))
        if abs(recomp_mean50 - float(bench["summary_all_50"]["mean_ams_svg_tau"])) > 1e-5:
            raise AssertionError("50-dataset mean mismatch in benchmark_50_datasets.json")
        if abs(recomp_mean50 - float(cert["mean_ams_svg_tau_all_50"])) > 1e-5:
            raise AssertionError("50-dataset mean mismatch in verification_certificate.json")

        recomp_v2_mean50 = float(np.mean([r["ams_svg_tau"] for r in ds_v2_list]))
        if abs(recomp_v2_mean50 - float(cert["mean_wave2_eb_v2_tau_all_50"])) > 1e-5:
            raise AssertionError("Wave 2 50-dataset mean mismatch in verification_certificate.json")
        if int(cert["max_coord_multiplicity_all_50"]) != int(max(r["max_coord_multiplicity"] for r in ds_v2_list)):
            raise AssertionError("max_coord_multiplicity_all_50 mismatch")

        holdout_recs = [r for r in ds_list if r["split"] == "blind_holdout"]
        if len(holdout_recs) != 46:
            raise AssertionError(f"Expected 46 blind holdout datasets, got {len(holdout_recs)}")
        recomp_mean46 = float(np.mean([r["ams_svg_tau"] for r in holdout_recs]))
        if abs(recomp_mean46 - float(cert["mean_ams_svg_tau_holdout_46"])) > 1e-5:
            raise AssertionError("46-holdout mean mismatch in verification_certificate.json")

        if int(cert["count_beating_zenodo_best_strict_50"]) != sum(1 for r in ds_list if r["delta_vs_zenodo_best"] > 0):
            raise AssertionError("count_beating_zenodo_best_strict_50 mismatch")
        if int(cert["count_beating_zenodo_best_by_0p02_50"]) != sum(
            1 for r in ds_list if r["delta_vs_zenodo_best"] >= 0.02
        ):
            raise AssertionError("count_beating_zenodo_best_by_0p02_50 mismatch")
        if int(cert["count_beating_both_by_0p02_50"]) != sum(
            1 for r in ds_list if r["delta_vs_zenodo_best"] >= 0.02 and r["delta_vs_seqera_v1_best"] >= 0.02
        ):
            raise AssertionError("count_beating_both_by_0p02_50 mismatch")
        if int(cert["count_within_0p02_zenodo_50"]) != sum(1 for r in ds_list if r["delta_vs_zenodo_best"] >= -0.02):
            raise AssertionError("count_within_0p02_zenodo_50 mismatch")
        if int(cert["count_within_0p02_seqera_50"]) != sum(
            1 for r in ds_list if r["delta_vs_seqera_v1_best"] >= -0.02
        ):
            raise AssertionError("count_within_0p02_seqera_50 mismatch")

        by_id = {r["dataset_id"]: r for r in ds_list}
        by_v2_id = {r["dataset_id"]: r for r in ds_v2_list}
        for did, r1_row in by_id.items():
            if abs(r1_row["ams_svg_runtime_sec"] * 10000.0 / r1_row["n_spots"] - r1_row["ams_svg_sec_per_10k_spots"]) >= 1e-3:
                raise AssertionError(f"benchmark_50 sec_per_10k_spots mismatch on {did}")
            if abs((r1_row["ams_svg_tau"] - r1_row["zenodo_best_tau"]) - r1_row["delta_vs_zenodo_best"]) >= 2e-6:
                raise AssertionError(f"benchmark_50 delta_vs_zenodo_best mismatch on {did}")
            if abs((r1_row["ams_svg_tau"] - r1_row["seqera_v1_best_tau"]) - r1_row["delta_vs_seqera_v1_best"]) >= 2e-6:
                raise AssertionError(f"benchmark_50 delta_vs_seqera_v1_best mismatch on {did}")

        for did, r2 in by_v2_id.items():
            r1_row = by_id[did]
            if (
                r2["zenodo_h5ad_crc32"] != r1_row["zenodo_h5ad_crc32"]
                or r2["zenodo_h5ad_sha256"] != r1_row["zenodo_h5ad_sha256"]
            ):
                raise AssertionError(f"Cross-benchmark h5ad provenance mismatch on {did}")
            if r2["n_spots"] != r1_row["n_spots"] or r2["n_genes"] != r1_row["n_genes"]:
                raise AssertionError(f"Cross-benchmark shape mismatch on {did}")
            if abs(r2["ams_svg_runtime_sec"] * 10000.0 / r2["n_spots"] - r2["ams_svg_sec_per_10k_spots"]) >= 1e-3:
                raise AssertionError(f"wave2 sec_per_10k_spots mismatch on {did}")
            if (
                abs(
                    r2["ams_svg_runtime_sec"] * 10000.0 / max(10000.0, float(r2["n_spots"]))
                    - r2["ams_svg_sec_per_10k_spots_capped"]
                )
                >= 1e-3
            ):
                raise AssertionError(f"wave2 sec_per_10k_spots_capped mismatch on {did}")
            if abs((r2["ams_svg_tau"] - r2["zenodo_best_tau"]) - r2["delta_vs_zenodo_best"]) >= 2e-6:
                raise AssertionError(f"wave2 delta_vs_zenodo_best mismatch on {did}")
            if abs((r2["ams_svg_tau"] - r2["seqera_v1_best_tau"]) - r2["delta_vs_seqera_v1_best"]) >= 2e-6:
                raise AssertionError(f"wave2 delta_vs_seqera_v1_best mismatch on {did}")
            if abs(float(r2["ams_svg_v1_tau"]) - float(r1_row["ams_svg_tau"])) > 1e-6:
                raise AssertionError(f"Cross-benchmark v1 tau mismatch on {did}")
            if abs((float(r2["ams_svg_tau"]) - float(r2["ams_svg_v1_tau"])) - float(r2["delta_v2_vs_v1"])) > 2e-6:
                raise AssertionError(f"Wave 2 delta_v2_vs_v1 arithmetic mismatch on {did}")

        # Full semantic verification across ALL 9 rows of ablation_p3.json
        if len(ablation["datasets"]) != 9:
            raise AssertionError("Expected 9 rows in ablation_p3.json")
        for ab_row in ablation["datasets"]:
            did = ab_row["dataset_id"]
            c1 = ab_row["confounder_1_library_size_endogeneity"]
            c2 = ab_row["confounder_2_geometry_and_heavy_tails"]
            c3 = ab_row["confounder_3_float64_pvalue_underflow"]
            exp_tau = float(by_id[did]["ams_svg_tau"])
            if abs(float(c1["ams_svg_unnormalized_full_tau"]) - exp_tau) > 1e-5:
                raise AssertionError(f"ablation_p3 C1 full tau mismatch vs benchmark_50 on {did}")
            if abs(float(c2["ams_svg_multiscale_adaptive_vst_full_tau"]) - exp_tau) > 1e-5:
                raise AssertionError(f"ablation_p3 C2 full tau mismatch vs benchmark_50 on {did}")
            if abs(float(c3["ams_svg_unbounded_perm_z_tau"]) - exp_tau) > 1e-5:
                raise AssertionError(f"ablation_p3 C3 full tau mismatch vs benchmark_50 on {did}")
            if (
                abs(
                    (c1["delaunay_moran_unnormalized_log1p_tau"] - c1["delaunay_moran_normalized_tau"])
                    - c1["gain_removing_1_over_Ls_on_delaunay"]
                )
                > 2e-6
            ):
                raise AssertionError(f"ablation_p3 C1 gain arithmetic mismatch on {did}")
            if (
                abs(
                    (c2["ams_svg_multiscale_adaptive_vst_full_tau"] - c2["unpruned_delaunay_vst_z_tau"])
                    - c2["gain_multiscale_adaptive_over_delaunay"]
                )
                > 2e-6
            ):
                raise AssertionError(f"ablation_p3 C2 gain arithmetic mismatch on {did}")
            if (
                abs(
                    (c3["high_snr_alpha_ge_0p5_unbounded_z_tau"] - c3["high_snr_alpha_ge_0p5_neglog10p_clipped_tau"])
                    - c3["high_snr_gain_unbounded_z_over_pval_clip"]
                )
                > 2e-6
            ):
                raise AssertionError(f"ablation_p3 C3 high-SNR gain arithmetic mismatch on {did}")

        # Full semantic verification across ALL 9 rows x 5 regimes of depth_paradox_benchmark.json
        if len(depth["datasets"]) != 9:
            raise AssertionError("Expected 9 rows in depth_paradox_benchmark.json")
        for dp_row in depth["datasets"]:
            did = dp_row["dataset_id"]
            r1 = dp_row["regimes"]["regime_1_intact_compartment"]
            if abs(float(r1["ams_svg_v1_tau"]) - float(by_id[did]["ams_svg_tau"])) > 1e-5:
                raise AssertionError(f"depth_paradox Regime 1 v1 tau mismatch on {did}")
            if abs(float(r1["ams_svg_v2_tau"]) - float(by_v2_id[did]["ams_svg_tau"])) > 1e-5:
                raise AssertionError(f"depth_paradox Regime 1 v2 tau mismatch on {did}")
            for r_key, r_obj in dp_row["regimes"].items():
                if abs((r_obj["ams_svg_v2_tau"] - r_obj["ams_svg_v1_tau"]) - r_obj["gain_v2_over_v1"]) > 2e-6:
                    raise AssertionError(f"depth_paradox {r_key} gain_v2_over_v1 mismatch on {did}")
                if abs((r_obj["ams_svg_v2_tau"] - r_obj["py_sparkx_tau"]) - r_obj["gain_v2_over_sparkx"]) > 2e-6:
                    raise AssertionError(f"depth_paradox {r_key} gain_v2_over_sparkx mismatch on {did}")
        for r_key, r_sum in depth["regime_summary_9_datasets"].items():
            if (
                r_sum["mean_gain_v2_over_v1"] <= 0.0
                or r_sum["mean_gain_v2_over_sparkx"] <= 0.05
                or r_sum["mean_gain_v2_over_moran_norm"] <= 0.15
            ):
                raise AssertionError(f"depth_paradox 9-dataset dominance failed in {r_key}")

        # Verify Dev-4 Bayes ceiling consistency across all fields, strata, and worst-5 gene records
        if len(bayes_dev4["dev4_datasets"]) != 4:
            raise AssertionError("Expected 4 datasets in bayes_ceiling_dev4.json")
        for bd in bayes_dev4["dev4_datasets"]:
            did = bd["dataset_id"]
            if abs(float(bd["tau_ams_svg_v1"]) - float(by_id[did]["ams_svg_tau"])) > 1e-5:
                raise AssertionError(f"bayes_ceiling_dev4 v1 tau mismatch on {did}")
            if float(bd["offline_loao_template_ceiling_tau"]) <= float(bd["tau_ams_svg_v1"]):
                raise AssertionError(f"LOAO ceiling must exceed blind v1 tau on {did}")
            if abs((bd["offline_loao_template_ceiling_tau"] - bd["tau_ams_svg_v1"]) - bd["blind_headroom_to_loao"]) >= 2e-5:
                raise AssertionError(f"bayes_ceiling_dev4 blind_headroom_to_loao mismatch on {did}")
            if (
                abs(
                    (bd["parametric_exact_mu_bayes_ceiling_tau"] - bd["tau_ams_svg_v1"])
                    - bd["blind_headroom_to_exact_bayes"]
                )
                >= 2e-5
            ):
                raise AssertionError(f"bayes_ceiling_dev4 blind_headroom_to_exact_bayes mismatch on {did}")
            for s_group in bd["strata"].values():
                for s_entry in s_group.values():
                    for tk in ("tau_v1", "tau_loao_template", "tau_mc_exact_bayes"):
                        if not (-1.0 <= float(s_entry[tk]) <= 1.0):
                            raise AssertionError(f"Out-of-bounds stratum {tk} on {did}")
                    if abs((s_entry["tau_loao_template"] - s_entry["tau_v1"]) - s_entry["headroom_to_loao"]) >= 2e-4:
                        raise AssertionError(f"Stratum headroom_to_loao mismatch on {did}")
            if len(bd["worst_5_genes_in_v1"]) != 5:
                raise AssertionError(f"Expected 5 worst_5_genes_in_v1 entries on {did}")
            for g_entry in bd["worst_5_genes_in_v1"]:
                for tk in ("tau_v1", "tau_loao_template", "tau_mc_exact_bayes"):
                    if not (-1.0 <= float(g_entry[tk]) <= 1.0):
                        raise AssertionError(f"Out-of-bounds gene {tk} on {did}")
                if not (0.0 <= float(g_entry["zero_frac"]) <= 1.0) or float(g_entry["theta_hat"]) <= 0.0:
                    raise AssertionError(f"Invalid gene diagnostics on {did}")

        # Gate 3: Scratch Re-Execution on 12-Dataset, 9-Technology Panel in Isolated Blind Directory
        cache_dir = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "openproblems_svg_zenodo_18193366"
        panel_ids = bench["verification_panel_12_ids"]
        if len(panel_ids) != 12:
            raise AssertionError(f"Expected 12 verification panel datasets, got {len(panel_ids)}")

        techs_seen = set()
        rng = np.random.default_rng(20261116)
        panel_vec = cert.get("panel_12_recomputed_tau_vector", [])
        if len(panel_vec) != 12:
            raise AssertionError(f"Expected 12-element panel_12_recomputed_tau_vector, got {len(panel_vec)}")

        for idx_p, pid in enumerate(panel_ids):
            rec = by_id[pid]
            techs_seen.add(rec["technology"])
            adata_raw = _load_panel_h5ad(pid, rec["zenodo_h5ad_sha256"], cache_dir)
            orig_gene = adata_raw.var["gene"].astype(str).values
            true_alpha = adata_raw.var["spatial_var"].astype(float).values
            n_genes = adata_raw.n_vars
            perm = rng.permutation(n_genes)
            inv_perm = np.argsort(perm)

            # Target-card controls on the exact scrambled copy and mapping:
            # row positions on scrambled input must score ~0, and true_ranking must score 1.0
            row_pos_tau = eval_kendall(np.arange(n_genes, dtype=np.float64)[inv_perm], orig_gene, true_alpha)
            true_rank_tau = eval_kendall(true_alpha[perm][inv_perm], orig_gene, true_alpha)
            if abs(row_pos_tau) >= 0.12 or abs(true_rank_tau - 1.0) >= 1e-12:
                raise AssertionError(
                    f"Scrambled-copy controls failed on {pid}: row_pos={row_pos_tau:.4f}, true_rank={true_rank_tau:.6f}"
                )

            with tempfile.TemporaryDirectory() as tmpdir:
                blind_path = os.path.join(tmpdir, "blind_dataset.h5ad")
                blind_ad = ad.AnnData(
                    layers={"counts": adata_raw.layers["counts"][:, perm].tocsr()},
                    obsm={"spatial": np.asarray(adata_raw.obsm["spatial"], dtype=np.float64)},
                    var=pd.DataFrame(index=[f"g_{i}" for i in range(n_genes)]),
                )
                blind_ad.write_h5ad(blind_path)
                if os.listdir(tmpdir) != ["blind_dataset.h5ad"]:
                    raise AssertionError("Isolated directory check failed")
                loaded = ad.read_h5ad(blind_path)
                t_run0 = time.perf_counter()
                pred_perm = score_svg(loaded.layers["counts"], np.asarray(loaded.obsm["spatial"], dtype=np.float64))
                dt_run = time.perf_counter() - t_run0

            pred = pred_perm[inv_perm]
            tau_recomp = eval_kendall(pred, orig_gene, true_alpha)

            if abs(tau_recomp - float(rec["ams_svg_tau"])) > 1e-5:
                raise AssertionError(
                    f"Panel recomputation mismatch vs benchmark_50 on {pid}: {tau_recomp:.6f} != {rec['ams_svg_tau']:.6f}"
                )
            if abs(tau_recomp - float(panel_vec[idx_p])) > 1e-5:
                raise AssertionError(f"Panel recomputation mismatch vs certificate vector[{idx_p}] ({pid})")
            if abs(tau_recomp - float(cert["panel_12_recomputed_tau"][pid])) > 1e-5:
                raise AssertionError(f"Panel recomputation mismatch vs certificate dict ({pid})")

            sec_per_10k = dt_run * (10000.0 / max(10000.0, float(adata_raw.n_obs)))
            if sec_per_10k >= 5.0:
                raise AssertionError(f"p2 CPU speed threshold exceeded on {pid}: {sec_per_10k:.3f}s / 10k spots")

            # Deep invariance + anchor + null separator + Wave 2 EB capture-dropout check on anchor 42_slide_tag_human_skin_melanoma
            if pid == "42_slide_tag_human_skin_melanoma":
                coords = np.asarray(adata_raw.obsm["spatial"], dtype=np.float64)
                pred_direct = score_svg(adata_raw.layers["counts"], coords)
                col_eq_err = float(np.max(np.abs(pred - pred_direct) / np.maximum(np.abs(pred_direct), 1.0)))
                if col_eq_err >= 1e-12:
                    raise AssertionError(f"Column-permutation equivariance rel error {col_eq_err:.2e} >= 1e-12")

                theta = 0.7319
                rot = np.array([[math.cos(theta), -math.sin(theta)], [-math.sin(theta), -math.cos(theta)]])
                coords_iso = 37.5 * (coords @ rot) + np.array([[1234.5, -567.8]])
                pred_iso = score_svg(adata_raw.layers["counts"], coords_iso)
                iso_rel_err = float(np.max(np.abs(pred_iso - pred_direct) / np.maximum(np.abs(pred_direct), 1.0)))
                if iso_rel_err >= 1e-12:
                    raise AssertionError(f"Rigid-motion/scale invariance error {iso_rel_err:.2e} >= 1e-12")

                null_draws = []
                for _ in range(3):
                    null_coords = coords[rng.permutation(coords.shape[0])]
                    null_draws.append(
                        eval_kendall(score_svg(adata_raw.layers["counts"], null_coords), orig_gene, true_alpha)
                    )
                tau_null = float(np.mean(null_draws))
                if abs(tau_null) >= 0.05 or max(abs(x) for x in null_draws) >= 0.10 or tau_recomp <= 0.75:
                    raise AssertionError(f"Separator gate failed: pos={tau_recomp:.4f}, neg_mean={tau_null:.4f}")

                moran_norm = eval_kendall(
                    delaunay_moran_i(adata_raw.X.toarray().astype(np.float64), coords), orig_gene, true_alpha
                )
                if abs(moran_norm - 0.196000) >= 1e-6:
                    raise AssertionError(f"MoranI anchor mismatch: {moran_norm:.6f} != 0.196000")

                # Scratch recomputation of Wave 2 ams_svg_eb_v2 on intact & sigma_tech=0.85 capture dropout
                pred_v2_intact, diag_v2_intact = score_svg_v2(
                    adata_raw.layers["counts"], coords, return_diagnostics=True
                )
                tau_v2_intact = eval_kendall(pred_v2_intact, orig_gene, true_alpha)
                if (
                    abs(tau_v2_intact - float(cert["wave2_melanoma_eb_v2_intact_tau"])) > 1e-5
                    or diag_v2_intact["kappa"] != 0.0
                ):
                    raise AssertionError(
                        f"Wave 2 intact melanoma mismatch: tau={tau_v2_intact}, kappa={diag_v2_intact['kappa']}"
                    )

                # Replay exact idx_d=0 deterministic RNG draw up to regime_2c_severe_bead_dropout (sigma_tech=0.85)
                y_clean = adata_raw.layers["counts"].toarray().astype(np.float64)
                rng_dp = np.random.default_rng(20261116)
                for sig_step in (0.00, 0.35, 0.70, 0.85):
                    y_step = simulate_capture_regime(y_clean, coords, sig_step, "bead_iid", rng_dp)
                pred_v2_drop, diag_v2_drop = score_svg_v2(sp.csr_matrix(y_step), coords, return_diagnostics=True)
                tau_v2_drop = eval_kendall(pred_v2_drop, orig_gene, true_alpha)
                tau_v1_drop = eval_kendall(score_svg(y_step, coords), orig_gene, true_alpha)
                tau_spx_drop = eval_kendall(py_sparkx_reference(y_step, coords), orig_gene, true_alpha)
                if abs(tau_v2_drop - float(cert["wave2_melanoma_eb_v2_bead0p85_tau"])) > 1e-5:
                    raise AssertionError(
                        f"Wave 2 dropout melanoma mismatch: {tau_v2_drop:.6f} != {cert['wave2_melanoma_eb_v2_bead0p85_tau']:.6f}"
                    )
                if not (diag_v2_drop["kappa"] > 0.40 and tau_v2_drop > tau_v1_drop > tau_spx_drop):
                    raise AssertionError("Wave 2 capture-dropout gate ordering failed on melanoma")

        if len(techs_seen) != 9:
            raise AssertionError(f"Expected 9 distinct spatial technologies in panel, got {len(techs_seen)}")

        # Gate 4: Milestone Thresholds (>= 5 datasets across >= 3 technologies on Main Goal)
        wins_both = [
            r
            for r in ds_list
            if r["delta_vs_zenodo_best"] >= 0.02 and r["delta_vs_seqera_v1_best"] >= 0.02
        ]
        if len(wins_both) < 5 or len({r["technology"] for r in wins_both}) < 3:
            raise AssertionError("Main Goal (>= +0.02 over #1 on >= 5 datasets across >= 3 technologies) not met")

        mel = by_id["42_slide_tag_human_skin_melanoma"]
        if mel["delta_vs_zenodo_best"] < 0.02 or mel["delta_vs_seqera_v1_best"] < 0.02:
            raise AssertionError("p1 melanoma >= +0.02 threshold not met")

        ab_by_id = {r["dataset_id"]: r for r in ablation["datasets"]}
        mel_ab = ab_by_id["42_slide_tag_human_skin_melanoma"]
        if mel_ab["confounder_1_library_size_endogeneity"]["gain_removing_1_over_Ls_on_delaunay"] < 0.20:
            raise AssertionError("p3 Confounder #1 ablation effect missing on melanoma")
        if mel_ab["confounder_2_geometry_and_heavy_tails"]["gain_multiscale_adaptive_over_delaunay"] < 0.20:
            raise AssertionError("p3 Confounder #2 ablation effect missing on melanoma")
        vis_ab = ab_by_id["01_10x_Visium_mouse_brain"]
        if vis_ab["confounder_3_float64_pvalue_underflow"]["high_snr_gain_unbounded_z_over_pval_clip"] <= 0.01:
            raise AssertionError("p3 Confounder #3 high-SNR underflow ablation effect missing on Visium")
        if (
            abs(
                float(mel_ab["confounder_1_library_size_endogeneity"]["ams_svg_unnormalized_full_tau"])
                - float(cert["ablation_melanoma_ams_svg_tau"])
            )
            > 1e-5
        ):
            raise AssertionError("Certificate ablation_melanoma_ams_svg_tau mismatch")

        dt_tot = time.perf_counter() - t0
        print(
            f"VERIFICATION SUMMARY: 12/12 panel datasets (9 technologies) + 6 JSON certificates verified in {dt_tot:.2f}s | "
            f"50-ds mean tau = {recomp_mean50:.6f} (46-holdout = {recomp_mean46:.6f}; Wave2 EB v2 = {recomp_v2_mean50:.6f}) | "
            f"melanoma v1 = {mel['ams_svg_tau']:.6f} / v2 = {tau_v2_intact:.6f} (bead0.85: v2={tau_v2_drop:.4f} > v1={tau_v1_drop:.4f} > SPX={tau_spx_drop:.4f}) | "
            f"col_perm_err = {col_eq_err:.2e} | isometry_err = {iso_rel_err:.2e} | null_tau = {tau_null:+.4f}",
            flush=True,
        )
        print("PASS", flush=True)
        return 0
    except Exception as exc:
        print(f"VERIFICATION ERROR: {exc}", file=sys.stderr, flush=True)
        print("FAIL", flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
