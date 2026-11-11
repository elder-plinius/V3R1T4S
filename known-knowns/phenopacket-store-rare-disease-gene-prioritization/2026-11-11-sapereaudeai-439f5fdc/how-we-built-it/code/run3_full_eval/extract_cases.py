"""Extract the phenopackets of a case list from the pinned corpus zip (sha256-checked) as <case_id>.json.
usage: python -I extract_cases.py <corpus_zip> <run1_cases.tsv> <caselist> <outdir>"""
import sys, zipfile, csv, os, hashlib
zp, ctsv, lst, out = sys.argv[1:5]
assert hashlib.sha256(open(zp, 'rb').read()).hexdigest() == 'd0c70005bb09b87035087516252b6b539fbc0415be7c664b73c9cde7eedf205a'
files = {r['case_id']: r['file'] for r in csv.DictReader(open(ctsv, encoding='utf-8'), delimiter='\t')}
z = zipfile.ZipFile(zp)
os.makedirs(out, exist_ok=True)
n = 0
for c in (l.strip() for l in open(lst, encoding='utf-8')):
    if not c: continue
    open(os.path.join(out, c + '.json'), 'wb').write(z.read(files[c])); n += 1
print('extracted', n, 'phenopackets; corpus sha256 ok')
