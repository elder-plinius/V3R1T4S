"""Standalone checker (Python standard library only), written from the success criterion of the V3R1T4S bank target
proteingym-cancer-dms-zero-shot:

  "a saved score file assigning one real-valued fitness prediction to every mutant in the ProteinGym reference CSV for a
  chosen cancer-gene DMS assay ... such that the Spearman correlation, recomputed by the skeptic with the official
  ProteinGym scoring convention (same mutant set, same direction convention, same NaN handling), is STRICTLY HIGHER
  ... than the maximum over all model columns for that assay in the live DMS-level Spearman CSV ... by at least 0.015
  absolute."

It checks the object's sha256, downloads the official ProteinGym v1.3 reference zip once (43 MB, verified by sha256;
cached in DATA_DIR, default ./data), checks the mutant sets are identical, recomputes Spearman (average ranks for ties),
and compares with the table value recorded in INDEX.csv. Optional: TABLE_CSV=<path to a fresh copy of the live table>
re-reads the bar from that file instead. Exit 0 and a last line PASS iff all checks hold.
"""
import csv, hashlib, io, math, os, sys, urllib.request, zipfile

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSAY = 'PTEN_HUMAN_Matreyek_2021'
OBJ = os.path.join(HERE, 'object', ASSAY + '.M1.csv')
ZIP_URL = 'https://marks.hms.harvard.edu/proteingym/ProteinGym_v1.3/DMS_ProteinGym_substitutions.zip'
ZIP_SHA = '3a83766254ac9ac9984ec25cb73c6e010ea4418f5e35f143933e6b6e6473b921'
REF_SHA = '1c52aba95950c6d3b1ac8320df4cb99a79ae97353bd43e24c87ef78dbb02e636'
META = {'DMS ID', 'Number of Mutants', 'Selection Type', 'UniProt ID', 'MSA_Neff_L_category', 'Taxon'}

def sha(b): return hashlib.sha256(b).hexdigest()

def ranks(v):
    order = sorted(range(len(v)), key=lambda i: v[i]); r = [0.0] * len(v); i = 0
    while i < len(v):
        j = i
        while j + 1 < len(v) and v[order[j + 1]] == v[order[i]]: j += 1
        for k in range(i, j + 1): r[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return r

def pearson(a, b):
    n = len(a); ma = sum(a) / n; mb = sum(b) / n
    sab = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    return sab / math.sqrt(sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b))

def main():
    ok = True
    index = list(csv.DictReader(open(os.path.join(HERE, 'INDEX.csv'), newline='')))[0]
    obj = open(OBJ, 'rb').read()
    print('object sha256', sha(obj), 'matches INDEX.csv' if sha(obj) == index['sha256'] else 'MISMATCH')
    ok &= sha(obj) == index['sha256']
    data_dir = os.environ.get('DATA_DIR', os.path.join(os.getcwd(), 'data')); os.makedirs(data_dir, exist_ok=True)
    zp = os.path.join(data_dir, 'DMS_ProteinGym_substitutions.zip')
    if not os.path.exists(zp):
        req = urllib.request.Request(ZIP_URL, headers={'User-Agent': 'V3R1T4S-verify'})
        open(zp, 'wb').write(urllib.request.urlopen(req, timeout=600).read())
    zb = open(zp, 'rb').read()
    print('reference zip sha256', 'ok' if sha(zb) == ZIP_SHA else 'MISMATCH ' + sha(zb)); ok &= sha(zb) == ZIP_SHA
    z = zipfile.ZipFile(io.BytesIO(zb))
    name = [n for n in z.namelist() if n.endswith('/' + ASSAY + '.csv') or n == ASSAY + '.csv'][0]
    rb = z.read(name)
    print('reference file sha256', 'ok' if sha(rb) == REF_SHA else 'MISMATCH ' + sha(rb)); ok &= sha(rb) == REF_SHA
    ref = {r['mutant']: float(r['DMS_score']) for r in csv.DictReader(io.StringIO(rb.decode()))}
    pred = {r['mutant']: float(r['prediction']) for r in csv.DictReader(io.StringIO(obj.decode()))}
    same = set(ref) == set(pred) and len(pred) == len(ref) == len(obj.decode().strip().splitlines()) - 1
    print('mutants', len(ref), 'identical sets' if same else 'SETS DIFFER'); ok &= same
    finite = all(math.isfinite(v) for v in pred.values()); ok &= finite
    keys = sorted(ref)
    rho = pearson(ranks([ref[k] for k in keys]), ranks([pred[k] for k in keys]))
    bar = float(index['table_value'])
    tc = os.environ.get('TABLE_CSV')
    if tc:
        row = [r for r in csv.DictReader(open(tc, newline='')) if r['DMS ID'] == ASSAY][0]
        bar = max(float(v) for k, v in row.items() if k not in META and v not in ('', None))
        print('bar re-read from', tc)
    margin = rho - bar
    print(f'spearman {rho:.6f}  table max {bar:.3f}  margin {margin:+.6f}  (needs > 0 and >= 0.015)')
    ok &= margin >= 0.015 and rho > bar
    print('PASS' if ok else 'FAIL')
    sys.exit(0 if ok else 1)

if __name__ == '__main__':
    main()
