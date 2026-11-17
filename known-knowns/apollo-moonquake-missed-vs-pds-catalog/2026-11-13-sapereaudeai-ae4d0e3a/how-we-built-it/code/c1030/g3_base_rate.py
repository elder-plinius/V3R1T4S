"""Claim run a100_1030, glitch-gates lens: base rate of the G1 test (descriptive; written after the PREREG freeze and
labelled so; it gates nothing).

For S14 and S16 separately: the fraction of 20000 random 450 s windows in 1973 (seed 20261113) that overlap any
catalogued Liu, Xiao and Li 2025 interval (Spike, Step-Up, Step-Down) on MH1 or MH2; the same for windows
[start - 30 s, start + 450 s] at the 1973 catalogued A100 events; and per-day entry counts for 1973 days 296-310.

usage: g3_base_rate.py LIT_ACC_DIR LEVENT.csv
"""
import sys, os, csv, datetime as dt
import numpy as np

ACC = sys.argv[1]
NS = 1_000_000_000


def tns(s):
    s = s.strip()
    d = dt.datetime.strptime(s[:26], '%Y-%m-%d %H:%M:%S.%f' if '.' in s else '%Y-%m-%d %H:%M:%S')
    return int((d - dt.datetime(1970, 1, 1)).total_seconds() * 1e9)


y0 = tns('1973-01-01 00:00:00'); y1 = tns('1974-01-01 00:00:00')
rng = np.random.default_rng(20261113)
starts = np.sort(rng.integers(y0, y1 - 450 * NS, 20000))
a100 = []
for r in csv.DictReader(open(sys.argv[2], newline='')):
    if r['Y'] == '73' and r['T2'] == 'A' and (r['N2'] or '').strip() == '100':
        d = dt.datetime(1973, 1, 1) + dt.timedelta(days=int(r['JD']) - 1, hours=int(r['S'].zfill(4)[:2]), minutes=int(r['S'].zfill(4)[2:]))
        a100.append(d.strftime('%Y-%m-%d %H:%M:%S'))
for sta in ('S14', 'S16'):
    iv = []
    for typ in ('Spike', 'Step-Up', 'Step-Down'):
        for comp in ('MH1', 'MH2'):
            for r in csv.DictReader(open(os.path.join(ACC, '%s_ACC-%s_%s_all.csv' % (sta, typ, comp)), newline='')):
                a = tns(r['Start time'])
                if y0 - 86400 * NS <= a <= y1:
                    iv.append((a, tns(r['End time'])))
    iv.sort()
    A = np.array([a for a, b in iv], dtype=np.int64); B = np.array([b for a, b in iv], dtype=np.int64)
    Bmax = np.maximum.accumulate(B)

    def overlaps(t0, t1):
        j = np.searchsorted(A, t1, side='right')  # intervals starting before the window ends
        return j > 0 and Bmax[j - 1] >= t0

    fr = np.mean([overlaps(s, s + 450 * NS) for s in starts])
    fa = [overlaps(tns(t) - 30 * NS, tns(t) + 450 * NS) for t in a100]
    days = {}
    for a, b in iv:
        d = (a - y0) // (86400 * NS) + 1
        if 296 <= d <= 310:
            days[int(d)] = days.get(int(d), 0) + 1
    print('%s: MH1/MH2 intervals in 1973: %d; random 450 s windows overlapping one: %.3f; catalogued 1973 A100 events overlapping: %d of %d; entries per day 296-310: %s' % (
        sta, len(iv), fr, sum(fa), len(fa), dict(sorted(days.items()))))
