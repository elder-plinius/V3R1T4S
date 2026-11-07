"""Standalone checker for the p3 completeness map (Python standard library only). Run from the package folder.

Headline map (object/map.csv): the rules frozen before scoring, PREREG.md section 2-3 with PREREG.v2 to PREREG.v4 (code
with the PREREG.v6 corrections). Per gauge code and origin, from the per-sensor results in object/quakes/:
- the scored sensor is the first of the tied sensors (the sea-level sensor with the most samples in the stage-1 window);
- DETECTS = usable and r > 5 and |arrival - ETA| <= 10 min;
- control days: a usable control day counts; PASSES = DETECTS, >= 10 counted control days and none of them DETECTS;
  UNDECIDED = DETECTS, fewer than 10 counted and none DETECTS. The control days come from object/quakes/ where the
  PREREG.v5 run computed them for this sensor, else from object/v4_ctrl_refetch.json (6 origins, recomputed 2026-11-07);
- sites group codes; an origin is NO_GAUGE (no code in scope), NO_DATA (no usable site), SIGNAL (a passing site),
  SIGNAL_UNDECIDED (an undecided site) or NO_SIGNAL. No overlap rule.
Sensitivity map (sensitivity-v5/map.csv): the post-hoc PREREG.v5 rules (literal control days, every tied sensor, the
24 h overlap rule), checked from the same per-sensor results.
Also checked: LISTED and the NCEI ids of both maps against the NCEI events pages saved on 2026-11-07 (rule of
PREREG.md section 3 as implemented: calendar dates within 1 day, epicentres within 1000 km or no NCEI coordinates);
every gauge in scope has a model arrival time (ETA) and a stage-1 row in how-we-built-it/ioc_requests.csv with that ETA;
every v4 control-day window has a stage-2 row; every response named there is a line of ioc_windows_1/2.tsv with that
sha256; headline, Wilson interval, bounds over 264, SIGNAL x LISTED, fake-origin rate and a deterministic worst case of
the fake-catalogue null (a fake SIGNAL wherever either fake origin has one).
What it cannot check without the raw IOC series (not shipped): the per-sensor r, arrival and control-day values
themselves; RUN_IT_YOURSELF.md rebuilds them from IOC."""
import csv, datetime as dt, glob, hashlib, json, math, os, sys

FAILS = []
def need(ok, msg):
    if not ok:
        FAILS.append(msg)

here = os.path.dirname(os.path.abspath(__file__)); pkg = os.path.dirname(here)
obj = os.path.join(pkg, 'object'); sen = os.path.join(pkg, 'sensitivity-v5'); hw = os.path.join(pkg, 'how-we-built-it')
UC = ('SIGNAL', 'NO_SIGNAL', 'SIGNAL_UNDECIDED')
ORIG = ('real', 'fake5', 'fake7')
# 1. object/ and sensitivity-v5/ files are the published ones
man = json.load(open(os.path.join(here, 'expected_sha256.json')))
for rel, h in man.items():
    p = os.path.join(pkg, rel)
    need(os.path.isfile(p) and hashlib.sha256(open(p, 'rb').read()).hexdigest() == h, f'sha256 mismatch: {rel}')
have = {os.path.relpath(os.path.join(d, f), pkg) for top in (obj, sen) for d, _, fs in os.walk(top) for f in fs}
need(have == set(man), 'object/ or sensitivity-v5/ holds files not in the manifest, or misses some')


def det_ok(x, eta):
    det = x['r'] > 5 and x.get('arrival') is not None and abs(x['arrival'] - eta) <= 10
    need(det == bool(x['detects']), 'detects flag disagrees with r and arrival')
    return det


# 2. headline map: v4 classes from the per-sensor results
ref = json.load(open(os.path.join(obj, 'v4_ctrl_refetch.json')))
REF = {(r['quake'], r['origin'], r['code']): r for r in ref['codes']}
used_ref = set()
for r in REF.values():
    need(r['ctrl_n'] == len(r['ctrl']) and r['ctrl_any_detect'] == any(c['detects'] for c in r['ctrl']), 'refetch ctrl summary')
    for c in r['ctrl']:
        need(c['detects'] == (c['r'] > 5 and c['arrival'] is not None and abs(c['arrival'] - r['eta']) <= 10), 'refetch ctrl detects')


def v4_code(q, g, nm):
    t, per = g.get('tied', []), g.get('res_by_sensor', {})
    if not t or t[0] not in per:
        return dict(usable=False)
    x = per[t[0]][nm]
    if not x.get('usable'):
        return dict(usable=False)
    d = dict(usable=True, detects=det_ok(x, g['eta']))
    if d['detects']:
        if 'ctrl' in x:
            need(len(x['ctrl']) == x['ctrl_n'], 'ctrl_n disagrees with the control list')
            n, anyd = len(x['ctrl']), any(c['detects'] for c in x['ctrl'])
        else:
            k = (q['label'], nm, g['code']); r = REF.get(k)
            need(r is not None, f'{k}: v4 control days neither in object/quakes/ nor in object/v4_ctrl_refetch.json')
            if r is None:
                return d
            used_ref.add(k); need(r['eta'] == g['eta'] and r['site'] == g['site'], f'{k}: refetch eta or site differs')
            n, anyd = r['ctrl_n'], r['ctrl_any_detect']
        d['passes'] = n >= 10 and not anyd
        d['undecided'] = n < 10 and not anyd
    return d


