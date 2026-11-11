"""Head-to-head scorer (run 2026-11-11-1222, PREREG.md): frozen method vs LIRICAL 2.4.1 on the same cases, same
candidate space (run 1's 19,274 HGNC protein-coding genes), same cleaned HPOA.

LIRICAL gene level (primary, unchanged from run 2's confirmed scorer score_lirical_run2.py): gene score = max
post_test_proba over the output's OMIM diseases linked to the gene by the data directory's mim2gene_medgen
('phenotype' rows) mapped NCBIGene -> HGNC with its hgnc_complete_set (2026-06-05); unlinked genes score 0.
LIRICAL gene level (secondary, sensitivity only, label L2): the same, with the frozen method's map (HPO
genes_to_disease v2026-06-06, MENDELIAN, OMIM).
Method: per-case rr/top1/top10 from frozen_method.py percase.tsv.
Expected rank under uniform random tie-breaking for both. Paired statistics on the cases present in both.
usage: python -I h2h_score.py <method_percase.tsv> <lirical_out_dir> <hgnc_pc> <hgnc_full> <mim2gene>
         <genes_to_disease> <caselist> <resultdir>
A LIRICAL output <x>.csv.gz is read only if <x>.log.summary exists and contains 'rc=0 '.
"""
import sys, os, csv, json, glob, random, collections
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import score_lirical_run2 as L

SEED = 20261111
B = 2000


def g2d_map(g2d, hgnc_pc, cidx):
    e2h = {}
    for r in csv.DictReader(open(hgnc_pc, encoding='utf-8'), delimiter='\t'):
        if r['status'] == 'Approved' and r['locus_group'] == 'protein-coding gene' and r['entrez_id']:
            e2h[r['entrez_id']] = r['hgnc_id']
    d2g = collections.defaultdict(set)
    for r in csv.DictReader(open(g2d, encoding='utf-8'), delimiter='\t'):
        if r['disease_id'].startswith('OMIM:') and r['association_type'] == 'MENDELIAN':
            h = e2h.get(r['ncbi_gene_id'].replace('NCBIGene:', ''))
            if h in cidx:
                d2g[r['disease_id']].add(cidx[h])
    return d2g


def case_row(c, m, sc, cand, cidx, d2g_L, d2g_M):
    tg = cidx.get(m['gene'], -1)
    out = {'case_id': c, 'pmid': m['pmid'], 'gene': m['gene'], 'n_terms': int(m['n_terms']),
           'gscore_M': float(m['gene_score']),
           'rr_M': float(m['rr']), 'top1_M': float(m['top1']), 'top10_M': float(m['top10'])}
    for lab, d2g in (('L', d2g_L), ('L2', d2g_M)):
        t, gt, eq = L.gene_counts(sc, d2g, len(cand), tg)
        rr, t1, t10 = L.rank_stats([gt], [eq])
        out.update({f'gscore_{lab}': float(t), f'ngt_{lab}': gt, f'ties_{lab}': eq, f'rr_{lab}': float(rr[0]),
                    f'top1_{lab}': float(t1[0]), f'top10_{lab}': float(t10[0])})
    return out


