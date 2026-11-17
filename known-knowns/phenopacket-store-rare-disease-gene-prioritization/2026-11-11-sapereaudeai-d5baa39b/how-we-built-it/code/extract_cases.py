"""Extract the run-1 temporal-subset phenopackets (and all included cases' file list) from the pinned corpus zip.
Usage: python -I extract_cases.py <corpus_zip> <run1_work_dir> <outdir>"""
import sys, zipfile, csv, os, hashlib
zp, w, out = sys.argv[1:4]
h = hashlib.sha256(open(zp, 'rb').read()).hexdigest()
assert h == 'd0c70005bb09b87035087516252b6b539fbc0415be7c664b73c9cde7eedf205a', h
cases = {r['case_id']: r for r in csv.DictReader(open(os.path.join(w, 'cases.tsv'), encoding='utf-8'), delimiter='\t')}
pre = list(csv.DictReader(open(os.path.join(w, 'PRE_percase.tsv'), encoding='utf-8'), delimiter='\t'))
z = zipfile.ZipFile(zp)
names = set(z.namelist())
n = 0
for r in pre:
    f = cases[r['case_id']]['file']
    assert f in names, f
    data = z.read(f)
    with open(os.path.join(out, r['case_id'] + '.json'), 'wb') as fh:
        fh.write(data)
    n += 1
print('extracted', n, 'phenopackets; corpus sha256 ok')
