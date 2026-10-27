"""Relocation of the event from picks.csv (run from claim/: python -I code/locate.py). Grid search, homogeneous
half-space Vp 6.0 km/s and Vs 3.46 km/s, travel time = sqrt(epicentral distance^2 + (depth + station elevation)^2) / v
(epicentral distance by haversine on a 6371 km sphere); grid lat/lon +/- 0.5 deg in 0.01 deg steps around 39.1535 N,
119.0559 W and depth 0-20 km in 0.5 km steps; origin time = mean residual at each node; RMS of the demeaned residuals.
Horizontal error = the largest epicentral distance from the best node to any node with RMS <= best RMS + 0.1 s."""
import csv, os, datetime as dt
import numpy as np
CL = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")); U = dt.timezone.utc
VP, VS = 6.0, 3.46
def km(a, b, c, d):
    p = np.radians; h = np.sin(p(c - a) / 2) ** 2 + np.cos(p(a)) * np.cos(p(c)) * np.sin(p(d - b) / 2) ** 2; return 12742 * np.arcsin(np.sqrt(np.minimum(1.0, h)))
obs = [(r["station"], r["phase"], dt.datetime.strptime(r["time_utc"], "%Y-%m-%dT%H:%M:%S.%f").replace(tzinfo=U).timestamp(), float(r["sta_lat"]), float(r["sta_lon"]), float(r["sta_elev_m"])) for r in csv.DictReader(open(os.path.join(CL, "picks.csv")))]
LA = 39.1535 + np.arange(-50, 51) * 0.01; LO = -119.0559 + np.arange(-50, 51) * 0.01; Z = np.arange(0, 20.01, 0.5)
to = np.array([o[2] for o in obs]); v = np.array([VP if o[1] == "P" else VS for o in obs]); el = np.array([o[5] / 1000.0 for o in obs])
hd = km(LA[:, None, None], LO[None, :, None], np.array([o[3] for o in obs])[None, None, :], np.array([o[4] for o in obs])[None, None, :])
tt = np.sqrt(hd[:, :, None, :] ** 2 + (Z[None, None, :, None] + el[None, None, None, :]) ** 2) / v
res = to - tt; ot = res.mean(axis=3); r = res - ot[..., None]; rms = np.sqrt((r ** 2).mean(axis=3))
i, j, k = np.unravel_index(np.argmin(rms), rms.shape); best = rms[i, j, k]
ii, jj, kk = np.nonzero(rms <= best + 0.1); herr = km(LA[i], LO[j], LA[ii], LO[jj]).max()
print("picks %d on %d stations" % (len(obs), len({o[0] for o in obs})))
print("best node %.4f N %.4f W depth %.1f km; origin %s; RMS %.4f s; horizontal error %.3f km (%d nodes within +0.1 s)" % (LA[i], -LO[j], Z[k], dt.datetime.fromtimestamp(ot[i, j, k], U).strftime("%Y-%m-%dT%H:%M:%S.%f")[:22], best, herr, len(ii)))
print("residuals (s): " + ", ".join("%s %s %+.3f" % (o[0].split(".")[1], o[1], x) for o, x in zip(obs, r[i, j, k])))
