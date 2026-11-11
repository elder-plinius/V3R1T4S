"""Compare LIRICAL's single-case `phenopacket -f tsv` output with its `benchmark` CSV for the same case (dev case 1).
usage: python -I equivalence.py <single.tsv> <bench.csv> <case_id>"""
import sys, csv
st, bc, cid = sys.argv[1:4]
single = [l.rstrip('\n').split('\t') for l in open(st, encoding='utf-8') if not l.startswith('!') and l.strip()]
hdr = single[0]; rows = single[1:]
s_order = [r[hdr.index('diseaseCurie')] for r in rows]
s_pct = {r[hdr.index('diseaseCurie')]: r[hdr.index('posttestprob')] for r in rows}
b = [r for r in csv.DictReader(open(bc, encoding='utf-8')) if r['phenopacket'] == cid + '.json']
b_order = [r['disease_id'] for r in b]
bp = {r['disease_id']: float(r['post_test_proba']) for r in b}
print('diseases single', len(s_order), 'benchmark', len(b_order), 'same set', set(s_order) == set(b_order))
same_top = sum(1 for x, y in zip(s_order[:100], b_order[:100]) if x == y)
print('identical positions in top 100:', same_top)
bad = 0
for d in s_order[:100]:
    v = s_pct[d].rstrip('%')
    if abs(float(v) / 100 - bp[d]) > 1e-4 * max(1, 1):
        bad += 1
print('top-100 post-test probabilities differing by > 1e-4:', bad)
