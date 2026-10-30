"""Map GF(9) codes (n, kappa, d, max hull h) to qutrit EAQECC cells (n, kappa-l, n-kappa-l), l = 0..h, and report
cells where d beats the live table's d_lower. 'listed' = the (n,k,c) cell is printed on the page; otherwise the
effective d_lower is that of the largest listed c' <= c for that (n,k).
Usage: cells_from_codes.py cells.csv analysis_file [hullfield]"""
import csv, re, sys
from collections import defaultdict
cells = {}; byk = defaultdict(list)
for r in csv.DictReader(open(sys.argv[1])):
    n, k, c = int(r['n']), int(r['k']), int(r['c'])
    cells[(n, k, c)] = (int(r['d_lower']), int(r['d_upper']), r['title']); byk[(n, k)].append(c)
def eff(n, k, c):
    cs = [x for x in byk[(n, k)] if x <= c]
    if not cs: return None
    return max(cs)
field = sys.argv[3] if len(sys.argv) > 3 else 'hull'
for line in open(sys.argv[2]):
    kv = dict(x.split('=', 1) for x in line.split() if '=' in x)
    if 'd' not in kv: continue
    n, K, d = int(kv['n']), int(kv['K']), int(kv['d'])
    h = int(kv.get(field, kv.get('hull')))
    for l in range(0, h + 1):
        k, c = K - l, n - K - l
        if c < 1 or k < 0: continue
        c0 = eff(n, k, c)
        if c0 is None: continue
        dl, du, t = cells[(n, k, c0)]
        if d > dl:
            print(f"{line.split()[0]} {line.split()[1]} code [{n},{K},{d}] hull_used={l} -> [[{n},{k},{d};{c}]] "
                  f"table {'LISTED' if c0 == c else 'implied-from-c=%d' % c0} [[{n},{k},{dl}-{du};{c0}]] gain={d - dl} "
                  f"{'(d>d_upper!)' if d > du else ''} | {t[:60]}")
