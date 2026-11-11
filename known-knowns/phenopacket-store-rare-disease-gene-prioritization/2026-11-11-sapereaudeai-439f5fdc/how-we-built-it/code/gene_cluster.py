"""POST HOC, descriptive only (not in PREREG, not a gate): gene-cluster bootstrap of the p1 subset, because the audit
showed the net advantage concentrated in a few publications. Usage: python -I gene_cluster.py <p1_subset_cases.tsv>"""
import collections, csv, sys
import numpy as np
rows = list(csv.DictReader(open(sys.argv[1], encoding='utf-8'), delimiter='\t'))
M = np.array([float(r['rr_M']) for r in rows]); L = np.array([float(r['rr_L']) for r in rows])
for key in ('gene', 'pmid'):
    mem = collections.defaultdict(list)
    for i, r in enumerate(rows): mem[r[key]].append(i)
    u = sorted(mem); rng = np.random.default_rng(20261113); rat = []; dif = []
    for _ in range(2000):
        ix = np.concatenate([mem[u[j]] for j in rng.integers(0, len(u), len(u))])
        rat.append(M[ix].mean() / L[ix].mean()); dif.append(M[ix].mean() - L[ix].mean())
    print('%s clusters %d: dMRR 95%% [%.4f, %.4f]; ratio 95%% [%.4f, %.4f]; P(ratio>=1.10) %.3f' % (key, len(u),
          np.percentile(dif, 2.5), np.percentile(dif, 97.5), np.percentile(rat, 2.5), np.percentile(rat, 97.5), np.mean(np.array(rat) >= 1.10)))
g = collections.defaultdict(lambda: [0, 0.0])
for r in rows: g[r['gene']][0] += 1; g[r['gene']][1] += float(r['rr_M']) - float(r['rr_L'])
top = sorted(g.items(), key=lambda kv: -kv[1][1])[:5]
print('genes in subset %d; top 5 gene contributions (cases, sum dRR): %s; total %.3f' % (len(g), [(k, v[0], round(v[1], 3)) for k, v in top], sum(v[1] for v in g.values())))
