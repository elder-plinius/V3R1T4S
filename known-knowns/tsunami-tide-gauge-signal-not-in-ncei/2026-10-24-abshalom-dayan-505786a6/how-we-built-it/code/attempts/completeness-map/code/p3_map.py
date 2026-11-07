"""PREREG.md section 3 (with PREREG.v2): the p3 completeness map. One JSON per quake (resumable).
usage: p3_map.py <shard> <nshards>"""
import sys, os, json, time
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, '..', '..', '..')
sys.path.insert(0, os.path.join(R, 'lib'))
import numpy as np, pandas as pd, tt, det
O = os.environ.get('V3_MAPOUT') or os.path.join(H, '..', 'out')
shard, nsh = int(sys.argv[1]), int(sys.argv[2])
q = pd.read_csv(os.path.join(R, 'data', 'comcat', 'm65_d70_2015_2025.csv'))
q = q[q.type == 'earthquake'].copy()
q['alt'] = tt.alt_at(q.latitude.values, q.longitude.values)
q = q[q.alt < 0].sort_values('time').reset_index(drop=True)
assert len(q) == 264, len(q)
for i, e in q.iterrows():
    if i % nsh != shard:
        continue
    os.makedirs(os.path.join(O, 'quakes'), exist_ok=True)
    fn = os.path.join(O, 'quakes', f"{e['id']}.json")
    if os.path.exists(fn):
        continue
    t = time.time()
    try:
        res = det.run_source(e['id'], e.time, float(e.latitude), float(e.longitude), fakes=(5, 7))
    except det.Blocked as ex:
        print('BLOCKED, stopping:', ex, flush=True); sys.exit(2)
    res['meta'] = dict(id=e['id'], time=e.time, lat=float(e.latitude), lon=float(e.longitude), depth=float(e.depth),
                       mag=float(e.mag), place=e.place, alt=int(e.alt))
    json.dump(res, open(fn + '.part', 'w'), default=str)
    os.replace(fn + '.part', fn)
    print(time.strftime('%H:%M:%S'), i, e['id'], e.mag, e.place, {k: v['cls'] for k, v in res.get('summary', {}).items()},
          'scope', len(res['gauges']), f'{time.time() - t:.0f}s', flush=True)
print('DONE shard', shard, flush=True)
