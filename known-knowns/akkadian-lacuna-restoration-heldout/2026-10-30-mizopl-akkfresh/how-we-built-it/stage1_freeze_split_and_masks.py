#!/usr/bin/env python3
"""
Stage I: Deterministic Split, Composition-Disjoint & Parallel-Exemplar Deduplication,
MBERT+Akk Tokenizer Construction (99 Injected Tokens), and Frozen Masking
for akkadian-lacuna-restoration-heldout (SEED = 20261031).
Contains zero absolute paths; operates relative to AKK_WORK_DIR or its own directory.
"""
import os, sys, csv, json, re, time, hashlib
from pathlib import Path
from collections import Counter, defaultdict
from sklearn.model_selection import train_test_split
import numpy as np
import torch
from transformers import BertTokenizer, BertTokenizerFast

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORK_DIR = os.environ.get("AKK_WORK_DIR", SCRIPT_DIR)
REPO_DIR = os.environ.get("AKK_REPO_DIR", os.path.join(WORK_DIR, "akk_repo"))
sys.path.insert(0, REPO_DIR)
import types, importlib.machinery
nltk_mod = types.ModuleType("nltk")
nltk_mod.__spec__ = importlib.machinery.ModuleSpec("nltk", None)
nltk_mod.FreqDist = Counter
sys.modules["nltk"] = nltk_mod

from preprocessing.main_preprocess import MISSING_SIGN_CHAR
from akkadian_bert.tokenize_bert import train_tokenizer, inject_new_tokens_to_tokenizer, ROBERTA_UNUSED_TOKENS_NUM
from akkadian_bert.datasets_bert import ORACCDataset
from akkadian_bert.data_collators_bert import DataCollatorForLanguageModelingAkkadian

SPLIT_SEED = 20261031
MASK_SEED = 20261031


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(1 << 20)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def get_kgrams(words, k):
    if len(words) < k:
        return set()
    return set(tuple(words[i:i+k]) for i in range(len(words) - k + 1))


