"""Summarize the PREREG.v5 repair map: as summarize_map.py, with the OVERLAP class (rule 3) outside the USABLE denominator,
the chance-corrected excess, the v4 comparison and the PREREG.v3 main-win check."""
import os, sys, json, glob, math, collections
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, '..', '..', '..')
sys.path.insert(0, os.path.join(R, 'lib'))
import numpy as np, pandas as pd, tt
O = os.environ.get('V3_MAPOUT') or os.path.join(H, '..', 'out')
ev = []
for f in glob.glob(os.path.join(R, 'data', 'ncei_events_2015_2026_p*.json')):
    ev += json.load(open(f))['items']
ev = pd.DataFrame(ev)
ev['date'] = pd.to_datetime(dict(year=ev.year, month=ev.month.fillna(1), day=ev.day.fillna(1)), errors='coerce')


def listed(t, lat, lon):
    t = pd.Timestamp(t).tz_convert(None) if pd.Timestamp(t).tzinfo else pd.Timestamp(t)
    near = ev[((ev.date - t.normalize()).dt.days.abs() <= 1) | (ev.day.isna() & (ev.year == t.year) & (ev.month == t.month))]
    km = tt.gc_km(lat, lon, near.latitude.values, near.longitude.values)
    return near[(km <= 1000) | near.latitude.isna()]


q = pd.read_csv(os.path.join(R, 'data', 'comcat', 'm65_d70_2015_2025.csv'))
q = q[q.type == 'earthquake'].copy()
q['alt'] = tt.alt_at(q.latitude.values, q.longitude.values)
rows, missing = [], []
for _, e in q[q.alt < 0].iterrows():
    fn = os.path.join(O, 'quakes', f"{e['id']}.json")
    L = listed(e.time, e.latitude, e.longitude)
    if not os.path.exists(fn):
        missing.append(e['id'])
        rows.append(dict(id=e['id'], time=e.time, lat=e.latitude, lon=e.longitude, depth=e.depth, mag=e.mag, place=e.place,
                         listed=len(L) > 0, listed_v4=bool((L.eventValidity == 4).any()), ncei_ids=';'.join(map(str, L.id)),
                         ncei_validity=';'.join(map(str, L.eventValidity)), real_cls='NOT_PROCESSED', fake5_cls='NOT_PROCESSED',
                         fake7_cls='NOT_PROCESSED', error='not processed (PREREG.v4 budget or time stop)'))
        continue
    d = json.load(open(fn))
    row = dict(id=e['id'], time=e.time, lat=e.latitude, lon=e.longitude, depth=e.depth, mag=e.mag, place=e.place,
               listed=len(L) > 0, listed_v4=bool((L.eventValidity == 4).any()), ncei_ids=';'.join(map(str, L.id)),
               ncei_validity=';'.join(map(str, L.eventValidity)))
    for nm in ('real', 'fake5', 'fake7'):
        s = d.get('summary', {}).get(nm, {})
        row[f'{nm}_cls'] = s.get('cls', 'ERROR' if 'error' in d else 'NO_GAUGE')
        row[f'{nm}_usable_sites'] = s.get('n_usable', 0)
        row[f'{nm}_detect_sites'] = s.get('n_detect', 0)
        row[f'{nm}_pass_sites'] = s.get('n_pass', 0)
    row['sites_in_scope'] = d.get('summary', {}).get('real', {}).get('n_sites', 0)
    row['passing'] = ';'.join(f"{g['code']}:r{g['res']['real']['r']}:dt{round(g['res']['real']['arrival'] - g['eta'], 1)}"
                              for g in d.get('gauges', []) if g.get('res', {}).get('real', {}).get('passes'))
    row['error'] = d.get('error', '')
    rows.append(row)
m = pd.DataFrame(rows).sort_values('time')
m.to_csv(os.path.join(O, 'map.csv'), index=False)
N = 264
out = [f'quakes in population (subsea): {N}; rows: {len(m)}; processed: {len(m) - len(missing)}; NOT_PROCESSED: {len(missing)} {missing}']
c = collections.Counter(m.real_cls)
out.append(f'real classes: {dict(c)}')
U = m[m.real_cls.isin(['SIGNAL', 'NO_SIGNAL', 'SIGNAL_UNDECIDED'])]
S = int((m.real_cls == 'SIGNAL').sum()); nU = len(U); und = int((m.real_cls == 'SIGNAL_UNDECIDED').sum())


def wilson(k, n, z=1.96):
    if n == 0:
        return (float('nan'),) * 2
    p = k / n; d = 1 + z * z / n; cen = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return cen - h, cen + h


