#!/usr/bin/env python3
"""
Step 2: Strictly train_val-only (2013-2018) inner temporal split anatomy.
Never touches `test`. Analyzes:
  1. Inner temporal split A: 2013-2016 -> 2017-2018
  2. Inner temporal split B: 2013-2017 -> 2018
  3. Official Seed 1 split: train -> valid (how PyTDC splits train_val)
Checks exact (Drug, Target) repeat correlation, per-Target mean baseline,
per-Drug mean baseline, and how PyTDC's default split is constructed.
"""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import pearsonr
from tdc.benchmark_group import dti_dg_group

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


def analyze_split(name: str, tr: pd.DataFrame, va: pd.DataFrame):
    print(f"\n================ {name} ================")
    print(f"tr rows: {len(tr)}, va rows: {len(va)}")
    tr_targets = set(tr["Target"])
    va_targets = set(va["Target"])
    tr_drugs = set(tr["Drug"])
    va_drugs = set(va["Drug"])
    tr_pairs = set(zip(tr["Drug"], tr["Target"]))

    seen_t = va["Target"].isin(tr_targets)
    seen_d = va["Drug"].isin(tr_drugs)
    exact_p = pd.Series([ (d, t) in tr_pairs for d, t in zip(va["Drug"], va["Target"]) ], index=va.index)

    print(f"va seen_target:   {seen_t.sum():6d} / {len(va)} ({100*seen_t.mean():.2f}%)")
    print(f"va unseen_target: {(~seen_t).sum():6d} / {len(va)} ({100*(~seen_t).mean():.2f}%) [unique unseen targets: {len(va_targets - tr_targets)}]")
    print(f"va seen_drug:     {seen_d.sum():6d} / {len(va)} ({100*seen_d.mean():.2f}%)")
    print(f"va exact_pair:    {exact_p.sum():6d} / {len(va)} ({100*exact_p.mean():.2f}%)")

    # Simple baselines on va:
    global_mean = tr["Y"].mean()
    t_mean = tr.groupby("Target")["Y"].mean()
    t_cnt = tr.groupby("Target")["Y"].count()
    d_mean = tr.groupby("Drug")["Y"].mean()
    p_mean = tr.groupby(["Drug", "Target"])["Y"].mean()

    # Smoothed target mean
    for m_smooth in [1.0, 5.0, 10.0, 20.0]:
        t_smooth = (t_mean * t_cnt + global_mean * m_smooth) / (t_cnt + m_smooth)
        pred_t = va["Target"].map(t_smooth).fillna(global_mean).values
        r_t, _ = pearsonr(pred_t, va["Y"].values)
        print(f"  Baseline [Smoothed Target Mean m={m_smooth:4.1f}] PCC = {r_t:.5f}")

    # Drug + Target additive baseline
    t_smooth = (t_mean * t_cnt + global_mean * 10.0) / (t_cnt + 10.0)
    tr_resid = tr["Y"] - tr["Target"].map(t_smooth)
    d_resid_mean = tr_resid.groupby(tr["Drug"]).mean()
    d_cnt = tr.groupby("Drug")["Y"].count()
    d_resid_smooth = (d_resid_mean * d_cnt) / (d_cnt + 2.0)

    pred_dt = va["Target"].map(t_smooth).fillna(global_mean) + va["Drug"].map(d_resid_smooth).fillna(0.0)
    r_dt, _ = pearsonr(pred_dt.values, va["Y"].values)
    print(f"  Baseline [Target + Drug Residual]         PCC = {r_dt:.5f}")

    # If exact pair exists in tr, what is the correlation on exact_pair subset?
    if exact_p.sum() > 10:
        va_ep = va[exact_p]
        ep_preds = [p_mean[(d, t)] for d, t in zip(va_ep["Drug"], va_ep["Target"])]
        r_ep, _ = pearsonr(ep_preds, va_ep["Y"].values)
        print(f"  On exact_pair subset (n={len(va_ep)}): exact pair tr mean PCC = {r_ep:.5f}")
        pred_dt_ep = pred_dt.copy()
        pred_dt_ep.loc[exact_p] = 0.7 * np.array(ep_preds) + 0.3 * pred_dt.loc[exact_p].values
        r_dtep, _ = pearsonr(pred_dt_ep.values, va["Y"].values)
        print(f"  Baseline [Target + Drug + ExactPair]      PCC = {r_dtep:.5f}")


def main():
    group = dti_dg_group(path=str(DATA_DIR))
    bm = group.get("BindingDB_Patent")
    tv = bm["train_val"]

    # Check Target_ID vs Target (1-to-1?) and Drug_ID vs Drug
    print("Unique Target_ID:", tv["Target_ID"].nunique(), "Unique Target seq:", tv["Target"].nunique())
    print("Unique Drug_ID:  ", tv["Drug_ID"].nunique(), "Unique Drug SMILES:", tv["Drug"].nunique())

    # Split A: 2013-2016 -> 2017-2018
    analyze_split("Inner Temporal A (2013-2016 -> 2017-2018)", tv[tv["Year"] <= 2016], tv[tv["Year"] >= 2017])

    # Split B: 2013-2017 -> 2018
    analyze_split("Inner Temporal B (2013-2017 -> 2018)", tv[tv["Year"] <= 2017], tv[tv["Year"] == 2018])

    # Official Seed 1 split
    tr1, va1 = group.get_train_valid_split(benchmark=bm["name"], split_type="default", seed=1)
    analyze_split("Official Seed 1 Split (train -> valid)", tr1, va1)


if __name__ == "__main__":
    main()