def v5_code(g, nm):
    U = {k: v[nm] for k, v in g.get('res_by_sensor', {}).items() if v[nm].get('usable')}
    if not U:
        return dict(usable=False)
    dets = [det_ok(x, g['eta']) for x in U.values()]
    d = dict(usable=True, detects=all(dets))
    if d['detects']:
        n = [len(x.get('ctrl', [])) for x in U.values()]
        need(all(len(x['ctrl']) == x['ctrl_n'] for x in U.values()), 'ctrl_n disagrees with the control list')
        r5 = [any(c['r'] > 5 for c in x['ctrl']) for x in U.values()]
        d['passes'] = all(k >= 10 and not f for k, f in zip(n, r5))
        d['undecided'] = (not d['passes']) and not any(r5) and any(k < 10 for k in n)
    return d


def classify(gs, rs, overlap=False):
    us = {s for s, r in rs if r.get('usable')}; de = {s for s, r in rs if r.get('detects')}
    pa = {s for s, r in rs if r.get('passes')}; un = {s for s, r in rs if r.get('undecided')}
    c = ('NO_GAUGE' if not gs else 'OVERLAP' if overlap else 'NO_DATA' if not us else 'SIGNAL' if pa else
         'SIGNAL_UNDECIDED' if un else 'NO_SIGNAL')
    return c, len(us), len(de), len(pa)


Q, c4, c5 = {}, {}, {}
for f in sorted(glob.glob(os.path.join(obj, 'quakes', '*.json'))):
    q = json.load(open(f)); gs = q.get('gauges', []); Q[q['label']] = q
    for g in gs:
        need(isinstance(g.get('eta'), (int, float)) and 10 <= g['eta'] <= 150, f"{q['label']} {g['code']}: ETA missing or out of 10-150 min")
    c4[q['label']], c5[q['label']] = {}, {}
    for nm in ORIG:
        c4[q['label']][nm] = classify(gs, [(g['site'], v4_code(q, g, nm)) for g in gs])
        rs = [(g['site'], v5_code(g, nm)) for g in gs]
        for g, (_, r) in zip(gs, rs):
            a = g.get('res', {}).get(nm, {})
            for k in ('usable', 'detects', 'passes', 'undecided'):
                if k in r:
                    need(bool(a.get(k)) == bool(r[k]), f"{q['label']} {g['code']} {nm}: {k} differs from the PREREG.v5 per-sensor rule")
        ov = q['overlap_with'][nm]
        need(all(float(e.split('@')[1].split('h')[0]) <= 24 and float(e.split('/')[1][:-2]) <= 1000 for e in ov), f"{q['label']}: overlap entry out of range")
        need(bool(ov) == bool(q['overlap'].get(nm)), f"{q['label']} {nm}: overlap flag disagrees with its list")
        c5[q['label']][nm] = classify(gs, rs, bool(ov))
        need(c5[q['label']][nm][0] == q['summary'][nm]['cls'] and c5[q['label']][nm][3] == q['summary'][nm]['n_pass'],
             f"{q['label']} {nm}: PREREG.v5 class or passing sites differ from the quake file")
need(len(Q) == 264, f'{len(Q)} quake files, expected 264')
need(used_ref == set(REF), 'object/v4_ctrl_refetch.json holds codes the v4 rule does not need')

# 3. both maps agree with the derived classes; LISTED re-derived from the saved NCEI pages
ev = []
for f in sorted(glob.glob(os.path.join(hw, 'ncei_2026-11-07', 'events_2015_2026_p*.json'))):
    ev += json.load(open(f))['items']
need(len(ev) == 231, f'{len(ev)} NCEI events in the 2026-11-07 pages, expected 231')


def gc(a, b, c, d):
    a, b, c, d = map(math.radians, (a, b, c, d))
    x = math.sin((c - a) / 2) ** 2 + math.cos(a) * math.cos(c) * math.sin((d - b) / 2) ** 2
    return 6371.0 * 2 * math.asin(math.sqrt(min(1.0, max(0.0, x))))


def listed_ids(r):
    t = dt.datetime.strptime(r['time'][:19], '%Y-%m-%dT%H:%M:%S'); out = []
    for e in ev:
        d = dt.date(e['year'], e.get('month') or 1, e.get('day') or 1)
        if abs((d - t.date()).days) <= 1 or (e.get('day') is None and e['year'] == t.year and e.get('month') == t.month):
            if e.get('latitude') is None or e.get('longitude') is None or gc(float(r['lat']), float(r['lon']), e['latitude'], e['longitude']) <= 1000:
                out.append(str(e['id']))
    return ';'.join(out)


