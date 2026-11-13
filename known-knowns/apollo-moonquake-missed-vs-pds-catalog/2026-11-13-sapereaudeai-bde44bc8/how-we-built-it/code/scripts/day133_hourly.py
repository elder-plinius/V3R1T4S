"""Descriptive: catalogued S14 MH1/MH2 intervals (Spike, Step-Up, Step-Down; Liu, Xiao and Li 2025) per UTC hour on
1971-05-12..14, to see whether the catalogue covers the hours around the A38 window.
usage: day133_hourly.py ARCHIVE.zip OUT.txt   (standard library only)"""
import sys, csv, io, zipfile, datetime as dt, collections
ZIP, OUT = sys.argv[1:3]
z = zipfile.ZipFile(ZIP)
cnt = collections.Counter()
for kind in ('Spike', 'Step-Up', 'Step-Down'):
    for ch in ('MH1', 'MH2'):
        name = 'S14_ACC-%s_%s_all.csv' % (kind, ch)
        mem = [n for n in z.namelist() if n.endswith('/catalogs/' + name)][0]
        for r in csv.DictReader(io.TextIOWrapper(z.open(mem), encoding='utf-8', newline='')):
            s = r['Start time'].strip()
            if s.startswith(('1971-05-12', '1971-05-13', '1971-05-14')):
                cnt[(s[:13], kind)] += 1
lines = ['hour_utc,Spike,Step-Up,Step-Down (MH1 + MH2)']
h = dt.datetime(1971, 5, 12)
while h < dt.datetime(1971, 5, 15):
    k = h.strftime('%Y-%m-%d %H')
    lines.append('%s,%d,%d,%d' % (k, cnt[(k, 'Spike')], cnt[(k, 'Step-Up')], cnt[(k, 'Step-Down')]))
    h += dt.timedelta(hours=1)
open(OUT, 'w', newline='\n').write('\n'.join(lines) + '\n')
print('\n'.join(lines))
