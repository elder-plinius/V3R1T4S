#!/usr/bin/env python3
"""
Stage III: Runs `clss_akk_engine_v3` on the frozen composition-disjoint split (`SEED = 20261031`,
`9,221` clean training docs, `2,886` test docs, `N = 38,151` masked positions), freezes the
top-5 prediction files BEFORE scoring, and exports the complete audit manifest and 5-part
compact prediction tables (`akkadian_predictions_part1..5.csv`).
"""
import os, sys, csv, json, time, hashlib, subprocess
import numpy as np
from transformers import BertTokenizerFast

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORK_DIR = os.environ.get("AKK_WORK_DIR", SCRIPT_DIR)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(1 << 20)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def export_scores_to_csv(scores_bin_path, out_csv_path, masked_rows, tok, true_lbls):
    with open(scores_bin_path, "rb") as f:
        nm = int(np.frombuffer(f.read(4), dtype=np.int32)[0])
        vg = int(np.frombuffer(f.read(4), dtype=np.uint32)[0])
        v_ids = np.frombuffer(f.read(vg * 4), dtype=np.int32).tolist()
        sc = np.frombuffer(f.read(nm * vg * 4), dtype=np.float32).reshape(nm, vg)

    assert nm == len(masked_rows), f"Row mismatch: {nm} != {len(masked_rows)}"
    r_idx = np.arange(nm)[:, None]
    top100_v = np.argpartition(-sc, 100, axis=1)[:, :100]
    ord100 = np.argsort(-sc[r_idx, top100_v], axis=1)
    top100_sorted = top100_v[r_idx, ord100]
    v_ids_arr = np.array(v_ids, dtype=np.int32)
    top100_ids = v_ids_arr[top100_sorted]

    top5_ids_list = []
    top10_hit_list = []
    rank_top100_list = []

    with open(out_csv_path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "mask_idx", "doc_idx", "token_pos", "corrupted_input_id",
            "pred1_id", "pred2_id", "pred3_id", "pred4_id", "pred5_id",
            "pred1_str", "pred2_str", "pred3_str", "pred4_str", "pred5_str",
            "top10_hit", "rank_top100"
        ])
        for idx, mrow in enumerate(masked_rows):
            row_top100 = top100_ids[idx]
            pids = row_top100[:5].tolist()
            pstrs = [tok.convert_ids_to_tokens(int(pid)) for pid in pids]
            t_id = int(true_lbls[idx])
            matches = np.nonzero(row_top100 == t_id)[0]
            if len(matches) > 0:
                rk = int(matches[0]) + 1
                h10 = 1 if rk <= 10 else 0
            else:
                rk = 0
                h10 = 0
            top5_ids_list.append(pids)
            top10_hit_list.append(h10)
            rank_top100_list.append(rk)
            w.writerow([
                idx,
                int(mrow["doc_idx"]),
                int(mrow["token_pos"]),
                int(mrow["shown_input_id"]),
                pids[0], pids[1], pids[2], pids[3], pids[4],
                pstrs[0], pstrs[1], pstrs[2], pstrs[3], pstrs[4],
                h10,
                rk,
            ])

    return {
        "sha256": sha256_file(out_csv_path),
        "bytes": os.path.getsize(out_csv_path),
        "top5_ids": np.array(top5_ids_list, dtype=np.int64),
        "top10_hit": np.array(top10_hit_list, dtype=np.int64),
        "rank_top100": np.array(rank_top100_list, dtype=np.int64),
    }


