#!/usr/bin/env python3
"""Calibrate full-Z verifiers on a pinned positive and one changed output sign."""
import copy, json, pathlib, sys
import synth
sys.path.insert(0,str(synth.ROOT/'tools'))
import basis_check

p=synth.ROOT/'sources/schemes/4x4x5_m61_cr233_fv93_cn452_ZT_reduced.json'
s=json.loads(p.read_text())
positive={'exact':synth.exact_check.verify(s),'basis':basis_check.check(s)}
bad=copy.deepcopy(s); bad['w'][0][0]['value']*=-1
neg={}
for name,fn in [('exact',synth.exact_check.verify),('basis',basis_check.check)]:
    try: fn(bad)
    except Exception as e: neg[name]={'rejected':True,'error':str(e)}
    else: neg[name]={'rejected':False}
assert all(v['rejected'] for v in neg.values())
out={'source':p.name,'positive':positive,'corrupt_output_sign':neg,'pass':True}
(synth.HERE/'output/calibration.json').write_text(json.dumps(out,indent=2)+'\n')
(synth.HERE/'output/corrupt-negative.json').write_text(json.dumps(bad)+'\n')
print(json.dumps(out,indent=2))
