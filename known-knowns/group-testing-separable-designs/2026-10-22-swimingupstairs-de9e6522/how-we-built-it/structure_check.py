#!/usr/bin/env python3
"""Structure of a family (one 0/1 line per vector): weight distribution, column sums, and the largest number of
vectors vanishing on one coordinate (the size of the largest zero-padded n-1 subfamily it contains)."""
import sys, collections
L = open(sys.argv[1]).read().split()
n = len(L[0])
print('m=%d n=%d' % (len(L), n))
print('weights:', sorted(collections.Counter(l.count('1') for l in L).items()))
cs = [sum(l[k] == '1' for l in L) for k in range(n)]
print('column sums:', cs)
print('max vectors vanishing on 1 coordinate:', len(L) - min(cs))
