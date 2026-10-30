#!/usr/bin/env python3
"""
Stage I: Deterministic Split, Zero-Composition/8-Gram-Leakage Deduplication,
MBERT+Akk Tokenizer Construction (99 Injected Tokens), and Frozen Masking
for akkadian-lacuna-restoration-heldout (SEED = 20261030).
"""
import os, sys, csv, json, re, time, hashlib
from pathlib import Path
from collections import Counter
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

SPLIT_SEED = 20261030
MASK_SEED = 20261030

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(1 << 20)
            if not b:
                break
            h.update(b)
    return h.hexdigest()

def norm_words(text):
    t = re.sub(r"[\[\]⸢⸣?*<>]", "", text)
    return t.split()

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

    # 80/20 split by text at SEED = 20261030
    train_raw, test_raw = train_test_split(dedup_docs, test_size=0.2, random_state=SPLIT_SEED)
    assert len(train_raw) == 11544 and len(test_raw) == 2886

    # Filter empty lines in test as ORACCDataset does (1 empty record P342168)
    test_docs = [r for r in test_raw if len(r["bert_input"]) > 0 and not r["bert_input"].isspace()]
    print(f"Split at SEED={SPLIT_SEED}: train_raw={len(train_raw)}, test_raw={len(test_raw)}, non-empty test_docs={len(test_docs)}")

    # Load textdata.csv metadata
    td_by_id = {}
    with open(os.path.join(REPO_DIR, "data/Finished/PreWork/textdata.csv"), "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["Name"]:
                td_by_id[r["Name"]] = r

    # Collect test signatures for composition / duplicate exclusion from training
    test_id_set = set(r["id_text"] for r in test_raw)
    test_bi_set = set(r["bert_input"].strip() for r in test_docs)
    test_titles = set()
    test_disp = set()
    test_8g_bi = set()
    test_8g_raw = set()
    short_test_spans = set()

    for r in test_docs:
        ws = r["bert_input"].split()
        test_8g_bi.update(get_kgrams(ws, 8))
        test_8g_raw.update(get_kgrams(norm_words(r["raw_text"]), 8))
        if 0 < len(ws) < 8:
            short_test_spans.add(tuple(ws))
        m = td_by_id.get(r["id_text"])
        if m:
            if m["title"].strip(): test_titles.add(m["title"].strip())
            if m["display_name"].strip(): test_disp.add(m["display_name"].strip())

    # Index short test spans by length for O(1) lookup
    short_by_len = {}
    for sp in short_test_spans:
        short_by_len.setdefault(len(sp), set()).add(sp)

    # Filter train_raw to build composition-disjoint train_clean
    removed_counts = {
        "empty_or_exact_bert_input_match": 0,
        "shared_textdata_title_or_display_name": 0,
        "shared_word_8gram_bert_input": 0,
        "shared_word_8gram_raw_text": 0,
        "contains_short_test_doc_span": 0,
    }
    train_clean = []
    for r in train_raw:
        bi = r["bert_input"].strip()
        if not bi or bi in test_bi_set:
            removed_counts["empty_or_exact_bert_input_match"] += 1
            continue
        m = td_by_id.get(r["id_text"])
        if m and ((m["title"].strip() and m["title"].strip() in test_titles) or
                  (m["display_name"].strip() and m["display_name"].strip() in test_disp)):
            removed_counts["shared_textdata_title_or_display_name"] += 1
            continue
        ws = bi.split()
        if get_kgrams(ws, 8) & test_8g_bi:
            removed_counts["shared_word_8gram_bert_input"] += 1
            continue
        if get_kgrams(norm_words(r["raw_text"]), 8) & test_8g_raw:
            removed_counts["shared_word_8gram_raw_text"] += 1
            continue
        has_short = False
        for k_len, sp_set in short_by_len.items():
            if get_kgrams(ws, k_len) & sp_set:
                has_short = True
                break
        if has_short:
            removed_counts["contains_short_test_doc_span"] += 1
            continue
        train_clean.append(r)

    print("Train filtering breakdown:", json.dumps(removed_counts, indent=2))
    print(f"Clean composition-disjoint train_clean: {len(train_clean)} docs (removed {len(train_raw) - len(train_clean)} total)")

    # Double-check 0.0% 8-gram overlap and 0 shared compositions between train_clean and test_docs
    clean_train_8g_bi = set()
    clean_train_8g_raw = set()
    for r in train_clean:
        clean_train_8g_bi.update(get_kgrams(r["bert_input"].split(), 8))
        clean_train_8g_raw.update(get_kgrams(norm_words(r["raw_text"]), 8))
    assert len(clean_train_8g_bi & test_8g_bi) == 0, "Non-zero bert_input 8-gram overlap!"
    assert len(clean_train_8g_raw & test_8g_raw) == 0, "Non-zero raw_text 8-gram overlap!"
    assert len(set(r["id_text"] for r in train_clean) & test_id_set) == 0, "Non-zero id_text overlap!"
    print("[VERIFIED] 0 shared id_text, 0 shared textdata.csv titles/display_names, and 0.00000% word 8-gram overlap between train_clean and test_docs!")

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
    orig_vocab = dict(base_tok.vocab)
    inject_new_tokens_to_tokenizer(akk_tokens, base_tok, base_tok.all_special_tokens)
    main_tok_dir = os.path.join(WORK_DIR, "main_tokenizer")
    base_tok.save_pretrained(main_tok_dir)

    # Extract the exact 99 injected tokens at IDs 1..99
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

    # Verify that no special token and no U+1F607 (missing_id) is ever masked
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

    # Save frozen_test_tensors_seed20261030.npz
    npz_path = os.path.join(WORK_DIR, "frozen_test_tensors_seed20261030.npz")
    np.savez_compressed(npz_path, input_ids=input_ids, labels=labels)

    # Save public frozen_masked_positions.csv and frozen_masked_positions.json
    # NOTE: Does NOT include the hidden ground-truth label_id in the pre-registration CSV if we want a blind mask manifest,
    # OR wait: what does the criterion say?
    # Let's check: "and the frozen list records what is shown at each masked position, so that every system sees the identical input"
    positions_list = []
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
                    positions_list.append({
                        "mask_idx": m_idx,
                        "doc_idx": d_idx,
                        "id_text": id_txt,
                        "token_pos": t_pos,
                        "shown_input_id": sh_id,
                        "shown_token_str": sh_str,
                    })
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
            "verified_shared_id_text_count": 0,
            "verified_shared_textdata_title_or_display_name_count": 0,
            "verified_word_8gram_overlap_bert_input": 0,
            "verified_word_8gram_overlap_raw_text": 0,
            "verified_short_test_doc_span_overlap": 0,
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
    print(f"Stage I local freeze completed in {time.time()-t0:.2f}s.")

if __name__ == "__main__":
    main()
