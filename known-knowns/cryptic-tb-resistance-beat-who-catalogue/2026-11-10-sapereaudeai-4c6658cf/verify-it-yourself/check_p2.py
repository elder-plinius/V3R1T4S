"""Standalone checker for the p2 leakage claim (Python standard library only; run from the package folder).
Definition checked: on the CRyPTIC reuse table (12,287 isolates), split v2 is cluster-aware (every 12-SNP cluster is
wholly in TRAIN or TEST); the 10-NN model's ETH sensitivity at >= 95% specificity on split-v2 TEST, recomputed here from
the per-isolate scores with the stated threshold rule, is 0.3496; each of the 400 random control splits holds 3,073 of
the 12,287 isolates; every one of the 400 random-split values in the metrics file exceeds the split-v2 value.
Optional full recompute: set CRYPTIC_GPI_DISTANCES (GPI_SNP_DISTANCES_VALUES.npy), CRYPTIC_GPI_LABELS
(GPI_SNP_DISTANCES_LABELS.npy) and CRYPTIC_REUSE_TABLE (CRyPTIC_reuse_table_20240917.csv); needs numpy."""
import csv, gzip, hashlib, io, os
OBJ = 'object'
EXPECT = {'p2_knn_ETH_metrics.csv': '4c6658cfc2a0b212af072273305c1cbc35fc10a38ffc406f73724303a4c202d4',
          'predictions_ETH_knn10_split_v2_test.csv': '433c16d4bf7f779653201bbff90113b193a23bf268febda458a93dccddd536df',
          'random_control_splits_membership.bin': 'bfb9e339dff46910225c411e35b29839a084d1d8227dd953d9552910edd43ceb',
          'split_v2.csv.gz': 'c61f25f84d2b7f3ea05435c9225e08f5d3967f4e27ec52d75fb4dbc823550ad1'}
SPLIT_SHA = '3b4ed12292c1804bdd5e226c72e233eacf1be780f8432656e292e1d225640a56'
ok = True


def check(cond, msg):
    global ok
    print(('ok   ' if cond else 'FAIL ') + msg)
    ok = ok and bool(cond)


for f, h in EXPECT.items():
    b = open(os.path.join(OBJ, f), 'rb').read()
    check(hashlib.sha256(b).hexdigest() == h, 'sha256 of object/%s' % f)
raw = gzip.decompress(open(os.path.join(OBJ, 'split_v2.csv.gz'), 'rb').read())
check(hashlib.sha256(raw).hexdigest() == SPLIT_SHA, 'uncompressed split v2 sha256 = %s' % SPLIT_SHA)
rows = list(csv.DictReader(io.StringIO(raw.decode())))
clus = {}
for r in rows:
    clus.setdefault(r['CLUSTER'], set()).add(r['SPLIT'])
ntest = sum(r['SPLIT'] == 'test' for r in rows)
check(len(rows) == 12287 and ntest == 3073, 'split v2: %d isolates, %d TEST' % (len(rows), ntest))
check(all(len(v) == 1 for v in clus.values()), 'no cluster spans TRAIN and TEST (%d clusters)' % len(clus))
pr = list(csv.DictReader(open(os.path.join(OBJ, 'predictions_ETH_knn10_split_v2_test.csv'), newline='')))
test_ids = {r['UNIQUEID'] for r in rows if r['SPLIT'] == 'test'}
check(all(r['UNIQUEID'] in test_ids for r in pr), 'every scored isolate is in split-v2 TEST (%d scored)' % len(pr))
check(min(int(r['NEAREST_TRAIN_DISTANCE']) for r in pr) > 12, 'nearest TRAIN neighbour of every scored TEST isolate is > 12 SNPs')
sc = [(float(r['KNN10_SCORE']), r['ETH_PHENOTYPE'] == 'R') for r in pr]
neg = sorted(s for s, y in sc if not y)
pos = [s for s, y in sc if y]
cands = sorted(set(s for s, _ in sc)) + [float('inf')]
t = next(c for c in cands if 20 * sum(1 for s in neg if s >= c) <= len(neg))   # exact integer form of <= 5%
sens = sum(1 for s in pos if s >= t) / len(pos)
spec = sum(1 for s in neg if s < t) / len(neg)
print('recomputed split-v2 ETH: R %d, S %d, threshold %.6f, sensitivity %.6f, specificity %.6f' % (len(pos), len(neg), t, sens, spec))
check(abs(sens - 0.34962406015037595) < 1e-9 and spec >= 0.95, 'split-v2 sensitivity at >= 95% specificity = 0.3496')
check(all((r['CALL'] == 'R') == (float(r['KNN10_SCORE']) >= t) for r in pr), 'per-isolate calls follow the threshold')
met = list(csv.DictReader(open(os.path.join(OBJ, 'p2_knn_ETH_metrics.csv'), newline='')))
real = [m for m in met if m['kind'] == 'real_split_v2']
rnd = [m for m in met if m['kind'] == 'random']
alt = [m for m in met if m['kind'] == 'alt_cluster_aware']
check(len(real) == 1 and abs(float(real[0]['sens95']) - sens) < 1e-12, 'metrics file real value equals the recomputed value')
check(sorted(int(m['seed']) for m in rnd) == list(range(1, 401)), '400 random control splits, seeds 1..400')
rv = [float(m['sens95']) for m in rnd]
print('random controls: min %.4f mean %.4f max %.4f; above split v2: %d of %d' % (
    min(rv), sum(rv) / len(rv), max(rv), sum(v > sens for v in rv), len(rv)))
