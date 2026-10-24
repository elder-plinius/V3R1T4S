# V3R1T4S run: NT benchmark (revised) histone tasks - audit lenses + small deterministic CNN noise-floor lens.
# subcommands: train <task> <fold> | grid | nulls | speed | kmer_audit | fold_audit
# Training precision: fp32 everywhere (no autocast). Determinism: torch.use_deterministic_algorithms(True), fixed seeds.
import os, sys, json, time, math, itertools, hashlib
os.environ.setdefault('CUBLAS_WORKSPACE_CONFIG', ':4096:8')
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data', 'nt'); OUT = os.path.join(ROOT, 'out_smoke' if os.environ.get('SMOKE') == '1' else 'out'); os.makedirs(OUT, exist_ok=True)
TASKS = ['H2AFZ', 'H3K27ac', 'H3K27me3', 'H3K36me3', 'H3K4me1', 'H3K4me2', 'H3K4me3', 'H3K9ac', 'H3K9me3', 'H4K20me1']
SMOKE = os.environ.get('SMOKE') == '1'   # 1 epoch, separate out dir, returns BEFORE any test read
NFOLD = 10; EPOCHS = 1 if SMOKE else 25; BS = 256; LR = 1e-3
LUT = np.full(256, 4, np.uint8)
for i, c in enumerate(b'ACGT'): LUT[c] = i; LUT[c + 32] = i

def load(task, split):
    import pandas as pd
    d = pd.read_parquet(os.path.join(DATA, task, split + '.parquet'))
    seqs = d.sequence.tolist(); L = max(len(s) for s in seqs)
    X = np.full((len(seqs), L), 4, np.uint8)
    for i, s in enumerate(seqs): X[i, :len(s)] = LUT[np.frombuffer(s.encode(), np.uint8)]
    return X, d.label.values.astype(np.int64), d.name.tolist()

def mcc(y, p):
    y = np.asarray(y); p = np.asarray(p); tp = float(((p == 1) & (y == 1)).sum()); tn = float(((p == 0) & (y == 0)).sum())
    fp = float(((p == 1) & (y == 0)).sum()); fn = float(((p == 0) & (y == 1)).sum())
    den = math.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn)); return (tp * tn - fp * fn) / den if den > 0 else 0.0

def folds(n, k=NFOLD):
    rs = np.random.default_rng(2026); idx = rs.permutation(n); return np.array_split(idx, k)

def build():
    import torch.nn as nn
    class Net(nn.Module):
        def __init__(s):
            super().__init__()
            s.f = nn.Sequential(nn.Conv1d(4, 128, 15, padding=7), nn.BatchNorm1d(128), nn.ReLU(), nn.MaxPool1d(4),
                                nn.Conv1d(128, 128, 9, padding=4), nn.BatchNorm1d(128), nn.ReLU(), nn.MaxPool1d(4),
                                nn.Conv1d(128, 128, 5, padding=2), nn.BatchNorm1d(128), nn.ReLU())
            s.h = nn.Sequential(nn.Dropout(0.3), nn.Linear(256, 2))
        def forward(s, x):
            import torch
            z = s.f(x); return s.h(torch.cat([z.amax(-1), z.mean(-1)], 1))
    return Net()

def onehot(Xb):
    import torch
    x = torch.nn.functional.one_hot(Xb.long(), 5)[..., :4].float().permute(0, 2, 1); return x.contiguous()

def rc(x): return x.flip(1).flip(2)   # A<->T, C<->G with order ACGT is channel flip; reverse along length

def predict(net, X, bs=1024):
    """fp32 inference, average of forward and reverse-complement softmax (the real inference used for scores and speed)."""
    import torch
    net.eval(); out = []
    with torch.no_grad():
        for i in range(0, len(X), bs):
            x = onehot(X[i:i + bs]); p = (torch.softmax(net(x), 1) + torch.softmax(net(rc(x)), 1)) / 2
            out.append(p[:, 1].double().cpu().numpy())
    return np.concatenate(out)

