"""Score LIRICAL 2.4.1 benchmark outputs (PREREG.md of run 2026-11-11-1032).

Gene level (primary): candidate space = run 1's 19,274 HGNC protein-coding genes; gene score = max post_test_proba
over the output's OMIM diseases linked to the gene by mim2gene_medgen (type "phenotype", numeric GeneID) mapped
NCBIGene -> HGNC with hgnc_complete_set 2026-06-05; unlinked genes score 0. Expected rank under uniform random
tie-breaking among exactly equal scores. Disease level (secondary): candidate space = OMIM diseases of the case's
condition-C output; causal = LIRICAL's is_causal rows.

usage:
  python -I score_lirical.py score <outdir> <groupdir> <run1_work> <hgnc_pc> <hgnc_full> <mim2gene> <resultdir>
  python -I score_lirical.py dev <csv(.gz)> <run1_work> <hgnc_pc> <hgnc_full> <mim2gene>
"""
import sys, csv, gzip, io, os, json, random, collections
import numpy as np
from scipy.special import digamma

EULER = 0.57721566490153286
SEED = 20261111


def rank_stats(g, k):
    g = np.asarray(g, dtype=np.float64); k = np.asarray(k, dtype=np.float64)
    H = lambda n: digamma(n + 1.0) + EULER
    rr = (H(g + k + 1.0) - H(g)) / (k + 1.0)
    top1 = np.where(g == 0, 1.0 / (k + 1.0), 0.0)
    top10 = np.where(g >= 10, 0.0, np.minimum(k + 1.0, 10.0 - g) / (k + 1.0))
    return rr, top1, top10


def load_candidates(path, cutoff='2026-06-09'):
    cand = []
    with open(path, encoding='utf-8') as fh:
        for row in csv.DictReader(fh, delimiter='\t'):
            if row['status'] != 'Approved' or row['locus_group'] != 'protein-coding gene':
                continue
            if row['date_approved_reserved'] and row['date_approved_reserved'] > cutoff:
                continue
            cand.append(row['hgnc_id'])
    return cand


def load_entrez2hgnc(path):
    e2h = {}
    with open(path, encoding='utf-8') as fh:
        for row in csv.DictReader(fh, delimiter='\t'):
            if row.get('entrez_id'):
                e2h[row['entrez_id'].strip()] = row['hgnc_id']
    return e2h


def load_mim2gene(path, e2h, cand_index):
    d2g = collections.defaultdict(set)
    with open(path, encoding='utf-8') as fh:
        for line in fh:
            if line.startswith('#'):
                continue
            f = line.rstrip('\n').split('\t')
            if len(f) < 3 or f[2] != 'phenotype' or not f[1].isdigit():
                continue
            h = e2h.get(f[1])
            if h is not None and h in cand_index:
                d2g['OMIM:' + f[0]].add(cand_index[h])
    return d2g


def read_output(path):
    """-> {case_id: (dict disease->score, set causal diseases)}"""
    op = gzip.open if path.endswith('.gz') else open
    res = {}
    with op(path, 'rt', encoding='utf-8', newline='') as fh:
        for row in csv.DictReader(fh):
            cid = row['phenopacket'][:-5] if row['phenopacket'].endswith('.json') else row['phenopacket']
            sc, causal = res.setdefault(cid, ({}, set()))
            d = row['disease_id']; p = float(row['post_test_proba'])
            if d not in sc or p > sc[d]:
                sc[d] = p
            if row['is_causal'].strip().lower() == 'true':
                causal.add(d)
    return res


def gene_counts(scores, d2g, ncand, target):
    arr = np.zeros(ncand)
    for d, p in scores.items():
        for gi in d2g.get(d, ()):
            if p > arr[gi]:
                arr[gi] = p
    t = arr[target] if target >= 0 else 0.0
    gt = int((arr > t).sum())
    eq = int((arr == t).sum()) - (1 if target >= 0 else 0)
    return t, gt, eq


def disease_counts(scores, space, causal):
    t = max([scores.get(d, 0.0) for d in causal] or [0.0])
    vals = np.array([scores.get(d, 0.0) for d in space])
    gt = int((vals > t).sum())
    eq = int((vals == t).sum())
    if any(d in space for d in causal):
        eq -= 1  # the target itself is in the space
    return t, gt, eq


