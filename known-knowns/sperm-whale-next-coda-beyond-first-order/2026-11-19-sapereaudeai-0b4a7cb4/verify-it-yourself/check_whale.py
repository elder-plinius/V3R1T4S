"""Standalone checker for the full success criterion of bank target
sperm-whale-next-coda-beyond-first-order. Python 3 standard library only.

Run from the package folder:  sh verify-it-yourself/run_checks.sh

The criterion, as the bank words it, pooled over the 5 held-out folds:
  (1) the model's cross-entropy is at least 0.10 bits per coda BELOW reference R1;
  (2) it is at least 0.05 bits below the same model retrained with its input cut to the single previous coda,
      and the 95% interval of a paired bootstrap over REC groups (10,000 resamples) for that gain excludes 0.

What this checker does NOT do: it does not refit the model. Refitting needs the source data and scipy, and is
covered by RUN_IT_YOURSELF.md and by the run's REPRODUCE panellist, who refit everything independently. This
checker verifies the arithmetic of the claim from the shipped object, which holds the per-position log-loss of
every model at every scored position, and it runs the bootstrap itself with its own seed.

Checks:
 1. every file in object/ has the sha256 recorded below, so a corrupted copy fails;
 2. the scored set is the bank's: 3,418 positions, each with at least 2 earlier codas, 5 folds each held out once,
    fold membership equal to object/folds.csv and per-fold counts equal to object/content_summary.json;
 3. every per-position loss is finite and strictly positive (a full distribution with no zero and no probability
    of exactly 1 at the true token);
 4. the pooled cross-entropies recomputed from the per-position losses equal object/content_summary.json;
 5. condition (1): R1 minus full is at least 0.10 bits;
 6. condition (2): twin minus full is at least 0.05 bits, and this checker's own 10,000-resample paired bootstrap
    over REC groups (its own seed, not the claim's) has a 95% interval that excludes 0;
 7. the null test in how-we-built-it/null_test.md reports at least 400 controls, says the real gain beat all of
    them, and its stated real gain equals the twin gain recomputed here.
Last line: PASS or FAIL.
"""
import csv
import hashlib
import json
import os
import random
import re
import sys

EXPECT = {
    'bin_edges.csv': 'c05e94716fa83081c247b1200aa259a68d91c75bd4d89b6c64046c7182903967',
    'content_summary.json': '9d2c0aecae9623a83a51db0f3d69e8157100f2c128910027af3599c0e3a09a5f',
    'folds.csv': '675bd6cbd2250d2eaf24fe560ee22e4889a683876fe4d070ad97d117a8519e82',
    'per_position_bits.csv': '0b4a7cb45ddd85aa53e1ea793007cc6af54c83b3ce9e42ea32e41ace1a294c03',
    'run_output.txt': 'b40802b0eb0a38d9e947aa85ce7056e84a60814c7064975bd719db99b350143b',
}
N_SCORED = 3418
N_FOLDS = 5
MODELS = ['R1', 'twin', 'rep', 'local', 'full']
COND1_MIN = 0.10
COND2_MIN = 0.05
RESAMPLES = 10000
SEED = 8675309          # this checker's own seed, deliberately not the claim's

fails = []


def ok(cond, msg):
    print(('ok   ' if cond else 'FAIL ') + msg)
    if not cond:
        fails.append(msg)


