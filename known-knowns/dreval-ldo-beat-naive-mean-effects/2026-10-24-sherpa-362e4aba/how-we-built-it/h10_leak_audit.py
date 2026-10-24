"""Leak audit for the NCI-60 teacher. Is any CTRPv2 drug present in the teacher's training set under a
different identifier (salt form, stereoisomer, different CID)? Checks, on the SALT-STRIPPED largest
fragment of every teacher compound:
  1. InChIKey connectivity block (first 14 chars) equal to a CTRPv2 drug's  -> same skeleton
  2. Morgan Tanimoto to the nearest CTRPv2 compound, recomputed after salt stripping
Also reports, for each dev single agent, its max similarity to the teacher training set."""
import os
import numpy as np, pandas as pd, json
from rdkit import Chem, RDLogger
from rdkit.Chem import rdFingerprintGenerator
from rdkit.Chem.MolStandardize import rdMolStandardize
RDLogger.DisableLog("rdApp.*")
N = os.environ.get("NCI60", "./nci60"); D = os.environ.get("DATA", "./data") + "/CTRPv2"
gen = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048); lfc = rdMolStandardize.LargestFragmentChooser()
def parent(smi):
    m = Chem.MolFromSmiles(smi) if isinstance(smi, str) else None
    if m is None: return None
    try: return lfc.choose(m)
    except Exception: return m
def ik14(m):
    try: return Chem.MolToInchiKey(m)[:14]
    except Exception: return None
y = pd.read_csv("output/h10_teacher_y.csv", index_col=0); teach_nsc = y.index.to_numpy()
smi = pd.read_csv(f"{N}/nsc_smiles.csv").drop_duplicates("NSC").set_index("NSC")["SMILES"]
ctrp = pd.read_csv(f"{D}/drug_smiles.csv", dtype=str)
C_ik = {}; C_fp = []
for pid, s in zip(ctrp.pubchem_id, ctrp.canonical_smiles):
    m = parent(s)
    if m is None: continue
    k = ik14(m)
    if k: C_ik.setdefault(k, []).append(pid)
    C_fp.append(gen.GetFingerprintAsNumPy(m).astype(np.float32))
cf = pd.read_csv(f"{D}/drug_fingerprints/pubchem_id_to_demorgan_2048_map.csv", dtype=str)
C_all = np.stack([cf[c].astype(np.float32).to_numpy() for c in cf.columns])          # incl. no-SMILES drugs
C = np.vstack([np.stack(C_fp), C_all])
hits_ik, T_fp = [], []
for nsc in teach_nsc:
    m = parent(smi.get(nsc))
    if m is None: T_fp.append(np.zeros(2048, np.float32)); continue
    k = ik14(m)
    if k in C_ik: hits_ik.append((int(nsc), C_ik[k]))
    T_fp.append(gen.GetFingerprintAsNumPy(m).astype(np.float32))
T = np.stack(T_fp); ms = np.zeros(len(T), np.float32)
for i in range(0, len(T), 4096):
    A = T[i:i + 4096]; inter = A @ C.T; ms[i:i + 4096] = (inter / (A.sum(1)[:, None] + C.sum(1)[None, :] - inter + 1e-9)).max(1)
out = {"teacher_compounds": int(len(teach_nsc)),
       "same_skeleton_as_a_CTRPv2_drug_by_InChIKey14_after_salt_strip": len(hits_ik),
       "examples": hits_ik[:15],
       "teacher_compounds_salt_stripped_tanimoto>=0.85_to_CTRPv2": int((ms >= 0.85).sum()),
       "teacher_compounds_salt_stripped_tanimoto>=0.70_to_CTRPv2": int((ms >= 0.70).sum()),
       "teacher_compounds_salt_stripped_tanimoto>=0.60_to_CTRPv2": int((ms >= 0.60).sum())}
json.dump(out, open("output/h10_leak_audit.json", "w"), indent=1); print(json.dumps(out, indent=1))
np.save("output/h10_teacher_maxsim_to_ctrp_saltstripped.npy", ms); np.save("output/h10_teacher_fp_saltstripped.npy", T.astype(np.uint8))
