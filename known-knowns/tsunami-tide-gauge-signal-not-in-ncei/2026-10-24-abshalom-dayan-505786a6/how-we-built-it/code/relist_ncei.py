"""Re-derive the LISTED flags of both maps against the NCEI events API pages saved on 2026-11-07
(how-we-built-it/ncei_2026-11-07/). Python 3 standard library only. Run from the package folder:

    python3 how-we-built-it/code/relist_ncei.py > how-we-built-it/ncei_2026-11-07/relist.txt

The rule is the one frozen in PREREG.md section 3 and implemented in attempts/completeness-map/code/summarize_map.py
(listed()): an NCEI tsunami event of any validity and any cause is a match when
  (a) its UTC calendar date (year, month, day; a missing month or day read as 1) differs from the calendar date of the
      ComCat origin (UTC) by at most 1 day, or it has no day and the same year and month as the origin, and
  (b) its epicentre is within 1000 km (haversine, R = 6371 km) of the ComCat epicentre, or it has no coordinates.
So the clock-time tolerance is up to 1 day on either side of the origin's calendar date: an event up to just under 48 h
from the origin can match. The script also prints every matched pair with no coordinates, no NCEI clock time, or a
clock-time gap above 24 h, and the listed counts under a strict variant (coordinates required, |gap| <= 24 h)."""
import csv, datetime as dt, glob, json, math, os

H = os.path.dirname(os.path.abspath(__file__)); PKG = os.path.dirname(os.path.dirname(H))
ev = []
for f in sorted(glob.glob(os.path.join(PKG, 'how-we-built-it', 'ncei_2026-11-07', 'events_2015_2026_p*.json'))):
    ev += json.load(open(f))['items']
print(f'NCEI events 2015-2026 in the saved pages: {len(ev)}')
UC = ('SIGNAL', 'NO_SIGNAL', 'SIGNAL_UNDECIDED')


def gc(a, b, c, d):
    a, b, c, d = map(math.radians, (a, b, c, d))
    x = math.sin((c - a) / 2) ** 2 + math.cos(a) * math.cos(c) * math.sin((d - b) / 2) ** 2
    return 6371.0 * 2 * math.asin(math.sqrt(min(1.0, max(0.0, x))))


def evtime(e):
    if e.get('day') is None or e.get('hour') is None:
        return None
    return dt.datetime(e['year'], e['month'], e['day'], e['hour'], e.get('minute') or 0, int(e.get('second') or 0))


def matches(t, lat, lon):
    out = []
    for e in ev:
        d = dt.date(e['year'], e.get('month') or 1, e.get('day') or 1)
        if not (abs((d - t.date()).days) <= 1 or (e.get('day') is None and e['year'] == t.year and e.get('month') == t.month)):
            continue
        if e.get('latitude') is None or e.get('longitude') is None:
            out.append((e, None))
        else:
            k = gc(lat, lon, e['latitude'], e['longitude'])
            if k <= 1000:
                out.append((e, k))
    return out


for path in ('object/map.csv', 'sensitivity-v5/map.csv'):
    rows = list(csv.DictReader(open(os.path.join(PKG, path))))
    print(f'\n== {path}')
    changes, odd, strict = [], [], {}
    for r in rows:
        t = dt.datetime.strptime(r['time'][:19], '%Y-%m-%dT%H:%M:%S')
        L = matches(t, float(r['lat']), float(r['lon']))
        ids = ';'.join(str(e['id']) for e, _ in L)
        if str(bool(L)) != r['listed'] or ids != r['ncei_ids']:
            changes.append(f"  {r['id']}: map listed={r['listed']} ids={r['ncei_ids']} -> live listed={bool(L)} ids={ids}")
        ok = False
        for e, k in L:
            et = evtime(e); gap = None if et is None else (et - t).total_seconds() / 3600
            if k is not None and gap is not None and abs(gap) <= 24:
                ok = True
            if k is None or gap is None or abs(gap) > 24:
                odd.append(f"  {r['id']} ({r['real_cls']}) ~ NCEI {e['id']} {e.get('locationName')}, {e.get('country')}, validity "
                           f"{e.get('eventValidity')}, cause {e.get('causeCode')}: distance "
                           f"{'none (no coordinates)' if k is None else f'{k:.0f} km'}, NCEI minus ComCat "
                           f"{'n/a' if gap is None else f'{gap:+.1f} h'}")
        strict[r['id']] = ok
    print(f'LISTED flag or NCEI id changes against the map: {len(changes)}')
    print('\n'.join(changes))
    print('matched pairs with no coordinates, no NCEI clock time or a gap above 24 h:')
    print('\n'.join(odd))
    U = [r for r in rows if r['real_cls'] in UC]; S = [r for r in U if r['real_cls'] == 'SIGNAL']
    print(f"frozen rule: USABLE {len(U)}, listed {sum(r['listed'] == 'True' for r in U)}; SIGNAL {len(S)}, listed {sum(r['listed'] == 'True' for r in S)}")
    print(f"strict variant (coordinates required, |gap| <= 24 h): USABLE listed {sum(strict[r['id']] for r in U)}, SIGNAL listed "
          f"{sum(strict[r['id']] for r in S)}; USABLE quakes that lose the flag: {[r['id'] for r in U if r['listed'] == 'True' and not strict[r['id']]]}")
