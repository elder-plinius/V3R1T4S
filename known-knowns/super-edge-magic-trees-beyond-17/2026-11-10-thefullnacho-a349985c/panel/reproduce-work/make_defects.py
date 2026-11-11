import sys, random, lzma
src, outdir = sys.argv[1], sys.argv[2]
L = open(src).read().splitlines(True)
random.seed(1)
def w(name, lines, xz=False):
    p = outdir + '/' + name + ('.txt.xz' if xz else '.txt')
    (lzma.open(p,'wt') if xz else open(p,'w')).writelines(lines)
def parse(l):
    f=l.rstrip('\n').split(';'); return f
# 1 swap two labels in one line (likely breaks sums)
A=L[:]; f=parse(A[500]); lab=f[2].split(','); lab[0],lab[1]=lab[1],lab[0]; f[2]=','.join(lab); A[500]=';'.join(f)+'\n'; w('d1_swaplabels',A)
# 2 duplicate line replaces another
A=L[:]; A[700]=A[701]; w('d2_dupline',A)
# 3 isomorphic relabelled copy (valid SEM labelling carried along) replaces another line
A=L[:]; f=parse(A[900]); n=18; perm=list(range(n)); random.shuffle(perm)
es=[tuple(map(int,e.split('-'))) for e in f[1].split(',')]; lab=f[2].split(',')
nl=[None]*n
for i in range(n): nl[perm[i]]=lab[i]
A[1234]='18;'+','.join('%d-%d'%(perm[u],perm[v]) for u,v in es)+';'+','.join(nl)+'\n'; w('d3_isocopy',A)
# 4 delete one line
A=L[:]; del A[42]; w('d4_dropline',A)
# 5 label out of range
A=L[:]; f=parse(A[10]); lab=f[2].split(','); i=lab.index('18'); lab[i]='19'; f[2]=','.join(lab); A[10]=';'.join(f)+'\n'; w('d5_labelrange',A)
# 6 non-tree: replace an edge by a repeated one
A=L[:]; f=parse(A[20]); es=f[1].split(','); es[-1]=es[0]; f[1]=','.join(es); A[20]=';'.join(f)+'\n'; w('d6_nottree',A)
# 7 wrong n field
A=L[:]; A[30]='17'+A[30][2:]; w('d7_nfield',A)
# 8 extra line (copy) -> count too high
A=L[:]+[L[5]]; w('d8_extraline',A)
# 9 xz copy of original and of d3 (exercise lzma path)
w('d9_orig_xz',L,xz=True)
A=L[:]; A[1234]=open(outdir+'/d3_isocopy.txt').read().splitlines(True)[1234]; w('d10_isocopy_xz',A,xz=True)
# 11 cycle + isolated vertex: 17 edges, connected fails
A=L[:]; f=parse(A[60]); es=[tuple(map(int,e.split('-'))) for e in f[1].split(',')]
deg=[0]*18
for u,v in es: deg[u]+=1; deg[v]+=1
leaf=[i for i in range(18) if deg[i]==1][0]
es=[e for e in es if leaf not in e]
# add an edge between two non-adjacent remaining vertices
S=set(es)|{(b,a) for a,b in es}
x=next((a,b) for a in range(18) for b in range(18) if a<b and a!=leaf and b!=leaf and (a,b) not in S)
es.append(x); f[1]=','.join('%d-%d'%e for e in es); A[60]=';'.join(f)+'\n'; w('d11_cycle',A)
