"""Standalone checker written from the definition (standard library only).

Definition (JARVIS-Leaderboard, *_forces tasks): MAE of force components, flattened, over the benchmark json 'test' ids, eV/A.
Checks: object hashes, prediction ids/lengths vs the benchmark json, the MAE, the claim margin, and that the training-id list
used is exactly the benchmark 'train' ids (disjoint from 'test'). Prints PASS only if everything holds; exits non-zero otherwise."""
import csv, hashlib, io, json, os, sys, zipfile
here = os.path.dirname(os.path.abspath(__file__)); pkg = os.path.dirname(here)
src = json.load(open(os.path.join(here, 'sources.json')))
fails = []
def check(cond, msg):
    print(('ok   ' if cond else 'FAIL ') + msg)
    if not cond: fails.append(msg)
# 1. object files unchanged
for line in open(os.path.join(here, 'expected_hashes.txt')):
    h, p = line.split()
    full = os.path.join(pkg, p)
    check(os.path.isfile(full) and hashlib.sha256(open(full, 'rb').read()).hexdigest() == h, 'sha256 ' + p)
# 2. benchmark json
zpath = os.path.join(here, '_cache', 'benchmark.json.zip')
bench = json.load(zipfile.ZipFile(zpath).open(src['benchmark_member']))
check(hashlib.sha256(open(zpath, 'rb').read()).hexdigest() == src['inputs'][0]['sha256'], 'benchmark json sha256')
test = {k: [float(x) for x in v.split(';')] for k, v in bench['test'].items()}
# 3. predictions
rows = list(csv.reader(io.StringIO(open(os.path.join(pkg, src['predictions']), encoding='utf8').read())))
check(rows[0] == ['id', 'prediction'], 'csv header')
pred = {r[0]: [float(x) for x in r[1].split(';')] for r in rows[1:]}
check(set(pred) == set(test), 'prediction ids == official test ids (%d)' % len(test))
check(all(len(pred[k]) == len(test[k]) for k in test), 'every prediction has the right number of components')
err = [abs(a - b) for k in test for a, b in zip(pred[k], test[k])]
mae = sum(err) / len(err)
print('components %d  force MAE %.17g eV/A' % (len(err), mae))
index = list(csv.DictReader(open(os.path.join(pkg, 'INDEX.csv'))))[0]
check(abs(mae - float(index['value'])) < 1e-12, 'MAE equals INDEX.csv value %s' % index['value'])
tv = float(index['table_value'])
check(mae <= 0.95 * tv, 'MAE %.6f <= 0.95 * listed best %.17g (= %.6f): improvement %.1f%%' % (mae, tv, 0.95 * tv, 100 * (1 - mae / tv)))
# 4. training ids
tr = open(os.path.join(pkg, 'how-we-built-it', 'train_ids.txt')).read().split()
check(tr == list(bench['train']), 'training ids used == benchmark train ids (%d)' % len(tr))
check(not (set(tr) & set(test)), 'no test id in the training list')
print('PASS' if not fails else 'FAIL')
sys.exit(1 if fails else 0)
