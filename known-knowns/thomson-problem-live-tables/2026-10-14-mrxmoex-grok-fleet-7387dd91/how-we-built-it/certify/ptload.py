"""robust point-file loader: xyz (count + comment + 'LA x y z'), .dat (x y z per line), Deeter (one number per line)."""
import re
NUM = re.compile(r'^[-+]?(\d+\.?\d*|\.\d+)([eE][-+]?\d+)?$')
def tokens(f):
    lines = open(f).read().splitlines(); rows = []
    for l in lines:
        t = l.split()
        if len(t) in (3, 4) and all(NUM.match(x) for x in t[-3:]) and (len(t) == 3 or not NUM.match(t[0])):
            rows.append(t[-3:])
    if len(rows) >= 4: return [x for r in rows for x in r]
    flat = [x for l in lines for x in l.split() if NUM.match(x)]
    return flat[:len(flat)//3*3]
