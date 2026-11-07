"""Re-fetch check of 2026-11-07 (needs numpy, pandas, scipy as in how-we-built-it/requirements.txt).

usage: python recheck_refetch.py RUN PKG
  RUN: a folder laid out like how-we-built-it/code/ (lib/, attempts/); re-fetched windows go to RUN/data/ioc/
  PKG: this package folder

1. Lists the IOC windows to re-fetch: the stage-1 window [floor_h(o-31 h), ceil_h(o+7 h)] of every code whose stage-1
   sensor detects at the real origin of a v4 SIGNAL quake, or at an origin where object/quakes/ has no control days
   for that sensor (the PREREG.v5 run computed control days only when every usable tied sensor detects), and, for the
   latter, the stage-2 window [floor_h(oo-8 d-1 h), ceil_h(oo+9 d)] at that origin (oo = o, o-5 h or o-7 h).
2. Fetches each one with one GET (sequential, 1 s apart, stops on 401/403/429/503), logging URL, UTC time, HTTP status,
   sha256 and bytes to RUN/data/refetch_log.tsv. Windows already in RUN/data/ioc/ are not fetched again.
3. With lib/det.py (IMPL6 = True, v4 rules as in det.run_source) recomputes, offline, the stage-1 r and arrival of those
   codes (compared with the shipped per-sensor values) and the v4 control days at the 6 origins. Writes RUN/recheck.json."""
import sys, os, json, csv, subprocess, hashlib, gzip, time, datetime as dt
RUN, PKG = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.join(RUN, 'lib'))
import numpy as np, pandas as pd
import det
det.IMPL6 = True
HRS = {'real': 0, 'fake5': 5, 'fake7': 7}
v4 = {r['id']: r for r in csv.DictReader(open(os.path.join(PKG, 'object', 'map.csv')))}
Q = {k: json.load(open(os.path.join(PKG, 'object', 'quakes', k + '.json'))) for k in v4}


def name(c, a, b):
    return f'{c}_{a:%Y%m%d%H%M}_{b:%Y%m%d%H%M}.json'


def url(c, a, b):
    return (f'https://www.ioc-sealevelmonitoring.org/service.php?query=data&code={c}'
            f'&timestart={a:%Y-%m-%dT%H:%M:%S}&timestop={b:%Y-%m-%dT%H:%M:%S}&format=json')


def windows(lab):
    q = Q[lab]; o = pd.Timestamp(q['origin'])
    s1 = (det.floor_h(o - pd.Timedelta(hours=31)), det.ceil_h(o + pd.Timedelta(hours=7)))
    for g in q['gauges']:
        t, per = g.get('tied', []), g.get('res_by_sensor', {})
        if not t or t[0] not in per:
            continue
        for nm, h in HRS.items():
            x = per[t[0]][nm]
            if not x.get('detects') or not ((nm == 'real' and v4[lab]['real_cls'] == 'SIGNAL') or 'ctrl' not in x):
                continue
            oo = o - pd.Timedelta(hours=h)
            s2 = (det.floor_h(oo - pd.Timedelta(days=8, hours=1)), det.ceil_h(oo + pd.Timedelta(days=9)))
            yield g, nm, oo, s1, (s2 if 'ctrl' not in x else None)


todo = []
for lab in v4:
    for g, nm, oo, s1, s2 in windows(lab):
        for w in (s1, s2):
            if w and (g['code'], w) not in todo:
                todo.append((g['code'], w))
os.makedirs(os.path.join(RUN, 'data', 'ioc'), exist_ok=True)
for c, (a, b) in todo:
    fn = os.path.join(RUN, 'data', 'ioc', name(c, a, b) + '.gz')
    if os.path.exists(fn):
        continue
    u = url(c, a, b); t = dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    r = subprocess.run(['curl', '-g', '-s', '--compressed', '-m', '180', '-A', det.UA, '-o', fn + '.part', '-w', '%{http_code}', u],
                       capture_output=True, text=True)
    code = r.stdout.strip() or '000'
    raw = open(fn + '.part', 'rb').read() if os.path.exists(fn + '.part') else b''
    with open(os.path.join(RUN, 'data', 'refetch_log.tsv'), 'a') as f:
        f.write(f'{u}\t{t}\t{code}\t{hashlib.sha256(raw).hexdigest()}\t{len(raw)}\n')
    if os.path.exists(fn + '.part'):
        os.remove(fn + '.part')
    if code in ('401', '403', '429', '503'):
        sys.exit(f'BLOCKED {code} {u}')
    if code == '200':
        with gzip.open(fn, 'wb') as g:
            g.write(raw)
    time.sleep(1)
os.environ['V3_OFFLINE'] = '1'
s1rows, s2rows = [], []
for lab in v4:
    for g, nm, oo, (t0, t1), s2 in windows(lab):
        s, sen = det.series(det.ioc_raw(g['code'], t0, t1), t0, t1)
        st = det.stat(s, det.highpass(s), oo, g['eta'], det.highpass_causal(s))
        x = g['res_by_sensor'][g['tied'][0]][nm]
        s1rows.append(dict(quake=lab, origin=nm, code=g['code'], eta=g['eta'], sensor=sen, shipped_r=x['r'],
                           shipped_arrival=x['arrival'], refetch_r=st.get('r'), refetch_arrival=st.get('arrival'),
                           identical=bool(sen == g['tied'][0] and st.get('r') == x['r'] and st.get('arrival') == x['arrival'])))
        if s2:
            s2_, sen2 = det.series(det.ioc_raw(g['code'], *s2), *s2)
            b2, c2 = det.highpass(s2_), det.highpass_causal(s2_)
            ctrl = []
            for k in det.CTRL:
                cc = det.stat(s2_, b2, oo + pd.Timedelta(days=k), g['eta'], c2)
                if cc['usable']:
                    ctrl.append(dict(day=k, r=cc['r'], arrival=cc['arrival'], detects=cc['detects']))
            n, anyd = len(ctrl), any(cc['detects'] for cc in ctrl)
            s2rows.append(dict(quake=lab, origin=nm, code=g['code'], site=g['site'], eta=g['eta'],
                               stage2_window=[str(s2[0]), str(s2[1])], stage2_sensor=sen2, ctrl_n=n, ctrl_any_detect=anyd,
                               passes=bool(n >= 10 and not anyd), undecided=bool(n < 10), ctrl=ctrl))
json.dump(dict(stage1=s1rows, stage2=s2rows), open(os.path.join(RUN, 'recheck.json'), 'w'), indent=1)
print('stage 1:', len(s1rows), 'codes,', sum(r['identical'] for r in s1rows), 'identical to the shipped r, arrival and sensor')
for r in s2rows:
    print(r['quake'], r['origin'], r['code'], 'sensor', r['stage2_sensor'], 'counted control days', r['ctrl_n'],
          'any detects', r['ctrl_any_detect'], 'passes', r['passes'])
