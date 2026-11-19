"""Standalone checker for partial win p4 of bank target sperm-whale-next-coda-beyond-first-order.
Python 3 standard library only.

Run from the package folder:  sh verify-it-yourself/run_checks.sh

Partial win p4, pooled over the 5 held-out REC folds of the pinned sperm-whale-dialogues.csv: predicting whether
each scored coda carries the same whale label as the coda before it, the model's cross-entropy must be at least
0.05 bits per position BELOW a smoothed first-order same-or-switch reference, and the 95% interval of a paired
bootstrap over REC groups for that gain must exclude 0.

What this checker does NOT do: it does not refit the model. Refitting needs the source data and scipy and is
covered by RUN_IT_YOURSELF.md and by the run's REPRODUCE panellist, who refit everything independently. This
checker starts from the shipped per-position *probabilities* - not from losses - so it also verifies the step from
probability to log-loss, then recomputes every pooled number and runs the bootstrap itself under its own seed.

Checks:
 1. every file in object/ has the sha256 recorded below, so a corrupted copy fails;
 2. the scored set is the bank's: 3,418 positions, each with at least 2 earlier codas in its REC stream, 5 folds
    each held out once, fold membership equal to object/folds.csv, per-fold counts equal to p4_summary.json;
 3. every shipped probability lies strictly inside (0, 1) and every label is 0 or 1;
 4. the pooled cross-entropies recomputed from those probabilities equal p4_summary.json, for the reference, the
    model and the switch-pattern-only diagnostic;
 5. p4's threshold: reference minus model is at least 0.05 bits;
 6. p4's interval condition: this checker's own 10,000-resample paired bootstrap over REC groups (its own seed,
    not the claim's) has a 95% interval for the gain that excludes 0;
 7. the switch-pattern-only diagnostic is reported at the value the claim discloses, which is below the gain of
    the draft PR that cleared this cell first - see README.md, "Compared to";
 8. the null test in how-we-built-it/null_test.md reports at least 400 controls, says the real gain beat all of
    them, and its stated real gain equals the gain recomputed here.
Last line: PASS or FAIL.
"""
import csv
import hashlib
import json
import math
import os
import random
import re
import sys

EXPECT = {
    'folds.csv': '675bd6cbd2250d2eaf24fe560ee22e4889a683876fe4d070ad97d117a8519e82',
    'p4_per_position.csv': 'b2c1a3541708b20742174cb3ccf9f68a77c23ce0c77bc4b7f21cae66cb0bdad6',
    'p4_summary.json': '129919405109aa4de43e90aafbeeac5c9af6b254213a8db528afba53e3bee57a',
    'run_output.txt': '002032eae0fdf89fa05565af0958f094be9defe6b2e148a9baa7c8381eaebbd4',
}
N_SCORED = 3418
N_FOLDS = 5
N_RECS = 188
P4_MIN = 0.05
RESAMPLES = 10000
SEED = 20261119          # this checker's own seed, deliberately not the claim's
COLS = [('ref_bits', 'p_same_ref'), ('model_bits', 'p_same_model'), ('pattern_bits', 'p_same_pattern')]

fails = []


def ok(cond, msg):
    print(('ok   ' if cond else 'FAIL ') + msg)
    if not cond:
        fails.append(msg)


