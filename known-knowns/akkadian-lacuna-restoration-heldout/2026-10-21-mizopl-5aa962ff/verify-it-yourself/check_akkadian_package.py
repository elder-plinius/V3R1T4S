#!/usr/bin/env python3
import csv, hashlib, json, os, sys
import numpy as np

EXPECTED_FILES = {
    "object/akkadian_audit_manifest.json": (11351, "5aa962ffd7f53168a043fa8477d88ffd10ab00afa296614869d3c5c3381e8db0"),
    "object/frozen_test_tensors_seed42.npz": (302914, "8033d870bd9d8787627690fc26771693a6acc112be17c7d94f204ed4a9654ec4"),
    "object/akkadian_predictions_part1.csv": (881312, "674fa60f65097b553aaa1fd8e8f946a7e1f8544eebf344447f5fa262dbfbd91d"),
    "object/akkadian_predictions_part2.csv": (885457, "7bd071b2de004066cf47d95b0b2ec23ed43b8b4e3c66d4524fc4cbd3c604a9ca"),
    "object/akkadian_predictions_part3.csv": (891053, "d57a42df831d4d1615b39ac38dac9dae70aed739a1535ab45851813cfaa6838b"),
    "object/akkadian_predictions_part4.csv": (852229, "9af89e1e184092e5d46c3fea2ff464891a332dbcf6f55b84a70a7674aa9b5aed"),
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
    print("[1/5] Object SHA-256 digests and byte sizes verified (6/6 files).")

    manifest = json.load(open(os.path.join(root, "object/akkadian_audit_manifest.json")))
    if manifest.get("benchmark_id") != "akkadian-lacuna-restoration-heldout":
        fail("Manifest benchmark_id mismatch")
    if manifest["split_protocol"]["n_test_rows_strict_zero_overlap"] != 1875 or manifest["split_protocol"]["n_masked_positions_all"] != 27650:
        fail("Manifest split count mismatch")

    npz = np.load(os.path.join(root, "object/frozen_test_tensors_seed42.npz"))
    labels = npz["labels"]
    mask_coords = np.argwhere(labels != -100)
    if len(mask_coords) != 27650:
        fail(f"Expected 27650 masked positions in npz, got {len(mask_coords)}")

    rows = []
    for i in range(1, 5):
        with open(os.path.join(root, f"object/akkadian_predictions_part{i}.csv")) as f:
            rows.extend(list(csv.DictReader(f)))
    if len(rows) != 27650:
        fail(f"Expected 27650 total CSV rows, got {len(rows)}")

    N = 27650
    lbl_arr = np.zeros(N, dtype=np.int64)
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
        d = int(r["doc_idx"])
        p = int(r["token_pos"])
        if d != int(mask_coords[idx, 0]) or p != int(mask_coords[idx, 1]):
            fail(f"Position mismatch at {idx}")
        lbl = int(r["label_id"])
        if lbl != int(labels[d, p]):
            fail(f"Label mismatch at {idx}")
        lbl_arr[idx] = lbl
        genre_arr[idx] = int(r["genre_id"])
        single_arr[idx] = int(r["is_single_word"])
        for m in models:
            ps = [int(r[f"{m}_p{k}"]) for k in range(1, 6)]
            if len(set(ps)) != 5:
                fail(f"Duplicate top-5 candidates in {m} at {idx}")
            models[m]["p"][idx] = ps
            models[m]["h10"][idx] = int(r[f"{m}_h10"])
            models[m]["r100"][idx] = int(r[f"{m}_r100"])

    print("[2/5] Verified 27,650 frozen masked positions against seed=42 test tensors (0 mismatches).")

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
    non_miss = (lbl_arr != 4) & (lbl_arr != 5)
    single_mask = (single_arr == 1)

    mb_h1, mb_h5, mb_h10, mb_mrr, mb_mrr5 = score_subset("mb", all_mask)
    cl_h1, cl_h5, cl_h10, cl_mrr, cl_mrr5 = score_subset("cl", all_mask)
    m1_h1, m1_h5, m1_h10, m1_mrr, _ = score_subset("m1", all_mask)
    pc_h1, pc_h5, pc_h10, pc_mrr, _ = score_subset("pc", all_mask)

    _, mb_nm_h5, _, mb_nm_mrr, _ = score_subset("mb", non_miss)
    cl_nm_h1, cl_nm_h5, cl_nm_h10, cl_nm_mrr, _ = score_subset("cl", non_miss)
    _, cl_sw_h5, _, cl_sw_mrr, _ = score_subset("cl", single_mask)

    if not (0.87 <= mb_h5 <= 0.91 and 0.87 <= mb_nm_h5 <= 0.91):
        fail(f"MBERT+Akk baseline outside [0.87, 0.91]: {mb_h5:.5f}, {mb_nm_h5:.5f}")
    if abs(mb_h5 - 0.87700) > 1e-5 or abs(mb_mrr - 0.82369) > 1e-5:
        fail(f"MBERT+Akk baseline metric drift: Hit@5={mb_h5:.5f}, MRR={mb_mrr:.5f}")
    if abs(cl_h5 - 0.92156) > 1e-5 or abs(cl_mrr - 0.85593) > 1e-5 or abs(cl_h1 - 0.80098) > 1e-5 or abs(cl_h10 - 0.94517) > 1e-5:
        fail(f"CLSS-Akk-v3 metric drift: Hit@1={cl_h1:.5f}, Hit@5={cl_h5:.5f}, Hit@10={cl_h10:.5f}, MRR={cl_mrr:.5f}")
    if not (cl_nm_h5 > 0.895 and cl_nm_mrr > 0.83 and cl_sw_h5 > 0.895 and cl_sw_mrr > 0.83 and m1_h5 > 0.895 and m1_mrr > 0.83 and pc_h5 > 0.895):
        fail("Subset or 100%_MASK or pure-C check failed")
    print(f"[3/5] Verified MBERT+Akk (Hit@5={mb_h5:.5f}, MRR={mb_mrr:.5f}) and CLSS-Akk-v3 (Hit@5={cl_h5:.5f}, MRR={cl_mrr:.5f}, Hit@1={cl_h1:.5f}, Hit@10={cl_h10:.5f}).")

    # Check Table 2 genre subsets (Lexical=9, Astrological Report=2, Royal or Monumental=14)
    for gid, gname, p_mrr, p_h5 in [(9, "Lexical", 0.69, 0.85), (2, "Astrological Report", 0.81, 0.88), (14, "Royal or Monumental", 0.84, 0.90)]:
        gm = (genre_arr == gid)
        _, g_mb_h5, _, g_mb_mrr, _ = score_subset("mb", gm)
        _, g_cl_h5, _, g_cl_mrr, _ = score_subset("cl", gm)
        if not (g_cl_h5 > p_h5 and g_cl_mrr > p_mrr and g_cl_h5 > g_mb_h5 and g_cl_mrr > g_mb_mrr):
            fail(f"Genre {gname} failed p1 threshold")
    print("[4/5] Verified Partial Win p1 (> +0.01 overall margin and Table 2 genre subsets Lexical, Astrological Report, Royal or Monumental).")

    # 400 label-permutation null controls (seed=0)
    rng = np.random.default_rng(0)
    cl_p = models["cl"]["p"]
    best_ctrl = 0.0
    for _ in range(400):
        perm_lbl = rng.permutation(lbl_arr)[:, None]
        ctrl_h5 = float(np.mean(np.any(cl_p == perm_lbl, axis=1)))
        if ctrl_h5 > best_ctrl:
            best_ctrl = ctrl_h5
    if best_ctrl >= 0.30:
        fail(f"Null control too high: {best_ctrl:.5f}")
    print(f"[5/5] Verified 400 label-permutation null controls (best_control Hit@5 = {best_ctrl:.5f} << real = {cl_h5:.5f}).")
    print("PASS")

if __name__ == "__main__":
    main()
