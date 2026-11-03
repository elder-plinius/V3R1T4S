# Independent count of unlabeled trees (A000055) via rooted-tree numbers A000081 and Otter's dissimilarity theorem.
from fractions import Fraction
N = 20
r = [0, 1]
for n in range(1, N):
    # r(n+1) = (1/n) * sum_{k=1..n} (sum_{d|k} d r(d)) r(n-k+1)
    s = 0
    for k in range(1, n+1):
        s += sum(d*r[d] for d in range(1, k+1) if k % d == 0) * r[n-k+1]
    r.append(s // n)
for n in (18, 19, 20):
    t = r[n] - sum(r[i]*r[n-i] for i in range(1, n)) // 2 if n % 2 else r[n] - (sum(r[i]*r[n-i] for i in range(1, n)) - r[n//2]) // 2 
    print(n, t)
