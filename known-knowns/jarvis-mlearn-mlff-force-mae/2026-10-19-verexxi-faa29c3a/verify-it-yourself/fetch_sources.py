"""Download the public inputs listed in sources.json (standard library only) and verify their sha256."""
import hashlib, json, os, sys, urllib.request
here = os.path.dirname(os.path.abspath(__file__))
cache = os.path.join(here, '_cache'); os.makedirs(cache, exist_ok=True)
src = json.load(open(os.path.join(here, 'sources.json')))
want = sys.argv[1:] or [s['name'] for s in src['inputs']]
bad = 0
for s in src['inputs']:
    if s['name'] not in want:
        continue
    path = os.path.join(cache, s['name'])
    if not os.path.isfile(path):
        req = urllib.request.Request(s['url'], headers={'User-Agent': 'V3R1T4S-verify (plain fetch)'})
        with urllib.request.urlopen(req, timeout=120) as r, open(path, 'wb') as f:
            f.write(r.read())
    h = hashlib.sha256(open(path, 'rb').read()).hexdigest()
    ok = h == s['sha256']
    print(('ok   ' if ok else 'BAD  ') + s['name'] + ' ' + h)
    bad += not ok
sys.exit(1 if bad else 0)