def headline(m):
    real = [r['real_cls'] for r in m]
    S = real.count('SIGNAL'); n = sum(c in UC for c in real)
    z = 1.96; p = S / n; dd = 1 + z * z / n; c0 = (p + z * z / (2 * n)) / dd; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / dd
    L = [r for r in m if r['real_cls'] in UC and r['listed'] == 'True']
    fs = sum(r[k] == 'SIGNAL' for r in m for k in ('fake5_cls', 'fake7_cls')); fu = sum(r[k] in UC for r in m for k in ('fake5_cls', 'fake7_cls'))
    ws = sum(1 for r in m if 'SIGNAL' in (r['fake5_cls'], r['fake7_cls']))
    wu = ws + sum(1 for r in m if 'SIGNAL' not in (r['fake5_cls'], r['fake7_cls']) and r['fake5_cls'] in UC and r['fake7_cls'] in UC)
    unk = sum(c in ('NO_DATA', 'NO_GAUGE', 'OVERLAP', 'SIGNAL_UNDECIDED') for c in real)
    return dict(S=S, USABLE=n, frac=round(p, 4), wilson=(round(c0 - h, 3), round(c0 + h, 3)), over264=round(S / 264, 4),
                upper264=round((S + unk) / 264, 4), listed_signal=sum(r['real_cls'] == 'SIGNAL' for r in L), listed_usable=len(L),
                unlisted_signal=sum(r['real_cls'] == 'SIGNAL' and r['listed'] != 'True' for r in m),
                fake_signal=fs, fake_usable=fu, fake_rate=round(fs / fu, 4), fake_worst_case=round(ws / max(1, wu), 4))


exp = json.load(open(os.path.join(here, 'expected_values.json')))
res = {}
for key, path, cls in (('v4', os.path.join(obj, 'map.csv'), c4), ('v5_sensitivity', os.path.join(sen, 'map.csv'), c5)):
    m = list(csv.DictReader(open(path)))
    need(len(m) == 264 and {r['id'] for r in m} == set(Q), f'{key} map.csv ids differ from quakes/')
    for r in m:
        for nm in ORIG:
            c, nu, nd, npass = cls.get(r['id'], {}).get(nm, (None,) * 4)
            need(r[f'{nm}_cls'] == c, f"{key} map.csv {r['id']} {nm}_cls {r[f'{nm}_cls']} vs derived {c}")
            if key == 'v4' or c != 'OVERLAP':
                need((int(r[f'{nm}_usable_sites']), int(r[f'{nm}_pass_sites'])) == (nu, npass), f"{key} map.csv {r['id']} {nm} site counts")
            if key == 'v4':
                need(int(r[f'{nm}_detect_sites']) == nd, f"{key} map.csv {r['id']} {nm} detecting sites")
        need(r['ncei_ids'] == listed_ids(r) and r['listed'] == str(bool(r['ncei_ids'])), f"{key} map.csv {r['id']}: LISTED differs from the 2026-11-07 NCEI pages")
    res[key] = headline(m)
    for k, v in exp[key].items():
        need(json.dumps(res[key].get(k)) == json.dumps(v), f'{key} {k}: computed {res[key].get(k)}, expected {v}')
    nj = json.load(open(os.path.join(obj if key == 'v4' else sen, 'null.json')))
    h = res[key]
    need(nj['S'] == h['S'] and nj['USABLE'] == h['USABLE'] and abs(nj['real'] - h['frac']) < 1e-4 and abs(nj['fake_rate'] - h['fake_rate']) < 1e-4, f'{key} null.json disagrees with map.csv')
    need(h['frac'] > nj['best_control'] and h['frac'] > h['fake_worst_case'], f'{key}: real does not beat the fake-origin null')

# 4. IOC request list: a stage-1 row per gauge with its ETA, a stage-2 row per v4 control-day window, refs resolve
W = {t: open(os.path.join(hw, f'ioc_windows_{t}.tsv')).read().splitlines() for t in ('1', '2')}
st1, st2 = {}, set()
for r in csv.DictReader(open(os.path.join(hw, 'ioc_requests.csv'))):
    if r['stage'] == '1':
        st1[(r['quake'], r['code'])] = float(r['eta_min'])
    else:
        for nm in r['origin'].split(';'):
            st2.add((r['quake'], r['code'], nm, r['used_by']))
    for e in r['responses'].split():
        t, ln, h = e.split(':'); line = W[t][int(ln) - 1].split('\t')
        need(line[1] == h and f"code={r['code']}&" in line[3], f"ioc_requests.csv {r['quake']} {r['code']}: response {t}:{ln} does not resolve")
for lab, q in Q.items():
    for g in q['gauges']:
        need(st1.get((lab, g['code'])) == g['eta'], f"{lab} {g['code']}: no stage-1 request row with ETA {g['eta']}")
        t, per = g.get('tied', []), g.get('res_by_sensor', {})
        for nm in ORIG:
            if t and t[0] in per and per[t[0]][nm].get('detects'):
                need(any(k[:3] == (lab, g['code'], nm) and 'v4' in k[3] for k in st2), f"{lab} {g['code']} {nm}: no v4 stage-2 request row")
print(json.dumps(res))
for x in FAILS[:20]:
    print('mismatch:', x)
print('FAIL' if FAILS else 'PASS')
sys.exit(1 if FAILS else 0)
