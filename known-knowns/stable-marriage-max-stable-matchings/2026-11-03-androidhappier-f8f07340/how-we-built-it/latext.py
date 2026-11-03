# Latin instance of Z2^3 (order 8), extended to order 9 by appending a new man/woman pair:
# new man/woman go to the bottom of every old list; their own lists are random. Output prefs (1-based).
import random,sys
seed=int(sys.argv[1]); random.seed(seed); n=8; N=9
L=[[(m^w)+1 for w in range(n)] for m in range(n)]
mp=[[None]*n for _ in range(n)]; wp=[[None]*n for _ in range(n)]
for m in range(n):
    for w in range(n):
        mp[m][L[m][w]-1]=w; wp[w][n-L[m][w]]=m
mp=[r+[8] for r in mp]; wp=[r+[8] for r in wp]
mp.append(random.sample(range(N),N)); wp.append(random.sample(range(N),N))
for r in mp+wp: print(' '.join(str(x+1) for x in r))
