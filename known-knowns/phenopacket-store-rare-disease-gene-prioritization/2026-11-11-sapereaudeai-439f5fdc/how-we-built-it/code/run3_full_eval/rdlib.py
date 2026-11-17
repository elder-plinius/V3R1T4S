"""rdlib: pinned-corpus loader and Phenomizer-style Resnik baseline ranker (V3R1T4S run 2026-11-11-0916).

Everything follows PREREG.md of the run. Inputs are passed as paths; nothing is fetched here.
Ranker: s(P,D) = mean_{p in P} max_{a in anc(p) & closure(D)} IC(a)  (Koehler et al. 2009, asymmetric Resnik BMA)
Gene score = max over OMIM diseases linked to the gene (fixed map) with >= 1 annotation in the release.
Rank of causal gene under uniform random tie-breaking (scores rounded to 1e-9).
"""
import csv, re, datetime
import numpy as np
import scipy.sparse as sp
from scipy.special import digamma

ROOT = 'HP:0000118'
EULER = 0.5772156649015329


# ---------------------------------------------------------------- ontology
def load_obo(path):
    terms, alt, repl, obsolete, parents = set(), {}, {}, set(), {}
    cur = None
    with open(path, encoding='utf-8') as fh:
        for line in fh:
            line = line.rstrip('\n')
            if line == '[Term]':
                cur = {'is_a': []}; continue
            if line.startswith('[') and line.endswith(']'):
                cur = None; continue
            if cur is None or not line or ':' not in line:
                if cur is not None and not line and 'id' in cur:
                    _store(cur, terms, alt, repl, obsolete, parents); cur = None
                continue
            k, v = line.split(':', 1); v = v.strip()
            if k == 'id': cur['id'] = v
            elif k == 'alt_id': cur.setdefault('alt', []).append(v)
            elif k == 'is_a': cur['is_a'].append(v.split('!')[0].strip())
            elif k == 'is_obsolete' and v == 'true': cur['obs'] = True
            elif k == 'replaced_by': cur['repl'] = v
    if cur is not None and 'id' in cur:
        _store(cur, terms, alt, repl, obsolete, parents)
    return terms, alt, repl, obsolete, parents


def _store(cur, terms, alt, repl, obsolete, parents):
    i = cur['id']
    if not i.startswith('HP:'): return
    if cur.get('obs'):
        obsolete.add(i)
        if 'repl' in cur: repl[i] = cur['repl']
    else:
        terms.add(i); parents[i] = [p for p in cur['is_a'] if p.startswith('HP:')]
    for a in cur.get('alt', []): alt[a] = i


class Ontology:
    def __init__(self, obo_path):
        terms, alt, repl, obsolete, parents = load_obo(obo_path)
        self.alt, self.repl, self.obsolete, self.parents = alt, repl, obsolete, parents
        anc = {}
        def ancestors(t):
            if t in anc: return anc[t]
            s = {t}
            for p in parents.get(t, []):
                if p in parents: s |= ancestors(p)
            anc[t] = frozenset(s); return anc[t]
        import sys; sys.setrecursionlimit(100000)
        for t in terms: ancestors(t)
        self.T = sorted(t for t in terms if ROOT in anc[t])
        self.idx = {t: i for i, t in enumerate(self.T)}
        rows, cols = [], []
        for t in self.T:
            i = self.idx[t]
            for a in anc[t]:
                if a in self.idx: rows.append(i); cols.append(self.idx[a])
        self.ANC = sp.csr_matrix((np.ones(len(rows), dtype=np.int8), (rows, cols)), shape=(len(self.T), len(self.T)))
        self.ANC.sort_indices()

    def map_term(self, t, depth=0):
        """Map an HPO id to a current term index under HP:0000118, or None."""
        if t in self.idx: return self.idx[t]
        if t in self.alt and depth < 5: return self.map_term(self.alt[t], depth + 1)
        if t in self.repl and depth < 5: return self.map_term(self.repl[t], depth + 1)
        return None


