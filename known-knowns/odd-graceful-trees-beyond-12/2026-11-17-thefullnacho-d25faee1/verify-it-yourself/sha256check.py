#!/usr/bin/env python3
"""Check sha256sum-format file against files under a root (and optional subpaths).
Usage: sha256check.py SUMS ROOT [SUBDIR ...]
If SUBDIR arguments are given, only entries whose path is in or under those
subdirectories are checked. Exit 0 if every selected entry matches.
"""
import hashlib, os, sys

def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def main(argv):
    if len(argv) < 3:
        print("usage: sha256check.py SUMS ROOT [SUBDIR ...]")
        return 2
    sums, root = argv[1], argv[2]
    filters = [os.path.normpath(s) for s in argv[3:]]
    ok = bad = missing = skipped = 0
    with open(sums) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            hexd, name = line.split(None, 1)
            name = os.path.normpath(name.lstrip("*").lstrip("./"))
            if filters and not any(name == d or name.startswith(d + os.sep) for d in filters):
                skipped += 1
                continue
            path = os.path.join(root, name)
            if not os.path.isfile(path):
                print("MISSING", name)
                missing += 1
                continue
            got = digest(path)
            if got != hexd:
                print("MISMATCH", name)
                bad += 1
            else:
                ok += 1
    print("checked=%d ok=%d mismatch=%d missing=%d skipped=%d" % (ok + bad + missing, ok, bad, missing, skipped))
    if bad or missing:
        print("FAIL")
        return 1
    print("PASS")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
