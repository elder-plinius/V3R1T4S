"""Summary and fake-origin null of the headline map (PREREG.md to PREREG.v4 rules, with the PREREG.v6 implementation
corrections), computed from object/map.csv only. Written 2026-11-07 to replace the run's summarize_map.py output for
this map, which needed the run's data/ folder (not shipped). Same statistics and the same null draw as
attempts/completeness-map/code/summarize_map.py (numpy default_rng(20261024), map rows in time order).
Run from the package folder: python3 how-we-built-it/code/summarize_v4_from_map.py   (needs numpy)
Writes object/map_summary.txt and object/null.json."""
import csv, json, math, os, collections
import numpy as np

H = os.path.dirname(os.path.abspath(__file__)); PKG = os.path.dirname(os.path.dirname(H)); O = os.path.join(PKG, 'object')
m = sorted(csv.DictReader(open(os.path.join(O, 'map.csv'))), key=lambda r: r['time'])
N = 264; UC = ('SIGNAL', 'NO_SIGNAL', 'SIGNAL_UNDECIDED')
c = collections.Counter(r['real_cls'] for r in m)
U = [r for r in m if r['real_cls'] in UC]
S = c['SIGNAL']; nU = len(U); und = c['SIGNAL_UNDECIDED']; nd = c['NO_DATA']; ng = c['NO_GAUGE']


def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n; cen = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return cen - h, cen + h


lo, hi = wilson(S, nU)
out = [f'map: object/map.csv, rules PREREG.md to PREREG.v4 (no overlap rule), code with the PREREG.v6 corrections; rows {len(m)}',
       f'real classes: {dict(c)}',
       f'HEADLINE: SIGNAL / USABLE = {S} / {nU} = {S / nU:.3f} (Wilson 95 % {lo:.3f}-{hi:.3f}); SIGNAL_UNDECIDED {und}',
       f'over all {N}: SIGNAL / {N} = {S / N:.3f}; bounds [{S / N:.3f}, {(S + und + nd + ng) / N:.3f}] (SIGNAL_UNDECIDED {und}, NO_DATA {nd}, NO_GAUGE {ng})']
for col, lab in (('listed', 'LISTED'), ('listed_v4', 'LISTED validity 4')):
    t = collections.Counter((r['real_cls'], r[col] == 'True') for r in U)
    out.append(f'SIGNAL x {lab} over USABLE quakes (listed / not listed): ' +
               '; '.join(f'{k} {t[(k, True)]} / {t[(k, False)]}' for k in UC))
out.append(f"LISTED among NO_DATA: {sum(r['listed'] == 'True' for r in m if r['real_cls'] == 'NO_DATA')} of {nd}; "
           f"among NO_GAUGE: {sum(r['listed'] == 'True' for r in m if r['real_cls'] == 'NO_GAUGE')} of {ng}")
sig = [r for r in U if r['real_cls'] == 'SIGNAL']
out.append(f"single-site SIGNALs: {sum(r['real_pass_sites'] == '1' for r in sig)} of {S} (never claims of a missed tsunami)")
cand = [r['id'] for r in sig if r['listed'] != 'True' and int(r['real_pass_sites']) >= 2]
out.append(f"unlisted SIGNALs: {[(r['id'], int(r['real_pass_sites'])) for r in sig if r['listed'] != 'True']}; "
           f"PREREG.v3 main-win candidates (unlisted, >= 2 passing sites): {len(cand)} {cand}")
band = collections.defaultdict(lambda: [0, 0, 0, 0])
for r in m:
    b = int((float(r['lon']) + 180) // 30 * 30 - 180)
    band[b][0] += 1; band[b][1] += r['real_cls'] in UC; band[b][2] += r['real_cls'] == 'SIGNAL'; band[b][3] += r['listed'] == 'True'
out.append('by 30-degree longitude band (west edge): band n usable signal listed')
out += [f'  {b:5d} {v[0]:3d} {v[1]:3d} {v[2]:3d} {v[3]:3d}' for b, v in sorted(band.items())]
rng = np.random.default_rng(20261024)
fk = np.array([[r['fake5_cls'], r['fake7_cls']] for r in m])
fr = []
for _ in range(400):
    pick = fk[np.arange(len(fk)), rng.integers(0, 2, len(fk))]
    u = np.isin(pick, UC)
    fr.append((pick == 'SIGNAL').sum() / max(1, u.sum()))
fr = np.array(fr)
f5 = sum(r['fake5_cls'] == 'SIGNAL' for r in m); f5u = sum(r['fake5_cls'] in UC for r in m)
f7 = sum(r['fake7_cls'] == 'SIGNAL' for r in m); f7u = sum(r['fake7_cls'] in UC for r in m)
rate = (f5 + f7) / (f5u + f7u); real = S / nU
unl = sum(r['listed'] != 'True' for r in U)
out.append(f'fake-origin null: fake SIGNAL at o-5h {f5}/{f5u}, at o-7h {f7}/{f7u}; pooled fake rate {f5 + f7}/{f5u + f7u} = {rate:.4f}; '
           f'expected chance SIGNALs among {nU} real USABLE quakes {rate * nU:.1f}, among the {unl} unlisted ones {rate * unl:.1f}')
out.append(f'400 fake catalogs (seed 20261024): max {fr.max():.4f}, mean {fr.mean():.4f}; real {real:.4f}; real beats all: {bool(real > fr.max())}')
out.append(f'chance-corrected: excess {S - rate * nU:.1f} = {real - rate:.3f} of USABLE')
open(os.path.join(O, 'map_summary.txt'), 'w').write('\n'.join(out) + '\n')
json.dump(dict(controls=400, best_control=round(float(fr.max()), 4), real=round(real, 4), real_beats_all=bool(real > fr.max()),
               fake_rate=round(float(rate), 4), S=S, USABLE=nU, N=N), open(os.path.join(O, 'null.json'), 'w'), indent=1)
print('\n'.join(out))
