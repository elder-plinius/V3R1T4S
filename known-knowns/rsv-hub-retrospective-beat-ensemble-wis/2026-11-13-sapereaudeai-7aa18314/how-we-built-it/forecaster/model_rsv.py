"""V3R1T4S as-of RSV forecaster for the HopkinsIDD RSV hub (route a): 'inc hosp' counts for every location x
{0-130, 0-0.99, 1-4, 5-64, 65-130} x horizon -1..5, 23 quantiles. Deterministic, no randomness.

Pipeline for origin O (asof_rsv.snapshot gives the data vintage V with last week T <= O - 8 days):
 1. rates r = 1e5 * count / pop per series (location, age group); z = log(r + c).
 2. revision correction (backfill nowcast) from earlier usable vintages U (last week T_U <= T - 7*gap): for age group a
    and lag L (weeks before T_U), rev[a, L] = log( sum over U, locations of count_V(week) / sum of count_U(week) ),
    applied as z[T - 7L] += shrink * rev[a, L] for L = 0..Lmax.
 3. kernel analogs pooled over all series and history weeks of V (weeks after T - 7*guard are never used as outcomes):
    features d1, d2, d3 (weekly z differences), lv = z - max z over the last 52 weeks, week of year;
    Gaussian kernel on standardised features (bandwidths bw), week-of-year kernel (sd bw_woy), weight x age_w if the
    analog's age group differs; outcome y = z[t+s] - z[t]; weighted quantiles of y give the step-s quantiles, spread
    multiplier mult around the median.
 4. weeks already in V (s <= 0): corrected value plus the s=1 analog spread x nowcast_mult.
 Back-transform to counts with the series' own population from V, clip at 0, enforce monotone quantiles.
Inputs: only asof_rsv (archive vintages usable at O). Never the current target-data file, never model-output/.
"""
import os, sys, datetime as dt
import numpy as np, pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import asof_rsv as A  # noqa: E402

LEVELS = np.array([0.01, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75,
                   0.8, 0.85, 0.9, 0.95, 0.975, 0.99])
HORIZONS = (-1, 0, 1, 2, 3, 4, 5)
DEFAULT = dict(c=0.1, gap=8, Lmax=4, nrev=26, shrink=1.0, rev_by="age", guard=4, bw=(1.0, 1.0, 1.0, 1.0), bw_woy=4.0,
               age_w=1.0, loc_w=1.0, nd=3, phi=0.0, trend_k=2, bw_d=None, bw_lv=None, min_ess=30, mult=1.0, nowcast_mult=0.5, excl=("2020-06-01", "2021-08-31"), min_hist="2016-08-01")


def wquantile(y, w, levels):
    o = np.argsort(y); y = y[o]; w = w[o]
    cw = np.cumsum(w); cw = (cw - 0.5 * w) / cw[-1]
    return np.interp(levels, cw, y)


def revision_table(O, V_label, X_V, p):
    """rev[(age, L)] from earlier usable vintages (see module doc)."""
    meta = A.meta()
    if p.get("dev_rev_ref"):
        # DEVELOPMENT ONLY (never in a frozen configuration): a later reference vintage stands in for "near final",
        # to preview the correction the test-season pipeline will compute from the previous season's vintages.
        V_label = p["dev_rev_ref"]
        X_V, _ = A.wide(A._parse(V_label))
        cands = [l for l in sorted(meta) if p["dev_rev_from"] <= l <= p["dev_rev_to"] and meta[l] <= l]
    else:
        TV = A._d(meta[V_label])
        cands = [l for l in A.usable(O) if A._d(meta[l]) <= TV - dt.timedelta(days=7 * p["gap"])]
        if p.get("rev_months"):
            # only vintages whose last data week falls in the listed months (season weeks; summer pulls excluded)
            cands = [l for l in cands if A._d(meta[l]).month in p["rev_months"]]
        cands = cands[-p["nrev"]:]
    num, den = {}, {}
    if not cands:
        return {}
    XV = X_V.stack(["location", "age_group"], future_stack=True).rename("v").reset_index().rename(columns={"index": "date"})
    XV.columns = ["date", "location", "age_group", "v"]
    for l in cands:
        U = A._parse(l)
        TU = A._d(meta[l])
        wk = {(TU - dt.timedelta(days=7 * L)).isoformat(): L for L in range(p["Lmax"] + 1)}
        u = U[U.date.isin(list(wk))].merge(XV, on=["date", "location", "age_group"], how="inner").dropna(subset=["v"])
        for _, g in u.groupby([u.date, u.age_group] + ([] if p["rev_by"] == "age" else [u.location == "US"])):
            r0 = g.iloc[0]
            L = wk[r0.date]
            k = (r0.age_group if p["rev_by"] == "age" else (r0.age_group, r0.location == "US"), L) if p["rev_by"] == "age"                 else ((r0.age_group, bool(g.location.eq("US").all())), L)
            num[k] = num.get(k, 0.0) + g.v.sum()
            den[k] = den.get(k, 0.0) + g["count"].sum()
    return {k: float(np.log(num[k] / den[k])) for k in num if den[k] > 0 and num[k] > 0}