# ---------------------------------------------------------------- annotations
def load_hpoa(path, onto, keep_refs=False):
    """Return dict disease -> set(term idx); and if keep_refs, dict (disease, term idx) -> set(refs) (union over rows)."""
    dis = {}
    refs = {} if keep_refs else None
    with open(path, encoding='utf-8') as fh:
        for line in fh:
            if line.startswith('#') or line.startswith('database_id') or line.startswith('DatabaseID'):
                continue
            f = line.rstrip('\n').split('\t')
            if len(f) < 11: continue
            if f[10] != 'P' or f[2] == 'NOT': continue
            ti = onto.map_term(f[3])
            if ti is None: continue
            dis.setdefault(f[0], set()).add(ti)
            if keep_refs:
                rs = refs.setdefault((f[0], ti), set())
                for r in f[4].split(';'):
                    r = r.strip()
                    if r: rs.add(r)
    return dis, refs


def closure_mask(term_idxs, onto):
    """Boolean vector over T: union of ancestors of the given term indices."""
    m = np.zeros(len(onto.T), dtype=bool)
    if term_idxs:
        sub = onto.ANC[sorted(term_idxs)]
        m[sub.indices] = True
    return m


def information_content(dis_terms, onto):
    n = np.zeros(len(onto.T), dtype=np.float64)
    for d, ts in dis_terms.items():
        n += closure_mask(ts, onto)
    N = len(dis_terms)
    with np.errstate(divide='ignore'):
        ic = -np.log(n / N)
    ic[n == 0] = 0.0  # never reached by any disease: cannot be a common ancestor anyway
    return ic, N


# ---------------------------------------------------------------- corpus and candidate space
def load_hgnc(path, cutoff='2026-06-09'):
    cand, entrez2hgnc = [], {}
    with open(path, encoding='utf-8') as fh:
        r = csv.DictReader(fh, delimiter='\t')
        for row in r:
            if row['status'] != 'Approved' or row['locus_group'] != 'protein-coding gene':
                continue
            if row['date_approved_reserved'] and row['date_approved_reserved'] > cutoff:
                continue
            cand.append(row['hgnc_id'])
            if row['entrez_id']:
                entrez2hgnc[row['entrez_id']] = row['hgnc_id']
    return cand, entrez2hgnc


def load_gene_disease(path, entrez2hgnc, types=('MENDELIAN',)):
    links = set()
    with open(path, encoding='utf-8') as fh:
        r = csv.DictReader(fh, delimiter='\t')
        for row in r:
            if not row['disease_id'].startswith('OMIM:') or row['association_type'] not in types:
                continue
            e = row['ncbi_gene_id'].replace('NCBIGene:', '')
            if e in entrez2hgnc:
                links.add((entrez2hgnc[e], row['disease_id']))
    return sorted(links)


def load_cases(cases_tsv, onto, cand_set):
    """Apply the PREREG inclusion rule. Returns included list of dicts and exclusion counts."""
    inc, exc = [], {'n_genes_not_1': 0, 'no_mappable_observed_term': 0, 'gene_not_in_candidate_space': 0}
    with open(cases_tsv, encoding='utf-8') as fh:
        for row in csv.DictReader(fh, delimiter='\t'):
            genes = [g for g in row['genes'].split(';') if g]
            if len(genes) != 1:
                exc['n_genes_not_1'] += 1; continue
            ts = sorted({ti for t in row['observed'].split(';') if t for ti in [onto.map_term(t)] if ti is not None})
            if not ts:
                exc['no_mappable_observed_term'] += 1; continue
            if genes[0] not in cand_set:
                exc['gene_not_in_candidate_space'] += 1; continue
            inc.append({'case_id': row['case_id'], 'pmid': row['pmids'].split(';')[0], 'gene': genes[0],
                        'terms': ts, 'n_raw_observed': len([t for t in row['observed'].split(';') if t]),
                        'diseases': row['diseases']})
    return inc, exc


