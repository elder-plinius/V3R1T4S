#!/usr/bin/env python3
"""PHYLO lens, run 2026-10-18-0202 (built on run 2026-10-18-0104 phylo lens code): phylogenetic imputation of a masked cognate reflex.

train (per family, from the manifest's training file only):
  1. multiple alignment (lingpy SCA progressive alignment) of every training cognate set's reflexes;
  2. language distances from the aligned columns (identity + correspondence predictability), neighbour joining,
     rooted at the last join (or a star tree with --tree star);
  3. a latent-tree model over the aligned columns: every edge parent->child carries a free conditional probability
     table P(child segment | parent segment) over segments + gap (Dirichlet prior towards identity), internal nodes
     are latent, absent languages are marginalised; fitted by EM with Felsenstein's pruning (up/down passes).
predict (per row, nothing carried between rows): align the visible reflexes, compute the posterior of the masked
  tip's state in each column, take the argmax, drop gaps.
Deterministic: no random numbers; prediction is single-threaded and row by row.
"""
import os
import sys

_CMD = sys.argv[1] if len(sys.argv) > 1 else ""
_NT = "2" if _CMD == "train" else "1"
for _v in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = _NT
_HERE = os.path.dirname(os.path.abspath(__file__))
_HOME = os.path.join(os.path.dirname(_HERE), "home")
try:
    os.makedirs(os.path.join(_HOME, ".w"), exist_ok=True)
except OSError:
    import tempfile
    _HOME = tempfile.mkdtemp(prefix="phylo-home-")
os.environ["HOME"] = _HOME

import argparse
import json
import logging
import pickle
from collections import defaultdict

import numpy as np

CFG = {"tree": "nj", "iters": 40, "alpha": 1.0, "beta_tip": 0.6, "beta_int": 0.8, "tip_supp": "soft",
       "gap_thr": 0.5, "merge": 0, "ctx": 0,
       "gamma": 3.0, "aligner": "lingpy", "gap": -2.0, "bonus": 1.0, "guide_passes": 1,
       "poe": 0.0, "tau": 0.05, "kappa": 2.0, "simprior": 0, "boot": 1,
       "rctx": 0, "ctxb": 2.0, "lmw": 0.0, "lmk": 6, "lmb": 1.0}

CFG.update({"aligner": "own", "bagem": 1, "beta_tip": 0.8, "boot": 20, "gap_lo": 0.2, "poe": 0.5, "rctx": 1})  # frozen PRIMARY config (chosen on val-0.50 only)


def load(path):
    with open(path, encoding="utf-8") as f:
        lines = [ln.rstrip("\n") for ln in f if ln.strip()]
    h = lines[0].split("\t")
    langs = h[1:]
    data = {}
    for ln in lines[1:]:
        r = ln.split("\t") + [""] * len(h)
        data[r[0]] = {l: r[i + 1].split() for i, l in enumerate(langs)}
    return langs, data


_MULT = None


def msa(seqs):
    """Rows of an alignment matrix (gap '-') for the given token lists, in the given order."""
    global _MULT
    if len(seqs) == 1:
        return [list(seqs[0])]
    if _MULT is None:
        logging.disable(logging.CRITICAL)
        from lingpy import Multiple
        _MULT = Multiple
    try:
        m = _MULT([list(s) for s in seqs])
        m.prog_align()
        A = [list(r) for r in m.alm_matrix]
        if len(A) == len(seqs) and all(len(r) == len(A[0]) for r in A) and \
                all([x for x in r if x != "-"] == list(s) for r, s in zip(A, seqs)):
            return A
    except Exception:
        pass
    n = max(len(s) for s in seqs)
    return [list(s) + ["-"] * (n - len(s)) for s in seqs]


def merge_solo(A, known=None):
    """Merge every column where exactly one row has a segment into that row's neighbouring segment (composite token
    'x y'); with `known`, only merges whose composite token is in `known`."""
    n = len(A)
    if n < 2:
        return A
    C = len(A[0])
    solo = [sum(1 for r in A if r[j] != "-") == 1 for j in range(C)]
    if not any(solo):
        return A
    B = [list(r) for r in A]
    keep = [not x for x in solo]
    for j in range(C):  # appends to the previous kept segment
        if not solo[j]:
            continue
        k = next(i for i in range(n) if A[i][j] != "-")
        jp = next((q for q in range(j - 1, -1, -1) if keep[q] and B[k][q] != "-"), None)
        if jp is not None:
            tok = B[k][jp] + " " + A[k][j]
            if known is None or tok in known:
                B[k][jp] = tok
                solo[j] = "done"
    for j in range(C - 1, -1, -1):  # prepends to the next kept segment
        if solo[j] is not True:
            continue
        k = next(i for i in range(n) if A[i][j] != "-")
        jn = next((q for q in range(j + 1, C) if keep[q] and B[k][q] != "-"), None)
        if jn is not None:
            tok = A[k][j] + " " + B[k][jn]
            if known is None or tok in known:
                B[k][jn] = tok
                solo[j] = "done"
    cols = [j for j in range(C) if solo[j] != "done"]
    return [[r[j] for j in cols] for r in B]


