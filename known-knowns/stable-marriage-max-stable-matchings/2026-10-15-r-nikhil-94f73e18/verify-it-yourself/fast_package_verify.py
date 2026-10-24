from pathlib import Path
import hashlib,json,subprocess,tempfile,sys,shutil
P=Path(__file__).resolve().parents[1];V=P/'verify-it-yourself'
def need(ok,message):
 if not ok:raise ValueError(message)
try:
 o=json.loads((P/'object/object.json').read_text())
 for name,key in [('object.prefs','prefs_sha256'),('construction.word','word_sha256')]:
  need(hashlib.sha256((P/'object'/name).read_bytes()).hexdigest()==o[key],'object hash mismatch')
 prior=P/'the-record-we-beat/prior_n23.prefs'
 need(hashlib.sha256(prior.read_bytes()).hexdigest()=='54a3893d2994d461bff07d942221ed9c83fe8d5019330298babb0ff21d1ebff0','prior hash mismatch')
 with tempfile.TemporaryDirectory(prefix='stable-exact-') as td:
  t=Path(td);exe=t/'count';rebuilt=t/'rebuilt.prefs'
  subprocess.run([sys.executable,str(V/'rebuild.py'),str(P/'object/construction.word'),str(rebuilt)],check=True)
  need(rebuilt.read_bytes()==(P/'object/object.prefs').read_bytes(),'construction mismatch')
  subprocess.run([shutil.which('c++') or 'c++','-O3','-std=c++17',str(V/'memo.cpp'),'-o',str(exe)],check=True,capture_output=True)
  positive=t/'positive';positive.write_text('1 2\n2 1\n2 1\n1 2\n')
  need(json.loads(subprocess.check_output([str(exe),str(positive)],text=True))['count']==2,'positive control')
  negative=t/'negative';negative.write_text('1 1\n2 1\n2 1\n1 2\n')
  need(subprocess.run([str(exe),str(negative)],capture_output=True).returncode!=0,'malformed control')
  for profile,expected in [(P/'object/object.prefs',o['count']),(prior,o['bar'])]:
   result=json.loads(subprocess.check_output([str(exe),str(profile)],text=True))
   need(result['n']==o['n'] and result['count']==expected,'exact count mismatch')
   result['file']=str(profile.relative_to(P));print(json.dumps(result,sort_keys=True))
  need(o['count']>o['bar'],'strict improvement failed')
 print('PASS')
except Exception as e:
 print('FAIL: '+str(e));sys.exit(1)
