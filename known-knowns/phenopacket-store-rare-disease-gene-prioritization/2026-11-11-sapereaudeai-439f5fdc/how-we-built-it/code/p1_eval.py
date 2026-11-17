"""Lens p1-eval: partial win p1 exactly as frozen in PREREG.md (rules part sha256 25573018...f1ff).

Reuses run 3's panelled per-case head-to-head table unchanged. Subset: n_terms <= 3 (run 1's definition: distinct
observed HPO terms mapped under HP:0000118). Gate: G1 MRR ratio >= 1.10 (point); G2 paired case-bootstrap 95% interval
of dMRR > 0; G3 paired label-swap null, real dMRR beats all 400 controls. Everything else is reported, not gated.

Usage: python -I p1_eval.py <h2h_percase.tsv> <run1 C_percase.tsv> <out_dir>
"""
import collections
import csv
import hashlib
import json
import os
import random
import sys

import numpy as np

SEED = 20261111
B = 2000
EXPECT = {'h2h': '4d0f30083447be88d8b9b11104776798e4f2b7ed6a9ff062886041aeb96680a9',
          'c1': '1e36379c9a57daf665335806b7585c0e165cf5fc918b368c2145daaf67b08b6f'}


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def stats(A, ix, ref):
    mM, mR = A['rr_M'][ix].mean(), A['rr_' + ref][ix].mean()
    tM, tR = A['top1_M'][ix].mean(), A['top1_' + ref][ix].mean()
    kM, kR = A['top10_M'][ix].mean(), A['top10_' + ref][ix].mean()
    return np.array([mM, mR, mM - mR, mM / mR if mR > 0 else np.inf, tM, tR, tM - tR, kM, kR, kM - kR])


NAMES = ['MRR_method', 'MRR_lirical', 'dMRR', 'MRR_ratio', 'top1_method', 'top1_lirical', 'dTop1',
         'top10_method', 'top10_lirical', 'dTop10']


def analyse(A, pm, ref):
    """A: dict of arrays restricted to the subset (in table order); pm: source PMID per case."""
    n = len(pm)
    allix = np.arange(n)
    pt = stats(A, allix, ref)
    rng = np.random.default_rng(SEED)
    bc = np.array([stats(A, rng.integers(0, n, n), ref) for _ in range(B)])
    u = sorted(set(pm)); mem = collections.defaultdict(list)
    for i, c in enumerate(pm):
        mem[c].append(i)
    rng2 = np.random.default_rng(SEED + 1)
    bp = np.array([stats(A, np.concatenate([mem[u[j]] for j in rng2.integers(0, len(u), len(u))]), ref)
                   for _ in range(B)])
    ci = lambda a: [float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5))]
    block = {nm: {'point': float(pt[j]), 'ci95_case_paired': ci(bc[:, j]), 'ci95_pub_cluster': ci(bp[:, j])}
             for j, nm in enumerate(NAMES)}
    d = A['rr_M'] - A['rr_' + ref]; real = float(d.mean()); ctrl = []
    for k in range(400):
        r = random.Random(SEED + k)
        s = np.array([(-1.0 if r.random() < 0.5 else 1.0) for _ in range(n)])
        ctrl.append(float((s * d).mean()))
    null = {'controls': 400, 'best_control': max(ctrl), 'real': real, 'real_beats_all_controls': bool(real > max(ctrl)),
            'n_controls_ge_real': int(sum(c >= real for c in ctrl))}
    gate = {'G1_MRR_ratio_point_ge_1.10': bool(pt[3] >= 1.10),
            'G2_dMRR_case_ci_lower_gt_0': bool(block['dMRR']['ci95_case_paired'][0] > 0),
            'G3_null_real_beats_all_400': null['real_beats_all_controls']}
    gate['P1_MET'] = all(gate.values())
    info = {'strict_ratio_case_ci_lower_ge_1.10': bool(block['MRR_ratio']['ci95_case_paired'][0] >= 1.10),
            'strict_ratio_pub_ci_lower_ge_1.10': bool(block['MRR_ratio']['ci95_pub_cluster'][0] >= 1.10),
            'dMRR_pub_ci_lower_gt_0': bool(block['dMRR']['ci95_pub_cluster'][0] > 0),
            'top1_ratio_point': float(pt[4] / pt[5]) if pt[5] > 0 else None,
            'bootstrap_fraction_ratio_ge_1.10': float(np.mean(bc[:, 3] >= 1.10))}
    return {'n_cases': n, 'n_pmids': len(u), 'stats': block, 'gate': gate, 'info_not_gates': info, 'null_NSF_dMRR': null}


