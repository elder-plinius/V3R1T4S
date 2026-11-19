#!/usr/bin/env python3
import csv, hashlib, json, os, sys
import numpy as np

EXPECTED_FILES = {
    "object/akkadian_audit_manifest.json": (326637, "7e5e592d5c9f056ae11bc04eebe65e1bf1139024642c709f4da6b7a25c3b8097"),
    "object/prereg_split_and_mask_manifest.json": (190476, "06ba9a82589d8eeb31433480b275e4821df574938d1104ea607558cc88104877"),
    "object/baseline_frozen_manifest.json": (979, "b30998900a380114736b025b5e1fc333754af49e59eafae456c8cddb358d82c4"),
    "object/test_tensors_recipe.md": (3498, "10e76d818b299317b99422d379cd443ff1825dbdf44d0878485bac07fb82f3bc"),
    "object/akkadian_predictions_part1.csv": (831159, "f6669e1dbd8e383baab4e29bea5b62c8d16b25eee602f0119a76e389858cc905"),
    "object/akkadian_predictions_part2.csv": (837389, "7a4a4d9b62615aa995d283f97bff252eaa997a157c1931f4d36cea3146396cce"),
    "object/akkadian_predictions_part3.csv": (846352, "01fee33f699f9a77efd270f60f361a2b17066cf8e1ad5681bfe958083090999f"),
    "object/akkadian_predictions_part4.csv": (845892, "a9279330136ae3c0243cfa948656098e47ec4b02cee9ccea7c632125b6fa851e"),
    "object/akkadian_predictions_part5.csv": (848306, "397f971cc5135e59e138897de5841ea9cd474f64c0cb670dcbf1c7cac7aef3bf"),
    "object/akkadian_predictions_part6.csv": (846334, "0ae0fe2878b2c10ddd6d8a137164668ae672ba74cb6bfc69edaf633214a44c92"),
}


