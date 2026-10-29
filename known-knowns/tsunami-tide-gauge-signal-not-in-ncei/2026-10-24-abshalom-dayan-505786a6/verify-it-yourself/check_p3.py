"""Standalone checker for the p3 completeness map (Python standard library only). Run from the package folder.

Definitions checked (PREREG.v5, how-we-built-it/PREREG.v5.md, on top of PREREG.md sections 2-3; the per-sensor values
come from the code as corrected by PREREG.v6):
- per tied sensor and origin: DETECTS = usable and r > 5 and |arrival - ETA| <= 10 min;
- rule 1: a detecting sensor PASSES only if >= 10 of its control days are usable and none has r > 5;
- rule 2: a code is USABLE if any tied sensor is usable, DETECTS if every usable tied sensor detects, PASSES if every
  usable tied sensor passes, UNDECIDED if it detects, no usable tied sensor has a control day with r > 5, and one has
  fewer than 10 usable control days;
- sites group codes; an origin is NO_GAUGE (no code in scope), OVERLAP (rule 3: another M >= 6.5, depth <= 70 km ComCat
  event within 1000 km in the 24 h before), NO_DATA (no usable site), SIGNAL (a passing site), SIGNAL_UNDECIDED or
  NO_SIGNAL;
- headline SIGNAL / USABLE over the 264 quakes, bounds over 264, SIGNAL x LISTED, fake-origin rate, and a deterministic
  worst case of the fake-catalogue null (a fake SIGNAL wherever either fake origin has one).
What it cannot check without the raw IOC series (not shipped): the per-sensor r, arrival and control-day values
themselves; RUN_IT_YOURSELF.md rebuilds them from IOC."""
import csv, glob, hashlib, json, math, os, sys

FAILS = []
def need(ok, msg):
    if not ok:
        FAILS.append(msg)

here = os.path.dirname(os.path.abspath(__file__)); pkg = os.path.dirname(here)
obj = os.path.join(pkg, 'object')
# 1. object files are the published ones
man = json.load(open(os.path.join(here, 'expected_sha256.json')))
for rel, h in man.items():
    p = os.path.join(obj, rel)
    need(os.path.isfile(p) and hashlib.sha256(open(p, 'rb').read()).hexdigest() == h, f'sha256 mismatch: object/{rel}')
need(len(man) == sum(len(fs) for _, _, fs in os.walk(obj)), 'object/ holds files not in the manifest')
# 2. classes from per-sensor results
UC = ('SIGNAL', 'NO_SIGNAL', 'SIGNAL_UNDECIDED')
def sensor_ok(x, eta):
    if not x.get('usable'):
        return
    det = x['r'] > 5 and x.get('arrival') is not None and abs(x['arrival'] - eta) <= 10
    need(det == bool(x['detects']), 'detects flag disagrees with r and arrival')
    return det
def code_res(g, nm):
    U = {k: v[nm] for k, v in g.get('res_by_sensor', {}).items() if v[nm].get('usable')}
    if not U:
        return dict(usable=False)
    dets = [sensor_ok(x, g['eta']) for x in U.values()]
    d = dict(usable=True, detects=all(dets))
    if d['detects']:
        n = [len(x.get('ctrl', [])) for x in U.values()]
        need(all(len(x['ctrl']) == x['ctrl_n'] for x in U.values()), 'ctrl_n disagrees with the control list')
        r5 = [any(c['r'] > 5 for c in x['ctrl']) for x in U.values()]
        d['passes'] = all(k >= 10 and not f for k, f in zip(n, r5))
        d['undecided'] = (not d['passes']) and not any(r5) and any(k < 10 for k in n)
    return d
