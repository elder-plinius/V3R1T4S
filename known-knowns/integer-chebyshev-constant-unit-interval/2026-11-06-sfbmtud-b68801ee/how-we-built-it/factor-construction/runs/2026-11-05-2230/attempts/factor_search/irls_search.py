"""Dual-weighted reciprocal-value LLL: imported IRLS/auxiliary lattice heuristic."""
import json,math,time,resource,argparse,random,hashlib
from pathlib import Path
from flint import fmpz_mat,fmpz_poly
from lattice_search import eval_num,keypoly
B=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--dual',required=True);ap.add_argument('--seeds',required=True);ap.add_argument('--out',default='irls');ap.add_argument('--seconds',type=float,default=40);ap.add_argument('--power',type=float,default=1.0,choices=[0.5,1.0,1.5,2.0]);args=ap.parse_args();D=json.loads(Path(args.dual).read_text());F=json.loads(Path(args.seeds).read_text());LIB=F.get('candidates',F.get('factors'));known={tuple(f['coeffs_desc_w']) for f in json.loads((B.parent.parent/'data/upper_certificate.json').read_text())['factors']};q=2**24;st=time.perf_counter();found={};jobs=[]
points=[round(q*float(x)) for x in D['support_w']];masses=[max(1,round(10**30*math.sqrt(float(m)))) for m in D['masses']]
for i,f in enumerate(LIB):
 if time.perf_counter()-st>args.seconds:break
 c=f['coeffs_desc_w'];d=len(c)-1
 if not 3<=d<=30:continue
 z=[abs(eval_num(c,n,q)) for n in points]
 if min(z)==0:continue
 if args.power==0.5:z=[math.isqrt(v) for v in z]
 elif args.power==1.5:z=[v*math.isqrt(v) for v in z]
 elif args.power==2:z=[v*v for v in z]
 # Reciprocal evaluation weights are exact rational numbers after dyadic rounding.
 common=min(z);S=10**(3*d+30);rows=[]
 for k in range(d+1):
  ident=[0]*(d+1);ident[k]=1
  rows.append(ident+[(S*common*m*n**k)//(v*q**k*10**30) for n,m,v in zip(points,masses,z)])
 t=time.perf_counter();M=fmpz_mat(rows).lll();ps=[fmpz_poly([M[r,k] for k in range(d+1)]) for r in range(d+1)]
 for a in range(min(7,len(ps))):
  for b in range(a):ps.extend([ps[a]+ps[b],ps[a]-ps[b]])
 old=len(found)
 for p in ps:
  for h,e in p.factor()[1]:
   co=keypoly(h)
   if len(co)<2 or co in known or co in found:continue
   found[co]={'id':'irls_'+str(len(found)),'coeffs_desc_w':list(co),'degree':len(co)-1,'primitive':True,'irreducible_over_Q':True,'origin':{'method':'dual_reciprocal_value_lll','seed_coeffs_desc_w':c,'dual_source':args.dual,'denominator':q,'mass_scale':10**30,'matrix_scale_power':3*d+30,'reciprocal_power':args.power}}
 jobs.append({'source_index':i,'degree':d,'seconds':time.perf_counter()-t,'new_factors':len(found)-old});print(jobs[-1],flush=True)
 out={'claim_level':'HEURISTIC','variable':'w','coefficient_order':'descending','candidates':list(found.values()),'jobs':jobs,'elapsed_seconds':time.perf_counter()-st,'maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss};(B/(args.out+'.json')).write_text(json.dumps(out,indent=2))
print({k:v for k,v in out.items() if k not in ['jobs','candidates']});print('candidate_count',len(found))
