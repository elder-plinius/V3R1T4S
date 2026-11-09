# Independent checker: explicit enumeration of locally disjoint rooted identity trees.
# A tree = set of pairwise-distinct child trees (identity, enforced by strictly increasing
# child ids over canonical ids), with every two children having disjoint child-sets
# (locally disjoint). Recursive by construction: only valid trees ever get ids.
import sys
N=int(sys.argv[1]); nodisj = len(sys.argv)>2
size=[]; kids=[]   # per tree id: size, frozenset of child ids
for n in range(1,N+1):
    last = (n==N)
    out=[]; cnt=0
    if n==1:
        out=[frozenset()]; cnt=1
    else:
        tot=len(size)
        def rec(rem,start,chosen,used):
            global cnt
            if rem==0:
                cnt+=1
                if not last: out.append(frozenset(chosen))
                return
            for i in range(start,tot):
                s=size[i]
                if s>rem: break
                k=kids[i]
                if not nodisj and not used.isdisjoint(k): continue
                chosen.append(i)
                rec(rem-s,i+1,chosen,used|k)
                chosen.pop()
        rec(n-1,0,[],frozenset())
    print(n,cnt,flush=True)
    for m in out: size.append(n); kids.append(m)