def train(task, fold):
    import torch
    d = os.path.join(OUT, '%s__f%d' % (task, fold)); os.makedirs(d, exist_ok=True)
    if os.path.exists(os.path.join(d, 'done.json')): print('skip', d); return
    torch.manual_seed(fold); np.random.seed(fold); torch.use_deterministic_algorithms(True)
    torch.backends.cudnn.benchmark = False; torch.backends.cudnn.deterministic = True
    X, y, _ = load(task, 'train'); F = folds(len(y)); va = F[fold]; tr = np.concatenate([F[j] for j in range(NFOLD) if j != fold])
    dev = 'cuda'; Xg = torch.tensor(X, device=dev); yg = torch.tensor(y, device=dev)
    net = build().to(dev); npar = sum(p.numel() for p in net.parameters())
    opt = torch.optim.AdamW(net.parameters(), lr=LR, weight_decay=0.01); lossf = torch.nn.CrossEntropyLoss()
    g = torch.Generator(device=dev); g.manual_seed(fold); trg = torch.tensor(tr, device=dev)
    best = (-2, -1); hist = []; t0 = time.time()
    for ep in range(EPOCHS):
        net.train(); perm = trg[torch.randperm(len(trg), device=dev, generator=g)]
        for i in range(0, len(perm), BS):
            b = perm[i:i + BS]; x = onehot(Xg[b])
            flip = torch.rand(len(b), device=dev, generator=g) < 0.5; x = torch.where(flip[:, None, None], rc(x), x)
            loss = lossf(net(x), yg[b]); opt.zero_grad(set_to_none=True); loss.backward(); opt.step()
        pv = predict(net, Xg[torch.tensor(va, device=dev)]); m = mcc(y[va], (pv > 0.5).astype(int)); hist.append(round(m, 5))
        if m > best[0]: best = (m, ep); torch.save(net.state_dict(), os.path.join(d, 'model.pt'))
    net.load_state_dict(torch.load(os.path.join(d, 'model.pt'))); pv = predict(net, Xg[torch.tensor(va, device=dev)])
    info = dict(task=task, fold=fold, seed=fold, params=npar, precision='fp32', best_epoch=best[1], val_mcc=mcc(y[va], (pv > 0.5).astype(int)),
                val_hist=hist, train_s=round(time.time() - t0, 1))
    if SMOKE: print('SMOKE', json.dumps({k: v for k, v in info.items() if k != 'val_hist'})); return
    print('TEST_READ', task, fold, time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), flush=True)
    Xt, yt, _ = load(task, 'test'); Xtg = torch.tensor(Xt, device=dev)
    pt = predict(net, Xtg); pt2 = predict(net, Xtg); info['test_deterministic'] = bool(np.array_equal(pt, pt2))
    np.save(os.path.join(d, 'score_test.npy'), pt); info['test_mcc'] = mcc(yt, (pt > 0.5).astype(int))
    json.dump(info, open(os.path.join(d, 'done.json'), 'w')); print('DONE', json.dumps({k: v for k, v in info.items() if k != 'val_hist'}), flush=True)

def grid():
    for t in TASKS:
        for f in range(NFOLD): train(t, f)
    print('GRIDDONE', flush=True)

def speed():
    """throughput of the real inference (fp32, forward+RC average) on the H3K9me3 test set, GPU and CPU (1 and all threads)."""
    import torch
    net = build(); net.load_state_dict(torch.load(os.path.join(OUT, 'H3K9me3__f0', 'model.pt'), map_location='cpu'))
    Xt, _, _ = load('H3K9me3', 'test'); res = {}
    for dev, th in (('cuda', None), ('cpu', 1), ('cpu', os.cpu_count())):
        if th: torch.set_num_threads(th)
        n = net.to(dev); X = torch.tensor(Xt, device=dev); predict(n, X[:256]); t0 = time.time(); k = 0
        while time.time() - t0 < 5: predict(n, X); k += len(X)
        if dev == 'cuda': torch.cuda.synchronize()
        res['%s_%s' % (dev, th or 'gpu')] = round(k / (time.time() - t0), 1)
    print('SPEED', json.dumps(res), flush=True); json.dump(res, open(os.path.join(OUT, 'SPEED.json'), 'w'))

