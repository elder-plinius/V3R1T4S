import itertools, sys
sys.path.insert(0, __file__.rsplit("/",1)[0])
from check_odd_graceful import check
# known positive: star K_{1,12} (13 vertices, q=12): centre 0, leaves 1,3,...,23
n=13; edges=[(0,i) for i in range(1,13)]; lab=[0]+list(range(1,24,2))
print("positive star K1,12:", check(n,edges,lab))
# known positive: path P13 (caterpillar), zigzag labeling 0,23,2,21,4,19,... gives diffs 23,21,...,1
lab=[]; lo,hi=0,23
for i in range(13):
    if i%2==0: lab.append(lo); lo+=2
    else: lab.append(hi); hi-=2
pe=[(i,i+1) for i in range(12)]
print("positive path P13:", check(13,pe,lab), lab)
# known negative 1: corrupt the star (one leaf gets an even difference)
bad=[0]+list(range(1,24,2)); bad[5]=10
print("negative corrupted star:", check(13,edges,bad))
# known negative 2: triangle C3 has an odd cycle, so no odd-graceful labeling exists; exhaust all injections
c3=[(0,1),(1,2),(0,2)]
found=[p for p in itertools.permutations(range(6),3) if check(3,c3,list(p))[0]]
print("negative C3 exhaustive: labelings found =", len(found))
