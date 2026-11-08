"""Standalone checker (Python standard library only) for partial win p3 of
massbalancemachine-norway-test-glaciers-rmse. Usage: python3 verify-it-yourself/check.py [object CSV]
Reads object/test_record_predictions_primary.csv (one row per test point record: rid, season, y = observed point
balance, yhat = sum of the re-implementation's monthly predictions), recomputes RMSE per season, and checks:
 1. record counts 1065 annual / 999 winter / 1028 summer (notebook 3.1.1 cell 36 Count values);
 2. each RMSE within 0.01 m w.e. of the published MBM value (1.00 / 0.59 / 0.70, same notebook cell);
 3. each RMSE equals the value the re-implementation printed (expected.json) to 1e-9;
 4. the file's sha256 equals the one the run recorded (expected.json, INDEX.csv), so it is the file that run
    produced, digit for digit. Last output line: PASS or FAIL."""
import csv, hashlib, json, math, os, sys

here = os.path.dirname(os.path.abspath(__file__))
path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, '..', 'object', 'test_record_predictions_primary.csv')
exp = json.load(open(os.path.join(here, 'expected.json')))
acc = {}
rids = set()
ok = True
try:
    with open(path, newline='') as f:
        for row in csv.DictReader(f):
            if row['rid'] in rids:
                print('duplicate record id', row['rid']); ok = False
            rids.add(row['rid'])
            e = float(row['yhat']) - float(row['y'])
            a = acc.setdefault(row['season'], [0.0, 0])
            a[0] += e * e
            a[1] += 1
except (OSError, KeyError, ValueError) as err:
    print('cannot read object:', err)
    print('FAIL')
    sys.exit(1)
for s in ('annual', 'winter', 'summer'):
    if s not in acc:
        print(s, 'missing'); ok = False; continue
    rmse = math.sqrt(acc[s][0] / acc[s][1]); n = acc[s][1]
    pub, pn = exp['published'][s]
    c1 = n == pn
    c2 = abs(rmse - pub) <= exp['tolerance']
    c3 = abs(rmse - exp['reimplementation_printed'][s]) <= 1e-9
    print(f'{s}: RMSE {rmse:.6f} n={n} | published {pub:.2f} n={pn} | |diff| {abs(rmse - pub):.4f} <= 0.01: {c2} '
          f'| count ok: {c1} | equals printed {exp["reimplementation_printed"][s]:.10f}: {c3}')
    ok = ok and c1 and c2 and c3
h = hashlib.sha256(open(path, 'rb').read()).hexdigest()
c4 = h == exp['object_sha256']
print(f'object sha256 {h} equals the recorded {exp["object_sha256"]}: {c4}')
ok = ok and c4
if set(acc) - {'annual', 'winter', 'summer'}:
    print('unexpected seasons', set(acc)); ok = False
print('PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