def load_csv_model_arrays(csv_path, N):
    p = np.zeros((N, 5), dtype=np.int64)
    h10 = np.zeros(N, dtype=np.int64)
    r100 = np.zeros(N, dtype=np.int64)
    with open(csv_path, "r", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        for idx, row in enumerate(rdr):
            assert int(row["mask_idx"]) == idx
            p[idx] = [int(row[f"pred{k}_id"]) for k in range(1, 6)]
            h10[idx] = int(row["top10_hit"])
            r100[idx] = int(row["rank_top100"])
    return {
        "sha256": sha256_file(csv_path),
        "bytes": os.path.getsize(csv_path),
        "top5_ids": p,
        "top10_hit": h10,
        "rank_top100": r100,
    }


def score_subset(mod_dict, lbl_arr, mask):
    sub_lbl = lbl_arr[mask][:, None]
    sub_p = mod_dict["top5_ids"][mask]
    hits = (sub_p == sub_lbl)
    n = int(mask.sum())
    hits_1 = int(hits[:, 0].sum())
    hits_5 = int(np.any(hits, axis=1).sum())
    hits_10 = int((mod_dict["top10_hit"][mask] > 0).sum())
    r100 = mod_dict["rank_top100"][mask]
    rr = np.where(r100 > 0, 1.0 / np.maximum(r100, 1), 0.0)
    rr5 = np.where((r100 >= 1) & (r100 <= 5), 1.0 / np.maximum(r100, 1), 0.0)
    return {
        "n": n,
        "mrr": round(float(np.mean(rr)), 6),
        "mrr_at_5": round(float(np.mean(rr5)), 6),
        "hit_at_1": round(float(hits_1 / n), 6),
        "hit_at_5": round(float(hits_5 / n), 6),
        "hit_at_10": round(float(hits_10 / n), 6),
        "hits_1": hits_1,
        "hits_5": hits_5,
        "hits_10": hits_10,
        "rr_vec": rr,
        "hit5_vec": np.any(hits, axis=1),
    }


def main():
    t0 = time.time()
    tok = BertTokenizerFast.from_pretrained(os.path.join(WORK_DIR, "main_tokenizer"))
    npz = np.load(os.path.join(WORK_DIR, "frozen_test_tensors_seed20261031.npz"))
    test_in = npz["input_ids"]
    test_lbl = npz["labels"]
    true_lbls = test_lbl[test_lbl != -100].astype(np.int64)
    N = len(true_lbls)
    assert N == 38151

    masked_rows = []
    with open(os.path.join(WORK_DIR, "frozen_masked_positions.csv"), "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            masked_rows.append(r)
    assert len(masked_rows) == N

    # Reconstruct neural prior from mbert_baseline_top128.npz so the pipeline is 100% reproducible from compact artifacts
    bin_path = os.path.join(WORK_DIR, "clss_akk_corpus_clean.bin")
    with open(bin_path, "rb") as f:
        V_glob = int(np.frombuffer(f.read(4), dtype=np.uint32)[0])
    p_npz = np.load(os.path.join(WORK_DIR, "mbert_baseline_top128.npz"))
    top_idx, top_vals = p_npz["top_idx"], p_npz["top_vals"]
    K = top_idx.shape[1]
    r_idx = np.arange(N)[:, None]
    floor_val = top_vals[:, -1:].astype(np.float32) - 1.0
    mbert_logp = np.broadcast_to(floor_val, (N, V_glob)).copy()
    tie_break = (np.arange(K, 0, -1, dtype=np.float32) * 1e-5)[None, :]
    mbert_logp[r_idx, top_idx] = top_vals.astype(np.float32) + tie_break
    prior_path = os.path.join(WORK_DIR, "mbert_prior_reconstructed.bin")
    with open(prior_path, "wb") as f:
        f.write(mbert_logp.tobytes())

    c_bin = os.path.join(WORK_DIR, "clss_akk_engine_v3")
    pure_scores_path = os.path.join(WORK_DIR, "clss_c_v3_pure_scores.bin")
    hyb_scores_path = os.path.join(WORK_DIR, "clss_akk_v3_scores.bin")
    m100_scores_path = os.path.join(WORK_DIR, "clss_akk_v3_100mask_scores.bin")

    if "--export-only" not in sys.argv:
        print("=== [1/4] Running CLSS-C-v3 Pure Symbolic (0 Neural) ===", flush=True)
        subprocess.run([c_bin, "", "0.0", bin_path, pure_scores_path], check=True)

        print("=== [2/4] Running CLSS-Akk-v3 Hybrid (alpha=11.5) + 100%_MASK ===", flush=True)
        env = os.environ.copy()
        env["CLSS_OUT_100MASK"] = m100_scores_path
        subprocess.run([c_bin, prior_path, "11.5", bin_path, hyb_scores_path], env=env, check=True)
    else:
        print("=== [1-2/4] Using existing CLSS score binaries (--export-only) ===", flush=True)

    print("=== [3/4] Freezing Top-5 Prediction CSVs BEFORE Scoring ===", flush=True)
    mb_csv = os.path.join(WORK_DIR, "mbert_akk_baseline_top5_predictions.csv")
    pure_csv = os.path.join(WORK_DIR, "clss_c_v3_pure_top5_predictions.csv")
    m100_csv = os.path.join(WORK_DIR, "clss_akk_100mask_top5_predictions.csv")
    hyb_csv = os.path.join(WORK_DIR, "clss_akk_top5_predictions.csv")

    mb_mod = load_csv_model_arrays(mb_csv, N)
    pure_mod = export_scores_to_csv(pure_scores_path, pure_csv, masked_rows, tok, true_lbls)
    m100_mod = export_scores_to_csv(m100_scores_path, m100_csv, masked_rows, tok, true_lbls)
    hyb_mod = export_scores_to_csv(hyb_scores_path, hyb_csv, masked_rows, tok, true_lbls)

    print(f"  [Frozen] mbert_akk_baseline_top5_predictions.csv : sha256={mb_mod['sha256']}")
    print(f"  [Frozen] clss_c_v3_pure_top5_predictions.csv     : sha256={pure_mod['sha256']}")
    print(f"  [Frozen] clss_akk_100mask_top5_predictions.csv   : sha256={m100_mod['sha256']}")
    print(f"  [Frozen] clss_akk_top5_predictions.csv           : sha256={hyb_mod['sha256']}")

    print("=== [4/4] Scoring Frozen Predictions & Exporting Package Objects ===", flush=True)
    # Build metadata arrays for the N=38,151 positions (map id_text -> genre from textdata.csv + ORACC sub_project_name)
    id2genre = {}
    subproj_genre_counts = {}
    id2subproj = {}
    raw_jsonl = os.path.join(WORK_DIR, "akk_repo", "data", "akk_from_jsons.jsonl")
    with open(raw_jsonl, "r", encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            if r["id_text"] not in id2subproj:
                id2subproj[r["id_text"]] = r.get("sub_project_name", "")

    td_csv = os.path.join(WORK_DIR, "akk_repo", "data", "Finished", "PreWork", "textdata.csv")
    with open(td_csv, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            nm = r.get("Name", "").strip()
            gn = r.get("genre", "").strip()
            if nm and gn:
                id2genre[nm] = gn
                sp = id2subproj.get(nm, "")
                if sp:
                    subproj_genre_counts.setdefault(sp, {})
                    subproj_genre_counts[sp][gn] = subproj_genre_counts[sp].get(gn, 0) + 1

    # Also check data/jsonl/*.jsonl project membership (e.g. dcclt.jsonl -> Lexical)
    jsonl_dir = os.path.join(WORK_DIR, "akk_repo", "data", "jsonl")
    id2projfile = {}
    if os.path.isdir(jsonl_dir):
        for fn in sorted(os.listdir(jsonl_dir)):
            if fn.endswith(".jsonl"):
                pname = fn[:-6]
                with open(os.path.join(jsonl_dir, fn), "r", encoding="utf-8") as f:
                    for line in f:
                        try:
                            obj = json.loads(line)
                            if "id_text" in obj:
                                id2projfile[obj["id_text"]] = pname
                        except Exception:
                            pass

    subproj_default_genre = {
        sp: max(gmap.items(), key=lambda x: x[1])[0]
        for sp, gmap in subproj_genre_counts.items()
    }
    proj_fallback = {
        "dcclt": "Lexical",
        "dccmt": "Mathematical",
        "rinap": "Royal Inscription",
        "riao": "Royal Inscription",
        "ribo": "Royal Inscription",
        "etcsri": "Royal Inscription",
        "suhu": "Royal Inscription",
        "ario": "Royal Inscription",
    }

    test_docs = [json.loads(line) for line in open(os.path.join(WORK_DIR, "akk_test_heldout.jsonl"), "r", encoding="utf-8")]
    for d in test_docs:
        tid = d["id_text"]
        sp = d.get("sub_project_name") or id2subproj.get(tid, "")
        pf = id2projfile.get(tid, "")
        if tid in id2genre:
            d["genre"] = id2genre[tid]
        elif pf in proj_fallback:
            d["genre"] = proj_fallback[pf]
        elif sp in subproj_default_genre:
            d["genre"] = subproj_default_genre[sp]
        elif sp in ("ebla", "nineveh", "signlists", "scholarly"):
            d["genre"] = "Lexical"
        elif sp == "saa08":
            d["genre"] = "Astrological Report"
        elif sp == "saa04":
            d["genre"] = "Extispicy Query"
        elif sp == "saa10":
            d["genre"] = "Scholarly Letter"
        elif sp.startswith("saa"):
            d["genre"] = "Administrative Letter"
        else:
            d["genre"] = "Unknown"
    genre_list = sorted({d["genre"] for d in test_docs})
    genre2id = {g: idx for idx, g in enumerate(genre_list)}

    doc_arr = np.zeros(N, dtype=np.int64)
    pos_arr = np.zeros(N, dtype=np.int64)
    genre_arr = np.zeros(N, dtype=np.int64)
    genre_str_arr = []
    single_arr = np.zeros(N, dtype=np.int64)
    kept_indices = []
    rand_indices = []
    same_word_pairs = []

    # Precompute per-document full token sequence to identify single-token words & continuation subtokens
    doc_orig_tokens = {}
    for d_idx, d in enumerate(test_docs):
        t_strs = tok.tokenize(d["bert_input"].strip())[:126]
        doc_orig_tokens[d_idx] = ["[CLS]"] + t_strs + ["[SEP]"]

    def is_cont(prev_s, cur_s):
        if cur_s.startswith("##"):
            return True
        if prev_s.endswith("-") or cur_s.startswith("-"):
            return True
        return False

    prev_doc = -1
    prev_pos = -1
    for idx, mrow in enumerate(masked_rows):
        d_idx = int(mrow["doc_idx"])
        t_pos = int(mrow["token_pos"])
        shown_id = int(mrow["shown_input_id"])
        doc_arr[idx] = d_idx
        pos_arr[idx] = t_pos
        g_name = test_docs[d_idx].get("genre") or "Unknown"
        genre_arr[idx] = genre2id[g_name]
        genre_str_arr.append(g_name)
        if shown_id == int(true_lbls[idx]) and shown_id != 103:
            kept_indices.append(idx)
        elif shown_id != 103:
            rand_indices.append(idx)

        orig_seq = doc_orig_tokens[d_idx]
        cur_s = orig_seq[t_pos]
        prev_s = orig_seq[t_pos - 1] if t_pos > 1 else ""
        next_s = orig_seq[t_pos + 1] if t_pos + 1 < len(orig_seq) - 1 else ""
        cont_prev = is_cont(prev_s, cur_s) if prev_s else False
        cont_next = is_cont(cur_s, next_s) if next_s else False
        single_arr[idx] = 0 if (cont_prev or cont_next) else 1
        if d_idx == prev_doc and t_pos == prev_pos + 1 and cont_prev:
            same_word_pairs.append([idx, idx - 1])
        prev_doc = d_idx
        prev_pos = t_pos

    all_mask = np.ones(N, dtype=bool)
    is_kept = np.zeros(N, dtype=bool)
    is_kept[kept_indices] = True
    is_rand = np.zeros(N, dtype=bool)
    is_rand[rand_indices] = True
    is_mask_only = (~is_kept) & (~is_rand)
    non_miss = (true_lbls != 4)
    single_mask = (single_arr == 1)

    res_all_mb = score_subset(mb_mod, true_lbls, all_mask)
    res_all_pure = score_subset(pure_mod, true_lbls, all_mask)
    res_all_m100 = score_subset(m100_mod, true_lbls, all_mask)
    res_all_hyb = score_subset(hyb_mod, true_lbls, all_mask)

    print(f"  Overall (N={N}):")
    print(f"    MBERT+Akk Baseline : MRR={res_all_mb['mrr']:.5f} | Hit@1={res_all_mb['hit_at_1']:.5f} | Hit@5={res_all_mb['hit_at_5']:.5f} | Hit@10={res_all_mb['hit_at_10']:.5f}")
    print(f"    CLSS-C-v3 Pure     : MRR={res_all_pure['mrr']:.5f} | Hit@1={res_all_pure['hit_at_1']:.5f} | Hit@5={res_all_pure['hit_at_5']:.5f} | Hit@10={res_all_pure['hit_at_10']:.5f}")
    print(f"    CLSS-Akk-v3 100%M  : MRR={res_all_m100['mrr']:.5f} | Hit@1={res_all_m100['hit_at_1']:.5f} | Hit@5={res_all_m100['hit_at_5']:.5f} | Hit@10={res_all_m100['hit_at_10']:.5f}")
    print(f"    CLSS-Akk-v3 Full   : MRR={res_all_hyb['mrr']:.5f} | Hit@1={res_all_hyb['hit_at_1']:.5f} | Hit@5={res_all_hyb['hit_at_5']:.5f} | Hit@10={res_all_hyb['hit_at_10']:.5f}")

    # Whole-word unit evaluation
    parent = list(range(N))
    for cur_i, prev_i in same_word_pairs:
        parent[cur_i] = parent[prev_i]
    word_groups_all = {}
    word_groups_mo = {}
    for i in range(N):
        root_i = parent[i]
        word_groups_all.setdefault(root_i, []).append(i)
        if is_mask_only[i]:
            word_groups_mo.setdefault(root_i, []).append(i)

    def word_hit5(mod_dict, groups):
        p_mat = mod_dict["top5_ids"]
        hits = sum(1 for idxs in groups.values() if all(true_lbls[i] in p_mat[i] for i in idxs))
        return round(hits / len(groups), 6), hits, len(groups)

    mb_ww_h5, mb_ww_hits, n_ww_all = word_hit5(mb_mod, word_groups_all)
    cl_ww_h5, cl_ww_hits, _ = word_hit5(hyb_mod, word_groups_all)
    mb_ww_mo_h5, mb_ww_mo_hits, n_ww_mo = word_hit5(mb_mod, word_groups_mo)
    cl_ww_mo_h5, cl_ww_mo_hits, _ = word_hit5(hyb_mod, word_groups_mo)

    # 400 label-permutation null controls (seed=0)
    rng = np.random.default_rng(0)
    cl_p = hyb_mod["top5_ids"]
    null_h5 = np.zeros(400, dtype=np.float64)
    null_mrr = np.zeros(400, dtype=np.float64)
    weights = np.array([1.0, 0.5, 1.0 / 3.0, 0.25, 0.2], dtype=np.float64)
    for s in range(400):
        perm_lbl = rng.permutation(true_lbls)[:, None]
        matches = (cl_p == perm_lbl)
        null_h5[s] = np.mean(np.any(matches, axis=1))
        null_mrr[s] = np.mean((matches * weights).max(axis=1))
    null_h5_iqr = float(np.percentile(null_h5, 75) - np.percentile(null_h5, 25))
    null_mrr_iqr = float(np.percentile(null_mrr, 75) - np.percentile(null_mrr, 25))

    # Cross-split composition, Q-number, and union-D8 audit (@DmitrL-dev & @elder-plinius review checks)
    train_docs = [json.loads(line) for line in open(os.path.join(WORK_DIR, "akk_train_clean.jsonl"), "r", encoding="utf-8")]

    def words_of(d):
        return [w for w in d["bert_input"].strip().split() if w]

    def ngrams_set(ws, n):
        if len(ws) < n:
            return set()
        return set(tuple(ws[i:i + n]) for i in range(len(ws) - n + 1))

    train_ws = [words_of(d) for d in train_docs]
    test_ws = [words_of(d) for d in test_docs]

    union_train_8 = set()
    union_train_10 = set()
    union_train_q_6 = set()
    for d, ws in zip(train_docs, train_ws):
        union_train_8 |= ngrams_set(ws, 8)
        union_train_10 |= ngrams_set(ws, 10)
        if d["id_text"].split("/")[-1].startswith("Q"):
            union_train_q_6 |= ngrams_set(ws, 6)

    id2titles = {}
    with open(td_csv, "r", encoding="utf-8", errors="ignore") as f:
        for r in csv.DictReader(f):
            nm = (r.get("Name") or "").strip()
            sid = nm.split("/")[-1]
            tset = set()
            for col in ("display_name", "title"):
                val = (r.get(col) or "").strip()
                if val:
                    tset.add(val)
            if tset:
                id2titles.setdefault(nm, set()).update(tset)
                id2titles.setdefault(sid, set()).update(tset)

    train_titles = set()
    for d in train_docs:
        idt = d["id_text"]
        sid = idt.split("/")[-1]
        train_titles |= id2titles.get(idt, set()) | id2titles.get(sid, set())

    excl_d8_05 = []
    excl_d8_02 = []
    excl_q = []
    excl_q_or_title = []
    excl_q_or_q6 = []
    excl_10w = []
    d8_vals = []

    for d_idx, (d, ws) in enumerate(zip(test_docs, test_ws)):
        idt = d["id_text"]
        sid = idt.split("/")[-1]
        is_q = sid.startswith("Q")
        if is_q:
            excl_q.append(d_idx)
        g8 = ngrams_set(ws, 8)
        if g8:
            d8 = len(g8 & union_train_8) / len(g8)
            d8_vals.append(d8)
            if d8 >= 0.5:
                excl_d8_05.append(d_idx)
            if d8 >= 0.2:
                excl_d8_02.append(d_idx)
        t_titles = id2titles.get(idt, set()) | id2titles.get(sid, set())
        if is_q or bool(t_titles & train_titles):
            excl_q_or_title.append(d_idx)
        g6 = ngrams_set(ws, 6)
        if is_q or bool(g6 & union_train_q_6):
            excl_q_or_q6.append(d_idx)
        g10 = ngrams_set(ws, 10)
        if bool(g10 & union_train_10):
            excl_10w.append(d_idx)

    def strip_vec(d):
        return {k: v for k, v in d.items() if not k.endswith("_vec")}

    def eval_doc_filter(excl_list):
        fmask = ~np.isin(doc_arr, excl_list)
        return {
            "excluded_test_docs": len(excl_list),
            "kept_test_docs": len(test_docs) - len(excl_list),
            "n_positions": int(fmask.sum()),
            "mbert_akk_baseline": strip_vec(score_subset(mb_mod, true_lbls, fmask)),
            "clss_akk_v3_full": strip_vec(score_subset(hyb_mod, true_lbls, fmask)),
        }

    cross_split_audit = {
        "n_test_docs_total": len(test_docs),
        "n_test_docs_with_8grams": len(d8_vals),
        "median_union_d8": round(float(np.median(d8_vals)), 6),
        "count_union_d8_ge_05": len(excl_d8_05),
        "count_union_d8_ge_02": len(excl_d8_02),
        "excl_union_d8_ge_05": eval_doc_filter(excl_d8_05),
        "excl_union_d8_ge_02": eval_doc_filter(excl_d8_02),
        "excl_q_number_test_docs": eval_doc_filter(excl_q),
        "excl_q_or_shared_textdata_title": eval_doc_filter(excl_q_or_title),
        "excl_q_or_6word_train_q_witness": eval_doc_filter(excl_q_or_q6),
        "excl_10word_any_train_overlap": eval_doc_filter(excl_10w),
    }

    # Write 6-part compact prediction CSVs into WORK_DIR/object_staging/ (each ~835 KB < 1 MB)
    obj_dir = os.path.join(WORK_DIR, "object_staging")
    os.makedirs(obj_dir, exist_ok=True)
    for old_f in os.listdir(obj_dir):
        if old_f.startswith("akkadian_predictions_part"):
            os.remove(os.path.join(obj_dir, old_f))
    n_parts = 6
    chunk_sz = (N + n_parts - 1) // n_parts
    part_files_meta = {}
    for p_idx in range(n_parts):
        lo = p_idx * chunk_sz
        hi = min(N, (p_idx + 1) * chunk_sz)
        part_name = f"akkadian_predictions_part{p_idx+1}.csv"
        part_path = os.path.join(obj_dir, part_name)
        with open(part_path, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow([
                "mask_idx", "doc_idx", "token_pos", "genre_id", "is_single_word", "label_id",
                "mb_p1", "mb_p2", "mb_p3", "mb_p4", "mb_p5", "mb_h10", "mb_r100",
                "cl_p1", "cl_p2", "cl_p3", "cl_p4", "cl_p5", "cl_h10", "cl_r100",
                "m1_p1", "m1_p2", "m1_p3", "m1_p4", "m1_p5", "m1_h10", "m1_r100",
                "pc_p1", "pc_p2", "pc_p3", "pc_p4", "pc_p5", "pc_h10", "pc_r100",
            ])
            for idx in range(lo, hi):
                mb_p = mb_mod["top5_ids"][idx]
                cl_p_row = hyb_mod["top5_ids"][idx]
                m1_p = m100_mod["top5_ids"][idx]
                pc_p = pure_mod["top5_ids"][idx]
                w.writerow([
                    idx, int(doc_arr[idx]), int(pos_arr[idx]), int(genre_arr[idx]),
                    int(single_arr[idx]), int(true_lbls[idx]),
                    int(mb_p[0]), int(mb_p[1]), int(mb_p[2]), int(mb_p[3]), int(mb_p[4]),
                    int(mb_mod["top10_hit"][idx]), int(mb_mod["rank_top100"][idx]),
                    int(cl_p_row[0]), int(cl_p_row[1]), int(cl_p_row[2]), int(cl_p_row[3]), int(cl_p_row[4]),
                    int(hyb_mod["top10_hit"][idx]), int(hyb_mod["rank_top100"][idx]),
                    int(m1_p[0]), int(m1_p[1]), int(m1_p[2]), int(m1_p[3]), int(m1_p[4]),
                    int(m100_mod["top10_hit"][idx]), int(m100_mod["rank_top100"][idx]),
                    int(pc_p[0]), int(pc_p[1]), int(pc_p[2]), int(pc_p[3]), int(pc_p[4]),
                    int(pure_mod["top10_hit"][idx]), int(pure_mod["rank_top100"][idx]),
                ])
        part_files_meta[f"object/{part_name}"] = {
            "bytes": os.path.getsize(part_path),
            "sha256": sha256_file(part_path),
            "rows": hi - lo,
        }

    # Build genre breakdown table
    paper_table2 = {
        "Lexical": (0.69, 0.85),
        "Astrological Report": (0.81, 0.88),
        "Royal or Monumental": (0.84, 0.90),
        "Royal Inscription": (None, None),
        "Administrative Letter": (None, None),
        "Scholarly Letter": (None, None),
        "Extispicy Query": (None, None),
        "Literary": (None, None),
        "Legal Transaction": (None, None),
        "Administrative Record": (None, None),
    }
    genre_breakdown = {}
    for g_name, g_id in sorted(genre2id.items(), key=lambda x: x[1]):
        gm = (genre_arr == g_id)
        if not gm.any():
            continue
        s_mb = score_subset(mb_mod, true_lbls, gm)
        s_cl = score_subset(hyb_mod, true_lbls, gm)
        s_m1 = score_subset(m100_mod, true_lbls, gm)
        s_pc = score_subset(pure_mod, true_lbls, gm)
        p_mrr, p_h5 = paper_table2.get(g_name, (None, None))
        genre_breakdown[g_name] = {
            "genre_id": g_id,
            "n": int(gm.sum()),
            "paper_mrr": p_mrr,
            "paper_hit_at_5": p_h5,
            "mbert_akk_baseline": {k: v for k, v in s_mb.items() if not k.endswith("_vec")},
            "clss_akk_v3_full": {k: v for k, v in s_cl.items() if not k.endswith("_vec")},
            "clss_akk_v3_100pct_mask": {k: v for k, v in s_m1.items() if not k.endswith("_vec")},
            "clss_c_v3_pure": {k: v for k, v in s_pc.items() if not k.endswith("_vec")},
        }

    def strip_vec(d):
        return {k: v for k, v in d.items() if not k.endswith("_vec")}

    prereg_manifest = json.load(open(os.path.join(WORK_DIR, "prereg_split_and_mask_manifest.json"), "r", encoding="utf-8"))

    audit_manifest = {
        "benchmark_id": "akkadian-lacuna-restoration-heldout",
        "category": "ancient-texts",
        "repository": "https://github.com/SLAB-NLP/Akk",
        "repository_commit": "dfd2a66d4305cf36981e4fd3fde823a5020161dd",
        "data_file": "data/akk_from_jsons.jsonl",
        "data_file_bytes": 21156545,
        "data_file_sha256": "b970895b8be1ff6dfe8b569110b311d9d6f3b213e60d1a61e6b963da783623a3",
        "preregistration_commit_before_training": {
            "github_repo": "mizopl/V3R1T4S",
            "branch": "submission/2026-10-30-mizopl-akkfresh",
            "commit_sha": "e26fa2cb33964bfe549770d311120ba1f804d81f",
            "committed_utc": "2026-10-30T08:24:24Z",
            "prereg_manifest_sha256": "06ba9a82589d8eeb31433480b275e4821df574938d1104ea607558cc88104877",
            "frozen_masked_positions_csv_sha256": prereg_manifest["masked_positions"]["frozen_masked_positions_csv_sha256"],
            "frozen_test_tensors_npz_sha256": prereg_manifest["masked_positions"]["frozen_test_tensors_npz_sha256"],
            "tokenizer_vocab_txt_sha256": prereg_manifest["tokenizer"]["vocab_txt_sha256"],
        },
        "split_protocol": {
            "train_test_split_seed": 20261031,
            "mask_seed": 20261031,
            "raw_corpus_rows": 23211,
            "unique_id_text_rows": 14430,
            "initial_train_rows_80pct": 11544,
            "test_rows_20pct": 2886,
            "removed_empty_or_exact_bert_input_matches": 23,
            "removed_8gram_composition_overlap_ge_020": 1704,
            "removed_shared_15word_block_with_test": 596,
            "n_train_rows_clean_composition_disjoint": 9221,
            "n_test_rows_heldout": 2886,
            "shared_id_text_train_vs_test": 0,
            "shared_15word_blocks_train_vs_test": 0,
            "max_pairwise_8gram_share_train_vs_test": 0.195122,
            "mlm_probability": 0.15,
            "block_size": 128,
            "n_masked_positions_all": N,
            "n_masked_positions_mask_only": int(is_mask_only.sum()),
            "n_masked_positions_kept_unchanged": int(is_kept.sum()),
            "n_masked_positions_random_token": int(is_rand.sum()),
            "n_masked_positions_non_missing_sign": int(non_miss.sum()),
            "n_masked_positions_single_token_words": int(single_mask.sum()),
            "active_akkadian_vocab_size_train_only": V_glob,
        },
        "frozen_prediction_hashes": {
            "mbert_akk_baseline_top5_predictions_csv": {
                "bytes": mb_mod["bytes"],
                "sha256": mb_mod["sha256"],
            },
            "clss_c_v3_pure_top5_predictions_csv": {
                "bytes": pure_mod["bytes"],
                "sha256": pure_mod["sha256"],
            },
            "clss_akk_100mask_top5_predictions_csv": {
                "bytes": m100_mod["bytes"],
                "sha256": m100_mod["sha256"],
            },
            "clss_akk_top5_predictions_csv": {
                "bytes": hyb_mod["bytes"],
                "sha256": hyb_mod["sha256"],
            },
        },
        "paper_benchmarks_lazar_et_al_2021": {
            "source": "Lazar et al., EMNLP 2021 Findings (arXiv:2109.04513), Section 5 & Table 2",
            "mbert_plus_akk_overall": {
                "mrr": 0.83,
                "hit_at_5": 0.89,
                "hit_at_5_precise_text": 0.895,
                "hit_at_10": 0.92,
            },
        },
        "overall_results_all_38151_frozen_positions": {
            "mbert_akk_reproduced_baseline": strip_vec(res_all_mb),
            "clss_c_v3_pure_symbolic_0_neural": strip_vec(res_all_pure),
            "clss_akk_v3_100pct_mask": strip_vec(res_all_m100),
            "clss_akk_v3_full_collator_80_10_10": strip_vec(res_all_hyb),
            "margins_clss_akk_v3_over_paper": {
                "delta_mrr_vs_083": round(res_all_hyb["mrr"] - 0.83, 6),
                "delta_hit5_vs_089": round(res_all_hyb["hit_at_5"] - 0.89, 6),
                "delta_hit5_vs_0895": round(res_all_hyb["hit_at_5"] - 0.895, 6),
                "delta_hit10_vs_092": round(res_all_hyb["hit_at_10"] - 0.92, 6),
            },
            "margins_clss_akk_v3_over_reproduced_baseline": {
                "delta_mrr": round(res_all_hyb["mrr"] - res_all_mb["mrr"], 6),
                "delta_hit1": round(res_all_hyb["hit_at_1"] - res_all_mb["hit_at_1"], 6),
                "delta_hit5": round(res_all_hyb["hit_at_5"] - res_all_mb["hit_at_5"], 6),
                "delta_hit10": round(res_all_hyb["hit_at_10"] - res_all_mb["hit_at_10"], 6),
            },
        },
        "subset_results": {
            "mask_only_positions_30545": {
                "mbert_akk_reproduced_baseline": strip_vec(score_subset(mb_mod, true_lbls, is_mask_only)),
                "clss_akk_v3_full": strip_vec(score_subset(hyb_mod, true_lbls, is_mask_only)),
                "clss_akk_v3_100pct_mask": strip_vec(score_subset(m100_mod, true_lbls, is_mask_only)),
                "clss_c_v3_pure_symbolic_0_neural": strip_vec(score_subset(pure_mod, true_lbls, is_mask_only)),
            },
            "kept_token_positions_3833": {
                "mbert_akk_reproduced_baseline": strip_vec(score_subset(mb_mod, true_lbls, is_kept)),
                "clss_akk_v3_full": strip_vec(score_subset(hyb_mod, true_lbls, is_kept)),
                "clss_akk_v3_100pct_mask": strip_vec(score_subset(m100_mod, true_lbls, is_kept)),
                "clss_c_v3_pure_symbolic_0_neural": strip_vec(score_subset(pure_mod, true_lbls, is_kept)),
            },
            "random_token_positions_3773": {
                "mbert_akk_reproduced_baseline": strip_vec(score_subset(mb_mod, true_lbls, is_rand)),
                "clss_akk_v3_full": strip_vec(score_subset(hyb_mod, true_lbls, is_rand)),
                "clss_akk_v3_100pct_mask": strip_vec(score_subset(m100_mod, true_lbls, is_rand)),
                "clss_c_v3_pure_symbolic_0_neural": strip_vec(score_subset(pure_mod, true_lbls, is_rand)),
            },
            "single_token_whole_words": {
                "mbert_akk_reproduced_baseline": strip_vec(score_subset(mb_mod, true_lbls, single_mask)),
                "clss_akk_v3_full": strip_vec(score_subset(hyb_mod, true_lbls, single_mask)),
                "clss_akk_v3_100pct_mask": strip_vec(score_subset(m100_mod, true_lbls, single_mask)),
                "clss_c_v3_pure_symbolic_0_neural": strip_vec(score_subset(pure_mod, true_lbls, single_mask)),
            },
            "whole_word_units": {
                "n_all_words": n_ww_all,
                "mbert_hit_at_5_all_words": mb_ww_h5,
                "clss_hit_at_5_all_words": cl_ww_h5,
                "n_mask_only_words": n_ww_mo,
                "mbert_hit_at_5_mask_only_words": mb_ww_mo_h5,
                "clss_hit_at_5_mask_only_words": cl_ww_mo_h5,
            },
        },
        "cross_split_composition_and_d8_audit": cross_split_audit,
        "table2_genre_breakdown": genre_breakdown,
        "null_permutation_controls_400_seed0": {
            "n_permutations": 400,
            "seed": 0,
            "hit_at_5_mean": round(float(null_h5.mean()), 6),
            "hit_at_5_std": round(float(null_h5.std()), 6),
            "hit_at_5_median": round(float(np.median(null_h5)), 6),
            "hit_at_5_iqr": round(null_h5_iqr, 6),
            "hit_at_5_max": round(float(null_h5.max()), 6),
            "mrr_mean": round(float(null_mrr.mean()), 6),
            "mrr_std": round(float(null_mrr.std()), 6),
            "mrr_median": round(float(np.median(null_mrr)), 6),
            "mrr_iqr": round(null_mrr_iqr, 6),
            "mrr_max": round(float(null_mrr.max()), 6),
        },
        "compact_prediction_parts": part_files_meta,
        "index_partition_metadata": {
            "kept_token_mask_indices": kept_indices,
            "random_token_mask_indices": rand_indices,
            "same_word_continuation_pairs": same_word_pairs,
            "excl_doc_indices_union_d8_ge_05": excl_d8_05,
            "excl_doc_indices_union_d8_ge_02": excl_d8_02,
            "excl_doc_indices_q_number": excl_q,
            "excl_doc_indices_q_or_shared_title": excl_q_or_title,
            "excl_doc_indices_q_or_6word_q_witness": excl_q_or_q6,
            "excl_doc_indices_10word_train_overlap": excl_10w,
        },
    }

    manifest_out = os.path.join(obj_dir, "akkadian_audit_manifest.json")
    with open(manifest_out, "w", encoding="utf-8") as f:
        json.dump(audit_manifest, f, indent=2)
    print(f"Wrote {manifest_out} ({os.path.getsize(manifest_out)} bytes, sha256={sha256_file(manifest_out)})")
    print(f"Stage III completed in {time.time()-t0:.2f}s.")


if __name__ == "__main__":
    main()
