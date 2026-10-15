#!/usr/bin/env python3
"""prodGen.py: lexicographic product O[J] of an outer instance O (order k) with an inner instance J (order r):
man (i,a) -> r*i+a ranks woman (j,b) -> r*j+b by O-rank of j first, then J-rank of b in man a's J-list; women symmetric
(woman (j,b) ranks man (i,a) by O-rank of i, then J-rank of a in woman b's J-list). With J = K2 (men a: [a,1-a],
women b: [1-b,b]) this is prodK2.py. Usage: prodGen.py OUTER.prefs INNER.prefs OUT.prefs"""
import sys
def load(p):
    rows = [list(map(int, l.split())) for l in open(p) if l.strip() and not l.startswith('#')]
    n = len(rows) // 2; return n, [[x - 1 for x in r] for r in rows[:n]], [[x - 1 for x in r] for r in rows[n:]]
k, om, ow = load(sys.argv[1]); r, jm, jw = load(sys.argv[2])
mp = [None] * (k * r); wp = [None] * (k * r)
for i in range(k):
    for a in range(r): mp[r * i + a] = [r * j + b for j in om[i] for b in jm[a]]
for j in range(k):
    for b in range(r): wp[r * j + b] = [r * i + a for i in ow[j] for a in jw[b]]
with open(sys.argv[3], 'w') as f:
    f.write('# O[J] lexicographic product: outer %s (order %d), inner %s (order %d); order %d\n' % (sys.argv[1], k, sys.argv[2], r, k * r))
    for row in mp + wp: f.write(' '.join(str(x + 1) for x in row) + '\n')
print('wrote', sys.argv[3], 'order', k * r)
