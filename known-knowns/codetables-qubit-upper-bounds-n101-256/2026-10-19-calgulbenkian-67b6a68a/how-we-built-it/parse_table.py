"""Parse the codetables.de qubit table (Tables_color.php) saved exactly as fetched into JSON {n: {k: [lo, up]}}."""
import json, re, sys
src, out = sys.argv[1], sys.argv[2]
t = open(src, encoding='latin-1').read()
cells = re.findall(r'title="n=(\d+), k=(\d+)"[^>]*>([^<]*)</A>', t)
tab = {}
for n, k, v in cells:
    v = v.strip()
    m = re.fullmatch(r'(\d+)\s*-\s*(\d+)', v)
    lo, up = (int(m[1]), int(m[2])) if m else (int(v), int(v))
    tab.setdefault(int(n), {})[int(k)] = [lo, up]
json.dump(tab, open(out, 'w'))
print('cells', len(cells), 'n-range', min(tab), max(tab))
