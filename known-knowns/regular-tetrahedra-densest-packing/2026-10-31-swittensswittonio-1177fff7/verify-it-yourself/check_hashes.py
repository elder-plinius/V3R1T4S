"""Check sha256 of every file in object/ against verify-it-yourself/object.sha256 (stdlib only).
Exit 1 on any mismatch, missing or extra file."""
import hashlib, os, sys
pkg = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
want = {}
for line in open(os.path.join(pkg, 'verify-it-yourself', 'object.sha256'), encoding='utf-8'):
    if line.strip():
        h, name = line.split(None, 1); want[name.strip().lstrip('*')] = h
have = {}
for r, _, fs in os.walk(os.path.join(pkg, 'object')):
    for f in fs:
        p = os.path.join(r, f); rel = os.path.relpath(p, pkg).replace(os.sep, '/')
        have[rel] = hashlib.sha256(open(p, 'rb').read()).hexdigest()
bad = [n for n in sorted(set(want) | set(have)) if want.get(n) != have.get(n)]
for n in bad: print("MISMATCH", n)
print("object/ hashes: %d files, %d mismatches" % (len(have), len(bad)))
sys.exit(1 if bad else 0)
