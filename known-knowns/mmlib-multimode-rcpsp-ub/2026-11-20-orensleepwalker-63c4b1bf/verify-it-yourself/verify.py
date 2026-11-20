"""Standalone checker for the MMLIB+ package (Python standard library only), written from the bank's definition.
Usage: python3 verify-it-yourself/verify.py <package folder> <MMLIB_v2_1.zip>
The release zip is the GitHub release v2.1 of the MMLIB library (run_checks.sh downloads it and checks its sha256).
For each schedule in object/schedules/*.json it reads the instance from the release's MMLIB+.zip and checks: one valid mode per job,
non-renewable totals within availability, every precedence, renewable usage within capacity in every period, and the stated
makespan. It then compares the makespan with the values recorded at the claim's fetch in the-record-we-beat/values.csv (LB, the
SolutionsUpdate dataset UB and best-known value) and with UB-lit in the release Excel (sheet 'MMLIB+'), requiring makespan strictly
below all three UB values and not below the LB. Prints one line per schedule and PASS or FAIL last."""
import sys, os, io, re, csv, json, glob, zipfile, xml.etree.ElementTree as ET
P, RZ = sys.argv[1], sys.argv[2]

def read(t):
    L = t.splitlines(); n = int(re.search(r'jobs\s+\(incl\.\s*supersource/sink\s*\):\s*(\d+)', t).group(1))
    nR = int(re.search(r'- renewable\s*:\s*(\d+)', t).group(1)); nN = int(re.search(r'- nonrenewable\s*:\s*(\d+)', t).group(1))
    i = next(k for k, l in enumerate(L) if l.startswith('PRECEDENCE RELATIONS')) + 2; succ = {}; nm = {}
    for k in range(n):
        p = L[i + k].split(); j = int(p[0]) - 1; nm[j] = int(p[1]); succ[j] = [int(x) - 1 for x in p[3:3 + int(p[2])]]
    i = next(k for k, l in enumerate(L) if l.startswith('REQUESTS/DURATIONS')) + 3; modes = {j: [] for j in range(n)}; j = None
    while not L[i].startswith('*'):
        p = L[i].split()
        if len(p) == 3 + nR + nN: j = int(p[0]) - 1; p = p[1:]
        modes[j].append((int(p[1]), [int(x) for x in p[2:2 + nR]], [int(x) for x in p[2 + nR:2 + nR + nN]])); i += 1
    assert all(len(modes[j]) == nm[j] for j in range(n))
    i = next(k for k, l in enumerate(L) if 'RESOURCE AVAILABILITIES' in l) + 2; cap = [int(x) for x in L[i].split()]
    return n, succ, [modes[j] for j in range(n)], cap[:nR], cap[nR:nR + nN]

def check(inst, mode, start):
    n, succ, modes, Rc, Nc = inst
    if len(mode) != n or len(start) != n: return None, 'wrong length'
    if any(not (1 <= mode[j] <= len(modes[j])) for j in range(n)) or any(s < 0 for s in start): return None, 'bad mode or start'
    M = [modes[j][mode[j] - 1] for j in range(n)]; fin = [start[j] + M[j][0] for j in range(n)]
    for k, c in enumerate(Nc):
        if sum(m[2][k] for m in M) > c: return None, 'non-renewable %d over budget' % (k + 1)
    for j in range(n):
        for s in succ[j]:
            if start[s] < fin[j]: return None, 'precedence %d -> %d' % (j + 1, s + 1)
    T = max(fin)
    for k, c in enumerate(Rc):
        use = [0] * T
        for j in range(n):
            for t in range(start[j], fin[j]): use[t] += M[j][1][k]
        if max(use) > c: return None, 'renewable %d over capacity' % (k + 1)
    return T, 'valid'

outer = zipfile.ZipFile(RZ)
x = zipfile.ZipFile(io.BytesIO(outer.read('MMLIB_v2_1/MMLIB (Parameters and BKS).xlsx')))
A = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'; RN = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'
ss = [''.join(t.text or '' for t in si.iter(A + 't')) for si in ET.fromstring(x.read('xl/sharedStrings.xml')).findall(A + 'si')]
rid = [s.get(RN + 'id') for s in ET.fromstring(x.read('xl/workbook.xml')).find(A + 'sheets') if s.get('name') == 'MMLIB+'][0]
target = [r.get('Target') for r in ET.fromstring(x.read('xl/_rels/workbook.xml.rels')) if r.get('Id') == rid][0]
sheet = 'xl/' + target.lstrip('/').replace('xl/', '', 1)
excel = {}
for r in ET.fromstring(x.read(sheet)).iter(A + 'row'):
    v = {}
    for c in r.findall(A + 'c'):
        e = c.find(A + 'v')
        if e is not None: v[re.match(r'[A-Z]+', c.get('r')).group()] = ss[int(e.text)] if c.get('t') == 's' else e.text
    if str(v.get('D', '')).endswith('.mm') and str(v.get('O', '')).isdigit(): excel[v['D']] = int(v['O'])
inner = zipfile.ZipFile(io.BytesIO(outer.read('MMLIB_v2_1/MMLIB+.zip'))); files = {n.split('/')[-1]: n for n in inner.namelist() if n.endswith('.mm')}
rec = {r['file']: r for r in csv.DictReader(open(os.path.join(P, 'the-record-we-beat', 'values.csv')))}
S = sorted(glob.glob(os.path.join(P, 'object', 'schedules', '*.json'))); bad = 0; pts = 0
for p in S:
    w = json.load(open(p)); f = w['file']; r = rec[f]
    mk, why = check(read(inner.read(files[f]).decode()), [int(v) for v in w['modes']], [int(v) for v in w['starts']])
    lb, ub, bk, xu = int(r['lb']), int(r['dataset_ub']), int(r['bks_value']), excel[f]
    ok = mk == int(w['makespan']) and lb < ub and mk < ub and mk < bk and mk < xu and mk >= lb
    bad += not ok; pts += (ub - mk) if ok else 0
    print('%-14s LB %3d UB %3d BKS %3d Excel %3d ours %s %s %s' % (f, lb, ub, bk, xu, mk, why, 'ok' if ok else 'FAIL'))
print('%d of %d schedules verified, %d makespan units below the recorded UBs' % (len(S) - bad, len(S), pts))
print('PASS' if bad == 0 and len(S) == 30 else 'FAIL'); sys.exit(0 if bad == 0 and len(S) == 30 else 1)
