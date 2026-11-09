"""Standalone checker (Python standard library only) for partial win p1 of the V3R1T4S bank target
proteingym-cancer-dms-zero-shot:

  "Beat the live per-assay best by >= 0.015 Spearman on at least three cancer-gene assays simultaneously with ONE method
  and ONE frozen configuration (pre-registered, fitted only on non-cancer assays)."

For each of the 13 pre-registered cancer-gene assays it checks the prediction file's sha256, the mutant set against the
official ProteinGym v1.3 reference file (zip downloaded once, 43 MB, sha256-verified, cached in DATA_DIR, default ./data),
recomputes Spearman (average ranks), and compares with the table maximum recorded below (fetched 2026-10-18T20:50:39Z).
TABLE_CSV=<fresh copy of the live table> re-reads the bars from that file instead. PASS iff at least 3 assays clear +0.015.
"""
import csv, hashlib, io, math, os, sys, urllib.request, zipfile

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZIP_URL = 'https://marks.hms.harvard.edu/proteingym/ProteinGym_v1.3/DMS_ProteinGym_substitutions.zip'
ZIP_SHA = '3a83766254ac9ac9984ec25cb73c6e010ea4418f5e35f143933e6b6e6473b921'
META = {'DMS ID', 'Number of Mutants', 'Selection Type', 'UniProt ID', 'MSA_Neff_L_category', 'Taxon'}
# assay: (sha256 of object/<assay>.M1.csv, table max 2026-10-18, sha256 of the official reference file)
ASSAYS = {
    'BRCA1_HUMAN_Findlay_2018': ('f4512818b17b6acb26547903e1e91de64adb5dd1f4133f547d454d95bfa71e4b', 0.56, 'abde5d47e84b1feeac6c32b60c1f3b5d2881accf3ceccfbadccceeea73e81c43'),
    'BRCA2_HUMAN_Erwood_2022_HEK293T': ('aae37b33c4ca26f6ce1c99d9eeafce8c0fe81ac187f2f56b6988d0d624e34ad6', 0.534, '4fc00cf38e89679c11266fa651644c61297a3ac5eb36320fba3a715d5b64f8f2'),
    'ERBB2_HUMAN_Elazar_2016': ('7101dc220436c823fe1ea9ca43a4ee5d8c6ddcc333f43b5d14ce38d7f7bd4ffb', 0.695, 'e1190b949da4835344be4069c98b336825a6975e2f0f169221772070007bec0d'),
    'MSH2_HUMAN_Jia_2020': ('faa2d0458469e03e5f1a3ef8e14f5531a5a0ac1fa727d61d570ac210f3e79536', 0.409, '00ac2d2b66ab786150025988ec8e9bb9570caa42ad5fcd0833a4eb5c0d1d58bc'),
    'P53_HUMAN_Giacomelli_2018_Null_Etoposide': ('98f04433fcc67a429fa7e230f96fbf446dfa8426421d67106e80f2661eca092b', 0.509, '4c7a24d5f9bf80f8e10afa9b0edb23f1301c497d1d2d096307f813a8ca7d3e0d'),
    'P53_HUMAN_Giacomelli_2018_Null_Nutlin': ('7468ac639ab3e9e87dbe434809a5af4df11fcee8474982d4968a7e367189be85', 0.523, 'cb68559e515c44aa3ba42a56085c011c739d41b83e1fd815c0a8b4d2cd0a0f29'),
    'P53_HUMAN_Giacomelli_2018_WT_Nutlin': ('a5473d16cf50ff35cdb7e4e86378e9b59e362a114e257a1600d920b4b1ad855c', 0.616, '5a91fd89e27be9b564168568b52f3daac06fabdbad9c8f86dc7a0d21c9c5ae67'),
    'P53_HUMAN_Kotler_2018': ('78b38b6d6163a2461b45c42b4a6c1531a07e405da8f51595a527ef5e21979264', 0.722, '0e6fd5232d1a6893fb310fea7d433b11dc6d1be708bc430b00075e27e9ecf886'),
    'PTEN_HUMAN_Matreyek_2021': ('1aecf9c14a0746b6b434b38acebfdfe8ddeefec98bedb322d6ea53b1ee7760db', 0.516, '1c52aba95950c6d3b1ac8320df4cb99a79ae97353bd43e24c87ef78dbb02e636'),
    'PTEN_HUMAN_Mighell_2018': ('498eb6c09c658b96a68cbd30ec8be33885f966dbb83765cfaccbd6444b7b7fdd', 0.561, 'd532bed24c80449936dd61cf303225d78e6e9963a58165c1c36dff92c89557e1'),
    'RASH_HUMAN_Bandaru_2017': ('33f14be64ce3916f9f0c9199ed157a71de1e8812c237eccb92a09f101f13bc05', 0.619, '0704164d427ab68cfb8ac72fcbe438a819ad91b31f9fa4fcb1056690173a0736'),
    'RASK_HUMAN_Weng_2022_abundance': ('5ff3157375f29d7e67e1a1cd5c5b20b71527c1ebea2f3be4abea90e1fbedea2f', 0.47, 'e0281932c577821ef127d5df1d4e3824e383e5af4ca5219cadfd7c757f6de722'),
    'RASK_HUMAN_Weng_2022_binding-DARPin_K55': ('dc9579d5dc42b77cbc676f8aa40c065aa5238c3416c0539cd5fd009982b6565a', 0.71, '081ea292571d20822447b65cee79839c04abc27915a0d2218aef9f217d2504ab'),
}

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
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / math.sqrt(sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b))

