"""Genes of the fixed candidate space (19,274 HGNC protein-coding genes, run 1) left with no annotated disease after
cleaning, under the two disease->gene maps used in this run: (M) HPO genes_to_disease v2026-06-06, MENDELIAN, OMIM
(the frozen method's map) and (L) mim2gene_medgen 'phenotype' rows of the LIRICAL data directory (run 2's LIRICAL
gene-level scorer). Annotated = >= 1 phenotype-aspect (P, not NOT) row in the HPOA. Resource census only; it reads
no tool output. Also writes the included-case list and the seeded DEV sample.
usage: python -I gene_census.py <orig.hpoa> <clean.hpoa> <g2d> <mim2gene> <hgnc_pc> <hgnc_full_20260605> <run1_C_percase.tsv> <workdir>
"""
import sys, csv, json, random, collections, hashlib
orig, clean, g2d, m2g, hpc, hfull, cper, wd = sys.argv[1:9]
def pdis(p):
    s = set()
    for ln in open(p, encoding='utf-8'):
        if ln.startswith('#') or ln.startswith('database_id'): continue
        f = ln.rstrip('\n').split('\t')
        if len(f) > 10 and f[10] == 'P' and f[2] != 'NOT': s.add(f[0])
    return s
A, B = pdis(orig), pdis(clean)
cand, e2h_pc = [], {}
for r in csv.DictReader(open(hpc, encoding='utf-8'), delimiter='\t'):
    if r['status'] != 'Approved' or r['locus_group'] != 'protein-coding gene': continue
    if r['date_approved_reserved'] and r['date_approved_reserved'] > '2026-06-09': continue
    cand.append(r['hgnc_id'])
    if r['entrez_id']: e2h_pc[r['entrez_id']] = r['hgnc_id']
cs = set(cand)
M = collections.defaultdict(set)
for r in csv.DictReader(open(g2d, encoding='utf-8'), delimiter='\t'):
    if r['disease_id'].startswith('OMIM:') and r['association_type'] == 'MENDELIAN':
        h = e2h_pc.get(r['ncbi_gene_id'].replace('NCBIGene:', ''))
        if h: M[h].add(r['disease_id'])
e2h = {}
for r in csv.DictReader(open(hfull, encoding='utf-8'), delimiter='\t'):
    if r.get('entrez_id'): e2h[r['entrez_id'].strip()] = r['hgnc_id']
L = collections.defaultdict(set)
for ln in open(m2g, encoding='utf-8'):
    if ln.startswith('#'): continue
    f = ln.rstrip('\n').split('\t')
    if len(f) >= 3 and f[2] == 'phenotype' and f[1].isdigit():
        h = e2h.get(f[1])
        if h in cs: L[h].add('OMIM:' + f[0])
inc = []; gene = {}
for r in csv.DictReader(open(cper, encoding='utf-8'), delimiter='\t'):
    inc.append(r['case_id']); gene[r['case_id']] = r['gene']
inc = sorted(inc)
out = {'candidates': len(cand), 'included_cases': len(inc)}
for lab, mp in (('method_map_g2d', M), ('lirical_map_mim2gene', L)):
    before = {g for g in cs if mp.get(g, set()) & A}
    after = {g for g in cs if mp.get(g, set()) & B}
    lost = sorted(before - after)
    out[lab] = {'genes_annotated_before': len(before), 'genes_annotated_after': len(after),
                'genes_left_unannotated': len(lost), 'genes_left_unannotated_list': lost,
                'included_cases_whose_gene_annotated_before': sum(1 for c in inc if gene[c] in before),
                'included_cases_whose_gene_annotated_after': sum(1 for c in inc if gene[c] in after)}
open(wd + '/included_cases.txt', 'w', newline='\n').write('\n'.join(inc) + '\n')
SEED_DEV = 202611111222
dev = sorted(random.Random(SEED_DEV).sample(inc, 500))
open(wd + '/dev500.txt', 'w', newline='\n').write('\n'.join(dev) + '\n')
out['dev_seed'] = SEED_DEV
out['dev_sha256'] = hashlib.sha256(open(wd + '/dev500.txt', 'rb').read()).hexdigest()
out['included_sha256'] = hashlib.sha256(open(wd + '/included_cases.txt', 'rb').read()).hexdigest()
json.dump(out, open(wd + '/gene_census.json', 'w'), indent=1)
for lab in ('method_map_g2d', 'lirical_map_mim2gene'):
    out[lab] = {k: v for k, v in out[lab].items() if k != 'genes_left_unannotated_list'}
print(json.dumps(out, indent=1))
