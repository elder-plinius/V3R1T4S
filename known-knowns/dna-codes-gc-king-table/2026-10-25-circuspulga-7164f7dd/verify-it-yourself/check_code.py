#!/usr/bin/env python3
"""Standalone checker from the definition: A_4^GC(n,d,w) code = distinct words of length n over {A,C,G,T},
each with exactly w letters in {G,C}, pairwise Hamming distance >= d. Prints PASS if object/A4GC_15_11_7_M42.txt
is such a code for (15,11,7) with more than 34 words (the table value it is compared to), else FAIL."""
import itertools, sys
N, D, W, TABLE = 15, 11, 7, 34
try:
    words = [l.strip() for l in open("object/A4GC_15_11_7_M42.txt") if l.strip()]
except OSError:
    print("FAIL"); sys.exit(1)
ok = len(words) == len(set(words)) and all(len(x) == N and set(x) <= set("ACGT") and sum(c in "GC" for c in x) == W for x in words)
md = min(sum(a != b for a, b in zip(x, y)) for x, y in itertools.combinations(words, 2)) if len(words) > 1 else 0
print("size=%d distinct=%s alphabet_length_gc_ok=%s min_hamming=%d table=%d" % (len(words), len(set(words)) == len(words), ok, md, TABLE))
res = "PASS" if ok and md >= D and len(words) > TABLE else "FAIL"
print(res); sys.exit(0 if res == "PASS" else 1)
