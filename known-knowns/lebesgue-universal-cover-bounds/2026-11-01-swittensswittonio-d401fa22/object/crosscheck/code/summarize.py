import csv, collections, statistics as st
rows=list(csv.DictReader(open('outputs/leaf_table.tsv'),delimiter='\t'))
def f(r,k):
    try: return float(r[k])
    except: return None
print('leaves',len(rows),'accepted',sum(int(r['accepted']) for r in rows),'below 0.8344:',[r['gid'] for r in rows if float(r['slack_vs_0.8344'])<0])
for s in ('U','W','D','ALL'):
    R=[r for r in rows if s=='ALL' or s in r['strata'].split('+')]
    sl=[float(r['slack_vs_0.8344']) for r in R]
    print(s,'n',len(R),'min slack %.6e mean %.6e max %.6e'%(min(sl),st.mean(sl),max(sl)),'accepted',sum(int(r['accepted']) for r in R))
# hull-only (leaves not closed a-priori)
H=[r for r in rows if float(r['lb_certified'])>float(r['apriori_lb'])+1e-15]
print('hull-closed leaves',len(H),'min hull slack %.6e'%min(float(r['slack_vs_0.8344']) for r in H))
for N in ('1024','4096','16384'):
    below=[r for r in H if float(r['hull_lb_N'+N])<0.8344]
    print('N',N,'hull leaves with LB<0.8344 at this resolution only:',len(below))
# comparison with author double bound and previous C# value
d=[abs(float(r['lb_certified'])-float(r['author_double_lb'])) for r in H]
print('vs author double (K=1024): max |diff| %.3e, mean %.3e; mine>=author-? min(mine-author) %.3e max %.3e'%(max(d),st.mean(d),min(float(r['lb_certified'])-float(r['author_double_lb']) for r in H),max(float(r['lb_certified'])-float(r['author_double_lb']) for r in H)))
P=[r for r in rows if r['prev_run_lb'] not in ("''",'')]
dd=[float(r['lb_certified'])-float(r['prev_run_lb'].strip("'")) for r in P]
print('vs previous-run C# (dump LB) n',len(P),'mine - prev: min %.3e max %.3e mean %.3e'%(min(dd),max(dd),st.mean(dd)))
print('by depth: n, min slack')
bd=collections.defaultdict(list)
for r in rows: bd[int(r['depth'])].append(float(r['slack_vs_0.8344']))
for k in sorted(bd): print(k,len(bd[k]),'%.4e'%min(bd[k]))
