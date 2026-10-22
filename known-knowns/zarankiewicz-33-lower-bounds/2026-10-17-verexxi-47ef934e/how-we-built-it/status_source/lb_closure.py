import json, math
nb=json.load(open('df_new_bounds.json',encoding='utf-8'))['cells']
ex=json.load(open('df_extended.json',encoding='utf-8'))['frontier']['paper_bounds']
# V1: Bhan et al Fig.2 lower bounds (BNL2026) for open cells + established exact values (cells whose source is 'established')
L1={}
for k,v in ex.items():
    m,n=map(int,k.split(',')); L1[(m,n)]=v['lower']
for k,v in nb.items():
    m,n=map(int,k.split(','))
    if v['lower_source']=='established': L1[(m,n)]=max(L1.get((m,n),0),v['lower'])
# Fig.2 'established' beige cells also contain exact values for m<=9 etc. already in nb as established.
# V2: add Aug-2026 exact witnesses (Hou 2608.08549, Afrasyab 2608.08154, dfield repo)
V2add={(12,18):108,(12,19):114,(12,20):120,(12,21):126,(12,22):132,(13,17):110,(13,18):116,(14,17):118,(14,18):124,(15,17):126,(15,18):132,(16,17):132,(13,22):137,
       (9,23):103,(10,21):106,(10,22):110,(10,23):112,(11,19):106,(11,20):111,(11,23):123,(12,23):134}
# V3: add Saurabh 2608.26603
V3add={(13,19):118,(14,19):126,(16,18):136,(14,20):126,(16,19):136}
def close(base,rules=('mono','plus2','del')):
    L=dict(base)
    cells=[(m,n) for m in range(8,17) for n in range(16,24)]
    changed=True
    while changed:
        changed=False
        for (m,n) in cells:
            cand=L.get((m,n),0)
            if 'mono' in rules:
                for (a,b) in ((m-1,n),(m,n-1)):
                    if (a,b) in L: cand=max(cand,L[(a,b)])
            if 'plus2' in rules:
                for (a,b) in ((m-1,n),(m,n-1)):
                    if (a,b) in L: cand=max(cand,L[(a,b)]+2)
            if 'del' in rules:
                for (a,b) in ((m+1,n),(m,n+1)):
                    if (a,b) in L:
                        big = a if a!=m else b   # the dimension that was larger
                        cand=max(cand, -((-L[(a,b)]*(big-1))//big))
            if cand>L.get((m,n),0):
                L[(m,n)]=cand; changed=True
    return L
cells=[(13,19),(14,19),(16,18),(14,20),(16,19)]
ours={(13,19):119,(14,19):127,(16,18):137,(14,20):131,(16,19):142}
b1=dict(L1)
b2=dict(b1); 
for k,v in V2add.items(): b2[k]=max(b2.get(k,0),v)
b3=dict(b2)
for k,v in V3add.items(): b3[k]=max(b3.get(k,0),v)
for name,b in (('V1 Bhan Fig2 only',b1),('V2 +Hou/Afrasyab/dfield',b2),('V3 +Saurabh',b3)):
    for rules in (('mono',),('mono','plus2'),('mono','plus2','del')):
        L=close(b,rules)
        print(f'{name:26s} rules={"+".join(rules):14s}', {c:L.get(c) for c in cells})
print('ours   ', {c:ours[c] for c in cells})
# What does deletion from (13,22)=137 etc. give, verbose path
L=close(b3,('mono','plus2','del'))
for m in range(12,17): print(m,[L.get((m,n)) for n in range(17,24)])
