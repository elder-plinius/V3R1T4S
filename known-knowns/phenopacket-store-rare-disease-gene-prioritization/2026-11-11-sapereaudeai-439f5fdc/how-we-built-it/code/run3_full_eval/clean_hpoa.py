"""Build the cleaned HPOA used by BOTH tools (run 2026-11-11-1222, PREREG.md reading (a)).

Rule (fixed before any evaluation output):
  corpus PMIDs = every string PMID:<digits> appearing anywhere in any phenopacket JSON of the pinned
  phenopacket-store 0.1.27 all_phenopackets.zip (sha256 d0c70005...205a): metaData.externalReferences and any
  per-feature evidence reference alike, over ALL phenopackets of the release (not only included cases).
  An HPOA data row is DROPPED if ANY of its references (the ';'-separated tokens of the 'reference' column)
  is a corpus PMID ("drop if any"). Every other line (header comments, column header, other rows) is written
  byte-for-byte unchanged, in the original order. All aspects (P, I, C, M) and NOT rows are treated alike.
usage: python -I clean_hpoa.py <corpus_zip> <phenotype.hpoa v2026-06-06> <out.hpoa> <census.json>
"""
import sys, zipfile, re, hashlib, json, collections
zp, hp, out, cen = sys.argv[1:5]
zb = open(zp, 'rb').read()
assert hashlib.sha256(zb).hexdigest() == 'd0c70005bb09b87035087516252b6b539fbc0415be7c664b73c9cde7eedf205a'
hb = open(hp, 'rb').read()
assert hashlib.sha256(hb).hexdigest() == '9e10da9c4b92c2d58f65e2fbd005a8511b5bfde43dd4a026564c72cf2918fbb3'
pat = re.compile(rb'PMID:\s*(\d+)')
z = zipfile.ZipFile(zp)
all_pm, meta_pm, npk = set(), set(), 0
for name in z.namelist():
    if not name.endswith('.json'):
        continue
    raw = z.read(name)
    npk += 1
    for m in pat.findall(raw):
        all_pm.add('PMID:' + m.decode())
    d = json.loads(raw)
    for r in (d.get('metaData', {}) or {}).get('externalReferences', []) or []:
        i = (r.get('id') or '').replace(' ', '')
        if i.startswith('PMID:'):
            meta_pm.add(i)
lines = hb.decode('utf-8').split('\n')
kept, dropped = [], 0
nrows = 0
before_P = collections.defaultdict(set); after_P = collections.defaultdict(set)
before_any = set(); after_any = set()
drop_by_aspect = collections.Counter(); row_by_aspect = collections.Counter()
for ln in lines:
    if ln.startswith('#') or ln.startswith('database_id') or not ln.strip():
        kept.append(ln); continue
    f = ln.split('\t')
    nrows += 1
    refs = [r.strip().replace('PMID: ', 'PMID:') for r in f[4].split(';') if r.strip()]
    asp = f[10] if len(f) > 10 else '?'
    row_by_aspect[asp] += 1
    before_any.add(f[0])
    isP = (asp == 'P' and f[2] != 'NOT')
    if isP:
        before_P[f[0]].add(f[3])
    if any(r in all_pm for r in refs):
        dropped += 1; drop_by_aspect[asp] += 1
        continue
    kept.append(ln)
    after_any.add(f[0])
    if isP:
        after_P[f[0]].add(f[3])
ob = '\n'.join(kept).encode('utf-8')
open(out, 'wb').write(ob)
res = {
    'corpus_zip_sha256': hashlib.sha256(zb).hexdigest(), 'phenopackets_read': npk,
    'corpus_pmids_anywhere': len(all_pm), 'corpus_pmids_metaData_only': len(meta_pm),
    'metaData_pmids_not_in_anywhere_set': len(meta_pm - all_pm),
    'input_hpoa_sha256': hashlib.sha256(hb).hexdigest(), 'input_data_rows': nrows,
    'rows_dropped': dropped, 'rows_kept': nrows - dropped, 'rows_by_aspect': dict(row_by_aspect),
    'dropped_by_aspect': dict(drop_by_aspect),
    'diseases_with_any_row_before': len(before_any), 'diseases_with_any_row_after': len(after_any),
    'diseases_with_P_annotation_before': len(before_P), 'diseases_with_P_annotation_after': len(after_P),
    'diseases_left_with_no_P_annotation': sorted(set(before_P) - set(after_P)),
    'P_disease_term_pairs_before': sum(len(v) for v in before_P.values()),
    'P_disease_term_pairs_after': sum(len(v) for v in after_P.values()),
    'output_sha256': hashlib.sha256(ob).hexdigest(), 'output_bytes': len(ob),
}
n_omim_lost = sum(1 for d in res['diseases_left_with_no_P_annotation'] if d.startswith('OMIM:'))
res['n_diseases_left_with_no_P_annotation'] = len(res['diseases_left_with_no_P_annotation'])
res['n_OMIM_diseases_left_with_no_P_annotation'] = n_omim_lost
json.dump(res, open(cen, 'w'), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != 'diseases_left_with_no_P_annotation'}, indent=1))
