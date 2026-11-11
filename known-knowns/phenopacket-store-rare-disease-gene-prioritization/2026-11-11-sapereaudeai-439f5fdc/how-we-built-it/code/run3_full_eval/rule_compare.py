"""Descriptive: rows dropped under 'drop if any reference is a corpus PMID' (chosen) vs 'drop only if all are'.
Also counts rows by reference type kept after cleaning. Resource census only (reads no tool output).
usage: python -I rule_compare.py <corpus_zip> <orig.hpoa> <clean.hpoa>"""
import sys, zipfile, re, collections
zp, orig, clean = sys.argv[1:4]
pat = re.compile(rb'PMID:\s*(\d+)')
z = zipfile.ZipFile(zp); pm = set()
for n in z.namelist():
    if n.endswith('.json'):
        pm |= {'PMID:' + m.decode() for m in pat.findall(z.read(n))}
anyd = alld = multi = 0; kept_types = collections.Counter(); n = 0
for ln in open(orig, encoding='utf-8'):
    if ln.startswith('#') or ln.startswith('database_id') or not ln.strip(): continue
    f = ln.rstrip('\n').split('\t'); n += 1
    refs = [r.strip().replace('PMID: ', 'PMID:') for r in f[4].split(';') if r.strip()]
    hits = [r in pm for r in refs]
    if len(refs) > 1: multi += 1
    if any(hits): anyd += 1
    if hits and all(hits): alld += 1
    if not any(hits):
        kept_types[tuple(sorted({r.split(':')[0] for r in refs}))] += 1
print('rows', n, 'rows_with_multiple_references', multi)
print('drop_if_any', anyd, 'drop_if_all', alld, 'difference', anyd - alld)
print('kept rows by reference-type set (top 8):', kept_types.most_common(8))
