"""Independent scorer (PREREG.md statistic): point prediction = sum of monthly predictions per id; RMSE per season."""
import numpy as np

SEASONS = {"Ba": 12, "Bw": 7, "Bs": 5}
EXPECTED_N = {"Ba": 1065, "Bw": 999, "Bs": 1028}


def aggregate(gid, monthly_pred, balance, n_months):
    uid, inv = np.unique(gid, return_inverse=True)
    pred = np.bincount(inv, weights=monthly_pred, minlength=len(uid))
    obs = np.bincount(inv, weights=balance, minlength=len(uid)) / np.bincount(inv, minlength=len(uid))
    nm = np.zeros(len(uid), int); nm[inv] = n_months
    return uid, pred, obs, nm


def rmse_by_season(gid, monthly_pred, balance, n_months, check_counts=False):
    uid, pred, obs, nm = aggregate(gid, monthly_pred, balance, n_months)
    out = {}
    for s, m in SEASONS.items():
        k = nm == m
        if check_counts:
            assert k.sum() == EXPECTED_N[s], (s, int(k.sum()))
        out[s] = float(np.sqrt(np.mean((pred[k] - obs[k]) ** 2)))
        out["n_" + s] = int(k.sum())
    return out
