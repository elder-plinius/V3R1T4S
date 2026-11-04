"""Compare every saved run output in result/ with the OEIS DATA in data/ (run from claim/).
Prints one line per published term (A = benzZQ, B = benzB128 repro runs), then the two n=20 runs of A364417."""
import re,os
def data(f):
    t=open(f).read(); s=''.join(re.findall(r'^%[STU] A\d+ (.*)$',t,re.M)); return [int(x) for x in s.split(',') if x]
def run(pre):
    o,tm,er=pre+'.out',pre+'.time',pre+'.err'
    if not (os.path.exists(tm) and os.path.exists(o) and os.path.getsize(o)>0): return None
    e=open(er).read()
    return int(open(o).read().split()[0]), open(tm).read().split()[0], ('overflow=0' in e or 'overflow 0' in e)
D={'A364416':data('data/A364416.txt'),'A364417':data('data/A364417.txt')}
bad=0; missA=0
for s,v in D.items():
    for i,val in enumerate(v):
        n=i+3; row=[s,'n=%d'%n,str(val)]
        for p in 'AB':
            r=run('result/%s_repro/%s_n%d'%(p,s,n))
            if r is None:
                row.append(p+':not-run'); missA+= (p=='A')
            else:
                ok=r[0]==val and r[1]=='exit=0' and r[2]; bad+= not ok
                row.append(p+(':OK' if ok else ':MISMATCH got=%d %s overflow0=%s'%r))
        print(' '.join(row))
a=run('result/A_final/A364417_n20'); b=run('result/B_final/B_A364417_n20')
print('A364417 n=20 A(benzZQ)=%s B(benzB64)=%s'%(a,b))
agree = a and b and a[0]==b[0] and a[1]=='exit=0' and b[1]=='exit=0' and a[2] and b[2]
print('published mismatches=%d  A missing=%d  n20 agree=%s'%(bad,missA,bool(agree)))
print('RESULT', 'PASS' if bad==0 and missA==0 and agree else 'FAIL')
