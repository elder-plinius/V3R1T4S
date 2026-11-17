"""Decompose LIRICAL's C-vs-PRE drop (descriptive; PREREG.md secondary).
usage: python -I decompose.py <percase.tsv> <run1 PRE_percase.tsv> <out.json>"""
import sys, json
import numpy as np
import pandas as pd
pc = pd.read_csv(sys.argv[1], sep='\t')
r1 = pd.read_csv(sys.argv[2], sep='\t')[['case_id', 'disease_in_pre', 'gene_annotated_in_pre']]
d = pc.merge(r1, on='case_id', how='left')
out = {'n': int(len(d))}
def block(x):
    return {'n': int(len(x)), 'MRR_C': float(x.rr_C.mean()), 'MRR_PRE': float(x.rr_PRE.mean()),
            'dMRR': float((x.rr_C - x.rr_PRE).mean()), 'top1_C': float(x.top1_C.mean()), 'top1_PRE': float(x.top1_PRE.mean()),
            'base_MRR_C': float(x.base_rr_C.mean()), 'base_MRR_PRE': float(x.base_rr_PRE.mean()),
            'dis_MRR_C': float(x.drr_C.mean()), 'dis_MRR_PRE': float(x.drr_PRE.mean())}
out['all'] = block(d)
for k, v in d.groupby('disease_in_pre'):
    out[f'disease_in_pre={k}'] = block(v)
for k, v in d.groupby('gene_annotated_in_pre'):
    out[f'gene_annotated_in_pre={k}'] = block(v)
# share of the total drop carried by cases whose disease had no annotation before the paper
tot = (d.rr_C - d.rr_PRE).sum()
out['share_of_drop_from_disease_not_in_pre'] = float((d.rr_C - d.rr_PRE)[d.disease_in_pre == 0].sum() / tot)
# tool x condition: LIRICAL drop minus baseline drop (difference in differences), case bootstrap
rng = np.random.default_rng(20261111)
did = (d.rr_C - d.rr_PRE) - (d.base_rr_C - d.base_rr_PRE)
bs = [did.values[rng.integers(0, len(d), len(d))].mean() for _ in range(2000)]
out['LIRICAL_drop_minus_baseline_drop'] = {'point': float(did.mean()), 'ci95_case': [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]}
out['share_lost_LIRICAL'] = float((d.rr_C - d.rr_PRE).mean() / d.rr_C.mean())
out['share_lost_baseline'] = float((d.base_rr_C - d.base_rr_PRE).mean() / d.base_rr_C.mean())
# ties at score 0 in PRE (gene cannot be ranked above the unlinked mass)
out['cases_gene_score0_C'] = int((d.gscore_C == 0).sum()); out['cases_gene_score0_PRE'] = int((d.gscore_PRE == 0).sum())
out['cases_causal_disease_absent_C'] = int((d.dscore_C == 0).sum()); out['cases_causal_disease_absent_PRE'] = int((d.dscore_PRE == 0).sum())
json.dump(out, open(sys.argv[3], 'w'), indent=1)
print(json.dumps(out, indent=1))
