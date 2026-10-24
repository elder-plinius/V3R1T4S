"""Deep trivial-derivation frontier at target lengths: from every public witness of length L-12..L+12, every way to
remove symbols from the ends (r_front + r_back <= max(0, Lw - L) + 4) and then add symbols to reach L. Additions of
up to 10 symbols in total are exhaustive over signs and splits; longer ones use a beam (width 64) that grows one end
at a time. Exact integer energies. usage: deep_derivations.py L1,L2,... out.json"""
import json, sys, itertools
import numpy as np
sys.path.insert(0, 'code')
def E(s):
    s = np.asarray(s, dtype=np.int64); c = np.correlate(s, s, 'full')[len(s):]; return int(np.dot(c, c))
pm = lambda b: np.array([1 if ch == '1' else -1 for ch in b], dtype=np.int8)
W = []
def add(L, bits, src):
    if len(bits) == L: W.append((L, src, bits))
for r in json.load(open('data/dimitrov_2206.12070/records_verified.json')): add(r['L'], r['bits'], 'Dimitrov')
for r in json.load(open('data/dimitrov_2206.12070/recovered.json')):
    if r['recovered']: add(r['L'], r['bits'], 'Dimitrov(restored)')
import os
if os.path.exists('data/erk2025/table3_verified.json'):
    for r in json.load(open('data/erk2025/table3_verified.json')): add(r['L'], r['bits'], 'ERK2025')
for f, lab in [('v1', 'BB2011v1'), ('v2', 'BB2011v2')]:
    for r in json.load(open(f'data/brest_boskovic_2011.00068/{f}_verified.json')): add(r['L'], r['bits'], lab)
for fn in ['2018-labs-skew.txt', '2016-labs-skew.txt']:
    for line in open(f'data/borkob_git_labs/{fn}'):
        p = line.split()
        if len(p) >= 4 and p[0].isdigit(): add(int(p[0]), p[3], 'borkob ' + fn[:4])
for fn, lab in [('data/published_arXiv2607.09688_verified.tsv', '2607.09688'), ('data/published_arXiv2409.07222_verified.tsv', '2409.07222'),
                ('data/mdayan8_refetch/all_best_this_work.tsv', 'mdayan8'), ('data/mdayan8_refetch/legendre_baseline.tsv', 'mdayan8 Legendre')]:
    for line in open(fn):
        p = line.split()
        if len(p) > 3 and p[0].isdigit(): add(int(p[0]), p[3], lab)
def extend_best(core, d):
    """min energy over all ways to add d symbols (split front/back); exhaustive for d <= 10, beam otherwise."""
    best = None
    if d <= 10:
        for a in range(d + 1):
            for sg in itertools.product((-1, 1), repeat=d):
                t = np.concatenate([np.array(sg[:a], dtype=np.int8), core, np.array(sg[a:], dtype=np.int8)])
                e = E(t)
                if best is None or e < best: best = e
        return best
    beam = [core]
    for _ in range(d):
        cand = []
        for b in beam:
            for x in (-1, 1):
                for side in (0, 1):
                    t = np.concatenate([[x], b]).astype(np.int8) if side == 0 else np.concatenate([b, [x]]).astype(np.int8)
                    cand.append((E(t), t.tobytes(), t))
        cand.sort(key=lambda z: z[0]); seen = set(); beam = []
        for e, k, t in cand:
            if k in seen: continue
            seen.add(k); beam.append(t)
            if len(beam) >= 64: break
    return min(E(b) for b in beam)
targets = [int(x) for x in sys.argv[1].split(',')]; out = {}
for L in targets:
    best = (None, None)
    for Lw, src, b in W:
        if not (L - 12 <= Lw <= L + 12): continue
        s = pm(b)
        maxr = max(0, Lw - L) + 4
        for rf in range(maxr + 1):
            for rb in range(maxr + 1 - rf):
                core = s[rf:Lw - rb]
                d = L - len(core)
                if d < 0 or (rf == rb == 0 and d == 0): continue
                if d > 12: continue
                e = extend_best(core, d) if d > 0 else E(core)
                if best[0] is None or e < best[0]: best = (e, f'{src} L={Lw} remove {rf}/{rb} add {d}')
    out[L] = dict(L=L, deep_bar=best[0], from_=best[1], F=round(L * L / (2 * best[0]), 4) if best[0] else None)
    print(f"L={L}: deepest trivial derivation E={best[0]} (F {out[L]['F']}) <- {best[1]}", flush=True)
json.dump(out, open(sys.argv[2], 'w'), indent=1)
