"""Decisive scoring per PREREG R4-R9 (+ PREREG.v2). usage:
  python score_test.py <our forecast dir> <season 2024-25|2023-24> <out prefix>
Reads: our CSV files (<origin>-V3R1T4S-asofKA.csv), data/hopkins/hub/model-output (as fetched at the pinned commit),
the final truth file (score.load_truth). Writes <out prefix>_summary.txt and per-task CSVs."""
import os, sys, glob
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from parse_mo import load_all, quantile_wide  # noqa: E402
from score import load_truth, score_wide, paired_bootstrap, LEVS  # noqa: E402
from wis import LEVELS  # noqa: E402

SEASONS = {"2024-25": ("2024-10-01", "2025-07-31"), "2023-24": ("2023-10-01", "2024-07-31")}
K = ["origin_date", "horizon", "location", "age_group"]


def load_ours(d):
    parts = []
    for f in sorted(glob.glob(os.path.join(d, "*-V3R1T4S-asofKA.csv"))):
        x = pd.read_csv(f, dtype={"location": str, "age_group": str, "output_type_id": str})
        parts.append(x)
    x = pd.concat(parts, ignore_index=True)
    x["output_type_id"] = x.output_type_id.astype(float)
    x["target_end_date"] = (pd.to_datetime(x.origin_date) + pd.to_timedelta(7 * x.horizon - 1, unit="D")).dt.strftime("%Y-%m-%d")
    x["model_id"] = "V3R1T4S-asofKA"; x["file"] = "ours"; x["retro"] = False
    return x


def per_date(S, col):
    g = S.groupby("origin_date")[col].agg(["sum", "count"]).sort_index()
    return g.to_numpy(float), list(g.index)


def compare(ours, theirs, label, out, L=3):
    """ours/theirs: scored task tables (K + wis); compare on theirs' scored tasks."""
    J = theirs[K + ["wis"]].merge(ours[K + ["wis"]], on=K, how="left", suffixes=("_c", "_o"))
    missing = int(J.wis_o.isna().sum())
    J = J.dropna(subset=["wis_o"])
    A_, dates = per_date(J.rename(columns={"wis_o": "x"}), "x")
    B_, _ = per_date(J.rename(columns={"wis_c": "x"}), "x")
    bs = paired_bootstrap(A_, B_, L=L)
    # descriptive: reference-date sign-flip permutation of per-date mean differences
    rng = np.random.default_rng(1)
    d = A_[:, 0] / A_[:, 1] - B_[:, 0] / B_[:, 1]
    w = A_[:, 1]
    obs = np.sum(d * w) / w.sum()
    flips = rng.choice([-1, 1], size=(10000, len(d)))
    perm = (flips * d * w).sum(1) / w.sum()
    p_perm = float(np.mean(perm <= obs))
    row = dict(comparator=label, tasks=len(J), missing_ours=missing, dates=len(dates), wis_ours=J.wis_o.mean(),
               wis_comp=J.wis_c.mean(), rel=bs["rel"], rel_lo=bs["rel_lo"], rel_hi=bs["rel_hi"], dif=bs["dif"],
               dif_lo=bs["dif_lo"], dif_hi=bs["dif_hi"], signflip_p=p_perm)
    J.to_csv(out + "_tasks_%s.csv.gz" % label.replace("/", "_"), index=False)
    return row


if __name__ == "__main__":
    ours_dir, season, out = sys.argv[1], sys.argv[2], sys.argv[3]
    a, b = SEASONS[season]
    T = load_truth()
    hub = load_all()
    hub = hub[(hub.origin_date >= a) & (hub.origin_date <= b)]
    Wh, nd = quantile_wide(hub, LEVELS)
    Sh = score_wide(Wh, T)
    O = load_ours(ours_dir)
    O = O[(O.origin_date >= a) & (O.origin_date <= b)]
    Wo, nd2 = quantile_wide(O, LEVELS)
    So = score_wide(Wo, T)
    lines = ["season %s; hub wide tasks %d (incomplete dropped %d); ours wide tasks %d (incomplete %d)" % (season, len(Wh), nd, len(Wo), nd2),
             "max |pinball - interval| hub %.3g ours %.3g" % (np.abs(Sh.wis - Sh.wis_int).max(), np.abs(So.wis - So.wis_int).max())]
    rows = []
    E = Sh[Sh.model_id == "hub-ensemble"]
    if season == "2023-24":   # real-time file wins where both exist (descriptive season only)
        rt = set(E[~E.retro].origin_date)
        E = E[~(E.retro & E.origin_date.isin(rt))]
    rows.append(compare(So, E, "MAIN hub-ensemble (all ensemble tasks)", out))
    rows.append(compare(So, E[E.age_group.isin(["0-0.99", "1-4"])], "P2 hub-ensemble (0-0.99, 1-4)", out))
    rows.append(compare(So, E[E.age_group == "0-130"], "descr hub-ensemble 0-130 only", out))
    for m in sorted(Sh.model_id.unique()):
        if m == "hub-ensemble":
            continue
        g = Sh[Sh.model_id == m]
        if season == "2023-24":
            rt = set(g[~g.retro].origin_date)
            g = g[~(g.retro & g.origin_date.isin(rt))]
        rows.append(compare(So, g, "P1 " + m, out))
    R = pd.DataFrame(rows)
    pd.set_option("display.width", 250)
    txt = R.to_string(index=False, float_format=lambda x: "%.4f" % x)
    main = R.iloc[0]; p2 = R.iloc[1]; p1 = R[R.comparator.str.startswith("P1 ")]
    lines.append(txt)
    lines.append("MAIN criterion (R7: rel <= -0.03 and rel_hi < 0): %s (rel %.4f, 90%% [%.4f, %.4f])" % (
        "MET" if (main.rel <= -0.03 and main.rel_hi < 0) else "NOT MET", main.rel, main.rel_lo, main.rel_hi))
    lines.append("P2 (R9: rel < 0 and rel_hi < 0): %s (rel %.4f, 90%% [%.4f, %.4f])" % (
        "MET" if (p2.rel < 0 and p2.rel_hi < 0) else "NOT MET", p2.rel, p2.rel_lo, p2.rel_hi))
    ok = (p1.rel < 0) & (p1.rel_hi < 0)
    lines.append("P1 (R8: every model rel < 0 and rel_hi < 0): %s; failing: %s" % (
        "MET" if ok.all() else "NOT MET", ", ".join(p1[~ok].comparator) or "none"))
    open(out + "_summary.txt", "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))
