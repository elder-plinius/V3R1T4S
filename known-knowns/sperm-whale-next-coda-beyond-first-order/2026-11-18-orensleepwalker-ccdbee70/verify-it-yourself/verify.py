"""Rebuild the supplied held-out probability object from a hash-checked data source."""
import argparse
import json
from pathlib import Path
import sys

import numpy as np

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('package', type=Path)
parser.add_argument('inputs', type=Path)
args = parser.parse_args()
package = args.package.resolve()
sys.path.insert(0, str(package/'how-we-built-it/code'))
import campaign
campaign.ROOT = args.inputs.resolve()

sequences = campaign.load_sequences('dialogues')
losses, groups, fold_ids, folds, _ = campaign.evaluate(sequences,'dialogues',retain=True)
object_dir = package/'object'
for study in folds:
    with np.load(object_dir/f"dialogues-fold{study['fold']}.npz",allow_pickle=False) as saved:
        for field in ('row','target','group'):
            assert np.array_equal(saved[field],study[field]),field
        for name in ('R1','selected_twin','selected_full'):
            probs = saved[name]
            assert np.all(probs > 0) and np.allclose(probs.sum(axis=1),1,rtol=0,atol=1e-12),name
            assert np.allclose(probs,study['predictions'][name],rtol=0,atol=1e-12),name

criteria = json.loads((object_dir/'score-summary.json').read_text())
base = losses['R1']
twin = losses['selected_twin']
candidate = losses['selected_full']
baseline_gain = float((base-candidate).mean())
twin_gain = float((twin-candidate).mean())
twin_ci = campaign.group_ci(twin-candidate,groups)
assert len(candidate) == criteria['score']['n']
assert abs(float(candidate.mean())-criteria['score']['model_score']) < 1e-12
assert baseline_gain >= .10 and twin_gain >= .05 and twin_ci[0] > 0
for mode in ('payload','first_order'):
    control_file = package/'how-we-built-it'/f'dialogues-{mode}-controls.jsonl'
    with control_file.open() as f:
        records = [json.loads(row) for row in f]
    assert len(records) == 400 and {row['seed'] for row in records} == set(range(310000,310400))
    for record in records:
        values = record['models']['selected']['gain']
        assert values['baseline'] < baseline_gain and values['twin'] < twin_gain
print(f'{len(candidate)} eligible positions. R1 {base.mean():.9f}, model {candidate.mean():.9f}, twin {twin.mean():.9f} bits/coda.')
print(f'Twin gain {twin_gain:.9f}; 95% REC interval {twin_ci}. All 800 frozen control receipts below the observed gains.')
