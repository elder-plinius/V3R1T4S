#!/usr/bin/env python3
"""prodK2.py: lexicographic product O[K2] of an outer instance O (order k, from a prefs file) with the order-2
Knuth instance K2 (men a: [a, 1-a]; women b: [1-b, b]; 2 stable matchings): order 2k.
Man (i,a) -> 2i+a ranks woman (j,b) -> 2j+b by O-rank of j first, then K2-rank of b; women symmetric.
(The constructor lens found this product gives 24992 at n = 14 from the order-7 85-instance.)
Usage: prodK2.py OUTER.prefs OUT.prefs"""
import sys
rows = [list(map(int, l.split())) for l in open(sys.argv[1]) if l.strip() and not l.startswith('#')]
k = len(rows) // 2
om = [[x - 1 for x in r] for r in rows[:k]]; ow = [[x - 1 for x in r] for r in rows[k:]]
mp = [None] * (2 * k); wp = [None] * (2 * k)
for i in range(k):
    for a in range(2):
        mp[2 * i + a] = [2 * j + b for j in om[i] for b in [a, 1 - a]]
for j in range(k):
    for b in range(2):
        wp[2 * j + b] = [2 * i + a for i in ow[j] for a in [1 - b, b]]
with open(sys.argv[2], 'w') as f:
    f.write('# O[K2] lexicographic product of %s (order %d) with the order-2 Knuth instance; order %d\n' % (sys.argv[1], k, 2 * k))
    for r in mp + wp: f.write(' '.join(str(x + 1) for x in r) + '\n')
print('wrote', sys.argv[2], 'order', 2 * k)