def main():
    # ---- 1. object integrity
    found = sorted(os.listdir('object'))
    ok(found == sorted(EXPECT), 'object/ holds exactly the expected files (%s)' % ', '.join(found))
    for name in sorted(EXPECT):
        p = os.path.join('object', name)
        if not os.path.isfile(p):
            ok(False, 'object/%s is missing' % name)
            continue
        got = hashlib.sha256(open(p, 'rb').read()).hexdigest()
        ok(got == EXPECT[name], 'object/%s sha256 matches (%s)' % (name, got[:16]))
    if fails:
        # One changed byte in object/ lands here. kit/SUBMIT.md defines the terminal line as PASS or FAIL, so
        # say FAIL last and nothing after it.
        print('\nobject/ failed its integrity check, so the claimed numbers cannot be trusted; stopping here.')
        print('%d check(s) failed:' % len(fails))
        for f in fails:
            print('  - ' + f)
        print('FAIL')
        return 1

    # ---- 2. the scored set
    with open(os.path.join('object', 'per_position_bits.csv'), newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    ok(len(rows) == N_SCORED, '%d scored positions (bank: %d)' % (len(rows), N_SCORED))
    ok(all(int(r['pos']) >= 2 for r in rows), 'every scored position has at least 2 earlier codas in its stream')
    folds = {}
    with open(os.path.join('object', 'folds.csv'), newline='', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            folds[r['REC']] = int(r['fold'])
    ok(len(set(folds.values())) == N_FOLDS, '%d folds in folds.csv, each held out once' % len(set(folds.values())))
    ok(all(folds.get(r['REC']) == int(r['fold']) for r in rows),
       'every position is scored in the fold its REC belongs to')
    summary = json.load(open(os.path.join('object', 'content_summary.json'), encoding='utf-8'))
    per_fold = {}
    for r in rows:
        per_fold[int(r['fold'])] = per_fold.get(int(r['fold']), 0) + 1
    ok(all(per_fold[int(k)] == v['n'] for k, v in summary['folds'].items()),
       'per-fold counts match content_summary.json (%s)' % ', '.join(str(per_fold[k]) for k in sorted(per_fold)))

    # ---- 3. losses are finite and positive
    bits = {m: [float(r['bits_' + m]) for r in rows] for m in MODELS}
    for m in MODELS:
        good = all(b == b and b not in (float('inf'), float('-inf')) and b > 0.0 for b in bits[m])
        ok(good, '%-5s per-position losses are all finite and strictly positive' % m)

    # ---- 4. pooled cross-entropies
    pooled = {m: sum(bits[m]) / len(rows) for m in MODELS}
    for m in MODELS:
        claimed = summary['pooled_bits'][m]
        ok(abs(pooled[m] - claimed) < 1e-9,
           '%-5s pooled %.6f bits, matches content_summary.json (%.6f)' % (m, pooled[m], claimed))

    # ---- 5. condition (1)
    g1 = pooled['R1'] - pooled['full']
    ok(g1 >= COND1_MIN, 'condition (1): R1 - full = %.6f bits, at least %.2f' % (g1, COND1_MIN))

    # ---- 6. condition (2): threshold and this checker's own paired REC bootstrap
    g2 = pooled['twin'] - pooled['full']
    ok(g2 >= COND2_MIN, 'condition (2a): twin - full = %.6f bits, at least %.2f' % (g2, COND2_MIN))
    by_rec = {}
    for i, r in enumerate(rows):
        s, n = by_rec.setdefault(r['REC'], [0.0, 0])
        by_rec[r['REC']] = [s + (bits['twin'][i] - bits['full'][i]), n + 1]
    recs = sorted(by_rec)
    sums = [by_rec[k][0] for k in recs]
    ns = [by_rec[k][1] for k in recs]
    ok(len(recs) == 188, '%d REC groups own a scored position' % len(recs))
    rnd = random.Random(SEED)
    k = len(recs)
    stats = []
    rr = rnd.randrange
    for _ in range(RESAMPLES):
        tot = cnt = 0.0
        for _ in range(k):
            j = rr(k)
            tot += sums[j]
            cnt += ns[j]
        stats.append(tot / cnt)
    stats.sort()
    lo = stats[int(0.025 * RESAMPLES)]
    hi = stats[min(int(0.975 * RESAMPLES), RESAMPLES - 1)]
    ok(lo > 0.0, 'condition (2b): own-seed 95%% paired REC bootstrap [%.4f, %.4f] excludes 0' % (lo, hi))

    # ---- 7. the null test
    nt = os.path.join('how-we-built-it', 'null_test.md')
    if not os.path.isfile(nt):
        ok(False, 'how-we-built-it/null_test.md is missing')
    else:
        t = open(nt, encoding='utf-8').read()
        m_c = re.search(r'(?m)^controls:\s*([0-9]+)\s*$', t)
        m_b = re.search(r'(?m)^real_beats_all_controls:\s*(\w+)\s*$', t)
        m_r = re.search(r'(?m)^real:\s*([0-9.eE+-]+)\s*$', t)
        m_x = re.search(r'(?m)^best_control:\s*([0-9.eE+-]+)\s*$', t)
        ok(bool(m_c) and int(m_c.group(1)) >= 400,
           'null test ran %s controls (at least 400)' % (m_c.group(1) if m_c else '?'))
        ok(bool(m_b) and m_b.group(1).lower() in ('yes', 'true'), 'null test: the real gain beat every control')
        ok(bool(m_r) and abs(float(m_r.group(1)) - g2) < 1e-9,
           'null test real gain %s equals the twin gain recomputed here (%.9f)'
           % (m_r.group(1) if m_r else '?', g2))
        if m_x and m_r:
            ok(float(m_r.group(1)) > float(m_x.group(1)),
               'real %.6f is above the best control %.6f' % (float(m_r.group(1)), float(m_x.group(1))))

    print()
    if fails:
        print('%d check(s) failed:' % len(fails))
        for f in fails:
            print('  - ' + f)
        print('FAIL')
        return 1
    print('Both conditions of the bank criterion hold on the shipped object:')
    print('  full          %.6f bits per coda over %d scored codas' % (pooled['full'], len(rows)))
    print('  R1            %.6f   gain %.6f  (threshold %.2f)' % (pooled['R1'], g1, COND1_MIN))
    print('  cut twin      %.6f   gain %.6f  (threshold %.2f, 95%% [%.4f, %.4f])'
          % (pooled['twin'], g2, COND2_MIN, lo, hi))
    print('PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
