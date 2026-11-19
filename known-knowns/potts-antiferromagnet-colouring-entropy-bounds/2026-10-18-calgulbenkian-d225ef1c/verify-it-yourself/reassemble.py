"""Reassemble a split object and verify it. usage: reassemble.py PARTS.txt OUTFILE
PARTS.txt: first line 'whole file NAME: N bytes, sha256 H'; then one line 'NAME.partNN SIZE SHA256' per part.
Part files are looked up beside PARTS.txt. Verifies every part and the whole file; standard library only."""
import sys, os, hashlib, re
pt, out = sys.argv[1], sys.argv[2]
d = os.path.dirname(os.path.abspath(pt))
lines = [l.strip() for l in open(pt) if l.strip() and not l.startswith('#')]
m = re.match(r'whole file (\S+): (\d+) bytes, sha256 ([0-9a-f]{64})$', lines[0])
name, size, whole = m.group(1), int(m.group(2)), m.group(3)
h = hashlib.sha256(); total = 0; ok = True
with open(out, 'wb') as f:
    for l in lines[1:]:
        pn, ps, psha = l.split()
        data = open(os.path.join(d, pn), 'rb').read()
        if len(data) != int(ps) or hashlib.sha256(data).hexdigest() != psha or len(data) > 900000:
            print('FAIL: part %s does not match PARTS.txt' % pn); ok = False
        f.write(data); h.update(data); total += len(data)
if total != size or h.hexdigest() != whole:
    print('FAIL: reassembled %s has %d bytes, sha256 %s; expected %d, %s' % (name, total, h.hexdigest(), size, whole)); ok = False
if ok: print('PASS: %d parts reassemble to %s (%d bytes), sha256 %s' % (len(lines) - 1, name, total, whole))
sys.exit(0 if ok else 1)
