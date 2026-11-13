"""p3: independent Python recomputation of the published per-model mean WIS of the German Hospitalization Nowcast Hub
evaluation (Wolffram et al. 2023, PLoS Comput Biol 19:e1011394; tables data/scores/wis_{national,states,age}.csv of
github.com/dwolffram/hospitalization-nowcast-hub-evaluation), from the hub's nowcast files and the hub's truth data.

WIS (paper eq. 2, alpha = 0.5, 0.2, 0.05) = mean over the 7 quantile levels of 2 x pinball loss
    qs(q, y, tau) = 2 * (1{y < q} - tau) * (q - y);
decomposition as in the paper's code: spread = qs(q, median, tau); over = score - spread if median > y; under = score -
spread if median < y. Per model and level: plain mean over all scored quantile rows.

The rules of the published evaluation are re-implemented from its released R code (read as documentation, not run):
  S0 = all quantile rows, no fixes, no exclusions
  S1 = S0 + exclusion of every target listed as missing for Epiforecasts / MeanEnsemble / MedianEnsemble / SZ
       (removed for ALL models; anti_join on location, age_group, forecast_date, target_end_date, target, type, quantile)
  S2 = fixes, then the S1 exclusion (the published order): fix_RKI, fix_epiforecasts, fix_ILM, fix_LMU.
Usage: python -I p3_reproduce.py <run_folder> <out_dir>
"""
import sys, os, glob, json
import numpy as np, pandas as pd
from statistics import NormalDist

RUN, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
D = os.path.join(RUN, "data")
EV = os.path.join(D, "eval_data")
SHA_EVAL = "11c745322c055cfbd4f0c8f72241642a50aea399"
KEYS = ["location", "age_group", "forecast_date", "target_end_date", "target", "type", "quantile"]
STR = ["location", "age_group", "forecast_date", "target_end_date", "target", "type", "model"]
FULL2SHORT = {"Epiforecasts-independent": "Epiforecasts", "ILM-prop": "ILM", "KIT-frozen_baseline": "KIT-frozen_baseline",
              "KIT-simple_nowcast": "KIT", "LMU_StaBLab-GAM_nowcast": "LMU", "NowcastHub-MeanEnsemble": "MeanEnsemble",
              "NowcastHub-MedianEnsemble": "MedianEnsemble", "RIVM-KEW": "RIVM", "RKI-weekly_report": "RKI",
              "SU-hier_bayes": "SU", "SZ-hosp_nowcast": "SZ"}


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    with open(os.path.join(OUT, "p3_log.txt"), "a", encoding="utf-8") as f:
        f.write(s + "\n")


LOCS = ["DE", "DE-BB", "DE-BE", "DE-BW", "DE-BY", "DE-HB", "DE-HE", "DE-HH", "DE-MV", "DE-NI", "DE-NW",
        "DE-RP", "DE-SH", "DE-SL", "DE-SN", "DE-ST", "DE-TH"]
AGES = ["00+", "00-04", "05-14", "15-34", "35-59", "60-79", "80+"]
BASE = pd.Timestamp("2021-01-01")


def encode(df):
    """compact integer encoding of the key columns (memory: about 30 bytes per row)."""
    out = pd.DataFrame({
        "location": pd.Categorical(df["location"].astype(str), categories=LOCS).codes.astype("int8"),
        "age_group": pd.Categorical(df["age_group"].astype(str), categories=AGES).codes.astype("int8"),
        "forecast_date": (pd.to_datetime(df["forecast_date"]) - BASE).dt.days.astype("int16").values,
        "target_end_date": (pd.to_datetime(df["target_end_date"]) - BASE).dt.days.astype("int16").values,
        "target": df["target"].astype(str).str.split(" ").str[0].astype("int8").values,
        "type": (df["type"].astype(str) == "mean").astype("int8").values,
        "quantile": df["quantile"].astype(float).values,
        "value": df["value"].astype(float).values,
    })
    assert (out["location"] >= 0).all() and (out["age_group"] >= 0).all()
    if "model" in df.columns:
        out["model"] = df["model"].astype(str).values
    if "retrospective" in df.columns:
        out["retrospective"] = df["retrospective"].astype(bool).values
    out["pathogen"] = 0
    return out


