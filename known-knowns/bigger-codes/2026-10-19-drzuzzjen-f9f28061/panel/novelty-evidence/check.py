import hashlib,json,pathlib,resource,time
ROOT=pathlib.Path(__file__).resolve().parent
def inspect(rows,n,w,d,expected):
 if len(rows)!=expected:return {'ok':False,'reason':'count'}
 seen=set();values=[]
 for row in rows:
  if len(row)!=n or any(c not in '01' for c in row):return {'ok':False,'reason':'format'}
  v=int(row,2)
  if v.bit_count()!=w:return {'ok':False,'reason':'weight'}
  if v in seen:return {'ok':False,'reason':'duplicate'}
  seen.add(v);values.append(v)
 minimum=n;pairs=0
 for i,a in enumerate(values):
  for b in values[:i]:
   dist=(a^b).bit_count();pairs+=1
   if dist<d:return {'ok':False,'reason':'distance','distance':dist}
   minimum=min(minimum,dist)
 return {'ok':True,'minimum':minimum,'pairs':pairs,'count':len(rows)}
t=time.monotonic()
good=['111000000','000111000','000000111']
controls={'valid':inspect(good,9,3,6,3),'duplicate':inspect(good+[good[0]],9,3,6,4),'weight':inspect(['110000000']+good[1:],9,3,6,3),'distance':inspect(['111000000','110100000'],9,3,6,2),'format':inspect(['x11000000']+good[1:],9,3,6,3),'count':inspect(good,9,3,6,4)}
assert controls['valid']['ok'] and all(not r['ok'] for k,r in controls.items() if k!='valid')
p=ROOT.parent/'run/CANDIDATE_M8734.txt';raw=p.read_bytes()
result={'source_sha256':hashlib.sha256(raw).hexdigest(),'controls':controls,'result':inspect(raw.decode('ascii').splitlines(),25,11,6,8734),'wall_seconds':time.monotonic()-t,'max_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'threads':1}
(ROOT/'exact-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
