"""p3 (PREREG.v3): independent recomputation of per-model season-average WIS for the 2025-26 season of
CDCgov/rsv-forecast-hub (commit e947ca8fe8d50a581a181e6aefacfe922ba95af5), both targets, from the raw model-output
files and target-data/oracle-output.parquet at that commit. Deterministic; numpy, pandas, pyarrow; WIS from wis.py.

usage: python p3_recompute.py <hub dir (with model-output/, target-data/)> <out dir>
writes <out dir>/p3_table.csv, <out dir>/p3_exclusions.txt, <out dir>/p3_era_subset.txt and prints a summary.
"""
import os, sys, glob
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wis import LEVELS, wis_pinball, wis_interval, relative_skill  # noqa: E402

LEVS = [round(float(x), 4) for x in LEVELS]
TARGETS = ["wk inc rsv hosp", "wk inc rsv prop ed visits"]
WINDOW = ("2025-09-01", "2026-08-31")
ENS, BASE = "RSVHub-ensemble", "RSVHub-baseline"
K = ["reference_date", "location", "horizon"]
KF = K + ["target_end_date"]  # full task id (repair round: cross-model pairing must include target_end_date)


def loc(s):
    s = s.astype(str)
    return s.where(s == "US", s.str.zfill(2))


def read(f):
    d = pd.read_parquet(f) if f.endswith(".parquet") else pd.read_csv(f, dtype={"location": str, "output_type_id": str})
    d["location"] = loc(d["location"])
    for c in ("reference_date", "target_end_date"):
        d[c] = pd.to_datetime(d[c]).dt.strftime("%Y-%m-%d")
    d["horizon"] = d["horizon"].astype(int)
    d["target"] = d["target"].astype(str)
    d = d[d.output_type.astype(str) == "quantile"].copy()
    d["lev"] = pd.to_numeric(d.output_type_id, errors="coerce").round(4)
    return d[["target", "reference_date", "location", "horizon", "target_end_date", "lev", "value"]]


