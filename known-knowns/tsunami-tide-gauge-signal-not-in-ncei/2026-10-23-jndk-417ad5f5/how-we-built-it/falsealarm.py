"""settled-already lens: how specific is the frozen per-gauge DETECT rule on its own?
Draw stations with recent data and random quiet times; give each a random ETA (15-120 min) and apply
tsu.score/detect exactly as frozen. Rate p of per-gauge DETECT at random times gives the chance that
>= 2 of 8 gauges fire by luck (binomial) and the expected number of chance stage-2 passes over the sweep.
Also tabulates the stage-1 screen rate (R > 5 over [t0, t0+4 h]) on the same draws."""
import datetime as dt
import json
import math
import os
import random

import numpy as np

import tsu

OUT = os.environ.get("JOB_OUT", ".")
rng = random.Random(7)
st = [s for s in tsu.ioc_stationlist() if s.get("Lat") is not None]
codes = sorted({s["Code"] for s in st})
rng.shuffle(codes)
N_ST, N_T = 40, 6
t_lo = dt.datetime(2019, 1, 1, tzinfo=dt.timezone.utc).timestamp()
t_hi = dt.datetime(2026, 9, 30, tzinfo=dt.timezone.utc).timestamp()
draws, used = [], 0
for code in codes:
    if used >= N_ST:
        break
    got = 0
    for k in range(N_T):
        t0 = rng.uniform(t_lo, t_hi)
        eta = rng.uniform(15, 120) * 60
        try:
            rows = tsu.ioc_data(code, dt.datetime.fromtimestamp(t0 - 36 * 3600, dt.timezone.utc),
                                dt.datetime.fromtimestamp(t0 + 12 * 3600, dt.timezone.utc))
        except Exception as e:
            continue
        info = tsu.prepare_gauge(rows, t0)
        if not info.get("ok"):
            if k == 0 and info.get("why", "").startswith("no sensor"):
                break  # station without usable 1-min data: skip it
            continue
        sc = tsu.score(info["tg"], info["bp"], t0, eta)
        s1 = tsu.score(info["tg"], info["bp"], t0)
        draws.append({"code": code, "t0": t0, "eta_min": eta / 60, "R": sc["R"], "dt_arr": sc["dt_arr"],
                      "detect": tsu.detect(sc), "screenR": s1["R"]})
        got += 1
    if got:
        used += 1
    print(code, got, flush=True)

n = len(draws)
p = sum(d["detect"] for d in draws) / n
ps = sum(d["screenR"] > 5 for d in draws) / n
p2 = 1 - (1 - p) ** 8 - 8 * p * (1 - p) ** 7
ps2 = 1 - (1 - ps) ** 8 - 8 * ps * (1 - ps) ** 7
print("DRAWS", n, "stations", used)
print("per-gauge DETECT rate at random times p = %.4f (%d/%d)" % (p, sum(d["detect"] for d in draws), n))
print("per-gauge stage-1 screen rate = %.4f" % ps)
print("P(>=2 of 8 DETECT by chance, independent) = %.5f; x960 quakes = %.2f expected chance stage-2 passes" % (p2, p2 * 960))
print("P(>=2 of 8 screen by chance) = %.4f; x960 = %.1f" % (ps2, ps2 * 960))
json.dump(draws, open(os.path.join(OUT, "falsealarm_draws.json"), "w"))
