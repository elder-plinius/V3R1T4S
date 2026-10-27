"""Early-hours null (run 2026-10-26-1727 PREREG.md L2 with PREREG.v2.md): a stated sensitivity, not the criterion's null.
Run from claim/ after `null_full.py fetch` (it reads the raw HHZ day files of 2024-12-09 and 2024-12-10):

    python -I code/early_null.py [NPROC] [NCONTROLS]      # defaults 12 and 3000

Window: 2024-12-09T23:13:31 to 2024-12-10T01:13:31 UTC (the first 2 h of the searched span, 5 min after the
mainshock), 144,000 samples at 20 Hz. Prep as null_full.py, on one continuous 22:00-02:30 segment per station (gap
mask, demean, 5 % cosine taper, 2-8 Hz 4-pole zero-phase Butterworth, decimate to 20 Hz), then cut to the window.
Statistic: per template and station, circular normalised CC over the window (float64 FFT numerator; each window's
norm computed directly), circularly aligned by the moveout; NCC = mean over the template's stations with data (>= 3);
a control's value is the maximum NCC over all samples and all 385 templates. E2 = the maximum NCC of the unshifted data
within +/-0.5 s of 23:20:12.75 (the event's aligned time). Controls: seed 20261026; YER unshifted; the other 7
stations shifted circularly by integers drawn uniformly from [12000, 132000], redrawn until all 8 are pairwise
>= 12,000 samples (10 min) apart in circular distance. EFC_early = count(control >= E2) / NCONTROLS x 36 (72 h / 2 h).
Writes nullwork/early/ (per-control maxima CSV and a summary)."""
import os, sys, json, datetime as dt
import numpy as np, scipy.fft as F
HERE = os.path.dirname(os.path.abspath(__file__)); CL = os.path.abspath(os.path.join(HERE, ".."))
W = os.environ.get("NULLWORK", os.path.join(CL, "nullwork")); OUT = os.path.join(W, "early"); U = dt.timezone.utc
FS = 20.0; L = 120; NW = 144000; SEED = 20261026; SHMIN, SHMAX = 12000, 132000
STA = ["NN.YER..HHZ", "NN.PNT..HHZ", "NN.BFC..HHZ", "NN.WASH..HHZ", "NN.REDF..HHZ", "NN.BMHS..HHZ", "NN.CMK6..HHZ", "NN.KVN..HHZ"]
SEG0, SEG1 = "2024-12-09T22:00:00", "2024-12-10T02:30:00"; WIN0 = "2024-12-09T23:13:31"; EVENT = "2024-12-09T23:20:12.75"

def prep_window(s):
    import obspy
    st = obspy.Stream()
    for d in ("2024-12-09", "2024-12-10"):
        fn = os.path.join(W, "wf", s, d + ".mseed")
        if os.path.exists(fn): st += obspy.read(fn).select(component="Z")
    if not len(st): return None
    sr = st[0].stats.sampling_rate; st = st.select(sampling_rate=sr); st.merge(method=0, fill_value=None); tr = st[0]
    t0, t1 = obspy.UTCDateTime(SEG0), obspy.UTCDateTime(SEG1); tr.trim(t0, t1 - 1 / sr, pad=True, fill_value=None)
    x = tr.data; mask = np.ma.getmaskarray(x) if np.ma.isMaskedArray(x) else np.zeros(len(x), bool)
    x = np.asarray(np.ma.filled(x.astype(np.float64), np.nan) if np.ma.isMaskedArray(x) else x, dtype=np.float64)
    good = ~mask & np.isfinite(x); x[~good] = np.mean(x[good]); x[good] -= np.mean(x[good]); x[~good] = 0.0
    tr.data = x; tr.taper(0.05, type="cosine"); tr.filter("bandpass", freqmin=2.0, freqmax=8.0, corners=4, zerophase=True)
    f = sr / FS
    if abs(f - round(f)) < 1e-9: tr.decimate(int(round(f)), no_filter=True)
    else: tr.resample(FS)
    n = int(round((t1 - t0) * FS)); y = np.zeros(n); m = min(n, len(tr.data)); y[:m] = tr.data[:m]
    g = np.zeros(n, bool); gi = np.flatnonzero(~good)
    if len(gi):
        idx = np.unique(np.clip((gi / f).astype(np.int64), 0, n - 1)); g[idx] = True
        k = int(FS); g = np.convolve(g.astype(np.int8), np.ones(2 * k + 1, np.int8), mode="same") > 0
    g[m:] = True; y[g] = 0.0
    i0 = int(round((obspy.UTCDateTime(WIN0) - t0) * FS))
    return y[i0:i0 + NW].astype(np.float32), g[i0:i0 + NW]

def circ_station(x, g):
    """FFT of the window and each circular window's norm (direct, float64); gap windows and near-zero norms -> 0."""
    x = np.asarray(x, np.float64); xp = np.concatenate([x, x[:L - 1]])
    v = np.lib.stride_tricks.sliding_window_view(xp, L)[:NW]; d = v - v.mean(axis=1, keepdims=True); den = np.sqrt(np.einsum("ij,ij->i", d, d))
    gp = np.concatenate([g, g[:L - 1]]).astype(np.int32); cg = np.concatenate([[0], np.cumsum(gp)]); den[(cg[L:L + NW] - cg[:NW]) > 0] = 0.0
    pos = den[den > 0]
    if len(pos): den[den < 1e-3 * float(np.median(pos))] = 0.0
    return F.rfft(x), den