def setup(run1_work, hgnc_pc, hgnc_full, mim2gene):
    cand = load_candidates(hgnc_pc)
    cidx = {h: i for i, h in enumerate(cand)}
    e2h = load_entrez2hgnc(hgnc_full)
    d2g = load_mim2gene(mim2gene, e2h, cidx)
    gene = {}; pmid = {}
    with open(os.path.join(run1_work, 'C_percase.tsv'), encoding='utf-8') as fh:
        for r in csv.DictReader(fh, delimiter='\t'):
            gene[r['case_id']] = r['gene']; pmid[r['case_id']] = r['pmid']
    return cand, cidx, d2g, gene, pmid


def boot(vals_fn, n, clusters, B=2000, seed=SEED):
    rng = np.random.default_rng(seed)
    out_case = []
    for _ in range(B):
        idx = rng.integers(0, n, n)
        out_case.append(vals_fn(idx))
    uc = sorted(set(clusters)); members = collections.defaultdict(list)
    for i, c in enumerate(clusters):
        members[c].append(i)
    rng2 = np.random.default_rng(seed + 1)
    out_cl = []
    for _ in range(B):
        pick = rng2.integers(0, len(uc), len(uc))
        idx = np.concatenate([members[uc[j]] for j in pick])
        out_cl.append(vals_fn(idx))
    ci = lambda a: [float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5))]
    out_case = np.array(out_case); out_cl = np.array(out_cl)
    return [ci(out_case[:, j]) for j in range(out_case.shape[1])], [ci(out_cl[:, j]) for j in range(out_cl.shape[1])]


def main_dev(csvp, run1_work, hgnc_pc, hgnc_full, mim2gene):
    cand, cidx, d2g, gene, pmid = setup(run1_work, hgnc_pc, hgnc_full, mim2gene)
    print('candidates', len(cand), 'diseases linked to candidate genes', len(d2g))
    res = read_output(csvp)
    for cid, (sc, causal) in sorted(res.items()):
        tg = cidx.get(gene.get(cid), -1)
        t, gt, eq = gene_counts(sc, d2g, len(cand), tg)
        rr, t1, t10 = rank_stats([gt], [eq])
        ts, dg, de = disease_counts(sc, list(sc), causal)
        drr, _, _ = rank_stats([dg], [de])
        print(cid[:45], gene.get(cid), 'gene_score', round(t, 6), 'n_gt', gt, 'ties', eq, 'rr', round(float(rr[0]), 4),
              '| causal', sorted(causal), 'dis_rr', round(float(drr[0]), 4), 'ndis', len(sc))


