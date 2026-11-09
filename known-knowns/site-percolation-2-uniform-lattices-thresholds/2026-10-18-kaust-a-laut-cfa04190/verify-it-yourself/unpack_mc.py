"""Unpack the Monte Carlo archives of a folder (object/mc or how-we-built-it/timeline-aligner/mc) into <dest>, as
mc/<dataset>/<file>, after checking every archive against ARCHIVES.sha256 and every unpacked file against
FILES.sha256. Python 3 standard library only.

usage: python verify-it-yourself/unpack_mc.py <folder with ARCHIVES.sha256> <dest>
  e.g. python verify-it-yourself/unpack_mc.py object/mc work/timeline-aligner
The last line printed is PASS or FAIL.
"""
import hashlib
import os
import sys
import tarfile


def sha(b):
    return hashlib.sha256(b).hexdigest()


def listing(path):
    return [line.split(None, 1) for line in open(path) if line.strip()]


def main():
    src, dest = sys.argv[1], sys.argv[2]
    want = {name.strip(): h for h, name in listing(os.path.join(src, "FILES.sha256"))}
    bad, done = [], 0
    for h, name in listing(os.path.join(src, "ARCHIVES.sha256")):
        name = name.strip()
        blob = open(os.path.join(src, name), "rb").read()
        if sha(blob) != h:
            bad.append(name)
            continue
        with tarfile.open(os.path.join(src, name), "r:xz") as t:
            for m in t.getmembers():
                parts = m.name.split("/")
                if not m.isfile() or len(parts) != 3 or parts[0] != "mc" or ".." in parts:
                    bad.append("%s: unexpected member %s" % (name, m.name))
                    continue
                data = t.extractfile(m).read()
                if want.get(parts[1] + "/" + parts[2]) != sha(data):
                    bad.append(m.name)
                    continue
                os.makedirs(os.path.join(dest, "mc", parts[1]), exist_ok=True)
                with open(os.path.join(dest, "mc", parts[1], parts[2]), "wb") as f:
                    f.write(data)
                done += 1
    missing = len(want) - done
    print("%d files unpacked into %s, %d expected, %d problems" % (done, os.path.join(dest, "mc"), len(want), len(bad)))
    for b in bad[:20]:
        print("  bad: " + b)
    print("PASS" if not bad and missing == 0 else "FAIL")
    sys.exit(0 if not bad and missing == 0 else 1)


if __name__ == "__main__":
    main()