# ---------------------------------------------------------------- own aligner (no lingpy at predict time)
class Aligner:
    """Progressive profile alignment guided by the language tree. Segment scores from lingpy's SCA sound classes and
    SCA scoring table (a generic sound-symbol table, looked up at train time and stored in the model) plus a bonus
    for identical segments; linear gap penalty."""

    def __init__(self, tokens, gap=-2.0, bonus=1.0):
        logging.disable(logging.CRITICAL)
        from lingpy import rc
        from lingpy.sequence.sound_classes import token2class
        m = rc("sca")
        classes = ["0"] + sorted(set(m.converter.values()) - {"0"})
        self.cidx = {c: i for i, c in enumerate(classes)}
        nc = len(classes)
        T = np.zeros((nc, nc))
        for a in classes:
            for b in classes:
                try:
                    T[self.cidx[a], self.cidx[b]] = float(m.scorer[a, b])
                except Exception:
                    T[self.cidx[a], self.cidx[b]] = 0.0
        self.T = T
        self.tokcls, self.charcls = {}, {}
        for t in sorted(tokens):
            try:
                self.tokcls[t] = self.cidx.get(token2class(t, m), 0)
            except Exception:
                self.tokcls[t] = 0
            for ch in t:
                if ch not in self.charcls:
                    try:
                        self.charcls[ch] = self.cidx.get(token2class(ch, m), 0)
                    except Exception:
                        self.charcls[ch] = 0
        self.gap, self.bonus = gap, bonus

    def cls(self, t):
        c = self.tokcls.get(t)
        if c is not None:
            return c
        for ch in t:
            c = self.charcls.get(ch, 0)
            if c:
                return c
        return 0

    def merge(self, P1, P2):
        n1, n2 = len(P1[0]), len(P2[0])
        voc = {}
        for P in (P1, P2):
            for r in P:
                for t in r:
                    if t != "-" and t not in voc:
                        voc[t] = len(voc)
        cl = np.array([self.cls(t) for t in voc], dtype=np.int64)
        nv = len(voc)

        def counts(P, n):
            K = np.zeros((n, nv))
            for r in P:
                for j, t in enumerate(r):
                    if t != "-":
                        K[j, voc[t]] += 1
            return K
        K1, K2 = counts(P1, n1), counts(P2, n2)
        Tl = self.T[np.ix_(cl, cl)] + self.bonus * np.eye(nv)
        c1, c2 = K1.sum(axis=1), K2.sum(axis=1)
        S = (K1 @ Tl @ K2.T) / np.maximum(np.outer(c1, c2), 1.0)
        g = self.gap
        D = np.zeros((n1 + 1, n2 + 1))
        D[:, 0] = g * np.arange(n1 + 1)
        D[0, :] = g * np.arange(n2 + 1)
        for i in range(1, n1 + 1):
            for j in range(1, n2 + 1):
                D[i, j] = max(D[i - 1, j - 1] + S[i - 1, j - 1], D[i - 1, j] + g, D[i, j - 1] + g)
        i, j, ops = n1, n2, []
        while i > 0 or j > 0:
            if i > 0 and j > 0 and D[i, j] == D[i - 1, j - 1] + S[i - 1, j - 1]:
                ops.append((i - 1, j - 1)); i -= 1; j -= 1
            elif i > 0 and D[i, j] == D[i - 1, j] + g:
                ops.append((i - 1, None)); i -= 1
            else:
                ops.append((None, j - 1)); j -= 1
        ops.reverse()
        R1 = [[r[a] if a is not None else "-" for a, _ in ops] for r in P1]
        R2 = [[r[b] if b is not None else "-" for _, b in ops] for r in P2]
        return R1 + R2

    def msa(self, seqs_by_tip, children, root, L):
        """seqs_by_tip: {tip: tokens}. Returns (tips in output order, rows)."""
        def rec(node):
            if node < L:
                return ([list(seqs_by_tip[node])], [node]) if node in seqs_by_tip else None
            parts = [q for q in (rec(c) for c in children.get(node, [])) if q]
            if not parts:
                return None
            prof, tips = parts[0]
            for p2, t2 in parts[1:]:
                prof = self.merge(prof, p2)
                tips = tips + t2
            return prof, tips
        prof, tips = rec(root)
        return tips, prof


def own_msa(al, seqs_by_tip, children, root, L):
    """Rows in increasing tip order."""
    tips, rows = al.msa(seqs_by_tip, children, root, L)
    order = sorted(range(len(tips)), key=lambda k: tips[k])
    return [tips[k] for k in order], [rows[k] for k in order]


# ---------------------------------------------------------------- tree
def hash_tok(t):
    h = 0
    for ch in t:
        h = (h * 1000003 + ord(ch)) % 1000000007
    return h


def distances(obs, L, gap):
    D = np.full((L, L), np.nan)
    for a in range(L):
        D[a, a] = 0.0
        for b in range(a + 1, L):
            m = (obs[:, a] >= 0) & (obs[:, b] >= 0) & ~((obs[:, a] == gap) & (obs[:, b] == gap))
            n = int(m.sum())
            if n < 5:
                continue
            x, y = obs[m, a], obs[m, b]
            ident = float(np.sum((x == y) & (x != gap))) / n
            pab = defaultdict(lambda: defaultdict(int))
            for u, v in zip(x.tolist(), y.tolist()):
                pab[u][v] += 1
            pba = defaultdict(lambda: defaultdict(int))
            for u, v in zip(x.tolist(), y.tolist()):
                pba[v][u] += 1
            pr = (sum(max(d.values()) for d in pab.values()) + sum(max(d.values()) for d in pba.values())) / (2.0 * n)
            D[a, b] = D[b, a] = 1.0 - 0.5 * (ident + pr)
    # fill missing by shortest two-step paths, else the maximum
    mx = np.nanmax(D) if np.any(~np.isnan(D)) else 1.0
    for a in range(L):
        for b in range(L):
            if np.isnan(D[a, b]):
                c = [D[a, k] + D[k, b] for k in range(L) if not np.isnan(D[a, k]) and not np.isnan(D[k, b])]
                D[a, b] = min(c) if c else mx
    D = 0.5 * (D + D.T)
    return D


def nj_tree(D):
    """Neighbour joining; returns (children dict, root, n_nodes). Tips are 0..L-1."""
    L = D.shape[0]
    dist = {(i, j): float(D[i, j]) for i in range(L) for j in range(L)}
    nodes = list(range(L))
    adj = defaultdict(list)
    nxt = L
    while len(nodes) > 2:
        n = len(nodes)
        r = {i: sum(dist[(i, k)] for k in nodes) for i in nodes}
        best = None
        for ii in range(n):
            for jj in range(ii + 1, n):
                i, j = nodes[ii], nodes[jj]
                q = (n - 2) * dist[(i, j)] - r[i] - r[j]
                if best is None or q < best[0] - 1e-12:
                    best = (q, i, j)
        _, i, j = best
        u = nxt
        nxt += 1
        for k in nodes:
            if k not in (i, j):
                d = 0.5 * (dist[(i, k)] + dist[(j, k)] - dist[(i, j)])
                dist[(u, k)] = dist[(k, u)] = d
        dist[(u, u)] = 0.0
        adj[u] += [i, j]
        adj[i].append(u)
        adj[j].append(u)
        nodes = [k for k in nodes if k not in (i, j)] + [u]
    a, b = nodes
    adj[a].append(b)
    adj[b].append(a)
    root = nxt - 1 if nxt > L else 0
    children = defaultdict(list)
    seen = {root}
    stack = [root]
    while stack:
        p = stack.pop()
        for c in sorted(adj[p]):
            if c not in seen:
                seen.add(c)
                children[p].append(c)
                stack.append(c)
    return dict(children), root, nxt


