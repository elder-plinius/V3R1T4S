"""FROZEN METHOD (run 2026-11-11-1222): run 1's published Phenomizer-style asymmetric Resnik ranker (rdlib.py, byte-
identical to runs/2026-11-11-0916/attempts/evaluator-first/code/rdlib.py), no tuning, applied to the CLEANED HPOA.

Design (every choice, as in run 1; nothing tuned on evaluation cases):
- Ontology: HPO hp.obo v2026-06-06; terms under Phenotypic abnormality (HP:0000118); alt_id/replaced_by followed.
- Case profile: the phenopacket's OBSERVED HPO terms (excluded terms ignored), mapped to current ids; duplicates dropped.
- Disease profiles: phenotype-aspect (P) rows, qualifier not NOT, of the given HPOA (here the cleaned v2026-06-06);
  all databases (OMIM, ORPHA, DECIPHER) count for information content.
- Information content IC(t) = -log(n_t / N), n_t = diseases whose annotation closure contains t, N = diseases with >= 1
  P annotation, computed FROM THE GIVEN (CLEANED) HPOA.
- Disease score s(P, D) = mean over case terms p of max over common ancestors a of p and D's closure of IC(a)
  (Koehler et al. 2009, asymmetric best-match average), rounded to 1e-9.
- Gene score = max over the OMIM diseases linked to the gene by HPO genes_to_disease.txt v2026-06-06
  (association_type MENDELIAN, NCBIGene -> HGNC via the run-1 HGNC protein-coding file) that have >= 1 P annotation
  in the given HPOA; 0 if none.
- Candidate space: run 1's 19,274 HGNC approved protein-coding genes (approved on or before 2026-06-09).
- Rank of the causal gene: expected rank under uniform random tie-breaking among exactly equal scores:
  RR = E[1/rank], top1 = P(rank = 1), top10 = P(rank <= 10).
Outputs (outdir): percase.tsv; scores.npz (float64 gene-score matrix cases x linked genes, case order, gene order:
the full ranked list over the fixed candidate space, every unlisted candidate gene scores 0); top100.tsv.gz (the first
100 genes of every case's ranked list, ties in HGNC-id order for display only); run_info.json.
usage: python -I frozen_method.py <hp.obo> <hpoa> <genes_to_disease> <hgnc_pc> <cases.tsv> <caselist> <outdir>
"""
import sys, os, json, gzip, hashlib, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import rdlib as R


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def main(obo, hpoa, g2d, hgnc_pc, cases_tsv, caselist, outdir):
    t0 = time.time()
    os.makedirs(outdir, exist_ok=True)
    onto = R.Ontology(obo)
    cand, e2h = R.load_hgnc(hgnc_pc)
    cand_set = set(cand)
    links = R.load_gene_disease(g2d, e2h)
    allc, exc = R.load_cases(cases_tsv, onto, cand_set)
    want = [l.strip() for l in open(caselist, encoding='utf-8') if l.strip()]
    byid = {c['case_id']: c for c in allc}
    missing = [w for w in want if w not in byid]
    assert not missing, ('cases not in the included set', missing[:5])
    cases = [byid[w] for w in want]
    gene_list = sorted({g for g, d in links if g in cand_set})
    gpos = {g: i for i, g in enumerate(gene_list)}
    tcol = np.array([gpos.get(c['gene'], -1) for c in cases])
    n_unlinked = len(cand) - len(gene_list)
    scorer = R.Scorer(cases, onto)
    dis_terms, _ = R.load_hpoa(hpoa, onto)
    ic, N = R.information_content(dis_terms, onto)
    linked_dis = sorted({d for g, d in links})
    dis_list = [d for d in linked_dis if d in dis_terms]
    closures = [R.closure_mask(dis_terms[d], onto) for d in dis_list]
    G, _ = R.compute_G(scorer, dis_list, closures, ic, links, gene_list)
    del closures
    t, gt, eq = R.target_counts(G, tcol, n_unlinked)
    rr, top1, top10 = R.rank_stats(gt, eq)
    with open(os.path.join(outdir, 'percase.tsv'), 'w', newline='\n', encoding='utf-8') as fh:
        fh.write('case_id\tpmid\tgene\tn_terms\tgene_score\tn_greater\tn_ties\trr\ttop1\ttop10\n')
        for i, c in enumerate(cases):
            fh.write('%s\t%s\t%s\t%d\t%.9f\t%d\t%d\t%.10g\t%.10g\t%.10g\n' % (
                c['case_id'], c['pmid'], c['gene'], len(c['terms']), t[i], gt[i], eq[i], rr[i], top1[i], top10[i]))
    np.savez_compressed(os.path.join(outdir, 'scores.npz'), G=G, cases=np.array(want), genes=np.array(gene_list))
    with gzip.open(os.path.join(outdir, 'top100.tsv.gz'), 'wt', encoding='utf-8', newline='\n') as fh:
        fh.write('case_id\trank_position\thgnc_id\tgene_score\n')
        ga = np.array(gene_list)
        for i, c in enumerate(cases):
            o = np.lexsort((ga, -G[i]))[:100]
            for k, j in enumerate(o):
                fh.write('%s\t%d\t%s\t%.9f\n' % (c['case_id'], k + 1, ga[j], G[i, j]))
    info = {'n_cases': len(cases), 'candidate_space': len(cand), 'linked_candidate_genes': len(gene_list),
            'unlinked_candidate_genes': n_unlinked, 'annotated_diseases_N': int(N), 'scored_omim_diseases': len(dis_list),
            'cases_gene_unlinked_or_unannotated': int((t == 0).sum()),
            'MRR': float(rr.mean()), 'top1': float(top1.mean()), 'top10': float(top10.mean()),
            'inputs_sha256': {'obo': sha(obo), 'hpoa': sha(hpoa), 'g2d': sha(g2d), 'hgnc_pc': sha(hgnc_pc),
                              'cases_tsv': sha(cases_tsv), 'caselist': sha(caselist)},
            'code_sha256': {'frozen_method.py': sha(os.path.abspath(__file__)),
                            'rdlib.py': sha(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rdlib.py'))},
            'seconds': round(time.time() - t0, 1)}
    json.dump(info, open(os.path.join(outdir, 'run_info.json'), 'w'), indent=1)
    print(json.dumps(info, indent=1))


if __name__ == '__main__':
    main(*sys.argv[1:8])