def main(hub, out):
    os.makedirs(out, exist_ok=True)
    ex = []
    parts, outside = [], []
    for f in sorted(glob.glob(os.path.join(hub, "model-output", "*", "*"))):
        if not f.endswith((".csv", ".parquet")):
            continue
        rd = os.path.basename(f)[:10]
        m = os.path.basename(os.path.dirname(f))
        if not (WINDOW[0] <= rd <= WINDOW[1]):
            continue
        d = read(f)
        d["model_id"] = m
        parts.append(d)
    D = pd.concat(parts, ignore_index=True)
    o = pd.read_parquet(os.path.join(hub, "target-data", "oracle-output.parquet"))
    n_dup = int(o.duplicated(["target", "location", "target_end_date"]).sum())
    o = o[o.output_type == "quantile"].copy()
    o["location"] = loc(o["location"])
    o["target_end_date"] = pd.to_datetime(o["target_end_date"]).dt.strftime("%Y-%m-%d")
    assert not o.duplicated(["target", "location", "target_end_date"]).any()
    truth = o.set_index(["target", "location", "target_end_date"]).oracle_value
    ex.append("oracle-output: %d rows repeat a (target, location, target_end_date) once per output_type (quantile, "
              "sample) with the same value; the quantile rows are used." % n_dup)
    rows, era = [], []
    for tg in TARGETS:
        W = D[D.target == tg].pivot_table(index=["model_id"] + K + ["target_end_date"], columns="lev", values="value",
                                          aggfunc="first")
        W = W[LEVS]
        n0 = len(W); W = W.dropna().reset_index()
        ex.append("%s: %d model tasks with quantiles, %d dropped for an incomplete set of the 23 levels." % (tg, n0, n0 - len(W)))
        y = truth.reindex(list(zip([tg] * len(W), W.location, W.target_end_date))).to_numpy()
        ex.append("%s: %d model tasks have no oracle value (unscored for every model)." % (tg, int(np.isnan(y).sum())))
        exp_ted = (pd.to_datetime(W.reference_date) + pd.to_timedelta(7 * W.horizon, unit="D")).dt.strftime("%Y-%m-%d")
        W["ted_ok"] = (exp_ted == W.target_end_date).to_numpy()
        badg = W[~W.ted_ok].groupby(["model_id", "reference_date"]).size()
        if len(badg):
            for (m_, r_), n_ in badg.items():
                lag = sorted(set(((pd.to_datetime(W[(~W.ted_ok) & (W.model_id == m_) & (W.reference_date == r_)].target_end_date)
                                   - pd.to_datetime(r_)).dt.days // 7 - W[(~W.ted_ok) & (W.model_id == m_) & (W.reference_date == r_)].horizon).tolist()))
                ex.append("%s: TARGET_END_DATE INCONSISTENT: %s file %s has %d tasks whose target_end_date is not "
                          "reference_date + 7*horizon (offset in weeks: %s); they are scored at the target_end_date they "
                          "state (task id = reference_date, location, horizon, target_end_date), as a hubverse join on "
                          "target_end_date would." % (tg, m_, r_, n_, ",".join(map(str, lag))))
        dup = W.duplicated(["model_id"] + K, keep=False)
        if dup.any():
            for (m_, r_), n_ in W[dup].groupby(["model_id", "reference_date"]).size().items():
                ex.append("%s: %s file %s has %d tasks sharing a (reference_date, location, horizon) with another task of "
                          "the same file (different target_end_date); each is a separate task here." % (tg, m_, r_, n_))
        W["y"] = y
        W = W[~np.isnan(y)].copy()
        Q = W[LEVS].to_numpy(float); yy = W.y.to_numpy(float)
        W["wis"] = wis_pinball(Q, yy)
        dmax = float(np.max(np.abs(W.wis - wis_interval(Q, yy))))
        ex.append("%s: max |pinball - interval| WIS over all scored rows = %.3g." % (tg, dmax))
        W["ae"] = np.abs(yy - Q[:, 11])
        W["c50"] = ((yy >= Q[:, 6]) & (yy <= Q[:, 16])).astype(float)
        W["c95"] = ((yy >= Q[:, 1]) & (yy <= Q[:, 21])).astype(float)
        E = W[W.model_id == ENS]
        if (~E.ted_ok).any():
            ex.append("%s: sensitivity, %s mean WIS: %.6g on all %d tasks; %.6g on its %d date-consistent tasks only; "
                      "%.6g with every task of its file(s) holding inconsistent rows dropped." % (
                          tg, ENS, E.wis.mean(), len(E), E[E.ted_ok].wis.mean(), int(E.ted_ok.sum()),
                          E[~E.reference_date.isin(set(E[~E.ted_ok].reference_date))].wis.mean(),))
        eks = set(map(tuple, E[KF].to_numpy()))
        ex.append("%s: %s has %d files and %d scored tasks; horizon -1 present on %d of its reference dates." % (
            tg, ENS, E.reference_date.nunique(), len(E), E[E.horizon == -1].reference_date.nunique()))
        models = sorted(W.model_id.unique())
        P = W.pivot_table(index=KF, columns="model_id", values="wis", aggfunc="first")
        assert not W.duplicated(["model_id"] + KF).any()
        rs, _ = relative_skill(P[models].to_numpy(float), models, BASE) if BASE in models else ({m: np.nan for m in models}, None)
        for m in models:
            g = W[W.model_id == m]
            mk = set(map(tuple, g[KF].to_numpy()))
            g_e = g[[tuple(r) in eks for r in g[KF].to_numpy()]]
            outside_dates = sorted(set(g.reference_date) - set(E.reference_date))
            if outside_dates:
                ex.append("%s: %s has reference dates without an ensemble file: %s." % (tg, m, ", ".join(outside_dates)))
            rows.append(dict(target=tg, model_id=m, n_tasks=len(g), n_dates=g.reference_date.nunique(),
                             first_date=g.reference_date.min(), last_date=g.reference_date.max(),
                             n_locations=g.location.nunique(), horizons=",".join(map(str, sorted(g.horizon.unique()))),
                             mean_wis=g.wis.mean(), mae=g.ae.mean(), cov50=g.c50.mean(), cov95=g.c95.mean(),
                             share_of_ens_tasks=len(mk & eks) / len(eks), mean_wis_on_ens_tasks=g_e.wis.mean() if len(g_e) else np.nan,
                             ens_mean_wis_same_tasks=E[[tuple(r) in mk for r in E[KF].to_numpy()]].wis.mean() if len(g_e) else np.nan,
                             rel_wis_pairwise_vs_baseline=rs[m]))
        if tg == "wk inc rsv hosp":
            S = W[(W.location != "US") & W.horizon.between(0, 3) & (W.reference_date >= "2026-01-03") & (W.reference_date <= "2026-05-30")]
            PUBLISHED = {"Google_SAI-RSVEns", "RSVHub-ensemble", "CEPH-Rtrend_rsv", "RSVHub-baseline"}
            for m, g in S.groupby("model_id"):
                era.append("%-28s tasks %5d dates %2d mean WIS %8.3f MAE %7.2f cov95 %.3f" % (m, len(g), g.reference_date.nunique(), g.wis.mean(), g.ae.mean(), g.c95.mean()))
            cnt = S.groupby("model_id").size()
            elig = sorted(cnt[cnt >= 3660].index)
            era.append("eligible by the published rule (>= 3,660 scorable tasks on this set): %s" % ", ".join(elig))
            for m in elig:
                if m not in PUBLISHED:
                    era.append("DISCREPANCY: %s meets the published eligibility count (%d tasks) but has no row in the published "
                               "table (cause: see p3_reconcile_epi_hub_analysis.txt)." % (m, cnt[m]))
    T = pd.DataFrame(rows)
    T.to_csv(os.path.join(out, "p3_table.csv"), index=False, float_format="%.10g", lineterminator="\n")
    open(os.path.join(out, "p3_exclusions.txt"), "w", newline="\n").write("\n".join(ex) + "\n")
    pub = ["published (arXiv 2605.16238 v2, Supp. Table 6; 52 states, horizons 0-3, reference dates 2026-01-03..2026-05-30):",
           "  Google_SAI-RSVEns 14.7 (MAE 21.2, cov95 85%); RSVHub-ensemble 16.4 (25.3, 87%); CEPH-Rtrend_rsv 19.8 (28.4, 78%); RSVHub-baseline 18.3 (27.8, 93%)",
           "recomputed on the same subset (every model directory with tasks there):"] + era
    open(os.path.join(out, "p3_era_subset.txt"), "w", newline="\n").write("\n".join(pub) + "\n")
    pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
    print(T.drop(columns=["first_date", "last_date"]).to_string(index=False, float_format=lambda x: "%.4f" % x))
    print("\n".join(ex)); print("\n".join(pub))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