def main(mper, ldir, hgnc_pc, hgnc_full, m2g, g2d, caselist, resdir):
    os.makedirs(resdir, exist_ok=True)
    cand = L.load_candidates(hgnc_pc)
    cidx = {h: i for i, h in enumerate(cand)}
    d2g_L = L.load_mim2gene(m2g, L.load_entrez2hgnc(hgnc_full), cidx)
    d2g_M = g2d_map(g2d, hgnc_pc, cidx)
    want = [l.strip() for l in open(caselist, encoding='utf-8') if l.strip()]
    M = {r['case_id']: r for r in csv.DictReader(open(mper, encoding='utf-8'), delimiter='\t')}
    # streamed per output file (PREREG.v2: memory only; same statistics): each LIRICAL output is reduced to per-case
    # gene-level rows at once and its disease scores are discarded.
    wantset = set(want)
    chunks_ok, chunks_bad = [], []
    per = {}
    for p in sorted(glob.glob(os.path.join(ldir, '*.csv.gz'))):
        sm = p[:-7] + '.log.summary'
        if not (os.path.exists(sm) and 'rc=0 ' in open(sm).read()):
            chunks_bad.append(os.path.basename(p)); continue
        chunks_ok.append(os.path.basename(p))
        for c, (sc, causal) in L.read_output(p).items():
            if c in wantset and c in M:
                per[c] = case_row(c, M[c], sc, cand, cidx, d2g_L, d2g_M)
    rows, dropped = [], []
    for c in want:
        if c not in per:
            dropped.append(c); continue
        rows.append(per[c])
    del per
    keys = list(rows[0].keys())
    with open(os.path.join(resdir, 'h2h_percase.tsv'), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\t'.join(keys) + '\n')
        for r in rows:
            fh.write('\t'.join(f'{r[k]:.10g}' if isinstance(r[k], float) else str(r[k]) for k in keys) + '\n')
    n = len(rows)
    A = {k: np.array([r[k] for r in rows], dtype=float) for k in keys if isinstance(rows[0][k], (int, float))}
    pm = np.array([r['pmid'] for r in rows])

    def stats(ix, ref='L'):
        mM, mR = A['rr_M'][ix].mean(), A['rr_' + ref][ix].mean()
        tM, tR = A['top1_M'][ix].mean(), A['top1_' + ref][ix].mean()
        kM, kR = A['top10_M'][ix].mean(), A['top10_' + ref][ix].mean()
        return np.array([mM, mR, mM - mR, mM / mR if mR > 0 else np.inf, tM, tR, tM - tR, kM, kR, kM - kR])
    names = ['MRR_method', 'MRR_lirical', 'dMRR', 'MRR_ratio', 'top1_method', 'top1_lirical', 'dTop1',
             'top10_method', 'top10_lirical', 'dTop10']
    summ = {'n_cases': n, 'n_pmids': int(len(set(pm))), 'dropped_cases': dropped, 'lirical_chunks_ok': chunks_ok,
            'lirical_chunks_not_ok': chunks_bad}
    u = sorted(set(pm)); mem = collections.defaultdict(list)
    for i, c in enumerate(pm):
        mem[c].append(i)
    for ref in ('L', 'L2'):
        pt = stats(np.arange(n), ref)
        rng = np.random.default_rng(SEED)
        bc = np.array([stats(rng.integers(0, n, n), ref) for _ in range(B)])
        rng2 = np.random.default_rng(SEED + 1)
        bp = np.array([stats(np.concatenate([mem[u[j]] for j in rng2.integers(0, len(u), len(u))]), ref)
                       for _ in range(B)])
        ci = lambda a: [float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5))]
        block = {nm: {'point': float(pt[j]), 'ci95_case_paired': ci(bc[:, j]), 'ci95_pub_cluster': ci(bp[:, j])}
                 for j, nm in enumerate(names)}
        gate = {
            'MRR_ratio_point_ge_1.10': bool(pt[3] >= 1.10),
            'top1_point_strictly_greater': bool(pt[6] > 0),
            'dMRR_case_ci_lower_gt_0': bool(block['dMRR']['ci95_case_paired'][0] > 0),
            'dTop1_case_ci_lower_gt_0': bool(block['dTop1']['ci95_case_paired'][0] > 0),
        }
        gate['GATE_literal_reading_met'] = all(gate.values())
        gate['info_strict_ratio_ci_lower_ge_1.10'] = bool(block['MRR_ratio']['ci95_case_paired'][0] >= 1.10)
        gate['info_top1_ratio_point'] = float(pt[4] / pt[5]) if pt[5] > 0 else None
        gate['info_bootstrap_fraction_meeting_point_gate'] = float(np.mean((bc[:, 3] >= 1.10) & (bc[:, 6] > 0)))
        d = A['rr_M'] - A['rr_' + ref]; real = float(d.mean()); ctrl = []
        for k in range(400):
            r = random.Random(SEED + k)
            s = np.array([(-1.0 if r.random() < 0.5 else 1.0) for _ in range(n)])
            ctrl.append(float((s * d).mean()))
        summ['vs_' + ref] = {'stats': block, 'gate': gate,
                             'null_NSF_dMRR': {'controls': 400, 'best_control': max(ctrl), 'real': real,
                                               'real_beats_all_controls': bool(real > max(ctrl))}}
    strata = {'le3_terms': A['n_terms'] <= 3, 'gt3_terms': A['n_terms'] > 3,
              'method_gene_score_0': A['gscore_M'] == 0, 'method_gene_score_pos': A['gscore_M'] > 0,
              'lirical_gene_score_0': A['gscore_L'] == 0}
    summ['strata_vs_L'] = {k: {'n': int(v.sum()),
                               'MRR_method': float(A['rr_M'][v].mean()) if v.any() else None,
                               'MRR_lirical': float(A['rr_L'][v].mean()) if v.any() else None,
                               'top1_method': float(A['top1_M'][v].mean()) if v.any() else None,
                               'top1_lirical': float(A['top1_L'][v].mean()) if v.any() else None}
                           for k, v in strata.items()}
    json.dump(summ, open(os.path.join(resdir, 'h2h_summary.json'), 'w'), indent=1)
    print(json.dumps(summ, indent=1))


if __name__ == '__main__':
    main(*sys.argv[1:9])