# ---------------------------------------------------------------- scoring
class Scorer:
    """Holds the case-term structure; scores a release (or a modified disease) against all cases."""
    def __init__(self, cases, onto):
        self.onto = onto
        U = sorted({t for c in cases for t in c['terms']})
        self.U = np.array(U)
        uidx = {t: i for i, t in enumerate(U)}
        rows, cols, vals = [], [], []
        for ci, c in enumerate(cases):
            w = 1.0 / len(c['terms'])
            for t in c['terms']:
                rows.append(ci); cols.append(uidx[t]); vals.append(w)
        self.M = sp.csr_matrix((vals, (rows, cols)), shape=(len(cases), len(U)), dtype=np.float64)
        self.ANCU = onto.ANC[self.U]  # U x T, rows sorted indices
        self.ANCU.sort_indices()
        self.indptr0 = self.ANCU.indptr[:-1]

    def best_block(self, vals_TxB):
        """vals_TxB: T x B (IC * closure mask). Returns U x B: max over ancestors of each case term."""
        g = vals_TxB[self.ANCU.indices]
        return np.maximum.reduceat(g, self.indptr0, axis=0)

    def disease_scores(self, closures, ic, block=64):
        """closures: list of boolean masks over T (one per disease). Yields (start, cases x B float64 block)."""
        icf = ic.astype(np.float64)
        for s in range(0, len(closures), block):
            cl = np.stack(closures[s:s + block], axis=1)  # T x B
            b = self.best_block(icf[:, None] * cl)
            yield s, np.round(self.M @ b, 9)

    def disease_column(self, closure, ic):
        """Score vector (all cases) of one disease closure."""
        b = self.best_block((ic.astype(np.float64) * closure)[:, None])
        return np.round(self.M @ b, 9)[:, 0]


def compute_G(scorer, dis_list, closures, ic, links, gene_list):
    """G: cases x len(gene_list) float64, gene score = max over its linked diseases in dis_list; 0 if none.
    Returns G and by_gene (gene col -> list of disease positions in dis_list)."""
    dpos = {d: i for i, d in enumerate(dis_list)}
    gpos = {g: i for i, g in enumerate(gene_list)}
    by_dis, by_gene = {}, {}
    for g, d in links:
        if d in dpos and g in gpos:
            by_dis.setdefault(dpos[d], []).append(gpos[g]); by_gene.setdefault(gpos[g], []).append(dpos[d])
    G = np.zeros((scorer.M.shape[0], len(gene_list)), dtype=np.float64)
    for s, blk in scorer.disease_scores(closures, ic):
        for j in range(blk.shape[1]):
            for gi in by_dis.get(s + j, ()):
                np.maximum(G[:, gi], blk[:, j], out=G[:, gi])
    return G, by_gene


def rank_stats(n_greater, n_ties):
    """Expected reciprocal rank, P(rank=1), P(rank<=10) under uniform random tie-breaking.
    n_greater: genes strictly above the target; n_ties: other genes tied with it."""
    g = np.asarray(n_greater, dtype=np.float64); k = np.asarray(n_ties, dtype=np.float64)
    H = lambda n: digamma(n + 1.0) + EULER
    rr = (H(g + k + 1.0) - H(g)) / (k + 1.0)
    top1 = np.where(g == 0, 1.0 / (k + 1.0), 0.0)
    top10 = np.where(g >= 10, 0.0, np.minimum(k + 1.0, 10.0 - g) / (k + 1.0))
    return rr, top1, top10


def target_counts(G, tcol, n_unlinked):
    """G: cases x linked genes; tcol: column of the target gene in G or -1 if the target is unlinked (score 0).
    n_unlinked: number of candidate genes not in G (all score 0)."""
    n = G.shape[0]
    t = np.where(tcol >= 0, G[np.arange(n), np.maximum(tcol, 0)], 0.0)
    gt = (G > t[:, None]).sum(axis=1)
    eq = (G == t[:, None]).sum(axis=1) - (tcol >= 0)
    eq = eq + np.where(t == 0.0, n_unlinked - (tcol < 0), 0)
    return t, gt, eq


