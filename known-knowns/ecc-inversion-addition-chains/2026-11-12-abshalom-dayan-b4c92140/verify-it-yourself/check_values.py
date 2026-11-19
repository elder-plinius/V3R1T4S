#!/usr/bin/env python3
"""Replay a published chain given as a list of values, one per line (the format of the files on
additionchains.com). Standard library only.  usage: python3 check_values.py FILE
Checks: first value 1; every later value is the sum of two earlier values; reports the length
(number of values minus one), the number of doublings of an earlier value, and
whether the last value is n - 2 for the secp256k1 group order n."""
import sys
N = int("fffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141", 16)
v = [int(x) for x in open(sys.argv[1]).read().split()]
ok = v[0] == 1
seen = {1}
dbl = 0
for t in range(1, len(v)):
    x = v[t]
    if not any((x - a) in seen for a in v[:t]):
        ok = False
        print("value %d at line %d is not a sum of two earlier values" % (x, t + 1))
    if x % 2 == 0 and x // 2 in seen:
        dbl += 1
    seen.add(x)
print("values %d, length %d, steps that can be doublings %d, distinct %s" % (len(v), len(v) - 1, dbl, len(seen) == len(v)))
print("all steps valid: %s" % ok)
print("ends at target n-2: %s" % (v[-1] == N - 2))
