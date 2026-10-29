"""Fetch NCEI tide-gauge runup rows (typeMeasurementId=2) with travel times, per event, for earthquake-cause events 2005-2026.
One honest GET per page via code/fetch.sh; stops at the first 401/403/429/503 (no retries)."""
import json, glob, os, subprocess, collections, math
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(H)
rows = []
for f in sorted(glob.glob(os.path.join(R, 'data/ncei_tg/p0*.json'))):
    rows += json.load(open(f))['items']
ev = collections.defaultdict(int)
for r in rows:
    if r['year'] >= 2005 and r.get('sourceCauseCode') == 1:
        ev[r['tsunamiEventId']] += 1
os.makedirs(os.path.join(R, 'data/ncei_tg/ev'), exist_ok=True)
for e, n in sorted(ev.items()):
    for p in range(1, math.ceil(n / 200) + 1):
        fn = os.path.join(R, f'data/ncei_tg/ev/{e}_p{p}.json')
        if os.path.exists(fn) and os.path.getsize(fn) > 50:
            continue
        url = f'https://www.ngdc.noaa.gov/hazel/hazard-service/api/v1/tsunamis/runups?tsunamiEventId={e}&typeMeasurementId=2&itemsPerPage=200&page={p}'
        out = subprocess.run([os.path.join(H, 'fetch.sh'), url, fn], capture_output=True, text=True).stdout
        code = out.split()[0] if out else '000'
        if code in ('401', '403', '429', '503'):
            print('BLOCKED', code, url, flush=True); raise SystemExit(1)
        if code != '200':
            print('non-200', code, url, flush=True)
print('DONE', len(ev), 'events', flush=True)
