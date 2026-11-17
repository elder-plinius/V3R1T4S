"""Lens sensitivity-audit (contrarian): try to break the p1 result.

1. Independent re-derivation of the subset: parse hp.obo v2026-06-06 with a minimal parser written here (not rdlib),
   map each observed id (alt_id -> primary, obsolete+replaced_by -> replacement, else dropped), keep terms under
   HP:0000118, de-duplicate, count; compare with the n_terms column; recompute both MRRs with plain Python sums.
2. Sensitivity subsets declared in PREREG (not gates): S1 raw observed ids <= 3; S2 observed + excluded raw ids <= 3.
3. Concentration: per-n_terms strata, leave-one-PMID-out extremes of the ratio, top contributing PMIDs, cases
   where both tools score ~0, DEV vs non-DEV.
Usage: python -I audit.py <h2h_percase.tsv> <cases.tsv> <hp.obo> <included_cases.txt> <dev500.txt> <out_dir>
"""
import collections
import csv
import json
import os
import random
import sys

import numpy as np


def parse_obo(path):
    terms, alt, repl, obs, parents = set(), {}, {}, set(), {}
    cur = None; in_term = False
    for line in open(path, encoding='utf-8'):
        line = line.rstrip('\n')
        if line.startswith('['):
            in_term = line == '[Term]'; cur = None; continue
        if not in_term:
            continue
        if line.startswith('id: '):
            cur = line[4:].strip(); terms.add(cur); parents.setdefault(cur, [])
        elif cur is None:
            continue
        elif line.startswith('alt_id: '):
            alt[line[8:].strip()] = cur
        elif line.startswith('is_obsolete: true'):
            obs.add(cur)
        elif line.startswith('replaced_by: '):
            repl[cur] = line[13:].strip()
        elif line.startswith('is_a: '):
            parents[cur].append(line[6:].split('!')[0].strip())
    return terms, alt, repl, obs, parents


