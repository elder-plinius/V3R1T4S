"""Write SHA256SUMS for a package: sha256 of every file except SHA256SUMS itself, in
`sha256sum` format with relative paths. Usage: python -I make_sha256sums.py <package_dir>"""
import hashlib
import io
import os
import sys

pkg = os.path.abspath(sys.argv[1])
rows = []
for root, dirs, files in os.walk(pkg):
    dirs[:] = sorted(dirs)
    for f in sorted(files):
        p = os.path.join(root, f)
        rel = os.path.relpath(p, pkg).replace(os.sep, "/")
        if rel == "SHA256SUMS":
            continue
        with open(p, "rb") as fh:
            rows.append((rel, hashlib.sha256(fh.read()).hexdigest()))
rows.sort()
with io.open(os.path.join(pkg, "SHA256SUMS"), "w", encoding="utf-8", newline="\n") as fh:
    for rel, h in rows:
        fh.write("%s  %s\n" % (h, rel))
print("SHA256SUMS: %d files" % len(rows))
big = [(r, os.path.getsize(os.path.join(pkg, r))) for r, _ in rows
       if os.path.getsize(os.path.join(pkg, r)) > 1_000_000]
print("files over 1 MB:", big if big else "none")
print("package bytes:", sum(os.path.getsize(os.path.join(pkg, r)) for r, _ in rows))
