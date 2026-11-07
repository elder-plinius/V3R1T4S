#!/usr/bin/env python3
"""Check files against a sha256sum-format list. Standard library only.
Usage: python3 sha256check.py SUMS_FILE BASE_DIR [PREFIX]   (only entries whose path starts with PREFIX)
Prints one line per file and a last line PASS or FAIL."""
import hashlib, os, re, sys
sums, base = sys.argv[1], sys.argv[2]
prefix = sys.argv[3] if len(sys.argv) > 3 else ""
bad = n = 0
for line in open(sums):
    m = re.match(r"^([0-9a-f]{64})\s+\*?(.+)$", line.strip())
    if not m or not m.group(2).lstrip("./").startswith(prefix): continue
    n += 1
    p = os.path.join(base, m.group(2))
    h = hashlib.sha256()
    try:
        with open(p, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""): h.update(chunk)
        ok = h.hexdigest() == m.group(1)
    except OSError:
        ok = False
    bad += not ok
    print("%s %s" % ("ok  " if ok else "BAD ", m.group(2)))
print("PASS" if n and not bad else "FAIL")
sys.exit(0 if n and not bad else 1)
