#!/usr/bin/env python3
"""Recount every posted witness square in a092237_2.txt and a307164_5.txt with both counters,
check Latin-ness, and compare against each list's own header bound. Prints a table.
"""
import re, sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from countA import count_intercalates, is_latin
from countB import count_by_transpositions

BASE = os.environ.get('DATA_DIR', 'data/')

def parse(fn):
    txt = open(BASE + fn).read()
    out = []
    for m in re.finditer(r'(?m)^n=(\d+), a\(\1\)(>=|=)(\d+)\s*$', txt):
        n = int(m.group(1)); bound = int(m.group(3)); ge = m.group(2) == '>='
        start = m.end()
        nxt = re.search(r'(?m)^n=\d+, a\(\d+\)', txt[start:])
        body = txt[start:start + (nxt.start() if nxt else len(txt))]
        sq = []; collecting = False
        for toks in [l.split() for l in body.splitlines()]:
            if len(toks) == n and all(t.isdigit() for t in toks):
                sq.append([int(t) for t in toks]); collecting = True
            elif collecting and sq:
                break
        if len(sq) == n:
            out.append((n, bound, ge, sq))
    return out

print(f"{'file':16s} {'n':>3s} {'header':>7s} {'A':>6s} {'B':>6s} {'latin':>6s} {'matches':>8s}")
issues = []
for fn in ('a092237_2.txt', 'a307164_5.txt'):
    for n, bound, ge, sq in parse(fn):
        a = count_intercalates(sq); b = count_by_transpositions(sq)
        lat = is_latin(sq)
        ok = (a == b) and lat and (a == bound if not ge else a >= bound)
        print(f"{fn:16s} {n:3d} {('>=' if ge else '=')+str(bound):>7s} {a:6d} {b:6d} {str(lat):>6s} {str(ok):>8s}")
        if not ok:
            issues.append((fn, n, bound, ge, a, b, lat))
print()
print("ISSUES:", len(issues))
for i in issues: print("  ", i)
