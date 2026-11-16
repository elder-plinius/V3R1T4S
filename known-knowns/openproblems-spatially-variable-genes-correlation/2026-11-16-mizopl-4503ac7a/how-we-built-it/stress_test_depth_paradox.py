#!/opt/homebrew/bin/python3
"""
Dual-Regime Spatial Transcriptomics Depth-Paradox Stress Benchmark
(`code/stress_test_depth_paradox.py` -> `results/depth_paradox_benchmark.json`).

Evaluates the normalization paradox of spatial transcriptomics across the
9-dataset multi-technology ablation panel (`slide-tags`, `Stereo-seq`, `MERFISH`,
`Slide-seqV2`, `10x Xenium`, `10x Visium`):
  - Camp A (`Global 1/L_s Normalized`): `Delaunay Moran's I (normalized)` and `AMS + Global 1/L_s`
  - Camp B (`Unnormalized Counts`): `Py-SPARK-X` and `AMS-SVG v1` (`object/method.py`)
  - Wave 2 (`Scale-Separated EB + Geodesic Quadrature`): `AMS-SVG v2` (`object/ams_svg_eb_v2.py`)
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import os
import struct
import sys
import tempfile
import time
import urllib.request
import zlib
from pathlib import Path

sys.dont_write_bytecode = True

import anndata as ad
import numpy as np
import pandas as pd
import scipy.sparse as sp
import scipy.spatial
import scipy.stats

SCRIPT_DIR = Path(__file__).resolve().parent
PKG_DIR = SCRIPT_DIR.parent
OBJECT_DIR = PKG_DIR / "object"
DEFAULT_OUT = OBJECT_DIR / "depth_paradox_benchmark.json"

sys.path.insert(0, str(OBJECT_DIR))
from ams_svg_eb_v2 import (  # noqa: E402
    _normalize_gene_columns,
    _spatial_morton_order,
    build_mercer_gaussian_lowrank_operator,
    build_self_tuning_biweight_knn_operator,
    cliff_ord_permutation_z,
    score_svg as score_svg_v2,
)

ZENODO_ZIP_URL = "https://zenodo.org/api/records/18193366/files/simulation_data.zip/content"
ZENODO_ZIP_SIZE = 411713101

STRESS_PANEL = [
    ("42_slide_tag_human_skin_melanoma", "slide-tags"),
    ("41_slide_tag_human_cortex", "slide-tags"),
    ("44_stereo_seq_Drosophila_embryo_E7", "Stereo-seq"),
    ("47_stereo_seq_Drosophila_embryo_E10.5", "Stereo-seq"),
    ("34_MERFISH_Human_cortex", "MERFISH"),
    ("21_slide_seqv2_Mouse_Olfactory_Bulb", "Slide-seqV2"),
    ("32_10x_Xenium_Human_Colon_Cancer", "10x Xenium"),
    ("04_10x_Visium_Human_Heart", "10x Visium"),
    ("01_10x_Visium_mouse_brain", "10x Visium"),
]


def _http_range(url: str, start: int, end_inclusive: int, timeout: int = 90) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"Range": f"bytes={start}-{end_inclusive}", "User-Agent": "AMS-SVG-Verifier/2.0"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def _load_or_fetch_panel_h5ad(stem: str, cache_dir: Path) -> tuple[ad.AnnData, str]:
    cache_dir.mkdir(parents=True, exist_ok=True)
    gz_path = cache_dir / f"{stem}.h5ad.gz"
    if gz_path.is_file():
        raw_bytes = gzip.decompress(gz_path.read_bytes())
    else:
        tail = _http_range(ZENODO_ZIP_URL, ZENODO_ZIP_SIZE - 65536, ZENODO_ZIP_SIZE - 1)
        eocd = tail.rfind(b"PK\x05\x06")
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
            raise KeyError(f"Dataset {stem} not found in Zenodo 18193366 archive")
        comp_m, crc_exp, comp_sz, lhdr = found
        chunk = _http_range(ZENODO_ZIP_URL, lhdr, min(ZENODO_ZIP_SIZE - 1, lhdr + 542 + comp_sz))
        fn_l, ex_l = struct.unpack("<26xHH", chunk[:30])
        comp_bytes = chunk[30 + fn_l + ex_l : 30 + fn_l + ex_l + comp_sz]
        raw_bytes = zlib.decompress(comp_bytes, -zlib.MAX_WBITS) if comp_m == 8 else comp_bytes
        assert (zlib.crc32(raw_bytes) & 0xFFFFFFFF) == crc_exp
        gz_path.write_bytes(gzip.compress(raw_bytes, compresslevel=6))

    sha = hashlib.sha256(raw_bytes).hexdigest()
    with tempfile.NamedTemporaryFile(suffix=".h5ad", delete=True) as tf:
        tf.write(raw_bytes)
        tf.flush()
        adata = ad.read_h5ad(tf.name)
    return adata, sha


def eval_kendall(pred: np.ndarray, orig_gene: np.ndarray, true_alpha: np.ndarray) -> float:
    df = pd.DataFrame({"gene": orig_gene, "true": true_alpha, "pred": pred})
    corrs = df.groupby("gene", observed=True).apply(
        lambda x: x["pred"].corr(x["true"], method="kendall")
    )
    return float(corrs.fillna(0.0).mean())


def eval_svg_vs_null_auroc(pred: np.ndarray, true_alpha: np.ndarray) -> float:
    pos = pred[true_alpha >= 0.5]
    neg = pred[true_alpha == 0.0]
    if pos.size == 0 or neg.size == 0:
        return 0.5
    ranks = scipy.stats.rankdata(np.concatenate([neg, pos]), method="average")
    pos_rank_sum = float(np.sum(ranks[neg.size :]))
    u_stat = pos_rank_sum - pos.size * (pos.size + 1.0) / 2.0
    return float(u_stat / (pos.size * neg.size))


def score_svg_v1_reference(y: np.ndarray, coords: np.ndarray) -> np.ndarray:
    coords_f = np.asarray(coords, dtype=np.float64)
    n = int(coords_f.shape[0])
    if n >= 8192 and coords_f.shape[1] >= 2:
        ord_s = _spatial_morton_order(coords_f)
        coords_f = np.ascontiguousarray(coords_f[ord_s])
        y = np.ascontiguousarray(y[ord_s])

    k_scales = sorted({
        min(24, max(8, n // 15)),
        min(120, max(28, int(round(0.025 * n)))),
        min(320, max(64, int(round(0.075 * n)))),
    })
    ops = [build_self_tuning_biweight_knn_operator(coords_f, k) for k in k_scales]
    for beta in (0.14, 0.26, 0.50):
        ops.append(build_mercer_gaussian_lowrank_operator(coords_f, beta=beta))

    tr_log = _normalize_gene_columns(np.log1p(y))
    tr_ft = _normalize_gene_columns(np.sqrt(y) + np.sqrt(y + 1.0) - 1.0)
    acc = np.zeros(y.shape[1], dtype=np.float64)
    for tr in (tr_log, tr_ft):
        for op in ops:
            acc += cliff_ord_permutation_z(*tr, op)
    return acc / float(2 * len(ops))


def delaunay_moran_i_normalized(x_norm: np.ndarray, coords: np.ndarray) -> np.ndarray:
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
    w_row = sp.diags(inv_deg) @ w
    zc = x_norm - x_norm.mean(axis=0, keepdims=True)
    denom = np.sum(zc * zc, axis=0)
    wz = w_row @ zc
    s0 = float(w_row.sum())
    return (n / s0) * np.sum(zc * wz, axis=0) / np.where(denom > 1e-15, denom, 1.0)


def py_sparkx_reference(y: np.ndarray, coords: np.ndarray) -> np.ndarray:
    n = y.shape[0]
    yc = y - y.mean(axis=0, keepdims=True)
    ss = np.sum(yc * yc, axis=0)
    valid = ss > 1e-15
    y_hat = np.zeros_like(yc)
    y_hat[:, valid] = yc[:, valid] / np.sqrt(ss[valid])[None, :]

    c = coords - coords.mean(axis=0, keepdims=True)
    sd = np.where(np.std(c, axis=0, keepdims=True) > 0, np.std(c, axis=0, keepdims=True), 1.0)
    cs = c / sd
    basis_list = [cs]
    q_scales = np.maximum(np.quantile(np.abs(cs), [0.2, 0.4, 0.6, 0.8, 1.0]), 0.1)
    for w in q_scales:
        basis_list.append(np.exp(-(cs * cs) / (2.0 * w * w)))
        basis_list.append(np.hstack([np.cos(np.pi * cs / w), np.sin(np.pi * cs / w)]))

    p_mat = []
    for xb in basis_list:
        xbc = xb - xb.mean(axis=0, keepdims=True)
        uq, sq_v, _ = np.linalg.svd(xbc, full_matrices=False)
        qo = uq[:, sq_v > 1e-8 * sq_v[0]]
        stat = n * np.sum((qo.T @ y_hat) ** 2, axis=0)
        pv = np.clip(scipy.stats.chi2.sf(stat, df=int(qo.shape[1])), 1e-300, 1.0)
        p_mat.append(pv)
    p_arr = np.vstack(p_mat)
    t_cauchy = np.mean(np.tan((0.5 - np.clip(p_arr, 1e-15, 1.0 - 1e-15)) * math.pi), axis=0)
    p_comb = np.clip(0.5 - np.arctan(t_cauchy) / math.pi, 1e-300, 1.0)
    min_p = np.min(p_arr, axis=0)
    p_comb = np.where(min_p < 1e-14, np.clip(len(basis_list) * min_p, 1e-300, 1.0), p_comb)
    return np.where(valid, -np.log10(p_comb), 0.0)


def make_normalized_counts_and_log1p(y_counts: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    ls = np.sum(y_counts, axis=1, keepdims=True)
    pos = ls[ls > 0]
    med = float(np.median(pos)) if pos.size > 0 else 1.0
    scaled = y_counts / np.where(ls > 0, ls, 1.0) * med
    return scaled, np.log1p(scaled)


def simulate_capture_regime(
    y_clean: np.ndarray, coords: np.ndarray, sigma_tech: float, mode: str, rng: np.random.Generator
) -> np.ndarray:
    n = y_clean.shape[0]
    if sigma_tech <= 0.0:
        return y_clean.copy()
    if mode == "bead_iid":
        z = rng.normal(0.0, 1.0, size=n)
    elif mode == "channel_striping":
        c = coords - coords.mean(axis=0, keepdims=True)
        span = np.maximum(np.ptp(c, axis=0), 1e-8)
        ch_x = np.floor((c[:, 0] - c[:, 0].min()) / (span[0] / 40.0)).astype(int)
        ch_y = np.floor((c[:, 1] - c[:, 1].min()) / (span[1] / 40.0)).astype(int)
        rx = rng.normal(0.0, 1.0, size=45)[np.clip(ch_x, 0, 44)]
        ry = rng.normal(0.0, 1.0, size=45)[np.clip(ch_y, 0, 44)]
        z = (rx + ry) / math.sqrt(2.0)
        z = (z - np.mean(z)) / max(float(np.std(z)), 1e-8)
    else:
        raise ValueError(mode)

    eta = sigma_tech * z - 0.5 * (sigma_tech ** 2)
    c_s = np.exp(eta)[:, None]
    y_int = np.rint(y_clean).astype(np.int64)
    out = np.empty_like(y_int)
    low = c_s[:, 0] <= 1.0
    if np.any(low):
        out[low] = rng.binomial(y_int[low], np.clip(c_s[low], 0.0, 1.0))
    if np.any(~low):
        out[~low] = y_int[~low] + rng.poisson((c_s[~low] - 1.0) * y_int[~low])
    return out.astype(np.float64)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    t0 = time.perf_counter()
    cache_dir = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "openproblems_svg_zenodo_18193366"
    method_sha = hashlib.sha256((SCRIPT_DIR / "ams_svg_eb_v2.py").read_bytes()).hexdigest()

    regimes = [
        ("regime_1_intact_compartment", 0.00, "bead_iid"),
        ("regime_2a_moderate_bead_dropout", 0.35, "bead_iid"),
        ("regime_2b_strong_bead_dropout", 0.70, "bead_iid"),
        ("regime_2c_severe_bead_dropout", 0.85, "bead_iid"),
        ("regime_2d_channel_stripe_artifact", 0.70, "channel_striping"),
    ]

    ds_rows = []
    for idx_d, (stem, tech) in enumerate(STRESS_PANEL):
        adata, h5_sha = _load_or_fetch_panel_h5ad(stem, cache_dir)
        coords = np.asarray(adata.obsm["spatial"], dtype=np.float64)
        y_clean = adata.layers["counts"].toarray().astype(np.float64)
        orig_gene = adata.var["gene"].astype(str).values
        true_alpha = adata.var["spatial_var"].astype(float).values

        rng = np.random.default_rng(20261116 + 1009 * idx_d)
        reg_dict = {}
        for r_key, sig, mode in regimes:
            y_obs = simulate_capture_regime(y_clean, coords, sig, mode, rng)
            y_ls_scaled, x_norm = make_normalized_counts_and_log1p(y_obs)

            s_moran = delaunay_moran_i_normalized(x_norm, coords)
            s_ams_ls = score_svg_v1_reference(y_ls_scaled, coords)
            s_sparkx = py_sparkx_reference(y_obs, coords)
            s_v1 = score_svg_v1_reference(y_obs, coords)
            s_v2, diag = score_svg_v2(sp.csr_matrix(y_obs), coords, return_diagnostics=True)

            t_moran = eval_kendall(s_moran, orig_gene, true_alpha)
            t_ams_ls = eval_kendall(s_ams_ls, orig_gene, true_alpha)
            t_sparkx = eval_kendall(s_sparkx, orig_gene, true_alpha)
            t_v1 = eval_kendall(s_v1, orig_gene, true_alpha)
            t_v2 = eval_kendall(s_v2, orig_gene, true_alpha)

            auc_moran = eval_svg_vs_null_auroc(s_moran, true_alpha)
            auc_sparkx = eval_svg_vs_null_auroc(s_sparkx, true_alpha)
            auc_v1 = eval_svg_vs_null_auroc(s_v1, true_alpha)
            auc_v2 = eval_svg_vs_null_auroc(s_v2, true_alpha)

            reg_dict[r_key] = {
                "sigma_tech": sig,
                "mode": mode,
                "eb_kappa": round(float(diag["kappa"]), 6),
                "eb_cap_to_floor_ratio": round(float(diag["ratio"]), 4),
                "moran_norm_tau": round(t_moran, 6),
                "ams_global_ls_norm_tau": round(t_ams_ls, 6),
                "py_sparkx_tau": round(t_sparkx, 6),
                "ams_svg_v1_tau": round(t_v1, 6),
                "ams_svg_v2_tau": round(t_v2, 6),
                "gain_v2_over_v1": round(t_v2 - t_v1, 6),
                "gain_v2_over_sparkx": round(t_v2 - t_sparkx, 6),
                "gain_v2_over_moran_norm": round(t_v2 - t_moran, 6),
                "gain_v2_over_ams_global_ls": round(t_v2 - t_ams_ls, 6),
                "auroc_svg_vs_null_moran_norm": round(auc_moran, 6),
                "auroc_svg_vs_null_sparkx": round(auc_sparkx, 6),
                "auroc_svg_vs_null_v1": round(auc_v1, 6),
                "auroc_svg_vs_null_v2": round(auc_v2, 6),
            }

        ds_rows.append({
            "dataset_id": stem,
            "technology": tech,
            "zenodo_h5ad_sha256": h5_sha,
            "n_spots": int(coords.shape[0]),
            "n_genes": int(y_clean.shape[1]),
            "regimes": reg_dict,
        })

    regime_summary = {}
    for r_key, sig, mode in regimes:
        sub = [d["regimes"][r_key] for d in ds_rows]
        m_mor = float(np.mean([x["moran_norm_tau"] for x in sub]))
        m_als = float(np.mean([x["ams_global_ls_norm_tau"] for x in sub]))
        m_spx = float(np.mean([x["py_sparkx_tau"] for x in sub]))
        m_v1 = float(np.mean([x["ams_svg_v1_tau"] for x in sub]))
        m_v2 = float(np.mean([x["ams_svg_v2_tau"] for x in sub]))
        regime_summary[r_key] = {
            "sigma_tech": sig,
            "mode": mode,
            "mean_eb_kappa": round(float(np.mean([x["eb_kappa"] for x in sub])), 6),
            "mean_moran_norm_tau": round(m_mor, 6),
            "mean_ams_global_ls_norm_tau": round(m_als, 6),
            "mean_py_sparkx_tau": round(m_spx, 6),
            "mean_ams_svg_v1_tau": round(m_v1, 6),
            "mean_ams_svg_v2_tau": round(m_v2, 6),
            "mean_gain_v2_over_v1": round(m_v2 - m_v1, 6),
            "mean_gain_v2_over_sparkx": round(m_v2 - m_spx, 6),
            "mean_gain_v2_over_moran_norm": round(m_v2 - m_mor, 6),
            "mean_gain_v2_over_ams_global_ls": round(m_v2 - m_als, 6),
            "mean_auroc_moran_norm": round(float(np.mean([x["auroc_svg_vs_null_moran_norm"] for x in sub])), 6),
            "mean_auroc_sparkx": round(float(np.mean([x["auroc_svg_vs_null_sparkx"] for x in sub])), 6),
            "mean_auroc_v1": round(float(np.mean([x["auroc_svg_vs_null_v1"] for x in sub])), 6),
            "mean_auroc_v2": round(float(np.mean([x["auroc_svg_vs_null_v2"] for x in sub])), 6),
        }

    payload = {
        "schema_version": "2.0.0",
        "evaluated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "frozen_method_sha256": method_sha,
        "runtime_sec": round(time.perf_counter() - t0, 3),
        "n_panel_datasets": len(ds_rows),
        "regime_summary_9_datasets": regime_summary,
        "datasets": ds_rows,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