def main():
    ok = True
    data_dir = os.environ.get('DATA_DIR', os.path.join(os.getcwd(), 'data')); os.makedirs(data_dir, exist_ok=True)
    zp = os.path.join(data_dir, 'DMS_ProteinGym_substitutions.zip')
    if not os.path.exists(zp):
        req = urllib.request.Request(ZIP_URL, headers={'User-Agent': 'V3R1T4S-verify'})
        open(zp, 'wb').write(urllib.request.urlopen(req, timeout=600).read())
    zb = open(zp, 'rb').read()
    print('reference zip sha256', 'ok' if sha(zb) == ZIP_SHA else 'MISMATCH'); ok &= sha(zb) == ZIP_SHA
    z = zipfile.ZipFile(io.BytesIO(zb))
    bars = {a: v[1] for a, v in ASSAYS.items()}
    tc = os.environ.get('TABLE_CSV')
    if tc:
        for r in csv.DictReader(open(tc, newline='')):
            if r['DMS ID'] in bars:
                bars[r['DMS ID']] = max(float(v) for k, v in r.items() if k not in META and v not in ('', None))
        print('bars re-read from', tc)
    wins = []
    for a, (osha, _, rsha) in ASSAYS.items():
        ob = open(os.path.join(HERE, 'object', a + '.M1.csv'), 'rb').read()
        name = [n for n in z.namelist() if n.endswith('/' + a + '.csv') or n == a + '.csv'][0]
        rb = z.read(name)
        good = sha(ob) == osha and sha(rb) == rsha
        ref = {r['mutant']: float(r['DMS_score']) for r in csv.DictReader(io.StringIO(rb.decode()))}
        pred = {r['mutant']: float(r['prediction']) for r in csv.DictReader(io.StringIO(ob.decode()))}
        good &= set(ref) == set(pred) and all(math.isfinite(v) for v in pred.values())
        keys = sorted(ref)
        rho = pearson(ranks([ref[k] for k in keys]), ranks([pred[k] for k in keys]))
        m = rho - bars[a]
        if good and m >= 0.015 and rho > bars[a]: wins.append(a)
        print(f'{a:42s} sha {"ok" if good else "FAIL"}  spearman {rho:.4f}  table {bars[a]:.3f}  margin {m:+.4f}')
        ok &= good
    print(f'assays clearing +0.015: {len(wins)} of {len(ASSAYS)} -> {", ".join(wins)}')
    ok &= len(wins) >= 3
    print('PASS' if ok else 'FAIL')
    sys.exit(0 if ok else 1)

if __name__ == '__main__':
    main()