def read_sub(path):
    parts = [encode(ch) for ch in pd.read_csv(path, chunksize=500_000)]
    return pd.concat(parts, ignore_index=True)


def read_keys(path):
    M = pd.read_csv(path)
    M["value"] = np.nan
    E = encode(M)
    return E[KEYS]


# ---------------- truth from the hub (preprocessed triangle as of 2022-08-08) ----------------
def hub_truth():
    P = pd.read_csv(os.path.join(D, "hub", "truth", SHA_EVAL, "COVID-19_hospitalizations_preprocessed.csv"))
    vc = [c for c in P.columns if c.startswith("value")]
    P["value"] = P[vc].sum(axis=1, skipna=True)          # rowSums(..., na.rm = TRUE)
    P = P.sort_values(["location", "age_group", "date"])
    P["truth"] = P.groupby(["location", "age_group"])["value"].transform(lambda s: s.rolling(7).sum())
    T = P.dropna(subset=["truth"])[["date", "location", "age_group", "truth"]].copy()
    return T


# ---------------- fixes (re-implemented from code/src/fix_submissions.R) ----------------
def fix_RKI(df):
    isR = df.model == "RKI"
    bad = isR & ((df.value > 1e6) | df.value.isna())
    n_bad = int(bad.sum())
    if n_bad == 0:
        return df, 0
    err = df.loc[bad, ["location", "age_group", "forecast_date", "type", "quantile"]]
    rep = df.loc[isR & df.target.isin([0, -1])]
    j = err.merge(rep, on=["location", "age_group", "forecast_date", "type", "quantile"], how="left")
    g = j.groupby(["location", "age_group", "forecast_date", "type", "quantile", "pathogen", "model", "retrospective"],
                  dropna=False)
    fixed = g.agg(target_end_date=("target_end_date", "max"), target=("target", "max"),
                  value=("value", "min")).reset_index()
    out = pd.concat([df.loc[~bad], fixed[df.columns]], ignore_index=True)
    return out, n_bad


def interp_q10(q025, q25):
    if q025 == q25:
        return q025
    z1, z2 = NormalDist().inv_cdf(0.025), NormalDist().inv_cdf(0.25)
    a, b = sorted([q025, q25])
    sd = (b - a) / (z2 - z1)
    mu = a - sd * z1
    return mu + sd * NormalDist().inv_cdf(0.1)


def fix_epiforecasts(df):
    m = (df.model == "Epiforecasts") & (df.type == 0)
    E = df.loc[m]
    gk = ["location", "age_group", "target_end_date", "forecast_date", "target"]
    has10 = E.assign(h=(E["quantile"] == 0.1)).groupby(gk)["h"].transform("any")
    inc = E.loc[~has10]
    if len(inc) == 0:
        return df, 0
    idc = [c for c in E.columns if c not in ("quantile", "value")]
    W = inc.pivot_table(index=idc, columns="quantile", values="value", aggfunc="first", dropna=False).reset_index()
    W = W.dropna(subset=[0.025, 0.25], how="all")
    W[0.1] = [interp_q10(a, b) for a, b in zip(W[0.025], W[0.25])]
    L = W.melt(id_vars=idc, value_vars=[0.025, 0.1, 0.25, 0.5, 0.75, 0.9, 0.975], var_name="quantile", value_name="value")
    L["quantile"] = L["quantile"].astype(float)
    out = pd.concat([df.loc[~m], E.loc[has10], L[df.columns]], ignore_index=True)
    return out, int(W.shape[0])


