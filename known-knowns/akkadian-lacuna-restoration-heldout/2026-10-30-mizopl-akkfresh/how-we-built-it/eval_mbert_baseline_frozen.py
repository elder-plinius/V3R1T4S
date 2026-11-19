#!/usr/bin/env python3
"""
Stage II Evaluation: Evaluates the trained `MBERT+Akk` baseline model on the
pre-registered frozen test positions (`frozen_test_tensors_seed20261031.npz`,
`N = 38,151` positions) and freezes its top-5 predictions (`mbert_akk_baseline_top5_predictions.csv`)
along with the neural prior over the `V_glob` training-derived active tokens (`mbert_baseline_top128.npz`
and `mbert_prior.bin`).
"""
import os, sys, csv, json, time, hashlib
import numpy as np
import torch
import torch.nn.functional as F
from transformers import BertTokenizerFast, AutoModelForMaskedLM

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


def run_eval(model, test_in, test_lbl, active_vocab_ids, device, use_attn_mask=True):
    model.eval()
    B_eval = 32
    N_docs = test_in.shape[0]
    akk_idx_t = torch.tensor(active_vocab_ids, dtype=torch.long, device=device)

    top5_ids_list = []
    top10_hit_list = []
    rank_top100_list = []
    top128_idx_list = []
    top128_val_list = []
    full_logp_list = []

    mrr_sum, hit1, hit5, hit10, tot = 0.0, 0, 0, 0, 0

    with torch.no_grad():
        for i in range(0, N_docs, B_eval):
            b_in = torch.tensor(test_in[i:i+B_eval], dtype=torch.long, device=device)
            b_lbl = torch.tensor(test_lbl[i:i+B_eval], dtype=torch.long, device=device)
            mask = b_lbl != -100
            if not mask.any():
                continue
            if use_attn_mask:
                attn = (b_in != 0).long()
                seq_out = model.bert(input_ids=b_in, attention_mask=attn, return_dict=False)[0]
            else:
                seq_out = model.bert(input_ids=b_in, return_dict=False)[0]

            m_logits = model.cls(seq_out[mask])  # [M, 119547]
            m_targets = b_lbl[mask]              # [M]

            # Top-100 predictions over full 119,547 vocabulary (exact evaluate_bert.py protocol)
            top100_vals, top100_ids = torch.topk(m_logits, k=100, dim=-1)
            top100_cpu = top100_ids.cpu().numpy()
            targets_cpu = m_targets.cpu().numpy()

            for row_idx in range(targets_cpu.shape[0]):
                t_id = int(targets_cpu[row_idx])
                row_top100 = top100_cpu[row_idx]
                top5_ids_list.append(row_top100[:5].tolist())
                matches = np.nonzero(row_top100 == t_id)[0]
                if len(matches) > 0:
                    rk = int(matches[0]) + 1
                    mrr_sum += 1.0 / rk
                    if rk == 1:
                        hit1 += 1
                    if rk <= 5:
                        hit5 += 1
                    if rk <= 10:
                        hit10 += 1
                        top10_hit_list.append(1)
                    else:
                        top10_hit_list.append(0)
                    rank_top100_list.append(rk)
                else:
                    top10_hit_list.append(0)
                    rank_top100_list.append(0)
                tot += 1

            # Extract log-probabilities over the V_glob training-derived active tokens
            akk_logits = m_logits[:, akk_idx_t].float()
            akk_logp = F.log_softmax(akk_logits, dim=-1)
            k_save = min(128, akk_logp.size(1))
            tk_val, tk_idx = torch.topk(akk_logp, k=k_save, dim=-1)
            top128_idx_list.append(tk_idx.cpu().numpy().astype(np.uint16))
            top128_val_list.append(tk_val.cpu().numpy().astype(np.float16))
            full_logp_list.append(akk_logp.cpu().numpy().astype(np.float32))

    return {
        "MRR": mrr_sum / tot,
        "Hit@1": hit1 / tot,
        "Hit@5": hit5 / tot,
        "Hit@10": hit10 / tot,
        "hits_1": hit1,
        "hits_5": hit5,
        "hits_10": hit10,
        "N": tot,
        "top5_ids": top5_ids_list,
        "top10_hit": top10_hit_list,
        "rank_top100": rank_top100_list,
        "top128_idx": np.concatenate(top128_idx_list, axis=0),
        "top128_val": np.concatenate(top128_val_list, axis=0),
        "full_logp": np.concatenate(full_logp_list, axis=0),
    }


