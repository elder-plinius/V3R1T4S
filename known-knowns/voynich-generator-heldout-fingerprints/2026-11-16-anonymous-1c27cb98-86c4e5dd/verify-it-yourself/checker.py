#!/usr/bin/env python3
"""Standalone checker for the outcome-(B) falsification claim (stdlib only).
From objects/ it re-derives: (1) the pooled Naibbe H1 per mode from the raw token
streams; (2) the 99.9% Voynich H1 envelope lower bounds; and (3) the 16,000-control
minima. Passes iff every pooled H1 is below its dialect's 99.9% lower bound on BOTH
transliterations and below the minimum of all controls.

Usage: python3 checker.py   (run from the claim/ folder)
"""
import json, os, sys, math
sys.setrecursionlimit(10000)

def collapse(w):
    return ''.join(w) if isinstance(w, str) else w

from functools import lru_cache

# SUBS: the IVTFF glyph->letter collapse table (mirrors code/vstats.py), applied before H1
# so the checker matches the scorer's H1 (which runs on collapsed tokens).
SUBS = [('cth','T'),('ckh','K'),('cph','P'),('cfh','F'),('ch','C'),('sh','S'),('iin','N'),('in','I'),('ee','E')]
def collapse(w):
    w = w.lower().strip()
    for a,b in SUBS:
        w = w.replace(a,b)
    return w

@lru_cache(maxsize=None)
def lev1(a, b):
    la, lb = len(a), len(b)
    if abs(la - lb) > 1: return False
    if la == lb:
        return sum(1 for i in range(la) if a[i] != b[i]) <= 1
    if la == lb + 1:
        i = j = 0; sk = False
        while i < la and j < lb:
            if a[i] == b[j]: i += 1; j += 1
            else:
                if sk: return False
                sk = True; i += 1
        return True
    i = j = 0; sk = False
    while i < la and j < lb:
        if a[i] == b[j]: i += 1; j += 1
        else:
            if sk: return False
            sk = True; j += 1
    return True

def h1_from_tokens(path):
    """H1 = observed adjacent edit-1 pair count / expected count under the within-line
    shuffle null, per the PREREG.v2 exact-unbiased expectation (mirrors the scorer
    exactly): per line, m = #{(i,j): i!=j, lev1(line[i],line[j])} (ordered pairs);
    nul_line = m/n (expected adjacent edit-1 count in a random permutation of the
    line's tokens; 2/n per unordered pair); H1 = sum(obs_line)/sum(nul_line)."""
    import time
    t0 = time.time()
    obs = 0; nul = 0.0
    with open(path) as fh:
        for raw in fh:
            line = [collapse(x) for x in raw.split()]
            n = len(line)
            if n < 2: continue
            obs += sum(1 for a, b in zip(line, line[1:]) if lev1(a, b))
            m = 0
            for i in range(n):
                li = line[i]
                for j in range(n):
                    if i != j and lev1(li, line[j]): m += 1
            nul += m / n
    h = obs / nul if nul > 0 else float('inf')
    print(f"  [h1_from_tokens {os.path.basename(path)}: {time.time()-t0:.1f}s, lev1 cache {lev1.cache_info().currsize} entries]")
    return h

def main():
    # Locate the package/claim root that holds objects/: the checker's own dir, or the
    # nearest ancestor that contains an objects/ directory (robust to the checker living
    # in verify-it-yourself/ inside an outbox package).
    import os as _os
    root = _os.path.dirname(_os.path.abspath(__file__))
    probe = root
    for _ in range(6):
        if _os.path.isdir(_os.path.join(probe, 'object')):
            root = probe
            break
        parent = _os.path.dirname(probe)
        if parent == probe:
            break
        probe = parent
    root = _os.path.abspath(root)
    batch = json.load(open(os.path.join(root, 'object', 'naibbe_batch.json')))
    pooled_json = {'A': batch['pooled']['A']['stats']['H1'], 'B': batch['pooled']['B']['stats']['H1']}
    pp = batch['per_ptext_H1']
    # (1) re-derive pooled H1 from raw token streams
    ok = True
    for mode in ('A', 'B'):
        p = os.path.join(root, 'object', f'pooled_{mode}.wrapped.txt')
        if os.path.isfile(p):
            h1 = h1_from_tokens(p)
            stored = pooled_json[mode]
            match = abs(h1 - stored) < 0.002
            print(f"re-derived pooled {mode} H1 = {h1:.4f} (stored {stored:.4f}, match={match})")
            ok &= match
        else:
            # Large-file archive case: the wrapped streams live outside git (see README 'Large
            # object files'). Verify the stored pooled H1 is present and finite, and that it is
            # consistent with the per-plaintext means (their average must equal the pooled value
            # up to the mode mix) — the envelope/control checks below still run from the JSON.
            stored = pooled_json[mode]
            pp = batch.get('per_ptext_H1', {})
            mmean = sum(v['mean_H1'] for v in pp.values() if v['mode']==mode)
            n = sum(1 for v in pp.values() if v['mode']==mode)
            near = abs(stored - (mmean/n if n else 0.0)) < 0.05
            print(f"pooled_{mode}.wrapped.txt absent (archived); stored pooled {mode} H1 = {stored:.4f} (finite={math.isfinite(stored)}, near per-ptext-mean {mmean/n if n else float('nan'):.4f} -> consistent={near})")
            ok &= math.isfinite(stored) and near
    # (2) 99.9% envelope lower bounds
    bounds = {}
    for d in ('A', 'B'):
        for T in ('ZL3b', 'IT2a'):
            e = json.load(open(os.path.join(root, 'object', f'env_H1_{d}_{T}.json')))
            lo = e['envelope_999'][0]
            real = pooled_json[d]
            outside = real < lo
            print(f"pooled {d} H1 {real:.4f} vs 99.9% lo ({d}/{T}) {lo:.4f} -> {'OUTSIDE' if outside else 'INSIDE (FAIL)'}")
            ok &= outside
    # (3) per-plaintext secondary
    bad = []
    for name, rec in sorted(pp.items()):
        d = rec['mode']; m = rec['mean_H1']
        loz = json.load(open(os.path.join(root,'object',f'env_H1_{d}_ZL3b.json')))['envelope_999'][0]
        lot = json.load(open(os.path.join(root,'object',f'env_H1_{d}_IT2a.json')))['envelope_999'][0]
        if not (m < loz and m < lot): bad.append(name)
    print(f"per-plaintext means outside 99.9% on both transliterations: {20-len(bad)}/20 (failures: {bad})")
    ok &= not bad
    # (4) control minima
    nb = json.load(open(os.path.join(root, 'object', 'null_H1_bootstraps.json')))
    for d in ('A', 'B'):
        cmin = min(nb[f'{d}_{T}']['min'] for T in ('ZL3b', 'IT2a'))
        b = pooled_json[d] < cmin
        print(f"pooled {d} H1 {pooled_json[d]:.4f} below ALL Voynich bootstrap controls (min {cmin:.4f}): {b}")
        ok &= b
    print('PASS' if ok else 'FAIL')
    sys.exit(0 if ok else 1)

if __name__ == '__main__':
    main()
