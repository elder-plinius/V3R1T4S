#!/usr/bin/env python3
import json,random,sys
sys.dont_write_bytecode=True
import synth,dag_search,milp_search
rng=random.Random(19);g=dag_search.grammar(2,[],[{0:1,1:1}],False)
p,positive=milp_search.solve(2,g,1,5,rng)
assert p is not None and synth.count(*p)==1
q,negative=milp_search.solve(2,g,0,5,rng)
assert q is None and negative['status']==2
checks=[]
for item in json.loads((synth.HERE.parents[1]/'data/selected-sources.json').read_text()):
 s=json.loads((synth.ROOT/'sources/schemes'/item['file']).read_text());sizes,maps=synth.load_maps(s)
 for k,n in sizes.items():
  f,r=maps[k];df,dr=synth.transpose(n,f,r,rng)
  checks.append({'file':item['file'],'map':k,'source':synth.count(f,r),'transpose':synth.count(df,dr),'observed_delta':synth.count(df,dr)-synth.count(f,r),'dimension_delta':len(r)-n})
out={'positive':positive,'negative':negative,'transpose_count_calibration':checks,'all_deltas_match':all(x['observed_delta']==x['dimension_delta'] for x in checks),'pass':True}
assert out['all_deltas_match']
(synth.HERE/'output/milp-calibration.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