def main():
    t0 = time.time()
    raw_jsonl = os.path.join(REPO_DIR, "data/akk_from_jsons.jsonl")
    assert sha256_file(raw_jsonl) == "b970895b8be1ff6dfe8b569110b311d9d6f3b213e60d1a61e6b963da783623a3"

    # Load preprocessed deduplicated 14,430 records (first occurrence of each id_text in data/akk_from_jsons.jsonl)
    dedup_path = os.path.join(WORK_DIR, "dedup_14430_preprocessed.jsonl")
    dedup_docs = [json.loads(line) for line in open(dedup_path, "r", encoding="utf-8")]
    assert len(dedup_docs) == 14430

    # 80/20 split by text at SEED = 20261031
    train_raw, test_raw = train_test_split(dedup_docs, test_size=0.2, random_state=SPLIT_SEED)
    assert len(train_raw) == 11544 and len(test_raw) == 2886

    # Filter empty lines in test as ORACCDataset does (0 empty in SEED=20261031 test; P342168 is in train_raw)
    test_docs = [r for r in test_raw if len(r["bert_input"]) > 0 and not r["bert_input"].isspace()]
    print(f"Split at SEED={SPLIT_SEED}: train_raw={len(train_raw)}, test_raw={len(test_raw)}, non-empty test_docs={len(test_docs)}")

    # Load textdata.csv metadata
    td_by_id = {}
    disp_counts = Counter()
    with open(os.path.join(REPO_DIR, "data/Finished/PreWork/textdata.csv"), "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["Name"]:
                td_by_id[r["Name"]] = r
                if r["display_name"].strip():
                    disp_counts[r["display_name"].strip()] += 1

    # Collect test signatures for composition / parallel-exemplar exclusion from training
    test_id_set = set(r["id_text"] for r in test_raw)
    test_bi_set = set(r["bert_input"].strip() for r in test_docs)
    test_specific_disp = set()
    test_8g_per_doc = []
    all_test_15grams = set()

    for r in test_docs:
        ws = r["bert_input"].split()
        test_8g_per_doc.append(get_kgrams(ws, 8))
        all_test_15grams.update(get_kgrams(ws, 15))
        m = td_by_id.get(r["id_text"])
        if m:
            dn = m["display_name"].strip()
            if dn and disp_counts[dn] <= 5:
                test_specific_disp.add(dn)

    ng8_to_test = defaultdict(list)
    for idx, s8 in enumerate(test_8g_per_doc):
        for ng in s8:
            ng8_to_test[ng].append(idx)

    # Filter train_raw to build composition-disjoint train_clean:
    # 1. Remove empty or exact bert_input matches with any test doc
    # 2. Remove any train doc sharing a specific publication display_name in textdata.csv with any test doc
    # 3. Remove any train doc that shares >= 20% of distinct word 8-grams with any test doc (in either direction:
    #    c / len(test_8g) >= 0.20 or c / len(train_8g) >= 0.20, which eliminates composite/witness pairs like P229143 vs Q002268 at 83.3%)
    # 4. Remove any train doc sharing a contiguous block of >= 15 words with any test doc
    removed_counts = {
        "empty_or_exact_bert_input_match": 0,
        "shared_specific_publication_display_name": 0,
        "shared_composition_pairwise_8gram_share_ge_20pct": 0,
        "shared_contiguous_15word_block": 0,
    }
    train_clean = []
    for r in train_raw:
        bi = r["bert_input"].strip()
        if not bi or bi in test_bi_set:
            removed_counts["empty_or_exact_bert_input_match"] += 1
            continue
        m = td_by_id.get(r["id_text"])
        if m and m["display_name"].strip() in test_specific_disp:
            removed_counts["shared_specific_publication_display_name"] += 1
            continue
        ws = bi.split()
        s8 = get_kgrams(ws, 8)
        hit_test_counts = defaultdict(int)
        for ng in s8:
            if ng in ng8_to_test:
                for tidx in ng8_to_test[ng]:
                    hit_test_counts[tidx] += 1
        drop_8g = False
        for tidx, c in hit_test_counts.items():
            if c / len(test_8g_per_doc[tidx]) >= 0.20 or (len(s8) > 0 and c / len(s8) >= 0.20):
                drop_8g = True
                break
        if drop_8g:
            removed_counts["shared_composition_pairwise_8gram_share_ge_20pct"] += 1
            continue
        if get_kgrams(ws, 15) & all_test_15grams:
            removed_counts["shared_contiguous_15word_block"] += 1
            continue
        train_clean.append(r)

    print("Train filtering breakdown:", json.dumps(removed_counts, indent=2))
    print(f"Clean composition-disjoint train_clean: {len(train_clean)} docs (removed {len(train_raw) - len(train_clean)} total)")

    # Verify max pairwise 8-gram share < 0.20 and 0 shared 15-word blocks across all (train_clean, test_docs) pairs
    clean_15g = set()
    max_pair_share = 0.0
    for r in train_clean:
        ws = r["bert_input"].split()
        clean_15g.update(get_kgrams(ws, 15))
        s8 = get_kgrams(ws, 8)
        hit_tc = defaultdict(int)
        for ng in s8:
            if ng in ng8_to_test:
                for tidx in ng8_to_test[ng]:
                    hit_tc[tidx] += 1
        for tidx, c in hit_tc.items():
            sh = max(c / len(test_8g_per_doc[tidx]), c / len(s8) if s8 else 0.0)
            if sh > max_pair_share:
                max_pair_share = sh
    assert len(clean_15g & all_test_15grams) == 0, "Non-zero 15-gram overlap!"
    assert max_pair_share < 0.20, f"Max pairwise 8-gram share {max_pair_share} >= 0.20!"
    assert len(set(r["id_text"] for r in train_clean) & test_id_set) == 0, "Non-zero id_text overlap!"
    print(f"[VERIFIED] 0 shared id_text, 0 shared 15-word blocks, and max pairwise 8-gram share = {max_pair_share:.5f} (< 0.20) across all ({len(train_clean)} x {len(test_docs)}) pairs!")

    # Write train_clean and test_docs files
    train_jsonl_path = os.path.join(WORK_DIR, "akk_train_clean.jsonl")
    test_jsonl_path = os.path.join(WORK_DIR, "akk_test_heldout.jsonl")
    train_txt_path = os.path.join(WORK_DIR, "bert_train_clean.txt")
    test_txt_path = os.path.join(WORK_DIR, "bert_test_heldout.txt")

    with open(train_jsonl_path, "w", encoding="utf-8") as fj, open(train_txt_path, "w", encoding="utf-8") as ft:
        for r in train_clean:
            fj.write(json.dumps({"id_text": r["id_text"], "sub_project_name": r["sub_project_name"], "bert_input": r["bert_input"]}, ensure_ascii=False) + "\n")
            ft.write(r["bert_input"] + "\n")

    with open(test_jsonl_path, "w", encoding="utf-8") as fj, open(test_txt_path, "w", encoding="utf-8") as ft:
        for r in test_docs:
            fj.write(json.dumps({"id_text": r["id_text"], "sub_project_name": r["sub_project_name"], "bert_input": r["bert_input"]}, ensure_ascii=False) + "\n")
            ft.write(r["bert_input"] + "\n")

    # Build MBERT+Akk tokenizer strictly from train_txt_path using repository's train_tokenizer + inject_new_tokens_to_tokenizer
    os.chdir(WORK_DIR)
    train_tokenizer(".", ROBERTA_UNUSED_TOKENS_NUM * 10, train_txt_path)
    with open(os.path.join(WORK_DIR, "akk_tokenizer/vocab.txt"), "r", encoding="utf-8") as fv:
        akk_tokens = fv.read().splitlines()

    base_tok = BertTokenizer.from_pretrained("bert-base-multilingual-cased")
    inject_new_tokens_to_tokenizer(akk_tokens, base_tok, base_tok.all_special_tokens)
    main_tok_dir = os.path.join(WORK_DIR, "main_tokenizer")
    base_tok.save_pretrained(main_tok_dir)

    inv_vocab = {v: k for k, v in base_tok.vocab.items()}
    injected_99 = [{"slot_id": i, "token": inv_vocab[i]} for i in range(1, 100)]
    vocab_txt_path = os.path.join(main_tok_dir, "vocab.txt")
    vocab_sha256 = sha256_file(vocab_txt_path)
    print(f"Built main_tokenizer/vocab.txt (sha256: {vocab_sha256}), missing sign U+1F607 id = {base_tok.vocab.get(MISSING_SIGN_CHAR)}")
    print("First 15 injected tokens:", [x["token"] for x in injected_99[:15]])

    # Tokenize test_txt_path with ORACCDataset and mask with DataCollatorForLanguageModelingAkkadian at torch.manual_seed(MASK_SEED)
    tok_fast = BertTokenizerFast.from_pretrained(main_tok_dir)
    tok_fast._pad_token = tok_fast.pad_token
    missing_id = tok_fast.get_vocab()[MISSING_SIGN_CHAR]
    assert missing_id in range(1, 100), f"Expected U+1F607 in 1..99, got {missing_id}"

    test_ds = ORACCDataset(
        file_path=test_txt_path,
        tokenizer=tok_fast,
        block_size=128,
        missing_sign_encoding=missing_id,
        encode_only_first_token_in_word=False,
        ignore_missing=True,
    )
    assert len(test_ds) == len(test_docs), f"Dataset length mismatch: {len(test_ds)} != {len(test_docs)}"

    collator = DataCollatorForLanguageModelingAkkadian(
        tokenizer=tok_fast,
        mlm_probability=0.15,
        missing_sign=MISSING_SIGN_CHAR,
    )
    torch.manual_seed(MASK_SEED)
    batch = collator([test_ds[i] for i in range(len(test_ds))])
    input_ids = batch["input_ids"].numpy()
    labels = batch["labels"].numpy()

    masked_mask = labels != -100
    n_masked = int(masked_mask.sum())
    assert not np.any(labels[masked_mask] == missing_id), "U+1F607 was masked!"
    for sp_id in tok_fast.all_special_ids:
        assert not np.any(labels[masked_mask] == sp_id), f"Special token {sp_id} was masked!"

    mask_token_id = tok_fast.mask_token_id
    n_shown_mask = int((input_ids[masked_mask] == mask_token_id).sum())
    n_shown_kept = int((input_ids[masked_mask] == labels[masked_mask]).sum())
    n_shown_rand = n_masked - n_shown_mask - n_shown_kept
    print(f"Total masked positions (label_ids != -100): N = {n_masked} across {len(test_docs)} test docs")
    print(f"  80/10/10 breakdown: [MASK]={n_shown_mask} ({n_shown_mask/n_masked:.4f}), kept={n_shown_kept} ({n_shown_kept/n_masked:.4f}), random={n_shown_rand} ({n_shown_rand/n_masked:.4f})")

    npz_path = os.path.join(WORK_DIR, "frozen_test_tensors_seed20261031.npz")
    np.savez_compressed(npz_path, input_ids=input_ids, labels=labels)

    csv_path = os.path.join(WORK_DIR, "frozen_masked_positions.csv")
    with open(csv_path, "w", encoding="utf-8", newline="") as fc:
        w = csv.writer(fc)
        w.writerow(["mask_idx", "doc_idx", "id_text", "token_pos", "shown_input_id", "shown_token_str"])
        m_idx = 0
        for d_idx in range(input_ids.shape[0]):
            id_txt = test_docs[d_idx]["id_text"]
            for t_pos in range(input_ids.shape[1]):
                if labels[d_idx, t_pos] != -100:
                    sh_id = int(input_ids[d_idx, t_pos])
                    sh_str = tok_fast.convert_ids_to_tokens(sh_id)
                    w.writerow([m_idx, d_idx, id_txt, t_pos, sh_id, sh_str])
                    m_idx += 1

    json_manifest_path = os.path.join(WORK_DIR, "prereg_split_and_mask_manifest.json")
    prereg_manifest = {
        "target_id": "akkadian-lacuna-restoration-heldout",
        "upstream_repo": "https://github.com/SLAB-NLP/Akk",
        "upstream_commit": "dfd2a66d4305cf36981e4fd3fde823a5020161dd",
        "upstream_data_file": "data/akk_from_jsons.jsonl",
        "upstream_data_sha256": "b970895b8be1ff6dfe8b569110b311d9d6f3b213e60d1a61e6b963da783623a3",
        "split_seed": SPLIT_SEED,
        "mask_seed": MASK_SEED,
        "deduplication_and_composition_filtering": {
            "raw_records_in_akk_from_jsons": 23211,
            "duplicate_id_text_records_removed_before_split": 23211 - 14430,
            "unique_id_text_records_split_80_20": 14430,
            "initial_train_split_80pct": len(train_raw),
            "initial_test_split_20pct": len(test_raw),
            "empty_test_records_dropped_by_oraccdataset": len(test_raw) - len(test_docs),
            "final_test_documents": len(test_docs),
            "train_filtering_breakdown": removed_counts,
            "total_train_records_removed_for_composition_disjointness": len(train_raw) - len(train_clean),
            "final_clean_train_documents": len(train_clean),
            "final_clean_train_words": sum(len(r["bert_input"].split()) for r in train_clean),
            "verified_shared_id_text_count": 0,
            "verified_shared_15word_block_count": 0,
            "verified_max_pairwise_word_8gram_share": round(max_pair_share, 6),
        },
        "tokenizer": {
            "base_model": "bert-base-multilingual-cased",
            "missing_sign_char": "U+1F607",
            "missing_sign_token_id": missing_id,
            "vocab_txt_sha256": vocab_sha256,
            "injected_99_tokens": injected_99,
        },
        "masked_positions": {
            "n_test_docs": len(test_docs),
            "block_size": 128,
            "mlm_probability": 0.15,
            "n_masked_positions_total": n_masked,
            "n_shown_mask_token": n_shown_mask,
            "n_shown_kept_token": n_shown_kept,
            "n_shown_random_token": n_shown_rand,
            "frozen_masked_positions_csv_sha256": sha256_file(csv_path),
            "frozen_masked_positions_csv_bytes": os.path.getsize(csv_path),
            "frozen_test_tensors_npz_sha256": sha256_file(npz_path),
            "frozen_test_tensors_npz_bytes": os.path.getsize(npz_path),
            "bert_train_clean_txt_sha256": sha256_file(train_txt_path),
            "bert_test_heldout_txt_sha256": sha256_file(test_txt_path),
            "akk_train_clean_jsonl_sha256": sha256_file(train_jsonl_path),
            "akk_test_heldout_jsonl_sha256": sha256_file(test_jsonl_path),
        },
        "train_clean_id_texts": [r["id_text"] for r in train_clean],
        "test_heldout_id_texts": [r["id_text"] for r in test_docs],
    }
    with open(json_manifest_path, "w", encoding="utf-8") as fj:
        json.dump(prereg_manifest, fj, indent=2, ensure_ascii=False)

    print(f"Saved {json_manifest_path} (sha256: {sha256_file(json_manifest_path)})")
    print(f"Saved {csv_path} (sha256: {sha256_file(csv_path)})")
    print(f"Stage I (SEED={SPLIT_SEED}) local freeze completed in {time.time()-t0:.2f}s.")


if __name__ == "__main__":
    main()
