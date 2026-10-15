#!/usr/bin/env python3
"""cross_compare.py -- compare P(0,0,0) values for n = 1..30 across independent sources.
Sources: text files with lines "n num/den" (one per solver), and JSON files mapping "n" -> "num/den"
(a dict, or {"values": {...}}). Prints, per n, whether all sources agree, and a summary.
Usage: python3 -I cross_compare.py label1=path1 label2=path2 ...
"""
import sys, json
from fractions import Fraction

def load(path):
    out = {}
    if path.endswith(".json"):
        d = json.load(open(path))
        if "values" in d and isinstance(d["values"], dict):
            d = d["values"]
        for k, v in d.items():
            try:
                out[int(k)] = Fraction(v)
            except Exception:
                pass
    else:
        for line in open(path):
            p = line.split()
            if len(p) == 2 and '/' in p[1]:
                out[int(p[0])] = Fraction(p[1])
    return out

def main():
    srcs = []
    for arg in sys.argv[1:]:
        label, path = arg.split("=", 1)
        srcs.append((label, load(path)))
    ns = sorted(set().union(*[set(d) for _, d in srcs]))
    all_ok = True
    for n in ns:
        vals = [(l, d.get(n)) for l, d in srcs]
        present = [v for _, v in vals if v is not None]
        agree = all(v == present[0] for v in present)
        all_ok &= agree and len(present) == len(srcs)
        print("n=%2d  sources=%d/%d  agree=%s  %s" % (n, len(present), len(srcs), "yes" if agree else "NO",
              "" if agree else "  ".join("%s:%s" % (l, v) for l, v in vals)))
    print("ALL_AGREE_ALL_PRESENT" if all_ok else "DISAGREEMENT_OR_MISSING")

if __name__ == "__main__":
    main()
