"""DEV evaluation on 2023-24 only (PREREG development protocol). For one configuration: as-of forecasts for every 2023-24
hub-ensemble origin date, scored against the final truth (PREREG R4/R5) on the hub-ensemble's tasks (real-time file where
a RETRO and a real-time file share an origin), horizons 0..4. Prints the selection statistic (ratio of mean WIS ours /
hub-ensemble) and diagnostics. usage: python dev_eval.py <name> '<json params>'"""
import os, sys, json, time
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "evaluator", "code"))
import model_rsv as M  # noqa: E402
from score import load_truth, score_wide, LEVS  # noqa: E402

RUN = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
WORK = os.path.join(RUN, "attempts", "forecaster", "work")
HUB = os.path.join(RUN, "attempts", "evaluator", "work", "hub_scores_2023-24.csv.gz")


def ensemble_tasks():
    H = pd.read_csv(HUB, dtype={"location": str})
    E = H[(H.model_id == "hub-ensemble") & (H.horizon.between(0, 4))]
    # real-time file wins where both exist
    rt = set(E[~E.retro].origin_date)
    E = E[~((E.retro) & (E.origin_date.isin(rt)))]
    return H, E


def run(name, params):
    H, E = ensemble_tasks()
    origins = sorted(E.origin_date.unique())
    t0 = time.time()
    fc = []
    for O in origins:
        df, info = M.forecast(O, params)
        fc.append(df)
    F = pd.concat(fc, ignore_index=True)
    F["lev"] = F.output_type_id.round(4)
    W = F.pivot_table(index=["origin_date", "horizon", "location", "age_group", "target_end_date"], columns="lev",
                      values="value").reset_index()
    W.columns = [c if not isinstance(c, float) else round(c, 4) for c in W.columns]
    S = score_wide(W, load_truth())
    k = ["origin_date", "horizon", "location", "age_group"]
    J = E[k + ["wis"]].merge(S[k + ["wis", "cov50", "cov90"]], on=k, suffixes=("_ens", "_ours"), how="left")
    miss = int(J.wis_ours.isna().sum())
    J = J.dropna(subset=["wis_ours"])
    res = dict(name=name, params=params, n=len(J), missing=miss, ens=J.wis_ens.mean(), ours=J.wis_ours.mean(),
               ratio=J.wis_ours.mean() / J.wis_ens.mean(), cov50=J.cov50.mean(), cov90=J.cov90.mean(), secs=time.time() - t0)
    for lab, m in [("all0130", J.age_group == "0-130"), ("ped", J.age_group.isin(["0-0.99", "1-4"])),
                   ("US0130", (J.location == "US") & (J.age_group == "0-130")), ("states", J.location != "US")]:
        res["r_" + lab] = J[m].wis_ours.mean() / J[m].wis_ens.mean()
    # ratio vs each individual model on that model's tasks (horizons 0..4)
    Hm = H[(H.model_id != "hub-ensemble") & (H.horizon.between(0, 4))]
    for mid, g in Hm.groupby("model_id"):
        rt = set(g[~g.retro].origin_date)
        g = g[~((g.retro) & (g.origin_date.isin(rt)))]
        jj = g[k + ["wis"]].merge(S[k + ["wis"]], on=k, suffixes=("_m", "_o"))
        res["vs_" + mid] = jj.wis_o.mean() / jj.wis_m.mean()
    os.makedirs(os.path.join(WORK, "dev"), exist_ok=True)
    J.to_csv(os.path.join(WORK, "dev", name + "_tasks.csv.gz"), index=False)
    with open(os.path.join(WORK, "dev", "dev_results.jsonl"), "a") as f:
        f.write(json.dumps(res, default=float) + "\n")
    print(json.dumps({k2: (round(v, 4) if isinstance(v, float) else v) for k2, v in res.items()}, default=float))


if __name__ == "__main__":
    run(sys.argv[1], json.loads(sys.argv[2]) if len(sys.argv) > 2 else {})
