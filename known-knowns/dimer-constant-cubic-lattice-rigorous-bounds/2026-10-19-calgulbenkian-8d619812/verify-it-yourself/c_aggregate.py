import sys
sys.path.insert(0, '.')
import cwcheck as cw
from decimal import Decimal
rows = {}
for line in open(sys.argv[1]):
    if line.startswith('CHECK sector'):
        d = dict(x.split('=') for x in line.split()[1:5])
        n, den = d['ratio'].split('/')
        rows[int(d['sector'])] = cw.bound_from_ratio(int(n), int(den), 50)
mx = max(rows.values())
ok = len(rows) == 13 and cw.ceil6(mx) <= Decimal('0.452010') and rows[12] == mx
print('%s C implementation, all 13 sectors: maximum %.10f in sector %d, rounded up %s (claimed 0.452010)' % ('PASS' if ok else 'FAIL', mx, max(rows, key=rows.get), cw.ceil6(mx)))
sys.exit(0 if ok else 1)
