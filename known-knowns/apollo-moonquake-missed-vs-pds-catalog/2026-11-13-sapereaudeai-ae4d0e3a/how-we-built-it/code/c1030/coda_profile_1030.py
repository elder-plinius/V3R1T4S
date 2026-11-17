"""Claim run a100_1030 (descriptive, written AFTER the PREREG freeze; gates nothing): is the candidate part of the coda
of the catalogued A1 deep moonquake of 1973-10-30 01:00 (levent stop 02:00), 85 min earlier? Prints the RMS of the
frozen preprocessed data (0.25-1.0 Hz, whitened) in 5-min blocks from 00:30 to 04:30 on S14 and S16 MH1/MH2, in units
of the median 5-min RMS of 12:00-24:00 the same day (a quiet reference), and the NCC of each 5-min block's best
lag with nothing (no template): energy only.

usage: coda_profile_1030.py TOOLS_DIR
"""
import sys
sys.path.insert(0, sys.argv[1])
import threadcap  # noqa: F401
import numpy as np
from apollo_lib import load_span, preprocess, RATE
from evlib import FS

w = int(300 * FS)
rows = {}
for sta in ('s14', 's16'):
    for ch in ('mh1', 'mh2'):
        sp = load_span(sta, ch, 1973, 303, int(7200 * RATE))
        y, v = preprocess(sp[0], sp[1], (0.25, 1.0, 0.1), dec=2)
        ref = np.median([np.sqrt(np.mean(y[k:k + w] ** 2)) for k in range(int(12 * 3600 * FS), int(24 * 3600 * FS) - w, w) if v[k:k + w].mean() > 0.99])
        prof = []
        for k in range(int(0.5 * 3600 * FS), int(4.5 * 3600 * FS), w):
            prof.append(np.sqrt(np.mean(y[k:k + w] ** 2)) / ref if v[k:k + w].mean() > 0.99 else float('nan'))
        rows['%s %s' % (sta.upper(), ch.upper())] = prof
print('5-min block start (UTC)  ' + '  '.join('%-7s' % k for k in rows))
for i in range(len(next(iter(rows.values())))):
    s = 0.5 * 3600 + i * 300
    print('%02d:%02d                   ' % (s // 3600, (s % 3600) // 60) + '  '.join('%7.2f' % rows[k][i] for k in rows),
          ' <- candidate window 02:25:21-02:32:51' if s in (8400, 8700, 9000) else (' <- A1 levent start 01:00' if s == 3600 else ''))
