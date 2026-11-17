"""Re-derive the published evaluation's exclusion lists (submission_check/fixed/{Epiforecasts,MeanEnsemble,
MedianEnsemble,SZ}-missing.csv) from the nowcast files themselves: template = every (location, age_group, forecast_date,
target, type, quantile) the hub format requires (DE x 7 age groups + 16 states x 00+, horizons 0..-28, mean + 7
quantiles, 159 dates); missing = template minus the keys a model submitted (Epiforecasts after the 0.1-quantile
interpolation repair). Compare the sets with the released lists.
Usage: python -I rederive_exclusions.py <run_folder> <out_txt>"""
import sys, os, itertools
import pandas as pd
RUN, OUT = sys.argv[1], sys.argv[2]
EV = os.path.join(RUN, "data", "eval_data")
LOCS = ["DE-BB", "DE-BE", "DE-BW", "DE-BY", "DE-HB", "DE-HE", "DE-HH", "DE-MV", "DE-NI", "DE-NW", "DE-RP", "DE-SH",
        "DE-SL", "DE-SN", "DE-ST", "DE-TH"]
AGES = ["00+", "00-04", "05-14", "15-34", "35-59", "60-79", "80+"]
dates = pd.date_range("2021-11-22", "2022-04-29").strftime("%Y-%m-%d")
TQ = [("mean", -1.0)] + [("quantile", q) for q in [0.025, 0.1, 0.25, 0.5, 0.75, 0.9, 0.975]]
strata = [("DE", a) for a in AGES] + [(l, "00+") for l in LOCS]
template = {(l, a, d, h, t, q) for (l, a), d, h, (t, q) in itertools.product(strata, dates, range(-28, 1), TQ)}
MODELS = {"Epiforecasts": "Epiforecasts-independent", "MeanEnsemble": "NowcastHub-MeanEnsemble",
          "MedianEnsemble": "NowcastHub-MedianEnsemble", "SZ": "SZ-hosp_nowcast"}
present = {k: set() for k in MODELS}
epi_q = {}
for ch in pd.read_csv(os.path.join(EV, "submissions.csv.gz"), chunksize=1_000_000):
    for short, full in MODELS.items():
        c = ch[ch.model == full]
        if not len(c):
            continue
        h = c.target.str.split(" ").str[0].astype(int)
        q = c["quantile"].fillna(-1.0)
        present[short].update(zip(c.location, c.age_group, c.forecast_date, h, c.type, q))
lines = [f"template keys {len(template)}"]
# Epiforecasts repair: a target with 0.025 and 0.25 but no 0.1 gets an interpolated 0.1 row
E = present["Epiforecasts"]
tg = {}
for (l, a, d, h, t, q) in E:
    if t == "quantile":
        tg.setdefault((l, a, d, h), set()).add(q)
added = 0
for key, qs in tg.items():
    if 0.1 not in qs and (0.025 in qs or 0.25 in qs):
        E.add(key + ("quantile", 0.1)); added += 1
lines.append(f"Epiforecasts 0.1 rows added by the repair: {added}")
for short in MODELS:
    miss = template - present[short]
    L = pd.read_csv(os.path.join(EV, f"submission_check_fixed_{short}-missing.csv"))
    h = L.target.str.split(" ").str[0].astype(int)
    lst = set(zip(L.location, L.age_group, L.forecast_date, h, L.type, L["quantile"].fillna(-1.0)))
    lines.append(f"{short}: re-derived missing {len(miss)}, released list {len(lst)}, equal sets: {miss == lst}, "
                 f"only re-derived {len(miss - lst)}, only list {len(lst - miss)}")
open(OUT, "w", encoding="utf-8").write("\n".join(lines) + "\n")
print("\n".join(lines))
