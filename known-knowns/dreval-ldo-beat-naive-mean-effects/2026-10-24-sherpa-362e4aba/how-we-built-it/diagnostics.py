"""Pre-declared diagnostics (PREREG.v4 s5) on a confirmatory run, from drevalpy's own true_vs_pred.
Normalization replicates drevalpy.visualization.utils._normalize_metrics_by_mean_effects exactly
(left merge with the baseline on drug, cell line, CV split, then sklearn r2 per split), and is first
checked to reproduce drevalpy's full-set value before any subset is scored.
usage: diagnostics.py <eval_dir> <splits_dir> <model> [<model> ...]"""
import os
import sys, json, numpy as np, pandas as pd
from sklearn.metrics import r2_score
from scipy.stats import pearsonr
ev_dir, sp_dir, models = sys.argv[1], sys.argv[2], sys.argv[3:]
t = pd.read_csv(f"{ev_dir}/true_vs_pred.csv", low_memory=False); t["drug_name"] = t["drug_name"].astype(str)
t = t[(t.test_mode == "LDO") & (t.rand_setting == "predictions")]
names = pd.read_csv(os.environ.get("DATA", "./data") + "/CTRPv2/drug_names.csv", dtype=str); NM = dict(zip(names.pubchem_id, names.drug_name))
assert names.drug_name.is_unique and names.pubchem_id.is_unique, "drug names/ids not one-to-one"
N2I = dict(zip(names.drug_name, names.pubchem_id))
# drevalpy's true_vs_pred labels drugs by NAME; translate to pubchem_id once, and check nothing is lost
t["drug_name"] = t["drug_name"].map(N2I)
assert t["drug_name"].notna().all(), "a drug name in true_vs_pred has no pubchem_id"
vault = set(l for l in open("data/vault_drugs.txt").read().splitlines() if l)
contam = set(l for l in open("data/vault_contaminated.txt").read().splitlines() if l)
fp = pd.read_csv(os.environ.get("DATA", "./data") + "/CTRPv2/drug_fingerprints/pubchem_id_to_demorgan_2048_map.csv", dtype=str)
FP = {c: fp[c].astype(np.float32).to_numpy() for c in fp.columns}
def tani(A, B):
    inter = A @ B.T; return inter / (A.sum(1)[:, None] + B.sum(1)[None, :] - inter + 1e-9)
nme = t[t.algorithm == "NaiveMeanEffectsPredictor"][["drug_name", "cell_line_name", "CV_split", "y_pred"]].rename(columns={"y_pred": "y_nme"})
def norm_r2(alg, mask_fn=None):
    s = t[t.algorithm == alg][["drug_name", "cell_line_name", "CV_split", "y_true", "y_pred"]].merge(nme, on=["drug_name", "cell_line_name", "CV_split"], how="left")
    if mask_fn is not None: s = s[mask_fn(s)]
    vals = [r2_score(g.y_true - g.y_nme, g.y_pred - g.y_nme) for _, g in s.groupby("CV_split") if len(g) > 1]
    return float(np.mean(vals)), float(np.std(vals, ddof=1) / np.sqrt(len(vals))), len(vals)
out = {}
is_combo = lambda s: s.drug_name.map(lambda d: "mol-mol" in NM.get(d, ""))
for alg in models + ["NaiveMeanEffectsPredictor"]:
    full = norm_r2(alg)
    n_v = t[(t.algorithm == alg) & t.drug_name.isin(vault)].drug_name.nunique()
    assert n_v == 82, f"{alg}: only {n_v} vault drugs found in predictions"
    out[alg] = {"all_drugs": full,
                "single_agents": norm_r2(alg, lambda s: ~is_combo(s)),
                "combinations_only": norm_r2(alg, is_combo),
                "vault_all_82": norm_r2(alg, lambda s: s.drug_name.isin(vault)),
                "vault_74_never_exposed": norm_r2(alg, lambda s: s.drug_name.isin(vault - contam))}
for alg in models:
    s = t[t.algorithm == alg].merge(nme, on=["drug_name", "cell_line_name", "CV_split"], how="left")
    s["r"] = s.y_true - s.y_nme; s["p"] = s.y_pred - s.y_nme
    rows = []
    for sp, g in s.groupby("CV_split"):
        trd = pd.read_csv(f"{sp_dir}/cv_split_{int(sp)}_train.csv", dtype=str)["pubchem_id"].unique()
        vad = pd.read_csv(f"{sp_dir}/cv_split_{int(sp)}_validation.csv", dtype=str)["pubchem_id"].unique()
        Xtr = np.stack([FP[d] for d in set(trd) | set(vad)])
        d = g.groupby("drug_name").agg(true=("r", "mean"), pred=("p", "mean"))
        d["maxsim"] = tani(np.stack([FP[x] for x in d.index]), Xtr).max(1); d["combo"] = [("mol-mol" in NM.get(x, "")) for x in d.index]
        rows.append(d)
    D = pd.concat(rows); single = D[~D.combo]; bins = {}
    for lo, hi in ((0, .3), (.3, .45), (.45, .6), (.6, 1.01)):
        b = single[(single.maxsim >= lo) & (single.maxsim < hi)]
        bins[f"singles maxsim [{lo:.2f},{hi:.2f})"] = (int(len(b)), float(pearsonr(b.pred, b.true)[0]) if len(b) > 4 else None)
    out[alg]["drug_level_potency_r"] = {"all": float(pearsonr(D.pred, D.true)[0]), "singles": float(pearsonr(single.pred, single.true)[0]), **bins}
json.dump(out, open(f"{ev_dir}/diagnostics.json", "w"), indent=1)
for alg, o in out.items():
    print(f"== {alg}")
    for k, v in o.items():
        if k != "drug_level_potency_r": print(f"   {k:24s} normR2 {v[0]:+.4f} (SE {v[1]:.4f}, {v[2]} splits)")
    if "drug_level_potency_r" in o:
        for k, v in o["drug_level_potency_r"].items(): print(f"   drug-level r  {k:30s} {v}")
