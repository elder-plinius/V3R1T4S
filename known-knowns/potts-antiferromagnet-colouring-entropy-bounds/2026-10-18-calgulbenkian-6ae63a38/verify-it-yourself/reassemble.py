"""Reassemble a split, xz-compressed object and verify it. usage: reassemble.py PARTS.txt OUTFILE
PARTS.txt: line 1 'whole file NAME: N bytes, sha256 H' (the decompressed file); line 2 'xz file NAME.xz: N bytes, sha256 H'
(the parts joined); then one line 'NAME.xz.partNN SIZE SHA256' per part. Part files are looked up beside PARTS.txt.
Checks every part, the joined .xz and the decompressed file; decompresses with lzma. Standard library only."""
import sys, os, hashlib, re, lzma
pt, out = sys.argv[1], sys.argv[2]
d = os.path.dirname(os.path.abspath(pt))
lines = [l.strip() for l in open(pt) if l.strip() and not l.startswith('#')]
m = re.match(r'whole file (\S+): (\d+) bytes, sha256 ([0-9a-f]{64})$', lines[0])
name, size, whole = m.group(1), int(m.group(2)), m.group(3)
m = re.match(r'xz file (\S+): (\d+) bytes, sha256 ([0-9a-f]{64})$', lines[1])
xzname, xzsize, xzsha = m.group(1), int(m.group(2)), m.group(3)
h = hashlib.sha256(); total = 0; ok = True; chunks = []
for l in lines[2:]:
    pn, ps, psha = l.split()
    data = open(os.path.join(d, pn), 'rb').read()
    if len(data) != int(ps) or hashlib.sha256(data).hexdigest() != psha or len(data) > 900000:
        print('FAIL: part %s does not match PARTS.txt' % pn); ok = False
    chunks.append(data); h.update(data); total += len(data)
if total != xzsize or h.hexdigest() != xzsha:
    print('FAIL: joined %s has %d bytes, sha256 %s; expected %d, %s' % (xzname, total, h.hexdigest(), xzsize, xzsha)); ok = False
try:
    raw = lzma.decompress(b''.join(chunks))
except lzma.LZMAError as e:
    print('FAIL: xz decompression error: %s' % e); sys.exit(1)
with open(out, 'wb') as f:
    f.write(raw)
if len(raw) != size or hashlib.sha256(raw).hexdigest() != whole:
    print('FAIL: decompressed %s has %d bytes, sha256 %s; expected %d, %s' % (name, len(raw), hashlib.sha256(raw).hexdigest(), size, whole)); ok = False
if ok: print('PASS: %d xz parts join to %s (%d bytes) which decompresses to %s (%d bytes), sha256 %s' % (len(lines) - 2, xzname, total, name, len(raw), whole))
sys.exit(0 if ok else 1)