def circ_cc(P, w):
    X, den = P; wp = np.zeros(NW); wp[:L] = w; num = F.irfft(X * np.conj(F.rfft(wp)), NW)
    nt = float(np.sqrt(np.dot(w, w))); out = np.zeros(NW); ok = den > 0; out[ok] = num[ok] / (den[ok] * nt); return out

def draw_shifts(n):
    rng = np.random.default_rng(SEED); jobs = []
    while len(jobs) < n:
        sh = rng.integers(SHMIN, SHMAX + 1, size=7); pts = np.concatenate([[0], sh])
        dd = np.abs(pts[:, None] - pts[None, :]); dd = np.minimum(dd, NW - dd); np.fill_diagonal(dd, NW)
        if dd.min() >= SHMIN: jobs.append({s: int(v) for s, v in zip(STA, pts)})
    return jobs

G = {}
def init(path):
    G["P"] = dict(np.load(path, allow_pickle=True).item())
def one_template(args):
    tp, jobs, kev = args; P = G["P"]; use = [s for s in tp["st"] if s in P]
    if len(use) < 3: return tp["id"], None, None, None
    A = {s: np.roll(circ_cc(P[s], np.asarray(tp["st"][s]["w"], np.float64)), -tp["st"][s]["m"]).astype(np.float32) for s in use}
    real = np.mean([A[s] for s in use], axis=0); e2 = float(real[kev - 10:kev + 11].max())
    acc = np.empty(NW, np.float32); mx = np.empty(len(jobs)); arg = np.empty(len(jobs), np.int64)
    for c, sh in enumerate(jobs):
        acc[:] = 0.0
        for s in use:
            k = sh[s]
            if k: acc[k:] += A[s][:NW - k]; acc[:k] += A[s][NW - k:]
            else: acc += A[s]
        i = int(np.argmax(acc)); mx[c] = acc[i] / len(use); arg[c] = i
    return tp["id"], e2, mx, arg

if __name__ == "__main__":
    nproc = int(sys.argv[1]) if len(sys.argv) > 1 else 12; nctl = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
    os.makedirs(OUT, exist_ok=True); T = json.load(open(os.path.join(CL, "data", "templates.json")))["templates"]
    pth = os.path.join(OUT, "stations.npy")
    if not os.path.exists(pth):
        P = {}
        for s in STA:
            r = prep_window(s)
            if r is not None: P[s] = circ_station(*r)
        np.save(pth, np.array(P, dtype=object), allow_pickle=True)
    jobs = draw_shifts(nctl); t0 = dt.datetime.fromisoformat(WIN0).replace(tzinfo=U)
    kev = int(round((dt.datetime.fromisoformat(EVENT).replace(tzinfo=U) - t0).total_seconds() * FS))
    from multiprocessing import Pool
    best = np.full(nctl, -1.0); btp = [""] * nctl; bk = np.zeros(nctl, np.int64); e2 = (-1.0, ""); done = 0
    with Pool(nproc, initializer=init, initargs=(pth,)) as p:
        for tid, e, mx, arg in p.imap_unordered(one_template, [(tp, jobs, kev) for tp in T], chunksize=2):
            done += 1
            if e is None: continue
            if e > e2[0]: e2 = (e, tid)
            up = mx > best; best[up] = mx[up]; bk[up] = arg[up]
            for c in np.flatnonzero(up): btp[c] = tid
            if done % 50 == 0: print("templates done", done, "of", len(T), dt.datetime.now(U).strftime("%H:%M:%SZ"), flush=True)
    with open(os.path.join(OUT, "early_per_control_max.csv"), "w") as o:
        o.write("control,shifts_samples_20Hz,max_ncc,template,time_utc\n")
        for c in np.argsort(-best):
            o.write("%d,%s,%.4f,%s,%s\n" % (c, ";".join("%s:%d" % (s.split(".")[1], v) for s, v in jobs[c].items() if v), best[c], btp[c], (t0 + dt.timedelta(seconds=bk[c] / FS)).strftime("%Y-%m-%dT%H:%M:%S.%f")[:22]))
    n = int((best >= e2[0]).sum())
    lines = ["window %s + %d samples at 20 Hz; templates %d; controls %d (seed %d)" % (WIN0, NW, len(T), nctl, SEED),
             "E2 (event, unshifted, +/-0.5 s of %s): %.4f (template %s)" % (EVENT, e2[0], e2[1]),
             "best control %.4f; controls >= E2: %d; EFC_early = %d / %d x 36 = %.4f" % (best.max(), n, n, nctl, n / nctl * 36)]
    open(os.path.join(OUT, "early_summary.txt"), "w").write("\n".join(lines) + "\n"); print("\n".join(lines))
