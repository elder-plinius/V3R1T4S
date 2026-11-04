#!/bin/sh
# Verification for: OEIS A054759 a(15) = the exact integer in object/a15.txt.
# Run from the package folder:  sh verify-it-yourself/run_checks.sh
# The last output line is exactly PASS on success and exactly FAIL on any failure.
ok=1

echo "== 1. object files present"
[ -s object/a15.txt ] || { echo "FAIL: object/a15.txt missing"; ok=0; }
[ -s object/residues_run1.json ] || { echo "FAIL: residues_run1.json missing"; ok=0; }
[ -s object/residues_run2.json ] || { echo "FAIL: residues_run2.json missing"; ok=0; }

echo "== 2. full verification (CRT certificates, ladder evidence, growth checks)"
python3 verify-it-yourself/checker.py || ok=0

echo "== 3. corruption self-test (the checker must reject a broken object)"
python3 - <<'PY' || ok=0
import os, subprocess, sys, tempfile
src = open(os.path.join('object', 'a15.txt'), 'rb').read()
bad = bytearray(src)
# flip one hex digit of the claimed integer
i = next(i for i, c in enumerate(bad) if chr(c).isdigit())
bad[i] = ord('1') if bad[i] != ord('1') else ord('2')
d = tempfile.mkdtemp()
os.makedirs(os.path.join(d, 'object'))
os.makedirs(os.path.join(d, 'how-we-built-it'))
open(os.path.join(d, 'object', 'a15.txt'), 'wb').write(bytes(bad))
for f in ('residues_run1.json', 'residues_run2.json'):
    open(os.path.join(d, 'object', f), 'wb').write(open(os.path.join('object', f), 'rb').read())
for f in ('ladder.json', 'ladder2.json'):
    open(os.path.join(d, 'how-we-built-it', f), 'wb').write(open(os.path.join('how-we-built-it', f), 'rb').read())
os.makedirs(os.path.join(d, 'verify-it-yourself'))
open(os.path.join(d, 'verify-it-yourself', 'checker.py'), 'wb').write(
    open(os.path.join('verify-it-yourself', 'checker.py'), 'rb').read())
r = subprocess.run([sys.executable, os.path.join(d, 'verify-it-yourself', 'checker.py')],
                   capture_output=True, text=True)
out = (r.stdout + r.stderr).strip()
print("corrupted object ->", out.splitlines()[-1] if out else "(no output)")
if r.returncode == 0:
    print("detail: checker accepted a corrupted object")
    sys.exit(1)
print("corruption correctly rejected")
PY

echo "== 4. live OEIS cross-check (informational; skipped silently when offline)"
python3 - <<'PY' || true
import urllib.request
try:
    req = urllib.request.Request("https://oeis.org/A054759/b054759.txt",
                                 headers={"User-Agent": "V3R1T4S-research/1.0 (contact in repo README)"})
    t = urllib.request.urlopen(req, timeout=20).read().decode()
    rows = [l.split() for l in t.splitlines() if l and not l.startswith('#')]
    live = {int(n): v for n, v in rows}
    import json
    pub = json.loads('{"1":4,"2":18,"3":148,"4":2970,"5":143224,"6":16448400,"7":4484823396,"8":2901094068042,"9":4448410550095612,"10":16178049740086515288,"11":139402641051212392498528,"12":2849295959501939989625992464,"13":137950545200232788276834783781648,"14":15844635835975276495290739119895808472}')
    same = all(str(live.get(int(k))) == str(v) for k, v in pub.items())
    v = open('object/a15.txt').read().strip()
    print("live b-file: matches the extracted cells: %s; claimed a(15) still absent: %s"
          % (same and len(live) == 14, v not in t))
except Exception as e:
    print("live fetch unavailable (%s) - offline mode, embedded cells used" % type(e).__name__)
PY

if [ "$ok" = 1 ]; then
  echo "PASS"
else
  echo "FAIL"
  exit 1
fi