def main_score(outdir, groupdir, run1_work, hgnc_pc, hgnc_full, mim2gene, resdir):
    cand, cidx, d2g, gene, pmid = setup(run1_work, hgnc_pc, hgnc_full, mim2gene)
    os.makedirs(resdir, exist_ok=True)
    order = [l.strip() for l in open(os.path.join(groupdir, 'group_order.txt')) if l.strip()]
    sample = [l.strip() for l in open(os.path.join(groupdir, 'sample500.txt')) if l.strip()]
    base = {}
    with open(os.path.join(run1_work, 'PRE_percase.tsv'), encoding='utf-8') as fh:
        for r in csv.DictReader(fh, delimiter='\t'):
            base[r['case_id']] = r
    rows = []; missing_groups = []; dropped = []; no_entrez = 0
    for g in order:
        members = [l.strip() for l in open(os.path.join(groupdir, f'group_{g}.txt')) if l.strip()]
        pc, pp = os.path.join(outdir, f'{g}_C.csv.gz'), os.path.join(outdir, f'{g}_PRE.csv.gz')
        done = all(os.path.exists(p) and os.path.exists(p[:-7] + '.log.summary') and
                   'rc=0 ' in open(p[:-7] + '.log.summary').read() for p in (pc, pp))
        if not done:  # a group counts only when both JVMs finished (rc=0); partial or running files are never read
            missing_groups.append((g, len(members))); continue
        rc, rp = read_output(pc), read_output(pp)
        for cid in members:
            if cid not in rc or cid not in rp:
                dropped.append(cid); continue
            tg = cidx.get(gene[cid], -1)
            if tg < 0:
                no_entrez += 1
            scC, causalC = rc[cid]; scP, causalP = rp[cid]
            space = list(scC)
            out = {'case_id': cid, 'pmid': pmid[cid], 'pre_release': g, 'gene': gene[cid]}
            for lab, sc, causal in (('C', scC, causalC), ('PRE', scP, causalC | causalP)):
                t, gt, eq = gene_counts(sc, d2g, len(cand), tg)
                rr, t1, t10 = rank_stats([gt], [eq])
                out.update({f'gscore_{lab}': t, f'g_ngt_{lab}': gt, f'g_ties_{lab}': eq, f'rr_{lab}': float(rr[0]),
                            f'top1_{lab}': float(t1[0]), f'top10_{lab}': float(t10[0])})
                ts, dg, de = disease_counts(sc, space, causal)
                drr, dt1, _ = rank_stats([dg], [de])
                out.update({f'drr_{lab}': float(drr[0]), f'dtop1_{lab}': float(dt1[0]), f'dscore_{lab}': ts,
                            f'n_dis_{lab}': len(sc)})
            out['n_causal_dis'] = len(causalC)
            out['base_rr_C'] = float(base[cid]['rr_C']); out['base_rr_PRE'] = float(base[cid]['rr_PRE'])
            out['base_top1_C'] = float(base[cid]['top1_C']); out['base_top1_PRE'] = float(base[cid]['top1_PRE'])
            rows.append(out)
    keys = list(rows[0].keys())
    with open(os.path.join(resdir, 'percase.tsv'), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\t'.join(keys) + '\n')
        for r in rows:
            fh.write('\t'.join(f'{r[k]:.10g}' if isinstance(r[k], float) else str(r[k]) for k in keys) + '\n')
    n = len(rows)
    A = {k: np.array([r[k] for r in rows]) for k in keys if isinstance(rows[0][k], (float, int))}
    clusters = [r['pmid'] for r in rows]

    def stats(idx):
        mC, mP = A['rr_C'][idx].mean(), A['rr_PRE'][idx].mean()
        t1C, t1P = A['top1_C'][idx].mean(), A['top1_PRE'][idx].mean()
        return [mC, mP, mC - mP, (mC - mP) / mC, t1C, t1P, t1C - t1P,
                A['drr_C'][idx].mean(), A['drr_PRE'][idx].mean(), A['dtop1_C'][idx].mean(), A['dtop1_PRE'][idx].mean()]
    names = ['MRR_C', 'MRR_PRE', 'dMRR', 'share_dMRR', 'top1_C', 'top1_PRE', 'dTop1',
             'dis_MRR_C', 'dis_MRR_PRE', 'dis_top1_C', 'dis_top1_PRE']
    allidx = np.arange(n)
    point = stats(allidx)
    ci_case, ci_cl = boot(stats, n, clusters)
    summ = {'n_cases': n, 'n_pmids': len(set(clusters)), 'missing_groups': missing_groups, 'dropped_cases': dropped,
            'causal_gene_not_in_candidates_or_no_entrez': no_entrez,
            'top10_C': float(A['top10_C'].mean()), 'top10_PRE': float(A['top10_PRE'].mean()),
            'baseline_run1_MRR_C': float(A['base_rr_C'].mean()), 'baseline_run1_MRR_PRE': float(A['base_rr_PRE'].mean()),
            'baseline_run1_top1_C': float(A['base_top1_C'].mean()), 'baseline_run1_top1_PRE': float(A['base_top1_PRE'].mean())}
    for j, nm in enumerate(names):
        summ[nm] = {'point': float(point[j]), 'ci95_case': ci_case[j], 'ci95_pub_cluster': ci_cl[j]}
    # per-release-group breakdown (descriptive)
    grp = collections.defaultdict(list)
    for i, r in enumerate(rows):
        grp[r['pre_release']].append(i)
    summ['by_release'] = {g: {'n': len(ix), 'MRR_C': float(A['rr_C'][ix].mean()), 'MRR_PRE': float(A['rr_PRE'][ix].mean()),
                              'top1_C': float(A['top1_C'][ix].mean()), 'top1_PRE': float(A['top1_PRE'][ix].mean())}
                          for g, ix in sorted(grp.items())}
    # N-SF null: paired label swaps
    real = point[2]; d = A['rr_C'] - A['rr_PRE']; ctrl = []
    for k in range(400):
        rng = random.Random(SEED + k)
        s = np.array([(-1.0 if rng.random() < 0.5 else 1.0) for _ in range(n)])
        ctrl.append(float((s * d).mean()))
    summ['null_NSF'] = {'controls': 400, 'best_control': max(ctrl), 'real': float(real),
                        'real_beats_all_controls': bool(real > max(ctrl))}
    json.dump(summ, open(os.path.join(resdir, 'summary.json'), 'w'), indent=1)
    print(json.dumps(summ, indent=1))


if __name__ == '__main__':
    if sys.argv[1] == 'dev':
        main_dev(*sys.argv[2:7])
    else:
        main_score(*sys.argv[2:9])