def main(h2h, c1, out):
    os.makedirs(out, exist_ok=True)
    got = {'h2h': sha(h2h), 'c1': sha(c1)}
    print('sha256 h2h %s expected %s -> %s' % (got['h2h'], EXPECT['h2h'], got['h2h'] == EXPECT['h2h']))
    print('sha256 run1 C_percase %s expected %s -> %s' % (got['c1'], EXPECT['c1'], got['c1'] == EXPECT['c1']))
    if got != EXPECT:
        sys.exit('E2: integrity mismatch, stop')
    rows = list(csv.DictReader(open(h2h, encoding='utf-8'), delimiter='\t'))
    r1 = {r['case_id']: int(r['n_terms']) for r in csv.DictReader(open(c1, encoding='utf-8'), delimiter='\t')}
    mism = [r['case_id'] for r in rows if r1.get(r['case_id']) != int(r['n_terms'])]
    print('cases %d; run1 cases %d; n_terms mismatches vs run 1: %d' % (len(rows), len(r1), len(mism)))
    if mism or len(rows) != 10189 or set(r1) != {r['case_id'] for r in rows}:
        sys.exit('E2: n_terms cross-check failed, stop')
    keys = ['rr_M', 'top1_M', 'top10_M', 'rr_L', 'top1_L', 'top10_L', 'rr_L2', 'top1_L2', 'top10_L2', 'n_terms']
    Afull = {k: np.array([float(r[k]) for r in rows]) for k in keys}
    pmfull = np.array([r['pmid'] for r in rows])
    sub = Afull['n_terms'] <= 3
    hist = collections.Counter(int(x) for x in Afull['n_terms'][sub])
    print('p1 subset (n_terms <= 3): %d cases; by n_terms %s' % (sub.sum(), dict(sorted(hist.items()))))
    res = {'subset_definition': 'included cases with n_terms <= 3 (distinct observed HPO terms mapped by hp.obo '
                                'v2026-06-06 under HP:0000118; run 1 definition)',
           'inputs_sha256': got, 'n_terms_histogram': dict(sorted(hist.items()))}
    A = {k: v[sub] for k, v in Afull.items()}
    pm = list(pmfull[sub])
    res['vs_LIRICAL'] = analyse(A, pm, 'L')
    res['vs_LIRICAL_L2_sensitivity'] = analyse(A, pm, 'L2')
    comp = ~sub
    res['complement_gt3_context'] = {'n': int(comp.sum()), 'MRR_method': float(Afull['rr_M'][comp].mean()),
                                     'MRR_lirical': float(Afull['rr_L'][comp].mean()),
                                     'top1_method': float(Afull['top1_M'][comp].mean()),
                                     'top1_lirical': float(Afull['top1_L'][comp].mean())}
    json.dump(res, open(os.path.join(out, 'p1_summary.json'), 'w'), indent=1)
    with open(os.path.join(out, 'p1_subset_cases.tsv'), 'w', encoding='utf-8', newline='') as fh:
        w = csv.writer(fh, delimiter='\t', lineterminator='\n')
        w.writerow(['case_id', 'pmid', 'gene', 'n_terms', 'rr_M', 'top1_M', 'rr_L', 'top1_L'])
        for r, f in zip(rows, sub):
            if f:
                w.writerow([r['case_id'], r['pmid'], r['gene'], r['n_terms'], r['rr_M'], r['top1_M'], r['rr_L'], r['top1_L']])
    v = res['vs_LIRICAL']; s = v['stats']
    f = lambda nm: '%.4f [%.4f, %.4f] pub [%.4f, %.4f]' % (s[nm]['point'], *s[nm]['ci95_case_paired'], *s[nm]['ci95_pub_cluster'])
    print('n %d cases, %d PMIDs' % (v['n_cases'], v['n_pmids']))
    for nm in NAMES:
        print('%-14s %s' % (nm, f(nm)))
    print('null N-SF: real %.6f best of 400 %.6f beats all: %s (controls >= real: %d)' %
          (v['null_NSF_dMRR']['real'], v['null_NSF_dMRR']['best_control'], v['null_NSF_dMRR']['real_beats_all_controls'],
           v['null_NSF_dMRR']['n_controls_ge_real']))
    print('GATE', json.dumps(v['gate']))
    print('INFO', json.dumps(v['info_not_gates']))
    l2 = res['vs_LIRICAL_L2_sensitivity']
    print('L2 sensitivity: MRR_lirical %.4f ratio %.4f [%.4f, %.4f] gate %s' %
          (l2['stats']['MRR_lirical']['point'], l2['stats']['MRR_ratio']['point'], *l2['stats']['MRR_ratio']['ci95_case_paired'],
           json.dumps(l2['gate'])))
    print('complement > 3 terms (context):', json.dumps(res['complement_gt3_context']))


if __name__ == '__main__':
    main(*sys.argv[1:4])
