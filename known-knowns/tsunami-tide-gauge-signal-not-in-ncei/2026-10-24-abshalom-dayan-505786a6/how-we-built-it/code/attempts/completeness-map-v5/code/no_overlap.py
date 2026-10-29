"""Effect of PREREG.v5 rule 3 (OVERLAP): reclassify every origin from the per-gauge v5 results with the overlap flag
ignored (rules 1-2 only), then the same headline and 400-catalogue fake-origin null as summarize_v5.py."""
import os, json, glob, math
import numpy as np
H = os.path.dirname(os.path.abspath(__file__))
O = os.environ.get('V3_MAPOUT') or os.path.join(H, '..', 'out')
UC = ('SIGNAL', 'NO_SIGNAL', 'SIGNAL_UNDECIDED')


def cls(d, nm):
    gs = d.get('gauges', [])
    if not gs:
        return 'NO_GAUGE'
    us = {g['site'] for g in gs if g.get('res', {}).get(nm, {}).get('usable')}
    pa = {g['site'] for g in gs if g.get('res', {}).get(nm, {}).get('passes')}
    und = {g['site'] for g in gs if g.get('res', {}).get(nm, {}).get('undecided')}
    return 'NO_DATA' if not us else 'SIGNAL' if pa else 'SIGNAL_UNDECIDED' if und else 'NO_SIGNAL'


rows = []
for f in sorted(glob.glob(os.path.join(O, 'quakes', '*.json'))):
    d = json.load(open(f))
    rows.append({nm: cls(d, nm) for nm in ('real', 'fake5', 'fake7')} | {'with_rule3': d['summary']['real']['cls']})
real = [r['real'] for r in rows]
S = real.count('SIGNAL'); n = sum(c in UC for c in real)
z = 1.96; p = S / n; dd = 1 + z * z / n; c0 = (p + z * z / (2 * n)) / dd; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / dd
fs = sum(r[k] == 'SIGNAL' for r in rows for k in ('fake5', 'fake7')); fu = sum(r[k] in UC for r in rows for k in ('fake5', 'fake7'))
rate = fs / fu
rng = np.random.default_rng(20261024)
fk = np.array([[r['fake5'], r['fake7']] for r in rows])
fr = []
for _ in range(400):
    pick = fk[np.arange(len(fk)), rng.integers(0, 2, len(fk))]
    fr.append((pick == 'SIGNAL').sum() / max(1, np.isin(pick, UC).sum()))
fr = np.array(fr)
moved = sum(1 for r in rows if r['with_rule3'] == 'OVERLAP' and r['real'] == 'SIGNAL')
out = [f'rules 1-2 only (OVERLAP ignored): SIGNAL / USABLE = {S} / {n} = {p:.4f} (Wilson 95 % {c0 - h:.3f}-{c0 + h:.3f})',
       f'fake SIGNAL {fs} / {fu} usable fake origins = {rate:.4f}; expected chance {rate * n:.1f}; excess {(S - rate * n) / n:.3f} of USABLE',
       f'400 fake catalogues (seed 20261024): mean {fr.mean():.4f}, best {fr.max():.4f}; real beats all: {bool(p > fr.max())}',
       f'real OVERLAP quakes that would be SIGNAL without rule 3: {moved}; real classes without rule 3: '
       + str({k: real.count(k) for k in sorted(set(real))})]
open(os.path.join(O, 'no_overlap.txt'), 'w').write('\n'.join(out) + '\n')
print('\n'.join(out))