def nulls(n_ctrl=1000):
    rs = np.random.default_rng(2026); out = {}
    for t in TASKS:
        _, yt, _ = load(t, 'test'); per = []
        for f in range(NFOLD):
            p = os.path.join(OUT, '%s__f%d' % (t, f), 'score_test.npy')
            if not os.path.exists(p): continue
            pr = (np.load(p) > 0.5).astype(int); real = mcc(yt, pr); ctrl = [mcc(rs.permutation(yt), pr) for _ in range(n_ctrl)]
            per.append(dict(fold=f, real=real, best_control=max(ctrl), beats=real > max(ctrl)))
        if not per: continue
        p0 = (np.load(os.path.join(OUT, '%s__f0' % t, 'score_test.npy')) > 0.5).astype(int)
        boot = [mcc(yt[i], p0[i]) for i in (rs.integers(0, len(yt), len(yt)) for _ in range(1000))]
        out[t] = dict(n_test=int(len(yt)), fold_mcc=[r['real'] for r in per], mean=float(np.mean([r['real'] for r in per])),
                      sd=float(np.std([r['real'] for r in per], ddof=1)), null_controls=n_ctrl, best_control=float(max(r['best_control'] for r in per)),
                      all_beat=bool(all(r['beats'] for r in per)), test_boot_se_f0=float(np.std(boot, ddof=1)))
        print('NULL', t, json.dumps(out[t]), flush=True)
    json.dump(out, open(os.path.join(OUT, 'NULLS.json'), 'w'), indent=1); print('NULLDONE', flush=True)

# ---------------- CPU audits (no models) ----------------
K = 31
def kmers(X):
    """canonical 31-mer codes (uint64) per sequence; windows with N skipped."""
    out = []
    w = np.uint64(4) ** np.arange(K - 1, -1, -1, dtype=np.uint64)
    for s in X:
        s = s[s < 4].astype(np.uint64)
        if len(s) < K: out.append(np.zeros(0, np.uint64)); continue
        v = np.lib.stride_tricks.sliding_window_view(s, K); f = (v * w).sum(1)
        r = ((3 - v[:, ::-1]) * w).sum(1); out.append(np.minimum(f, r))
    return out