def analog_rows(Z, dates, s, last_ok, p, ages):
    """rows: [y, d1..d_nd, lv, woy, series index] for every series and history week t (t + s <= last_ok)."""
    n, L = Z.shape
    nd = p["nd"]
    rows = []
    woy = np.array([dt.date.fromisoformat(d).isocalendar()[1] for d in dates])
    excl = np.array([(p["excl"][0] <= d <= p["excl"][1]) or d < p["min_hist"] for d in dates])
    for t in range(max(52, nd + 1), n - s):
        if t + s > last_ok or excl[t] or excl[t + s]:
            continue
        cols = [Z[t + s] - Z[t]] + [Z[t - i] - Z[t - i - 1] for i in range(nd)]
        cols += [Z[t] - np.nanmax(Z[t - 52:t + 1], axis=0), np.full(L, woy[t]), np.arange(L)]
        M = np.column_stack(cols)
        rows.append(M[~np.isnan(M).any(axis=1)])
    return np.vstack(rows)


def features(col, t, nd):
    f = [col[t - i] - col[t - i - 1] for i in range(nd)] + [col[t] - np.nanmax(col[max(0, t - 52):t + 1])]
    return np.nan_to_num(np.array(f))


def forecast(O, p=None):
    q = dict(DEFAULT)
    if p:
        q.update(p)
    p = q
    s_long, lab = A.snapshot(O)
    X, pop = A.wide(s_long)
    dates = list(X.index)
    T = dates[-1]
    series = list(X.columns)
    ages = [a for (_, a) in series]
    R = X.to_numpy(float) / pop.to_numpy(float)[None, :] * 1e5
    Z = np.log(np.clip(R, 0, None) + p["c"])
    # revision correction of the last Lmax+1 weeks
    rev = revision_table(O, lab, X, p) if p["shrink"] > 0 else {}
    Zc = Z.copy()
    n = len(dates)
    for j, (loc, a) in enumerate(series):
        for L in range(p["Lmax"] + 1):
            k = (a if p["rev_by"] == "age" else (a, loc == "US"), L)
            if k in rev and not np.isnan(Zc[n - 1 - L, j]):
                # correct on the count scale, then back to z
                rr = np.exp(Zc[n - 1 - L, j]) - p["c"]
                Zc[n - 1 - L, j] = np.log(max(rr, 0) * np.exp(p["shrink"] * rev[k]) + p["c"])
    last_ok = n - 1 - p["guard"]
    nd = p["nd"]
    if p.get("bw_d") is not None:
        bw = np.array([p["bw_d"]] * nd + [p["bw_lv"]], float)
    else:
        bw = np.array(list(p["bw"])[:3] + [p["bw"][2]] * (nd - 3) + [p["bw"][3]], float)
    locs = [l for (l, _) in series]
    out = []
    cache = {}
    woyT = dt.date.fromisoformat(T).isocalendar()[1]
    for j, (loc, a) in enumerate(series):
        col = Zc[:, j]
        v = np.where(~np.isnan(col))[0]
        if len(v) < 1 or v[-1] < n - 1 - 8:
            # empty or stale series (last week more than 8 weeks before the vintage's last week, e.g. 65-130 rows that
            # stop in 2016 in the 2024-10-11 vintage): treated as absent; the missing-group fallback below covers it
            continue
        t = v[-1]
        f = features(col, t, nd)
        for h in HORIZONS:
            ted = (dt.date.fromisoformat(O) + dt.timedelta(days=7 * h - 1)).isoformat()
            s = int(round((dt.date.fromisoformat(ted) - dt.date.fromisoformat(dates[t])).days / 7))
            ss = max(s, 1)
            if ss not in cache:
                tr = analog_rows(Zc, dates, ss, last_ok, p, ages)
                sd = tr[:, 1:2 + nd].std(axis=0) + 1e-9
                cache[ss] = (tr, sd)
            tr, sd = cache[ss]
            d = (tr[:, 1:2 + nd] - f[None, :]) / (sd[None, :] * bw[None, :])
            w = np.exp(-0.5 * np.sum(d * d, axis=1))
            if p["bw_woy"]:
                dw = np.abs(tr[:, 2 + nd] - woyT); dw = np.minimum(dw, 52 - dw)
                w = w * np.exp(-0.5 * (dw / p["bw_woy"]) ** 2)
            if p["age_w"] != 1.0 or p["loc_w"] != 1.0:
                si = tr[:, 3 + nd].astype(int)
                ag = np.array(ages)[si]; lc = np.array(locs)[si]
                w = w * np.where(ag == a, 1.0, p["age_w"]) * np.where(lc == loc, 1.0, p["loc_w"])
            if w.sum() <= 0 or (w.sum() ** 2 / np.sum(w * w)) < p["min_ess"]:
                w = np.ones(len(tr))
            if p["phi"] > 0:
                # damped local trend: analog quantiles of the residual y - g * sum_{i<=s} phi^i, g = mean of the last k
                # weekly differences (row features 1..k), then the current trend added back
                kk = p["trend_k"]
                damp = sum(p["phi"] ** i for i in range(1, ss + 1))
                yres = tr[:, 0] - tr[:, 1:1 + kk].mean(axis=1) * damp
                qy = wquantile(yres, w, LEVELS) + f[:kk].mean() * damp
            else:
                qy = wquantile(tr[:, 0], w, LEVELS)
            med = np.interp(0.5, LEVELS, qy)
            if s <= 0:
                k = len(dates) - 1 + s if (len(dates) - 1 + s) >= 0 else None
                base = Zc[dates.index(ted), j] if ted in dates else col[t]
                if np.isnan(base):
                    base = col[t]
                zq = base + p["nowcast_mult"] * (qy - med)
            else:
                zq = col[t] + med + p["mult"] * (qy - med)
            val = np.clip(np.exp(zq) - p["c"], 0, None) * pop[(loc, a)] / 1e5
            val = np.maximum.accumulate(val)
            for lev, x in zip(LEVELS, val):
                out.append((O, "inc hosp", h, loc, a, "quantile", float(lev), float(x), ted))
    df = pd.DataFrame(out, columns=["origin_date", "target", "horizon", "location", "age_group", "output_type",
                                    "output_type_id", "value", "target_end_date"])
    # fallback for series absent from the vintage (e.g. 65-130 in some locations): the location's 0-130 quantiles times
    # the US share of that group in 0-130 over the vintage's last 52 weeks (these tasks have no truth in the hub target
    # data for 2023-24/2024-25 and are unscored; they are produced so that every task of the hub-ensemble is covered)
    have = set(zip(df.location, df.age_group))
    locs_all = sorted(set(l for (l, _) in series))
    for loc in locs_all:
        for a in A.GROUPS:
            if (loc, a) in have or (loc, "0-130") not in have:
                continue
            if ("US", a) in X.columns and ("US", "0-130") in X.columns:
                share = float(np.nansum(X[("US", a)].to_numpy()[-52:]) / max(np.nansum(X[("US", "0-130")].to_numpy()[-52:]), 1e-9))
            else:
                share = 0.3
            b = df[(df.location == loc) & (df.age_group == "0-130")].copy()
            b["age_group"] = a
            b["value"] = b["value"] * share
            df = pd.concat([df, b], ignore_index=True)
    return df, dict(vintage=lab, T=T, rev={str(k): v for k, v in rev.items()})


if __name__ == "__main__":
    O = sys.argv[1] if len(sys.argv) > 1 else "2024-01-07"
    df, info = forecast(O)
    print(info["vintage"], info["T"], len(df))
    print({k: round(v, 3) for k, v in info["rev"].items()})
    print(df[(df.location == "US") & (df.age_group == "0-130") & (df.output_type_id.isin([0.05, 0.5, 0.95]))]
          .pivot_table(index="horizon", columns="output_type_id", values="value").round(0))