def star_tree(L):
    return {L: list(range(L))}, L, L + 1


def orders(children, root):
    pre = []
    stack = [root]
    while stack:
        p = stack.pop()
        pre.append(p)
        for c in reversed(children.get(p, [])):
            stack.append(c)
    return pre, pre[::-1]


# ---------------------------------------------------------------- latent tree model
class Model:
    pass


def upward(mod, obs, ctx):
    """Messages up[c] (C x V over parent states) and Lnode[p] (C x V) for internal nodes.
    Tip CPTs are K x V x V (K context classes; ctx gives each column's class); internal CPTs are V x V."""
    C = obs.shape[0]
    V = mod.V
    up, Ln = {}, {}
    for c in mod.post:
        if c < mod.L:
            o = obs[:, c]
            m = np.ones((C, V))
            k = o >= 0
            if k.any():
                m[k] = mod.M[c][ctx[k], :, o[k]]
            up[c] = m
        else:
            Lc = np.ones((C, V))
            for ch in mod.children[c]:
                Lc = Lc * up[ch]
            s = Lc.max(axis=1, keepdims=True)
            s[s <= 0] = 1.0
            Lc = Lc / s
            Ln[c] = Lc
            if c != mod.root:
                up[c] = Lc @ mod.M[c].T
    return up, Ln


def em_fit(mod, obs, ctx, iters, alpha, gamma):
    C = obs.shape[0]
    V = mod.V
    K = mod.K
    prev = None
    for it in range(iters):
        up, Ln = upward(mod, obs, ctx)
        E = {c: np.zeros(mod.M[c].shape) for c in mod.M}
        out = {mod.root: np.tile(mod.pi, (C, 1))}
        rp = out[mod.root] * Ln[mod.root]
        z = rp.sum(axis=1)
        ll = float(np.sum(np.log(np.maximum(z, 1e-300))))
        Er = (rp / z[:, None]).sum(axis=0)
        for p in mod.pre:
            if p < mod.L:
                continue
            for c in mod.children[p]:
                Dc = out[p].copy()
                for s in mod.children[p]:
                    if s != c:
                        Dc = Dc * up[s]
                Dc = Dc / np.maximum(Dc.sum(axis=1, keepdims=True), 1e-300)
                if c < mod.L:
                    o = obs[:, c]
                    k = o >= 0
                    if k.any():
                        ok, ck = o[k], ctx[k]
                        w = Dc[k] * mod.M[c][ck, :, ok]
                        w = w / np.maximum(w.sum(axis=1, keepdims=True), 1e-300)
                        Y = np.zeros((len(ok), V))
                        Y[np.arange(len(ok)), ok] = 1.0
                        for kk in range(K):
                            sel = ck == kk
                            if not sel.any():
                                continue
                            E[c][kk] += w[sel].T @ Y[sel]
                else:
                    Zc = np.maximum((Dc * up[c]).sum(axis=1), 1e-300)
                    E[c] += mod.M[c] * ((Dc / Zc[:, None]).T @ Ln[c])
                    oc = Dc @ mod.M[c]
                    out[c] = oc / np.maximum(oc.sum(axis=1, keepdims=True), 1e-300)
        for c in mod.M:
            if c < mod.L:
                P0 = mod.P0[c]
                pooled = E[c].sum(axis=0) + alpha * P0
                pooled = pooled / np.maximum(pooled.sum(axis=1, keepdims=True), 1e-300)
                A = E[c] + (gamma * pooled + alpha * P0)[None, :, :] if K > 1 else E[c] + alpha * P0[None]
                mod.M[c] = A / np.maximum(A.sum(axis=2, keepdims=True), 1e-300)
            else:
                A = E[c] + alpha * mod.P0[c]
                mod.M[c] = A / np.maximum(A.sum(axis=1, keepdims=True), 1e-300)
        a = Er + alpha * mod.pi0
        mod.pi = a / a.sum()
        if prev is not None and abs(ll - prev) < mod.tol * max(1.0, abs(prev)):
            break
        prev = ll
    mod.ll = ll
    mod.n_iter = it + 1


def target_posterior(mod, obs, ctx, t):
    """Posterior over tip t's state for every column (C x V); tip t must be unobserved in obs."""
    up, Ln = upward(mod, obs, ctx)
    path = [t]
    while path[-1] != mod.root:
        path.append(mod.parent[path[-1]])
    path = path[::-1]  # root ... t
    C = obs.shape[0]
    out = np.tile(mod.pi, (C, 1))
    for p, c in zip(path[:-1], path[1:]):
        Dc = out.copy()
        for s in mod.children[p]:
            if s != c:
                Dc = Dc * up[s]
        Dc = Dc / np.maximum(Dc.sum(axis=1, keepdims=True), 1e-300)
        if c < mod.L:
            oc = np.einsum("cv,cvw->cw", Dc, mod.M[c][ctx])
        else:
            oc = Dc @ mod.M[c]
        out = oc / np.maximum(oc.sum(axis=1, keepdims=True), 1e-300)
    return out


def ens_posterior(mod, obs, cc, t):
    """Tree posterior averaged over the main tree and the bootstrap trees; with cfg bma = T > 0 the trees are
    weighted by exp((ll - max ll) / T) (training log-likelihood; Bayesian model averaging at temperature T)."""
    trees = [mod] + list(getattr(mod, "ens", []))
    T = mod.cfg.get("bma", 0)
    if T > 0 and len(trees) > 1:
        ll = np.array([m.ll for m in trees])
        w = np.exp((ll - ll.max()) / T)
    else:
        w = np.ones(len(trees))
    w = w / w.sum()
    post = None
    for wi, m in zip(w, trees):
        if wi < 1e-6:
            continue
        p = wi * target_posterior(m, obs, cc, t)
        post = p if post is None else post + p
    return post