def kmer_audit():
    res = {}
    for t in TASKS:
        Xtr, ytr, ntr = load(t, 'train'); Xte, yte, nte = load(t, 'test')
        ctr = sorted(set(n.split(':')[0] for n in ntr)); cte = sorted(set(n.split(':')[0] for n in nte))
        ktr = kmers(Xtr); kte = kmers(Xte)
        allk = np.unique(np.concatenate(ktr))
        # k-mer -> label share in train (positive-only / negative-only / both)
        pos = np.unique(np.concatenate([k for k, l in zip(ktr, ytr) if l == 1])); neg = np.unique(np.concatenate([k for k, l in zip(ktr, ytr) if l == 0]))
        sid = np.concatenate([np.full(len(k), i) for i, k in enumerate(kte)]); cat = np.concatenate(kte); cnt = np.maximum(np.bincount(sid, minlength=len(kte)), 1)
        frac = np.bincount(sid, np.isin(cat, allk), len(kte)) / cnt
        fpos = np.bincount(sid, np.isin(cat, pos), len(kte)) / cnt; fneg = np.bincount(sid, np.isin(cat, neg), len(kte)) / cnt
        # exact sequence duplicates (either strand)
        def key(s): return hashlib.sha1(s.tobytes()).hexdigest()
        def rck(s): r = np.where(s < 4, 3 - s, 4)[::-1].astype(np.uint8); return hashlib.sha1(r.tobytes()).hexdigest()
        trk = {}
        for s, l in zip(Xtr, ytr): trk.setdefault(key(s), set()).add(int(l)); trk.setdefault(rck(s), set()).add(int(l))
        exact = [key(s) in trk for s in Xte]
        # memorisation baseline: predict label by which train class shares more 31-mers (no learning)
        pred = (fpos > fneg).astype(int); tie = fpos == fneg
        near = frac >= 0.5
        r = dict(n_train=len(ytr), n_test=len(yte), chrom_train=ctr, chrom_test=cte, chrom_overlap=sorted(set(ctr) & set(cte)),
                 exact_dup_test=int(sum(exact)), test_frac31_mean=float(frac.mean()), test_frac31_ge_0p5=int(near.sum()),
                 test_frac31_ge_0p9=int((frac >= 0.9).sum()), near_pos_rate=float(yte[near].mean()) if near.any() else None,
                 kmer_vote_mcc=mcc(yte, pred), kmer_vote_ties=int(tie.sum()),
                 kmer_vote_mcc_on_near=mcc(yte[near], pred[near]) if near.sum() > 5 else None)
        res[t] = r; print('KAUDIT', t, json.dumps({k: v for k, v in r.items() if not k.startswith('chrom_t')}), flush=True)
        np.save(os.path.join(OUT, 'kfrac_%s.npy' % t), np.stack([frac, fpos, fneg]))
    json.dump(res, open(os.path.join(OUT, 'KMER_AUDIT.json'), 'w'), indent=1)

def fold_audit(path):
    """p3-style audit of benchmark.csv: paired exact sign-flip tests (1024 sign patterns) for every model pair per task."""
    import pandas as pd, ast
    d = pd.read_csv(path); d['m'] = d.MCC.apply(lambda s: np.array(ast.literal_eval(s))); res = {}
    signs = np.array(list(itertools.product([1, -1], repeat=10)))
    for t, g in d.groupby('Dataset'):
        g = g.assign(mean=g.m.apply(np.mean)).sort_values('mean', ascending=False); rows = list(g.itertuples())
        best = rows[0]; pairs = []
        for a, b in itertools.combinations(rows, 2):
            diff = a.m - b.m; obs = abs(diff.mean()); null = np.abs((signs * diff).mean(1)); p = float((null >= obs - 1e-12).mean())
            pairs.append(dict(a=a.Model, b=b.Model, diff=float(diff.mean()), p=p))
        adj = [p for p in pairs if abs(rows.index(next(r for r in rows if r.Model == p['a'])) - rows.index(next(r for r in rows if r.Model == p['b']))) == 1]
        res[t] = dict(n_models=len(rows), best=best.Model, best_mean=float(best.mean), fold_sd_best=float(best.m.std(ddof=1)),
                      n_pairs=len(pairs), pairs_p_ge_0p05=int(sum(p['p'] >= 0.05 for p in pairs)),
                      adjacent_pairs=len(adj), adjacent_p_ge_0p05=int(sum(p['p'] >= 0.05 for p in adj)),
                      best_vs_second=dict(second=rows[1].Model, diff=float(best.mean - rows[1].mean), p=next(p['p'] for p in pairs if p['a'] == best.Model and p['b'] == rows[1].Model)),
                      models_not_sig_below_best=[p['b'] for p in pairs if p['a'] == best.Model and p['p'] >= 0.05])
        print('FAUDIT', t, json.dumps(res[t]), flush=True)
    json.dump(res, open(os.path.join(OUT, 'FOLD_AUDIT.json'), 'w'), indent=1)

if __name__ == '__main__':
    a = sys.argv[1:]
    {'train': lambda: train(a[1], int(a[2])), 'grid': grid, 'nulls': nulls, 'speed': speed,
     'kmer_audit': kmer_audit, 'fold_audit': lambda: fold_audit(a[1])}[a[0]]()
