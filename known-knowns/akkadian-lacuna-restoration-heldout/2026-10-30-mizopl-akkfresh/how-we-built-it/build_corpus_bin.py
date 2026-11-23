#!/usr/bin/env python3
"""
Builds the compact binary training/test corpus file `clss_akk_corpus_clean.bin`
strictly from `akk_train_clean.jsonl` (`9,221` composition-disjoint training docs)
and `frozen_test_tensors_seed20261031.npz` (`2,886` held-out test docs, `N = 38,151` masks).

ZERO-TRUST INVARIANT: `active_vocab_ids` (`V_glob`) is constructed 100% from the
clean training set (`akk_train_clean.jsonl`) and the 99 injected tokenizer slots (`1..99`),
with ZERO tokens added from `test_lbl` or `test_in`.
"""
import os, json, struct
import numpy as np
from transformers import BertTokenizerFast

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORK_DIR = os.environ.get("AKK_WORK_DIR", SCRIPT_DIR)


def main():
    tok = BertTokenizerFast.from_pretrained(os.path.join(WORK_DIR, "main_tokenizer"))
    npz = np.load(os.path.join(WORK_DIR, "frozen_test_tensors_seed20261031.npz"))
    test_in = npz["input_ids"]
    test_lbl = npz["labels"]

    train_rows = [
        json.loads(line)
        for line in open(os.path.join(WORK_DIR, "akk_train_clean.jsonl"), "r", encoding="utf-8")
    ]
    N_train = len(train_rows)
    N_test = test_in.shape[0]
    assert N_train == 9221 and N_test == 2886, f"Unexpected counts: N_train={N_train}, N_test={N_test}"

    # Active vocabulary strictly from training texts + injected slots 1..99 (100% test-blind)
    active_set = set(range(1, 100))
    train_tok_lists = []
    seen_bi = set()
    train_is_unique = []
    for r in train_rows:
        bi = r["bert_input"].strip()
        is_u = 1 if bi not in seen_bi else 0
        seen_bi.add(bi)
        t_ids = tok.convert_tokens_to_ids(tok.tokenize(bi))
        train_tok_lists.append(t_ids)
        train_is_unique.append(is_u)
        active_set.update(t_ids)

    # Exclude special tokens [PAD]=0, [UNK]=100, [CLS]=101, [SEP]=102, [MASK]=103 from active target vocab
    for sp in [0, 100, 101, 102, 103]:
        active_set.discard(sp)

    active_vocab_ids = sorted(active_set)
    V_glob = len(active_vocab_ids)
    assert V_glob < 2040, f"V_glob={V_glob} exceeds MAX_V=2048"
    orig2c = {tid: c for c, tid in enumerate(active_vocab_ids)}

    BOS_C = V_glob
    EOS_C = V_glob + 1
    MISS_C = V_glob + 2
    UNK_C = V_glob + 3
    MASK_C = V_glob + 4

    out_bin = os.path.join(WORK_DIR, "clss_akk_corpus_clean.bin")
    oov_test_masks = 0
    with open(out_bin, "wb") as f:
        f.write(struct.pack("<III", V_glob, N_train, N_test))
        f.write(np.array(active_vocab_ids, dtype=np.int32).tobytes())

        for i in range(N_train):
            t_ids = train_tok_lists[i][:4096]
            L = len(t_ids)
            c_toks = [orig2c.get(t, UNK_C) for t in t_ids]
            f.write(struct.pack("<HH", L, train_is_unique[i]))
            f.write(np.array(c_toks, dtype=np.uint16).tobytes())

        total_masked = 0
        for d in range(N_test):
            row_in = test_in[d]
            row_lbl = test_lbl[d]
            valid_pos = np.nonzero((row_in != 0) | (row_lbl != -100))[0]
            last_idx = int(valid_pos[-1])
            interior_in = row_in[1:last_idx]
            interior_lbl = row_lbl[1:last_idx]
            L = len(interior_in)
            c_in = []
            c_lbl = []
            c_pos = []
            for k in range(L):
                inp_t = int(interior_in[k])
                lbl_t = int(interior_lbl[k])
                if inp_t == 103:
                    c_in.append(MASK_C)
                elif inp_t in orig2c:
                    c_in.append(orig2c[inp_t])
                else:
                    c_in.append(UNK_C)
                if lbl_t != -100:
                    if lbl_t in orig2c:
                        c_lbl.append(orig2c[lbl_t])
                    else:
                        c_lbl.append(-2)
                        oov_test_masks += 1
                    total_masked += 1
                else:
                    c_lbl.append(-1)
                c_pos.append(k + 1)
            f.write(struct.pack("<H", L))
            f.write(np.array(c_in, dtype=np.uint16).tobytes())
            f.write(np.array(c_lbl, dtype=np.int16).tobytes())
            f.write(np.array(c_pos, dtype=np.uint16).tobytes())

    print(
        f"Wrote {out_bin}: V_glob={V_glob} (100% train-derived), N_train={N_train}, "
        f"N_test={N_test}, total_masked={total_masked}, oov_test_masks={oov_test_masks}"
    )


if __name__ == "__main__":
    main()
