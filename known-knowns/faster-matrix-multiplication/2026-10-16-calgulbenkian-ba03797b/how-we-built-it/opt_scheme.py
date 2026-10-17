#!/usr/bin/env python3
"""Optimise one Perminov scheme: run slpopt on U, U^T, V, V^T, W, W^T in parallel (6 single-thread jobs),
transpose back where needed, assemble the best SLP per map, verify with check_slp, write result JSON.
usage: opt_scheme.py scheme.json seconds seed outdir"""
import json, sys, os, subprocess, time
sys.path.insert(0, '[addcomp]/tools')
import graphs as G
from check_slp import check
BIN = '[addcomp]/src/slpopt'
path, secs, seed, outdir = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
extra = sys.argv[5:]
os.makedirs(outdir, exist_ok=True)
d = json.load(open(path)); n, m, p = d['n']; r = d['m']
ref = check(d)
U, V, W = G.maps_of(d)
SRC = '[addcomp]/src/'
JOBSET = os.environ.get('JOBSET', 'u:p:bp,v:p:bp,w:t:bp,u:t:slpopt,v:t:slpopt,w:p:slpopt').split(',')
jobs = {}
mats = {'u': U, 'v': V, 'w': W}
for j in JOBSET:
    name, orient, algo = j.split(':')
    M = mats[name]; X = M if orient == 'p' else G.T(M)
    tag = '%s_%s_%s' % (name, orient, algo)
    mat = os.path.join(outdir, tag + '.mat'); G.write_mat(X, mat)
    gr = os.path.join(outdir, tag + '.graph')
    lg = open(os.path.join(outdir, tag + '.log'), 'w')
    binname = {'bp': 'bpopt', 'slpopt': 'slpopt', 'bp4a': 'bpopt4', 'bp4b': 'bpopt4', 'bp4c': 'bpopt4', 'bp5a': 'bpopt5', 'bp5b': 'bpopt5', 'bp6s': 'bpopt6', 'bp6t': 'bpopt6', 'bp6r': 'bpopt6'}[algo]
    cmd = ['nice', '-n', '19', SRC + binname, mat, gr, str(seed * 7 + len(jobs)), str(secs)] + extra
    if algo in ('bp6s', 'bp6t'): cmd += ['30', '0.8', '1', '1']
    jobs[(name, orient, algo)] = (subprocess.Popen(cmd, stdout=lg, stderr=lg), gr, M)
t0 = time.time()
res = {}
for key, (pr, gr, M) in jobs.items():
    pr.wait()
    g = G.read_graph(gr)
    if key[1] == 't': g = G.transpose(g)
    g = G.prune(g)
    # sanity: graph computes M
    E = G.expand_graph(g)
    want = [{j: v for j, v in enumerate(row) if v} for row in M]
    assert E == want, ('graph mismatch', key)
    res[key] = (G.cost(g), g)
best = {}
for name in 'uvw':
    c = {k[1] + '_' + k[2]: res[k][0] for k in res if k[0] == name}
    if not c: continue
    o = min(c, key=lambda k: c[k]); kk = (name,) + tuple(o.split('_'))
    best[name] = (o, res[kk][1], c)
out = {"n": [n, m, p], "m": r, "z2": False}
nins = {'u': n*m, 'v': m*p, 'w': r}
refc = {'u': ref['adds_U'], 'v': ref['adds_V'], 'w': ref['adds_W']}
src = {}
for name in 'uvw':
    if name not in best or refc[name] <= G.cost(best[name][1]):
        out[name + '_fresh'] = d.get(name + '_fresh', []); out[name] = d[name]; src[name] = 'perminov'
    else:
        fr, rows = G.to_perminov(best[name][1], nins[name])
        out[name + '_fresh'] = fr; out[name] = rows; src[name] = 'ours_' + best[name][0]
chk = check(out)
out['complexity'] = {"naive": chk['naive_total'], "reduced": chk['adds_total']}
summary = dict(format='%dx%dx%d' % (n, m, p), rank=r, perminov=ref['adds_total'], perminov_maps=[ref['adds_U'], ref['adds_V'], ref['adds_W']],
               ours=chk['adds_total'], ours_maps=[chk['adds_U'], chk['adds_V'], chk['adds_W']],
               per_orient={k: best[k][2] for k in best}, valid=chk['VALID'], source=src, tensor=chk['tensor_exact'], secs=round(time.time() - t0, 1))
json.dump(out, open(os.path.join(outdir, 'best_scheme.json'), 'w'))
json.dump(summary, open(os.path.join(outdir, 'summary.json'), 'w'))
print(json.dumps(summary))
