"""Step-5 self-check (written from the PREREG definitions, not from rdlib/h2h_score):
(1) the method: pure-Python sets on a seeded sample of cases. It parses hp.obo, the CLEANED HPOA and
    genes_to_disease itself, computes IC from the cleaned annotations, the asymmetric Resnik best-match average per
    disease (rounded to 1e-9), the gene max and the tie-aware expected reciprocal rank over the 19,274 candidates.
(2) LIRICAL: for seeded chunks, gene score = max post_test_proba over the case's output diseases mapped by
    mim2gene_medgen ('phenotype' rows) -> HGNC (hgnc 2026-06-05). Naive expected rank, compared with h2h_percase rr_L.
(3) The metrics recomputed from h2h_percase.tsv with plain means.
usage: python -I selfcheck.py <W>
"""
import sys, csv, gzip, random, math, collections, os, json
W = sys.argv[1]  # workspace root
R = W + '/runs/2026-11-11-1222'; O = R + '/attempts/full-eval/output'
H = W + '/cache/raredisease-run-2026-11-11-0916/hpo'; DD = W + '/cache/raredisease-run-2026-11-11-1222/lirical/dd_cleaned'
HPC = W + '/runs/2026-11-11-0916/data/hgnc_protein-coding_gene.txt'


def err(g, k):  # expected 1/rank, ranks g+1..g+k+1 equally likely
    return sum(1.0 / r for r in range(g + 1, g + k + 2)) / (k + 1)


# ---- candidates and maps
cand, e2h = [], {}
for r in csv.DictReader(open(HPC, encoding='utf-8'), delimiter='\t'):
    if r['status'] == 'Approved' and r['locus_group'] == 'protein-coding gene' and not (
            r['date_approved_reserved'] and r['date_approved_reserved'] > '2026-06-09'):
        cand.append(r['hgnc_id'])
        if r['entrez_id']:
            e2h[r['entrez_id']] = r['hgnc_id']
cs = set(cand)
g2d = collections.defaultdict(set)
for r in csv.DictReader(open(H + '/v2026-06-06.genes_to_disease.txt', encoding='utf-8'), delimiter='\t'):
    if r['disease_id'].startswith('OMIM:') and r['association_type'] == 'MENDELIAN':
        h = e2h.get(r['ncbi_gene_id'].replace('NCBIGene:', ''))
        if h in cs:
            g2d[h].add(r['disease_id'])
# ---- ontology
par, alt, repl, obs, cur = {}, {}, {}, set(), None
for line in open(H + '/v2026-06-06.hp.obo', encoding='utf-8'):
    line = line.strip()
    if line == '[Term]':
        cur = {'isa': []}; continue
    if line.startswith('['):
        cur = None; continue
    if cur is None:
        continue
    if line.startswith('id: '):
        cur['id'] = line[4:]; par[cur['id']] = cur['isa']
    elif line.startswith('is_a: '):
        cur['isa'].append(line[6:].split(' ')[0])
    elif line.startswith('alt_id: '):
        alt[line[8:]] = cur['id']
    elif line.startswith('is_obsolete: true'):
        obs.add(cur['id'])
    elif line.startswith('replaced_by: '):
        repl[cur['id']] = line[13:]
sys.setrecursionlimit(100000)
memo = {}


def anc(t):
    if t not in memo:
        s = {t}
        for p in par.get(t, []):
            if p.startswith('HP:'):
                s |= anc(p)
        memo[t] = s
    return memo[t]


def mp(t):
    for _ in range(6):
        if t in par and t not in obs:
            break
        t = alt.get(t) or repl.get(t)
        if t is None:
            return None
    if t not in par or t in obs or 'HP:0000118' not in anc(t):
        return None
    return t


# ---- cleaned annotations, IC
dis = collections.defaultdict(set)
for line in open(DD + '/phenotype.hpoa', encoding='utf-8'):
    if line.startswith('#') or line.startswith('database_id'):
        continue
    f = line.rstrip('\n').split('\t')
    if len(f) > 10 and f[10] == 'P' and f[2] != 'NOT':
        t = mp(f[3])
        if t:
            dis[f[0]].add(t)
clo = {d: set().union(*(anc(t) for t in ts)) & {x for x in set().union(*(anc(t) for t in ts)) if 'HP:0000118' in anc(x)}
       for d, ts in dis.items()}
cnt = collections.Counter()
for d, c in clo.items():
    cnt.update(c)
