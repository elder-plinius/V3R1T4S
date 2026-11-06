"""Check the sha256 of the object files that are not certificate parts. usage: check_object_files.py LISTFILE ROOT
(the parts are checked by reassemble.py against object/PARTS.txt). Standard library only."""
import sys, os, hashlib
lst, root = sys.argv[1], sys.argv[2]
bad = 0; n = 0
for line in open(lst):
    if not line.strip():
        continue
    h, name = line.split(None, 1)
    name = name.strip()
    p = os.path.join(root, name)
    ok = os.path.isfile(p) and hashlib.sha256(open(p, 'rb').read()).hexdigest() == h
    n += 1
    if not ok:
        bad += 1
        print('FAIL: %s does not match its recorded sha256' % name)
print('PASS: %d object files match their recorded sha256' % n if bad == 0 else 'object file check FAILED')
sys.exit(1 if bad else 0)
