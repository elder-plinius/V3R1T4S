#!/usr/bin/env python3
"""convert_seed.py ARCHIVE_FILE N W OUT.npy : read a `$BASE=16` code file from Brouwer's archive
(https://aeb.win.tue.nl/codes/cwc/...) and save its words as a sorted int64 array (np.unique), the input format of
every search engine here.

Hex convention (as in the archive): one word per line, or several words packed on one line at a fixed width of
ceil(n/4) hex digits (files with a `$N=` header); lines starting with `$` or `#` are headers.  The integer value of
the hex string is the word; bit i of the integer is coordinate i (the rightmost hex digit holds coordinates 0..3).
All 28 seed files used for this release are in this format.  This is the hex branch of the loader that was used to
make the original seed arrays, so the output is identical to theirs.
"""
import re
import sys

import numpy as np


def load_hex(path, n):
    """Return the list of python ints of a `$BASE=16` archive file of length-n words."""
    raw = open(path, encoding="utf8", errors="replace").read()
    lines = [ln.strip() for ln in raw.splitlines()]
    if not any(l.upper().startswith("$BASE=16") for l in lines):
        raise ValueError(f"{path}: not a $BASE=16 file (other archive formats are not needed for these seeds)")
    words = []
    for l in lines:
        if not l or l.startswith("#") or l.startswith("$"):
            continue
        if not re.fullmatch(r"[0-9a-fA-F]+", l):
            raise ValueError(f"bad hex line: {l!r}")
        width = (n + 3) // 4
        chunks = [l] if len(l) <= width else [l[i:i + width] for i in range(0, len(l), width)]
        if len(l) > width and len(l) % width:
            raise ValueError(f"packed hex line length {len(l)} not a multiple of word width {width}")
        for c in chunks:
            v = int(c, 16)
            if v >> n:
                raise ValueError(f"hex word {c} has a 1 beyond coordinate n-1 (n={n})")
            words.append(v)
    return words


def main():
    if len(sys.argv) != 5:
        sys.exit(__doc__)
    f, n, w, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    ws = np.unique(np.array(load_hex(f, n), dtype=np.int64))
    assert all(bin(int(x)).count("1") == w for x in ws), "weight mismatch"
    np.save(out, ws)
    print(out, len(ws), "hex")


if __name__ == "__main__":
    main()
