"""Derived summary (our statistic, not the catalogue itself): per UTC day of 1971 days 36-365 and per S14 channel (MH1,
MH2), the number of catalogued intervals of each type (Spike, Step-Up, Step-Down) in the Liu, Xiao and Li (2025)
catalogue whose start falls on that day, and the longest stretch of that day with no catalogued interval of any type
on that channel (gaps measured from an interval's end to the next interval's start, with the day's edges as bounds).
A gap-length summary then asks how common a stretch as long as the one around the A38 onset is: the stretch with no
catalogued S14 MH1 or MH2 interval of any type, both channels together, from 09:39:24.528 to 19:08:36.981 UTC on
1971-05-13 (9.487 h).

usage: python3 daily_counts.py lunar_ACC-v1.0.1.zip OUT_DAILY.csv OUT_SUMMARY.txt   (standard library only)
The script refuses an archive member whose sha256 differs from the values recorded below.
"""
import csv, datetime as dt, hashlib, io, sys, zipfile

SHA = {'S14_ACC-Spike_MH1_all.csv': '78e91b83ff3f80c51706b044786420dcd41dddfa359099ac1e1123503b6ac0a1',
       'S14_ACC-Spike_MH2_all.csv': '1219c0fa43fc26ff08950a217407d0b5b5c9daadcb56900565f8af08733bc9f9',
       'S14_ACC-Step-Up_MH1_all.csv': '5d0303919e3f71aa0dc3abcf26e1e7d2e7a5fa95c0f14d8d647ee87f7ac0c5df',
       'S14_ACC-Step-Up_MH2_all.csv': '39d06c4b6be745d2ee3763c294da18b31b088700c705df8936a8ce40dce5e159',
       'S14_ACC-Step-Down_MH1_all.csv': '29fe75796e28e482405d7ceed06e94afdfbff292aa6a8cb99b9d39ec1f094234',
       'S14_ACC-Step-Down_MH2_all.csv': '459a210443a4b510e6ab21a423deaa85254ce86ba712106ffeba4c9f8a611e8f'}
D0, D1 = dt.datetime(1971, 2, 5), dt.datetime(1972, 1, 1)        # 1971 day 36 00:00 .. end of day 365
HOLE = (dt.datetime(1971, 5, 13, 9, 39, 24, 528302), dt.datetime(1971, 5, 13, 19, 8, 36, 981132))


def T(s):
    s = s.strip()
    return dt.datetime.strptime(s[:26], '%Y-%m-%d %H:%M:%S.%f' if '.' in s else '%Y-%m-%d %H:%M:%S')


def gaps(iv, lo, hi):
    """Stretches inside [lo, hi] not covered by any interval of iv (sorted by start)."""
    out, cur = [], lo
    for a, b in iv:
        if b < lo or a > hi:
            continue
        if a > cur:
            out.append((cur, a))
        cur = max(cur, b)
    if hi > cur:
        out.append((cur, hi))
    return out


ZIP, OUT_D, OUT_S = sys.argv[1:4]
z = zipfile.ZipFile(ZIP)
iv = {}
for name, h in SHA.items():
    mem = [n for n in z.namelist() if n.endswith('/catalogs/' + name)]
    assert len(mem) == 1, name
    b = z.read(mem[0])
    if hashlib.sha256(b).hexdigest() != h:
        sys.exit('archive member %s has sha256 %s, expected %s' % (name, hashlib.sha256(b).hexdigest(), h))
    kind, ch = name.split('_')[1].replace('ACC-', ''), name.split('_')[2]
    iv[(kind, ch)] = [(T(r['Start time']), T(r['End time'])) for r in csv.DictReader(io.StringIO(b.decode('utf-8'), newline=''))]
kinds = ('Spike', 'Step-Up', 'Step-Down')
rows = ['date_utc,doy_1971,channel,spike,step_up,step_down,all_types,longest_gap_h_all_types']
for ch in ('MH1', 'MH2'):
    allv = sorted(x for k in kinds for x in iv[(k, ch)])
    d = D0
    while d < D1:
        e = d + dt.timedelta(days=1)
        n = [sum(1 for a, b in iv[(k, ch)] if d <= a < e) for k in kinds]
        g = max((y - x).total_seconds() for x, y in gaps(allv, d, e)) / 3600
        rows.append('%s,%d,%s,%d,%d,%d,%d,%.3f' % (d.date(), d.timetuple().tm_yday, ch, n[0], n[1], n[2], sum(n), g))
        d = e
open(OUT_D, 'w', newline='\n').write('\n'.join(rows) + '\n')

# gap-length summary over the whole span, both channels together and each channel, all types
lines = []
hole_h = (HOLE[1] - HOLE[0]).total_seconds() / 3600
for lab, sel in (('MH1 and MH2 together', ('MH1', 'MH2')), ('MH1', ('MH1',)), ('MH2', ('MH2',))):
    allv = sorted(x for k in kinds for c in sel for x in iv[(k, c)])
    gs = [(x, y, (y - x).total_seconds() / 3600) for x, y in gaps(allv, D0, D1)]
    long_ = [g for g in gs if g[2] >= hole_h - 1e-9]
    tot = (D1 - D0).total_seconds() / 3600
    lines.append('%s, 1971 days 36-365, all three types: %d gaps of %.3f h or longer (the stretch around the A38 onset '
                 'is %.3f h), covering %.1f%% of the span; longest %.3f h; gaps of 8 h or longer: %d' % (
                     lab, len(long_), hole_h, hole_h, 100 * sum(g[2] for g in long_) / tot, max(g[2] for g in gs),
                     sum(1 for g in gs if g[2] >= 8)))
    if lab == 'MH1 and MH2 together':
        days = sorted(set(g[0].date() for g in long_))
        lines.append('  start dates of those gaps (%d distinct days): %s' % (len(days), ' '.join(str(x) for x in days)))
        rank = sorted((g[2] for g in gs), reverse=True)
        lines.append('  the stretch around the onset (%.3f h) ranks %d of %d gaps by length' % (
            hole_h, 1 + sum(1 for x in rank if x > hole_h + 1e-9), len(rank)))
zero = {}
for ch in ('MH1', 'MH2'):
    zero[ch] = sum(1 for r in rows[1:] if r.split(',')[2] == ch and r.split(',')[6] == '0')
lines.append('days with no catalogued interval of any type: MH1 %d, MH2 %d (of 330)' % (zero['MH1'], zero['MH2']))
open(OUT_S, 'w', newline='\n').write('\n'.join(lines) + '\n')
print('\n'.join(lines))
