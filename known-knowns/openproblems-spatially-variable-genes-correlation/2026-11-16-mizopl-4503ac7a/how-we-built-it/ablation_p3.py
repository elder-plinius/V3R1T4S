#!/opt/homebrew/bin/python3
"""
Controlled Mechanistic Ablation (`p3`) for `openproblems-spatially-variable-genes-correlation`.

Isolates the three coupled failure modes of existing SVG methods across irregular point-cloud
(`slide-tags`, `Stereo-seq`, `MERFISH`) and dense grid/capture (`10x Visium`, `10x Xenium`,
`Slide-seqV2`) spatial transcriptomics technologies using single-factor interventions on
identical input matrices:

  1. Confounder #1 — Spot Library-Size Endogeneity (`1 / L_s` Normalization Contamination):
     Quantifies spatial autocorrelation of total spot counts `L_s = sum_g Y_{s,g}`, spurious
     spatial autocorrelation injected into true null (`alpha = 0`) genes by `Y / L_s`,
     single-factor removal of `1 / L_s` from Delaunay Moran's I, and single-factor injection
     of `1 / L_s` into frozen `AMS-SVG`.
  2. Confounder #2 — Irregular Point-Cloud Geometry, Cavity Bridging & NB Heavy Tails:
     Holds unnormalized variance-stabilized marginals and Cliff-Ord Z-scoring fixed while
     varying ONLY the spatial operator: unpruned Delaunay graph -> fixed global Euclidean
     Gaussian kernel -> single-scale adaptive kNN -> full 6-scale adaptive biweight kNN +
     low-rank Mercer (`AMS-SVG`), plus raw unstabilized counts vs VST (`log1p` + FT-root).
  3. Confounder #3 — IEEE-754 Binary64 P-Value Underflow Clipping (`-log10(max(p, 1e-300))`):
     Holds VST marginals and all 6 spatial operators of `AMS-SVG` fixed while comparing
     unbounded analytical permutation Z-scores against float64 p-value transformation
     `-log10(clip(Phi(-Z), 1e-300, 1.0))` (which saturates at Z >= 37.17), reporting both
     full-range (`alpha in [0, 1]`) and high-SNR (`alpha in [0.5, 1.0]`) Kendall's tau.
"""

from __future__ import annotations

import gzip
import hashlib
import json
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

PKG_DIR = Path(__file__).resolve().parents[1]
OBJECT_DIR = PKG_DIR / "object"
OUT_JSON = OBJECT_DIR / "ablation_p3.json"

sys.path.insert(0, str(OBJECT_DIR))
from method import (  # noqa: E402
    _normalize_gene_columns,
    build_multiscale_spatial_operators,
    build_self_tuning_biweight_knn_operator,
    cliff_ord_permutation_z,
    score_svg,
)

ZENODO_ZIP_URL = "https://zenodo.org/api/records/18193366/files/simulation_data.zip/content"
ZENODO_ZIP_SIZE = 411713101

