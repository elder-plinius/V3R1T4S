"""Lead agent's check on the FROZEN claim object (claim/output/dialogues-fold*.npz): per-fold gains and how concentrated the gain is across recordings.
Usage (from the run folder): python3 -I lead-agent-checks/frozen_object_folds_and_recordings.py claim/output"""
import sys, collections
import numpy as np
d = sys.argv[1]; allR = []; allM = []; allT = []; recs = []
print('fold  positions  model   R1     twin   gain over R1  gain over twin')
for f in range(5):
    z = np.load(f'{d}/dialogues-fold{f}.npz', allow_pickle=False); t = z['target']; i = np.arange(len(t))
    for k in ('R1', 'selected_full', 'selected_twin'):
        p = z[k]; assert np.all(p > 0) and np.allclose(p.sum(1), 1, atol=1e-12), (f, k)
    r1 = -np.log2(z['R1'][i, t]); m = -np.log2(z['selected_full'][i, t]); tw = -np.log2(z['selected_twin'][i, t])
    print(f'{f:4d} {len(t):10d}  {m.mean():.4f} {r1.mean():.4f} {tw.mean():.4f}   {r1.mean()-m.mean():+.4f}       {tw.mean()-m.mean():+.4f}')
    allR.append(r1); allM.append(m); allT.append(tw); recs += list(z['group'])
R = np.concatenate(allR); M = np.concatenate(allM); T = np.concatenate(allT)
print(f'pooled  {len(R)} positions: model {M.mean():.9f}  R1 {R.mean():.9f}  twin {T.mean():.9f}  (claim: 2.564370989 / 2.794780553 / 2.850951798)')
for name, base in (('R1', R), ('twin', T)):
    tot = collections.defaultdict(float); cnt = collections.Counter()
    for r, g in zip(recs, base - M): tot[r] += g; cnt[r] += 1
    top = sorted(tot.items(), key=lambda kv: -kv[1])[:5]; s = sum(tot.values()); keep = [r for r in tot if r not in dict(top)]
    print(f'gain over {name}: recordings with a positive total gain {sum(1 for v in tot.values() if v > 0)} of {len(tot)}; top 5 recordings supply {sum(v for _, v in top)/s:.1%} of the summed gain (largest {top[0][1]/s:.1%}); without those 5: {sum(tot[r] for r in keep)/sum(cnt[r] for r in keep):+.4f} bits/coda over {len(keep)} recordings')
