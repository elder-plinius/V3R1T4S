#!/usr/bin/env python3
import sys,subprocess,tempfile,pathlib
root=pathlib.Path(__file__).resolve().parents[1]
w=root/'object/A34_8_7_603.txt'; base=w.read_text().splitlines()
old_checker=root/'verify-it-yourself/upstream_cwcheck.py'
checks={}
for label,transform in {
 'bad_length':lambda w:w[:-1],
 'nonbinary':lambda w:'x'+w[1:],
 'weight':lambda w:'0'+w[1:] if w[0]=='1' else '1'+w[1:],
 'duplicate':lambda w:base[0],
 'short':lambda w:None,
}.items():
  rows=base.copy()
  if label=='short': rows.pop()
  else: rows[1]=transform(rows[1])
  with tempfile.TemporaryDirectory() as t:
    p=pathlib.Path(t)/'bad.txt';p.write_text('\n'.join(rows)+'\n')
    r=subprocess.run([sys.executable,str(old_checker),str(p),'34','8','7','--M','603'],capture_output=True,text=True)
    checks[label]=r.returncode!=0
    assert r.returncode!=0, label+' was unexpectedly accepted'
print('NEGATIVE_CONTROLS',checks)
print('PASS')
