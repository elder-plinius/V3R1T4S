"""Exactly reproduce each recorded construction; no other lens code is used."""
import json,time,resource,argparse,os,math
from pathlib import Path
from flint import fmpz_poly,fmpz_mat
import lattice_search as L
B=Path(__file__).resolve().parent;ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--out',required=True);a=ap.parse_args();(B/(a.out+'.pid')).write_text(str(os.getpid())+'\n');D=json.loads((B/a.input).read_text());groups={};st=time.perf_counter();rows=[]
def path(s):return Path(s) if str(s).startswith('runs/') or str(s).startswith('/') else B/s
for f in D['factors']:
 if f['source_class']!='generated_outside_both_shipped_libraries':continue
 o=f['origin'];method=o['method']
 if method in ['weighted_exact_sample_lll','weighted_lll_short_combination']:
  k=(method,o['N'],o['mode'],o['seed'],o['drop'],o.get('weight_certificate','../../data/upper_certificate.json'),o.get('support_source'),o.get('lll_delta',0.99),o.get('node_bits',18),o.get('node_jitter',2))
 else:k=(method,json.dumps(o,sort_keys=True))
 groups.setdefault(k,[]).append(f)
for k,fs in groups.items():
 if k[0] in ['weighted_exact_sample_lll','weighted_lll_short_combination']:
  _,N,mode,seed,drop,cert,support,delta,bits,jitter=k;W=json.loads(path(cert).read_text());L.DATA=W;L.LIB=W['factors'];L.DEN=W['N_w_degree'];xx=[float(x) for x in json.loads(path(support).read_text())['support_w']] if support else None
  d,es,polys,t=L.create(N,mode,seed,drop,xx,max(65,fs[0]['origin']['residual_degree']),delta,node_bits=bits,node_jitter=jitter)
  assert all(es==f['origin']['prescribed_exponents'] for f in fs)
  if k[0]=='weighted_lll_short_combination':
   basis=polys;polys=[sum((co*basis[i] for i,co in enumerate(f['origin']['basis_combination'])),fmpz_poly([0])) for f in fs]
 elif k[0] in ['small_product_neighbor','new_seed_small_product_neighbor']:
  o=fs[0]['origin'];p=fmpz_poly(o['source_coeffs_desc_w'][::-1]);z=fmpz_poly(o['direction_coeffs_desc_w'][::-1]);polys=[p+o['multiplier']*z]
 elif k[0]=='dual_reciprocal_value_lll':
  o=fs[0]['origin'];dual=json.loads(path(o['dual_source']).read_text());q=o['denominator'];massscale=o['mass_scale'];co=o['seed_coeffs_desc_w'];d=len(co)-1;points=[round(q*float(x)) for x in dual['support_w']];masses=[max(1,round(massscale*math.sqrt(float(m)))) for m in dual['masses']];zs=[abs(L.eval_num(co,n,q)) for n in points];power=o.get('reciprocal_power',1.0)
  if power==0.5:zs=[math.isqrt(v) for v in zs]
  elif power==1.5:zs=[v*math.isqrt(v) for v in zs]
  elif power==2:zs=[v*v for v in zs]
  common=min(zs);scale=10**o['matrix_scale_power'];matrix=[]
  for j in range(d+1):
   ident=[0]*(d+1);ident[j]=1;matrix.append(ident+[(scale*common*m*n**j)//(z*q**j*massscale) for n,m,z in zip(points,masses,zs)])
  M=fmpz_mat(matrix).lll();polys=[fmpz_poly([M[r,j] for j in range(d+1)]) for r in range(d+1)]
  for u in range(min(7,len(polys))):
   for v in range(u):polys.extend([polys[u]+polys[v],polys[u]-polys[v]])
 else:raise ValueError('unsupported replay method '+k[0])
 found={L.keypoly(h) for p in polys for h,e in p.factor()[1]}
 for f in fs:
  ok=tuple(f['coeffs_desc_w']) in found;assert ok,(f['candidate_factor_index'],k)
  rows.append({'candidate_factor_index':f['candidate_factor_index'],'reproduced':ok,'method':k[0]})
 R={'candidate_sha256':D['candidate_sha256'],'complete':len(rows)==sum(f['source_class']=='generated_outside_both_shipped_libraries' for f in D['factors']),'all_reproduced':True,'factors':rows,'job_count_total':len(groups),'elapsed_seconds':time.perf_counter()-st,'maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss};(B/a.out).write_text(json.dumps(R,indent=2));print('matched',len(rows),'elapsed',time.perf_counter()-st,flush=True)
print({k:v for k,v in R.items() if k!='factors'})
