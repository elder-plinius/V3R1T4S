"""Descriptive robustness checks of the 2024-25 result (none of these changes the PREREG decision):
 1. bootstrap mean block length 1, 2, 3, 4, 6 for MAIN and P2;
 2. alternative truths: first report (the earliest archive vintage holding the target week), the view 4 weeks later,
    and the season-end view (2025-05-16 vintage), each with the same derived age groups; ours vs hub-ensemble on the
    same tasks;
 3. breakdowns by horizon, age group, US vs states; leave-one-reference-date-out range of the ratio.
usage: python sensitivity.py"""
import os, sys, glob
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
RUN = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(RUN, "attempts", "evaluator", "code"))
sys.path.insert(0, os.path.join(RUN, "attempts", "forecaster", "code"))
from score import paired_bootstrap, score_wide, LEVS  # noqa: E402
from parse_mo import load_all, quantile_wide  # noqa: E402
from wis import LEVELS  # noqa: E402
import score_test as ST  # noqa: E402
import asof_rsv as A  # noqa: E402

K = ["origin_date", "horizon", "location", "age_group"]
TEST = os.path.join(RUN, "attempts", "evaluator", "test", "2024-25")


def per_date(J, col):
    g = J.groupby("origin_date")[col].agg(["sum", "count"]).sort_index()
    return g.to_numpy(float)


def ratio_line(J, label, L=3):
    bs = paired_bootstrap(per_date(J, "wis_o"), per_date(J, "wis_c"), L=L)
    return "%-58s tasks %5d  ours %9.3f  ens %9.3f  rel %+.4f  90%% [%+.4f, %+.4f]" % (
        label, len(J), J.wis_o.mean(), J.wis_c.mean(), bs["rel"], bs["rel_lo"], bs["rel_hi"])


def alt_truth(kind):
    """long truth table (location, age_group, target_end_date, truth) from archive vintages."""
    labs = sorted(A.meta())
    rows = []
    if kind == "season_end":
        s = A._parse("2025-05-16")
        rows.append(s[["location", "age_group", "date", "count"]])
    else:
        # for every week, the first vintage (by label) whose data include it, or the one >= 28 days after that
        seen = {}
        for l in labs:
            if l < "2024-10-01" or A.meta()[l] > l:
                continue
            s = A._parse(l)
            s = s[s.date >= "2024-10-01"]
            for d, g in s.groupby("date"):
                if d not in seen:
                    seen[d] = l
        pick = {}
        for d, l in seen.items():
            if kind == "first":
                pick[d] = l
            else:
                later = [x for x in labs if x >= (pd.Timestamp(l) + pd.Timedelta(days=28)).strftime("%Y-%m-%d") and A.meta()[x] <= x]
                if later:
                    pick[d] = later[0]
        for d, l in pick.items():
            s = A._parse(l)
            rows.append(s[s.date == d][["location", "age_group", "date", "count"]])
    T = pd.concat(rows, ignore_index=True).rename(columns={"date": "target_end_date", "count": "truth"})
    return T.drop_duplicates(["location", "age_group", "target_end_date"])


if __name__ == "__main__":
    out = []
    J = pd.read_csv(TEST + "_tasks_MAIN hub-ensemble (all ensemble tasks).csv.gz", dtype={"location": str})
    P2 = pd.read_csv(TEST + "_tasks_P2 hub-ensemble (0-0.99, 1-4).csv.gz", dtype={"location": str})
    out.append("== 1. block length (final truth, PREREG uses L = 3)")
    for L in (1, 2, 3, 4, 6):
        out.append(ratio_line(J, "MAIN L=%d" % L, L))
        out.append(ratio_line(P2, "P2   L=%d" % L, L))
    out.append("== 3. breakdowns (final truth)")
    for h, g in J.groupby("horizon"):
        out.append(ratio_line(g, "MAIN horizon %d" % h))
    for a, g in J.groupby("age_group"):
        out.append(ratio_line(g, "MAIN age %s" % a))
    out.append(ratio_line(J[J.location == "US"], "MAIN US only"))
    out.append(ratio_line(J[J.location != "US"], "MAIN states only"))
    lodo = []
    for d in sorted(J.origin_date.unique()):
        g = J[J.origin_date != d]
        lodo.append((g.wis_o.mean() / g.wis_c.mean() - 1, d))
    out.append("MAIN leave-one-date-out rel: min %+.4f (%s) max %+.4f (%s)" % (min(lodo)[0], min(lodo)[1], max(lodo)[0], max(lodo)[1]))
    per = J.groupby("origin_date")[["wis_o", "wis_c"]].mean()
    out.append("MAIN dates where ours < ensemble: %d of %d" % (int((per.wis_o < per.wis_c).sum()), len(per)))
    out.append("== 2. alternative truths (same task keys, ours vs hub-ensemble)")
    hub = load_all()
    hub = hub[(hub.model_id == "hub-ensemble") & (hub.origin_date >= "2024-10-01") & (hub.origin_date <= "2025-07-31")]
    We, _ = quantile_wide(hub, LEVELS)
    Wo, _ = quantile_wide(ST.load_ours(os.path.join(RUN, "attempts", "forecaster", "result", "forecasts")), LEVELS)
    Wo = Wo[(Wo.origin_date >= "2024-10-01")]
    for kind in ("first", "plus4w", "season_end"):
        T = alt_truth(kind)
        # derived groups are already in the vintage parse (asof_rsv builds 0-0.99, 1-4, 5-64 as sums)
        Se = score_wide(We, T); So = score_wide(Wo, T)
        JJ = Se[K + ["wis"]].merge(So[K + ["wis"]], on=K, suffixes=("_c", "_o")).merge(J[K], on=K)
        out.append(ratio_line(JJ, "MAIN truth=%s" % kind))
        out.append(ratio_line(JJ[JJ.age_group.isin(["0-0.99", "1-4"])], "P2   truth=%s" % kind))
    txt = "\n".join(out)
    open(os.path.join(RUN, "attempts", "contrarian", "out", "sensitivity.txt"), "w").write(txt + "\n")
    print(txt)