def loss(p, y):
    """Binary cross-entropy in bits of a single prediction."""
    return -math.log(p if y == 1 else 1.0 - p, 2)


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
        # say FAIL last and print nothing after it.
        print('\nobject/ failed its integrity check, so the claimed numbers cannot be trusted; stopping here.')
        print('%d check(s) failed:' % len(fails))
        for f in fails:
            print('  - ' + f)
        print('FAIL')
        return 1

    # ---- 2. the scored set
    with open(os.path.join('object', 'p4_per_position.csv'), newline='', encoding='utf-8') as f:
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
    summary = json.load(open(os.path.join('object', 'p4_summary.json'), encoding='utf-8'))
    per_fold = {}
    for r in rows:
        per_fold[int(r['fold'])] = per_fold.get(int(r['fold']), 0) + 1
    ok(all(per_fold[int(k)] == v['n'] for k, v in summary['folds'].items()),
       'per-fold counts match p4_summary.json (%s)' % ', '.join(str(per_fold[k]) for k in sorted(per_fold)))

    # ---- 3. the shipped probabilities are usable probabilities
    ys = [int(r['y_same']) for r in rows]
    ok(set(ys) <= {0, 1}, 'every label is 0 or 1')
    for _, col in COLS:
        vals = [float(r[col]) for r in rows]
        ok(all(0.0 < v < 1.0 for v in vals), '%-16s all probabilities lie strictly inside (0, 1)' % col)
    ok(abs(sum(ys) / len(ys) - summary['pooled']['same_rate']) < 1e-12,
       'same-label rate %.6f matches p4_summary.json' % (sum(ys) / len(ys)))

    # ---- 4. pooled cross-entropies, recomputed from the probabilities
    pooled = {}
    bits = {}
    for key, col in COLS:
        bits[key] = [loss(float(r[col]), y) for r, y in zip(rows, ys)]
        pooled[key] = sum(bits[key]) / len(rows)
        claimed = summary['pooled'][key]
        ok(abs(pooled[key] - claimed) < 1e-9,
           '%-12s pooled %.6f bits, matches p4_summary.json (%.6f)' % (key, pooled[key], claimed))
    ok(summary['pooled']['n'] == len(rows), 'p4_summary.json n equals the number of scored positions')

    # ---- 5. p4's threshold
    gain = pooled['ref_bits'] - pooled['model_bits']
    ok(gain >= P4_MIN, 'p4 threshold: reference - model = %.6f bits, at least %.2f' % (gain, P4_MIN))

    # ---- 6. p4's interval condition, under this checker's own seed
    by_rec = {}
    for i, r in enumerate(rows):
        s, n = by_rec.get(r['REC'], (0.0, 0))
        by_rec[r['REC']] = (s + (bits['ref_bits'][i] - bits['model_bits'][i]), n + 1)
    recs = sorted(by_rec)
    ok(len(recs) == N_RECS, '%d REC groups own a scored position' % len(recs))
    sums = [by_rec[k][0] for k in recs]
    ns = [by_rec[k][1] for k in recs]
    rnd = random.Random(SEED)
    rr = rnd.randrange
    k = len(recs)
    stats = []
    for _ in range(RESAMPLES):
        tot = 0.0
        cnt = 0
        for _ in range(k):
            j = rr(k)
            tot += sums[j]
            cnt += ns[j]
        stats.append(tot / cnt)
    stats.sort()
    lo = stats[int(0.025 * RESAMPLES)]
    hi = stats[min(int(0.975 * RESAMPLES), RESAMPLES - 1)]
    ok(lo > 0.0, 'p4 interval: own-seed 95%% paired REC bootstrap [%.4f, %.4f] excludes 0' % (lo, hi))

    # ---- 7. the disclosed diagnostic
    gain_pattern = pooled['ref_bits'] - pooled['pattern_bits']
    claimed_pattern = summary['pooled']['gain_pattern_diag'][0]
    ok(abs(gain_pattern - claimed_pattern) < 1e-9,
       'switch-pattern-only diagnostic gain %.6f matches the disclosed %.6f' % (gain_pattern, claimed_pattern))
    ok(gain_pattern < gain,
       'the full model beats the switch-pattern-only diagnostic (%.6f vs %.6f), so the extra margin comes from '
       'the timing, overlap and speaker-share features' % (gain, gain_pattern))

    # ---- 8. the null test
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
        ok(bool(m_r) and abs(float(m_r.group(1)) - gain) < 1e-9,
           'null test real gain %s equals the gain recomputed here (%.9f)' % (m_r.group(1) if m_r else '?', gain))
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
    print('Partial win p4 holds on the shipped object:')
    print('  model         %.6f bits per position over %d scored positions' % (pooled['model_bits'], len(rows)))
    print('  reference     %.6f   gain %.6f  (threshold %.2f, own-seed 95%% [%.4f, %.4f])'
          % (pooled['ref_bits'], gain, P4_MIN, lo, hi))
    print('  pattern only  %.6f   gain %.6f  (diagnostic, disclosed, not the claim)'
          % (pooled['pattern_bits'], gain_pattern))
    print('PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
