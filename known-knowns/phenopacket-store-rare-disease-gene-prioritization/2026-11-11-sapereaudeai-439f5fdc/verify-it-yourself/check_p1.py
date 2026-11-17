"""Standalone checker for partial win p1 (Python 3 standard library only). Run from the package folder.

Definition checked (bank p1): "Beat the reference tool's MRR by >= 10% relative on the subset of cases with <= 3 HPO
terms ..., with bootstrap intervals and identical candidate space." Readings fixed before the p1 statistics
(how-we-built-it/PREREG.md): subset = included cases whose number of distinct observed HPO terms (mapped by hp.obo
v2026-06-06, under HP:0000118) is <= 3; per-case RR = expected reciprocal rank of the causal gene among the same
19,274 protein-coding genes for both tools; G1 MRR ratio >= 1.10; G2 paired case-bootstrap 95% interval of the MRR
difference above 0; G3 the real difference beats all 400 paired label-swap controls.

Checks:
1. The object files have the sha256 recorded in INDEX.csv / below (a corrupted copy fails).
2. object/h2h_percase_all_cases.tsv.gz holds 10,189 distinct cases; the subset n_terms <= 3 selected here equals the
   rows of object/p1_subset_cases.tsv exactly (ids and values).
3. MRR of both tools, the ratio and G1, recomputed with plain sums, equal the claimed values.
4. G2 with an independent standard-library paired bootstrap (2,000 resamples, random.Random(20261111)); its lower
   end must be > 0 (the numpy interval in object/p1_summary.json is [0.0257, 0.0420]).
5. G3: the 400 label-swap controls, recomputed exactly as frozen (random.Random(20261111 + k), sign -1 when
   r.random() < 0.5); best control must equal the claimed 0.013722 (to 1e-6) and the real difference must beat it.
Last line: PASS or FAIL.
"""
import csv
import gzip
import hashlib
import io
import json
import random
import sys

EXPECT = {
    'object/p1_subset_cases.tsv': '439f5fdcfe13720bf61f201fe3b81c0a806ef3392f93da1491f1ab7fd9c98482',
    'object/h2h_percase_all_cases.tsv.gz': '1857481f0febecb3dd51f3dc3b8bd67a94ab7f22101cc9286ca1914d9e441c47',
}
CLAIM = {'n': 2038, 'MRR_method': 0.1384, 'MRR_lirical': 0.1047, 'ratio': 1.3218, 'best_control': 0.013722,
         'real': 0.033707}


def main():
    ok = True

    def check(cond, msg):
        nonlocal ok
        print(('ok    ' if cond else 'FAIL  ') + msg)
        ok = ok and bool(cond)

    for p, h in EXPECT.items():
        try:
            got = hashlib.sha256(open(p, 'rb').read()).hexdigest()
        except OSError as e:
            got = 'unreadable: %s' % e
        check(got == h, 'sha256 %s' % p)
    if not ok:
        print('FAIL'); return 1
    with gzip.open('object/h2h_percase_all_cases.tsv.gz', 'rt', encoding='utf-8') as fh:
        allrows = list(csv.DictReader(fh, delimiter='\t'))
    ids = [r['case_id'] for r in allrows]
    check(len(allrows) == 10189 and len(set(ids)) == 10189, 'all-case table: %d rows, %d distinct cases' % (len(allrows), len(set(ids))))
    sub = [r for r in allrows if int(r['n_terms']) <= 3]
    rows = list(csv.DictReader(open('object/p1_subset_cases.tsv', encoding='utf-8'), delimiter='\t'))
    same = [(r['case_id'], r['rr_M'], r['rr_L']) for r in sub] == [(r['case_id'], r['rr_M'], r['rr_L']) for r in rows]
    check(same and len(rows) == CLAIM['n'], 'subset n_terms <= 3 selected here = object/p1_subset_cases.tsv (%d rows)' % len(rows))
    check(all(1 <= int(r['n_terms']) <= 3 for r in rows), 'every subset case has 1 to 3 terms')
    M = [float(r['rr_M']) for r in rows]; L = [float(r['rr_L']) for r in rows]; n = len(rows)
    check(all(0.0 <= x <= 1.0 for x in M + L), 'all RR in [0, 1]')
    mM, mL = sum(M) / n, sum(L) / n
    print('      MRR method %.6f, LIRICAL %.6f, ratio %.6f' % (mM, mL, mM / mL))
    check(abs(mM - CLAIM['MRR_method']) < 5e-5 and abs(mL - CLAIM['MRR_lirical']) < 5e-5 and abs(mM / mL - CLAIM['ratio']) < 5e-5,
          'MRRs and ratio equal the claimed 0.1384 / 0.1047 / 1.3218')
    check(mM / mL >= 1.10, 'G1: MRR ratio >= 1.10')
    d = [a - b for a, b in zip(M, L)]
    rng = random.Random(20261111); boots = []
    for _ in range(2000):
        s = 0.0
        for _ in range(n):
            s += d[rng.randrange(n)]
        boots.append(s / n)
    boots.sort()
    lo, hi = boots[49], boots[1949]
    print('      stdlib paired bootstrap of the MRR difference: 95%% [%.4f, %.4f]' % (lo, hi))
    check(lo > 0, 'G2: paired case-bootstrap 95% interval of the difference lies above 0')
    real = sum(d) / n; ctrl = []
    for k in range(400):
        r = random.Random(20261111 + k)
        sg = [(-1.0 if r.random() < 0.5 else 1.0) for _ in range(n)]
        ctrl.append(sum(a * b for a, b in zip(sg, d)) / n)
    best = max(ctrl)
    print('      null: real %.6f, best of 400 controls %.6f' % (real, best))
    check(abs(best - CLAIM['best_control']) < 1e-6 and abs(real - CLAIM['real']) < 1e-6, 'null values equal the claimed ones')
    check(real > best, 'G3: real difference beats all 400 controls')
    summ = json.load(open('object/p1_summary.json', encoding='utf-8'))
    g = summ['vs_LIRICAL']['gate']
    check(g.get('P1_MET') is True and summ['vs_LIRICAL']['n_cases'] == n, 'object/p1_summary.json records the same gate and n')
    print('PASS' if ok else 'FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
