#!/usr/bin/env python3
"""Which of the packings given to the job does the object descend from?

Basin hops, the descent and the polish in gos_kernel.py keep the order of the vectors; an add move appends one
vector at the end and a delete move removes one column. So the object is compared, in order, with every input
of job.json: object vs each same-cell seed; the object's first n-1 vectors vs each (d, n-1) child; the object vs
each (d, n+1) parent with column i removed, for every i. One unitary and per-vector phases are fitted; the
score is mean(1 - |<w_j, U x_j>|^2) over the vectors (0 = the same lines, about 0.5 = unrelated), and 'close'
counts vectors with |<w_j, U x_j>|^2 > 0.99.
usage: python3 order_check.py OBJECT_FILE     (run in this folder after build_job.py; needs numpy)
"""
import json, sys
import numpy as np

job = json.load(open('job.json'))[0]
d, n = job['d'], job['n']


def mat(v, m):
    v = np.asarray(v, float)
    X = (v[:d * m].reshape(m, d) + 1j * v[d * m:].reshape(m, d)).T
    return X / np.linalg.norm(X, axis=0)


def fit(A, B):
    U = np.eye(d, dtype=complex)
    for _ in range(200):
        ph = np.angle(np.sum(A.conj() * (U @ B), axis=0))
        P, _, Qh = np.linalg.svd(A @ (B * np.exp(-1j * ph)).conj().T)
        U = P @ Qh
    s = np.abs(np.sum(A.conj() * (U @ B), axis=0)) ** 2
    return float(np.mean(1 - s)), int((s > 0.99).sum())


W = mat([float(t) for line in open(sys.argv[1]) for t in line.split()], n)
for s in job['seeds']:
    print('same-cell seed  %-26s score %.3e  close %d/%d' % ((s['src'],) + fit(W, mat(s['vals'], n)) + (n,)))
for c in job['children']:
    print('add: child      %-26s score %.3e  close %d/%d  (first n-1 vectors)' % ((c['src'],) + fit(W[:, :n - 1], mat(c['vals'], n - 1)) + (n - 1,)))
for p in job['parents']:
    P = mat(p['vals'], n + 1)
    best = min((fit(W, np.delete(P, i, axis=1)) + (i,) for i in range(n + 1)), key=lambda r: r[0])
    print('delete: parent  %-26s score %.3e  close %d/%d  (best with column %d removed)' % (p['src'], best[0], best[1], n, best[2]))