lo, hi = wilson(S, nU)
nd = int(c.get('NO_DATA', 0)); ng = int(c.get('NO_GAUGE', 0)); er = int(c.get('ERROR', 0)); npr = int(c.get('NOT_PROCESSED', 0)); nov = int(c.get('OVERLAP', 0))
out.append(f'HEADLINE: SIGNAL / USABLE = {S} / {nU} = {S / max(1, nU):.3f} (Wilson 95 % {lo:.3f}-{hi:.3f}); SIGNAL_UNDECIDED {und}')
out.append(f'over all {N}: SIGNAL / {N} = {S / N:.3f}; bounds [{S / N:.3f}, {(S + und + nd + ng + er + npr + nov) / N:.3f}] (OVERLAP {nov}, NO_DATA {nd}, NO_GAUGE {ng}, ERROR {er}, NOT_PROCESSED {npr})')
t2 = pd.crosstab(U.real_cls, U.listed.map({True: 'LISTED', False: 'not listed'}))
out.append('SIGNAL x LISTED over USABLE quakes:\n' + t2.to_string())
t2v = pd.crosstab(U.real_cls, U.listed_v4.map({True: 'LISTED validity 4', False: 'not validity 4'}))
out.append('SIGNAL x LISTED(validity 4) over USABLE quakes:\n' + t2v.to_string())
out.append(f"LISTED among NO_DATA: {int(m[m.real_cls == 'NO_DATA'].listed.sum())} of {nd}; among NO_GAUGE: {int(m[m.real_cls == 'NO_GAUGE'].listed.sum())} of {ng}")
out.append(f"LISTED among OVERLAP: {int(m[m.real_cls == 'OVERLAP'].listed.sum())} of {nov}: " + ', '.join(f"{r['id']}({'L' if r.listed else '-'})" for _, r in m[m.real_cls == 'OVERLAP'].iterrows()))
single = U[(U.real_cls == 'SIGNAL') & (U.real_pass_sites == 1)]
out.append(f'single-site SIGNALs: {len(single)} of {S} (never claims of a missed tsunami)')
m['band'] = ((m.lon + 180) // 30 * 30 - 180).astype(int)
bt = m.groupby('band').apply(lambda g: pd.Series(dict(n=len(g), usable=int(g.real_cls.isin(['SIGNAL', 'NO_SIGNAL', 'SIGNAL_UNDECIDED']).sum()),
                                                        signal=int((g.real_cls == 'SIGNAL').sum()), listed=int(g.listed.sum()))))
out.append('by 30-degree longitude band (west edge):\n' + bt.to_string())
# fake-origin null
rng = np.random.default_rng(20261024)
fk = m[m.real_cls != 'NOT_PROCESSED'][['fake5_cls', 'fake7_cls']].values
fr = []
for _ in range(400):
    pick = fk[np.arange(len(fk)), rng.integers(0, 2, len(fk))]
    u = np.isin(pick, ['SIGNAL', 'NO_SIGNAL', 'SIGNAL_UNDECIDED'])
    fr.append((pick == 'SIGNAL').sum() / max(1, u.sum()))
fr = np.array(fr)
real = S / max(1, nU)
f5u = m.fake5_cls.isin(['SIGNAL', 'NO_SIGNAL', 'SIGNAL_UNDECIDED']); f7u = m.fake7_cls.isin(['SIGNAL', 'NO_SIGNAL', 'SIGNAL_UNDECIDED'])
rate = ((m.fake5_cls == 'SIGNAL').sum() + (m.fake7_cls == 'SIGNAL').sum()) / max(1, f5u.sum() + f7u.sum())
out.append(f'fake-origin null: fake SIGNAL at o-5h {int((m.fake5_cls == "SIGNAL").sum())}/{int(f5u.sum())}, at o-7h {int((m.fake7_cls == "SIGNAL").sum())}/{int(f7u.sum())}; '
           f'pooled fake rate {rate:.4f}; expected chance SIGNALs among {nU} real USABLE quakes {rate * nU:.1f}')
out.append(f'400 fake catalogues: max {fr.max():.4f}, mean {fr.mean():.4f}; real {real:.4f}; real beats all: {bool(real > fr.max())}')
pf = ((U.fake5_cls == 'SIGNAL').astype(float) + (U.fake7_cls == 'SIGNAL').astype(float)) / 2
out.append(f'chance-corrected: expected chance SIGNALs (pooled rate) {rate * nU:.1f}, (per-quake fake means) {pf.sum():.1f}; '
           f'excess {S - rate * nU:.1f} = {(S - rate * nU) / max(1, nU):.3f} of USABLE')
v4 = pd.read_csv(os.path.join(R, 'attempts', 'completeness-map', 'out', 'map.csv'))[['id', 'real_cls']].rename(columns={'real_cls': 'v4_cls'})
mm = m.merge(v4, on='id')
out.append('v4 -> v5 real class transitions:\n' + pd.crosstab(mm.v4_cls, mm.real_cls).to_string())
out.append('v4 SIGNAL quakes not SIGNAL in v5: ' + ', '.join(f"{r['id']}->{r.real_cls}" for _, r in mm[(mm.v4_cls == 'SIGNAL') & (mm.real_cls != 'SIGNAL')].iterrows()))
mw = m[(m.real_cls == 'SIGNAL') & (~m.listed) & (m.real_pass_sites >= 2)]
out.append(f'PREREG.v3 main-win candidates under v5 (unlisted, >= 2 passing sites): {len(mw)} {list(mw.id)}')
open(os.path.join(O, 'map_summary.txt'), 'w').write('\n'.join(out) + '\n')
json.dump(dict(controls=400, best_control=round(float(fr.max()), 4), real=round(real, 4), real_beats_all=bool(real > fr.max()),
               fake_rate=round(float(rate), 4), S=S, USABLE=nU, N=N), open(os.path.join(O, 'null.json'), 'w'), indent=1)
# LISTED quakes: NCEI tide-gauge rows at codes in scope (within 5 km), rule misses kept apart from detection misses
tgr = collections.defaultdict(list)
for f in glob.glob(os.path.join(R, 'data', 'ncei_tg', 'ev', '*.json')):
    for x in json.load(open(f)).get('items', []):
        tgr[x['tsunamiEventId']].append(x)
rc = collections.Counter(); qc = collections.Counter(); per = []
for _, r in m[m.listed & (m.real_cls != 'NOT_PROCESSED')].iterrows():
    fn = os.path.join(O, 'quakes', f"{r['id']}.json"); d = json.load(open(fn)); G = d.get('gauges', [])
    outs = []; seen = set()
    for eid in str(r.ncei_ids).split(';'):
        for x in tgr.get(int(eid), []) if eid else []:
            if x.get('latitude') is None or x.get('longitude') is None:
                continue
            for g in G:
                if tt.gc_km(x['latitude'], x['longitude'], g['lat'], g['lon']) <= 5.0 and (x['id'], g['site']) not in seen:
                    seen.add((x['id'], g['site']))
                    R_ = g.get('res', {}).get('real', {})
                    if not R_.get('usable'):
                        o = 'NO_DATA'
                    elif R_.get('passes'):
                        o = 'PASS'
                    elif R_.get('detects'):
                        o = 'DETECT_ctrl_fail' if not R_.get('undecided') else 'DETECT_ctrl_undecided'
                    elif R_.get('r', 0) > 5:
                        o = 'r>5_arrival_outside_10'
                    else:
                        o = 'r<=5'
                    th, tm = x.get('travHours'), x.get('travMins')
                    ttn = None if th is None and tm is None else 60 * (th or 0) + (tm or 0)
                    rm = None if not ttn else abs(ttn - g['eta']) > 10
                    outs.append((o, rm))
                    rc[o] += 1
                    if rm is not None:
                        rc['rows with NCEI travel time'] += 1; rc['rule miss (|NCEI tt - ETA| > 10)'] += rm
                        if rm and o not in ('PASS', 'NO_DATA'):
                            rc['rule-miss rows not PASS (usable)'] += 1
                    per.append(f"  {r['id']} M{r.mag} {str(r.place)[:30]:30s} NCEI {eid} {x.get('locationName', '')[:22]:22s} -> {g['code']:7s} eta {g['eta']:6.1f} ncei_tt {ttn} r {R_.get('r')} arr {R_.get('arrival')} {o}")
    if r.real_cls in ('SIGNAL', 'NO_SIGNAL', 'SIGNAL_UNDECIDED'):
        if not outs:
            qc[f'{r.real_cls}: no NCEI tide-gauge row in scope'] += 1
        elif r.real_cls == 'SIGNAL':
            qc['SIGNAL with NCEI rows in scope'] += 1
        else:
            tts = [rm for o, rm in outs if rm is not None]
            if tts and all(tts):
                qc[f'{r.real_cls}: every NCEI row with a travel time is a rule miss'] += 1
            elif not tts:
                qc[f'{r.real_cls}: NCEI rows in scope, none with a travel time'] += 1
            else:
                qc[f'{r.real_cls}: >= 1 NCEI row within 10 min of ETA (detection miss)'] += 1
out.append(f'LISTED quakes, NCEI tide-gauge rows at codes in scope (<= 5 km, dedup per row and site): {dict(rc)}')
out.append(f'LISTED USABLE quakes by miss type: {dict(qc)}')
open(os.path.join(O, 'listed_rows.txt'), 'w').write('\n'.join(per) + '\n')
open(os.path.join(O, 'map_summary.txt'), 'w').write('\n'.join(out) + '\n')
# land-epicentre quakes that NCEI lists (not in the denominator)
land = []
for _, e in q[q.alt >= 0].iterrows():
    L = listed(e.time, e.latitude, e.longitude)
    if len(L):
        land.append(f"  {e['id']} {e.time[:10]} M{e.mag} {e.place} alt {int(e.alt)} m -> NCEI {list(L.id)} validity {list(L.eventValidity)}")
open(os.path.join(O, 'land_listed.txt'), 'w').write(f'land-epicentre quakes ({int((q.alt >= 0).sum())}) with an NCEI event within +/-1 day and 1000 km: {len(land)}\n' + '\n'.join(land) + '\n')
print('\n'.join(out)); print(f'land-epicentre listed: {len(land)}')