def parse_date(s):
    return datetime.date.fromisoformat(s)


def bootstrap_ci(x, n=2000, seed=20261111, clusters=None):
    """Percentile 95% CI of mean(x); x may be a 1-D array. If clusters given, resample clusters."""
    rng = np.random.default_rng(seed)
    x = np.asarray(x, dtype=np.float64)
    if clusters is None:
        idx = rng.integers(0, len(x), size=(n, len(x)))
        m = x[idx].mean(axis=1)
    else:
        cl = np.asarray(clusters)
        u, inv = np.unique(cl, return_inverse=True)
        sums = np.bincount(inv, weights=x, minlength=len(u)); cnt = np.bincount(inv, minlength=len(u))
        m = np.empty(n)
        for b in range(n):
            pick = rng.integers(0, len(u), size=len(u))
            m[b] = sums[pick].sum() / cnt[pick].sum()
    return float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


# ---------------------------------------------------------------- shared setup
W = "<WORKDIR>"  # PACKAGE EDIT: this line only; see code/README.md
RUN = W + '/runs/2026-11-11-0916'
HPO = W + '/cache/raredisease-run-2026-11-11-0916/hpo'
RELEASES = ['v2022-02-14', 'v2022-06-11', 'v2022-10-05', 'v2023-01-27', 'v2023-06-06', 'v2023-10-09', 'v2024-02-08',
            'v2024-06-25', 'v2024-12-12', 'v2025-05-06', 'v2025-10-22', 'v2026-02-16', 'v2026-06-06']
CONTEMP = 'v2026-06-06'


def setup(link_types=('MENDELIAN',)):
    onto = Ontology(HPO + '/v2026-06-06.hp.obo')
    cand, e2h = load_hgnc(RUN + '/data/hgnc_protein-coding_gene.txt')
    cand_set = set(cand)
    links = load_gene_disease(HPO + '/v2026-06-06.genes_to_disease.txt', e2h, link_types)
    cases, exc = load_cases(RUN + '/work/cases.tsv', onto, cand_set)
    gene_list = sorted({g for g, d in links if g in cand_set})
    gpos = {g: i for i, g in enumerate(gene_list)}
    tcol = np.array([gpos.get(c['gene'], -1) for c in cases])
    n_unlinked = len(cand) - len(gene_list)
    scorer = Scorer(cases, onto)
    return dict(onto=onto, cand=cand, e2h=e2h, links=links, cases=cases, exc=exc, gene_list=gene_list,
                tcol=tcol, n_unlinked=n_unlinked, scorer=scorer)


def release_eval(env, release, dis_terms=None):
    """Score every included case with one HPOA release. Returns dict with arrays t, gt, eq, rr, top1, top10 and G."""
    onto = env['onto']
    if dis_terms is None:
        dis_terms, _ = load_hpoa(HPO + '/%s.phenotype.hpoa' % release, onto)
    ic, N = information_content(dis_terms, onto)
    linked_dis = sorted({d for g, d in env['links']})
    dis_list = [d for d in linked_dis if d in dis_terms]
    closures = [closure_mask(dis_terms[d], onto) for d in dis_list]
    G, by_gene = compute_G(env['scorer'], dis_list, closures, ic, env['links'], env['gene_list'])
    del closures
    t, gt, eq = target_counts(G, env['tcol'], env['n_unlinked'])
    rr, top1, top10 = rank_stats(gt, eq)
    return dict(G=G, by_gene=by_gene, dis_list=dis_list, ic=ic, N=N, dis_terms=dis_terms,
                t=t, gt=gt, eq=eq, rr=rr, top1=top1, top10=top10)
