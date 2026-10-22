#!/usr/bin/env python3
"""Reassemble object/cert_md_h3_54.txt from its numbered parts and check sha256 of each part and of the whole.
Usage: python3 -I assemble.py OUTFILE"""
import hashlib, os, sys
here = os.path.dirname(os.path.abspath(__file__))
obj = os.path.join(os.path.dirname(here), 'object')
lines = [l.split() for l in open(os.path.join(obj, 'PARTS.sha256')) if l.strip()]
whole = [l for l in lines if l[1] == 'cert_md_h3_54.txt'][0][0]
parts = [l for l in lines if l[1].startswith('cert_md_h3_54.txt.part')]
data = b''
ok = True
for h, name in parts:
    b = open(os.path.join(obj, name), 'rb').read()
    good = hashlib.sha256(b).hexdigest() == h and len(b) <= 900000
    ok = ok and good
    print('%s part %s %d bytes' % ('PASS' if good else 'FAIL', name, len(b)))
    data += b
good = hashlib.sha256(data).hexdigest() == whole
print('%s whole certificate %d bytes sha256 %s' % ('PASS' if good else 'FAIL', len(data), whole))
if not (ok and good):
    sys.exit(1)
open(sys.argv[1], 'wb').write(data)
