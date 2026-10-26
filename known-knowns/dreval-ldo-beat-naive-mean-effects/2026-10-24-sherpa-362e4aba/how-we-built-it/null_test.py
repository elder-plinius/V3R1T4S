"""Pre-registered null test (PREREG.md s6, made concrete in PREREG.v4 s4).
400 random permutations of the 545-drug universe; in each, every drug's fingerprint, pathway set and
NCI-60 teacher value are taken from another drug, consistently in training and test. Seed-42 splits as
saved by the drevalpy pipeline; train on train+validation (as the pipeline does for its final model);
normalized R^2 against the NaiveMeanEffectsPredictor trained on the same data. Control index -1 is the
unpermuted model, recomputed through this same code as a cross-check against the pipeline's value.
usage: null_test.py <n_controls> <workers>"""
import os, sys
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "1"
import numpy as np, pandas as pd, multiprocessing as mp, time, json
from sklearn.metrics import r2_score
sys.path.insert(0, os.environ.get("PKG", ".") + "/how-we-built-it")
from potency_transfer_model import _lookups
from potency_core_fast import PotencyCoreFast, GlobalKernels
from drevalpy.datasets.loader import load_ctrpv2
from drevalpy.models.baselines.naive_pred import NaiveMeanEffectsPredictor
DATA = os.environ.get("DATA", "./data")
ds = load_ctrpv2(path_data=DATA); ds.remove_nan_responses()
ds.load_splits(path=os.environ.get("RESULTS", "./results") + "/repro_seed42/CTRPv2/LDO/splits")
FP, PW, T = _lookups(DATA, "CTRPv2"); GK = GlobalKernels(FP, PW, FP.keys())
nm = NaiveMeanEffectsPredictor(); CL, DR = nm.load_cell_line_features(DATA, "CTRPv2"), nm.load_drug_features(DATA, "CTRPv2")
SPL = []
for s in ds.cv_splits:
    tr = s["train"].copy() if hasattr(s["train"], "copy") else s["train"]; tr.add_rows(s["validation"]); te = s["test"]
    m = NaiveMeanEffectsPredictor(); m.build_model({}); m.train(output=tr, cell_line_input=CL, drug_input=DR)
    SPL.append((tr, te, m.predict(cell_line_ids=te.cell_line_ids, drug_ids=te.drug_ids, cell_line_input=CL, drug_input=DR)))
def run(k):
    perm = None if k < 0 else np.random.default_rng(1_000_000 + k).permutation(len(GK.ids))
    vals = []
    for tr, te, nme in SPL:
        core = PotencyCoreFast(GK, T, perm=perm).fit(tr.cell_line_ids, tr.drug_ids, tr.response)
        p = core.predict(te.cell_line_ids, te.drug_ids); vals.append(r2_score(te.response - nme, p - nme))
    return k, float(np.mean(vals)), vals
if __name__ == "__main__":
    n, workers = int(sys.argv[1]), int(sys.argv[2]); t0 = time.time()
    with mp.get_context("fork").Pool(workers) as pool: res = pool.map(run, [-1] + list(range(n)), chunksize=1)
    real = [r for r in res if r[0] == -1][0]; ctrl = np.array([r[1] for r in res if r[0] >= 0])
    pd.DataFrame([dict(control=k, mean_normR2=m, **{f"split{i}": v for i, v in enumerate(vs)}) for k, m, vs in res]).to_csv(
        os.environ.get("OUT", "./output") + "/null_results.csv", index=False)
    out = dict(controls=int(len(ctrl)), best_control=float(ctrl.max()), mean_control=float(ctrl.mean()),
               sd_control=float(ctrl.std(ddof=1)), real=real[1], real_per_split=real[2],
               real_beats_all_controls=bool(real[1] > ctrl.max()), seconds=round(time.time() - t0))
    json.dump(out, open(os.environ.get("OUT", "./output") + "/null_summary.json", "w"), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "real_per_split"}, indent=1))