def col_ctx(C, K):
    """Context class of each of C columns: 0 initial, 1 medial, 2 final (K=3); all 0 when K=1."""
    if K == 1:
        return np.zeros(C, dtype=np.int64)
    c = np.ones(C, dtype=np.int64)
    c[-1] = 2
    c[0] = 0
    return c


def nb_arrays(pres, A, idx, L, V):
    """Left / right neighbour symbol (index; V = word boundary, V + 1 = unknown symbol) of every visible row at every
    column of alignment A (rows in the order of pres); -1 where the language is absent."""
    C = len(A[0])
    LF = np.full((C, L), -1, dtype=np.int64)
    RG = np.full((C, L), -1, dtype=np.int64)
    for k, i in enumerate(pres):
        prev = V
        for j in range(C):
            LF[j, i] = prev
            if A[k][j] != "-":
                prev = idx.get(A[k][j], V + 1)
        nxt = V
        for j in range(C - 1, -1, -1):
            RG[j, i] = nxt
            if A[k][j] != "-":
                nxt = idx.get(A[k][j], V + 1)
    return LF, RG


def init_tree(m, children, root, L, V, K, supp, cfg, simW=None):
    bt, bi = cfg["beta_tip"], cfg["beta_int"]
    m.L, m.V, m.K = L, V, K
    m.children = {p: list(cs) for p, cs in children.items()}
    for i in range(L):
        m.children.setdefault(i, [])
    m.root = root
    m.parent = {c: p for p, cs in m.children.items() for c in cs}
    m.pre, m.post = orders(m.children, root)
    m.P0, m.M = {}, {}
    for c in m.parent:
        if c < L and cfg["tip_supp"] == "hard":
            sc = supp[c].astype(float)
            P = np.tile(sc * (1 - bt) / sc.sum(), (V, 1))
            for x in range(V):
                if supp[c][x]:
                    P[x, x] += bt
                else:
                    P[x] = sc / sc.sum()
        elif c < L:
            sc = supp[c].astype(float)
            u = 0.5 / V + 0.5 * sc / sc.sum()
            if simW is not None:
                Q = u[None, :] * simW
                Q = Q / Q.sum(axis=1, keepdims=True)
                P = (1 - bt) * Q + bt * np.eye(V)
            else:
                P = np.tile(u * (1 - bt), (V, 1)) + bt * np.eye(V)
        else:
            P = np.full((V, V), (1 - bi) / V) + bi * np.eye(V)
        P = P / P.sum(axis=1, keepdims=True)
        m.P0[c] = P
        m.M[c] = np.tile(P[None], (K, 1, 1)) if c < L else P.copy()
    m.pi0 = np.full(V, 1.0 / V)
    m.pi = m.pi0.copy()


def build_ens(mod, obs, ctx, cfg, simW=None):
    """Bootstrap ensemble of tree topologies (NJ on resampled columns), each fitted by EM on all columns.
    Deterministic (fixed seed); rebuilt from the stored columns when the model is loaded."""
    ens = []
    rng = np.random.RandomState(cfg.get("seed", 20261018))
    for bb in range(1, cfg.get("boot", 1)):
        sel = rng.randint(0, obs.shape[0], obs.shape[0])
        chb, rootb, _ = nj_tree(distances(obs[sel], mod.L, 0))
        sub = Model()
        sub.tol = mod.tol
        init_tree(sub, chb, rootb, mod.L, mod.V, mod.K, mod.supp, cfg, simW)
        if cfg.get("bagem", 0):
            em_fit(sub, obs[sel], ctx[sel], cfg["iters"], cfg["alpha"], cfg["gamma"])
        else:
            em_fit(sub, obs, ctx, cfg["iters"], cfg["alpha"], cfg["gamma"])
        for k in ("P0", "pi0"):
            sub.__dict__.pop(k, None)
        ens.append(sub)
    return ens


def build_cpair(obs, LFall, RGall):
    cpair = {}
    for o, lf, rg in zip(obs.tolist(), LFall.tolist(), RGall.tolist()):
        pr = [(i, x) for i, x in enumerate(o) if x >= 0]
        for i, x in pr:
            l, r = lf[i], rg[i]
            for t, y in pr:
                if t != i:
                    for key in ((i, t, x, l, -1), (i, t, x, -1, r), (i, t, x, l, r)):
                        dct = cpair.setdefault(key, {})
                        dct[y] = dct.get(y, 0) + 1
    return cpair


