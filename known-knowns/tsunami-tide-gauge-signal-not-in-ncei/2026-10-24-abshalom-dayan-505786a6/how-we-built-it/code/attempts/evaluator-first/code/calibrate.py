"""PREREG.md section 1: calibrate the travel-time model on NCEI tide-gauge travel times of 2005-2011 events, then report
2012-2014 and 2015-2026 once. Writes out/tt_rows.csv, out/tt_selected.json, out/calibrate.txt."""
import sys, os, json, glob
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, '..', '..', '..')
sys.path.insert(0, os.path.join(R, 'lib'))
import numpy as np, pandas as pd, tt
O = os.environ.get('V3_CALOUT') or os.path.join(H, '..', 'out')
ev = []
for f in glob.glob(os.path.join(R, 'data', 'ncei_events_20*.json')):
    ev += json.load(open(f)).get('items', [])
ev = {e['id']: e for e in ev}
rows = []
for f in glob.glob(os.path.join(R, 'data', 'ncei_tg', 'ev', '*.json')):
    rows += json.load(open(f))['items']
df = pd.DataFrame(rows).drop_duplicates('id')
df = df[df.typeMeasurementId == 2]
df['ev_valid'] = df.tsunamiEventId.map(lambda i: ev.get(i, {}).get('eventValidity'))
df['ev_cause'] = df.tsunamiEventId.map(lambda i: ev.get(i, {}).get('causeCode'))
df['ev_lat'] = df.tsunamiEventId.map(lambda i: ev.get(i, {}).get('latitude'))
df['ev_lon'] = df.tsunamiEventId.map(lambda i: ev.get(i, {}).get('longitude'))
df['ev_mag'] = df.tsunamiEventId.map(lambda i: ev.get(i, {}).get('eqMagnitude'))
df['ev_year'] = df.tsunamiEventId.map(lambda i: ev.get(i, {}).get('year'))
has = df.travHours.notna() | df.travMins.notna() if 'travMins' in df else df.travHours.notna()
df = df[has].copy()
df['ncei_tt'] = 60 * df.travHours.fillna(0) + df.travMins.fillna(0)
df = df[(df.ev_cause == 1) & (df.ev_valid == 4) & df.latitude.notna() & df.ev_lat.notna()]
df = df[(df.ncei_tt >= 15) & (df.ncei_tt <= 150)]
df['set'] = np.where(df.ev_year <= 2011, 'cal', np.where(df.ev_year <= 2014, 'pc', 'hold'))
print('rows', len(df), df.groupby('set').size().to_dict(), 'events', df.groupby('set').tsunamiEventId.nunique().to_dict(), flush=True)
DM = [1, 10, 20, 50]
for d in DM:
    df[f'm{d}'] = np.nan; df[f'sd{d}'] = np.nan
for e, g in df.groupby('tsunamiEventId'):
    try:
        f = tt.FMM(float(g.ev_lat.iloc[0]), float(g.ev_lon.iloc[0]), radius_km=1700)
    except RuntimeError as ex:
        print('event', e, ex, flush=True); continue
    for i, r in g.iterrows():
        for d in DM:
            t, sd, h = f.eta(r.latitude, r.longitude, dmin=d)
            df.loc[i, f'm{d}'] = t; df.loc[i, f'sd{d}'] = sd
df.to_csv(os.path.join(O, 'tt_rows.csv'), index=False)
out = []
cal = df[df.set == 'cal']
best = None
for d in DM:
    x = cal[cal[f'm{d}'].notna()]
    c = round(float(np.median(x.ncei_tt - x[f'm{d}'])), 1)
    share = float(np.mean(np.abs(x.ncei_tt - (x[f'm{d}'] + c)) <= 10))
    share0 = float(np.mean(np.abs(x.ncei_tt - x[f'm{d}']) <= 10))
    out.append(f'cal dmin {d:3d} m: n {len(x)} ({x.tsunamiEventId.nunique()} events), c {c:+.1f} min, within 10 with c {share:.3f}, without c {share0:.3f}')
    key = (share, -abs(c))
    if best is None or key > best[0]:
        best = (key, d, c)
_, D, C = best
sel = dict(dmin=D, c=C, rule='largest calibration share within +/-10 min; ties to smaller |c|')
json.dump(sel, open(os.path.join(O, 'tt_selected.json'), 'w'), indent=1)
out.append(f'SELECTED dmin {D} m, c {C:+.1f} min')
rng = np.random.default_rng(20261024)


def report(x, label):
    x = x[x[f'm{D}'].notna()].copy()
    if x.empty:
        out.append(f'{label}: no rows'); return
    x['err'] = x.ncei_tt - (x[f'm{D}'] + C)
    w10 = np.abs(x.err) <= 10
    evs = x.tsunamiEventId.unique()
    boots = []
    for _ in range(2000):
        s = rng.choice(evs, len(evs))
        xx = pd.concat([x[x.tsunamiEventId == e] for e in s])
        boots.append(np.mean(np.abs(xx.err) > 10))
    lo, hi = np.percentile(boots, [2.5, 97.5])
    per = x.groupby('tsunamiEventId').apply(lambda g: pd.Series(dict(n=len(g), any10=(np.abs(g.err) <= 10).any(), all10=(np.abs(g.err) <= 10).all())))
    out.append(f'{label}: rows {len(x)} events {len(evs)}; outside +/-10 {1 - w10.mean():.3f} (95% CI {lo:.3f}-{hi:.3f}); '
               f'within 10 {w10.mean():.3f}, 15 {(np.abs(x.err) <= 15).mean():.3f}, 20 {(np.abs(x.err) <= 20).mean():.3f}; '
               f'median err (NCEI - ETA) {x.err.median():+.1f} min, IQR {x.err.quantile(.25):+.1f}..{x.err.quantile(.75):+.1f}; '
               f'events with >=1 row within 10: {int(per.any10.sum())}/{len(per)}, all rows within 10: {int(per.all10.sum())}/{len(per)}')
    for nm, m in (('M<7.5', x.ev_mag < 7.5), ('M>=7.5', x.ev_mag >= 7.5)):
        y = x[m]
        if len(y):
            out.append(f'   {nm}: rows {len(y)} events {y.tsunamiEventId.nunique()} outside +/-10 {np.mean(np.abs(y.err) > 10):.3f} median {y.err.median():+.1f}')


report(df[df.set == 'cal'], 'calibration 2005-2011 (selected model)')
report(df[df.set == 'pc'], 'reported once: 2012-2014')
report(df[df.set == 'hold'], 'reported once (hold-out): 2015-2026')
open(os.path.join(O, 'calibrate.txt'), 'w').write('\n'.join(out) + '\n')
print('\n'.join(out))
