#!/usr/bin/env python3
"""Step 1: sha256 of every file under object/ against verify-it-yourself/object.sha256 (sha256sum format, paths relative to the package)."""
import hashlib, os, sys
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
bad = 0; n = 0
for line in open(os.path.join(root, 'verify-it-yourself', 'object.sha256')):
    h, p = line.strip().split(None, 1); p = p.lstrip('*')
    got = hashlib.sha256(open(os.path.join(root, p), 'rb').read()).hexdigest(); n += 1
    if got != h: bad += 1; print('MISMATCH', p)
files = set()
for d, _, fs in os.walk(os.path.join(root, 'object')):
    for f in fs: files.add(os.path.relpath(os.path.join(d, f), root).replace(os.sep, '/'))
listed = {l.strip().split(None, 1)[1].lstrip('*') for l in open(os.path.join(root, 'verify-it-yourself', 'object.sha256'))}
extra = files - listed
if extra: bad += 1; print('UNLISTED', sorted(extra)[:5])
print('files hashed', n, 'bad', bad)
sys.exit(1 if bad else 0)
