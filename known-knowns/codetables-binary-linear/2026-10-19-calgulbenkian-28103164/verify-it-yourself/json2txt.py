import json,sys
d=json.load(open(sys.argv[1])); G=d['G']
assert len(G)==d['k'] and all(len(r)==d['n'] for r in G), 'shape'
assert all(0<=x<=3 for r in G for x in r)
print(d['n'],d['k'])
for r in G: print(*r)
