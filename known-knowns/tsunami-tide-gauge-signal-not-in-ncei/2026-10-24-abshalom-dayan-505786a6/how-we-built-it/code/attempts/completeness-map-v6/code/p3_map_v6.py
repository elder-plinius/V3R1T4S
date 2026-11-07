"""PREREG.v6: the p3 map with the implementation corrections (det.IMPL6 = True), under the v5 rules (the claimed map) or
the v4 rules (the pre-registered map). One JSON per quake (resumable).
usage: p3_map_v6.py <v5|v4> <shard> <nshards>
env: V3_MAPOUT (default ../out or ../out_v4rules), V3_IDS (comma list: only these quakes), V3_IMPL6=0 (as-run code, for checks)"""
import sys, os, json, time
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, '..', '..', '..')
sys.path.insert(0, os.path.join(R, 'lib'))
import numpy as np, pandas as pd, tt, det, det5
det.IMPL6 = os.environ.get('V3_IMPL6', '1') != '0'
rules, shard, nsh = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
assert rules in ('v5', 'v4')
O = os.environ.get('V3_MAPOUT') or os.path.join(H, '..', 'out' if rules == 'v5' else 'out_v4rules')
os.makedirs(os.path.join(O, 'quakes'), exist_ok=True)
ids = set(os.environ['V3_IDS'].split(',')) if os.environ.get('V3_IDS') else None
allq = pd.read_csv(os.path.join(R, 'data', 'comcat', 'm65_d70_2015_2025.csv'))
allq['t'] = pd.to_datetime(allq.time).dt.tz_convert(None)
q = allq[allq.type == 'earthquake'].copy()
q['alt'] = tt.alt_at(q.latitude.values, q.longitude.values)
q = q[q.alt < 0].sort_values('time').reset_index(drop=True)
assert len(q) == 264, len(q)


def overlap(e, oo):
    """v5 rule 3: another ComCat event (M >= 6.5, depth <= 70) in the 24 h before oo within 1000 km of e's epicentre."""
    w = allq[(allq['id'] != e['id']) & (allq.t >= oo - pd.Timedelta(hours=24)) & (allq.t < oo)]
    if w.empty:
        return []
    km = tt.gc_km(e.latitude, e.longitude, w.latitude.values, w.longitude.values)
    return [f"{i}@{(oo - t).total_seconds() / 3600:.2f}h/{k:.0f}km" for i, t, k in zip(w['id'], w.t, km) if k <= 1000]


for i, e in q.iterrows():
    if i % nsh != shard or (ids and e['id'] not in ids):
        continue
    fn = os.path.join(O, 'quakes', f"{e['id']}.json")
    if os.path.exists(fn):
        continue
    t = time.time()
    try:
        if rules == 'v5':
            o = pd.Timestamp(e.time).tz_convert(None).floor('s')
            ov = {nm: overlap(e, o - pd.Timedelta(hours=h)) for nm, h in (('real', 0), ('fake5', 5), ('fake7', 7))}
            res = det5.run_source5(e['id'], e.time, float(e.latitude), float(e.longitude), fakes=(5, 7),
                                   overlap={k: bool(v) for k, v in ov.items()})
            res['overlap_with'] = ov
        else:
            res = det.run_source(e['id'], e.time, float(e.latitude), float(e.longitude), fakes=(5, 7))
    except det.Blocked as ex:
        print('BLOCKED, stopping:', ex, flush=True); sys.exit(2)
    res['meta'] = dict(id=e['id'], time=e.time, lat=float(e.latitude), lon=float(e.longitude), depth=float(e.depth),
                       mag=float(e.mag), place=e.place, alt=int(e.alt))
    if det.IMPL6:
        res['impl'] = 'PREREG.v6'
    json.dump(res, open(fn + '.part', 'w'), default=str)
    os.replace(fn + '.part', fn)
    print(time.strftime('%H:%M:%S'), i, e['id'], e.mag, e.place, {k: v['cls'] for k, v in res.get('summary', {}).items()},
          'scope', len(res['gauges']), f'{time.time() - t:.0f}s', flush=True)
print('DONE shard', shard, flush=True)
