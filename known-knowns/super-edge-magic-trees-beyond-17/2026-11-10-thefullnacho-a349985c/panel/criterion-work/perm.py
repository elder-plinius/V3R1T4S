import sys,random
random.seed(int(sys.argv[1]))
for line in sys.stdin:
    f=line.rstrip("\n").split(";"); n=int(f[0])
    E=[tuple(map(int,x.split("-"))) for x in f[1].split(",")]; L=list(map(int,f[2].split(",")))
    p=list(range(n)); random.shuffle(p)
    E2=[(p[u],p[v]) if random.random()<.5 else (p[v],p[u]) for u,v in E]; random.shuffle(E2)
    L2=[0]*n
    for i in range(n): L2[p[i]]=L[i]
    print("%d;%s;%s"%(n,",".join("%d-%d"%e for e in E2),",".join(map(str,L2))))
