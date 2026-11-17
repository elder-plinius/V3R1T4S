"""PREREG N1: Knapmeyer-Endrun and Hammer 2015 Tables S1-S3 against the candidate times.

usage: kn_check.py TSV_DIR XLS_DIR
(1) rows parsed from the TSVs written by the shipped reader; (2) independent check: date strings YYYY/MM/DD and
time strings HH:MM:SS.ss found directly in the raw .xls bytes (8-bit and UTF-16LE), counted and compared.
Pass rule: no row with onset within +/- 5 min of the onset or the window start, and no [onset, onset + duration]
span containing them."""
import sys, os, re, datetime as dt

TSV, XLS = sys.argv[1], sys.argv[2]
TARGETS = {'onset': dt.datetime(1973, 11, 26, 7, 46, 28, 641000), 'window_start': dt.datetime(1973, 11, 26, 7, 45, 58, 641000),
           'second_candidate_onset': dt.datetime(1973, 10, 30, 2, 25, 51, 509000)}
rows = []
for f in sorted(os.listdir(TSV)):
    lines = open(os.path.join(TSV, f), encoding='utf-8').read().splitlines()
    for ln in lines[1:]:
        c = [x.strip() for x in ln.split('\t')]
        if len(c) < 3 or not re.fullmatch(r'\d{4}/\d{2}/\d{2}', c[0] or ''):
            if any(x for x in c):
                print('unparsed row in', f, ':', c)
            continue
        t = dt.datetime.strptime(c[0] + ' ' + c[1], '%Y/%m/%d %H:%M:%S.%f' if '.' in c[1] else '%Y/%m/%d %H:%M:%S')
        dur = float(c[2]) if c[2] else 0.0
        rows.append((t, dur, c[3] if len(c) > 3 else '', c[4] if len(c) > 4 else '', c[5] if len(c) > 5 else '', f.split('__')[0]))
rows.sort()
print('rows parsed:', len(rows), 'span', rows[0][0], '->', rows[-1][0])
by = {}
for r in rows:
    by[r[0].year] = by.get(r[0].year, 0) + 1
print('per year:', dict(sorted(by.items())))

# independent byte-level count
pat8 = re.compile(rb'(19\d\d)/(\d\d)/(\d\d)')
tot8 = 0; tot16 = 0; dates_raw = []
for f in sorted(os.listdir(XLS)):
    if not f.endswith('.xls'):
        continue
    b = open(os.path.join(XLS, f), 'rb').read()
    m8 = pat8.findall(b)
    u = b.decode('utf-16-le', errors='ignore')
    m16 = re.findall(r'(19\d\d)/(\d\d)/(\d\d)', u)
    u1 = b[1:].decode('utf-16-le', errors='ignore')
    m16 += re.findall(r'(19\d\d)/(\d\d)/(\d\d)', u1)
    tot8 += len(m8); tot16 += len(m16)
    dates_raw += ['%s/%s/%s' % tuple(x.decode() for x in m) for m in m8] + ['/'.join(m) for m in m16]
    print('raw bytes %s: 8-bit date strings %d, utf-16 date strings %d' % (f, len(m8), len(m16)))
tsv_dates = sorted(r[0].strftime('%Y/%m/%d') for r in rows)
print('raw date strings total', len(dates_raw), '; TSV rows', len(tsv_dates),
      '; same multiset:', sorted(dates_raw) == tsv_dates)
print('raw date strings in 1973-11:', sorted(d for d in dates_raw if d.startswith('1973/11')))
print('raw date strings in 1973-10-25..11-05:', sorted(d for d in dates_raw if '1973/10/25' <= d <= '1973/11/05'))

ok = True
for lab, T in TARGETS.items():
    hits = [r for r in rows if abs((r[0] - T).total_seconds()) <= 300 or r[0] <= T <= r[0] + dt.timedelta(seconds=r[1])]
    near = sorted(rows, key=lambda r: abs((r[0] - T).total_seconds()))[:3]
    print('%s %s: rows within +/- 5 min or spanning it: %d' % (lab, T.isoformat(), len(hits)))
    for r in near:
        print('   nearest %s (%+.1f h) dur %.1f s class %s ch %s cluster %s [%s]' % (
            r[0].isoformat(), (r[0] - T).total_seconds() / 3600, r[1], r[2], r[3], r[4], r[5]))
    if lab != 'second_candidate_onset' and hits:
        ok = False
print('N1 pass:', ok)
