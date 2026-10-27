"""Side checks for the claim (run from claim/: python -I code/checks.py): S/P amplitude ratio, local time, teleseisms,
ComCat non-earthquake event types nearby, the published enhanced catalogue and the geoserve authoritative region.
All inputs are in data/ (live queries and their URLs: REPRODUCE.md)."""
import csv, json, os, glob, datetime as dt
import numpy as np, obspy
from obspy.taup import TauPyModel
CL = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")); D = os.path.join(CL, "data"); U = dt.timezone.utc
def km(a, b, c, d):
    p = np.radians; h = np.sin(p(c - a) / 2) ** 2 + np.cos(p(a)) * np.cos(p(c)) * np.sin(p(d - b) / 2) ** 2; return float(12742 * np.arcsin(np.sqrt(min(1.0, h))))
def ts(s):
    x = dt.datetime.fromisoformat(s.replace("Z", "+00:00")); return (x if x.tzinfo else x.replace(tzinfo=U)).timestamp()   # naive = UTC
E = json.load(open(os.path.join(CL, "event.json"))); la, lo, t = E["latitude"], E["longitude"], ts(E["origin_time_utc"])
pk = {(r["station"], r["phase"]): ts(r["time_utc"]) for r in csv.DictReader(open(os.path.join(CL, "picks.csv")))}
# 1. S/P: nearest station with both picks; causal 4-pole Butterworth 2-15 Hz (demean, 5 % taper, as the picks);
#    peak of sqrt(N^2 + E^2) in [S, S + 2 s] over peak |Z| in [P, P + 1 s].
SX = E["station_coordinates"]
for s in sorted(SX, key=lambda s: km(la, lo, SX[s][0], SX[s][1])):
    if (s, "P") in pk and (s, "S") in pk:
        st = obspy.read(glob.glob(os.path.join(D, "cand_*_%s.mseed" % s))[0]); st.detrend("demean"); st.taper(0.05); st.filter("bandpass", freqmin=2, freqmax=15, corners=4, zerophase=False)
        z = st.select(component="Z")[0]; h = [tr for tr in st if tr.stats.channel[-1] in "NE"]; sr = z.stats.sampling_rate; t0 = float(z.stats.starttime.timestamp)
        pi = int((pk[(s, "P")] - t0) * sr); si = int((pk[(s, "S")] - t0) * sr); n = min(len(h[0].data), len(h[1].data)); env = np.sqrt(h[0].data[:n].astype(float) ** 2 + h[1].data[:n].astype(float) ** 2)
        print("S/P at %s (%.1f km): %.2f" % (s, km(la, lo, SX[s][0], SX[s][1]), float(np.max(env[si:si + int(2 * sr)]) / np.max(np.abs(z.data[pi:pi + int(sr)]))))); break
print("local time (PST = UTC - 8 h): %s; depth %.1f km" % ((dt.datetime.fromtimestamp(t, U) - dt.timedelta(hours=8)).strftime("%H:%M"), E["depth_km"]))
# 2. Teleseisms: ComCat global M >= 5.5 in the hour before; P-type arrivals (iasp91) at YER within +/-60 s of the origin.
M = TauPyModel("iasp91"); hits = []
for e in csv.DictReader(open(os.path.join(D, "global_m55_window.csv"))):
    te = ts(e["time"])
    if t - 3600 <= te <= t:
        dg = km(float(e["latitude"]), float(e["longitude"]), *SX["NN.YER"][:2]) / 111.195
        hits += [(e["id"], a.name, round(te + a.time - t, 1)) for a in M.get_travel_times(max(float(e["depth"]), 0), dg, phase_list=["P", "PKP", "PKIKP", "Pdiff", "PP"]) if abs(te + a.time - t) <= 60]
print("teleseismic P-type arrivals at YER within +/-60 s:", hits or "none")
# 3. ComCat event types within 50 km of the event, 2019-12-09 to the query date.
ty = {}
for e in csv.DictReader(open(os.path.join(D, "alltypes_5y_event_centred.csv"))):
    ty.setdefault(e["type"], []).append(e)
print("ComCat types within 50 km (event-centred, 5 y):", {k: len(v) for k, v in ty.items()})
for k, v in ty.items():
    if k != "earthquake":
        for e in v: print("   %s %s M%s %s, %.2f km" % (k, e["time"], e["mag"], e["place"], km(la, lo, float(e["latitude"]), float(e["longitude"]))))
# 4. The published catalogue of the sequence (Bogolub and Trugman, Zenodo 10.5281/zenodo.15644553): anything within +/-30 s.
near = []
for r in csv.DictReader(open(os.path.join(D, "Parker_Butte_Catalog.csv"))):
    tr = dt.datetime(int(r["year"]), int(r["mon"]), int(r["day"]), int(r["hour"]), int(r["min"]), tzinfo=U).timestamp() + float(r["sec"])
    if abs(tr - t) <= 30: near.append((r["evid"], round(tr - t, 2), round(km(la, lo, float(r["reloc_lat"]), float(r["reloc_lon"])), 1)))
print("Bogolub and Trugman catalogue events within +/-30 s:", near or "none")
g = json.load(open(os.path.join(D, "point_v7.json")))["authoritative"]["features"]
print("geoserve authoritative region at the epicentre:", [(f["properties"]["network"], f["properties"]["name"], f["properties"]["type"]) for f in g])
