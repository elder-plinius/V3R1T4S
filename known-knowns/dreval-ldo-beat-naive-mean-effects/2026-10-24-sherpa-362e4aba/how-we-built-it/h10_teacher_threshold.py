"""Retrain the NCI-60 teacher under a salt-stripped exclusion threshold, write CTRPv2 predictions.
usage: h10_teacher_threshold.py <tanimoto_threshold>"""
import os
import sys, json, numpy as np, pandas as pd, torch
thr = float(sys.argv[1])
X = np.load("output/h10_teacher_X.npy").astype(np.float32)
y = pd.read_csv("output/h10_teacher_y.csv", index_col=0).iloc[:, 0].to_numpy(np.float32)
ms = np.load("output/h10_teacher_maxsim_to_ctrp_saltstripped.npy")
skel = {373989, 721951, 757444}
nsc = pd.read_csv("output/h10_teacher_y.csv", index_col=0).index.to_numpy()
keep = (ms < thr) & ~np.isin(nsc, list(skel))
X, y = X[keep], y[keep]
dev = "cuda"; torch.manual_seed(0); np.random.seed(0)
m = torch.nn.Sequential(torch.nn.Linear(2048, 1024), torch.nn.ReLU(), torch.nn.Dropout(0.3),
                        torch.nn.Linear(1024, 256), torch.nn.ReLU(), torch.nn.Dropout(0.3), torch.nn.Linear(256, 1)).to(dev)
opt = torch.optim.AdamW(m.parameters(), 1e-3, weight_decay=1e-4)
Xt, yt = torch.tensor(X, device=dev), torch.tensor(y, device=dev); mu = yt.mean()
for ep in range(25):
    m.train(); perm = torch.randperm(len(Xt), device=dev)
    for i in range(0, len(Xt), 256):
        b = perm[i:i + 256]; opt.zero_grad(); ((m(Xt[b]).squeeze(1) - (yt[b] - mu)) ** 2).mean().backward(); opt.step()
m.eval()
cf = pd.read_csv(os.environ.get("DATA", "./data") + "/CTRPv2/drug_fingerprints/pubchem_id_to_demorgan_2048_map.csv", dtype=str)
C = torch.tensor(np.stack([cf[c].astype(np.float32).to_numpy() for c in cf.columns]), device=dev)
with torch.no_grad(): p = (m(C).squeeze(1) + mu).cpu().numpy()
tag = f"{thr:.2f}"
pd.Series(p, index=cf.columns, name="teacher_logGI50").to_csv(f"output/h10_teacher_pred_ctrp_thr{tag}.csv")
torch.save(m.state_dict(), f"output/h10_teacher_thr{tag}.pt")
json.dump({"threshold": thr, "teacher_compounds": int(keep.sum()), "removed": int((~keep).sum())}, open(f"output/h10_teacher_thr{tag}.json", "w"))
print(f"threshold {tag}: teacher trained on {int(keep.sum())} compounds ({int((~keep).sum())} removed)")