def fit_family(langs, data, cfg):
    L = len(langs)
    syms = set()
    for r in data.values():
        for l in langs:
            syms.update(r[l])
    syms.discard("-")
    al = None
    if cfg["aligner"] == "own":
        al = Aligner(syms, cfg["gap"], cfg["bonus"])
        star = {L: list(range(L))}
        guide, groot = star, L
        for _ in range(cfg["guide_passes"]):
            gc = []
            for key in sorted(data):
                r = data[key]
                pres = [i for i, l in enumerate(langs) if r[l]]
                if len(pres) < 2:
                    continue
                pr, A = own_msa(al, {i: r[langs[i]] for i in pres}, guide, groot, L)
                for j in range(len(A[0])):
                    o = [-1] * L
                    for k, i in enumerate(pr):
                        o[i] = 0 if A[k][j] == "-" else 1 + hash_tok(A[k][j])
                    gc.append(o)
            Dg = distances(np.array(gc, dtype=np.int64).reshape(-1, L), L, 0)
            guide, groot, _ = nj_tree(Dg)
    alns = []
    for key in sorted(data):
        r = data[key]
        pres = [i for i, l in enumerate(langs) if r[l]]
        if len(pres) < 2:
            continue
        if al is not None:
            pres, A = own_msa(al, {i: r[langs[i]] for i in pres}, guide, groot, L)
        else:
            A = msa([r[langs[i]] for i in pres])
        if cfg["merge"]:
            A = merge_solo(A)
            for row in A:
                syms.update(x for x in row if x != "-")
        alns.append((pres, A))
    sym = ["-"] + sorted(syms)
    idx = {s: i for i, s in enumerate(sym)}
    V = len(sym)
    K = 3 if cfg["ctx"] else 1
    cols, ctxs, lfs, rgs = [], [], [], []
    for pres, A in alns:
        ctxs.extend(col_ctx(len(A[0]), K).tolist())
        if cfg.get("rctx", 0) or cfg.get("lmw", 0):
            LFa, RGa = nb_arrays(pres, A, idx, L, V)
            lfs.append(LFa)
            rgs.append(RGa)
        for j in range(len(A[0])):
            o = [-1] * L
            for k, i in enumerate(pres):
                o[i] = idx[A[k][j]]
            cols.append(o)
    obs = np.array(cols, dtype=np.int64).reshape(-1, L)
    ctx = np.array(ctxs, dtype=np.int64)
    D = distances(obs, L, 0)
    if cfg["tree"] == "star":
        children, root, N = star_tree(L)
    elif al is not None and cfg["tree"] == "guide":
        children, root = guide, groot
    else:
        children, root, N = nj_tree(D)
    supp = {}
    for i in range(L):
        s = np.zeros(V, dtype=bool)
        s[0] = True
        k = obs[:, i] >= 0
        s[np.unique(obs[k, i])] = True
        supp[i] = s
    bt, bi = cfg["beta_tip"], cfg["beta_int"]
    simW = None
    if cfg.get("simprior", 0) and al is not None:
        cl = np.array([0] + [al.cls(x) for x in sym[1:]], dtype=np.int64)
        simW = np.exp(al.T[np.ix_(cl, cl)] / cfg["simprior"])
        simW[0, :] = 1.0
        simW[:, 0] = 1.0

    mod = Model()
    mod.sym, mod.langs = sym, langs
    init_tree(mod, children, root, L, V, K, supp, cfg, simW)
    mod.D = D
    mod.supp = supp
    mod.tol = cfg.get("tol", 1e-4)
    em_fit(mod, obs, ctx, cfg["iters"], cfg["alpha"], cfg["gamma"])
    mod.obs_train = obs.astype(np.int32)
    mod.ctx_train = ctx.astype(np.int32)
    mod.ens = build_ens(mod, obs, ctx, cfg, simW) if cfg.get("keep_ens", 0) else []
    mod.idx = idx
    mod.al = al
    pair = {}
    cpair = {}
    if cfg.get("poe", 0.0) > 0:
        for o in obs.tolist():
            pr = [(i, x) for i, x in enumerate(o) if x >= 0]
            for i, x in pr:
                for t, y in pr:
                    if t != i:
                        dct = pair.setdefault((i, t), {}).setdefault(x, {})
                        dct[y] = dct.get(y, 0) + 1
        if cfg.get("rctx", 0):
            mod.LF_train = np.concatenate(lfs, axis=0).astype(np.int32)
            mod.RG_train = np.concatenate(rgs, axis=0).astype(np.int32)
            if cfg.get("keep_ens", 0):
                cpair = build_cpair(obs, mod.LF_train, mod.RG_train)
    mod.pair = pair
    mod.cpair = cpair
    # target-language segment bigram model (gap-free reflexes) for string-level decoding
    lm = {}
    if cfg.get("lmw", 0):
        for i, l in enumerate(langs):
            cnt = {}
            for key in sorted(data):
                w = [idx[x] for x in data[key][l] if x in idx]
                if not data[key][l]:
                    continue
                seq = [V] + w + [V]
                for a, b in zip(seq[:-1], seq[1:]):
                    dct = cnt.setdefault(a, {})
                    dct[b] = dct.get(b, 0) + 1
            lm[i] = cnt
    mod.lm = lm
    if al is not None:
        mod.guide, mod.groot = guide, groot
    mod.cfg = dict(cfg)
    mod.ncols = obs.shape[0]
    return mod


def pattern_expert(mod, obs, t, post):
    """Correspondence-pattern nearest neighbours (user-based collaborative filtering: columns are users, languages
    are items): every training column where the target is attested votes for its target symbol with weight
    exp(pmb * (agreements - disagreements)) over the languages visible in the test column; smoothed towards the
    tree posterior with pseudo-count pmk."""
    O = mod.obs_train
    has_t = O[:, t] >= 0
    Ot = O[has_t]
    yt = Ot[:, t]
    beta, kap = mod.cfg.get("pmb", 1.0), mod.cfg.get("pmk", 1.0)
    out = np.empty_like(post)
    for j in range(obs.shape[0]):
        vis = np.where(obs[j] >= 0)[0]
        if len(vis) == 0:
            out[j] = post[j]
            continue
        sub = Ot[:, vis]
        agree = (sub == obs[j, vis][None, :]).sum(axis=1)
        dis = ((sub >= 0) & (sub != obs[j, vis][None, :])).sum(axis=1)
        sc = agree - dis
        m = sc > 0
        if not m.any():
            out[j] = post[j]
            continue
        w = np.exp(beta * (sc[m] - sc[m].max()))
        n = np.bincount(yt[m], weights=w, minlength=mod.V)[:mod.V]
        n = n / n.sum() * min(float(m.sum()), mod.cfg.get("pmn", 10.0))
        out[j] = (n + kap * post[j]) / (n.sum() + kap)
    return out


