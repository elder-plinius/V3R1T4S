"""G3 (descriptive base rates) alone, with the code of glitch_gates_a38.py's G3 section unchanged, so the G3 numbers can
be regenerated from the source files without the waveforms. Needs numpy and pandas (the random times use numpy's
default_rng(20261113), as the gate code does).

G3: the fraction of catalogued levent events (T2 = A, N2 = 39; T2 = A, N2 = 201; all T2 = A; S14 operating
1971-02-05..1977-09-30) whose window [start - 60 s, start + 450 s] overlaps a catalogued S14 MH1/MH2 ACC-Spike interval
of the Liu, Xiao and Li (2025) catalogue, and the same for 20,000 uniform random times (seed 20261113).

usage: g3_base_rates.py LEVENT.csv SOURCE OUT.json
SOURCE is lunar_ACC-v1.0.1.zip (doi:10.5281/zenodo.15715187) or a folder holding S14_ACC-Spike_MH1_all.csv and
S14_ACC-Spike_MH2_all.csv; the script refuses files whose sha256 differs from the recorded values.
"""
import sys, json, csv, io, bisect, hashlib, zipfile, datetime as dt, os
import numpy as np
import pandas as pd

NS = 1_000_000_000
L = 450.0
SHA = {'MH1': '78e91b83ff3f80c51706b044786420dcd41dddfa359099ac1e1123503b6ac0a1',
       'MH2': '1219c0fa43fc26ff08950a217407d0b5b5c9daadcb56900565f8af08733bc9f9'}
LEV, SRC, OUT = sys.argv[1:4]


def T(s):
    return dt.datetime.strptime(s[:26], '%Y-%m-%d %H:%M:%S.%f' if '.' in s else '%Y-%m-%d %H:%M:%S')


def tns(d):
    return int((d - dt.datetime(1970, 1, 1)).total_seconds() * 1e9)


def source_text(ch):
    name = 'S14_ACC-Spike_%s_all.csv' % ch
    if SRC.lower().endswith('.zip'):
        z = zipfile.ZipFile(SRC)
        b = z.read([n for n in z.namelist() if n.endswith('/catalogs/' + name)][0])
    else:
        b = open(os.path.join(SRC, name), 'rb').read()
    if hashlib.sha256(b).hexdigest() != SHA[ch]:
        sys.exit('%s: sha256 %s, expected %s' % (name, hashlib.sha256(b).hexdigest(), SHA[ch]))
    return b.decode('utf-8')


acc = []
for ch in ('MH1', 'MH2'):
    for r in csv.DictReader(io.StringIO(source_text(ch), newline='')):
        acc.append((tns(T(r['Start time'])), tns(T(r['End time'])), ch, r['Mode'], r['Similarity'], r['Amplitude Range']))
acc.sort()
starts = np.array([a[0] for a in acc], dtype=np.int64)
ends = np.array([a[1] for a in acc], dtype=np.int64)
maxdur = int((ends - starts).max())


def overlapping(t0, t1):
    i0 = bisect.bisect_left(starts, t0 - maxdur); i1 = bisect.bisect_right(starts, t1)
    return [acc[i] for i in range(i0, i1) if acc[i][1] >= t0 and acc[i][0] <= t1]


# G3 section of glitch_gates_a38.py, unchanged
cat = pd.read_csv(LEV, dtype=str)


def cat_ns(y, jd, s):
    y = 1900 + int(y); jd = int(jd); s = str(s).zfill(4)
    return tns(dt.datetime(y, 1, 1) + dt.timedelta(days=jd - 1, hours=int(s[:2]), minutes=int(s[2:])))


s14_on = tns(dt.datetime(1971, 2, 5)); s14_off = tns(dt.datetime(1977, 9, 30))
g3 = {}
for lab, sel in (('A39', (cat['T2'] == 'A') & (cat['N2'].str.strip() == '39')),
                 ('A201', (cat['T2'] == 'A') & (cat['N2'].str.strip() == '201')),
                 ('all type A', cat['T2'] == 'A')):
    n = hit = 0
    for r in cat[sel].itertuples():
        try:
            t = cat_ns(r.Y, r.JD, r.S)
        except Exception:
            continue
        if not (s14_on <= t <= s14_off):
            continue
        n += 1
        if overlapping(t - 60 * NS, t + int(L * 1e9)):
            hit += 1
    g3[lab] = dict(events=n, with_spike=hit, fraction=round(hit / n, 4) if n else None)
rng = np.random.default_rng(20261113)
rt = rng.integers(s14_on, s14_off, 20000)
hit = sum(1 for t in rt if overlapping(int(t) - 60 * NS, int(t) + int(L * 1e9)))
g3['random times'] = dict(events=20000, with_spike=hit, fraction=round(hit / 20000, 4))
json.dump(dict(G3=g3), open(OUT, 'w', newline='\n'), indent=1)
print(json.dumps(dict(G3=g3), indent=1))
