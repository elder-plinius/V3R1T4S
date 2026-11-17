"""PREREG N2: Bulow, Johnson and Shearer 2005 (JGR 110, E10003) Table 2 (new A1 events) against the candidate.
usage: bulow_check.py TEXT_DUMP  (text from pdftxt.py; spaces are lost, cells concatenated as YYYY DDD HH:MM)"""
import sys, re, datetime as dt
t = open(sys.argv[1], encoding='utf-8').read()
segs = []
for key in ('NewlyIdentifiedA1EventsYearDayaHour:Minute', 'Table2.(continued)YearDayaHour:Minute'):
    i = t.find(key)
    s = t[i + len(key):]
    s = s[:min(x for x in (s.find('Table3'), s.find('aAlldays')) if x >= 0)]
    segs.append(s)
ev = []
for s in segs:
    for y, d, hm in re.findall(r'(19[67]\d)(\d{1,3})(\d\d:\d\d)', s):
        ev.append(dt.datetime(int(y), 1, 1) + dt.timedelta(days=int(d) - 1, hours=int(hm[:2]), minutes=int(hm[3:])))
print('Table 2 entries parsed:', len(ev), '(paper: 123 new A1 events)')
e73 = [e for e in ev if e.year == 1973]
print('1973 entries:', len(e73), [e.strftime('%j %H:%M') for e in e73])
T = dt.datetime(1973, 11, 26, 7, 46, 28)
near = sorted(ev, key=lambda e: abs((e - T).total_seconds()))[:3]
print('nearest to onset 1973-11-26 07:46:28:', [(e.isoformat(), round((e - T).total_seconds() / 3600, 1)) for e in near])
hits = [e for e in ev if abs((e - T).total_seconds()) <= 360]
print('entries within +/- 6 min:', len(hits), '-> N2 pass:', not hits)