def predict_row(mod, row, tname):
    langs = mod.langs
    t = langs.index(tname)
    pres = [i for i, l in enumerate(langs) if i != t and row[l] and row[l] != ["?"]]
    if not pres:
        return []
    seqs = [row[langs[i]] for i in pres]
    if mod.cfg.get("aligner") == "own":
        pres, A = own_msa(mod.al, {i: row[langs[i]] for i in pres}, mod.guide, mod.groot, mod.L)
        seqs = [row[langs[i]] for i in pres]
    else:
        A = msa(seqs)
    if mod.cfg.get("merge"):
        A = merge_solo(A, mod.idx)
    C = len(A[0])
    obs = np.full((C, mod.L), -1, dtype=np.int64)
    unk = np.zeros(C, dtype=bool)
    for k, i in enumerate(pres):
        for j in range(C):
            s = A[k][j]
            if s in mod.idx:
                obs[j, i] = mod.idx[s]
    cc = col_ctx(C, mod.K)
    post = ens_posterior(mod, obs, cc, t)
    if mod.cfg["tip_supp"] == "hard":
        post = post * mod.supp[t][None, :]
    post = post / np.maximum(post.sum(axis=1, keepdims=True), 1e-300)
    pt = mod.cfg.get("ptemp", 1.0)
    if pt != 1.0:
        post = np.exp(pt * np.log(np.maximum(post, 1e-300)))
        post = post / post.sum(axis=1, keepdims=True)
    lam = mod.cfg.get("poe", 0.0)
    if lam > 0 and pres:
        # reticulation correction: direct source->target correspondence counts, Dirichlet-smoothed towards the
        # tree posterior, combined over visible sources (weights softmax(-distance/tau)) as a product of experts
        tau, kap = mod.cfg["tau"], mod.cfg["kappa"]
        d = np.array([mod.D[i, t] for i in pres])
        w = np.exp(-(d - d.min()) / tau)
        w = w / w.sum()
        lp = np.zeros_like(post)
        rctx = mod.cfg.get("rctx", 0)
        if rctx:
            LFt, RGt = nb_arrays(pres, A, mod.idx, mod.L, mod.V)
            cb = mod.cfg.get("ctxb", 2.0)
            cp = getattr(mod, "cpair", {})

            def smooth(tab, prior):
                if not tab:
                    return prior
                n = np.zeros(mod.V)
                for y, c in tab.items():
                    n[y] = c
                return (n + cb * prior) / (n.sum() + cb)
        for k, i in enumerate(pres):
            cnt = mod.pair.get((i, t), {})
            for j in range(C):
                x = obs[j, i]
                tab = cnt.get(int(x)) if x >= 0 else None
                if tab:
                    n = np.zeros(mod.V)
                    for y, c in tab.items():
                        n[y] = c
                    pj = (n + kap * post[j]) / (n.sum() + kap)
                    if rctx:
                        l, r = int(LFt[j, i]), int(RGt[j, i])
                        pl = smooth(cp.get((i, t, int(x), l, -1)), pj)
                        pr_ = smooth(cp.get((i, t, int(x), -1, r)), pj)
                        if rctx == 1:
                            pj = smooth(cp.get((i, t, int(x), l, r)), 0.5 * (pl + pr_))
                        elif rctx == 2:
                            pj = 0.5 * (pl + pr_)
                        elif rctx == 3:
                            pj = pr_
                        else:
                            pj = pl
                else:
                    pj = post[j]
                lp[j] += w[k] * np.log(np.maximum(pj, 1e-300))
        lp = (1 - lam) * np.log(np.maximum(post, 1e-300)) + lam * lp
        pmw = mod.cfg.get("pmw", 0.0)
        if pmw > 0:
            lp = lp + pmw * np.log(np.maximum(pattern_expert(mod, obs, t, post), 1e-300))
        lp = lp - lp.max(axis=1, keepdims=True)
        post = np.exp(lp)
        post = post / post.sum(axis=1, keepdims=True)
    dd = np.array([mod.D[i, t] for i in pres])
    ww = np.exp(-(dd - dd.min()) / mod.cfg.get("gtau", mod.cfg["tau"]))
    ww = ww / ww.sum()
    gshare = np.array([sum(ww[k] for k in range(len(pres)) if A[k][j] == "-") for j in range(C)])
    if mod.cfg.get("lmw", 0) and getattr(mod, "lm", None):
        return lm_decode(mod, post, obs, A, pres, seqs, t)
    out = []
    for j in range(C):
        thr = mod.cfg["gap_thr"] if gshare[j] < 0.5 else mod.cfg.get("gap_lo", mod.cfg["gap_thr"])
        if not (obs[j] >= 0).any():
            # every visible segment unknown to the model: copy the first visible non-gap segment
            for k in range(len(pres)):
                if A[k][j] != "-":
                    out.extend(A[k][j].split())
                    break
            continue
        if post[j, 0] > thr:
            continue
        y = 1 + int(np.argmax(post[j, 1:]))
        out.extend(mod.sym[y].split())
    if not out:
        out = list(seqs[0])
    return out


def lm_decode(mod, post, obs, A, pres, seqs, t):
    """Viterbi over columns: each column emits its argmax-candidates (top lmk symbols or the gap) scored by
    log posterior; consecutive emitted symbols are scored by lmw * log P_bigram(b | a) of the target language
    (add-lmb smoothing); the gap bias log(gap_thr ratio) keeps the per-column gap rule as the lmw = 0 limit."""
    V = mod.V
    lmw, k, b = mod.cfg["lmw"], mod.cfg["lmk"], mod.cfg["lmb"]
    cnt = mod.lm.get(t, {})
    tot = {a: sum(d.values()) for a, d in cnt.items()}
    nsym = V + 1

    def lb(a, c):
        d = cnt.get(a, {})
        return np.log((d.get(c, 0) + b / nsym) / (tot.get(a, 0) + b))
    C = post.shape[0]
    thr = mod.cfg["gap_thr"]
    gbias = np.log((1 - thr) / thr)  # gap wins alone iff log p(gap) + gbias > log p(best symbol)
    beams = {V: (0.0, [])}  # last emitted symbol -> (score, symbols)
    for j in range(C):
        lp = np.log(np.maximum(post[j], 1e-300))
        if not (obs[j] >= 0).any():
            for kk in range(len(pres)):
                if A[kk][j] != "-":
                    tok = A[kk][j]
                    beams = {a: (sc, sq + [tok]) for a, (sc, sq) in beams.items()}
                    break
            continue
        cand = [int(y) for y in np.argsort(-lp[1:], kind="stable")[:k] + 1]
        # symbol emission: log P(not gap) + log(p_y / p_best), so with lmw = 0 the gap wins iff p(gap) > gap_thr
        lng = np.log(max(1.0 - post[j, 0], 1e-300))
        nb = {}
        for a, (sc, sq) in beams.items():
            g = sc + lp[0] + gbias
            if a not in nb or g > nb[a][0]:
                nb[a] = (g, sq)
            for y in cand:
                v = sc + lng + lp[y] - lp[cand[0]] + lmw * lb(a, y)
                if y not in nb or v > nb[y][0]:
                    nb[y] = (v, sq + [mod.sym[y]])
        beams = nb
    best = None
    for a, (sc, sq) in beams.items():
        v = sc + lmw * lb(a, V)
        if best is None or v > best[0]:
            best = (v, sq)
    out = []
    for tok in best[1]:
        out.extend(tok.split())
    if not out:
        out = list(seqs[0])
    return out


