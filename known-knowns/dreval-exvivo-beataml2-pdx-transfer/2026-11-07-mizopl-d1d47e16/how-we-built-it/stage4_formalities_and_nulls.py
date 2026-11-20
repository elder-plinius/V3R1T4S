#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stage 4: Pre-registered B=500 residual permutation null tests (`seed = 20261107`)
for `dreval-exvivo-beataml2-pdx-transfer` (`BeatAML2` and `PDX_Bruna`).
"""
import os
import numpy as np
import pandas as pd
from scipy.stats import pearsonr

DATA_DIR = os.environ.get("DREVAL_DATA_DIR", "DREVAL_CAMPAIGN/data")
PRED_DIR = os.environ.get("DREVAL_PRED_DIR", "DREVAL_CAMPAIGN/predictions/cross_study")


def run_null_test(cohort: str, n_controls: int = 500, seed: int = 20261107) -> dict:
    df = pd.read_csv(f"{PRED_DIR}/{cohort}/cross_study_{cohort}_split_0.csv")
    yt = df["response"].values
    yn = np.round(df["predictions_naive"].values, 4)
    ys = np.round(df["predictions"].values, 4)
    yt_res = yt - yn
    yp_res = ys - yn
    real_p = float(pearsonr(yt_res, yp_res)[0])
    rng = np.random.default_rng(seed)
    nulls = np.array([float(pearsonr(rng.permutation(yt_res), yp_res)[0]) for _ in range(n_controls)])
    return {
        "cohort": cohort,
        "n_rows": int(len(yt)),
        "controls": n_controls,
        "observed_Pearson_norm": round(real_p, 6),
        "null_mean": round(float(nulls.mean()), 6),
        "null_std": round(float(nulls.std(ddof=1)), 6),
        "best_control": round(float(nulls.max()), 6),
        "z_score": round(float((real_p - nulls.mean()) / nulls.std(ddof=1)), 2),
        "controls_beaten": int(np.sum(real_p > nulls)),
    }


if __name__ == "__main__":
    for c in ("BeatAML2", "PDX_Bruna"):
        print(run_null_test(c))
