#!/bin/sh
# Verification for: Brainfuck constant 114514 in 41 instructions.
# Run from the package folder:  sh verify-it-yourself/run_checks.sh
# The last output line is exactly PASS on success and exactly FAIL on any failure.
ok=1

echo "== 1. object byte-exactness"
echo "bytes: $(wc -c < object/program.bf)"
if [ "$(wc -c < object/program.bf)" -ne 41 ]; then echo "FAIL: object is not 41 bytes"; ok=0; fi

echo "== 2. interpreter check + agreement with object/expected.txt"
python3 - <<'PY' || ok=0
import re, subprocess, sys
exp = open('object/expected.txt').read()
m = re.search(r'^expected: (.+)$', exp, re.M)
if not m:
    print("FAIL: expected.txt has no 'expected:' line"); sys.exit(1)
fields = dict(kv.split('=', 1) for kv in m.group(1).split())
r = subprocess.run([sys.executable, 'verify-it-yourself/checker.py', 'object/program.bf', '114514'],
                   capture_output=True, text=True)
print(r.stdout.strip())
if r.returncode != 0 or not r.stdout.startswith('PASS'):
    print("detail: checker rejected the object"); sys.exit(1)
got = dict(re.findall(r'(\w+)=(\d+)', r.stdout))
for k, v in (('LEN', 'len'), ('VALUE', 'value'), ('STEPS', 'steps'), ('MINCELL', 'mincell')):
    if fields.get(k) != got.get(v):
        print("detail: expected.txt says %s=%s but the checker gives %s" % (k, fields.get(k), got.get(v)))
        sys.exit(1)
print("checker output matches expected.txt on len/value/steps/mincell")
PY

echo "== 3. corruption self-test (the checker must reject a broken object)"
python3 - <<'PY' || ok=0
import subprocess, sys, os, tempfile
prog = open(os.path.join('object', 'program.bf'), 'rb').read()
bad = bytearray(prog)
bad[13] = ord('+') if bad[13] != ord('+') else ord('-')   # flip one instruction
d = tempfile.mkdtemp()
p = os.path.join(d, 'bad.bf')
open(p, 'wb').write(bytes(bad))
r = subprocess.run([sys.executable, os.path.join('verify-it-yourself', 'checker.py'), p, '114514'],
                   capture_output=True, text=True)
out = (r.stdout + r.stderr).strip()
print("corrupted object ->", out.splitlines()[0] if out else "(no output)")
if r.returncode == 0:
    print("detail: checker accepted a corrupted object")
    sys.exit(1)
print("corruption correctly rejected")
PY

echo "== 4. instruction count equals the claimed 41"
python3 -c "
p = open('object/program.bf', 'rb').read()
assert len(p) == 41 and all(chr(c) in '+-<>.,[]' for c in p)
print('instructions: 41')
" || ok=0

if [ "$ok" = 1 ]; then
  echo "PASS"
else
  echo "FAIL"
  exit 1
fi