def fix_fill(df, short, missing_csv, folder, fname):
    miss = read_keys(missing_csv)
    new = []
    for di in sorted(miss.forecast_date.unique()):
        d = (BASE + pd.Timedelta(days=int(di))).strftime("%Y-%m-%d")
        p = os.path.join(D, "hub", "updated_models", folder, f"{d}-{fname}.csv")
        raw = pd.read_csv(p)
        if "forecast_date" not in raw.columns:
            # updated ILM files carry no forecast_date column; the R left_join then matches on target_end_date + target,
            # which identifies the forecast date uniquely (target_end_date = forecast_date + horizon)
            raw["forecast_date"] = d
        t = encode(raw)
        t["model"] = short
        t["retrospective"] = True
        new.append(t)
    new = pd.concat(new, ignore_index=True)
    j = miss.merge(new, on=KEYS, how="left")
    n_na = int(j.value.isna().sum())
    out = pd.concat([df, j[df.columns]], ignore_index=True)
    return out, len(miss), n_na


def exclusion(df):
    files = ["Epiforecasts-missing.csv", "MeanEnsemble-missing.csv", "MedianEnsemble-missing.csv", "SZ-missing.csv"]
    M = pd.concat([read_keys(os.path.join(EV, "submission_check_fixed_" + f)) for f in files], ignore_index=True)
    M = M.drop_duplicates()
    M["_x"] = 1
    j = df.merge(M, on=KEYS, how="left")
    out = j.loc[j._x.isna()].drop(columns="_x")
    return out, len(M), len(df) - len(out)


# ---------------- scoring (re-implemented from code/src/scoring_functions.R::compute_wis) ----------------
def level_filter(df, level):
    if level == "national":
        return df[(df.location == 0) & (df.age_group == 0)]
    if level == "states":
        return df[(df.location != 0) & (df.model != "ILM")]
    if level == "age":
        return df[(df.location == 0) & (df.age_group != 0) & (df.model != "RKI")]


def compute_wis(df):
    med = df.loc[df["quantile"] == 0.5].rename(columns={"value": "med"}).drop(
        columns=[c for c in ["quantile", "pathogen", "retrospective", "truth"] if c in df.columns])
    q = df.loc[df.type == 0]
    on = [c for c in med.columns if c != "med"]
    q = q.merge(med, on=on, how="left")
    y, v, tau, m = q.truth.values, q.value.values, q["quantile"].values, q.med.values
    score = 2 * ((y < v).astype(float) - tau) * (v - y)
    spread = 2 * ((m < v).astype(float) - tau) * (v - m)
    over = np.where(m > y, score - spread, 0.0)
    under = np.where(m < y, score - spread, 0.0)
    q = q.assign(score=score, spread=spread, overprediction=over, underprediction=under)
    g = q.groupby("model", observed=True)
    res = g[["spread", "overprediction", "underprediction", "score"]].agg(
        lambda s: s.mean() if s.notna().all() else np.nan)
    res["n_rows"] = g.size()
    res["n_nan_truth"] = g["score"].apply(lambda s: int(s.isna().sum()))
    return res, q


