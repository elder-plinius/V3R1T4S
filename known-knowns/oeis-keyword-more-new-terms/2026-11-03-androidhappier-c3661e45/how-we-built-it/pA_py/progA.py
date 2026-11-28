# Program A (A131449): rows n = 0..NMAX; per Dyck word (ordered tree, n non-root vertices) the number of
# increasing labelings by the hook formula n!/prod h(v) over non-root v (h = subtree size from the
# matching parentheses); row sorted non-increasing.  Prints flattened "index value" lines (offset 0).
import sys
from math import factorial, prod
def dyck(n):
    out=[]
    def g(s,o,c):
        if o==n and c==n: out.append(s); return
        if o<n: g(s+"U",o+1,c)
        if c<o: g(s+"D",o,c+1)
    g("",0,0); return out
def hooks(w):
    st=[]; hs=[]
    for i,ch in enumerate(w):
        if ch=="U": st.append(i)
        else: j=st.pop(); hs.append((i-j+1)//2)
    return hs
idx=0
for n in range(int(sys.argv[1])+1):
    row=sorted((factorial(n)//prod(hooks(w)) for w in dyck(n)), reverse=True)
    sys.stderr.write("row %d len %d sum %d\n"%(n,len(row),sum(row)))
    for v in row: print(idx,v); idx+=1
