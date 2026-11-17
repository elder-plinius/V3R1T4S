"""Baseline record (kit step 3c) on the DEV season 2023-24 only: season-average WIS of every submitted model and of the
hub-ensemble, recomputed by our scorer (pinball and interval forms), plus a check that each hub-ensemble file equals the
mean of its members' quantiles. usage: python baseline_dev.py <season> (default 2023-24)."""
import os, sys
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from parse_mo import load_all, quantile_wide  # noqa: E402
from score import load_truth, score_wide, LEVS  # noqa: E402
from wis import LEVELS  # noqa: E402

SEASONS = {"2023-24": ("2023-10-01", "2024-07-31"), "2024-25": ("2024-10-01", "2025-07-31")}

if __name__ == "__main__":
    season = sys.argv[1] if len(sys.argv) > 1 else "2023-24"
    a, b = SEASONS[season]
    d = load_all()
    d = d[(d.origin_date >= a) & (d.origin_date <= b)]
    W, ndrop = quantile_wide(d, LEVELS)
    print("season", season, "wide tasks", len(W), "dropped incomplete", ndrop)
    T = load_truth()
    S = score_wide(W, T)
    print("max |pinball - interval| over all scored hub tasks:", float(np.max(np.abs(S.wis - S.wis_int))))
    rows = []
    for (m, r), g in S.groupby(["model_id", "retro"]):
        rows.append(dict(model=m, retro=r, origins=g.origin_date.nunique(), scored_tasks=len(g),
                         ages=",".join(sorted(g.age_group.unique())), mean_wis=g.wis.mean(), mean_ae=g.ae.mean(),
                         cov50=g.cov50.mean(), cov90=g.cov90.mean()))
    R = pd.DataFrame(rows).sort_values(["retro", "mean_wis"])
    pd.set_option("display.width", 200)
    print(R.to_string(index=False, float_format=lambda x: "%.3f" % x))
    # ensemble = mean of member quantiles? (sanity only)
    E = W[W.model_id == "hub-ensemble"]
    M = W[(W.model_id != "hub-ensemble") & (W.model_id != "hub-baseline")]
    k = ["origin_date", "horizon", "location", "age_group", "retro"]
    for retro in [True, False]:
        mm = M[M.retro == retro].groupby(k)[LEVS].mean()
        ee = E[E.retro == retro].set_index(k)[LEVS]
        common = ee.index.intersection(mm.index)
        if len(common):
            diff = np.abs(ee.loc[common, LEVS].to_numpy() - mm.loc[common, LEVS].to_numpy())
            j = common
            print("ensemble vs mean of members (retro=%s): tasks %d, max abs diff %.3g, tasks with diff > 1e-6: %d"
                  % (retro, len(j), diff.max(), int((diff.max(1) > 1e-6).sum())))
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "work")
    os.makedirs(out, exist_ok=True)
    S.drop(columns=LEVS).to_csv(os.path.join(out, "hub_scores_%s.csv.gz" % season), index=False)
    R.to_csv(os.path.join(out, "hub_season_wis_%s.csv" % season), index=False)
