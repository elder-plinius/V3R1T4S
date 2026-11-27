#!/usr/bin/env python3
"""Random-perturbation search over exponent-box bounds.  usage: opt.py spec.json K SIGMA GENS [scale] [workers]
K = which root (1 lowest, 2 second).  Keeps spec.json.best (checkpoint) and appends to spec.json.log.
Each evaluation runs the GMP engine (../../evaluator-first/code/engine) with NT=1; at most `workers` at once."""
import json, sys, os, subprocess, random, copy, tempfile, math, time
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
ENG = os.path.join(HERE, '..', '..', 'evaluator-first', 'code')
sys.path.insert(0, ENG)
import mkbasis
def write_basis(spec, path):
    rows = mkbasis.gen(spec)
    with open(path, 'w') as f:
        f.write('L %d\nprec %d\nmasses %s\ncharges %s\nsym %d\nN %d\n' % (spec['L'], spec.get('prec', 384), ' '.join(spec['masses']),
                ' '.join(map(str, spec.get('charges', [1, 1, -1]))), spec.get('sym', 0), len(rows)))
        for t, vals in rows:
            f.write('%d %s\n' % (t, ' '.join('%.30f' % v for v in vals)))
    return len(rows)
def valid(spec):
    for bx in spec['boxes']:
        a, b, c = bx['a'], bx['b'], bx['c']
        if a[0] > a[1] or b[0] > b[1] or c[0] > c[1]: return False
        # each function must be integrable with every other: require a+b>0, a+c>0, b+c>0 at the box minima over all boxes
    mins = [min(bx[k][0] for bx in spec['boxes']) for k in 'abc']
    return mins[0] + mins[1] > 0.02 and mins[0] + mins[2] > 0.02 and mins[1] + mins[2] > 0.02
def evaluate(spec, K, sigma, nt=1, niter=6, timeout=3600):
    if not valid(spec): return None
    fd, path = tempfile.mkstemp(suffix='.txt', dir=os.environ.get('OPT_TMP', '/tmp')); os.close(fd)
    try:
        write_basis(spec, path)
        env = dict(os.environ, NT=str(nt))
        out = subprocess.run(['nice', os.path.join(ENG, 'engine'), path, 'eig', sigma, str(niter)], capture_output=True, text=True, env=env, timeout=timeout).stdout
    except Exception as ex:
        return None
    finally:
        os.unlink(path)
    cnt = None; E = None
    for line in out.splitlines():
        if 'roots_below_sigma' in line: cnt = int(line.split()[-1])
        if line.startswith('iter'): E = line.split()[-1]
    if cnt != K - 1 or E is None: return None
    return E
def perturb(spec, rng, scale):
    s = copy.deepcopy(spec)
    nb = len(s['boxes'])
    for _ in range(rng.choice([1, 1, 2, 3])):
        bx = s['boxes'][rng.randrange(nb)]
        key = rng.choice(['a', 'b', 'c', 'c', 'ci', 'ci'] if 'ci' in bx else ['a', 'b', 'c'])
        end = rng.randrange(2)
        if key == 'ci' or bx[key][end] <= 0:
            bx[key][end] = bx[key][end] + rng.gauss(0, scale) * max(0.3, abs(bx[key][end]))
            if key == 'ci': bx[key][end] = max(0.0, bx[key][end])
        else:
            bx[key][end] = bx[key][end] * math.exp(rng.gauss(0, scale))
        if bx[key][0] > bx[key][1]: bx[key] = [bx[key][1], bx[key][0]]
        if s.get('tie_ab') and key in 'ab': bx['b' if key == 'a' else 'a'] = list(bx[key])
    return s
if __name__ == '__main__':
    path, K, sigma, gens = sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4])
    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.15
    workers = int(sys.argv[6]) if len(sys.argv) > 6 else 6
    best = json.load(open(path + '.best')) if os.path.exists(path + '.best') else json.load(open(path))
    rng = random.Random(int(time.time()))
    Eb = evaluate(best, K, sigma)
    print('start', Eb, flush=True)
    log = open(path + '.log', 'a')
    from decimal import Decimal
    for gname in range(gens):
        cands = [perturb(best, rng, scale) for _ in range(workers)]
        with ThreadPoolExecutor(workers) as ex:
            res = list(ex.map(lambda s: evaluate(s, K, sigma), cands))
        ok = [(Decimal(E), i) for i, E in enumerate(res) if E is not None]
        if ok:
            Em, i = min(ok)
            if Eb is None or Em < Decimal(Eb):
                best, Eb = cands[i], res[i]
                json.dump(best, open(path + '.best', 'w'))
        log.write('%d %s\n' % (gname, Eb)); log.flush()
        if gname % 5 == 0: print(gname, Eb, flush=True)
    print('final', Eb)
