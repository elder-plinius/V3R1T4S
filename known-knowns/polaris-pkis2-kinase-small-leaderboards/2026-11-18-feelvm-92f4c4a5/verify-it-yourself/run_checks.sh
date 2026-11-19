#!/bin/sh
# Standalone verification of the polaris/pkis2-lok-slk-c-1 claim, from the package folder.
# The checker is pure standard-library Python; any Python 3.8+ works.
# The official inputs are pinned by sha256 in object/official_inputs.json; step 4 re-downloads
# them and compares hashes when online (informational; skipped silently when offline).
# The last output line is exactly PASS on success and exactly FAIL on any failure.
ok=1
cd "$(dirname "$0")/.."

PY=""
for c in python3 python python3.exe python.exe py py.exe; do
  if command -v "$c" >/dev/null 2>&1; then
    if "$c" -c "import sys; assert sys.version_info >= (3, 8)" >/dev/null 2>&1; then
      PY="$c"
      break
    fi
  fi
done
if [ -z "$PY" ]; then
  echo "FAIL: no python 3.8+ found on PATH"
  exit 1
fi

echo "== 1. object files present"
[ -s object/preds.csv ] || { echo "FAIL: object/preds.csv missing"; ok=0; }
[ -s object/official_inputs.json ] || { echo "FAIL: object/official_inputs.json missing"; ok=0; }
[ -s object/spec.json ] || { echo "FAIL: object/spec.json missing"; ok=0; }

echo "== 2. full verification (pure-stdlib checker: rows, metrics, margin, bootstrap, calibration)"
"$PY" verify-it-yourself/checker.py || ok=0

echo "== 3. corruption self-test (the checker must reject a reordered object)"
"$PY" - <<'PYEOF' || ok=0
import os, shutil, subprocess, sys, tempfile
d = tempfile.mkdtemp()
shutil.copytree("object", os.path.join(d, "object"))
shutil.copytree("verify-it-yourself", os.path.join(d, "verify-it-yourself"))
p = os.path.join(d, "object", "preds.csv")
lines = open(p).read().splitlines()
body = lines[1:]
body = [body[-1]] + body[:-1]          # rotate the prediction rows: order no longer official
open(p, "w").write("\n".join([lines[0]] + body) + "\n")
r = subprocess.run([sys.executable, os.path.join(d, "verify-it-yourself", "checker.py")],
                   capture_output=True, text=True)
out = (r.stdout + r.stderr).strip()
print("corrupted object ->", out.splitlines()[-1] if out else "(no output)")
if r.returncode == 0:
    print("detail: checker accepted a corrupted object")
    sys.exit(1)
print("corruption correctly rejected")
PYEOF

echo "== 4. online cross-check of the official input pins (informational; skipped when offline)"
"$PY" - <<'PYEOF' || true
import hashlib, json, urllib.request
try:
    inp = json.load(open("object/official_inputs.json"))
    for name, pin in inp["pins"].items():
        if "url" not in pin:
            continue
        req = urllib.request.Request(pin["url"],
                                      headers={"User-Agent": "V3R1T4S/1.0 (open research; github.com/elder-plinius/V3R1T4S)"})
        data = urllib.request.urlopen(req, timeout=60).read()
        got = hashlib.sha256(data).hexdigest()
        print("%s: sha256 %s (pinned %s) match=%s" % (name, got[:16] + "...", pin["sha256"][:16] + "...", got == pin["sha256"]))
        if got != pin["sha256"]:
            raise SystemExit("pin mismatch for " + name)
except Exception as e:
    print("online cross-check unavailable (%s) - offline mode" % type(e).__name__)
PYEOF

if [ "$ok" = 1 ]; then
  echo "PASS"
else
  echo "FAIL"
  exit 1
fi
