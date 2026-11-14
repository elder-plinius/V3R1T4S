#!/usr/bin/env python3
"""
Stage II: 100% Test-Blind Training of the Paper's MBERT+Akk Baseline (Lazar et al. 2021)
with Repository Code (`ORACCDataset`, `DataCollatorForLanguageModelingAkkadian`, `main_tokenizer`)
and Default Settings (`bert-base-multilingual-cased`, full 119,547 vocabulary, `block_size = 128`,
`mlm_probability = 0.15`, `lr = 5e-5`, `weight_decay = 0.0`, `adam_beta1 = 0.9`, `adam_beta2 = 0.999`,
`adam_epsilon = 1e-8`, `max_grad_norm = 1.0`, linear schedule, effective batch size = 8).

ZERO-TRUST INVARIANT: This script NEVER loads or references any test file, test tensor, or test label.
It trains strictly on `bert_train_clean.txt` (`9,221` composition-disjoint training documents) and monitors
progress on a fixed internal validation subset (`val_from_train`, `500` training documents) before saving
the final trained model checkpoint to `mbert_akk_baseline_model/`.
"""
import os, sys, json, time, random
from collections import Counter
import numpy as np
import torch
import torch.nn as nn
from transformers import BertTokenizerFast, AutoModelForMaskedLM, get_linear_schedule_with_warmup

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
from akkadian_bert.datasets_bert import ORACCDataset
from akkadian_bert.data_collators_bert import DataCollatorForLanguageModelingAkkadian


def eval_internal_train_val(model, val_inp, val_lbl, device):
    model.eval()
    mrr_sum, hit1, hit5, hit10, tot = 0.0, 0, 0, 0, 0
    B_eval = 32
    with torch.no_grad():
        for i in range(0, val_inp.size(0), B_eval):
            b_in = val_inp[i:i+B_eval].to(device)
            b_lbl = val_lbl[i:i+B_eval].to(device)
            attn = (b_in != 0).long()
            seq_out = model.bert(input_ids=b_in, attention_mask=attn, return_dict=False)[0]
            mask = b_lbl != -100
            if not mask.any():
                continue
            m_logits = model.cls(seq_out[mask])
            m_targets = b_lbl[mask]
            true_scores = m_logits.gather(1, m_targets.unsqueeze(1))
            ranks = (m_logits > true_scores).sum(dim=1) + 1
            for r in ranks.cpu().tolist():
                tot += 1
                if r <= 100:
                    mrr_sum += 1.0 / r
                if r == 1:
                    hit1 += 1
                if r <= 5:
                    hit5 += 1
                if r <= 10:
                    hit10 += 1
    return {
        "train_val_MRR": mrr_sum / tot,
        "train_val_Hit@1": hit1 / tot,
        "train_val_Hit@5": hit5 / tot,
        "train_val_Hit@10": hit10 / tot,
        "N_val_masks": tot,
    }


def main():
    t0 = time.time()
    torch.manual_seed(42)
    np.random.seed(42)
    random.seed(42)

    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    print(f"Using device: {device}", flush=True)

    tok_dir = os.path.join(WORK_DIR, "main_tokenizer")
    tokenizer = BertTokenizerFast.from_pretrained(tok_dir)
    tokenizer._pad_token = tokenizer.pad_token
    missing_id = tokenizer.get_vocab()[MISSING_SIGN_CHAR]

    train_txt_path = os.path.join(WORK_DIR, "bert_train_clean.txt")
    train_dataset = ORACCDataset(
        file_path=train_txt_path,
        tokenizer=tokenizer,
        block_size=128,
        missing_sign_encoding=missing_id,
        encode_only_first_token_in_word=False,
        ignore_missing=True,
    )
    print(f"Loaded ORACCDataset from {train_txt_path}: {len(train_dataset)} documents, vocab size = {len(tokenizer)}", flush=True)

    data_collator = DataCollatorForLanguageModelingAkkadian(
        tokenizer=tokenizer,
        mlm_probability=0.15,
        missing_sign=MISSING_SIGN_CHAR,
    )

    # Create a fixed internal monitoring batch from the first 500 training documents (100% inside train_dataset)
    torch.manual_seed(12345)
    val_batch = data_collator([train_dataset[i] for i in range(500)])
    val_inp = val_batch["input_ids"]
    val_lbl = val_batch["labels"]

    # Load full bert-base-multilingual-cased (V = 119,547)
    model = AutoModelForMaskedLM.from_pretrained("bert-base-multilingual-cased").to(device)

    # Default HuggingFace Trainer / AdamW settings from akkadian_bert/train_bert.py:
    # per_device_train_batch_size = 2, gradient_accumulation_steps = 4 -> effective batch size = 8
    # lr = 5e-5, weight_decay = 0.0, adam_beta1 = 0.9, adam_beta2 = 0.999, adam_epsilon = 1e-8, max_grad_norm = 1.0
    batch_size = 8
    num_epochs = 8
    train_loader = torch.utils.data.DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        collate_fn=data_collator,
    )
    total_steps = len(train_loader) * num_epochs
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=5e-5,
        betas=(0.9, 0.999),
        eps=1e-8,
        weight_decay=0.0,
    )
    scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=0,
        num_training_steps=total_steps,
    )
    loss_fn = nn.CrossEntropyLoss()

    out_dir = os.path.join(WORK_DIR, "mbert_akk_baseline_model")
    os.makedirs(out_dir, exist_ok=True)

    for ep in range(1, num_epochs + 1):
        ep_t0 = time.time()
        model.train()
        torch.manual_seed(1000 + ep)
        running_loss = 0.0
        n_steps = len(train_loader)
        for step, batch in enumerate(train_loader):
            inp = batch["input_ids"].to(device)
            lbl = batch["labels"].to(device)
            active = lbl != -100
            if not active.any():
                continue
            attn = (inp != 0).long()
            optimizer.zero_grad(set_to_none=True)
            seq_out = model.bert(input_ids=inp, attention_mask=attn, return_dict=False)[0]
            logits = model.cls(seq_out[active])
            loss = loss_fn(logits, lbl[active])
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            scheduler.step()
            running_loss += loss.item()
            if (step + 1) % 300 == 0 or (step + 1) == n_steps:
                print(f"  Epoch {ep}/{num_epochs} | Step {step+1}/{n_steps} | Loss={running_loss/min(300, step+1):.4f} | Elapsed={time.time()-ep_t0:.1f}s", flush=True)
                running_loss = 0.0

        val_res = eval_internal_train_val(model, val_inp, val_lbl, device)
        print(f"===> Epoch {ep} Done ({time.time()-ep_t0:.1f}s) | Internal Train-Val: MRR={val_res['train_val_MRR']:.5f}, Hit@1={val_res['train_val_Hit@1']:.5f}, Hit@5={val_res['train_val_Hit@5']:.5f}, Hit@10={val_res['train_val_Hit@10']:.5f}", flush=True)

        # Save model checkpoint after epoch >= 5
        if ep >= 5:
            ep_dir = os.path.join(WORK_DIR, f"mbert_akk_baseline_ep{ep}")
            model.save_pretrained(ep_dir)

    model.save_pretrained(out_dir)
    tokenizer.save_pretrained(out_dir)
    print(f"Saved final trained MBERT+Akk baseline model to {out_dir} in {time.time()-t0:.1f}s.", flush=True)


if __name__ == "__main__":
    main()
