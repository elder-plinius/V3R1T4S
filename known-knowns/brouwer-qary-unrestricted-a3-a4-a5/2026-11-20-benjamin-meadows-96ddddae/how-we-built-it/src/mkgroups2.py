"""Wave-2 subgroup sampler: mkgroups.py plus wave-1 exclusion, an order focus band and the 'fix' symbol parts.

usage: python mkgroups2.py alph family lo hi samples seed outdir maxk focus excl
  focus: "a-b" (half of the kept subgroups come from orders a..b, the rest spread over all orders) or "-".
  excl: wave-1 sampler calls for the same alphabet and family, "lo:hi:samples:seed:maxk" joined by ',', or "-".
        Each is replayed exactly as mkgroups.py ran it in wave 1, and any subgroup with the same invariant
        (order, orbit signature, cycle-type census) as a wave-1 subgroup is dropped.
  symbol parts added here: fix (global S_{q-1} on symbols 1..q-1, symbol 0 fixed at every coordinate),
        fixaff (fix plus the global q-cycle at one coordinate per block, as in aff).
Writes the same files as mkgroups.py (manifest.tsv, g<k>.txt) plus excluded.txt (how many were dropped).
"""
import os, random, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mkgroups as M  # noqa: E402


def build(alph, family):
    cpart, spart = family.split('/')
    if spart not in ('fix', 'fixaff'):
        return M.build_gens(alph, family)
    n, Q, idc, ids, gens = M.build_gens(alph, cpart + '/none')
    for q, start, cnt in M.blocks_of(alph):
        for s in M.sym_gens_full(q - 1):
            perm = [0] + [1 + x for x in s] + list(range(q, Q))
            sy = list(ids)
            for i in range(start, start + cnt):
                sy[i] = tuple(perm)
            gens.append((idc, tuple(sy)))
        if spart == 'fixaff':
            sy = list(ids); sy[start] = tuple(list(range(1, q)) + [0] + list(range(q, Q)))
            gens.append((idc, tuple(sy)))
    return n, Q, idc, ids, gens


def spread(items, k):
    if k <= 0 or len(items) <= k:
        return list(items)
    if k == 1:
        return items[:1]
    return [items[round(i * (len(items) - 1) / (k - 1))] for i in range(k)]


def main():
    alph, family, lo, hi, samples, seed, out, maxk, focus, excl = sys.argv[1:11]
    lo, hi, samples, seed, maxk = int(lo), int(hi), int(samples), int(seed), int(maxk)
    n, Q, idc, ids, gens = build(alph, family)
    e = (idc, ids)
    os.makedirs(out, exist_ok=True)
    seen = set()
    if gens and excl != '-':
        for spec in excl.split(','):
            l1, h1, s1, sd1, k1 = map(int, spec.split(':'))
            old = M.sample(random.Random(sd1), gens, e, l1, h1, s1)
            if k1 and len(old) > k1:
                old = spread(old, k1)
            seen |= {M.invariant(S, n) for S in old}
    items = M.sample(random.Random(seed), gens, e, lo, hi, samples) if gens else []
    before = len(items)
    items = [S for S in items if M.invariant(S, n) not in seen]
    dropped = before - len(items)
    if maxk and len(items) > maxk:
        if focus != '-':
            a, b = map(int, focus.split('-'))
            inband = [S for S in items if a <= len(S) <= b]
            kb = min(len(inband), maxk // 2)
            pick = spread(inband, kb)
            ids_ = {id(S) for S in pick}
            rest = [S for S in items if id(S) not in ids_]
            pick += spread(rest, maxk - len(pick))
            items = sorted(pick, key=lambda S: -len(S))
        else:
            items = spread(items, maxk)
    with open(os.path.join(out, 'manifest.tsv'), 'w') as mf:
        for k, S in enumerate(items):
            with open(os.path.join(out, f'g{k}.txt'), 'w') as f:
                for p, s in sorted(S):
                    f.write(' '.join(map(str, p)) + ' ' + ' '.join(' '.join(map(str, t)) for t in s) + '\n')
            mf.write(f'{k}\t{len(S)}\t{family}\t{M.orbit_sig(S, n)}\n')
    open(os.path.join(out, 'excluded.txt'), 'w').write(f'{dropped} of {before} sampled subgroups matched wave 1 ({len(seen)} wave-1 invariants)\n')
    print(f'{alph} {family}: {len(items)} subgroups (orders {lo}..{hi}), {dropped} dropped as wave-1 repeats')


if __name__ == '__main__':
    main()
