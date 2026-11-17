"""Standalone p1 checker (Python standard library only). From object/: recompute the normalised cross-correlation of
the saved S14 data window with the saved A39 template on each channel (NCC = sum t (w - mean w) / sqrt(sum (w - mean
w)^2) with the template already zero-mean and unit-norm), require one channel >= 0.6, recompute the two-channel mean D
and require it above every one of the 401 null controls' full-span maxima, check the object files' sha256 and the
claimed values. Last line: PASS or FAIL.
"""
import csv, hashlib, json, math, os, sys

here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here); ok = True


def fail(m):
    global ok
    ok = False; print('mismatch:', m)


for line in open(os.path.join(here, 'OBJECT_SHA256.txt')):
    h, name = line.split(); p = os.path.join(root, 'object', name)
    if not os.path.isfile(p) or hashlib.sha256(open(p, 'rb').read()).hexdigest() != h:
        fail('sha256 of object/' + name)
cand = json.load(open(os.path.join(root, 'object', 'candidate.json')))
rows = list(csv.DictReader(open(os.path.join(root, 'object', 'window_and_template.csv'))))
cc = []
for ch in ('mh1', 'mh2'):
    t = [float(r['template_' + ch]) for r in rows]; w = [float(r['data_' + ch]) for r in rows]
    mw = sum(w) / len(w); wd = [x - mw for x in w]
    st = sum(t); nt = math.sqrt(sum(x * x for x in t))
    if abs(st) > 1e-6 or abs(nt - 1) > 1e-6:
        fail('template %s not zero-mean unit-norm' % ch)
    cc.append(sum(a * b for a, b in zip(t, wd)) / math.sqrt(sum(x * x for x in wd)))
D = sum(cc) / 2
ctrl = [float(r['full_span_max']) for r in csv.DictReader(open(os.path.join(root, 'object', 'null_full_span_maxima.csv')))]
print('NCC MH1 %.4f, MH2 %.4f, D %.4f; controls %d, best control %.4f' % (cc[0], cc[1], D, len(ctrl), max(ctrl)))
if abs(cc[0] - cand['ncc_mh1']) > 2e-4 or abs(cc[1] - cand['ncc_mh2']) > 2e-4 or abs(D - cand['detection_statistic_D']) > 2e-4:
    fail('recomputed NCC differs from candidate.json')
if max(cc) < 0.6:
    fail('no channel reaches CC 0.6')
if len(ctrl) < 401 or not all(D > c for c in ctrl):
    fail('D does not exceed every control')
if abs(max(ctrl) - max(cand['null_best_phase_randomised_full_span_max'], cand['null_c0_time_reversed_full_span_max'])) > 1e-6:
    fail('control maxima differ from candidate.json')
if any(abs(r[0]) <= 5 for r in cand['nearest_catalogue_rows_min']):
    fail('a catalogue row lies within 5 minutes')
print('PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
