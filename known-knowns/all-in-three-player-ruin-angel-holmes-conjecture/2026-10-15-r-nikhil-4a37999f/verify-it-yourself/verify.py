from pathlib import Path
import hashlib,json,subprocess,sys,tempfile,time
p=Path(__file__).resolve().parent;root=p.parent;obj=root/'object';started=time.monotonic()
if sys.flags.optimize:raise RuntimeError('Python assertions must be enabled')
manifest=json.loads((obj/'proof-manifest.json').read_text())
for name,want in manifest.items():
 if hashlib.sha256((obj/name).read_bytes()).hexdigest()!=want:raise RuntimeError('Object hash mismatch: '+name)
expected=json.loads((p/'expected.json').read_text())
with tempfile.TemporaryDirectory(prefix='all-in-proof-') as td:
 out=Path(td)
 subprocess.run(['c++','-O3','-std=c++17',str(p/'independent_memo.cpp'),'-o',str(out/'kernel')],check=True)
 for item in expected['certificates']:
  name=Path(item['file']).stem;cert=obj/item['file']
  if hashlib.sha256(cert.read_bytes()).hexdigest()!=item['sha256']:raise RuntimeError('Certificate hash mismatch')
  with (out/(name+'.geometry')).open('w') as f:
   subprocess.run([sys.executable,'-E','-B',str(p/'independent.py'),str(cert),str(out/(name+'.tasks'))],stdout=f,check=True)
  geometry=json.loads((out/(name+'.geometry')).read_text())
  with (out/(name+'.bounds')).open('w') as f,(out/(name+'.stderr')).open('w') as e:
   subprocess.run([str(out/'kernel'),str(out/(name+'.tasks'))],stdout=f,stderr=e,check=True)
  transcript=hashlib.sha256((out/(name+'.bounds')).read_bytes()).hexdigest()
  if transcript!=item['full_transcript_sha256']:raise RuntimeError('Recomputed transcript mismatch')
  print(json.dumps({'certificate':item['file'],'nodes':geometry['nodes'],'leaves':geometry['leaves'],'minimum':geometry['stored_minimum'],'full_transcript_sha256':transcript,'verified':True}),flush=True)
print(json.dumps({'seconds':time.monotonic()-started,'verified':True}),flush=True)
print('PASS',flush=True)
