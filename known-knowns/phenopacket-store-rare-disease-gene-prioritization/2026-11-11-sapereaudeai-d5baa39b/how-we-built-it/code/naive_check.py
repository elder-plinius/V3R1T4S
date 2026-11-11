"""Independent naive re-check of gene-level reciprocal ranks from LIRICAL benchmark CSVs (pandas, explicit sums).
usage: python -I naive_check.py <csv.gz> <hgnc_pc> <hgnc_full> <mim2gene> <run1_C_percase.tsv> [percase.tsv cond]
Without percase.tsv: prints RR per case. With it: compares to column rr_<cond> and reports the max abs difference."""
import sys
import pandas as pd
csvp, hpc, hfull, m2g, c1 = sys.argv[1:6]
pc = pd.read_csv(hpc, sep='\t', dtype=str, usecols=['hgnc_id', 'status', 'locus_group', 'date_approved_reserved'])
pc = pc[(pc.status == 'Approved') & (pc.locus_group == 'protein-coding gene') &
        (pc.date_approved_reserved.fillna('') <= '2026-06-09')]
cand = set(pc.hgnc_id)
hf = pd.read_csv(hfull, sep='\t', dtype=str, usecols=['hgnc_id', 'entrez_id']).dropna()
m = pd.read_csv(m2g, sep='\t', dtype=str)
m.columns = ['mim', 'GeneID', 'type', 'Source', 'MedGenCUI', 'Comment']
m = m[(m.type == 'phenotype') & (m.GeneID != '-')]
m = m.merge(hf, left_on='GeneID', right_on='entrez_id')
m = m[m.hgnc_id.isin(cand)]
m['disease_id'] = 'OMIM:' + m.mim
d2g = m[['disease_id', 'hgnc_id']].drop_duplicates()
gold = pd.read_csv(c1, sep='\t', dtype=str).set_index('case_id')['gene']
df = pd.read_csv(csvp, dtype={'disease_id': str})
df['case_id'] = df.phenopacket.str.replace(r'\.json$', '', regex=True)
res = {}
for cid, sub in df.groupby('case_id'):
    gs = sub.merge(d2g, on='disease_id').groupby('hgnc_id').post_test_proba.max()
    allg = pd.Series(0.0, index=sorted(cand)); allg.loc[gs.index] = gs.values
    t = allg.get(gold[cid], 0.0)
    g = int((allg > t).sum()); k = int((allg == t).sum()) - 1
    res[cid] = sum(1.0 / r for r in range(g + 1, g + k + 2)) / (k + 1)
if len(sys.argv) > 6:
    pcs = pd.read_csv(sys.argv[6], sep='\t').set_index('case_id')['rr_' + sys.argv[7]]
    common = [c for c in res if c in pcs.index]
    diff = max(abs(res[c] - pcs[c]) for c in common)
    print(f'compared {len(common)} cases ({sys.argv[7]}), max |naive - scorer| = {diff:.3g}')
else:
    for c, v in sorted(res.items()):
        print(c, f'{v:.6f}')
