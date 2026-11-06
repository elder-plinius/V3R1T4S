"""For every plain candidate (a,b,l) of out/candidates.txt with r = K_b - K_a <= RMAX: exact coset table
mu(c) = min affine weight of c.(rows of pole in (a,b]) + L(aP) (capped at D = lb + 1; hdep, Wmax D - 1, valid
because d(P_a) >= D for every candidate), then one tailg block "V a,b,l,n,k r l D mu...". Tables cached per (a,b,D).
Usage: gen_tail.py CAND CODEDIR HDEP OUTBLOCKS RMAX WORKERS"""
import sys, os, json, itertools, subprocess
from concurrent.futures import ThreadPoolExecutor
cand, cdir, hd, outp, RMAX, W = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5]), int(sys.argv[6])
sys.path.insert(0, cdir)
from hermitian import pts, pw
from gf9lib import MUL, ADD
mons = sorted([(i, j) for j in range(3) for i in range(30) if 3 * i + 4 * j <= 26], key=lambda t: 3 * t[0] + 4 * t[1])
rows = [[MUL[pw(x, i)][pw(y, j)] for x, y in pts] for i, j in mons]
pole = [3 * i + 4 * j for i, j in mons]
def proj(r): return [v for v in itertools.product(range(9), repeat=r) if [x for x in v if x][0:1] == [1]]
def mu_of(args):
    Ka, top, c, D = args
    v = [0] * 27
    for ci, t in zip(c, top):
        if ci: v = [ADD[x][MUL[ci][y]] for x, y in zip(v, t)]
    G = rows[:Ka] + [v]
    s = "%d 27\n" % len(G) + "\n".join(" ".join(map(str, rr)) for rr in G) + "\n"
    o = subprocess.run(["nice", "-n", "10", hd, str(D - 1)], input=s, capture_output=True, text=True).stdout
    return int(o.split("d=")[-1].split()[0]) if "dependent_min" in o else D
cands = [json.loads(x) for x in open(cand) if x.startswith('{')]
cands = [o for o in cands if o['ext'] == 0 and o['r'] <= RMAX]
cache = {}
with ThreadPoolExecutor(W) as ex, open(outp, "w") as f:
    for o in cands:
        a, b, D, l = o['a'], o['b'], o['lb'] + 1, o['l']
        Ka = sum(1 for p in pole if p <= a); Kb = sum(1 for p in pole if p <= b); r = Kb - Ka
        key = (a, b, D)
        if key not in cache:
            top = rows[Ka:Kb]
            cache[key] = list(ex.map(mu_of, [(Ka, top, c, D) for c in proj(r)]))
        f.write("V %d,%d,%d,%d,%d %d %d %d " % (a, b, l, o['n'], o['k'], r, l, D) + " ".join(map(str, cache[key])) + "\n"); f.flush()
        print("block", a, b, l, o['n'], o['k'], "D", D, "min mu", min(cache[key])); sys.stdout.flush()
