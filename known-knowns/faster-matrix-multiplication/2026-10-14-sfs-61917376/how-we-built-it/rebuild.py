#!/usr/bin/env python3
"""Replay the recorded constructive decisions, without rerunning optimization."""
import hashlib,json,pathlib,sys
here=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(here/'discovery-code'))
import synth,exact_check
cert=json.loads((here/'certificate.json').read_text());s=cert['scheme'];a,b,c=s['n']
for k,n in zip('uvw',[a*b,b*c,s['m']]):
 circuit=synth.Circuit(n);refs=[{i:1} for i in range(n)]
 for row in s.get(k+'_fresh',[]):
  refs.append(circuit.materialize([(i,t['value']*v) for t in row for i,v in refs[t['index']].items()]))
 outputs=[circuit.materialize([(i,t['value']*v) for t in row for i,v in refs[t['index']].items()]) for row in s[k]]
 f,r=synth.prune(n,circuit.fresh,outputs);s[k+'_fresh']=synth.to_rows(f);s[k]=synth.to_rows(r)
result=exact_check.verify(s)
assert s['n']==[4, 5, 8] and s['m']==118 and result['additions']==486
(here/'rebuilt-scheme.json').write_text(json.dumps(s,indent=2)+'\n')
print(json.dumps(result));print('REBUILD PASS')