N = len(clo)
IC = {t: -math.log(n / N) for t, n in cnt.items()}
# ---- cases
cases = {r['case_id']: r for r in csv.DictReader(open(W + '/runs/2026-11-11-0916/work/cases.tsv', encoding='utf-8'), delimiter='\t')}
per = {r['case_id']: r for r in csv.DictReader(open(O + '/method/percase.tsv', encoding='utf-8'), delimiter='\t')}
inc = [l.strip() for l in open(R + '/work/included_cases.txt') if l.strip()]
sample = sorted(random.Random(424242).sample(inc, 40))
gene_dis = {g: [d for d in ds if d in clo] for g, ds in g2d.items()}
linked = [g for g in cand if gene_dis.get(g)]
ok = 0; maxd = 0.0
for cid in sample:
    terms = sorted({t for x in cases[cid]['observed'].split(';') if x for t in [mp(x)] if t})
    dscore = {}
    for g in linked:
        for d in gene_dis[g]:
            if d not in dscore:
                c = clo[d]
                dscore[d] = round(sum(max(IC.get(a, 0.0) for a in (anc(t) & c)) if anc(t) & c else 0.0 for t in terms) / len(terms), 9)
    gs = {g: max(dscore[d] for d in gene_dis[g]) for g in linked}
    target = cases[cid]['genes']
    t = gs.get(target, 0.0)
    allv = [gs.get(g, 0.0) for g in cand]
    gt = sum(1 for v in allv if v > t); k = sum(1 for v in allv if v == t) - 1
    rr = err(gt, k); d = abs(rr - float(per[cid]['rr'])); maxd = max(maxd, d)
    ok += int(d < 1e-9 and gt == int(per[cid]['n_greater']) and k == int(per[cid]['n_ties']))
print('METHOD naive check: %d/%d sampled cases identical (n_greater, n_ties, rr); max |rr diff| %.2e' % (ok, len(sample), maxd))
# ---- LIRICAL naive gene ranks on 3 seeded chunks
e2h_full = {}
for r in csv.DictReader(open(DD + '/hgnc_complete_set.txt', encoding='utf-8'), delimiter='\t'):
    if r.get('entrez_id'):
        e2h_full[r['entrez_id'].strip()] = r['hgnc_id']
d2g = collections.defaultdict(set)
for line in open(DD + '/mim2gene_medgen', encoding='utf-8'):
    if line.startswith('#'):
        continue
    f = line.rstrip('\n').split('\t')
    if len(f) >= 3 and f[2] == 'phenotype' and f[1].isdigit() and e2h_full.get(f[1]) in cs:
        d2g['OMIM:' + f[0]].add(e2h_full[f[1]])
h2h = {r['case_id']: r for r in csv.DictReader(open(O + '/h2h/h2h_percase.tsv', encoding='utf-8'), delimiter='\t')}
chunks = sorted(random.Random(4242).sample(sorted(x[:-7] for x in os.listdir(O + '/lirical') if x.endswith('.csv.gz')), 3))
okL = nL = 0; maxL = 0.0
for ch in chunks:
    sc = collections.defaultdict(dict)
    with gzip.open(O + '/lirical/' + ch + '.csv.gz', 'rt', encoding='utf-8') as fh:
        for row in csv.DictReader(fh):
            c = row['phenopacket'][:-5]; p = float(row['post_test_proba'])
            if p > sc[c].get(row['disease_id'], -1):
                sc[c][row['disease_id']] = p
    for c, ds in sc.items():
        gscore = collections.defaultdict(float)
        for d, p in ds.items():
            for g in d2g.get(d, ()):
                gscore[g] = max(gscore[g], p)
        t = gscore.get(cases[c]['genes'], 0.0)
        allv = [gscore.get(g, 0.0) for g in cand]
        gt = sum(1 for v in allv if v > t); k = sum(1 for v in allv if v == t) - 1
        rr = err(gt, k); d = abs(rr - float(h2h[c]['rr_L'])); maxL = max(maxL, d); nL += 1
        okL += int(d < 1e-9)
print('LIRICAL naive check: chunks %s: %d/%d cases identical rr_L; max |diff| %.2e' % (chunks, okL, nL, maxL))
# ---- plain means
rows = list(h2h.values()); n = len(rows)
m = lambda k: sum(float(r[k]) for r in rows) / n
print('PLAIN MEANS n=%d: MRR method %.6f LIRICAL %.6f ratio %.6f; top1 method %.6f LIRICAL %.6f; top10 %.6f %.6f' % (
    n, m('rr_M'), m('rr_L'), m('rr_M') / m('rr_L'), m('top1_M'), m('top1_L'), m('top10_M'), m('top10_L')))
print('cases in h2h == included list:', sorted(h2h) == sorted(inc), '| percase method cases == included:', sorted(per) == sorted(inc))
