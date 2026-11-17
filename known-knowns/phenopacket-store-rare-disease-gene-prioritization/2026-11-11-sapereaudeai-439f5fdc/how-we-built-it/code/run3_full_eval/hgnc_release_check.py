"""Check: does the candidate space / NCBIGene->HGNC map from run 1's HGNC file (fetched 2026-11-11, filtered to genes
approved <= 2026-06-09) equal what the pre-corpus HGNC monthly archive of 2026-06-05 gives? Resource census only.
usage: python -I hgnc_release_check.py <run1 hgnc_protein-coding_gene.txt> <hgnc_complete_set_2026-06-05.txt> <genes_to_disease>"""
import sys, csv
a, b, g2d = sys.argv[1:4]
def load(p):
    cand, e2h = set(), {}
    for r in csv.DictReader(open(p, encoding='utf-8'), delimiter='\t'):
        if r['status'] != 'Approved' or r['locus_group'] != 'protein-coding gene': continue
        if r['date_approved_reserved'] and r['date_approved_reserved'] > '2026-06-09': continue
        cand.add(r['hgnc_id'])
        if r['entrez_id']: e2h[r['entrez_id'].strip()] = r['hgnc_id']
    return cand, e2h
ca, ea = load(a); cb, eb = load(b)
print('candidates run1-file', len(ca), 'archive-2026-06-05', len(cb), 'in both', len(ca & cb),
      'only run1', len(ca - cb), 'only archive', len(cb - ca))
ents = set()
for r in csv.DictReader(open(g2d, encoding='utf-8'), delimiter='\t'):
    if r['disease_id'].startswith('OMIM:') and r['association_type'] == 'MENDELIAN':
        ents.add(r['ncbi_gene_id'].replace('NCBIGene:', ''))
la = {(e, ea[e]) for e in ents if e in ea}; lb = {(e, eb[e]) for e in ents if e in eb}
print('MENDELIAN OMIM gene links mapped: run1-file', len(la), 'archive', len(lb), 'identical', la == lb,
      'differ', len(la ^ lb))
print('only-run1 candidates (first 10):', sorted(ca - cb)[:10])
print('only-archive candidates (first 10):', sorted(cb - ca)[:10])
