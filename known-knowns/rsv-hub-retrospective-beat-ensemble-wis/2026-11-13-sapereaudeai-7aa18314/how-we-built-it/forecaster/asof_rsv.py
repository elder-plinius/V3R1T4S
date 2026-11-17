"""As-of data for the HopkinsIDD RSV hub (route a). Reads ONLY data/hopkins/hub/target-data/archive/<D>_rsvnet_hospitalization.csv.
Never the current target-data file, never model-output/.
Rule (PREREG.v2): vintage D usable for origin O iff D <= O and its latest date <= O - 8 days; the data vintage is the
usable one with the latest data date (ties: latest label).
Series groups (hub submission groups) as counts: 0-130 direct; 0-0.99 = 0-0.49 + 0.5-0.99; 1-4 = 1-1.99 + 2-4;
5-64 = 5-17 + 18-49 + 50-64; 65-130 direct when present, else 0-130 - (0-4 + 5-17 + 18-49 + 50-64).
Populations for derived groups = sum of the component populations in the same vintage."""
import os, glob, datetime as dt
import numpy as np, pandas as pd

RUN = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
ARCH = os.environ.get("RSV_ARCH") or os.path.join(RUN, "data", "hopkins", "hub", "target-data", "archive")
CACHE = os.environ.get("RSV_CACHE") or os.path.join(RUN, "attempts", "forecaster", "work", "vcache")
GROUPS = ["0-130", "0-0.99", "1-4", "5-64", "65-130"]
COMP = {"0-0.99": ["0-0.49", "0.5-0.99"], "1-4": ["1-1.99", "2-4"], "5-64": ["5-17", "18-49", "50-64"]}
READ_LOG = []   # (origin, vintage label, max date read) for the look-ahead audit


def _d(s):
    return dt.date.fromisoformat(str(s)[:10])


def labels():
    return sorted(os.path.basename(f)[:10] for f in glob.glob(os.path.join(ARCH, "*_rsvnet_hospitalization.csv")))


def _parse(label):
    """-> long DataFrame location, date, age_group (hub groups), count, pop."""
    os.makedirs(CACHE, exist_ok=True)
    cf = os.path.join(CACHE, label + ".pkl")
    if os.path.exists(cf):
        return pd.read_pickle(cf)
    t = pd.read_csv(os.path.join(ARCH, label + "_rsvnet_hospitalization.csv"), dtype={"location": str, "age_group": str})
    t = t[t.target == "inc hosp"]
    C = t.pivot_table(index=["location", "date"], columns="age_group", values="value", aggfunc="last")
    P = t.pivot_table(index=["location", "date"], columns="age_group", values="population", aggfunc="last")
    out = []
    for g in GROUPS:
        if g in COMP:
            comp = COMP[g]
            if not all(c in C.columns for c in comp):
                continue
            v = C[comp].sum(axis=1, min_count=len(comp)); p = P[comp].sum(axis=1, min_count=len(comp))
        elif g == "65-130" and "65-130" not in C.columns:
            need = ["0-130", "0-4", "5-17", "18-49", "50-64"]
            if not all(c in C.columns for c in need):
                continue
            v = C["0-130"] - C[["0-4", "5-17", "18-49", "50-64"]].sum(axis=1, min_count=4)
            p = P["0-130"] - P[["0-4", "5-17", "18-49", "50-64"]].sum(axis=1, min_count=4)
        else:
            if g not in C.columns:
                continue
            v = C[g]; p = P[g]
        out.append(pd.DataFrame({"count": v, "pop": p}).reset_index().assign(age_group=g))
    L = pd.concat(out, ignore_index=True)
    L = L[~L["count"].isna()]
    L["count"] = L["count"].clip(lower=0)
    L.to_pickle(cf)
    return L


_META = None


def meta():
    """label -> latest date in the vintage (any series)."""
    global _META
    if _META is None:
        mf = os.path.join(CACHE, "meta.csv")
        if os.path.exists(mf):
            m = pd.read_csv(mf)
        else:
            m = pd.DataFrame([(l, _parse(l).date.max()) for l in labels()], columns=["label", "maxdate"])
            m.to_csv(mf, index=False)
        _META = dict(zip(m.label, m.maxdate))
    return _META


def usable(O):
    """Usable vintages for origin O (ISO date), sorted by (maxdate, label)."""
    lim = (_d(O) - dt.timedelta(days=8)).isoformat()
    u = [(md, l) for l, md in meta().items() if l <= O and md <= lim]
    return [l for md, l in sorted(u)]


def snapshot(O):
    """The as-of data for origin O: long DataFrame (location, date, age_group, count, pop).
    Data vintage = the usable vintage with the latest data week (PREREG.v2). PREREG.v4: a location that is absent from
    it, or whose last week there is earlier than the vintage's last week, is taken from the usable vintage where that
    location's own last week is latest (ties: the later vintage in the PREREG.v2 order)."""
    u = usable(O)
    if not u:
        raise RuntimeError("no usable vintage for %s" % O)
    lab = u[-1]
    s = _parse(lab)
    T = s.date.max()
    last = s.groupby("location").date.max()
    if True:   # always check: a location may be absent while every present one is current
        best = {}
        for l in u:   # ascending (maxdate, label): later entries win ties
            for loc, d in _parse(l).groupby("location").date.max().items():
                if loc not in best or d >= best[loc][0]:
                    best[loc] = (d, l)
        swap = {loc: l for loc, (d, l) in best.items() if l != lab and (loc not in last.index or d > last[loc])}
        if swap:
            parts = [s[~s.location.isin(list(swap))]]
            for loc, l in sorted(swap.items()):
                x = _parse(l)
                parts.append(x[x.location == loc])
                READ_LOG.append((O, l, x.date.max()))
            s = pd.concat(parts, ignore_index=True)
    READ_LOG.append((O, lab, s.date.max()))
    return s, lab


def wide(s):
    """long -> (dates x series) count matrix and population vector; series = (location, age_group)."""
    X = s.pivot_table(index="date", columns=["location", "age_group"], values="count", aggfunc="last")
    Pp = s.sort_values("date").groupby(["location", "age_group"])["pop"].last()
    grid = pd.date_range(pd.Timestamp(X.index.min()), pd.Timestamp(X.index.max()), freq="7D").strftime("%Y-%m-%d")
    X = X.reindex(grid)
    return X, Pp.reindex(X.columns)


if __name__ == "__main__":
    import sys
    m = meta()
    for O in sys.argv[1:]:
        s, lab = snapshot(O)
        print(O, "->", lab, "maxdate", s.date.max(), "usable", len(usable(O)))
