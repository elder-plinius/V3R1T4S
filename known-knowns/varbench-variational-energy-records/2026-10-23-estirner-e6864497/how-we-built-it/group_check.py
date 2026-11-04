"""A8: are nqs.py's 8 C4v permutations (about site 0, periodic L x L) a group, and are its characters (A1, A2, B1, B2)
multiplicative on it?  Composition: (g(h s))[k] = s[p_h[p_g[k]]], i.e. the permutation of g.h is p_h[p_g]."""
import sys, os, json
sys.path.insert(0, sys.argv[1]); os.environ['NQS_DEVICE'] = 'cpu'
import numpy as np
import nqs
out = {}
for L in (4, 6, 10):
    P = nqs.c4v_perms(L); names = list(P)
    key = {tuple(P[n].tolist()): n for n in names}
    closed = True; mult = {ir: True for ir in nqs.CHARS}; table = {}
    for g in names:
        for h in names:
            comp = tuple(P[h][P[g]].tolist())
            k = key.get(comp)
            if k is None:
                closed = False; continue
            table[g + '*' + h] = k
            for ir, ch in nqs.CHARS.items():
                if ch[g] * ch[h] != ch[k]:
                    mult[ir] = False
    # every permutation preserves the bond set (a lattice symmetry)
    I, J, W = nqs.bonds(L, 1.0, 0.9)
    bset = {(min(a, b), max(a, b), w) for a, b, w in zip(I.tolist(), J.tolist(), W.tolist())}
    inv = {}
    for n in names:
        p = P[n]; q = np.argsort(p)   # site i of s goes to site q[i] of g s
        img = {(min(q[a], q[b]), max(q[a], q[b]), w) for a, b, w in bset}
        inv[n] = img == bset
    out[L] = dict(closed=closed, characters_multiplicative=mult, preserves_bonds=inv, n_elements=len(set(key)))
print(json.dumps(out, indent=1))
