# Derived upper bounds for z(m,n;3,3) from published base facts via the elementary averaging lemmas
#   z(m,n) <= floor(n*z(m,n-1)/(n-1))   and   z(m,n) <= floor(m*z(m-1,n)/(m-1))
# Base facts are tagged with their source; closure computed on window m in 12..16, n in 12..22 (symmetric z(m,n)=z(n,m) not needed here).
import itertools
W_M=range(12,17); W_N=range(12,23)
collins={ # Collins-Riasanovsky-Wallace-Radziszowski 2016, Table 4 (upper bounds, rows 12..16)
 12:{12:80,13:86,14:91,15:96,16:99,17:103,18:109},
 13:{13:92,14:98,15:104,16:107,17:110,18:116},
 14:{14:105,15:112,16:115,17:118,18:124},
 15:{15:120,16:123,17:126,18:132},
 16:{16:128,17:133,18:140}}
dgh={ # Davies-Gill-Horsley Table 2 entries (improved over Roman) for rows 13..16, n=17..23
 13:{17:116,18:121,19:125,20:130,21:135},
 14:{17:124,18:129,19:135,20:140,21:145,22:150},
 15:{17:132,18:138,19:143,20:149,21:154,23:165},
 16:{17:141,18:146,19:152,20:158,21:164,22:169,23:175}}
afr={ # Hou 2608.08549 / Afrasyab 2608.08154 (Aug 2026): exact/upper values
 (12,18):108,(12,19):114,(12,20):120,(12,21):126,(12,22):132,(13,22):137,
 (13,17):110,(13,18):116,(14,17):118,(14,18):124,(15,17):126,(15,18):132,(16,17):133}
def closure(base):
    U=dict(base)
    ch=True
    while ch:
        ch=False
        for m in W_M:
            for n in W_N:
                cands=[U.get((m,n),10**9)]
                if (m,n-1) in U: cands.append((n*U[(m,n-1)])//(n-1))
                if (m-1,n) in U: cands.append((m*U[(m-1,n)])//(m-1))
                v=min(cands)
                if v<U.get((m,n),10**9):
                    U[(m,n)]=v; ch=True
    return U
def tobase(d):
    return {(m,n):v for m,row in d.items() for n,v in row.items()}
bA=tobase(collins)
bB=dict(bA)
for k,v in afr.items(): bB[k]=min(bB.get(k,10**9),v)
bC=dict(bA)  # + DGH
for k,v in tobase(dgh).items(): bC[k]=min(bC.get(k,10**9),v)
UA=closure(bA); UB=closure(bB); UC=closure(bC)
cells=[(13,19),(14,19),(16,18),(14,20),(16,19)]
ours={(13,19):119,(14,19):127,(16,18):137,(14,20):131,(16,19):142}
print('cell  DGH-table  Collins-only-closure  +Hou/Afrasyab-closure  ours')
for c in cells:
    print(c, tobase(dgh).get(c), collins.get(c[0],{}).get(c[1]), '|', UA.get(c), UB.get(c), '| DGH-incl closure', UC.get(c), '| ours', ours[c])
print()
print('window of closure B (+Hou/Afrasyab):')
for m in W_M:
    print(m, [UB.get((m,n)) for n in range(17,23)])
