"""Parse the secondary 'Values of A(n,d,w)' tables of Andw.html (header row of n values, then a value row)."""
import re, sys
def parse2(path):
    h = open(path, encoding='latin-1').read()
    out = {}
    parts = re.split(r'<h3>Values of A\(n,(\d+),(\d+)\)</h3>', h)
    for i in range(1, len(parts), 3):
        d, w = int(parts[i]), int(parts[i + 1]); body = re.split(r'<h[123]>', parts[i + 2])[0]
        rows = [r for r in re.findall(r'<tr>(.*?)</tr>', body, re.S) if 'class="sep"' not in r]
        for a, b in zip(rows[0::2], rows[1::2]):
            ns = [re.sub(r'<[^>]*>', '', x).strip() for x in re.findall(r'<td[^>]*>(.*?)</td>', a, re.S)]
            vs = re.findall(r'<td[^>]*>(.*?)</td>', b, re.S)
            for nn, c in zip(ns, vs):
                if not nn.isdigit(): continue
                t = re.sub(r'<sup>.*?</sup>', '', c, flags=re.S); t = re.sub(r'<[^>]*>', '', t).strip()
                if not re.search(r'\d', t): continue
                if not re.match(r'\s*\d', t):
                    print('skip unparsed', (nn, d, w), repr(t)); continue
                if '-' in t:
                    x, y = t.split('-', 1); lo = int(re.findall(r'\d+', x)[0]); yy = re.findall(r'\d+', y); hi = int(yy[0]) if yy else None
                else:
                    lo = hi = int(re.findall(r'\d+', t)[0])
                out[(int(nn), d, w)] = (lo, hi, t)
    return out
if __name__ == '__main__':
    c = parse2(sys.argv[1]); print(len(c), 'cells;', sum(1 for v in c.values() if v[0] != v[1]), 'open')
    import collections; print(sorted(collections.Counter((d, w) for n, d, w in c).items()))
    for k in [(37,10,6),(51,6,5),(33,10,6),(47,6,6)]: print(k, c.get(k))
