#!/usr/bin/env python3
"""
Extracts frozen ESM-2 (`facebook/esm2_t12_35M_UR50D`) sequence representations
for the 477 unique protein targets in `BindingDB_Patent`.
Compliant with Rule (e): pretrained sequence-only protein language model
trained on UniRef50 sequences WITHOUT any binding affinity labels.
"""
import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import time
from pathlib import Path
import numpy as np
import torch
from sklearn.preprocessing import StandardScaler, normalize
from transformers import AutoModel, AutoTokenizer

BASE_DIR = Path(__file__).resolve().parent
CACHE_DIR = BASE_DIR / "cache"


def main():
    t0 = time.time()
    out_path = CACHE_DIR / "protein_esm2.npz"
    if out_path.exists():
        print(f"Found existing {out_path}")
        return

    prot_npz = np.load(CACHE_DIR / "protein_features.npz", allow_pickle=True)
    targets = [str(s).strip().upper() for s in prot_npz["targets"]]
    n_prots = len(targets)
    print(f"Loaded {n_prots} unique protein sequences.")

    model_name = "facebook/esm2_t12_35M_UR50D"
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"Loading frozen {model_name} on device={device}...", flush=True)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name).to(device)
    model.eval()

    dim = model.config.hidden_size  # 480
    E_mean = np.zeros((n_prots, dim), dtype=np.float32)
    E_pocket = np.zeros((n_prots, dim), dtype=np.float32)
    E_std = np.zeros((n_prots, dim), dtype=np.float32)

    with torch.no_grad():
        for i, seq in enumerate(targets):
            clean_seq = "".join(c if c in "ACDEFGHIKLMNPQRSTVWY" else "X" for c in seq)
            if len(clean_seq) == 0:
                clean_seq = "M"
            # For long proteins (> 1022 residues), extract both N-terminal/catalytic window (0..1022)
            # and central catalytic window if > 1022
            windows = [clean_seq[:1022]]
            if len(clean_seq) > 1022:
                mid = len(clean_seq) // 2
                w2 = clean_seq[max(0, mid - 511): min(len(clean_seq), mid + 511)]
                windows.append(w2)

            tok_reps = []
            for w_seq in windows:
                inputs = tokenizer(w_seq, return_tensors="pt", add_special_tokens=True).to(device)
                out = model(**inputs, output_hidden_states=True)
                # Average last 2 layers for richer structural + evolutionary signal
                h_last = 0.65 * out.hidden_states[-1][0, 1:-1] + 0.35 * out.hidden_states[-2][0, 1:-1]
                tok_reps.append(h_last.detach().cpu().numpy().astype(np.float32))

            H_full = tok_reps[0]
            mean_vec = np.mean(H_full, axis=0)
            if len(tok_reps) > 1:
                mean_vec = 0.65 * mean_vec + 0.35 * np.mean(tok_reps[1], axis=0)
            std_vec = np.std(H_full, axis=0)

            # Catalytic / binding-core region (residues 80..520 where kinase/GPCR pockets sit)
            L = H_full.shape[0]
            if L > 160:
                s_idx = min(80, L // 4)
                e_idx = min(L, max(s_idx + 120, min(520, (3 * L) // 4)))
                pocket_vec = np.mean(H_full[s_idx:e_idx], axis=0)
            else:
                pocket_vec = mean_vec

            E_mean[i] = mean_vec
            E_pocket[i] = pocket_vec
            E_std[i] = std_vec

            if (i + 1) % 100 == 0 or (i + 1) == n_prots:
                print(f"  Processed {i+1}/{n_prots} proteins ({time.time()-t0:.1f}s)", flush=True)

    E_mean_norm = normalize(StandardScaler().fit_transform(E_mean)).astype(np.float32)
    E_pocket_norm = normalize(StandardScaler().fit_transform(E_pocket)).astype(np.float32)
    E_std_norm = normalize(StandardScaler().fit_transform(E_std)).astype(np.float32)
    E_concat_norm = normalize(np.hstack([E_mean_norm, E_pocket_norm, 0.5 * E_std_norm])).astype(np.float32)

    S_esm2_mean = np.clip(E_mean_norm @ E_mean_norm.T, -1.0, 1.0).astype(np.float32)
    S_esm2_pocket = np.clip(E_pocket_norm @ E_pocket_norm.T, -1.0, 1.0).astype(np.float32)
    S_esm2_cos = np.clip(E_concat_norm @ E_concat_norm.T, -1.0, 1.0).astype(np.float32)
    S_esm2_rbf = np.exp(-1.2 * np.maximum(0.0, 2.0 - 2.0 * S_esm2_cos)).astype(np.float32)

    # Top-96 SVD coordinates of E_concat_norm
    U, S, _ = np.linalg.svd(E_concat_norm, full_matrices=False)
    V_esm2_96 = (U[:, :96] * S[:96]).astype(np.float32)

    np.savez_compressed(
        out_path,
        model_name=model_name,
        E_mean_norm=E_mean_norm,
        E_pocket_norm=E_pocket_norm,
        E_concat_norm=E_concat_norm,
        S_esm2_mean=S_esm2_mean,
        S_esm2_pocket=S_esm2_pocket,
        S_esm2_cos=S_esm2_cos,
        S_esm2_rbf=S_esm2_rbf,
        V_esm2_96=V_esm2_96,
    )
    print(f"Saved {out_path} in {time.time()-t0:.2f}s (V_esm2_96={V_esm2_96.shape})", flush=True)


if __name__ == "__main__":
    main()
