"""PREREG.v12: S14 MH1/MH2 templates for many nests from their 1971 catalogued events (glitch-screened builder).
usage: s14_multinest_build.py NESTS(comma) OUT.npz"""
import sys, json
sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', 'tools'))
import numpy as np
from evlib import load_nest_events, DayCache, event_block, FS
from nesttemplates2 import build, _clean
CAT = __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', '..', 'data', 'catalog', 'levent.1008weber.csv')
band = (0.25, 1.0, 0.1); L = 450.0; M = int(round(L * FS))
chans = [('s14', 'mh1'), ('s14', 'mh2')]
cache = DayCache(band)
keep, tms, info, dropped = [], [], {}, {}
for n in sys.argv[1].split(','):
    ev = load_nest_events(CAT, n, ['71'])
    ev = ev[ev['t_ns'] >= ev['t_ns'].min()]  # all 1971 events; days before S14 started give no S14 window
    amp = ev['A1n'].clip(lower=0).fillna(0) + ev['A2n'].clip(lower=0).fillna(0)
    clean = []
    for i, r in ev.iterrows():
        blk = event_block(cache, chans, int(r['t_ns']), M)
        clean.append(all(y is not None and v.mean() > 0.95 and _clean(y) for y, v in blk))
    if not any(clean):
        dropped[n] = 'no clean reference window'; print('A%s dropped: no clean reference' % n); continue
    ref = int(amp.where(clean, -1).idxmax())
    b = build(ev.reset_index(drop=True) if False else ev, chans, band, L, ref, cache=cache)
    if b is None or any(t is None for t in b['tm']):
        dropped[n] = 'no template'; print('A%s dropped: no template' % n); continue
    g = [round(float(np.abs(t).max() / t.std()), 1) for t in b['tm']]
    if len(b['members']) < 3 or max(g) > 8:
        dropped[n] = 'members %d, max|t|/rms %s' % (len(b['members']), g); print('A%s dropped:' % n, dropped[n]); continue
    keep.append(n); tms.append(np.array(b['tm']))
    info[n] = dict(events=len(ev), members=len(b['members']), onset=b['onset_rel_s'], glitchiness=g)
    print('A%s events %d members %d onset %.1f s max|t|/rms %s' % (n, len(ev), len(b['members']), b['onset_rel_s'], g), flush=True)
np.savez(sys.argv[2], nests=np.array(keep), tm=np.array(tms), chans=np.array(['%s.%s' % c for c in chans]),
         band=np.array(band), L=L, info=json.dumps(info), dropped=json.dumps(dropped))
