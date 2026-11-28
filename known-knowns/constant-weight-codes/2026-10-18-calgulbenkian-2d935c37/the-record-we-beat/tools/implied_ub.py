"""Table-implied upper bound: min over the live printed upper bound, merged V3R1T4S claims, and the two Johnson rules
A(n,d,w) <= floor(n/w A(n-1,d,w-1)) and A(n,d,w) <= floor(n/(n-w) A(n-1,d,w)), applied recursively.
Usage: python3 -I implied_ub.py Andw.html [--extra n,d,w=U ...] n,d,w ..."""
import re, sys, functools, runpy
sys.argv, args = sys.argv[:2], sys.argv[2:]
src = open(sys.argv[1], encoding='utf-8', errors='replace').read()
import importlib.util, os
spec = importlib.util.spec_from_file_location('ac', os.path.join(os.path.dirname(__file__), 'andw_cells.py'))
sys.argv = [sys.argv[0], sys.argv[1]]
ac = importlib.util.module_from_spec(spec); spec.loader.exec_module(ac)
cells = ac.cells
extra = {}
qs = []
i = 0
while i < len(args):
    if args[i] == '--extra':
        k, v = args[i + 1].split('='); extra[tuple(map(int, k.split(',')))] = int(v); i += 2
    else:
        qs.append(tuple(map(int, args[i].split(',')))); i += 1
def printed(n, d, w):
    for key in ((n, d, w), (n, d, n - w)):
        t = cells.get(key)
        if t is None:
            continue
        lb = t.startswith('LB:'); t = t[3:] if lb else t
        t = t.replace('–', '-')
        m = re.match(r'^\D*?(\d+)\D*?-\D*?(\d+)', t)
        if m:
            return int(m.group(2))
        m = re.match(r'^(\d+)[A-Za-zÀ-ɏ]*$', t)
        if m and not lb:
            return int(m.group(1))  # exact value
    return None
@functools.lru_cache(None)
def U(n, d, w):
    if w > n - w:
        w = n - w
    if w < 0:
        return 0
    if 2 * w < d:
        return 1
    if n < 1:
        return 1
    best = 10 ** 18
    p = printed(n, d, w)
    if p is not None:
        best = p
    for k in ((n, d, w), (n, d, n - w)):
        if k in extra:
            best = min(best, extra[k])
    if w >= 1:
        best = min(best, n * U(n - 1, d, w - 1) // w)
    if n - w >= 1:
        best = min(best, n * U(n - 1, d, w) // (n - w))
    return best
sys.setrecursionlimit(100000)
for q in qs:
    print('A(%d,%d,%d)' % q, 'printed', printed(*q), 'implied', U(*q))
