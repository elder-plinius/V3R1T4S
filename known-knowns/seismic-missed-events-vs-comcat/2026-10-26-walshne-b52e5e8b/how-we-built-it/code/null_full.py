"""Standalone detector and full null for the claim (float64 correlation; run 2026-10-26-1727 PREREG.md L1). Run from claim/:

    python -I code/null_full.py fetch            # 32 HHZ day files from EarthScope (honest GETs, logged, cached)
    python -I code/null_full.py prep             # 2-8 Hz zero-phase, 20 Hz, gap masks
    python -I code/null_full.py run [NPROC]      # 385 templates on the real days and on all 600 control jobs
    python -I code/null_full.py summary          # best control, count >= the event NCC, EFC, the event's own NCC;
                                                 # writes the per-control maxima and the real detections to nullwork/

Work files go to ./nullwork/ (or $NULLWORK). Inputs: data/templates.json (385 templates: per station the 120-sample
window `w`, moveout `m` in samples from the template origin, `rms`), data/null_jobs.json (400 controls, 2024-12-10..12)
and data/null_d9_jobs.json (200 controls, 2024-12-09): each job is [day, {station: shift in samples at 20 Hz}, tag].
Pipeline: per station-day normalised cross-correlation, numerator by chunked FFT in float64 and each window's norm
computed directly (an earlier version used float32 FFTs and running sums, which gave spurious CC near the mainshock),
each station's CC trace shifted by its moveout, NCC = mean over the template's stations with data; detections = local
maxima >= 9 x MAD of that template-day NCC, >= 2 s apart; controls declustered at +/-2 s (keep the highest NCC).
Each job also records its raw maximum NCC over all samples and templates (no threshold, no declustering).
Runtime: about 95 min for `run 12` (claimant, 14-core machine); about 2-3 GB of disk."""
import os, sys, json, math, glob, hashlib, time, urllib.request, urllib.error, datetime as dt
import numpy as np, scipy.fft as F
from scipy.signal import find_peaks
HERE = os.path.dirname(os.path.abspath(__file__)); CL = os.path.abspath(os.path.join(HERE, ".."))
W = os.environ.get("NULLWORK", os.path.join(CL, "nullwork")); U = dt.timezone.utc
FS = 20.0; N = 86400 * 20; L = 120; FFTN = 16384; STEP = FFTN - L + 1
STA = ["NN.YER..HHZ", "NN.PNT..HHZ", "NN.BFC..HHZ", "NN.WASH..HHZ", "NN.REDF..HHZ", "NN.BMHS..HHZ", "NN.CMK6..HHZ", "NN.KVN..HHZ"]
DAYS = ["2024-12-09", "2024-12-10", "2024-12-11", "2024-12-12"]
EVENT_T = dt.datetime(2024, 12, 9, 23, 20, 12, 750000, tzinfo=U).timestamp()   # aligned detection time (template origin)
T_MAIN = dt.datetime(2024, 12, 9, 23, 8, 31, tzinfo=U).timestamp(); SPAN = (T_MAIN + 300, T_MAIN + 72 * 3600)
UA = "V3R1T4S-research (+https://github.com/elder-plinius/V3R1T4S)"
def fetch():
    os.makedirs(os.path.join(W, "wf"), exist_ok=True); log = os.path.join(W, "wf", "_fetchlog.jsonl")
    for s in STA:
        net, sta, loc, cha = s.split(".")
        for d in DAYS:
            fn = os.path.join(W, "wf", s, d + ".mseed"); os.makedirs(os.path.dirname(fn), exist_ok=True)
            if os.path.exists(fn): continue
            e = (dt.date.fromisoformat(d) + dt.timedelta(days=1)).isoformat()
            u = "https://service.earthscope.org/fdsnws/dataselect/1/query?net=%s&sta=%s&loc=--&cha=%s&starttime=%sT00:00:00&endtime=%sT00:00:00&nodata=404" % (net, sta, cha, d, e)
            try:
                with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=900) as q: st, b = q.status, q.read()
            except urllib.error.HTTPError as x: st, b = x.code, b""
            except Exception as x: st, b = "ERR " + type(x).__name__, b""
            open(log, "a").write(json.dumps({"url": u, "fetch_time": dt.datetime.now(U).strftime("%Y-%m-%dT%H:%M:%SZ"), "http_status": st, "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest() if b else None}) + "\n")
            if st in (401, 403, 429, 503): sys.exit("STOP: HTTP %s on %s (do not retry)" % (st, u))
            if st == 200 and b: open(fn, "wb").write(b)
            print("fetched", s, d, st, len(b), flush=True); time.sleep(0.3)
def prep_one(fn):
    import obspy
    sta = os.path.basename(os.path.dirname(fn)); day = os.path.basename(fn)[:10]; out = os.path.join(W, "wf20", sta, day + ".npy")
    if os.path.exists(out): return sta, day, "cached"
    os.makedirs(os.path.dirname(out), exist_ok=True); st = obspy.read(fn).select(component="Z")
    sr = st[0].stats.sampling_rate; st = st.select(sampling_rate=sr)
    t0 = obspy.UTCDateTime(day); st.merge(method=0, fill_value=None); tr = st[0]; tr.trim(t0, t0 + 86400 - 1 / sr, pad=True, fill_value=None)
    x = tr.data; mask = np.ma.getmaskarray(x) if np.ma.isMaskedArray(x) else np.zeros(len(x), bool); x = np.asarray(np.ma.filled(x.astype(np.float64), np.nan) if np.ma.isMaskedArray(x) else x, dtype=np.float64)
    good = ~mask & np.isfinite(x)
    x[~good] = np.mean(x[good]); x[good] -= np.mean(x[good]); x[~good] = 0.0
    tr.data = x; tr.taper(0.05, type="cosine"); tr.filter("bandpass", freqmin=2.0, freqmax=8.0, corners=4, zerophase=True)
    f = sr / FS
    if abs(f - round(f)) < 1e-9: tr.decimate(int(round(f)), no_filter=True)
    else: tr.resample(FS)
    y = np.zeros(N, np.float32); n = min(N, len(tr.data)); y[:n] = tr.data[:n]
    g = np.zeros(N, bool); gi = np.flatnonzero(~good)
    if len(gi):
        idx = np.unique(np.clip((gi / f).astype(np.int64), 0, N - 1)); g[idx] = True
        k = int(FS); g = np.convolve(g.astype(np.int8), np.ones(2 * k + 1, np.int8), mode="same") > 0
    g[n:] = True; y[g] = 0.0
    np.save(out, y); np.save(out.replace(".npy", ".gap.npy"), g); return sta, day, "ok"
def load_day(day):
    D = {}
    for s in STA:
        fn = os.path.join(W, "wf20", s, day + ".npy")
        if os.path.exists(fn): D[s] = (np.load(fn), np.load(fn.replace(".npy", ".gap.npy")))
    return D
def window_norm(x, B=65536):
    """sqrt(sum (x - mean)^2) over every L-sample window, computed directly in float64 (no running sums: after the
    mainshock the dynamic range reaches about 1e16, where cumulative-sum differences lose all precision)."""
    v = np.lib.stride_tricks.sliding_window_view(np.asarray(x, np.float64), L); den = np.empty(len(v))
    for lo in range(0, len(v), B):
        blk = v[lo:lo + B]; d = blk - blk.mean(axis=1, keepdims=True); den[lo:lo + B] = np.sqrt(np.einsum("ij,ij->i", d, d))
    return den
def prep_station(x, g):
    nk = int(math.ceil((N - L + 1) / STEP)); pad = np.zeros(nk * STEP + L - 1 + FFTN, np.float64); pad[:N] = x
    idx = np.arange(nk)[:, None] * STEP + np.arange(FFTN)[None, :]; Xc = F.rfft(pad[idx], axis=1)
    den = window_norm(x)
    cg = np.concatenate([[0], np.cumsum(g.astype(np.int32))]); bad = (cg[L:] - cg[:-L]) > 0
    den[bad] = 0.0; pos = den[den > 0]
    if len(pos): den[den < 1e-3 * float(np.median(pos))] = 0.0
    return Xc, den, nk
def xcorr(P, w):
    Xc, den, nk = P; Tf = F.rfft(np.asarray(w, np.float64), FFTN); y = F.irfft(Xc * np.conj(Tf)[None, :], FFTN, axis=1)[:, :STEP].ravel()[:N - L + 1]
    nt = math.sqrt(sum(v * v for v in w)); out = np.zeros(N - L + 1, np.float64); ok = den > 0; out[ok] = y[ok] / (den[ok] * nt); out[np.abs(out) > 1.0001] = 0.0; return out
def aligned(P, tp, s):
    cc = xcorr(P[s], tp["st"][s]["w"]); m = tp["st"][s]["m"]; a = np.zeros(N, np.float64)
    if m >= 0: a[:N - L + 1 - m] = cc[m:]
    else: a[-m:] = cc[:N - L + 1 + m]
    return a
def run_day(day, T, shifts=None):
    D = load_day(day)
    if shifts: D = {s: (np.roll(v[0], shifts.get(s, 0)), np.roll(v[1], shifts.get(s, 0))) for s, v in D.items()}
    P = {s: prep_station(*v) for s, v in D.items()}; t0 = dt.datetime.fromisoformat(day).replace(tzinfo=U).timestamp(); dets = []; mx = {"ncc": -1.0}
    for tp in T:
        use = [s for s in tp["st"] if s in P]
        if len(use) < 3: continue
        A = {s: aligned(P, tp, s) for s in use}; ncc = np.mean([A[s] for s in use], axis=0)
        i = int(np.argmax(ncc))
        if ncc[i] > mx["ncc"]: mx = {"ncc": round(float(ncc[i]), 4), "tpl": tp["id"], "t": t0 + i / FS}
        mad = float(np.median(np.abs(ncc - np.median(ncc)))); thr = 9 * mad
        if thr <= 0: continue
        pk, _ = find_peaks(ncc, height=thr, distance=40)
        dets += [{"t": t0 + i / FS, "tpl": tp["id"], "ncc": round(float(ncc[i]), 4)} for i in pk]
    return dets, mx
def worker(job):
    day, shifts, tag = job; os.makedirs(os.path.join(W, "out", tag), exist_ok=True)
    fn = os.path.join(W, "out", tag, day + ("_" + "_".join("%s%d" % (k.split(".")[1], v // 1200) for k, v in sorted(shifts.items())) if shifts else "") + ".json")
    if not os.path.exists(fn):
        T = json.load(open(os.path.join(CL, "data", "templates.json")))["templates"]; dets, mx = run_day(day, T, shifts or None); json.dump({"day": day, "shifts": shifts, "dets": dets, "max": mx}, open(fn, "w"))
    return fn
def decluster(dets):
    keep = []
    for d in sorted(dets, key=lambda d: -d["ncc"]):
        if all(abs(d["t"] - k["t"]) > 2 for k in keep): keep.append(d)
    return keep
if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "fetch": fetch()
    elif mode == "prep":
        from multiprocessing import Pool
        with Pool(8) as p: res = p.map(prep_one, sorted(glob.glob(os.path.join(W, "wf", "*", "*.mseed"))))
        print("prepared", len(res), "station-days")
    elif mode == "run":
        from multiprocessing import Pool
        jobs = [(d, {}, "real") for d in DAYS] + [tuple(j[:2]) + ("null",) for j in json.load(open(os.path.join(CL, "data", "null_jobs.json")))] + [tuple(j[:2]) + ("null_d9",) for j in json.load(open(os.path.join(CL, "data", "null_d9_jobs.json")))]
        with Pool(int(sys.argv[2]) if len(sys.argv) > 2 else 8, maxtasksperchild=20) as p:
            for i, _ in enumerate(p.imap_unordered(worker, jobs)):
                if i % 50 == 0: print("done", i + 1, "of", len(jobs), dt.datetime.now(U).strftime("%H:%M:%SZ"), flush=True)
        print("run FINISHED", len(jobs))
    elif mode == "summary":
        real = [d for f in glob.glob(os.path.join(W, "out", "real", "*.json")) for d in json.load(open(f))["dets"]]
        ev = max([d for d in real if abs(d["t"] - EVENT_T) <= 0.5], key=lambda d: d["ncc"]); c = ev["ncc"]
        print("event: best real detection within 0.5 s of 2024-12-09T23:20:12.75: NCC %.4f (template %s, %s)" % (c, ev["tpl"], dt.datetime.fromtimestamp(ev["t"], U).strftime("%H:%M:%S.%f")[:11]))
        tot = 0; best = 0; ge = 0
        for tag in ("null", "null_d9"):
            fs = sorted(glob.glob(os.path.join(W, "out", tag, "*.json"))); vals = [d["ncc"] for f in fs for d in decluster(json.load(open(f))["dets"])]
            print("%-8s controls %d, declustered detections %d, best %.4f, >= %.4f: %d" % (tag, len(fs), len(vals), max(vals), c, sum(v >= c for v in vals)))
            tot += len(fs); best = max(best, max(vals)); ge += sum(v >= c for v in vals)
        print("ALL: controls %d, best_control %.4f, count >= event NCC %d, EFC over the 3.0-day span = %d x 3.0 / %d = %.4f (95%% upper bound %.4f)" % (tot, best, ge, ge, tot, ge * 3.0 / tot, 3 * 3.0 / tot))
        rows = []
        for tag in ("null", "null_d9"):
            for f in sorted(glob.glob(os.path.join(W, "out", tag, "*.json"))):
                j = json.load(open(f)); m = j["max"]
                rows.append((tag, j["day"], ";".join("%s:%d" % (k.split(".")[1], v) for k, v in sorted(j["shifts"].items())), m["ncc"], m["tpl"], dt.datetime.fromtimestamp(m["t"], U).strftime("%Y-%m-%dT%H:%M:%S.%f")[:22]))
        rows.sort(key=lambda r: -r[3])
        with open(os.path.join(W, "null_per_control_max.csv"), "w") as o:
            o.write("set,day,shifts_samples_20Hz,max_ncc,template,time_utc\n"); o.writelines("%s,%s,%s,%.4f,%s,%s\n" % r for r in rows)
        print("raw per-control maxima: best %.4f (%s %s), 12-09 best %.4f, 12-10..12 best %.4f, >= event NCC: %d; written to null_per_control_max.csv" % (rows[0][3], rows[0][0], rows[0][1], max(r[3] for r in rows if r[0] == "null_d9"), max(r[3] for r in rows if r[0] == "null"), sum(r[3] >= c for r in rows)))
        json.dump(sorted(real, key=lambda d: d["t"]), open(os.path.join(W, "real_detections.json"), "w"))
        near = sorted([d for d in real if abs(d["t"] - EVENT_T) <= 30], key=lambda d: d["t"])
        json.dump(near, open(os.path.join(W, "detections_within_30s.json"), "w"), indent=0)
        print("real detections: %d over the 4 days (real_detections.json); %d within +/-30 s of the event (detections_within_30s.json)" % (len(real), len(near)))
