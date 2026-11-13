"""Merge N nest-part outputs into one JSON line per day. usage: merge3.py P1 P2 [P3 ...] OUT"""
import sys, json
parts = [{json.loads(l)['doy']: json.loads(l) for l in open(p)} for p in sys.argv[1:-1]]
common = set.intersection(*[set(p) for p in parts])
with open(sys.argv[-1], 'w') as f:
    for d in sorted(common):
        r = dict(year=parts[0][d]['year'], doy=d, nests={})
        for p in parts:
            r['nests'].update(p[d]['nests'])
        f.write(json.dumps(r) + '\n')
print('days merged', len(common))
