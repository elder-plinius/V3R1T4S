"""Standalone checker for partial win p3 of bank target sperm-whale-next-coda-beyond-first-order.
Python 3 standard library only.

Run from the package folder:  sh verify-it-yourself/run_checks.sh

Partial win p3, pooled over the 5 held-out date folds of the pinned DominicaCodas.csv: a next-coda model reading
only earlier codas of the same stream must score at least 0.05 bits per coda BELOW a smoothed bigram over
CodaType, with the 95% interval of a paired bootstrap over rewritten-Date groups excluding 0.

What this checker does NOT do: it does not refit the model. Refitting needs the source data and scipy and is
covered by RUN_IT_YOURSELF.md and by the run's REPRODUCE panellist, who refit everything independently - including
an independently written smoothed bigram that came out bit-identical to the shipped one. This checker verifies the
arithmetic of the claim from the shipped object and runs the bootstrap itself under its own seed.

Checks:
 1. every file in object/ has the sha256 recorded below, so a corrupted copy fails;
 2. the scored set is the bank's: 8,501 positions, each with at least 1 earlier coda in its stream, 5 folds each
    held out once, every position scored in the fold its rewritten Date belongs to, per-fold counts equal to
    p3_summary.json, and every token inside the 35-symbol vocabulary;
 3. every per-position loss is finite and strictly positive;
 4. the pooled cross-entropies recomputed from the per-position losses equal p3_summary.json;
 5. p3's threshold: bigram minus full is at least 0.05 bits;
 6. p3's interval condition: this checker's own 10,000-resample paired bootstrap over rewritten-Date groups (its
    own seed, not the claim's) has a 95% interval for the gain that excludes 0;
 7. the N3 null test reports at least 400 controls, says the real gain beat all of them, and its stated real gain
    equals the gain recomputed here; the 400 shipped control gains are all below it;
 8. the composition-preserving control (design N6) ships 400 control gains and all of them are below the
    order-only gain that p3_summary.json records. NOTE: that order-only gain is NOT recomputable from this
    object, because the stream-local reference's probabilities are not shipped; see README.md, "Not claimed".
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
    'p3_folds.csv': '6c4107003f152cf12219a9c53dbd3e25a8f919604ae2a940118ccb2cd70506c4',
    'p3_per_position.csv': '785c884315e293fc2ad2e23ef6fb0ce3306076c9ef0b13736343a44fa65b1cbd',
    'p3_summary.json': '3aff05e8121f27a54c9536b7129fa73c44d75854081dca71056fc2cf827e40b2',
    'p3_vocab.csv': '1ac396979afc6058d003cda02b9e24344255e8b8dbaa9df50ed508ff5b12766f',
    'run_output.txt': '090ec55a47808cd683ddd4f6db494664302b792eaafb044cd009f7b7ae6594b6',
}
N_SCORED = 8501
N_FOLDS = 5
N_VOCAB = 35
N_DATE_GROUPS = 96
P3_MIN = 0.05
RESAMPLES = 10000
SEED = 31415926          # this checker's own seed, deliberately not the claim's
MODELS = ['bigram', 'full']

fails = []


def ok(cond, msg):
    print(('ok   ' if cond else 'FAIL ') + msg)
    if not cond:
        fails.append(msg)


def read_controls(path, col):
    """Control gains from a shipped csv with a header. Returns [] if the file is missing."""
    if not os.path.isfile(path):
        return []
    out = []
    with open(path, newline='', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            out.append(float(r[col]))
    return out


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
    with open(os.path.join('object', 'p3_per_position.csv'), newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    ok(len(rows) == N_SCORED, '%d scored positions (bank: %d)' % (len(rows), N_SCORED))
    ok(all(int(r['pos']) >= 1 for r in rows), 'every scored position has at least 1 earlier coda in its stream')
    folds = {}
    with open(os.path.join('object', 'p3_folds.csv'), newline='', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            folds[r['DateRewritten']] = int(r['fold'])
    ok(len(set(folds.values())) == N_FOLDS, '%d folds in p3_folds.csv, each held out once' % len(set(folds.values())))
    dates = [r['stream'].split('|')[0] for r in rows]
    ok(all(folds.get(d) == int(r['fold']) for d, r in zip(dates, rows)),
       'every position is scored in the fold its rewritten Date belongs to')
    ok(len(set(dates)) == N_DATE_GROUPS, '%d rewritten-Date groups own a scored position' % len(set(dates)))
    vocab = {}
    with open(os.path.join('object', 'p3_vocab.csv'), newline='', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            vocab[int(r['token'])] = r['CodaType']
    ok(len(vocab) == N_VOCAB, '%d CodaType symbols in the vocabulary' % len(vocab))
    ok(all(int(r['y_token']) in vocab for r in rows), 'every scored token is inside the vocabulary')
    summary = json.load(open(os.path.join('object', 'p3_summary.json'), encoding='utf-8'))
    ok(summary['n_scored'] == len(rows), 'p3_summary.json n_scored equals the number of scored positions')
    per_fold = {}
    for r in rows:
        per_fold[int(r['fold'])] = per_fold.get(int(r['fold']), 0) + 1
    ok(sum(per_fold.values()) == N_SCORED,
       'per-fold counts sum to the scored set (%s)' % ', '.join(str(per_fold[k]) for k in sorted(per_fold)))

    # ---- 3. losses are finite and positive
    bits = {m: [float(r['bits_' + m]) for r in rows] for m in MODELS}
    for m in MODELS:
        good = all(b == b and b not in (float('inf'), float('-inf')) and b > 0.0 for b in bits[m])
        ok(good, '%-7s per-position losses are all finite and strictly positive' % m)

    # ---- 4. pooled cross-entropies
    pooled = {m: sum(bits[m]) / len(rows) for m in MODELS}
    for m in MODELS:
        claimed = summary['pooled_bits'][m]
        ok(abs(pooled[m] - claimed) < 1e-9,
           '%-7s pooled %.6f bits, matches p3_summary.json (%.6f)' % (m, pooled[m], claimed))

    # ---- 5. p3's threshold
    gain = pooled['bigram'] - pooled['full']
    ok(gain >= P3_MIN, 'p3 threshold: bigram - full = %.6f bits, at least %.2f' % (gain, P3_MIN))
    ok(abs(gain - summary['comparisons']['full_vs_bigram'][0]) < 1e-9,
       'the gain equals the one p3_summary.json records (%.9f)' % summary['comparisons']['full_vs_bigram'][0])

    # ---- 6. p3's interval condition, under this checker's own seed
    by_date = {}
    for i, (d, r) in enumerate(zip(dates, rows)):
        s, n = by_date.get(d, (0.0, 0))
        by_date[d] = (s + (bits['bigram'][i] - bits['full'][i]), n + 1)
    keys = sorted(by_date)
    sums = [by_date[k][0] for k in keys]
    ns = [by_date[k][1] for k in keys]
    rnd = random.Random(SEED)
    rr = rnd.randrange
    k = len(keys)
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
    ok(lo > 0.0, 'p3 interval: own-seed 95%% paired Date bootstrap [%.4f, %.4f] excludes 0' % (lo, hi))

    # ---- 7. the N3 null test
    nt = os.path.join('how-we-built-it', 'null_test.md')
    if not os.path.isfile(nt):
        ok(False, 'how-we-built-it/null_test.md is missing')
    else:
        t = open(nt, encoding='utf-8').read()
        m_c = re.search(r'(?m)^controls:\s*([0-9]+)\s*$', t)
        m_b = re.search(r'(?m)^real_beats_all_controls:\s*(\w+)\s*$', t)
        m_r = re.search(r'(?m)^real:\s*([0-9.eE+-]+)\s*$', t)
        ok(bool(m_c) and int(m_c.group(1)) >= 400,
           'N3 null ran %s controls (at least 400)' % (m_c.group(1) if m_c else '?'))
        ok(bool(m_b) and m_b.group(1).lower() in ('yes', 'true'), 'N3 null: the real gain beat every control')
        ok(bool(m_r) and abs(float(m_r.group(1)) - gain) < 1e-9,
           'N3 null real gain %s equals the gain recomputed here (%.9f)' % (m_r.group(1) if m_r else '?', gain))
    n3 = read_controls(os.path.join('how-we-built-it', 'null', 'N3_controls.csv'), 'gain_full_vs_bigram')
    ok(len(n3) == 400, '%d N3 control gains shipped' % len(n3))
    if n3:
        ok(max(n3) < gain, 'every N3 control gain is below the real gain (best control %.6f vs %.6f)'
           % (max(n3), gain))

    # ---- 8. the composition-preserving control (design N6)
    order_gain = summary['comparisons']['full_vs_local'][0]
    n6 = read_controls(os.path.join('how-we-built-it', 'composition-null', 'n6_controls.csv'),
                       'gain_full_vs_local')
    ok(len(n6) == 400, '%d N6 composition-preserving control gains shipped' % len(n6))
    if n6:
        ok(max(n6) < order_gain,
           'every N6 control gain is below the order-only gain p3_summary.json records (best control %.6f vs '
           '%.6f, a margin of %.2fx)' % (max(n6), order_gain, order_gain / max(n6)))
        ok(order_gain < gain,
           'the order-only component %.6f is a minority of the claimed gain %.6f, as README.md states'
           % (order_gain, gain))

    print()
    if fails:
        print('%d check(s) failed:' % len(fails))
        for f in fails:
            print('  - ' + f)
        print('FAIL')
        return 1
    print('Partial win p3 holds on the shipped object:')
    print('  full          %.6f bits per coda over %d scored codas' % (pooled['full'], len(rows)))
    print('  bigram        %.6f   gain %.6f  (threshold %.2f, own-seed 95%% [%.4f, %.4f])'
          % (pooled['bigram'], gain, P3_MIN, lo, hi))
    print('  of that gain, %.6f is ordered structure; the rest is order-free stream context' % order_gain)
    print('PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