# ---------------------------------------------------------------- learned logarithmic opinion pool ("stack")
def direct_channel(mod, obs, LFt, RGt, i, t, post):
    """Contextual source i -> target t channel per column, backed off to the context-free table and then to the
    tree posterior (C x V)."""
    kap, cb = mod.cfg["kappa"], mod.cfg.get("ctxb", 2.0)
    cnt = mod.pair.get((i, t), {})
    cp = getattr(mod, "cpair", {})
    C = obs.shape[0]
    out = np.empty_like(post)

    def smooth(tab, prior, b):
        if not tab:
            return prior
        n = np.zeros(mod.V)
        for y, c in tab.items():
            n[y] = c
        return (n + b * prior) / (n.sum() + b)
    for j in range(C):
        x = int(obs[j, i])
        tab = cnt.get(x) if x >= 0 else None
        if not tab:
            out[j] = post[j]
            continue
        pj = smooth(tab, post[j], kap)
        if mod.cfg.get("rctx", 0):
            l, r = int(LFt[j, i]), int(RGt[j, i])
            pl = smooth(cp.get((i, t, x, l, -1)), pj, cb)
            pr_ = smooth(cp.get((i, t, x, -1, r)), pj, cb)
            pj = smooth(cp.get((i, t, x, l, r)), 0.5 * (pl + pr_), cb)
        out[j] = pj
    return out


NRANK = 3


def row_experts(mod, row, t):
    """Experts for target tip t of one row: [tree posterior, direct channel of the 1st..NRANK-th nearest visible
    source (uniform when absent)]. Returns (pres, A, obs, seqs, E) or None."""
    langs = mod.langs
    pres = [i for i, l in enumerate(langs) if i != t and row[l] and row[l] != ["?"]]
    if not pres:
        return None
    pres, A = own_msa(mod.al, {i: row[langs[i]] for i in pres}, mod.guide, mod.groot, mod.L)
    seqs = [row[langs[i]] for i in pres]
    C = len(A[0])
    obs = np.full((C, mod.L), -1, dtype=np.int64)
    for k, i in enumerate(pres):
        for j in range(C):
            if A[k][j] in mod.idx:
                obs[j, i] = mod.idx[A[k][j]]
    cc = col_ctx(C, mod.K)
    post = ens_posterior(mod, obs, cc, t)
    post = post / np.maximum(post.sum(axis=1, keepdims=True), 1e-300)
    LFt, RGt = nb_arrays(pres, A, mod.idx, mod.L, mod.V)
    order = sorted(pres, key=lambda i: (mod.D[i, t], i))
    E = [post]
    uni = np.full_like(post, 1.0 / mod.V)
    for r in range(NRANK):
        E.append(direct_channel(mod, obs, LFt, RGt, order[r], t, post) if r < len(order) else uni)
    return pres, A, obs, seqs, E


def pool(E, w, b):
    s = sum(wi * np.log(np.maximum(e, 1e-300)) for wi, e in zip(w, E))
    s[:, 0] += b
    s = s - s.max(axis=1, keepdims=True)
    p = np.exp(s)
    return p / p.sum(axis=1, keepdims=True)


def gold_columns(mod, A, gold):
    """Index of the gold target symbol at every column of the source alignment A (0 = gap, -1 = unknown symbol);
    gold segments aligned to no source column (insertions) are skipped."""
    R = mod.al.merge([list(r) for r in A], [list(gold)])
    n = len(A)
    y = []
    for c in range(len(R[0])):
        if all(R[k][c] == "-" for k in range(n)):
            continue
        g = R[n][c]
        y.append(0 if g == "-" else mod.idx.get(g, -1))
    return np.array(y, dtype=np.int64)


def fit_pool(langs, data, cfg):
    """Cross-fitted features: K folds over the training sets; for every held-out set and every attested language
    with at least one other attested language, the experts' column distributions and the gold symbol. Then fit the
    pool weights (w >= 0 per expert, gap bias b) by maximum likelihood (L-BFGS-B, small ridge towards the default)."""
    from scipy.optimize import minimize
    keys = sorted(data)
    K = cfg.get("folds", 5)
    feats, ys = [], []
    for f in range(K):
        tr = {k: data[k] for n, k in enumerate(keys) if n % K != f}
        te = [k for n, k in enumerate(keys) if n % K == f]
        m = fit_family(langs, tr, dict(cfg, stack=0))
        finish_model(m)
        for key in te:
            r = data[key]
            pres_all = [i for i, l in enumerate(langs) if r[l]]
            if len(pres_all) < 2:
                continue
            for t in pres_all:
                row = {l: (r[l] if i != t else ["?"]) for i, l in enumerate(langs)}
                res = row_experts(m, row, t)
                if res is None:
                    continue
                pres, A, obs, seqs, E = res
                y = gold_columns(m, A, r[langs[t]])
                if len(y) != len(A[0]):
                    continue
                ok = (y >= 0) & (obs >= 0).any(axis=1)
                if not ok.any():
                    continue
                # map the fold model's symbol indices onto the full-data symbol table by symbol name
                feats.append((m.sym, [e[ok] for e in E], y[ok]))
    return feats


