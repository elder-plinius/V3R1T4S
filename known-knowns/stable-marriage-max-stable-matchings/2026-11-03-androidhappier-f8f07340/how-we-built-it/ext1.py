# extend an order-n prefs file to order n+1: new man/woman appended at the bottom of every old list, own lists random
import random,sys
random.seed(int(sys.argv[2])); rows=[list(map(int,l.split())) for l in open(sys.argv[1]) if l.strip() and not l.startswith('#')]
n=len(rows)//2; N=n+1
mp=[r+[N] for r in rows[:n]]+[random.sample(range(1,N+1),N)]
wp=[r+[N] for r in rows[n:]]+[random.sample(range(1,N+1),N)]
for r in mp+wp: print(' '.join(map(str,r)))
