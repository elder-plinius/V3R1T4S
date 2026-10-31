#!/usr/bin/env python3
"""Offline full enumeration of one strict stable-marriage preference object."""
from pathlib import Path
import hashlib,json,subprocess,tempfile,shutil,sys
ROOT=Path(__file__).resolve().parent
def need(ok,message):
 if not ok:raise ValueError(message)
def invoke(args):
 p=subprocess.run(args,cwd=ROOT,text=True,capture_output=True)
 need(p.returncode==0,'verification command failed')
 return p.stdout
try:
 o=json.loads((ROOT/'object.json').read_text())
 for k in ('n','count','bar'):need(type(o.get(k)) is int,'invalid metadata')
 for name,key in [('object.prefs','prefs_sha256'),('construction.word','word_sha256')]:need(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==o[key],'object hash mismatch')
 cc=next((x for x in ['c++','clang++','g++'] if shutil.which(x)),None);need(cc is not None,'C++17 compiler required')
 with tempfile.TemporaryDirectory(prefix='verify-build-',dir=ROOT) as tmp:
  tmp=Path(tmp);binary=tmp/'arc_count'
  invoke([cc,'-O3','-std=c++17',str(ROOT/'arc_count.cpp'),'-o',str(binary)])
  rebuilt=tmp/'rebuilt.prefs';invoke([sys.executable,str(ROOT/'rebuild.py'),str(ROOT/'construction.word'),str(rebuilt)])
  need(rebuilt.read_bytes()==(ROOT/'object.prefs').read_bytes(),'construction does not rebuild the object')
  pos=tmp/'positive.prefs';pos.write_text('1 2\n2 1\n2 1\n1 2\n');need(json.loads(invoke([str(binary),str(pos)]))['count']==2,'positive calibration failed')
  bad=tmp/'bad.prefs';bad.write_text('1 1\n2 1\n2 1\n1 2\n');p=subprocess.run([str(binary),str(bad)],capture_output=True);need(p.returncode!=0,'malformed profile was accepted')
  z=json.loads(invoke([str(binary),str(ROOT/'object.prefs')]))
  need(z['complete'] is True and z['n']==o['n'] and z['count']==o['count'],'full exact count mismatch')
  need(z['stable_leaves']==o['count'] and o['count']>o['bar'],'strict improvement failed')
  print(json.dumps({'n':z['n'],'count':z['count'],'bar':o['bar'],'improvement':o['count']-o['bar'],'complete':True,'every_leaf_stable':True,'nodes':z['nodes'],'seconds':z['seconds'],'prefs_sha256':o['prefs_sha256'],'construction_rebuilds':True,'calibration_tests':'PASS'},sort_keys=True))
 print('PASS')
except Exception as e:
 print('FAIL: '+str(e) if isinstance(e,ValueError) else 'FAIL: verification error');sys.exit(1)