cls = {}
for f in sorted(glob.glob(os.path.join(obj, 'quakes', '*.json'))):
    q = json.load(open(f)); gs = q.get('gauges', []); out = {}
    for nm in ('real', 'fake5', 'fake7'):
        rs = [(g['site'], code_res(g, nm)) for g in gs]
        for g, (_, r) in zip(gs, rs):
            a = g.get('res', {}).get(nm, {})
            for k in ('usable', 'detects', 'passes', 'undecided'):
                if k in r:
                    need(bool(a.get(k)) == bool(r[k]), f"{q['label']} {g['code']} {nm}: {k} differs from the per-sensor rule")
        ov = q['overlap_with'][nm]
        need(all(float(e.split('@')[1].split('h')[0]) <= 24 and float(e.split('/')[1][:-2]) <= 1000 for e in ov), f"{q['label']}: overlap entry out of range")
        need(bool(ov) == bool(q['overlap'].get(nm)), f"{q['label']} {nm}: overlap flag disagrees with its list")
        us = {s for s, r in rs if r.get('usable')}; pa = {s for s, r in rs if r.get('passes')}; un = {s for s, r in rs if r.get('undecided')}
        c = ('NO_GAUGE' if not gs else 'OVERLAP' if ov else 'NO_DATA' if not us else 'SIGNAL' if pa else
             'SIGNAL_UNDECIDED' if un else 'NO_SIGNAL')
        need(c == q['summary'][nm]['cls'], f"{q['label']} {nm}: class {c} vs {q['summary'][nm]['cls']}")
        need(len(pa) == q['summary'][nm]['n_pass'], f"{q['label']} {nm}: passing sites differ")
        out[nm] = c
    cls[q['label']] = out
need(len(cls) == 264, f'{len(cls)} quake files, expected 264')
# 3. map.csv agrees and the headline numbers follow
m = list(csv.DictReader(open(os.path.join(obj, 'map.csv'))))
need(len(m) == 264 and {r['id'] for r in m} == set(cls), 'map.csv ids differ from quakes/')
for r in m:
    for nm in ('real', 'fake5', 'fake7'):
        need(r[f'{nm}_cls'] == cls.get(r['id'], {}).get(nm), f"map.csv {r['id']} {nm}_cls differs")
real = [r['real_cls'] for r in m]
S = real.count('SIGNAL'); n = sum(c in UC for c in real)
z = 1.96; p = S / n; dd = 1 + z * z / n; c0 = (p + z * z / (2 * n)) / dd; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / dd
L = [r for r in m if r['real_cls'] in UC and r['listed'] == 'True']
fs = sum(r[k] == 'SIGNAL' for r in m for k in ('fake5_cls', 'fake7_cls')); fu = sum(r[k] in UC for r in m for k in ('fake5_cls', 'fake7_cls'))
worst_s = sum(1 for r in m if 'SIGNAL' in (r['fake5_cls'], r['fake7_cls']))
worst_u = worst_s + sum(1 for r in m if 'SIGNAL' not in (r['fake5_cls'], r['fake7_cls'])
                       and r['fake5_cls'] in UC and r['fake7_cls'] in UC)
unk = sum(c in ('NO_DATA', 'NO_GAUGE', 'OVERLAP', 'SIGNAL_UNDECIDED') for c in real)
res = dict(S=S, USABLE=n, frac=round(p, 4), wilson=(round(c0 - h, 3), round(c0 + h, 3)), over264=round(S / 264, 4),
           upper264=round((S + unk) / 264, 4), listed_signal=sum(r['real_cls'] == 'SIGNAL' for r in L), listed_usable=len(L),
           unlisted_signal=sum(r['real_cls'] == 'SIGNAL' and r['listed'] != 'True' for r in m),
           fake_rate=round(fs / fu, 4), fake_worst_case=round(worst_s / max(1, worst_u), 4))
exp = json.load(open(os.path.join(here, 'expected_values.json')))
for k, v in exp.items():
    need(json.dumps(res.get(k)) == json.dumps(v), f'{k}: computed {res.get(k)}, expected {v}')
nj = json.load(open(os.path.join(obj, 'null.json')))
need(nj['S'] == S and nj['USABLE'] == n and abs(nj['real'] - p) < 1e-4 and abs(nj['fake_rate'] - fs / fu) < 1e-4, 'null.json disagrees with map.csv')
need(p > nj['best_control'] and p > res['fake_worst_case'], 'real does not beat the fake-origin null')
print(json.dumps(res))
for x in FAILS[:20]:
    print('mismatch:', x)
print('FAIL' if FAILS else 'PASS')
sys.exit(1 if FAILS else 0)