def fail(msg):
    print("CHECK ERROR:", msg)
    print("FAIL")
    sys.exit(1)


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for rel_p, (exp_sz, exp_sha) in EXPECTED_FILES.items():
        fp = os.path.join(root, rel_p)
        if not os.path.isfile(fp):
            fail(f"Missing file {rel_p}")
        data = open(fp, "rb").read()
        if len(data) != exp_sz or hashlib.sha256(data).hexdigest() != exp_sha:
            fail(f"SHA-256 or byte size mismatch on {rel_p}")
    print("[1/5] Object SHA-256 digests and byte sizes verified (10/10 files).")

    manifest = json.load(open(os.path.join(root, "object/akkadian_audit_manifest.json")))
    if manifest.get("benchmark_id") != "akkadian-lacuna-restoration-heldout":
        fail("Manifest benchmark_id mismatch")
    sp = manifest["split_protocol"]
    if (
        sp["n_train_rows_clean_composition_disjoint"] != 9221
        or sp["n_test_rows_heldout"] != 2886
        or sp["n_masked_positions_all"] != 38151
        or sp["active_akkadian_vocab_size_train_only"] != 1824
    ):
        fail("Manifest split count mismatch")
    prereg = manifest["preregistration_commit_before_training"]
    if prereg["commit_sha"] != "e26fa2cb33964bfe549770d311120ba1f804d81f":
        fail("Pre-registration commit SHA mismatch")

    rows = []
    for i in range(1, 7):
        with open(os.path.join(root, f"object/akkadian_predictions_part{i}.csv")) as f:
            rows.extend(list(csv.DictReader(f)))
    if len(rows) != 38151:
        fail(f"Expected 38151 total CSV rows, got {len(rows)}")

    N = 38151
    lbl_arr = np.zeros(N, dtype=np.int64)
    doc_arr = np.zeros(N, dtype=np.int64)
    genre_arr = np.zeros(N, dtype=np.int64)
    single_arr = np.zeros(N, dtype=np.int64)

    models = {"mb": {}, "cl": {}, "m1": {}, "pc": {}}
    for m in models:
        models[m]["p"] = np.zeros((N, 5), dtype=np.int64)
        models[m]["h10"] = np.zeros(N, dtype=np.int64)
        models[m]["r100"] = np.zeros(N, dtype=np.int64)

    for idx, r in enumerate(rows):
        if int(r["mask_idx"]) != idx:
            fail(f"mask_idx mismatch at {idx}")
        lbl_arr[idx] = int(r["label_id"])
        doc_arr[idx] = int(r["doc_idx"])
        genre_arr[idx] = int(r["genre_id"])
        single_arr[idx] = int(r["is_single_word"])
        for m in models:
            ps = [int(r[f"{m}_p{k}"]) for k in range(1, 6)]
            if len(set(ps)) != 5:
                fail(f"Duplicate top-5 candidates in {m} at {idx}")
            models[m]["p"][idx] = ps
            models[m]["h10"][idx] = int(r[f"{m}_h10"])
            models[m]["r100"][idx] = int(r[f"{m}_r100"])

    part_meta = manifest["index_partition_metadata"]
    kept_idx = set(part_meta["kept_token_mask_indices"])
    rand_idx = set(part_meta["random_token_mask_indices"])
    if len(kept_idx) != 3833 or len(rand_idx) != 3773 or (kept_idx & rand_idx):
        fail("Invalid kept/random partition indices")
    is_kept = np.array([i in kept_idx for i in range(N)], dtype=bool)
    is_rand = np.array([i in rand_idx for i in range(N)], dtype=bool)
    is_mask_only = (~is_kept) & (~is_rand)
    if int(is_mask_only.sum()) != 30545:
        fail(f"Expected 30545 [MASK]-only positions, got {int(is_mask_only.sum())}")

    print("[2/5] Verified 38,151 frozen positions (30,545 [MASK]-only, 3,833 kept-token, 3,773 random-token; 0 mismatches).")

    def score_subset(m, mask):
        sub_lbl = lbl_arr[mask][:, None]
        sub_p = models[m]["p"][mask]
        hits = (sub_p == sub_lbl)
        h1 = float(np.mean(hits[:, 0]))
        h5 = float(np.mean(np.any(hits, axis=1)))
        h10 = float(np.mean(models[m]["h10"][mask] > 0))
        r100 = models[m]["r100"][mask]
        mrr = float(np.mean(np.where(r100 > 0, 1.0 / np.maximum(r100, 1), 0.0)))
        mrr5 = float(np.mean(np.where((r100 >= 1) & (r100 <= 5), 1.0 / np.maximum(r100, 1), 0.0)))
        return h1, h5, h10, mrr, mrr5

    all_mask = np.ones(N, dtype=bool)
    single_mask = (single_arr == 1)

    mb_h1, mb_h5, mb_h10, mb_mrr, _ = score_subset("mb", all_mask)
    cl_h1, cl_h5, cl_h10, cl_mrr, _ = score_subset("cl", all_mask)
    m1_h1, m1_h5, m1_h10, m1_mrr, _ = score_subset("m1", all_mask)
    pc_h1, pc_h5, pc_h10, pc_mrr, _ = score_subset("pc", all_mask)

    _, mb_mo_h5, _, mb_mo_mrr, _ = score_subset("mb", is_mask_only)
    _, cl_mo_h5, _, cl_mo_mrr, _ = score_subset("cl", is_mask_only)
    _, mb_sw_h5, _, mb_sw_mrr, _ = score_subset("mb", single_mask)
    _, cl_sw_h5, _, cl_sw_mrr, _ = score_subset("cl", single_mask)

    # Reconstruct whole-word units (34,958 all words, 28,447 [MASK]-only words)
    parent = list(range(N))
    for cur_i, prev_i in part_meta["same_word_continuation_pairs"]:
        parent[cur_i] = parent[prev_i]
    word_groups_all = {}
    word_groups_mo = {}
    for i in range(N):
        root_i = parent[i]
        word_groups_all.setdefault(root_i, []).append(i)
        if is_mask_only[i]:
            word_groups_mo.setdefault(root_i, []).append(i)
    if len(word_groups_all) != 34958 or len(word_groups_mo) != 28447:
        fail(f"Word unit count mismatch: {len(word_groups_all)}, {len(word_groups_mo)}")

    def word_hit5(m, groups):
        p_mat = models[m]["p"]
        hits = sum(1 for idxs in groups.values() if all(lbl_arr[i] in p_mat[i] for i in idxs))
        return hits / len(groups)

    mb_ww_h5 = word_hit5("mb", word_groups_all)
    cl_ww_h5 = word_hit5("cl", word_groups_all)
    mb_ww_mo_h5 = word_hit5("mb", word_groups_mo)
    cl_ww_mo_h5 = word_hit5("cl", word_groups_mo)

    # Check all 6 cross-split composition / D8 / Q-number filters from manifest
    cs_audit = manifest["cross_split_composition_and_d8_audit"]
    filter_map = [
        ("excl_union_d8_ge_05", "excl_doc_indices_union_d8_ge_05"),
        ("excl_union_d8_ge_02", "excl_doc_indices_union_d8_ge_02"),
        ("excl_q_number_test_docs", "excl_doc_indices_q_number"),
        ("excl_q_or_shared_textdata_title", "excl_doc_indices_q_or_shared_title"),
        ("excl_q_or_6word_train_q_witness", "excl_doc_indices_q_or_6word_q_witness"),
        ("excl_10word_any_train_overlap", "excl_doc_indices_10word_train_overlap"),
    ]
    for audit_key, idx_key in filter_map:
        fmask = ~np.isin(doc_arr, part_meta[idx_key])
        exp_entry = cs_audit[audit_key]
        if int(fmask.sum()) != exp_entry["n_positions"]:
            fail(f"Position count mismatch on {audit_key}")
        _, f_mb_h5, _, f_mb_mrr, _ = score_subset("mb", fmask)
        _, f_cl_h5, _, f_cl_mrr, _ = score_subset("cl", fmask)
        if abs(f_mb_h5 - exp_entry["mbert_akk_baseline"]["hit_at_5"]) > 1e-5:
            fail(f"MBERT Hit@5 mismatch on {audit_key}")
        if abs(f_cl_h5 - exp_entry["clss_akk_v3_full"]["hit_at_5"]) > 1e-5:
            fail(f"CLSS Hit@5 mismatch on {audit_key}")
        if not (0.87 <= f_mb_h5 <= 0.91 and f_cl_h5 > 0.895 and f_cl_mrr > 0.83 and f_cl_h5 > f_mb_h5 and f_cl_mrr > f_mb_mrr):
            fail(f"Clause (1)/(2) failed on {audit_key}")

    if not (0.87 <= mb_h5 <= 0.91):
        fail(f"Clause (1) baseline gate failed: {mb_h5:.5f}")
    if abs(mb_h5 - 0.881576) > 1e-5 or abs(cl_h5 - 0.914209) > 1e-5:
        fail("Overall Hit@5 mismatch")
    if abs(mb_mrr - 0.831601) > 1e-5 or abs(cl_mrr - 0.848974) > 1e-5:
        fail("Overall MRR mismatch")
    if abs(m1_h5 - 0.913213) > 1e-5 or abs(pc_h5 - 0.877434) > 1e-5:
        fail("100%_MASK or CLSS-C-v3 Hit@5 mismatch")
    if abs(mb_mo_h5 - 0.868555) > 1e-5 or abs(cl_mo_h5 - 0.905058) > 1e-5:
        fail("[MASK]-only Hit@5 mismatch")
    if abs(mb_sw_h5 - 0.919439) > 1e-5 or abs(cl_sw_h5 - 0.935139) > 1e-5:
        fail("Single-word Hit@5 mismatch")
    if abs(mb_ww_h5 - 0.875937) > 1e-5 or abs(cl_ww_h5 - 0.909634) > 1e-5:
        fail("Whole-word unit Hit@5 mismatch")
    if abs(mb_ww_mo_h5 - 0.863465) > 1e-5 or abs(cl_ww_mo_h5 - 0.900939) > 1e-5:
        fail("[MASK]-only whole-word unit Hit@5 mismatch")

    d8_05_mb = cs_audit["excl_union_d8_ge_05"]["mbert_akk_baseline"]["hit_at_5"]
    d8_05_cl = cs_audit["excl_union_d8_ge_05"]["clss_akk_v3_full"]["hit_at_5"]
    print(
        f"[3/5] Verified all (MBERT={mb_h5:.5f}, CLSS={cl_h5:.5f}), [MASK]-only ({mb_mo_h5:.5f} vs {cl_mo_h5:.5f}), "
        f"single-word ({mb_sw_h5:.5f} vs {cl_sw_h5:.5f}), whole-word ({mb_ww_h5:.5f} vs {cl_ww_h5:.5f}), "
        f"and D8/Q-filtered ({d8_05_mb:.5f} vs {d8_05_cl:.5f}) subsets."
    )

    # Check Full Win & Partial Win p1 (> +0.01 overall margin and Table 2 genre subsets Lexical=10, Astrological Report=2, Royal Inscription=15)
    if not (cl_h5 - mb_h5 >= 0.01 and cl_mrr - mb_mrr >= 0.01 and cl_h5 - 0.895 >= 0.01 and cl_mrr - 0.83 >= 0.01):
        fail("Overall Full Win / p1 margin failed")
    for gid, gname, p_mrr, p_h5 in [(10, "Lexical", 0.69, 0.85), (2, "Astrological Report", 0.81, 0.88), (15, "Royal Inscription", 0.83, 0.90)]:
        gm = (genre_arr == gid)
        _, g_mb_h5, _, g_mb_mrr, _ = score_subset("mb", gm)
        _, g_cl_h5, _, g_cl_mrr, _ = score_subset("cl", gm)
        if not (g_cl_h5 > p_h5 and g_cl_mrr > p_mrr and g_cl_h5 > g_mb_h5 and g_cl_mrr > g_mb_mrr):
            fail(f"Genre {gname} failed p1 threshold")
    print("[4/5] Verified Full Win (Clause 1 & 2) and Partial Win p1 (> +0.01 overall margin and Table 2 genres Lexical, Astrological Report, Royal Inscription).")

    # 400 label-permutation null controls (seed=0)
    rng = np.random.default_rng(0)
    cl_p = models["cl"]["p"]
    null_h5 = np.zeros(400, dtype=np.float64)
    null_mrr = np.zeros(400, dtype=np.float64)
    weights = np.array([1.0, 0.5, 1.0 / 3.0, 0.25, 0.2], dtype=np.float64)
    for s in range(400):
        perm_lbl = rng.permutation(lbl_arr)[:, None]
        matches = (cl_p == perm_lbl)
        null_h5[s] = np.mean(np.any(matches, axis=1))
        null_mrr[s] = np.mean((matches * weights).max(axis=1))
    best_ctrl = float(null_h5.max())
    med_ctrl = float(np.median(null_h5))
    iqr_ctrl = float(np.percentile(null_h5, 75) - np.percentile(null_h5, 25))
    nm = manifest["null_permutation_controls_400_seed0"]
    if (
        abs(best_ctrl - nm["hit_at_5_max"]) > 1e-5
        or abs(med_ctrl - nm["hit_at_5_median"]) > 1e-5
        or abs(iqr_ctrl - nm["hit_at_5_iqr"]) > 1e-5
    ):
        fail(f"Null control mismatch: max={best_ctrl:.6f}, med={med_ctrl:.6f}, iqr={iqr_ctrl:.6f}")
    print(f"[5/5] Verified 400 label-permutation null controls (best_control Hit@5 = {best_ctrl:.5f} << real = {cl_h5:.5f}).")
    print("PASS")


if __name__ == "__main__":
    main()
