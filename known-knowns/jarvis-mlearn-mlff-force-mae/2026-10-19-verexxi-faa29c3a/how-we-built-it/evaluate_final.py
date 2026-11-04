"""evaluate_final.py EL JOBPREFIX : score the 3 seeds + ensemble on the official test ids (run once per element)."""
import sys, json, numpy as np, os
sys.path.insert(0, 'src')
import mldata as m
from ase import Atoms
from ase.io import write
import predict as P
el, prefix = sys.argv[1], sys.argv[2]
te = m.structs(el, 'test'); tr = m.structs(el, 'train')
xyz = f'work/{el}/test_nolabel.xyz'
write(xyz, [ (lambda a: (a.info.__setitem__('jid', s['jid']), a)[1])(Atoms(s['z'], positions=s['pos'], cell=s['cell'], pbc=True)) for s in te])
truth = {s['jid']: s['f'] for s in te}
preds = []
out = {}
for k in (1, 2, 3):
    p = P.predict(f'{prefix}_s{k}/m.model', xyz); preds.append(p)
    out[f'seed{k}'] = m.mae([p[j] for j in truth], [truth[j] for j in truth])
ens = {j: np.mean([p[j] for p in preds], axis=0) for j in truth}
out['ensemble'] = m.mae([ens[j] for j in truth], [truth[j] for j in truth])
out['sd_seed'] = float(np.std([out['seed1'], out['seed2'], out['seed3']], ddof=1))
zt = np.concatenate([truth[j].ravel() for j in truth]); ztr = np.concatenate([s['f'].ravel() for s in tr])
out['zero_baseline'] = float(np.abs(zt).mean()); out['train_mean_baseline'] = float(np.abs(zt - ztr.mean()).mean())
os.makedirs(f'results/{el}', exist_ok=True)
np.savez(f'results/{el}/ens_pred.npz', **ens)
json.dump(out, open(f'results/{el}/test_scores.json', 'w'), indent=1); print(json.dumps(out, indent=1))