def main():
    log("== p3 recomputation start")
    sub = read_sub(os.path.join(EV, "submissions.csv.gz"))
    base = read_sub(os.path.join(EV, "submissions_KIT-frozen_baseline.csv.gz"))
    base["retrospective"] = False
    log("assembly rows", len(sub), "baseline rows", len(base), "baseline model names", sorted(base.model.unique()))
    df = pd.concat([sub, base], ignore_index=True)
    del sub, base
    df["model"] = df.model.map(FULL2SHORT)
    assert df.model.notna().all()
    log("models", sorted(df.model.unique()))

    T = hub_truth()
    Tpub = pd.read_csv(os.path.join(EV, "truth_2022-08-08.csv"))
    c = Tpub.merge(T, on=["date", "location", "age_group"], how="outer", suffixes=("_pub", "_hub"), indicator=True)
    both = c[c._merge == "both"]
    log("truth check: published rows", len(Tpub), "hub-recomputed rows", len(T), "in both", len(both),
        "only published", int((c._merge == "left_only").sum()), "only hub", int((c._merge == "right_only").sum()),
        "max |diff| on common", float(np.abs(both.truth_pub - both.truth_hub).max()))
    T = T.rename(columns={"date": "target_end_date"})
    T["target_end_date"] = (pd.to_datetime(T.target_end_date) - BASE).dt.days.astype("int16")
    T["age_group"] = pd.Categorical(T.age_group, categories=AGES).codes.astype("int8")
    T["location"] = pd.Categorical(T.location, categories=LOCS).codes.astype("int8")

    pub = {lv: pd.read_csv(os.path.join(D, "evalrepo", f"data_scores_wis_{lv}.csv")).set_index("model")
           for lv in ["national", "states", "age"]}

    # ---- ladder ----
    q_only = lambda x: x  # keep all rows (mean rows matter for nothing in WIS; kept for rule fidelity)
    stages = {}
    S0 = df.copy()
    S1, n_excl_keys, n_excl_rows = exclusion(df)
    log("S1 exclusion: listed keys", n_excl_keys, "rows removed (all models)", n_excl_rows)
    S2, n_rki = fix_RKI(df)
    log("fix_RKI: RKI rows with value > 1e6 or NA replaced:", n_rki)
    S2, n_epi = fix_epiforecasts(S2)
    log("fix_epiforecasts: Epiforecasts targets with the 0.1 quantile interpolated:", n_epi)
    S2, n_ilm, na_ilm = fix_fill(S2, "ILM", os.path.join(EV, "submission_check_ILM-missing.csv"), "ILM-prop", "ILM-prop")
    log("fix_ILM: rows filled", n_ilm, "unfilled (NA)", na_ilm)
    S2, n_lmu, na_lmu = fix_fill(S2, "LMU", os.path.join(EV, "submission_check_LMU-missing.csv"),
                                 "LMU_StaBLab-GAM_nowcast", "LMU_StaBLab-GAM_nowcast")
    log("fix_LMU: rows filled", n_lmu, "unfilled (NA)", na_lmu)
    S2, _, n_excl2 = exclusion(S2)
    log("S2 exclusion rows removed", n_excl2)
    del df

    rows = []
    for name, S in [("S0", S0), ("S1", S1), ("S2", S2)]:
        S = S.merge(T, on=["location", "age_group", "target_end_date"], how="left")
        for lv in ["national", "states", "age"]:
            res, qrows = compute_wis(level_filter(S, lv))
            if name == "S2":
                qrows[["model", "location", "age_group", "forecast_date", "target", "quantile", "value", "truth",
                       "score"]].to_csv(os.path.join(OUT, f"rows_S2_{lv}.csv.gz"), index=False)
            for mo, r in res.iterrows():
                p = pub[lv].loc[mo] if mo in pub[lv].index else None
                rows.append(dict(stage=name, level=lv, model=mo, n_rows=int(r.n_rows), n_nan=int(r.n_nan_truth),
                                 wis=r.score, spread=r.spread, over=r.overprediction, under=r.underprediction,
                                 pub_wis=None if p is None else p.score,
                                 pub_spread=None if p is None else p.spread,
                                 pub_over=None if p is None else p.overprediction,
                                 pub_under=None if p is None else p.underprediction))
        del S
    R = pd.DataFrame(rows)
    R["rel_diff"] = R.wis / R.pub_wis - 1
    R["within_1pct"] = R.rel_diff.abs() <= 0.01
    R.to_csv(os.path.join(OUT, "p3_ladder.csv"), index=False)
    pd.set_option("display.width", 250)
    for st in ["S0", "S1", "S2"]:
        sub_ = R[R.stage == st]
        log(f"\n== {st}: cells {len(sub_)}, within 1%: {int(sub_.within_1pct.sum())}, "
            f"max |rel diff| {sub_.rel_diff.abs().max():.3e}")
        log(sub_[["level", "model", "n_rows", "n_nan", "wis", "pub_wis", "rel_diff"]].to_string(index=False))
    s2 = R[R.stage == "S2"].copy()
    for comp, pc in [("spread", "pub_spread"), ("over", "pub_over"), ("under", "pub_under")]:
        s2[comp + "_absdiff"] = (s2[comp] - s2[pc]).abs()
    log("\nS2 component max abs diffs:", float(s2.spread_absdiff.max()), float(s2.over_absdiff.max()),
        float(s2.under_absdiff.max()))
    log("S2 all 31 published cells present:", len(s2.dropna(subset=["pub_wis"])) == 31)
    log("== done")


if __name__ == "__main__":
    main()