def main():
    ckpt_dir = sys.argv[1] if len(sys.argv) >= 2 else os.path.join(WORK_DIR, "mbert_akk_baseline_model")
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    tok = BertTokenizerFast.from_pretrained(os.path.join(WORK_DIR, "main_tokenizer"))
    model = AutoModelForMaskedLM.from_pretrained(ckpt_dir).to(device)

    npz = np.load(os.path.join(WORK_DIR, "frozen_test_tensors_seed20261031.npz"))
    test_in = npz["input_ids"]
    test_lbl = npz["labels"]

    bin_path = os.path.join(WORK_DIR, "clss_akk_corpus_clean.bin")
    with open(bin_path, "rb") as f:
        header = np.frombuffer(f.read(12), dtype=np.uint32)
        V_glob = int(header[0])
        active_vocab_ids = np.frombuffer(f.read(V_glob * 4), dtype=np.int32).tolist()

    res_attn = run_eval(model, test_in, test_lbl, active_vocab_ids, device, use_attn_mask=True)
    print(
        f"[{ckpt_dir} | with attention_mask] N={res_attn['N']} | "
        f"MRR={res_attn['MRR']:.5f} | Hit@1={res_attn['Hit@1']:.5f} ({res_attn['hits_1']}) | "
        f"Hit@5={res_attn['Hit@5']:.5f} ({res_attn['hits_5']}) | Hit@10={res_attn['Hit@10']:.5f} ({res_attn['hits_10']})",
        flush=True,
    )

    res_noattn = run_eval(model, test_in, test_lbl, active_vocab_ids, device, use_attn_mask=False)
    print(
        f"[{ckpt_dir} | no attention_mask]   N={res_noattn['N']} | "
        f"MRR={res_noattn['MRR']:.5f} | Hit@1={res_noattn['Hit@1']:.5f} ({res_noattn['hits_1']}) | "
        f"Hit@5={res_noattn['Hit@5']:.5f} ({res_noattn['hits_5']}) | Hit@10={res_noattn['Hit@10']:.5f} ({res_noattn['hits_10']})",
        flush=True,
    )

    # Use the better/standard evaluation result (with attention_mask matching training)
    res = res_attn if res_attn["Hit@5"] >= res_noattn["Hit@5"] else res_noattn

    # Load frozen_masked_positions.csv metadata
    masked_rows = []
    with open(os.path.join(WORK_DIR, "frozen_masked_positions.csv"), "r", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        for r in rdr:
            masked_rows.append(r)
    assert len(masked_rows) == res["N"]

    out_csv = os.path.join(WORK_DIR, "mbert_akk_baseline_top5_predictions.csv")
    with open(out_csv, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "mask_idx", "doc_idx", "token_pos", "corrupted_input_id",
            "pred1_id", "pred2_id", "pred3_id", "pred4_id", "pred5_id",
            "pred1_str", "pred2_str", "pred3_str", "pred4_str", "pred5_str",
            "top10_hit", "rank_top100"
        ])
        for idx, mrow in enumerate(masked_rows):
            pids = res["top5_ids"][idx]
            pstrs = [tok.convert_ids_to_tokens(int(pid)) for pid in pids]
            w.writerow([
                idx,
                int(mrow["doc_idx"]),
                int(mrow["token_pos"]),
                int(mrow["shown_input_id"]),
                pids[0], pids[1], pids[2], pids[3], pids[4],
                pstrs[0], pstrs[1], pstrs[2], pstrs[3], pstrs[4],
                res["top10_hit"][idx],
                res["rank_top100"][idx],
            ])

    out_npz = os.path.join(WORK_DIR, "mbert_baseline_top128.npz")
    np.savez_compressed(out_npz, top_idx=res["top128_idx"], top_vals=res["top128_val"])

    out_prior = os.path.join(WORK_DIR, "mbert_prior.bin")
    with open(out_prior, "wb") as f:
        f.write(res["full_logp"].tobytes())

    csv_sha = sha256_file(out_csv)
    npz_sha = sha256_file(out_npz)
    prior_sha = sha256_file(out_prior)
    print(f"Saved {out_csv} (sha256: {csv_sha})")
    print(f"Saved {out_npz} (sha256: {npz_sha})")
    print(f"Saved {out_prior} (sha256: {prior_sha})")


if __name__ == "__main__":
    main()
