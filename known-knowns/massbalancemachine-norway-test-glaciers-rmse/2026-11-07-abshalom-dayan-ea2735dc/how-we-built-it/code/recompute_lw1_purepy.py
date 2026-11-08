"""Independent pure-Python (csv + math only) recompute of a frozen winter linear model's test Bw RMSE.
Usage: python3 -I recompute_lw1_purepy.py <test csv> <frozen_LW1.json>"""
import csv, json, math, sys, collections
rows = list(csv.DictReader(open(sys.argv[1]))); fz = json.load(open(sys.argv[2])); a, b, c = fz["coef"]
assert fz["phis"] == ["one", "solid", "solid_dz"]
by = collections.defaultdict(list)
for r in rows: by[r["id"]].append(r)
bad = 0; se = 0.0; n = 0
for i, g in by.items():
    if len({x["n_months"] for x in g}) != 1 or len({x["balance"] for x in g}) != 1 or len(g) != int(g[0]["n_months"]): bad += 1
    if g[0]["n_months"] != "7": continue
    assert [x["month"] for x in g] == ["oct", "nov", "dec", "jan", "feb", "mar", "apr"]
    p = 0.0
    for x in g:
        dz = float(x["altitude_diff"]); t = float(x["t2m"]) - 273.15 + 0.0065 * dz; tp = float(x["tp"]) * 1000
        s = tp if t < 1 else 0.0
        p += a + b * s + c * s * dz / 1000
    se += (p - float(g[0]["balance"])) ** 2; n += 1
print("ids", len(by), "bad groups", bad, "winter n", n, "Bw RMSE %.4f" % math.sqrt(se / n))