def train_pool_weights(feats, sym_full, cfg):
    from scipy.optimize import minimize
    idx = {s: i for i, s in enumerate(sym_full)}
    V = len(sym_full)
    nE = 1 + NRANK
    Ls, Y = [], []
    for sym, E, y in feats:
        mp = np.array([idx.get(s, -1) for s in sym])
        okc = mp >= 0
        for c in range(len(y)):
            if not okc[y[c]]:
                continue
            M = np.full((nE, V), np.log(1e-12))
            for e in range(nE):
                M[e, mp[okc]] = np.log(np.maximum(E[e][c][okc], 1e-12))
            Ls.append(M)
            Y.append(mp[y[c]])
    if not Ls:
        return [0.5, 0.5, 0.0, 0.0], 0.0, 0
    Lm = np.array(Ls)  # N x nE x V
    Y = np.array(Y)
    N = len(Y)
    w0 = np.array([0.5, 0.5] + [0.0] * (nE - 2) + [0.0])
    reg = cfg.get("pool_reg", 1.0)

    def f(th):
        w, b = th[:nE], th[nE]
        S = np.einsum("e,nev->nv", w, Lm)
        S[:, 0] += b
        mx = S.max(axis=1, keepdims=True)
        P = np.exp(S - mx)
        Z = P.sum(axis=1, keepdims=True)
        P = P / Z
        ll = S[np.arange(N), Y] - (mx[:, 0] + np.log(Z[:, 0]))
        Eexp = np.einsum("nv,nev->ne", P, Lm)
        gw = -(Lm[np.arange(N), :, Y] - Eexp).sum(axis=0)
        gb = -((Y == 0).astype(float) - P[:, 0]).sum()
        val = -ll.sum() + reg * np.sum((th - w0) ** 2)
        g = np.concatenate([gw, [gb]]) + 2 * reg * (th - w0)
        return val, g
    bounds = [(0.0, 5.0)] * nE + [(-10.0, 10.0)]
    r = minimize(f, w0, jac=True, method="L-BFGS-B", bounds=bounds, options={"maxiter": 300})
    th = r.x
    return [float(x) for x in th[:nE]], float(th[nE]), N


def predict_row_stack(mod, row, tname):
    t = mod.langs.index(tname)
    res = row_experts(mod, row, t)
    if res is None:
        return []
    pres, A, obs, seqs, E = res
    post = pool(E, mod.pool_w, mod.pool_b)
    if mod.cfg.get("lmw", 0) and getattr(mod, "lm", None):
        return lm_decode(mod, post, obs, A, pres, seqs, t)
    out = []
    dd = np.array([mod.D[i, t] for i in pres])
    ww = np.exp(-(dd - dd.min()) / mod.cfg.get("gtau", mod.cfg["tau"]))
    ww = ww / ww.sum()
    for j in range(len(A[0])):
        gsh = sum(ww[k] for k in range(len(pres)) if A[k][j] == "-")
        thr = mod.cfg["gap_thr"] if gsh < 0.5 else mod.cfg.get("gap_lo", mod.cfg["gap_thr"])
        if not (obs[j] >= 0).any():
            for k in range(len(pres)):
                if A[k][j] != "-":
                    out.extend(A[k][j].split())
                    break
            continue
        if post[j, 0] > thr:
            continue
        y = 1 + int(np.argmax(post[j, 1:]))
        out.extend(mod.sym[y].split())
    if not out:
        out = list(seqs[0])
    return out


def train(manifest, model_dir, cfg):
    man = json.load(open(manifest))
    models = {}
    for fam in sorted(man["surprise_train"]):
        langs, data = load(man["surprise_train"][fam])
        m = fit_family(langs, data, cfg)
        print("trained", fam, "V=%d cols=%d iters=%d ll=%.1f" % (m.V, m.ncols, m.n_iter, m.ll), flush=True)
        if cfg.get("stack", 0):
            feats = fit_pool(langs, data, cfg)
            m.pool_w, m.pool_b, n = train_pool_weights(feats, m.sym, cfg)
            print("  pool", fam, "N=%d w=%s b=%.3f" % (n, " ".join("%.3f" % x for x in m.pool_w), m.pool_b),
                  flush=True)
        for k in ("P0", "pi0", "ens", "cpair"):
            m.__dict__.pop(k, None)
        models[fam] = m.__dict__
    with open(os.path.join(model_dir, "model.pkl"), "wb") as f:
        pickle.dump({"cfg": cfg, "models": models}, f)


def finish_model(mod):
    """Rebuild the parts not stored in model.pkl (deterministic): the bootstrap tree ensemble and the contextual
    pair tables, from the stored training columns."""
    cfg = mod.cfg
    if cfg.get("boot", 1) > 1 and not getattr(mod, "ens", None):
        mod.ens = build_ens(mod, mod.obs_train.astype(np.int64), mod.ctx_train.astype(np.int64), cfg)
    if cfg.get("rctx", 0) and cfg.get("poe", 0) > 0 and not getattr(mod, "cpair", None):
        mod.cpair = build_cpair(mod.obs_train.astype(np.int64), mod.LF_train, mod.RG_train)


def predict(model_dir, fam, jobs):
    with open(os.path.join(model_dir, "model.pkl"), "rb") as f:
        mod = Model()
        mod.__dict__.update(pickle.load(f)["models"][fam])
    finish_model(mod)
    for ln in open(jobs, encoding="utf-8"):
        inp, outp = ln.rstrip("\n").split("\t")
        langs, data = load(inp)
        with open(outp, "w", encoding="utf-8") as f:
            f.write("COGID\t" + "\t".join(langs) + "\n")
            for key, row in data.items():
                tgt = [l for l in langs if row[l] == ["?"]][0]
                pred = predict_row_stack(mod, row, tgt) if mod.cfg.get("stack", 0) else predict_row(mod, row, tgt)
                f.write(key + "".join("\t" + (" ".join(pred) if l == tgt else "") for l in langs) + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd")
    ap.add_argument("--manifest")
    ap.add_argument("--model-dir")
    ap.add_argument("--family")
    ap.add_argument("--jobs")
    ap.add_argument("--cfg", default="")
    a = ap.parse_args()
    cfg = dict(CFG)
    if a.cfg:
        cfg.update(json.loads(a.cfg))
    if a.cmd == "train":
        train(a.manifest, a.model_dir, cfg)
    else:
        predict(a.model_dir, a.family, a.jobs)
