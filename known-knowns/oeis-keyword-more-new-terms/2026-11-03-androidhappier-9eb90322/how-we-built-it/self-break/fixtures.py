# self-break for A155520: (1) flattened DATA check of both programs' rows 1..5; (2) negative fixture:
# count leaf-deletion SEQUENCES (which UD factor is removed, positions distinguished) instead of distinct
# tree chains; (3) %e check: UDUUDD and UUDDUD have 2 drawings, UUUDDD/UUDUDD/UDUDUD have 1.
import sys
from functools import lru_cache
from collections import Counter
DATA=[1,2,3,2,4,2,6,1,1,5,2,6,9,1,4,4,4,2,1,2,2]
def rows(path):
    flat=[]
    for l in open(path):
        n=int(l.split()[0])
        if n<=5: flat+= [int(x) for x in l.split("row:")[1].split(",")]
    return flat
for p in sys.argv[1:]: print(p, "rows 1..5 == DATA:", rows(p)==DATA)
@lru_cache(None)
def D(w):
    if w=="": return 1
    return sum(D(t) for t in {w[:i]+w[i+2:] for i in range(len(w)-1) if w[i:i+2]=="UD"})
for w in ["UDUUDD","UUDDUD","UUUDDD","UUDUDD","UDUDUD"]: print("%e", w, D(w))
@lru_cache(None)
def S(w):
    if w=="": return 1
    return sum(S(w[:i]+w[i+2:]) for i in range(len(w)-1) if w[i:i+2]=="UD")
def dyck(n):
    out=[]
    def g(s,o,c):
        if o==n and c==n: out.append(s); return
        if o<n: g(s+"U",o+1,c)
        if c<o: g(s+"D",o,c+1)
    g("",0,0); return out
flat=[]
for n in range(1,6):
    C=Counter(S(w) for w in dyck(n)); flat+=[C.get(k,0) for k in range(1,max(C)+1)]
print("negative (deletion sequences) rows 1..5:", flat[:25], "differs" if flat!=DATA else "same")
