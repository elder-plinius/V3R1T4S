"""Enumerate a finite cube of LLL-basis combinations, then exact-factor short vectors."""
import json,time,resource,itertools,hashlib,os,argparse
from pathlib import Path
import numpy as np
from flint import fmpz_mat,fmpz_poly
import lattice_search as L
B=Path(__file__).resolve().parent;ap=argparse.ArgumentParser();ap.add_argument('--version',default='v4');ap.add_argument('--width',type=int,default=10);ap.add_argument('--take',type=int,default=1024);ap.add_argument('--seconds',type=float,default=45);ap.add_argument('--out',default='short_combinations_v4');args=ap.parse_args();V=args.version;cert='runs/'+B.parent.parent.name+'/attempts/weight_optimization/candidates/'+V+'/candidate.json';dual=cert.replace('candidate.json','dual_measure.json');D=json.loads(Path(cert).read_text());L.DATA=D;L.LIB=D['factors'];L.DEN=D['N_w_degree'];xx=[float(x) for x in json.loads(Path(dual).read_text())['support_w']];known={tuple(f['coeffs_desc_w']) for f in D['factors']};known|={tuple(f['coeffs_desc_w']) for f in json.loads((B.parent.parent/'data/upper_certificate.json').read_text())['factors']};st=time.perf_counter();found={};jobs=[];(B/(args.out+'.pid')).write_text(str(os.getpid())+'\n')
for N in [100,180,260,340]:
 if time.perf_counter()-st>args.seconds:break
 seed=5741+N;d,es,ps,t,M=L.create(N,'cheb',seed,0,xx,65,.99,True);k=min(args.width,d+1);S=fmpz_mat([[M[i,j] for j in range(M.ncols())] for i in range(k)]);G=S*S.transpose();norm=max(int(G[i,i]) for i in range(k));g=np.array([[int(G[i,j])/norm for j in range(k)] for i in range(k)])
 C=np.array(list(itertools.product([-1,0,1],repeat=k)),dtype=np.int8);first=np.argmax(C!=0,axis=1);C=C[(C[np.arange(len(C)),first]==1)&(np.sum(np.abs(C),axis=1)>=3)];vals=np.einsum('bi,ij,bj->b',C,g,C,optimize=True);order=np.argpartition(vals,min(args.take,len(vals)-1))[:args.take];old=len(found)
 for row in order:
  combo=list(map(int,C[row]));p=sum((a*ps[i] for i,a in enumerate(combo)),fmpz_poly([0]))
  for f,e in p.factor()[1]:
   co=L.keypoly(f)
   if len(co)<2 or co in known or co in found:continue
   found[co]={'id':'short_combo_'+str(len(found)),'coeffs_desc_w':list(co),'degree':len(co)-1,'primitive':True,'irreducible_over_Q':True,'origin':{'method':'weighted_lll_short_combination','N':N,'residual_degree':d,'mode':'cheb','seed':seed,'drop':0,'prescribed_exponents':es,'weight_certificate':cert,'support_source':dual,'lll_delta':.99,'basis_combination':combo}}
 jobs.append({'N':N,'residual_degree':d,'cube_size':len(C),'vectors_factored':len(order),'new_factors':len(found)-old,'elapsed_seconds':time.perf_counter()-st});print(jobs[-1],flush=True)
 R={'claim_level':'HEURISTIC','variable':'w','coefficient_order':'descending','candidates':list(found.values()),'jobs':jobs,'elapsed_seconds':time.perf_counter()-st,'maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss};(B/(args.out+'.json')).write_text(json.dumps(R,indent=2))
print({k:v for k,v in R.items() if k not in ['jobs','candidates']});print('candidates',len(found))
