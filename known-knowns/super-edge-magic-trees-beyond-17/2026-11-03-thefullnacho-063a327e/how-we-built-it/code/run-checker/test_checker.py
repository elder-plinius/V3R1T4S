import sys; sys.path.insert(0, sys.path[0])
from check_sem import check
# known positive: path P4 0-1-2-3 labels 1,3,2,4? sums 4,5,6 consecutive
print("pos P4", check(4, [(0,1),(1,2),(2,3)], [1,3,2,4]))
# known positive: star K1,3 centre 0 label 1, leaves 2,3,4 -> sums 3,4,5
print("pos star", check(4, [(0,1),(0,2),(0,3)], [1,2,3,4]))
# injected negative: swap two labels on P4 -> 1,2,3,4 sums 3,5,7
print("neg P4", check(4, [(0,1),(1,2),(2,3)], [1,2,3,4]))
# injected negative: label out of range / not bijection
print("neg range", check(4, [(0,1),(0,2),(0,3)], [0,2,3,4]))
# known non-SEM graph: cycle C4 (SEM cycles need odd length) -> exhaustive search must find nothing
import itertools
E=[(0,1),(1,2),(2,3),(3,0)]
print("C4 exhaustive SEM count", sum(check(4,E,list(p))[0] for p in itertools.permutations(range(1,5))))
