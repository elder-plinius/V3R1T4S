"""Descriptive survey of the nine S14 files of the Liu, Xiao and Li (2025) acceleration-glitch catalogue (Zenodo
15715187, archive lunar_ACC-v1.0.1.zip) around the A38 object: rows per file in 1971 days 36-365, intervals overlapping
the 450 s window [1971-05-13T18:39:33.735Z, +450 s], and the nearest interval starts relative to the onset (+30 s).
usage: survey_nine_files.py ARCHIVE.zip OUT.json   (reads the zip members directly; standard library only)"""
import sys, csv, io, json, zipfile, datetime as dt

ZIP, OUT = sys.argv[1:3]
WS = dt.datetime(1971, 5, 13, 18, 39, 33, 735000)
WE = WS + dt.timedelta(seconds=450)
ON = WS + dt.timedelta(seconds=30)
S0 = dt.datetime(1971, 1, 1) + dt.timedelta(days=35)       # 1971 day 36 00:00
S1 = dt.datetime(1971, 1, 1) + dt.timedelta(days=365)      # end of 1971 day 365


def T(s):
    s = s.strip()
    return dt.datetime.strptime(s[:26], '%Y-%m-%d %H:%M:%S.%f' if '.' in s else '%Y-%m-%d %H:%M:%S')


z = zipfile.ZipFile(ZIP)
res = {}
for kind in ('Spike', 'Step-Up', 'Step-Down'):
    for ch in ('MH1', 'MH2', 'MHZ'):
        name = 'S14_ACC-%s_%s_all.csv' % (kind, ch)
        mem = [n for n in z.namelist() if n.endswith('/catalogs/' + name)]
        assert len(mem) == 1, name
        rows = list(csv.DictReader(io.TextIOWrapper(z.open(mem[0]), encoding='utf-8', newline='')))
        span = ov = 0
        near = []
        for r in rows:
            a, b = T(r['Start time']), T(r['End time'])
            if S0 <= a < S1:
                span += 1
            if b >= WS and a <= WE:
                ov += 1
            near.append(((a - ON).total_seconds(), (b - ON).total_seconds()))
        near.sort(key=lambda x: abs(x[0]))
        res[name] = dict(rows=len(rows), rows_1971_days_36_365=span, overlapping_window=ov,
                         nearest_starts_s_from_onset=[round(x[0], 3) for x in near[:3]],
                         nearest_after=min((round(x[0], 3) for x in near if x[0] > 0), default=None),
                         nearest_before_end=max((round(x[1], 3) for x in near if x[1] < 0), default=None))
json.dump(res, open(OUT, 'w', newline='\n'), indent=1)
print(json.dumps(res, indent=1))
