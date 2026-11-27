"""Reproduce MBM's test RMSEs (PREREG baseline) from its shipped XGBoost JSON with an own numpy tree walker.

Usage: python3 -I -B code/xgb_json_walk.py <path to custom_loss_best_model.json> [optional .npy path for test monthly predictions]
"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mbdata, score


def predict(model, X):
    L = model["learner"]
    base = float(L["learner_model_param"]["base_score"])
    X = X.astype(np.float32)
    out = np.full(len(X), base, dtype=np.float64)
    for t in L["gradient_booster"]["model"]["trees"]:
        left = np.array(t["left_children"]); right = np.array(t["right_children"])
        feat = np.array(t["split_indices"]); cond = np.array(t["split_conditions"], dtype=np.float32)
        dl = np.array(t["default_left"], dtype=bool)
        node = np.zeros(len(X), dtype=np.int64)
        while True:
            internal = left[node] != -1
            if not internal.any():
                break
            n = node[internal]
            x = X[np.nonzero(internal)[0], feat[n]]
            go_left = np.where(np.isnan(x), dl[n], x < cond[n])
            node[internal] = np.where(go_left, left[n], right[n])
        out += cond[node].astype(np.float64)  # leaf value is stored in split_conditions
    return out


if __name__ == "__main__":
    model = json.load(open(sys.argv[1]))
    te = mbdata.load("test")
    p = predict(model, te["X"])
    r = score.rmse_by_season(te["gid"], p, te["balance"], te["n_months"], check_counts=True)
    print("MBM shipped model on test:", {k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()})
    print("2-decimal: Ba %.2f Bw %.2f Bs %.2f" % (r["Ba"], r["Bw"], r["Bs"]))
    if len(sys.argv) > 2:
        np.save(sys.argv[2], p)
