"""Descriptive: around the A38 onset (1971-05-13 18:40:03.735 UTC), the last catalogued S14 MH1/MH2 interval before it
and the first after it in each of the six MH1/MH2 files (Spike, Step-Up, Step-Down) of the Liu, Xiao and Li (2025)
catalogue, and the longest interval (end - start) in each file.
usage: coverage_boundaries.py ARCHIVE.zip OUT.txt   (standard library only)"""
import sys, csv, io, zipfile, datetime as dt
ZIP, OUT = sys.argv[1:3]
ON = dt.datetime(1971, 5, 13, 18, 40, 3, 735000)


def T(s):
    s = s.strip()
    return dt.datetime.strptime(s[:26], '%Y-%m-%d %H:%M:%S.%f' if '.' in s else '%Y-%m-%d %H:%M:%S')


z = zipfile.ZipFile(ZIP)
lines = []
before, after = [], []
for kind in ('Spike', 'Step-Up', 'Step-Down'):
    for ch in ('MH1', 'MH2'):
        name = 'S14_ACC-%s_%s_all.csv' % (kind, ch)
        mem = [n for n in z.namelist() if n.endswith('/catalogs/' + name)][0]
        iv = [(T(r['Start time']), T(r['End time'])) for r in csv.DictReader(io.TextIOWrapper(z.open(mem), encoding='utf-8', newline=''))]
        b = max((x for x in iv if x[1] < ON), key=lambda x: x[1])
        a = min((x for x in iv if x[0] > ON), key=lambda x: x[0])
        md = max((x[1] - x[0]).total_seconds() for x in iv)
        before.append((b, name)); after.append((a, name))
        lines.append('%s: last interval before the onset %s to %s; first after %s to %s; longest interval %.3f s' % (
            name, b[0], b[1], a[0], a[1], md))
lb = max(before, key=lambda x: x[0][1]); fa = min(after, key=lambda x: x[0][0])
lines.append('all six MH1/MH2 files: last interval end before the onset %s (%s, %.3f s before the onset); first interval start after %s (%s, %.3f s after)' % (
    lb[0][1], lb[1], (ON - lb[0][1]).total_seconds(), fa[0][0], fa[1], (fa[0][0] - ON).total_seconds()))
open(OUT, 'w', newline='\n').write('\n'.join(lines) + '\n')
print('\n'.join(lines))
