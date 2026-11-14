"""Independent evaluator for pricing050 points (.sol format 'name value'). Double precision + 50-digit mpmath."""
import json, sys, mpmath
mpmath.mp.dps = 50
M = json.load(open(sys.argv[1]))
def read_sol(fn):
    v = {}
    for line in open(fn):
        p = line.split()
        if len(p) >= 2: v[p[0]] = p[1]
    return v
def evaluate(sol, use_mp=False):
    F = (lambda s: mpmath.mpf(s)) if use_mp else float
    ex = mpmath.exp if use_mp else __import__('math').exp
    x = {k: F(sol.get(k, '0')) for k in M['vars']}
    bviol = max(max(F(M['bounds'][k][0]) - x[k], x[k] - F(M['bounds'][k][1]), 0) for k in M['vars'])
    obj = sum(F(c) * x[k] for k, c in M['cost_in_e1'].items())
    cviol = 0; acts = []
    for r in M['rows']:
        lhs = sum(-F(t['a']) * x[t['var']] * ex(-F(t['b']) * x[t['var']] ** t['p']) for t in r['terms'])
        acts.append(lhs - F(r['rhs']))
        cviol = max(cviol, lhs - F(r['rhs']))
    e1 = obj - F(sol.get('objvar', '0')) if 'objvar' in sol else 0
    return obj, bviol, cviol, abs(e1), acts
if __name__ == '__main__':
    sol = read_sol(sys.argv[2])
    for mp in (False, True):
        obj, bv, cv, e1, acts = evaluate(sol, mp)
        print(('mpmath50' if mp else 'double  '), 'objective', mpmath.nstr(obj, 15) if mp else repr(obj), 'max_bound_viol', mpmath.nstr(bv, 5) if mp else bv,
              'max_con_viol', mpmath.nstr(cv, 5) if mp else cv, 'e1_resid(objvar line)', mpmath.nstr(e1, 5) if mp else e1)
        print('   row slacks (lhs-rhs, <=0 feasible):', [mpmath.nstr(a, 8) if mp else float('%.8g' % a) for a in acts])