check(all(v > sens for v in rv), 'every random-split value exceeds the split-v2 value')
check(all(float(m['spec_at_t']) >= 0.95 for m in met), 'every split meets >= 95% specificity at its threshold')
av = [float(m['sens95']) for m in alt]
print('alternative cluster-aware splits: n %d, min %.4f mean %.4f max %.4f' % (len(av), min(av), sum(av) / len(av), max(av)))
mb = open(os.path.join(OBJ, 'random_control_splits_membership.bin'), 'rb').read()
check(len(mb) == 400 * 1536, 'membership file: 400 rows x 1536 bytes')
counts = [sum(bin(x).count('1') for x in mb[i * 1536:(i + 1) * 1536]) for i in range(400)]
check(all(c == 3073 for c in counts), 'each random control split holds 3,073 TEST isolates')
if os.environ.get('CRYPTIC_GPI_DISTANCES'):
    import numpy as np
    V = np.load(os.environ['CRYPTIC_GPI_DISTANCES'], mmap_mode='r')
    L = np.load(os.environ['CRYPTIC_GPI_LABELS'], allow_pickle=True)
    pos_ = {str(u): i for i, u in enumerate(L)}
    ids = [r['UNIQUEID'] for r in rows]
    ph = {r['UNIQUEID']: r['ETH_BINARY_PHENOTYPE'] for r in csv.DictReader(open(os.environ['CRYPTIC_REUSE_TABLE'], newline=''))
          if r['ETH_PHENOTYPE_QUALITY'] == 'HIGH' and r['ETH_BINARY_PHENOTYPE'] in ('R', 'S')}
    keep = sorted((pos_[u], u) for u in ids if u in ph)
    m = np.array([k for k, _ in keep])
    y = np.array([ph[u] == 'R' for _, u in keep])
    uidx = {u: j for j, u in enumerate(ids)}
    for seed in (0, 1, 2, 3):
        if seed == 0:
            tm = np.array([u in test_ids for _, u in keep])
        else:
            bits = np.unpackbits(np.frombuffer(mb[(seed - 1) * 1536:seed * 1536], dtype=np.uint8), bitorder='little')[:12287].astype(bool)
            tm = np.array([bits[uidx[u]] for _, u in keep])
        tr, te = m[~tm], m[tm]
        s_ = []
        for a in range(0, len(te), 256):
            D = np.asarray(V[te[a:a + 256]])[:, tr]
            o = np.argsort(D, axis=1, kind='stable')[:, :10]
            d = np.take_along_axis(D, o, 1).astype(float)
            w = 1 / (1 + d)
            s_.append((w * y[~tm][o]).sum(1) / w.sum(1))
        s_ = np.concatenate(s_)
        yt = y[tm]
        c2 = sorted(set(s_.tolist())) + [np.inf]
        t2 = next(c for c in c2 if 20 * int((s_[~yt] >= c).sum()) <= int((~yt).sum()))
        v = float((s_[yt] >= t2).mean())
        want = sens if seed == 0 else float(next(mm['sens95'] for mm in rnd if int(mm['seed']) == seed))
        check(abs(v - want) < 1e-9, 'full recompute, %s: %.6f vs %.6f' % ('split v2' if seed == 0 else 'random seed %d' % seed, v, want))
else:
    print('note: full kNN recompute skipped (set CRYPTIC_GPI_DISTANCES, CRYPTIC_GPI_LABELS, CRYPTIC_REUSE_TABLE to run it)')
print('PASS' if ok else 'FAIL')
raise SystemExit(0 if ok else 1)
