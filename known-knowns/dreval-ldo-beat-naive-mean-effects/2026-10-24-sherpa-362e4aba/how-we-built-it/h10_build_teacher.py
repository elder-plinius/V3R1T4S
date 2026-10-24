"""H10 teacher, per H10-PRECOMMIT.md. Builds per-compound NCI-60 mean log10 GI50 at a single standard
top concentration, excludes every CTRPv2 compound (by PubChem CID) and every NCI-60 compound with
Tanimoto >= 0.85 to any CTRPv2 compound, and writes the cleaned table plus exclusion counts."""
import os
import numpy as np, pandas as pd, time, json
from rdkit import Chem, RDLogger
from rdkit.Chem import rdFingerprintGenerator
RDLogger.DisableLog("rdApp.*")
N = os.environ.get("NCI60", "./nci60"); D = os.environ.get("DATA", "./data") + "/CTRPv2"; OUT = "output"
t0 = time.time(); log = {}
g = pd.read_csv(f"{N}/GI50.csv", usecols=["NSC", "CONCENTRATION_UNIT", "LOG_HI_CONCENTRATION", "AVERAGE"], low_memory=False)
log["rows_total"] = len(g); g = g[g.CONCENTRATION_UNIT == "M"]; log["rows_molar"] = len(g)
hi = float(g.LOG_HI_CONCENTRATION.round(4).mode().iloc[0]); log["standard_log_hi_conc"] = hi
g = g[g.LOG_HI_CONCENTRATION.round(4) == hi]; log["rows_standard_hi"] = len(g)
y = g.groupby("NSC")["AVERAGE"].mean(); n = g.groupby("NSC").size()
y = y[n >= 30]; log["nsc_with_>=30_cell_measurements"] = len(y)       # a panel mean needs a panel
smi = pd.read_csv(f"{N}/nsc_smiles.csv").drop_duplicates("NSC").set_index("NSC")["SMILES"]
cid = pd.read_csv(f"{N}/nsc_sid_cid.csv").dropna(subset=["CID"])
ctrp = pd.read_csv(f"{D}/drug_names.csv", dtype=str); ctrp_ids = set(ctrp.pubchem_id)
bad_cid = set(cid[cid.CID.astype("Int64").astype(str).isin(ctrp_ids)].NSC)
log["nsc_excluded_by_ctrp_cid"] = len(set(y.index) & bad_cid)
y = y[~y.index.isin(bad_cid)]
gen = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)
fps, keep = [], []
for nsc in y.index:
    s = smi.get(nsc)
    m = Chem.MolFromSmiles(s) if isinstance(s, str) else None
    if m is None: continue
    fps.append(gen.GetFingerprintAsNumPy(m).astype(np.uint8)); keep.append(nsc)
X = np.stack(fps); y = y.loc[keep]; log["nsc_with_valid_smiles"] = len(y)
cf = pd.read_csv(f"{D}/drug_fingerprints/pubchem_id_to_demorgan_2048_map.csv", dtype=str)
C = np.stack([cf[c].astype(np.uint8).to_numpy() for c in cf.columns]).astype(np.float32)
Xf = X.astype(np.float32); maxsim = np.zeros(len(Xf), np.float32)
for i in range(0, len(Xf), 4096):
    A = Xf[i:i + 4096]; inter = A @ C.T
    sim = inter / (A.sum(1)[:, None] + C.sum(1)[None, :] - inter + 1e-9); maxsim[i:i + 4096] = sim.max(1)
near = maxsim >= 0.85; log["nsc_excluded_tanimoto>=0.85"] = int(near.sum())
X, y = X[~near], y[~near]; log["teacher_training_compounds"] = len(y)
log["teacher_target_mean_logGI50"] = float(y.mean()); log["teacher_target_sd"] = float(y.std())
np.save(f"{OUT}/h10_teacher_X.npy", X); y.to_csv(f"{OUT}/h10_teacher_y.csv")
log["seconds"] = round(time.time() - t0)
json.dump(log, open(f"{OUT}/h10_teacher_build.json", "w"), indent=1); print(json.dumps(log, indent=1))
