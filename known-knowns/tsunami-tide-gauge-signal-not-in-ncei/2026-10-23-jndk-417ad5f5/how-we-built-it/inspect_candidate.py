"""Read the candidate's records closely (not a scoring step; scoring is frozen in tsu.py).
For each claimed gauge: time of the band-passed peak, max peak-to-trough, the de-tided (unfiltered) residual
amplitude, despike count, and a plot of t0-3 h .. t0+5 h with the onset, ETA and +/-10 min band marked,
plus the same clock window on the 12 control days (grey)."""
import datetime as dt
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import tsu

OUT = os.environ.get("JOB_OUT", ".")
ev = json.load(open(sys.argv[1]))[0]
t0 = ev["t0"]
gs = [g for g in ev["gauges"] if g["code"] in ev["claimed"]]
fig, axs = plt.subplots(len(gs), 1, figsize=(10, 3 * len(gs)), sharex=True)
for ax, g in zip(np.atleast_1d(axs), gs):
    rows = tsu.ioc_data(g["code"], dt.datetime.fromtimestamp(t0 - 36 * 3600, dt.timezone.utc),
                        dt.datetime.fromtimestamp(t0 + 12 * 3600, dt.timezone.utc))
    info = tsu.prepare_gauge(rows, t0)
    tg, bp, res = info["tg"], info["bp"], info["res"]
    sc = tsu.score(tg, bp, t0, g["eta_min"] * 60)
    w = (tg >= t0 + sc["onset"]) & (tg <= t0 + sc["onset"] + 180 * 60)
    k = np.flatnonzero(w)[np.argmax(np.abs(bp[w]))]
    # max peak-to-trough between consecutive extrema in the window
    seg = bp[w]
    ext = [i for i in range(1, len(seg) - 1) if (seg[i] - seg[i - 1]) * (seg[i + 1] - seg[i]) < 0]
    p2t = max([abs(seg[ext[i + 1]] - seg[ext[i]]) for i in range(len(ext) - 1)] or [0])
    resw = res[w] - np.nanmedian(res[(tg >= t0 - 3 * 3600) & (tg < t0)])
    print("%s sensor %s native_dt %.0fs spikes %d | onset %s (+%.1f min) ETA %.1f min dt_arr %+.1f | bp peak %.3f m at %s (+%.1f min) "
          "R %.2f rms24 %.4f | max peak-to-trough %.3f m | de-tided residual max |x| %.3f m" % (
              g["code"], info["sensor"], info["native_dt"], info["spikes"],
              dt.datetime.fromtimestamp(t0 + sc["onset"], dt.timezone.utc).strftime("%H:%M:%S"), sc["onset"] / 60,
              g["eta_min"], sc["dt_arr"], sc["peak"], dt.datetime.fromtimestamp(tg[k], dt.timezone.utc).strftime("%H:%M:%S"),
              (tg[k] - t0) / 60, sc["R"], sc["rms24"], p2t, np.nanmax(np.abs(resw))))
    m = (tg >= t0 - 3 * 3600) & (tg <= t0 + 5 * 3600)
    for dd in [-7, -6, -5, -4, -3, -2, 2, 3, 4, 5, 6, 7]:
        tc = t0 + dd * 86400
        r2 = tsu.ioc_data(g["code"], dt.datetime.fromtimestamp(tc - 36 * 3600, dt.timezone.utc),
                          dt.datetime.fromtimestamp(tc + 12 * 3600, dt.timezone.utc))
        i2 = tsu.prepare_gauge(r2, tc)
        if i2.get("ok"):
            m2 = (i2["tg"] >= tc - 3 * 3600) & (i2["tg"] <= tc + 5 * 3600)
            ax.plot((i2["tg"][m2] - tc) / 60, i2["bp"][m2], color="0.8", lw=0.6)
    ax.plot((tg[m] - t0) / 60, bp[m], color="C0", lw=1)
    ax.axvline(g["eta_min"], color="C1", ls="--"); ax.axvspan(g["eta_min"] - 10, g["eta_min"] + 10, color="C1", alpha=0.15)
    ax.axvline(sc["onset"] / 60, color="C3")
    for s in (3, 5):
        ax.axhline(s * sc["rms24"], color="k", lw=0.5, ls=":"); ax.axhline(-s * sc["rms24"], color="k", lw=0.5, ls=":")
    ax.set_ylabel("%s bp (m)" % g["code"])
np.atleast_1d(axs)[-1].set_xlabel("minutes after origin %s" % ev["time"])
fig.suptitle("%s %s: band-passed (2-120 min) series, control days grey, ETA +/-10 min shaded, onset red" % (ev["id"], ev.get("place")))
fig.tight_layout()
fig.savefig(os.path.join(OUT, "candidate_%s.png" % ev["id"]), dpi=110)
print("saved plot")
