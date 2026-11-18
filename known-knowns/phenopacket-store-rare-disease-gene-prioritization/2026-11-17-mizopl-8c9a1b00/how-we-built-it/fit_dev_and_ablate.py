#!/usr/bin/env python3
"""
Reference implementation of the 5-fold gene-grouped cross-validation weight-fitting procedure
and `l2_reg` sensitivity grid (`{0.0, 0.02, 0.03, 0.08, 0.20}` + uniform `1/6` baseline)
evaluated on `P2-Dev` (`1,132` cases across `112` even-indexed corpus-only unannotated genes).
"""
from __future__ import annotations

import sys
from pathlib import Path
import numpy as np
from scipy import optimize

sys.dont_write_bytecode = True


def fit_simplex_weights_5fold_gene_cv(
    f_tgts: list[np.ndarray],
    F_comps: list[np.ndarray],
    case_folds: np.ndarray,
    case_gene_weights: np.ndarray,
    l2_reg: float = 0.03,
) -> tuple[np.ndarray, list[np.ndarray]]:
    """
    Fits `w in Delta_6` via L2-regularized smooth reciprocal-rank optimization across 5
    gene-disjoint folds on `P2-Dev` (`temp = 0.18`, `l2_reg = 0.03` toward uniform `1/6`).
    """
    u6 = np.full(6, 1.0 / 6.0, dtype=np.float64)
    fold_weights: list[np.ndarray] = []
    n_cases = len(f_tgts)
    for fold in range(5):
        train_ix = [i for i in range(n_cases) if int(case_folds[i]) != fold]
        w_tr = case_gene_weights[train_ix]
        w_tr = w_tr / w_tr.sum()

        def loss_fn(theta: np.ndarray) -> float:
            ex = np.exp(theta - theta.max())
            w = ex / ex.sum()
            obj = 0.0
            for kl, ci in enumerate(train_ix):
                st = float(w @ f_tgts[ci])
                sc_c = w @ F_comps[ci]
                diff = np.clip((sc_c - st) / 0.18, -40.0, 40.0)
                soft_rk = 1.0 + float(np.sum(1.0 / (1.0 + np.exp(-diff))))
                obj += w_tr[kl] * (1.0 / soft_rk)
            return -(obj - l2_reg * float(np.sum((w - u6) ** 2)))

        res = optimize.minimize(loss_fn, np.zeros(6), method="BFGS", options={"maxiter": 80, "gtol": 1e-5})
        ex = np.exp(res.x - res.x.max())
        fold_weights.append(ex / ex.sum())

    w_frozen = np.mean(np.vstack(fold_weights), axis=0)
    w_frozen /= w_frozen.sum()
    return w_frozen, fold_weights


if __name__ == "__main__":
    here = Path(__file__).resolve().parent.parent
    print("Standalone pre-corpus ranker module:", here)
