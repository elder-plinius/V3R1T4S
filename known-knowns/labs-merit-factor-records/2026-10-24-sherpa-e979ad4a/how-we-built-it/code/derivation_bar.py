"""Strict bar B(L) = min over (i) every published value or claim at L, (ii) public PR claims at L, (iii) every trivial
end-derivation of a published witness of length L-4..L+4 (remove 0..2 symbols at each end, add 0..2 symbols at each
end in every sign pattern). Exact integer energies throughout."""
import json, itertools, sys
import numpy as np
D = 'data'
def E_np(s):
    s = np.asarray(s, dtype=np.int64); c = np.correlate(s, s, 'full')[len(s):]; return int(np.dot(c, c))
def pm(b): return np.array([1 if ch == '1' else -1 for ch in b], dtype=np.int8)
wit = []   # (L, E, source, bits)
for r in json.load(open(f'{D}/dimitrov_2206.12070/records_verified.json')): wit.append((r['L'], r['E'], 'arXiv:2206.12070', r['bits']))
for f, lab in [('v1', 'arXiv:2011.00068v1'), ('v2', 'arXiv:2011.00068v2')]:
    for r in json.load(open(f'{D}/brest_boskovic_2011.00068/{f}_verified.json')): wit.append((r['L'], r['E'], lab, r['bits']))
for fn in ['2018-labs-skew.txt', '2016-labs-skew.txt']:
    for line in open(f'{D}/borkob_git_labs/{fn}'):
        p = line.split()
        if len(p) >= 4 and p[0].isdigit(): wit.append((int(p[0]), int(p[2]), 'borkob/git_labs ' + fn, p[3]))
for fn, lab in [('published_arXiv2607.09688_verified.tsv', 'arXiv:2607.09688'), ('published_arXiv2409.07222_verified.tsv', 'arXiv:2409.07222')]:
    for line in open(f'{D}/{fn}'):
        p = line.split()
        if len(p) >= 4 and p[0].isdigit(): wit.append((int(p[0]), int(p[1]), lab + ' (seq. as extracted by mdayan8, energy re-verified)', p[3]))
good = []
for L, E, src, b in wit:
    if len(b) == L and E_np(pm(b)) == E: good.append((L, E, src, b))
print('witnesses', len(wit), 'verified', len(good))
front = {r['L']: r for r in json.load(open(f'{D}/frontier_121_449.json'))}
pr = {232: 3032, 242: 3337, 252: 3534, 328: 7148, 338: 7609, 377: 9452, 380: 10058, 384: 10192, 391: 10471, 463: 14047, 464: 14396}
lo, hi = int(sys.argv[1]), int(sys.argv[2])
out = {}
for L in range(lo, hi + 1):
    rec = {'L': L}
    pub = [(w[1], w[2]) for w in good if w[0] == L]
    if L in front: pub.append((front[L]['best_E'], front[L]['best_src']))
    rec['published'] = min(pub) if pub else None
    rec['pr_claim'] = pr.get(L)
    best = None
    for Ls, Es, src, b in good:
        if not (L - 4 <= Ls <= L + 4) or Ls == L and False: continue
        s = pm(b)
        for rf, rb, af, ab in itertools.product(range(3), repeat=4):
            if Ls - rf - rb + af + ab != L or (rf, rb, af, ab) == (0, 0, 0, 0): continue
            core = s[rf:Ls - rb]
            for signs in itertools.product((-1, 1), repeat=af + ab):
                t = np.concatenate([np.array(signs[:af], dtype=np.int8), core, np.array(signs[af:], dtype=np.int8)])
                e = E_np(t)
                if best is None or e < best[0]: best = (e, Ls, src, f'remove {rf} front/{rb} back, add {af} front/{ab} back')
    rec['derivation'] = best
    cands = [x for x in [rec['published'][0] if rec['published'] else None, rec['pr_claim'], best[0] if best else None] if x is not None]
    rec['bar'] = min(cands); rec['bar_F'] = round(L * L / (2 * rec['bar']), 4)
    rec['bar_from'] = 'published' if rec['published'] and rec['bar'] == rec['published'][0] else ('pr' if rec['bar'] == rec['pr_claim'] else 'derivation')
    out[L] = rec
json.dump(out, open(f'{D}/bar_{lo}_{hi}.json', 'w'), indent=1)
for L in range(lo, hi + 1):
    r = out[L]; p = r['published']; d = r['derivation']
    print(f"L={L}: bar {r['bar']} (F {r['bar_F']}, {r['bar_from']}) | published {p[0] if p else '-'} | deriv {d[0] if d else '-'} from L={d[1] if d else '-'}")
