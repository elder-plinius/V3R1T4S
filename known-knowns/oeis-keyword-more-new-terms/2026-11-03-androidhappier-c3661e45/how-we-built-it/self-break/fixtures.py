# self-break for A131449: (1) Lang's row-5 grouping by rooted-tree class (bars in data/a131449.txt):
# recompute class sizes in our sorted order; (2) negative fixtures: one entry per rooted class (row
# length A000081(n+1)), and dropping "increasing" (n! each); (3) whether any equal-value tie could
# change the flattened row (it cannot: equal values) -- print row-6 value groups.
from math import factorial, prod
from itertools import groupby
from collections import Counter
def dyck(n):
    out=[]
    def g(s,o,c):
        if o==n and c==n: out.append(s); return
        if o<n: g(s+"U",o+1,c)
        if c<o: g(s+"D",o,c+1)
    g("",0,0); return out
def tree(w):
    st=[[]]
    for ch in w:
        if ch=="U": st.append([])
        else: c=st.pop(); st[-1].append(c)
    return st[0]
def canon(t): return tuple(sorted(canon(c) for c in t))
def size(t): return 1+sum(size(c) for c in t)
def hookprod(t): return prod(size(c)*hookprod(c) for c in t)
DATA=[int(l.split()[1]) for l in open("preclaim_b131449.txt") if l[0].isdigit()]
for n in (5,6):
    items=[(factorial(n)//hookprod(tree(w)), canon(tree(w))) for w in dyck(n)]
    items.sort(key=lambda x:(-x[0],x[1]))
    groups=[len(list(g)) for _,g in groupby(items,key=lambda x:(x[0],x[1]))]
    print("row",n,"class-group sizes in sorted order:",groups)
    vals=sorted(Counter(v for v,_ in items).items(),reverse=True)
    print("row",n,"value multiplicities:",vals)
print("Lang row 5 bars: 1,4,3,3,2,1,3,2,4,3,2,2,2,1,1,2,2,2,1,1")
neg=[]
for n in range(6):
    cl={}
    for w in dyck(n): cl[canon(tree(w))]=factorial(n)//hookprod(tree(w))
    neg+=sorted(cl.values(),reverse=True)
print("negative (one per rooted class) first 12:",neg[:12],"DATA first 12:",DATA[:12],"differs" if neg!=DATA[:len(neg)] else "same")
neg2=[factorial(n) for n in range(6) for w in dyck(n)]
print("negative (n! each) first 12:",neg2[:12],"differs" if neg2!=DATA[:len(neg2)] else "same")