def main(h2h, cases_tsv, obo, inc_txt, dev_txt, out):
    os.makedirs(out, exist_ok=True)
    terms, alt, repl, obs, parents = parse_obo(obo)
    memo = {}

    def under_root(t):
        if t in memo: return memo[t]
        stack, seen = [t], set()
        found = False
        while stack:
            x = stack.pop()
            if x == 'HP:0000118': found = True; break
            if x in seen: continue
            seen.add(x); stack.extend(parents.get(x, []))
        memo[t] = found; return found

    def mapt(t, depth=0):
        if t in terms and t not in obs: return t
        if t in alt and depth < 5: return mapt(alt[t], depth + 1)
        if t in obs and t in repl and depth < 5: return mapt(repl[t], depth + 1)
        return None

    inc = set(open(inc_txt).read().split())
    dev = set(open(dev_txt).read().split())
    raw = {}
    for r in csv.DictReader(open(cases_tsv, encoding='utf-8'), delimiter='\t'):
        if r['case_id'] in inc:
            ob = [t for t in r['observed'].split(';') if t]; ex = [t for t in r['excluded'].split(';') if t]
            mapped = {m for t in ob for m in [mapt(t)] if m is not None and under_root(m)}
            raw[r['case_id']] = (len(mapped), len(ob), len(ob) + len(ex))
    rows = list(csv.DictReader(open(h2h, encoding='utf-8'), delimiter='\t'))
    mism = sum(1 for r in rows if raw[r['case_id']][0] != int(r['n_terms']))
    print('independent n_terms re-derivation: %d cases, mismatches vs table: %d' % (len(rows), mism))
    sub = [r for r in rows if raw[r['case_id']][0] <= 3]
    mM = sum(float(r['rr_M']) for r in sub) / len(sub); mL = sum(float(r['rr_L']) for r in sub) / len(sub)
    print('plain-Python p1: n %d MRR_M %.6f MRR_L %.6f ratio %.6f' % (len(sub), mM, mL, mM / mL))
    res = {'n_terms_mismatches': mism, 'plain': {'n': len(sub), 'MRR_M': mM, 'MRR_L': mL, 'ratio': mM / mL}}

    def block(name, rs, seed=20261111):
        n = len(rs)
        M = np.array([float(r['rr_M']) for r in rs]); L = np.array([float(r['rr_L']) for r in rs])
        rng = np.random.default_rng(seed); rat = []; dif = []
        for _ in range(2000):
            ix = rng.integers(0, n, n); rat.append(M[ix].mean() / L[ix].mean()); dif.append(M[ix].mean() - L[ix].mean())
        d = M - L; ctrl = []
        for k in range(400):
            rr = random.Random(seed + k)
            s = np.array([(-1.0 if rr.random() < 0.5 else 1.0) for _ in range(n)]); ctrl.append(float((s * d).mean()))
        o = {'n': n, 'MRR_M': float(M.mean()), 'MRR_L': float(L.mean()), 'ratio': float(M.mean() / L.mean()),
             'ratio_ci': [float(np.percentile(rat, 2.5)), float(np.percentile(rat, 97.5))],
             'dMRR_ci': [float(np.percentile(dif, 2.5)), float(np.percentile(dif, 97.5))],
             'null_best': max(ctrl), 'null_real': float(d.mean()), 'beats_all': bool(d.mean() > max(ctrl))}
        print('%-28s n %5d MRR %.4f vs %.4f ratio %.4f [%.4f, %.4f] dMRR CI [%.4f, %.4f] null best %.5f real %.5f beats %s' %
              (name, n, o['MRR_M'], o['MRR_L'], o['ratio'], *o['ratio_ci'], *o['dMRR_ci'], o['null_best'], o['null_real'], o['beats_all']))
        return o

    S = {}
    S['p1_primary'] = block('p1 primary (mapped <= 3)', sub)
    S['S1_raw_observed_le3'] = block('S1 raw observed <= 3', [r for r in rows if raw[r['case_id']][1] <= 3])
    S['S2_obs_plus_excl_le3'] = block('S2 observed+excluded <= 3', [r for r in rows if raw[r['case_id']][2] <= 3])
    for k in (1, 2, 3):
        S['n_terms_eq_%d' % k] = block('n_terms == %d' % k, [r for r in sub if int(r['n_terms']) == k])
    S['p1_nonDEV'] = block('p1 excluding run-3 DEV cases', [r for r in sub if r['case_id'] not in dev])
    S['p1_method_gene_scored'] = block('p1, method gene score > 0', [r for r in sub if float(r['gscore_M']) > 0])
    # concentration by publication
    bypm = collections.defaultdict(list)
    for r in sub: bypm[r['pmid']].append(r)
    contrib = sorted(((sum(float(r['rr_M']) - float(r['rr_L']) for r in v), k, len(v)) for k, v in bypm.items()), reverse=True)
    tot = sum(float(r['rr_M']) - float(r['rr_L']) for r in sub)
    print('total dMRR*n %.3f; top 5 PMID contributions: %s' % (tot, [(k, n, round(c, 3)) for c, k, n in contrib[:5]]))
    print('bottom 3 PMID contributions: %s' % [(k, n, round(c, 3)) for c, k, n in contrib[-3:]])
    lopo = []
    for k in bypm:
        rs = [r for r in sub if r['pmid'] != k]
        lopo.append((sum(float(r['rr_M']) for r in rs) / sum(float(r['rr_L']) for r in rs), k))
    lopo.sort()
    print('leave-one-PMID-out ratio: min %.4f (drop %s) max %.4f (drop %s)' % (lopo[0][0], lopo[0][1], lopo[-1][0], lopo[-1][1]))
    top5 = {k for c, k, n in contrib[:5]}
    S['p1_drop_top5_PMIDs'] = block('p1 minus top-5 PMIDs', [r for r in sub if r['pmid'] not in top5])
    largest = sorted(bypm.items(), key=lambda kv: -len(kv[1]))[:5]
    print('largest PMIDs in subset (cases): %s' % [(k, len(v)) for k, v in largest])
    zero = sum(1 for r in sub if float(r['rr_M']) < 1e-3 and float(r['rr_L']) < 1e-3)
    print('subset cases where both RR < 0.001: %d' % zero)
    res.update({'subsets': S, 'top5_pmid_contrib': [(k, n, c) for c, k, n in contrib[:5]], 'lopo_ratio_min': lopo[0],
                'lopo_ratio_max': lopo[-1], 'both_rr_lt_0.001': zero, 'total_dMRR_times_n': tot})
    json.dump(res, open(os.path.join(out, 'audit_summary.json'), 'w'), indent=1)


if __name__ == '__main__':
    main(*sys.argv[1:7])
