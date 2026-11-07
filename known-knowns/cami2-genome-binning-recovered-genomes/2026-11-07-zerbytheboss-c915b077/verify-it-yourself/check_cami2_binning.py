#!/usr/bin/env python3
import ast
import gzip
import json
import os
import sys
sys.dont_write_bytecode = True
from collections import defaultdict


def fail(msg):
    print(f"Verification error: {msg}")
    print("FAIL")
    sys.exit(1)


def comb2(n):
    return n * (n - 1) // 2


def parse_binning_gz(paths):
    bins = defaultdict(list)
    sample_id = None
    for p in paths:
        if not os.path.isfile(p):
            fail(f"Missing binning file {p}")
        with gzip.open(p, "rt", encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\n")
                if not line or line.startswith("#"):
                    continue
                if line.startswith("@SampleID:"):
                    sid = line.split(":", 1)[1].strip()
                    if sample_id is None:
                        sample_id = sid
                    elif sample_id != sid:
                        fail(f"SampleID mismatch: {sample_id} vs {sid}")
                    continue
                if line.startswith("@"):
                    continue
                parts = line.split("\t")
                if len(parts) != 2:
                    fail(f"Malformed binning line in {p}: {line}")
                bins[parts[1]].append(parts[0])
    return sample_id, dict(bins)


def load_amber_ref(paths):
    sample_id = None
    gs_len = {}
    remove_set = set()
    contig_map = {}
    for p in paths:
        if not os.path.isfile(p):
            fail(f"Missing reference file {p}")
        with gzip.open(p, "rt", encoding="utf-8") as f:
            d = json.load(f)
        if sample_id is None:
            sample_id = d["sample_id"]
        if d.get("gs_len"):
            gs_len.update({k: int(v) for k, v in d["gs_len"].items()})
        if d.get("remove_set"):
            remove_set.update(d["remove_set"])
        for s, pair in d["contig_map"].items():
            contig_map[s] = (pair[0], int(pair[1]))
    return sample_id, gs_len, remove_set, contig_map


def main():
    pkg_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    solver_path = os.path.join(pkg_root, "how-we-built-it", "solve_cami2_unsupervised.py")
    if not os.path.isfile(solver_path):
        fail("Missing how-we-built-it/solve_cami2_unsupervised.py")

    solver_src = open(solver_path, "r", encoding="utf-8").read()
    try:
        ast.parse(solver_src)
    except SyntaxError as e:
        fail(f"SyntaxError in solver: {e}")

    forbidden_tokens = ["gsa_pooled_mapping", "rhizosphere_short_read_pooled_gsa", "amber_ref", "TAXID", "plasmids.tsv", "marine_genome_cat.tsv"]
    for tok in forbidden_tokens:
        if tok in solver_src:
            fail(f"Zero-leakage check failed: forbidden token {tok} found in solver")

    sys.path.insert(0, os.path.join(pkg_root, "how-we-built-it"))
    import solve_cami2_unsupervised as cami_solver
    synth_len = {f"c{i}": 400_000 for i in range(10)}
    synth_binners = {
        "b1": {"binA": [f"c{i}" for i in range(5)], "binB": [f"c{i}" for i in range(5, 10)]},
        "b2": {"bin1": [f"c{i}" for i in range(5)], "bin2": [f"c{i}" for i in range(5, 10)]},
    }
    synth_sel, _ = cami_solver.run_refined_unsupervised_cami2(synth_binners, synth_len)
    if len(synth_sel) != 2:
        fail(f"Solver execution smoke check failed: expected 2 bins, got {len(synth_sel)}")

    obj_tsv = os.path.join(pkg_root, "object", "amber_cami2_per_bin_metrics.tsv")
    if not os.path.isfile(obj_tsv):
        fail("Missing object/amber_cami2_per_bin_metrics.tsv")

    with open(obj_tsv, "r", encoding="utf-8") as f:
        lines = [l.rstrip("\n") for l in f if l.strip()]

    expected_header = (
        "dataset\tsample_id\tbin_id\tn_contigs\ttotal_length_bp\tmost_abundant_genome\t"
        "tp_length_bp\tgs_length_bp\trecall_bp\tprecision_bp\tis_hq_all\tis_hq_filtered"
    )
    if not lines or lines[0] != expected_header:
        fail("Header mismatch in object/amber_cami2_per_bin_metrics.tsv")

    configs = [
        (
            "strain_madness",
            [os.path.join(pkg_root, "object", "strain_madness_refined.binning.gz")],
            [os.path.join(pkg_root, "verify-it-yourself", "data", "strain_madness_amber_ref.json.gz")],
        ),
        (
            "plant_associated",
            [os.path.join(pkg_root, "object", "plant_associated_refined.binning.gz")],
            [os.path.join(pkg_root, "verify-it-yourself", "data", "plant_associated_amber_ref.json.gz")],
        ),
        (
            "marine",
            [
                os.path.join(pkg_root, "object", "marine_refined_part1.binning.gz"),
                os.path.join(pkg_root, "object", "marine_refined_part2.binning.gz"),
            ],
            [
                os.path.join(pkg_root, "verify-it-yourself", "data", "marine_amber_ref_part1.json.gz"),
                os.path.join(pkg_root, "verify-it-yourself", "data", "marine_amber_ref_part2.json.gz"),
                os.path.join(pkg_root, "verify-it-yourself", "data", "marine_amber_ref_part3.json.gz"),
            ],
        ),
    ]

    recomputed_rows = []
    metrics = {}

    for name, bin_paths, ref_paths in configs:
        sid_b, bins = parse_binning_gz(bin_paths)
        sid_r, gs_len, rem_set, contig_map = load_amber_ref(ref_paths)
        if sid_b != sid_r:
            fail(f"Sample ID mismatch on {name}: {sid_b} vs {sid_r}")

        seen_contigs = set()
        hq_all = 0
        hq_filt = 0
        bin_row_sums = {}
        gs_col_sums = defaultdict(int)
        cell_sums = defaultdict(int)
        total_binned_bp = 0

        for bid in sorted(bins.keys()):
            sids = sorted(bins[bid])
            if not sids:
                fail(f"Empty bin {bid} in {name}")
            for s in sids:
                if s in seen_contigs:
                    fail(f"Duplicate contig {s} across bins in {name}")
                if s not in contig_map:
                    fail(f"Contig {s} missing from reference map in {name}")
                seen_contigs.add(s)

            n_c = len(sids)
            tot_l = sum(contig_map[s][1] for s in sids)
            g_counts = defaultdict(int)
            for s in sids:
                g, l_s = contig_map[s]
                g_counts[g] += l_s
                gs_col_sums[g] += l_s
                cell_sums[(bid, g)] += l_s
            bin_row_sums[bid] = tot_l
            total_binned_bp += tot_l

            best_g, tp_l = max(g_counts.items(), key=lambda x: (x[1], x[0]))
            gs_l = gs_len[best_g]
            rec = tp_l / gs_l
            prec = tp_l / tot_l
            hq_a = 1 if (rec > 0.90 and prec > 0.95) else 0
            hq_f = 1 if (hq_a == 1 and best_g not in rem_set) else 0
            hq_all += hq_a
            hq_filt += hq_f

            recomputed_rows.append(
                f"{name}\t{sid_b}\t{bid}\t{n_c}\t{tot_l}\t{best_g}\t{tp_l}\t{gs_l}\t{rec:.8f}\t{prec:.8f}\t{hq_a}\t{hq_f}"
            )

        sum_nij = sum(comb2(v) for v in cell_sums.values())
        sum_ai = sum(comb2(v) for v in bin_row_sums.values())
        sum_bj = sum(comb2(v) for v in gs_col_sums.values())
        tot_pairs = comb2(total_binned_bp)
        expected = (sum_ai * sum_bj) / tot_pairs if tot_pairs > 0 else 0.0
        max_idx = 0.5 * (sum_ai + sum_bj)
        ari_bp = (sum_nij - expected) / (max_idx - expected) if max_idx > expected else 0.0

        metrics[name] = {
            "hq_all": hq_all,
            "hq_filt": hq_filt,
            "ari_bp": ari_bp,
            "n_bins": len(bins),
        }

    actual_rows = lines[1:]
    if len(actual_rows) != len(recomputed_rows):
        fail(f"Row count mismatch in amber_cami2_per_bin_metrics.tsv: {len(actual_rows)} vs {len(recomputed_rows)}")

    for idx, (act, exp) in enumerate(zip(actual_rows, recomputed_rows), 2):
        if act != exp:
            fail(f"Line {idx} mismatch in object/amber_cami2_per_bin_metrics.tsv:\n  actual:   {act}\n  expected: {exp}")

    # Verify partial win thresholds (p1, p2, p3)
    sm = metrics["strain_madness"]
    pl = metrics["plant_associated"]
    mr = metrics["marine"]

    if not (sm["hq_all"] > 77 and sm["hq_all"] == 86):
        fail(f"p1 check failed: strain_madness HQ={sm['hq_all']} (expected 86 > 77)")
    if not (pl["hq_all"] > 118 and pl["hq_all"] == 135 and pl["hq_filt"] == 90):
        fail(f"p2 check failed: plant_associated HQ_all={pl['hq_all']}, HQ_noplasmid={pl['hq_filt']}")
    if not (mr["hq_filt"] >= 300 and mr["hq_filt"] == 328 and mr["ari_bp"] > 0.887 and abs(mr["ari_bp"] - 0.936349) < 1e-5):
        fail(f"p3 check failed: marine HQ_nocirc={mr['hq_filt']}, ARI={mr['ari_bp']:.6f}")

    print(
        f"Verified 1,325 CAMI II bins: p1 strain-madness HQ={sm['hq_all']} > 77 (ARI={sm['ari_bp']:.6f}), "
        f"p2 plant-associated HQ={pl['hq_all']} > 118 (no-plasmid={pl['hq_filt']} > 72, ARI={pl['ari_bp']:.6f}), "
        f"p3 marine HQ_nocirc={mr['hq_filt']} >= 300 & ARI={mr['ari_bp']:.6f} > 0.887"
    )
    print("PASS")


if __name__ == "__main__":
    main()
