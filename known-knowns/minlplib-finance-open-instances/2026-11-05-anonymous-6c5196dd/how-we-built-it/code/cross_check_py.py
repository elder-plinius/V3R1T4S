"""Cross-check the GAMS (.gms) parse against MINLPLib's Pyomo (.py) version of the same instance: evaluate every
constraint body of both at the same points and compare residuals (lhs - rhs) equation by equation.
Name mapping (from the .py header 'Reformulation has removed 1 variable and 1 equation'): pricing050 py x_k = gms x_(k+1),
py e_k = gms e_(k+1) (gms e1 = objective definition removed); saa_2 py index >= 4006 is gms index + 1
(objvar defined by gms e4003 removed), py e_k = gms e_k for k <= 4002 and gms e_(k+1) for k >= 4003."""
import re, sys, math, random
inst = sys.argv[1]; gms = sys.argv[2]; py = sys.argv[3]; sol = sys.argv[4]
src = open(py).read()
cons = {}
for m in re.finditer(r'm\.(e\d+) = Constraint\(expr=(.*?)\)\n\nm\.|m\.(e\d+) = Constraint\(expr=(.*?)\)\n', src, re.S):
    pass
blocks = re.split(r'\n(?=m\.e\d+ = Constraint)', src)
for b in blocks:
    m = re.match(r'm\.(e\d+) = Constraint\(expr=(.*)\)\s*$', b.strip().split('\n\n')[0], re.S)
    if not m: continue
    e = re.sub(r'\s+', ' ', m.group(2))
    mm = re.fullmatch(r'(.*?)(==|>=|<=)\s*([-0-9.eE+]+)', e.strip())
    assert mm, e[:100]
    body = re.sub(r'\bm\.([xb]\d+)\b', r'V["\1"]', mm.group(1)); body = re.sub(r'(?<![.\w])exp\s*\(', 'math.exp(', body)
    cons[m.group(1)] = (compile(body, m.group(1), 'eval'), mm.group(2), float(mm.group(3)))
print(inst, 'py constraints parsed:', len(cons))
def py2gms_var(v):
    k = int(v[1:])
    if inst == 'pricing050': return 'x%d' % (k + 1)
    return v[0] + str(k + 1 if k >= 4006 else k)
def py2gms_eq(e):
    k = int(e[1:])
    if inst == 'pricing050': return 'e%d' % (k + 1)
    return 'e%d' % (k + 1 if k >= 4003 else k)
pyvars = sorted(set(re.findall(r'\bm\.([xb]\d+)\b', src)), key=lambda z: int(z[1:]))
# gms side: generic evaluator (saa2_eval.load handles both formats' equations with only + - * ( ) for saa_2;
# for pricing050 add exp/power/sqr)
gt = open(gms).read()
gbody = gt.split('Equations', 1)[1].split(';', 1)[1].split('Model', 1)[0]
geqs = {}
for n, e, s, r in re.findall(r'(e\d+)\.\.(.*?)=([EGL])=(.*?);', gbody, re.S):
    e = re.sub(r'\s+', ' ', e).strip()
    e = re.sub(r'\b([xb]\d+|objvar)\b', r'V["\1"]', e)
    e = re.sub(r'\bsqr\s*\(', 'SQR(', e); e = re.sub(r'\bpower\s*\(', 'POW(', e); e = re.sub(r'\bexp\s*\(', 'math.exp(', e)
    geqs[n] = (compile(e, n, 'eval'), s, float(r))
env = {'math': math, 'SQR': lambda a: a * a, 'POW': lambda a, p: a ** p}
base = {}
for line in open(sol):
    p = line.split()
    if len(p) >= 2: base[p[0]] = float(p[1])
rnd = random.Random(5); worst = 0; n = 0
for trial in range(6):
    G = dict(base)
    if trial:
        for k in list(G): G[k] = G[k] * (1 + 0.01 * rnd.uniform(-1, 1))
        for v in pyvars:
            gv = py2gms_var(v)
            if gv not in G: G[gv] = rnd.uniform(0, 1) if trial > 3 else 0.0
    Vg = dict(G); Vg.setdefault('objvar', 0.0)
    for v in pyvars: Vg.setdefault(py2gms_var(v), 0.0)
    Vp = {v: Vg[py2gms_var(v)] for v in pyvars}
    for e, (code, sense, rhs) in cons.items():
        ge = py2gms_eq(e)
        gcode, gs, grhs = geqs[ge]
        rp = eval(code, dict(env, V=Vp)) - rhs
        rg = eval(gcode, dict(env, V=Vg)) - grhs
        d = abs(rp - rg) / (1 + abs(rg)); worst = max(worst, d); n += 1
        assert {'==': 'E', '>=': 'G', '<=': 'L'}[sense] == gs, (e, ge)
print('compared', n, 'residual pairs over 6 points (posted point + 5 perturbed/random); max relative difference %.3g' % worst)
print('CROSSCHECK', 'PASS' if worst < 1e-9 else 'FAIL')
