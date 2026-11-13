"""Standalone p2 checker (Python standard library only), written from the bank definition of p2 and the
pre-registered readings R1-R3:
  R1  a catalogued event is recovered if a declustered detection with D >= theta has its onset (window start + 30 s)
      within +/- 300 s of the catalogued start;
  R2  denominator = catalogued events whose window has scanned data;
  R3  false-alarm rate = time-reversed-data detections with D >= theta per scanned day.
It checks the object files' sha256, recomputes recovery and the false-alarm rate from them, compares with
object/claimed.json, and requires recall >= 0.90. Last line: PASS or FAIL.
"""
import csv, hashlib, json, os, sys, datetime as dt

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
ok = True


def fail(msg):
    global ok
    ok = False
    print('mismatch:', msg)


for line in open(os.path.join(here, 'OBJECT_SHA256.txt')):
    h, name = line.split()
    p = os.path.join(root, 'object', name)
    if not os.path.isfile(p):
        fail('missing object/' + name)
        continue
    if hashlib.sha256(open(p, 'rb').read()).hexdigest() != h:
        fail('sha256 of object/' + name)

det = json.load(open(os.path.join(root, 'object', 'detector.json')))
cl = json.load(open(os.path.join(root, 'object', 'claimed.json')))
theta = det['theta']
NS = 10 ** 9


def iso_ns(s):
    t = dt.datetime.strptime(s.rstrip('Z'), '%Y-%m-%dT%H:%M:%S.%f')
    d = t - dt.datetime(1970, 1, 1)
    return (d.days * 86400 + d.seconds) * NS + d.microseconds * 1000


def rows(name):
    return list(csv.DictReader(open(os.path.join(root, 'object', name))))


fwd = [(int(r['window_start_ns_since_1970']), float(r['D'])) for r in rows('forward_detections_1971_ge_theta.csv')]
rev = [float(r['D']) for r in rows('reversed_detections_1971_ge_theta.csv')]
scanned = sum(float(r['scanned_fraction']) for r in rows('scanned_fraction_1971.csv'))
cov = {}
for r in rows('event_window_coverage_1971.csv'):
    cov.setdefault(r['catalogued_start_utc'], []).append(float(r['coverage']))
events = rows('p2_recovery_1971.csv')
n = len(events)
n_sc = 0
rec = 0
for e in events:
    tc = iso_ns(e['catalogued_start_utc'])
    sc = any(c > 0 for c in cov.get(e['catalogued_start_utc'], []))
    n_sc += sc
    hit = any(D >= theta and abs(t + 30 * NS - tc) <= 300 * NS for t, D in fwd)
    if sc and hit:
        rec += 1
    if (e['recovered'] == 'yes') != hit:
        fail('recovered flag of %s' % e['catalogued_start_utc'])
far_n = sum(1 for v in rev if v >= theta)
far = far_n / scanned
recall = rec / n_sc if n_sc else 0.0
print('events %d, scanned %d, recovered %d, recall %.4f' % (n, n_sc, rec, recall))
print('time-reversed detections >= theta %d over %.4f scanned day-equivalents = %.4f per day' % (far_n, scanned, far))
if n != cl['n_events'] or n_sc != cl['n_scanned'] or rec != cl['recovered']:
    fail('event counts differ from claimed.json')
if far_n != cl['reversed_detections_ge_theta'] or abs(scanned - cl['scanned_day_equivalents']) > 1e-3 \
        or abs(far - cl['false_alarm_rate_per_day']) > 1e-3:
    fail('false-alarm numbers differ from claimed.json')
if any(D < theta for t, D in fwd):
    fail('a listed forward detection is below theta')
if recall < cl['p2_bar']:
    fail('recall below the p2 bar')
print('PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
