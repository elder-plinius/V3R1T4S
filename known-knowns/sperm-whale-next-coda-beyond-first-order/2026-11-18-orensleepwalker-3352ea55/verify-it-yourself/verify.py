"""Rebuild every saved turn-taking probability and recompute the p4 threshold."""
import argparse
from pathlib import Path
import json
import sys
import numpy as np

parser=argparse.ArgumentParser()
parser.add_argument('root',type=Path)
args=parser.parse_args()
root=args.root.resolve()
sys.path.insert(0,str(root/'code'))
import campaign
campaign.ROOT=root
values,groups,folds,studies,_=campaign.evaluate(campaign.load_sequences('turns'),'turns',retain=True)
saved_result=json.loads((root/'output/turns-result.json').read_text())
for study in studies:
    with np.load(root/'output'/f"turns-fold{study['fold']}.npz",allow_pickle=False) as obj:
        for field in ('row','group','target'):
            assert np.array_equal(obj[field],study[field])
        for name in ('R1','selected_full'):
            assert np.allclose(obj[name],study['predictions'][name],atol=1e-12,rtol=0)
gain=values['R1']-values['selected_full']
assert abs(float(gain.mean())-saved_result['models']['selected']['gain']['baseline'])<1e-12
interval=campaign.group_ci(gain,groups)
assert gain.mean()>=.05 and interval[0]>0
maxima={}
for mode in ('payload','first_order'):
    records=[json.loads(line) for line in (root/'output'/f'turns-{mode}-controls.jsonl').read_text().splitlines()]
    assert len(records)==400 and {r['seed'] for r in records}==set(range(310000,310400))
    maximum=max(row['models']['selected']['gain']['baseline'] for row in records)
    assert maximum<float(gain.mean())
    maxima[mode]=maximum
print(json.dumps(dict(scored=len(gain),baseline_bits=float(values['R1'].mean()),
    model_bits=float(values['selected_full'].mean()),gain_bits=float(gain.mean()),CI95=interval,
    control_maxima=maxima),indent=2))
print('PASS')
