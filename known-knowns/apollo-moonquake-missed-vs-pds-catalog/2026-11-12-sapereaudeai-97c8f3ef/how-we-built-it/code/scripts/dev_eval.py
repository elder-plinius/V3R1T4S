"""DEV ONLY (1972 A1 event days). One detector configuration -> leave-one-out recall at the 1/day threshold.

usage: dev_eval.py LO HI L_S WHITEN STATIONS OUT_PREFIX
 1. Templates: iterative alignment/stacking (reference = largest A1+A2 catalogue amplitude; search +/- 240 s
    around the catalogued start; stack events with D >= 0.3; 4 iterations).
 2. Threshold theta: smallest value with declustered (+/- 5 min) detections on time-reversed dev days <= 1 per
    scanned day (full stack templates).
 3. Leave-one-out recall: each dev event scored with the stack that excludes it; recovered if max D over window
    starts with onset (start + 30 s) within +/- 300 s of the catalogued start is >= theta.
"""
import sys, json, time
sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', 'tools'))
import numpy as np
from apollo_lib import NS, COMPS, norm_template, decluster
from evlib import DayCache, load_nest_events, best_lag, event_block, FS
from scan import prep_day, corr_channels, reverse_prepped

lo, hi, L, WH = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
stations = sys.argv[5].split(','); out = sys.argv[6]
band = (lo, hi, WH) if WH else (lo, hi)
CAT = __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', '..', 'data', 'catalog', 'levent.1008weber.csv')
ev = load_nest_events(CAT, '1', ['72'])
cache = DayCache(band)
chans_all = []
for st in stations:  # 's12' or 's14:mh1+mh2'
    if ':' in st:
        a, b = st.split(':'); chans_all += [(a, c) for c in b.split('+')]
    else:
        chans_all += [(st, c) for c in COMPS]
M = int(round(L * FS))
T0 = time.time()

def unit(y):
    y = y - y.mean(); n = np.sqrt((y * y).sum()); return y / n if n > 0 else None

def contributions(starts):
    """per event index -> list over chans of unit-norm window or None"""
    con = {}
    for i, s in starts.items():
        blk = event_block(cache, chans_all, s, M)
        con[i] = [unit(y) if (y is not None and v.mean() >= 0.95) else None for y, v in blk]
    return con

def make_tm(con, include):
    tm = []
    for k in range(len(chans_all)):
        acc = [con[i][k] for i in include if con[i][k] is not None]
        tm.append(norm_template(np.sum(acc, axis=0)) if acc else None)
    return tm

def active(tm):
    ch = [c for c, t in zip(chans_all, tm) if t is not None]
    return ch, [t for t in tm if t is not None]

amp = ev['A1n'].clip(lower=0).fillna(0) + ev['A2n'].clip(lower=0).fillna(0)
ref = int(amp.idxmax())
blk = event_block(cache, chans_all, int(ev.loc[ref, 't_ns']), M)
tm = [norm_template(y) if (y is not None and v.mean() > 0.95) else None for y, v in blk]
for it in range(4):
    ch, tt = active(tm)
    found = {}
    for i, r in ev.iterrows():
        t = int(r['t_ns'])
        b = best_lag(cache, ch, tt, t - 240 * NS, t + 240 * NS)
        if b is not None:
            found[i] = (b[0], b[1])
    members = [i for i, (d, s) in found.items() if d >= 0.3]
    if len(members) < 3:
        members = sorted(found, key=lambda i: -found[i][0])[:5]
    con = contributions({i: found[i][1] for i in members})
    tm = make_tm(con, members)
# P onset on the stack: envelope of a longer stack window; shift all member starts so the window starts 30 s
# before the onset (PREREG), then re-stack
PRE = int(120 * FS)
long_starts = {i: found[i][1] - 120 * NS for i in members}
Ml = M + 2 * PRE
conl = {}
for i, s in long_starts.items():
    blk = event_block(cache, chans_all, s, Ml)
    conl[i] = [unit(y) if (y is not None and v.mean() >= 0.95) else None for y, v in blk]
E = np.zeros(Ml)
for k in range(len(chans_all)):
    acc = [conl[i][k] for i in members if conl[i][k] is not None]
    if acc:
        st = np.mean(acc, axis=0); E += st * st
w5 = int(5 * FS); Es = np.convolve(E, np.ones(w5) / w5, mode='same')
noise = np.median(Es[:int(60 * FS)])
above = np.flatnonzero(Es[int(60 * FS):] > 4 * noise)
onset_idx = int(60 * FS) + int(above[0]) if above.size else PRE + int(30 * FS)
onset_rel_s = (onset_idx - PRE) / FS  # onset relative to the old window start (s)
shift_ns = int((onset_rel_s - 30.0) * NS)
print('stack P onset at %+.1f s from the aligned window start; shifting windows by %+.1f s' % (onset_rel_s, shift_ns / NS))
con = contributions({i: found[i][1] + shift_ns for i in members})
tm = make_tm(con, members)
ch, tt = active(tm)
# threshold from reversed dev days
days = sorted({(1972, int(j)) for j in ev['JD']})
SEP = int(300 * FS); rev = []; ndays = 0.0; revmax = []
for (y, d) in days:
    pp = prep_day(y, d, ch, band, M)
    if sum(p is not None for p in pp) < 2:
        continue
    Dr, _, _ = corr_channels(reverse_prepped(pp), tt)
    ndays += float(np.mean(~np.isnan(Dr)))
    rev.extend(Dr[decluster(Dr, SEP, 0.0)].tolist())
    revmax.append(float(np.nanmax(Dr)))
rev = np.sort(np.array(rev))[::-1]
k = int(np.floor(ndays))
theta = float(rev[k]) + 1e-6 if len(rev) > k else 0.0
# leave-one-out recall
loo = {}
offs = {}
for i, r in ev.iterrows():
    tmi = make_tm(con, [j for j in members if j != i]) if i in members else tm
    chi, tti = active(tmi)
    t = int(r['t_ns'])
    b = best_lag(cache, chi, tti, t - 330 * NS, t + 270 * NS)  # onset = start + 30 s within +/- 300 s
    if b is not None:
        offs[i] = (b[1] + 30 * NS - t) / NS
    loo[i] = None if b is None else b[0]
vals = [v for v in loo.values() if v is not None]
rec = sum(v >= theta for v in vals)
summary = dict(band=band, L=L, stations=stations, members=len(members), chans=['%s.%s' % c for c in ch],
               theta=theta, scanned_days=ndays, rev_peaks=len(rev), rev_max=float(rev[0]) if len(rev) else None,
               loo_recall=rec, loo_n=len(vals), n_events=len(ev), median_loo_D=float(np.median(vals)),
               seconds=time.time() - T0, onset_rel_s=onset_rel_s,
               onset_minus_catalogue_s_median=float(np.median(list(offs.values()))))
print(json.dumps(summary))
np.savez(out + '.npz', tm=np.array(tt), chans=np.array(['%s.%s' % c for c in ch]), band=np.array(list(band) + ([0.0] if len(band) == 2 else [])), L=L,
         loo=np.array([loo[i] if loo[i] is not None else np.nan for i in range(len(ev))]),
         members=np.array(members), theta=theta)
json.dump(summary, open(out + '.json', 'w'))