ABLATION_PANEL = [
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
        headers={"Range": f"bytes={start}-{end_inclusive}", "User-Agent": "AMS-SVG-Verifier/1.0"},
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
    # Constant-tied predictions (e.g. 100% float64 p-value underflow at 1e-300) carry zero rank order -> 0.0
    return float(corrs.fillna(0.0).mean())


def build_delaunay_sym_operator(coords: np.ndarray) -> tuple[sp.csr_matrix, dict, np.ndarray]:
    tri = scipy.spatial.Delaunay(coords)
    edges = set()
    for s in tri.simplices:
        for u, v in ((s[0], s[1]), (s[1], s[2]), (s[0], s[2])):
            if u != v:
                edges.add((int(u), int(v)))
                edges.add((int(v), int(u)))
    rows, cols = zip(*edges)
    n = coords.shape[0]
    edge_lens = np.linalg.norm(coords[list(rows)] - coords[list(cols)], axis=1)
    a_sym = sp.csr_matrix((np.ones(len(rows), dtype=np.float64), (rows, cols)), shape=(n, n))
    deg = np.asarray(a_sym.sum(axis=1)).ravel()
    inv_sqrt = np.where(deg > 0, 1.0 / np.sqrt(np.maximum(deg, 1e-30)), 0.0)
    w_sym = (sp.diags(inv_sqrt) @ a_sym @ sp.diags(inv_sqrt)).tocsr()
    s0 = float(w_sym.sum())
    s1 = float(2.0 * np.sum(w_sym.data * w_sym.data))
    rs = np.asarray(w_sym.sum(axis=1)).ravel()
    s2 = float(4.0 * np.sum(rs * rs))
    return w_sym, {"type": "sparse", "n": n, "s0": s0, "s1": s1, "s2": s2}, edge_lens


def build_delaunay_row_norm(coords: np.ndarray) -> sp.csr_matrix:
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
    return (sp.diags(inv_deg) @ w).tocsr()


def moran_i_row(z: np.ndarray, w_row: sp.csr_matrix) -> np.ndarray:
    n = z.shape[0]
    zc = z - z.mean(axis=0, keepdims=True)
    denom = np.sum(zc * zc, axis=0)
    wz = w_row @ zc
    s0 = float(w_row.sum())
    return (n / s0) * np.sum(zc * wz, axis=0) / np.where(denom > 1e-15, denom, 1.0)


def build_fixed_euclidean_gaussian_operator(coords: np.ndarray, k_bw: int = 30) -> tuple[sp.csr_matrix, dict]:
    """Non-adaptive global Euclidean bandwidth kernel (fixed global sigma = median d_k)."""
    n = coords.shape[0]
    k_eff = min(max(6, k_bw), n - 1)
    tree = scipy.spatial.cKDTree(coords)
    dists, nbrs = tree.query(coords, k=min(n, 4 * k_eff + 1))
    sigma_global = float(np.median(dists[:, k_eff])) or 1.0
    d_sub = dists[:, 1:]
    n_sub = nbrs[:, 1:]
    rows = np.repeat(np.arange(n, dtype=np.int32), d_sub.shape[1])
    cols = n_sub.ravel().astype(np.int32)
    w_vals = np.exp(-(d_sub.ravel() ** 2) / (2.0 * sigma_global * sigma_global))
    a_dir = sp.csr_matrix((w_vals, (rows, cols)), shape=(n, n))
    a_sym = 0.5 * (a_dir + a_dir.T)
    a_sym.setdiag(0.0)
    a_sym.eliminate_zeros()
    deg = np.asarray(a_sym.sum(axis=1)).ravel()
    inv_sqrt = np.where(deg > 0, 1.0 / np.sqrt(np.maximum(deg, 1e-30)), 0.0)
    w_sym = (sp.diags(inv_sqrt) @ a_sym @ sp.diags(inv_sqrt)).tocsr()
    s0 = float(w_sym.sum())
    s1 = float(2.0 * np.sum(w_sym.data * w_sym.data))
    rs = np.asarray(w_sym.sum(axis=1)).ravel()
    s2 = float(4.0 * np.sum(rs * rs))
    return w_sym, {"type": "sparse", "n": n, "s0": s0, "s1": s1, "s2": s2}


def score_with_ops(y_mat: np.ndarray, ops: list, use_vst: bool = True, pval_underflow_clip: bool = False) -> tuple[np.ndarray, float]:
    if use_vst:
        reps = [
            _normalize_gene_columns(np.log1p(y_mat)),
            _normalize_gene_columns(np.sqrt(y_mat) + np.sqrt(y_mat + 1.0) - 1.0),
        ]
    else:
        reps = [_normalize_gene_columns(y_mat)]

    z_list = [cliff_ord_permutation_z(*tr, op) for tr in reps for op in ops]
    z_mean = np.mean(np.vstack(z_list), axis=0)
    frac_above_underflow = float(np.mean(z_mean >= 37.17))
    if not pval_underflow_clip:
        return z_mean, frac_above_underflow

    # Standard IEEE-754 binary64 p-value transformation used in existing wrappers (-log10(clip(p, 1e-300, 1)))
    pvals = np.clip(scipy.stats.norm.sf(z_mean), 1e-300, 1.0)
    return -np.log10(pvals), frac_above_underflow


def main() -> int:
    t0 = time.perf_counter()
    cache_dir = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "openproblems_svg_zenodo_18193366"
    rows_out = []

    for stem, tech in ABLATION_PANEL:
        adata, h5_sha = _load_or_fetch_panel_h5ad(stem, cache_dir)
        coords = np.asarray(adata.obsm["spatial"], dtype=np.float64)
        y_raw = adata.layers["counts"].toarray().astype(np.float64)
        x_norm = adata.X.toarray().astype(np.float64)
        orig_gene = adata.var["gene"].astype(str).values
        true_alpha = adata.var["spatial_var"].astype(float).values

        # Geometry & library-size diagnostics
        w_del_row = build_delaunay_row_norm(coords)
        w_del_sym, st_del, edge_lens = build_delaunay_sym_operator(coords)
        delaunay_p99_over_med = float(np.percentile(edge_lens, 99) / np.median(edge_lens))

        tree = scipy.spatial.cKDTree(coords)
        d15, _ = tree.query(coords, k=min(coords.shape[0], 16))
        r15 = np.maximum(d15[:, -1], 1e-12)
        # Local density proportional to 1 / r15^2
        density_p95_over_p05 = float((np.percentile(r15, 95) / np.percentile(r15, 5)) ** 2)

        lib_size = y_raw.sum(axis=1, keepdims=True)
        moran_lib_size = float(moran_i_row(np.log1p(lib_size), w_del_row)[0])

        moran_norm_vec = moran_i_row(x_norm, w_del_row)
        moran_raw_log1p_vec = moran_i_row(np.log1p(y_raw), w_del_row)
        alpha0 = true_alpha == 0.0
        spurious_alpha0_norm = float(np.mean(moran_norm_vec[alpha0]))
        alpha0_unnorm = float(np.mean(moran_raw_log1p_vec[alpha0]))

        # Confounder #1: 1/L_s normalization vs unnormalized counts
        tau_del_norm = eval_kendall(moran_norm_vec, orig_gene, true_alpha)
        tau_del_unnorm_log1p = eval_kendall(moran_raw_log1p_vec, orig_gene, true_alpha)

        # Inject 1/L_s library-size normalization into AMS-SVG (holding operators & Z-score fixed!)
        med_ls = float(np.median(lib_size[lib_size > 0])) if np.any(lib_size > 0) else 1.0
        y_ls_contaminated = y_raw / np.where(lib_size > 0, lib_size, 1.0) * med_ls
        ops_ams = list(build_multiscale_spatial_operators(coords))
        s_ams_ls_injected, _ = score_with_ops(y_ls_contaminated, ops_ams, use_vst=True, pval_underflow_clip=False)
        tau_ams_ls_injected = eval_kendall(s_ams_ls_injected, orig_gene, true_alpha)

        # Confounder #2: Operator & Heavy-Tail progression (all unnormalized, exact Z-score)
        s_del_vst, _ = score_with_ops(y_raw, [(w_del_sym, st_del)], use_vst=True, pval_underflow_clip=False)
        s_fixed_euc, _ = score_with_ops(y_raw, [build_fixed_euclidean_gaussian_operator(coords, 30)], use_vst=True, pval_underflow_clip=False)
        s_single_knn, _ = score_with_ops(y_raw, [build_self_tuning_biweight_knn_operator(coords, 50)], use_vst=True, pval_underflow_clip=False)
        s_ams_raw_counts, _ = score_with_ops(y_raw, ops_ams, use_vst=False, pval_underflow_clip=False)
        s_ams_full = score_svg(adata.layers["counts"], coords)

        tau_del_vst = eval_kendall(s_del_vst, orig_gene, true_alpha)
        tau_fixed_euc = eval_kendall(s_fixed_euc, orig_gene, true_alpha)
        tau_single_knn = eval_kendall(s_single_knn, orig_gene, true_alpha)
        tau_ams_raw_counts = eval_kendall(s_ams_raw_counts, orig_gene, true_alpha)
        tau_ams_full = eval_kendall(s_ams_full, orig_gene, true_alpha)

        # Confounder #3: Float64 -log10(p) underflow clipping vs unbounded Z-score on AMS-SVG
        s_ams_pval_clip, frac_underflow = score_with_ops(y_raw, ops_ams, use_vst=True, pval_underflow_clip=True)
        tau_ams_pval_clip = eval_kendall(s_ams_pval_clip, orig_gene, true_alpha)

        # High-SNR stratum (alpha >= 0.50, 11 levels per gene) where float64 p-values underflow to 0
        hi_mask = true_alpha >= 0.50
        tau_high_alpha_z = eval_kendall(s_ams_full[hi_mask], orig_gene[hi_mask], true_alpha[hi_mask])
        tau_high_alpha_pval_clip = eval_kendall(s_ams_pval_clip[hi_mask], orig_gene[hi_mask], true_alpha[hi_mask])

        rec = {
            "dataset_id": stem,
            "technology": tech,
            "zenodo_h5ad_sha256": h5_sha,
            "n_spots": int(coords.shape[0]),
            "n_genes": int(y_raw.shape[1]),
            "geometry_diagnostics": {
                "delaunay_p99_over_median_edge": round(delaunay_p99_over_med, 4),
                "local_density_p95_over_p05": round(density_p95_over_p05, 4),
                "spot_library_size_moran_i": round(moran_lib_size, 6),
                "alpha0_null_mean_moran_i_normalized": round(spurious_alpha0_norm, 6),
                "alpha0_null_mean_moran_i_unnormalized": round(alpha0_unnorm, 6),
            },
            "confounder_1_library_size_endogeneity": {
                "delaunay_moran_normalized_tau": round(tau_del_norm, 6),
                "delaunay_moran_unnormalized_log1p_tau": round(tau_del_unnorm_log1p, 6),
                "gain_removing_1_over_Ls_on_delaunay": round(tau_del_unnorm_log1p - tau_del_norm, 6),
                "ams_svg_with_1_over_Ls_injected_tau": round(tau_ams_ls_injected, 6),
                "ams_svg_unnormalized_full_tau": round(tau_ams_full, 6),
                "drop_from_injecting_1_over_Ls_into_ams_svg": round(tau_ams_ls_injected - tau_ams_full, 6),
            },
            "confounder_2_geometry_and_heavy_tails": {
                "unpruned_delaunay_vst_z_tau": round(tau_del_vst, 6),
                "fixed_global_euclidean_vst_z_tau": round(tau_fixed_euc, 6),
                "single_scale_adaptive_knn50_vst_z_tau": round(tau_single_knn, 6),
                "multiscale_adaptive_raw_counts_no_vst_tau": round(tau_ams_raw_counts, 6),
                "ams_svg_multiscale_adaptive_vst_full_tau": round(tau_ams_full, 6),
                "gain_multiscale_adaptive_over_delaunay": round(tau_ams_full - tau_del_vst, 6),
                "gain_vst_over_raw_counts_on_ams_svg": round(tau_ams_full - tau_ams_raw_counts, 6),
            },
            "confounder_3_float64_pvalue_underflow": {
                "fraction_genes_exceeding_float64_1e300_cliff_Z37p17": round(frac_underflow, 6),
                "ams_svg_float64_neglog10p_clipped_tau": round(tau_ams_pval_clip, 6),
                "ams_svg_unbounded_perm_z_tau": round(tau_ams_full, 6),
                "full_range_gain_unbounded_z_over_pval_clip": round(tau_ams_full - tau_ams_pval_clip, 6),
                "high_snr_alpha_ge_0p5_neglog10p_clipped_tau": round(tau_high_alpha_pval_clip, 6),
                "high_snr_alpha_ge_0p5_unbounded_z_tau": round(tau_high_alpha_z, 6),
                "high_snr_gain_unbounded_z_over_pval_clip": round(tau_high_alpha_z - tau_high_alpha_pval_clip, 6),
            },
        }
        rows_out.append(rec)
        print(
            f"[{stem:38s}] C1(Del norm->raw): {tau_del_norm:.4f}->{tau_del_unnorm_log1p:.4f} | "
            f"C2(Del->AMS & Raw->VST): {tau_del_vst:.4f}->{tau_ams_full:.4f} (raw={tau_ams_raw_counts:.4f}) | "
            f"C3(p_clip->Z on alpha>=0.5): {tau_high_alpha_pval_clip:.4f}->{tau_high_alpha_z:.4f} (underflow={frac_underflow*100:.1f}%)",
            flush=True,
        )

    payload = {
        "schema_version": "1.0.0",
        "evaluated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "runtime_sec": round(time.perf_counter() - t0, 3),
        "n_panel_datasets": len(rows_out),
        "mechanistic_summary": {
            "confounder_1_largest_effect_dataset": max(
                rows_out,
                key=lambda r: abs(r["confounder_1_library_size_endogeneity"]["drop_from_injecting_1_over_Ls_into_ams_svg"]),
            )["dataset_id"],
            "mean_drop_injecting_1_over_Ls_into_ams_svg": round(
                float(np.mean([r["confounder_1_library_size_endogeneity"]["drop_from_injecting_1_over_Ls_into_ams_svg"] for r in rows_out])),
                6,
            ),
            "mean_gain_multiscale_adaptive_over_delaunay": round(
                float(np.mean([r["confounder_2_geometry_and_heavy_tails"]["gain_multiscale_adaptive_over_delaunay"] for r in rows_out])),
                6,
            ),
            "mean_gain_vst_over_raw_counts": round(
                float(np.mean([r["confounder_2_geometry_and_heavy_tails"]["gain_vst_over_raw_counts_on_ams_svg"] for r in rows_out])),
                6,
            ),
            "mean_high_snr_gain_unbounded_z_over_float64_pval_clip": round(
                float(np.mean([r["confounder_3_float64_pvalue_underflow"]["high_snr_gain_unbounded_z_over_pval_clip"] for r in rows_out])),
                6,
            ),
        },
        "datasets": rows_out,
    }

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    out_sha = hashlib.sha256(OUT_JSON.read_bytes()).hexdigest()
    print(f"\nSaved {OUT_JSON} (sha256={out_sha}) in {payload['runtime_sec']}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
