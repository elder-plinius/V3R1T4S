"""Fetch the public inputs of Hervay's rhombicosidodecahedron proof at a pinned commit and verify them by sha256.

usage: python fetch_inputs.py DEST      (standard library only; needs network for the GitHub archive download)
Writes DEST/certificate/search.cert, DEST/covers/{local,exotic}/*.json, DEST/paper/appendices/b-zoom-covers.tex
only (the author's Rust and Python code in that archive is neither extracted nor read).
"""
import hashlib, io, os, sys, urllib.request, zipfile
COMMIT = "802a3ded09535c4a99cef1371ce0d0277c433fa8"
URL = "https://github.com/bence-hervay/nopert-rid/archive/%s.zip" % COMMIT
MAP = [("certificate/", "proof/results/full/"), ("covers/", "proof/data/"), ("paper/appendices/", "paper/appendices/")]
here = os.path.dirname(os.path.abspath(__file__))
dest = sys.argv[1]
want = {}
for line in open(os.path.join(here, "INPUTS.sha256"), encoding="utf-8"):
    line = line.strip()
    if line:
        h, p = line.split(None, 1)
        want[p.lstrip("*")] = h
req = urllib.request.Request(URL, headers={"User-Agent": "V3R1T4S-verify-it-yourself"})
data = urllib.request.urlopen(req, timeout=300).read()
z = zipfile.ZipFile(io.BytesIO(data))
prefix = "nopert-rid-%s/" % COMMIT
names = set(z.namelist())
for rel, h in sorted(want.items()):
    for a, b in MAP:
        if rel.startswith(a):
            src = prefix + b + rel[len(a):]
            break
    else:
        sys.exit("no mapping for " + rel)
    if src not in names:
        sys.exit("missing in archive: " + src)
    blob = z.read(src)
    if hashlib.sha256(blob).hexdigest() != h:
        sys.exit("sha256 mismatch for " + rel)
    out = os.path.join(dest, rel)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "wb") as f:
        f.write(blob)
print("fetched and verified %d input files from commit %s" % (len(want), COMMIT[:8]))
