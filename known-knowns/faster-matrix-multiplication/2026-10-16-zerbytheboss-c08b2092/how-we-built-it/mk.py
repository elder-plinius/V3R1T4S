import json,lib,sys
def write(U,V,W,n,path):
    m=len(U)
    with open(path,'w') as f:
        f.write(f"{n[0]} {n[1]} {n[2]} {m}\n")
        for M in(U,V,W): f.write(' '.join(str(x) for r in M for x in r)+'\n')
if __name__=='__main__':
    d=json.load(open('repo/schemes/results/addition_reduced_ZT/3x4x5_m47_cr161_cn277_ZT_reduced.json'))
    U,V,W=lib.tensors(d); write(U,V,W,d['n'],'base.txt')
    print(sum(x!=0 for r in U for x in r)-47,sum(x!=0 for r in V for x in r)-47,sum(x!=0 for r in W for x in r)-15)
