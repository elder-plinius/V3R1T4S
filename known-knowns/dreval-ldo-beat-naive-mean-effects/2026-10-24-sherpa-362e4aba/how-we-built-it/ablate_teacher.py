"""The ablation pre-committed in H10-PRECOMMIT.md item 5 ("with and without the teacher") and never run.

Uses the frozen core with the external potency prior switched off (tau grid = {0}), on the official
seed-42 splits and on the independent generation. First reproduces the full model to confirm the harness,
then reports the no-prior variant on all drugs, single agents, and novel scaffolds."""
import os, sys
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "3"
import numpy as np, pandas as pd
from sklearn.metrics import r2_score
sys.path.insert(0, "attempts/potency-transfer/code")
from potency_transfer_model import _lookups
from potency_core_fast import PotencyCoreFast, GlobalKernels
from potency_core import tanimoto
from drevalpy.datasets.loader import load_ctrpv2
from drevalpy.models.baselines.naive_pred import NaiveMeanEffectsPredictor
DATA = os.environ.get("DATA", "./data")
FP, PW, T = _lookups(DATA, "CTRPv2"); GK = GlobalKernels(FP, PW, FP.keys())
names = pd.read_csv(f"{DATA}/CTRPv2/drug_names.csv", dtype=str); NM = dict(zip(names.pubchem_id, names.drug_name))
GENS = {"seed42": os.environ.get("RESULTS", "./results") + "/repro_seed42/CTRPv2/LDO/splits",
        "independent": os.environ.get("RESULTS", "./results") + "/indep_seed20261023/CTRPv2/LDO/splits"}
for gen, sp in GENS.items():
    ds = load_ctrpv2(path_data=DATA); ds.remove_nan_responses(); ds.load_splits(path=sp)
    nm = NaiveMeanEffectsPredictor(); CL, DR = nm.load_cell_line_features(DATA, "CTRPv2"), nm.load_drug_features(DATA, "CTRPv2")
    rows = []
    for i, s in enumerate(ds.cv_splits):
        tr = s["train"].copy(); tr.add_rows(s["validation"]); te = s["test"]
        m0 = NaiveMeanEffectsPredictor(); m0.build_model({}); m0.train(output=tr, cell_line_input=CL, drug_input=DR)
        ruler = m0.predict(cell_line_ids=te.cell_line_ids, drug_ids=te.drug_ids, cell_line_input=CL, drug_input=DR)
        full = PotencyCoreFast(GK, T).fit(tr.cell_line_ids, tr.drug_ids, tr.response).predict(te.cell_line_ids, te.drug_ids)
        noT = PotencyCoreFast(GK, T, taus=(0.0,)).fit(tr.cell_line_ids, tr.drug_ids, tr.response).predict(te.cell_line_ids, te.drug_ids)
        ids = te.drug_ids.astype(str)
        combo = np.array(["mol-mol" in NM.get(d, "") for d in ids])
        trd = np.unique(tr.drug_ids.astype(str)); Xtr = np.stack([FP[d] for d in trd])
        ms = {d: float(tanimoto(FP[d][None, :], Xtr).max()) for d in np.unique(ids)}
        novel = np.array([ms[d] < 0.30 for d in ids]) & ~combo
        r = lambda p, msk=None: r2_score((te.response - ruler) if msk is None else (te.response - ruler)[msk],
                                         (p - ruler) if msk is None else (p - ruler)[msk])
        rows.append(dict(split=i, full=r(full), noT=r(noT), noT_singles=r(noT, ~combo),
                         full_singles=r(full, ~combo), noT_novel=r(noT, novel), full_novel=r(full, novel)))
    R = pd.DataFrame(rows); R.to_csv(f"attempts/confirmation/output/ablate_teacher_{gen}.csv", index=False)
    f = lambda c: f"{R[c].mean():+.4f} (SE {R[c].std(ddof=1)/np.sqrt(10):.4f}, {int((R[c]>0).sum())}/10)"
    print(f"\n== {gen}")
    print(f"   WITH prior,    all drugs      {f('full')}")
    print(f"   WITHOUT prior, all drugs      {f('noT')}        <- the pre-committed ablation")
    print(f"   WITH prior,    single agents  {f('full_singles')}")
    print(f"   WITHOUT prior, single agents  {f('noT_singles')}")
    print(f"   WITH prior,    novel scaffold {f('full_novel')}")
    print(f"   WITHOUT prior, novel scaffold {f('noT_novel')}")
