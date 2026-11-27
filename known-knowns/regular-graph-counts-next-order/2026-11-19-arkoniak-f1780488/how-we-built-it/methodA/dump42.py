import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sys, time
import engine as E
E.set_degree(3)
N=42
t0=time.time()
parts=list(E.partitions(N))
rows=[]
for lam in parts:
    rows.append((lam, E.F_A(lam)))
with open(sys.argv[1] if len(sys.argv) > 1 else 'py42_out.csv','w') as f:  # output path
    f.write("# partition(desc,space-sep) ; F_A  (d=3, N=42)\n")
    for lam,v in rows:
        f.write("%s;%d\n" % (" ".join(map(str,lam)), v))
sys.stderr.write("types=%d dt=%.1fs cache=%d\n"%(len(parts), time.time()-t0, E.Phi.cache_info().currsize))
