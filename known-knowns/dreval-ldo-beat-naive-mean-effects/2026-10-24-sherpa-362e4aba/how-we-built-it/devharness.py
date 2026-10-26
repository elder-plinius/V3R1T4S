"""Development harness. DEVELOPMENT DATA ONLY: the 82 vault drugs are removed before anything
else, splits use development seed 7 (never 42 or 20261023), October-2025 data, drevalpy 1.3.5.

It reproduces drevalpy's LDO protocol for scoring: train on train+validation of each split, predict
the split's test drugs, and compute normalized R^2 exactly as
drevalpy.visualization.utils._normalize_metrics_by_mean_effects does -- subtract the
NaiveMeanEffectsPredictor (trained on the same training data) from truth and prediction, then
sklearn r2_score globally over the split's test pairs.
"""
import os
import numpy as np, pandas as pd
from sklearn.metrics import r2_score
from drevalpy.datasets.loader import load_ctrpv2
from drevalpy.datasets.dataset import DrugResponseDataset
from drevalpy.models.baselines.naive_pred import NaiveMeanEffectsPredictor

DATA = os.environ.get("DATA", "./data")
RUN = os.environ.get("PKG", ".")
DEV_SEED = 7


def load_dev():
    vault = [l for l in open(f"{RUN}/data/vault_drugs.txt").read().splitlines() if l]
    assert len(vault) == 82
    ds = load_ctrpv2(path_data=DATA)
    keep = ~np.isnan(ds.response) & ~np.isin(ds.drug_ids.astype(str), vault)
    dev = DrugResponseDataset(response=ds.response[keep], cell_line_ids=ds.cell_line_ids[keep],
                              drug_ids=ds.drug_ids[keep], tissues=ds.tissue[keep], dataset_name="CTRPv2")
    assert len(np.unique(dev.drug_ids)) == 545 - 82
    return dev


def dev_splits(dev, seed=DEV_SEED):
    sp = dev.split_dataset(n_cv_splits=10, mode="LDO", split_validation=True,
                           split_early_stopping=True, validation_ratio=0.1, random_state=seed)
    out = []
    for s in sp:
        tr = s["train"]; tr.add_rows(s["validation"])
        te = s["test"]
        assert not set(tr.drug_ids) & set(te.drug_ids)
        out.append((tr, te))
    return out


_NME_IO = None


def nme_predict(tr, te):
    global _NME_IO
    if _NME_IO is None:
        m0 = NaiveMeanEffectsPredictor()
        _NME_IO = (m0.load_cell_line_features(DATA, "CTRPv2"), m0.load_drug_features(DATA, "CTRPv2"))
    cl, dr = _NME_IO
    m = NaiveMeanEffectsPredictor(); m.build_model({})
    m.train(output=tr, cell_line_input=cl, drug_input=dr)
    return m.predict(cell_line_ids=te.cell_line_ids, drug_ids=te.drug_ids, cell_line_input=cl, drug_input=dr)


def normalized_r2(y, pred, nme):
    return r2_score(y - nme, pred - nme)


def load_fingerprints(nbits=2048):
    fp = pd.read_csv(f"{DATA}/CTRPv2/drug_fingerprints/pubchem_id_to_demorgan_{nbits}_map.csv", dtype=str)
    return {c: fp[c].astype(np.uint8).to_numpy() for c in fp.columns}


def drug_names():
    d = pd.read_csv(f"{DATA}/CTRPv2/drug_names.csv", dtype=str)
    return dict(zip(d.pubchem_id, d.drug_name))
