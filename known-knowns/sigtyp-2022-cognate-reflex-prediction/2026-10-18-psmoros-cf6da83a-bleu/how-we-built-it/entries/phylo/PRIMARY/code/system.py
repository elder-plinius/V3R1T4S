#!/usr/bin/env python3
"""PHYLO lens, run 2026-10-18-0839 (built on the phylo code of runs 2026-10-18-0202 and 2026-10-18-0104): phylogenetic imputation of a masked cognate reflex.

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

CFG.update({"aligner": "own", "bagem": 1, "beta_tip": 0.8, "boot": 20, "gap_lo": 0.2, "poe": 0.6, "rctx": 1, "tau": 0.1, "tctx": 1})  # frozen PRIMARY config (chosen on val-0.50 and my training-0.50 band folds only)


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
        pm = getattr(self, "pmi", None)

        def counts(P, n):
            K = np.zeros((n, nv))
            for r in P:
                for j, t in enumerate(r):
                    if t != "-":
                        K[j, voc[t]] += 1
            return K
        K1, K2 = counts(P1, n1), counts(P2, n2)
        Tl = self.T[np.ix_(cl, cl)] + self.bonus * np.eye(nv)
        if pm is not None:
            pidx, PM, pw = pm
            gi = np.array([pidx.get(t, -1) for t in voc], dtype=np.int64)
            ok = gi >= 0
            if ok.any():
                sub = np.zeros((nv, nv))
                sub[np.ix_(ok, ok)] = PM[np.ix_(gi[ok], gi[ok])]
                Tl = Tl + pw * sub
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


def distances(obs, L, gap, kind=0):
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
            if kind == 1:
                D[a, b] = D[b, a] = 1.0 - ident
            elif kind == 2:
                D[a, b] = D[b, a] = 1.0 - pr
            else:
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
        w = np.array([getattr(m, "ens_weight", 1.0) for m in trees])
    w = w / w.sum()
    post = None
    for wi, m in zip(w, trees):
        if wi < 1e-6:
            continue
        p = wi * target_posterior(m, obs, cc, t)
        post = p if post is None else post + p
    return post


_TONES = set("\u00b9\u00b2\u00b3\u2070\u2074\u2075\u2076\u2077\u2078\u2079")
_VOW = set("aeiouyɑɐɒæɛɜəɘɤɯɪʊʏøœɔɵɨʉɶʌɞɚɝ")


def tok_class(t):
    """1 vowel, 2 consonant, 3 tone (generic IPA symbol classes; no word lists)."""
    if t and set(t) <= _TONES:
        return 3
    for ch in t:
        if ch in _VOW:
            return 1
    return 2


_VOICED = set("bdgɡɖɟɢvzʒʐʑðβɣʁɦ")
_SONOR = set("mnŋɲɳlrɾɹjwʎɭɻʋɰ")
_GLOT = set("ʔh")


def onset_class(t):
    """Coarse phonation / manner class of a syllable onset (generic IPA symbol classes, no word lists):
    0 none (vowel-initial syllable), 1 voiceless, 2 aspirated, 3 voiced obstruent, 4 sonorant, 5 glottal."""
    if t is None or tok_class(t) == 1:
        return 0
    if "ʰ" in t:
        return 2
    c = t[0]
    if c in _GLOT:
        return 5
    if c in _SONOR:
        return 4
    if c in _VOICED or "\u0324" in t:
        return 3
    return 1


def col_ctx_aln(A, K):
    """Context class of every column of alignment A: with K = 4 the majority symbol class (1 vowel, 2 consonant,
    3 tone) of the next column, 0 at the right word edge; with K = 7 (H12, a partitioned model as for codon
    positions in molecular phylogenetics) tone columns get 1 + the majority onset class of their syllables, other
    columns 0; else positions (col_ctx)."""
    C = len(A[0])
    if K == 7:
        out = np.zeros(C, dtype=np.int64)
        for j in range(C):
            votes = [tok_class(r[j]) for r in A if r[j] != "-"]
            if not votes or max(set(votes), key=lambda v: (votes.count(v), -v)) != 3:
                continue
            oc = []
            for r in A:
                if r[j] == "-" or tok_class(r[j]) != 3:
                    continue
                q = j - 1
                first = None
                while q >= 0 and (r[q] == "-" or tok_class(r[q]) != 3):
                    if r[q] != "-":
                        first = r[q]
                    q -= 1
                oc.append(onset_class(first))
            if oc:
                out[j] = 1 + max(set(oc), key=lambda v: (oc.count(v), -v))
        return out
    if K != 4:
        return col_ctx(C, K)
    cls = []
    for j in range(C):
        votes = [tok_class(r[j]) for r in A if r[j] != "-"]
        cls.append(max(set(votes), key=lambda v: (votes.count(v), -v)) if votes else 0)
    out = np.zeros(C, dtype=np.int64)
    for j in range(C):
        nxt = [cls[q] for q in range(j + 1, C) if cls[q] > 0]
        out[j] = nxt[0] if nxt else 0
    return out


def col_ctx(C, K):
    """Context class of each of C columns: 0 initial, 1 medial, 2 final (K=3); all 0 when K=1."""
    if K == 1:
        return np.zeros(C, dtype=np.int64)
    c = np.ones(C, dtype=np.int64)
    c[-1] = 2
    c[0] = 0
    return c


_TCTX = [0, 0]  # from the model config: [tctx, sskip] (tone onset context; segment contexts skip tone tokens)


def nb_arrays(pres, A, idx, L, V):
    """Left / right neighbour symbol (index; V = word boundary, V + 1 = unknown symbol) of every visible row at every
    column of alignment A (rows in the order of pres); -1 where the language is absent. With _TCTX[0] = 1 the left
    context of a tone token is the onset of its syllable (first segment after the previous tone or the word start):
    tone splits conditioned by the initial consonant."""
    C = len(A[0])
    LF = np.full((C, L), -1, dtype=np.int64)
    RG = np.full((C, L), -1, dtype=np.int64)
    tctx = _TCTX[0]
    sskip = _TCTX[1]
    for k, i in enumerate(pres):
        prev = V
        prev_seg = V
        onset = None
        tone_prev = {}
        for j in range(C):
            tok = A[k][j]
            istone = tok != "-" and tok_class(tok) == 3
            if tctx and istone:
                LF[j, i] = onset if onset is not None else prev
                tone_prev[j] = prev
            elif sskip and not istone:
                LF[j, i] = prev_seg
            else:
                LF[j, i] = prev
            if tok != "-":
                prev = idx.get(tok, V + 1)
                if not istone:
                    prev_seg = prev
                if tctx:
                    if istone:
                        onset = None
                    elif onset is None:
                        onset = prev
        nxt = V
        nxt_seg = V
        for j in range(C - 1, -1, -1):
            tok = A[k][j]
            istone = tok != "-" and tok_class(tok) == 3
            RG[j, i] = nxt_seg if (sskip and not istone) else nxt
            if tok != "-":
                nxt = idx.get(tok, V + 1)
                if not istone:
                    nxt_seg = nxt
        if tctx == 2:
            # tctx 2: a tone's right context slot holds the segment just before it (rhyme / coda: checked syllables)
            for j, pv in tone_prev.items():
                RG[j, i] = pv
    return LF, RG


def init_tree(m, children, root, L, V, K, supp, cfg, simW=None, Ppool=None):
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
            sm = cfg.get("suppmix", 0.5)
            u = (1 - sm) / V + sm * sc / sc.sum()
            if simW is not None:
                Q = u[None, :] * simW
                Q = Q / Q.sum(axis=1, keepdims=True)
                P = (1 - bt) * Q + bt * np.eye(V)
            else:
                rho = cfg.get("pool_prior", 0.0)
                if rho > 0 and Ppool is not None:
                    P = np.tile(u * (1 - bt), (V, 1)) + bt * ((1 - rho) * np.eye(V) + rho * Ppool)
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
        if cfg.get("blockboot", 0) and getattr(mod, "set_train", None) is not None:
            # block bootstrap: resample whole cognate sets (all their columns together)
            sid = mod.set_train
            nset = int(sid.max()) + 1
            starts = np.searchsorted(sid, np.arange(nset))
            ends = np.searchsorted(sid, np.arange(nset), side="right")
            pick = rng.randint(0, nset, nset)
            sel = np.concatenate([np.arange(starts[q], ends[q]) for q in pick])
        elif cfg.get("cw", 0.0) > 0:
            # completeness-weighted bagging (importance weighting towards the most complete sets of the test split)
            nat = (obs >= 0).sum(axis=1).astype(float)
            pw = nat ** cfg["cw"]
            pw = pw / pw.sum()
            sel = rng.choice(obs.shape[0], max(10, int(round(cfg.get("bagfrac", 1.0) * obs.shape[0]))), p=pw)
        else:
            sel = rng.randint(0, obs.shape[0], max(10, int(round(cfg.get("bagfrac", 1.0) * obs.shape[0]))))
        ncdD = getattr(mod, "ncd_boot", None)
        nf = cfg.get("ncd_frac", 0.0)
        if nf > 0 and ncdD and (bb % max(1, int(round(1.0 / nf))) == 0) and (bb - 1) < len(ncdD) * max(1, int(round(1.0 / nf))):
            # tree mixture: this bag member's topology from NCD on a bootstrap resample of cognate sets
            chb, rootb, _ = nj_tree(ncdD[(bb // max(1, int(round(1.0 / nf)))) - 1])
        else:
            chb, rootb, _ = nj_tree(distances(obs[sel], mod.L, 0, (bb % 3) if cfg.get("distmix", 0) else 0))
        sub = Model()
        sub.tol = mod.tol
        init_tree(sub, chb, rootb, mod.L, mod.V, mod.K, mod.supp, cfg, simW, getattr(mod, "Ppool", None))
        if cfg.get("bagem", 0):
            em_fit(sub, obs[sel], ctx[sel], cfg["iters"], cfg["alpha"], cfg["gamma"])
        else:
            em_fit(sub, obs, ctx, cfg["iters"], cfg["alpha"], cfg["gamma"])
        for k in ("P0", "pi0"):
            sub.__dict__.pop(k, None)
        ens.append(sub)
    nw = cfg.get("ncd_member", 0)
    if nw and getattr(mod, "Dncd", None) is not None:
        chn, rootn, _ = nj_tree(mod.Dncd)
        sub = Model()
        sub.tol = mod.tol
        init_tree(sub, chn, rootn, mod.L, mod.V, mod.K, mod.supp, cfg, simW, getattr(mod, "Ppool", None))
        em_fit(sub, obs, ctx, cfg["iters"], cfg["alpha"], cfg["gamma"])
        for k in ("P0", "pi0"):
            sub.__dict__.pop(k, None)
        sub.ens_weight = float(nw)
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


def ncd_distances(langs, data, keys=None):
    """Normalised compression distance (zlib) between the languages' word lists restricted, for each pair, to the
    cognate sets both attest, in COGID order (Cilibrasi and Vitanyi 2005); `keys` (with repeats) = a bootstrap
    resample of the cognate sets."""
    import zlib
    L = len(langs)
    D = np.zeros((L, L))
    keys = sorted(data) if keys is None else keys

    def c(b):
        return len(zlib.compress(b, 9))
    for a in range(L):
        for b in range(a + 1, L):
            ks = [k for k in keys if data[k][langs[a]] and data[k][langs[b]]]
            if len(ks) < 5:
                D[a, b] = D[b, a] = 1.0
                continue
            xa = "|".join(" ".join(data[k][langs[a]]) for k in ks).encode("utf-8")
            xb = "|".join(" ".join(data[k][langs[b]]) for k in ks).encode("utf-8")
            xab = "|".join(" ".join(data[k][langs[a]]) + "#" + " ".join(data[k][langs[b]]) for k in ks).encode("utf-8")
            ca, cb = c(xa), c(xb)
            D[a, b] = D[b, a] = (c(xab) - min(ca, cb)) / max(ca, cb)
    return D


def nearest(D, pres, t):
    return min(pres, key=lambda i: (D[i, t], i))


def build_edge(alns, D, L):
    """Word-edge insertion tables (H10): for every training set, every attested target t with other attested
    languages V, the nearest member i of V (distance D) and i reaching the edge of V's material: t's segments before
    the first / after the last column where some member of V has a segment, keyed by (t, i) and i's edge segment.
    Returns {"suf"|"pre": {(t, i): {x: {string: count}}}}."""
    out = {"suf": {}, "pre": {}}
    for pres, A in alns:
        if len(pres) < 2:
            continue
        C = len(A[0])
        for kt, t in enumerate(pres):
            V = [k for k in range(len(pres)) if k != kt]
            cols = [j for j in range(C) if any(A[k][j] != "-" for k in V)]
            if not cols:
                continue
            f0, f1 = cols[0], cols[-1]
            i = nearest(D, [pres[k] for k in V], t)
            ki = pres.index(i)
            for side, edgecol, span in (("suf", f1, range(f1 + 1, C)), ("pre", f0, range(0, f0))):
                if A[ki][edgecol] == "-":
                    continue
                x = A[ki][edgecol]
                st = " ".join(A[kt][j] for j in span if A[kt][j] != "-")
                dct = out[side].setdefault((t, i), {}).setdefault(x, {})
                dct[st] = dct.get(st, 0) + 1
    return out


def edge_choice(mod, side, t, i, x):
    """Most probable edge string for target t given nearest source i with edge segment x: context counts smoothed
    (pseudo-count cfg edge) towards the pair's counts over all x (which are smoothed towards the empty string)."""
    tabs = mod.edge[side].get((t, i))
    if not tabs:
        return ""
    pair = {}
    for d in tabs.values():
        for k, c in d.items():
            pair[k] = pair.get(k, 0) + c
    npair = sum(pair.values())
    b0 = mod.cfg.get("edge_b0", 1.0)
    bias = mod.cfg.get("edge_bias", 1.0)
    pp = {k: (c + (b0 if k == "" else 0.0)) / (npair + b0) for k, c in pair.items()}
    pp.setdefault("", b0 / (npair + b0))
    ctx = tabs.get(x, {})
    nc = sum(ctx.values())
    beta = mod.cfg["edge"]
    sc = {k: (ctx.get(k, 0) + beta * v) / (nc + beta) for k, v in pp.items()}
    sc[""] *= bias
    return max(sorted(sc), key=lambda k: sc[k])


def fit_family(langs, data, cfg):
    _TCTX[0], _TCTX[1] = int(cfg.get("tctx", 0)), int(cfg.get("sskip", 0))
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
    if al is not None and cfg.get("realign", 0):
        # learned correspondence scores (PMI of segments sharing a column, pooled over language pairs), added to the
        # SCA scores; then every training set is re-aligned with them (and the test rows at predict time)
        toks = sorted(syms)
        pidx = {t: i for i, t in enumerate(toks)}
        Cn = np.zeros((len(toks), len(toks)))
        for pres_, A in alns:
            for j in range(len(A[0])):
                col = [pidx[A[k][j]] for k in range(len(A)) if A[k][j] != "-" and A[k][j] in pidx]
                for a in range(len(col)):
                    for b in range(a + 1, len(col)):
                        Cn[col[a], col[b]] += 1
                        Cn[col[b], col[a]] += 1
        Cn = Cn + cfg.get("pmi_eps", 0.1)
        mrg = Cn.sum(axis=1)
        PM = np.log(Cn * Cn.sum() / np.outer(mrg, mrg))
        PM = np.clip(PM, -cfg.get("pmi_clip", 3.0), cfg.get("pmi_clip", 3.0))
        al.pmi = (pidx, PM, cfg.get("pmiw", 2.0))
        alns = []
        for key in sorted(data):
            r = data[key]
            pres = [i for i, l in enumerate(langs) if r[l]]
            if len(pres) < 2:
                continue
            pres, A = own_msa(al, {i: r[langs[i]] for i in pres}, guide, groot, L)
            alns.append((pres, A))
    sym = ["-"] + sorted(syms)
    idx = {s: i for i, s in enumerate(sym)}
    V = len(sym)
    K = 7 if cfg["ctx"] == 3 else (4 if cfg["ctx"] == 2 else (3 if cfg["ctx"] else 1))
    cols, ctxs, lfs, rgs = [], [], [], []
    setid = []
    for si, (pres, A) in enumerate(alns):
        setid.extend([si] * len(A[0]))
        ctxs.extend(col_ctx_aln(A, K).tolist())
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
    edge = build_edge(alns, D, L) if cfg.get("edge", 0) else None
    if cfg["tree"] == "star":
        children, root, N = star_tree(L)
    elif al is not None and cfg["tree"] == "guide":
        children, root = guide, groot
    elif cfg["tree"] == "ncd":
        children, root, N = nj_tree(ncd_distances(langs, data))
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

    Ppool = None
    if cfg.get("pool_prior", 0.0) > 0:
        # family-pooled correspondence table: segments sharing a column, over all ordered language pairs
        Cn = np.zeros((V, V))
        for a in range(L):
            for b in range(L):
                if a == b:
                    continue
                m_ = (obs[:, a] > 0) & (obs[:, b] > 0)
                if m_.any():
                    np.add.at(Cn, (obs[m_, a], obs[m_, b]), 1.0)
        Cn[0, 0] = 1.0
        Cn = Cn + 0.01
        Ppool = Cn / Cn.sum(axis=1, keepdims=True)
    mod = Model()
    mod.sym, mod.langs = sym, langs
    mod.Ppool = Ppool
    init_tree(mod, children, root, L, V, K, supp, cfg, simW, Ppool)
    mod.D = D
    mod.edge = edge
    mod.Dncd = ncd_distances(langs, data) if cfg.get("ncd_member", 0) else None
    mod.ncd_boot = None
    if cfg.get("ncd_frac", 0.0) > 0 and cfg.get("boot", 1) > 1:
        nb = int((cfg["boot"] - 1) // max(1, int(round(1.0 / cfg["ncd_frac"]))))
        rng2 = np.random.RandomState(cfg.get("seed", 20261018) + 7)
        ks = sorted(data)
        mats = []
        for _ in range(nb):
            pick = sorted(rng2.randint(0, len(ks), len(ks)).tolist())
            mats.append(ncd_distances(langs, data, [ks[q] for q in pick]))
        mod.ncd_boot = mats
    mod.supp = supp
    mod.tol = cfg.get("tol", 1e-4)
    em_fit(mod, obs, ctx, cfg["iters"], cfg["alpha"], cfg["gamma"])
    mod.obs_train = obs.astype(np.int32)
    mod.set_train = np.array(setid, dtype=np.int32)
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


def joint_table(mod, i, s, t):
    """Counts of the target symbol y for every (x_i, x_s) pair of training columns where i, s and t are attested
    (two-source joint channel; computed from the stored training columns, cached per (i, s, t): a pure function of
    the model, so the cache never carries information between rows)."""
    jc = mod.__dict__.setdefault("_j2", {})
    key = (i, s, t)
    if key not in jc:
        O = mod.obs_train
        m = (O[:, i] >= 0) & (O[:, s] >= 0) & (O[:, t] >= 0)
        tab = {}
        for xi, xs, y in zip(O[m, i].tolist(), O[m, s].tolist(), O[m, t].tolist()):
            dct = tab.setdefault((xi, xs), {})
            dct[y] = dct.get(y, 0) + 1
        jc[key] = tab
    return jc[key]


def source_logs(mod, post, obs, A, pres, t, C):
    """Log direct-channel distribution (C x V) of every visible source (in the order of pres): source -> target
    counts smoothed towards the tree posterior, then the contextual back-off (rctx), then (cfg j2 > 0) the two-source
    joint channel for the nearest source."""
    kap = mod.cfg["kappa"]
    rctx = mod.cfg.get("rctx", 0)
    j2 = mod.cfg.get("j2", 0.0)
    knear, ssec = None, None
    if j2 > 0 and len(pres) >= 2:
        order = sorted(range(len(pres)), key=lambda k: (mod.D[pres[k], t], pres[k]))
        knear, ssec = order[0], pres[order[1]]
    if rctx:
        LFt, RGt = nb_arrays(pres, A, mod.idx, mod.L, mod.V)
        cb = mod.cfg.get("ctxb", 2.0)
        cp = getattr(mod, "cpair", {})

    def smooth(tab, prior, b=None):
        if not tab:
            return prior
        n = np.zeros(mod.V)
        for y, c in tab.items():
            n[y] = c
        b = cb if b is None else b
        return (n + b * prior) / (n.sum() + b)
    logs = []
    for k, i in enumerate(pres):
        cnt = mod.pair.get((i, t), {})
        jt = joint_table(mod, i, ssec, t) if k == knear else None
        lk = np.empty_like(post)
        for j in range(C):
            x = obs[j, i]
            tab = cnt.get(int(x)) if x >= 0 else None
            if tab:
                n = np.zeros(mod.V)
                for y, c in tab.items():
                    n[y] = c
                di = mod.cfg.get("dident", 0.0)
                if di > 0 and x > 0 and mod.supp[t][x]:
                    n[x] += di
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
                if jt is not None and obs[j, ssec] >= 0:
                    pj = smooth(jt.get((int(x), int(obs[j, ssec]))), pj, j2)
            else:
                pj = post[j]
            lk[j] = np.log(np.maximum(pj, 1e-300))
        logs.append(lk)
    return logs


def poe_combine(mod, post, obs, A, pres, t, C):
    pt = mod.cfg.get("ptemp", 1.0)
    if pt != 1.0:
        post = np.exp(pt * np.log(np.maximum(post, 1e-300)))
        post = post / post.sum(axis=1, keepdims=True)
    lam = mod.cfg.get("poe", 0.0)
    if lam > 0 and pres:
        # reticulation correction: direct source->target correspondence counts, Dirichlet-smoothed towards the
        # tree posterior, combined over visible sources (weights softmax(-distance/tau)) as a product of experts
        tau = mod.cfg["tau"]
        d = np.array([mod.D[i, t] for i in pres])
        w = np.exp(-(d - d.min()) / tau)
        w = w / w.sum()
        lp = np.zeros_like(post)
        for k, lk in enumerate(source_logs(mod, post, obs, A, pres, t, C)):
            lp += w[k] * lk
        if mod.cfg.get("poe_lin", 0):
            # linear opinion pool instead of the logarithmic one
            dp = np.exp(lp - lp.max(axis=1, keepdims=True))
            dp = dp / dp.sum(axis=1, keepdims=True)
            lp = np.log(np.maximum((1 - lam) * post + lam * dp, 1e-300))
        else:
            lp = (1 - lam) * np.log(np.maximum(post, 1e-300)) + lam * lp
        pmw = mod.cfg.get("pmw", 0.0)
        if pmw > 0:
            lp = lp + pmw * np.log(np.maximum(pattern_expert(mod, obs, t, post), 1e-300))
        lp = lp - lp.max(axis=1, keepdims=True)
        post = np.exp(lp)
        post = post / post.sum(axis=1, keepdims=True)
    return post


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
    cc = col_ctx_aln(A, mod.K)
    if mod.cfg.get("bagpoe", 0):
        # bagging of the whole predictor: PoE per tree member, then the average of the members' distributions
        acc = None
        trees = [mod] + list(getattr(mod, "ens", []))
        for m in trees:
            pm = target_posterior(m, obs, cc, t)
            pm = pm / np.maximum(pm.sum(axis=1, keepdims=True), 1e-300)
            pm = poe_combine(mod, pm, obs, A, pres, t, C)
            acc = pm if acc is None else acc + pm
        post = acc / len(trees)
    else:
        post = ens_posterior(mod, obs, cc, t)
        if mod.cfg["tip_supp"] == "hard":
            post = post * mod.supp[t][None, :]
        post = post / np.maximum(post.sum(axis=1, keepdims=True), 1e-300)
        post = poe_combine(mod, post, obs, A, pres, t, C)
    dd = np.array([mod.D[i, t] for i in pres])
    ww = np.exp(-(dd - dd.min()) / mod.cfg.get("gtau", mod.cfg["tau"]))
    ww = ww / ww.sum()
    gshare = np.array([sum(ww[k] for k in range(len(pres)) if A[k][j] == "-") for j in range(C)])
    if mod.cfg.get("glo_edge", 0):
        # gap_lo only outside the span of the nearest source (edge material: affixes), not word-internally
        kn = int(np.argmax(ww))
        nz = [j for j in range(C) if A[kn][j] != "-"]
        if nz:
            inside = np.array([nz[0] <= j <= nz[-1] for j in range(C)])
            gshare = np.where(inside, 0.0, gshare)
    if mod.cfg.get("lmw", 0) and getattr(mod, "lm", None):
        thrs = [mod.cfg["gap_thr"] if gshare[j] < 0.5 else mod.cfg.get("gap_lo", mod.cfg["gap_thr"]) for j in range(C)]
        return lm_decode(mod, post, obs, A, pres, seqs, t, thrs)
    out = []
    choice = []  # per column: fixed token list, or the chosen symbol index (0 = gap)
    for j in range(C):
        thr = mod.cfg["gap_thr"] if gshare[j] < 0.5 else mod.cfg.get("gap_lo", mod.cfg["gap_thr"])
        if not (obs[j] >= 0).any():
            # every visible segment unknown to the model: copy the first visible non-gap segment
            for k in range(len(pres)):
                if A[k][j] != "-":
                    out.extend(A[k][j].split())
                    choice.append(A[k][j].split())
                    break
            else:
                choice.append([])
            continue
        if post[j, 0] > thr:
            choice.append(0)
            continue
        y = 1 + int(np.argmax(post[j, 1:]))
        out.extend(mod.sym[y].split())
        choice.append(y)
    if mod.cfg.get("mbr", 0) and out:
        out = mbr_decode(mod, post, choice, row) or out
    if mod.cfg.get("edge", 0) and getattr(mod, "edge", None) and out:
        i = nearest(mod.D, pres, t)
        ki = pres.index(i)
        if A[ki][C - 1] != "-":
            suf = edge_choice(mod, "suf", t, i, A[ki][C - 1])
            if suf:
                out = out + suf.split()
        if A[ki][0] != "-" and mod.cfg.get("edge_pre", 1):
            pre = edge_choice(mod, "pre", t, i, A[ki][0])
            if pre:
                out = pre.split() + out
    if not out:
        out = list(seqs[0])
    return out


def item_ned(a, b):
    """Edit-distance alignment (unit costs): mismatched positions / alignment length."""
    n, m = len(a), len(b)
    if n == 0 and m == 0:
        return 0.0
    D = [[(0, 0)] * (m + 1) for _ in range(n + 1)]  # (cost, length)
    for i in range(1, n + 1):
        D[i][0] = (i, i)
    for j in range(1, m + 1):
        D[0][j] = (j, j)
    for i in range(1, n + 1):
        ai = a[i - 1]
        for j in range(1, m + 1):
            c0, l0 = D[i - 1][j - 1]
            c1, l1 = D[i - 1][j]
            c2, l2 = D[i][j - 1]
            D[i][j] = min((c0 + (ai != b[j - 1]), l0 + 1), (c1 + 1, l1 + 1), (c2 + 1, l2 + 1))
    c, l = D[n][m]
    return c / l


def mbr_decode(mod, post, choice, row):
    """Minimum-Bayes-risk choice under item NED: candidates flip the decision in the most uncertain columns (top-2
    options each); the risk of a candidate is its mean NED against strings sampled from the column distributions
    (independent columns; RNG seeded from the row's own content, so nothing depends on other rows)."""
    U, M = mod.cfg.get("mbr_u", 4), mod.cfg.get("mbr_m", 64)
    cols = [j for j, c in enumerate(choice) if not isinstance(c, list)]
    if not cols:
        return None
    unc = []
    for j in cols:
        p = post[j]
        order = np.argsort(-p, kind="stable")
        cur = choice[j]
        alt = int(order[0]) if int(order[0]) != cur else int(order[1])
        unc.append((p[cur], j, alt))
    unc.sort()
    flips = [(j, alt) for pc, j, alt in unc[:U] if pc < mod.cfg.get("mbr_conf", 0.8)]
    if not flips:
        return None
    key = "|".join(" ".join(row[l]) for l in mod.langs)
    rng = np.random.RandomState(hash_tok(key) % (2 ** 31))
    samples = []
    cum = {j: np.cumsum(post[j]) for j in cols}
    for _ in range(M):
        sq = []
        for j, c in enumerate(choice):
            if isinstance(c, list):
                sq.extend(c)
            else:
                y = int(np.searchsorted(cum[j], rng.random_sample() * cum[j][-1]))
                y = min(y, mod.V - 1)
                if y > 0:
                    sq.extend(mod.sym[y].split())
        samples.append(sq)
    best = None
    for mask in range(1 << len(flips)):
        ch = list(choice)
        for b, (j, alt) in enumerate(flips):
            if mask >> b & 1:
                ch[j] = alt
        cand = []
        for c in ch:
            if isinstance(c, list):
                cand.extend(c)
            elif c > 0:
                cand.extend(mod.sym[c].split())
        if not cand:
            continue
        r = sum(item_ned(cand, s_) for s_ in samples) / M
        if best is None or r < best[0] - 1e-12:
            best = (r, cand)
    return best[1] if best else None


def lm_decode(mod, post, obs, A, pres, seqs, t, thrs=None):
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
    gbias = np.log((1 - thr) / thr)
    tonly = mod.cfg.get("lmtone", 0)
    TONES = set("\u00b9\u00b2\u00b3\u2070\u2074\u2075\u2076\u2077\u2078\u2079")
    istone = [bool(x) and x != "-" and set(x.replace(" ", "")) <= TONES for x in mod.sym]  # gap wins alone iff log p(gap) + gbias > log p(best symbol)
    beams = {V: (0.0, [])}  # last emitted symbol -> (score, symbols)
    for j in range(C):
        if thrs is not None:
            gbias = np.log((1 - thrs[j]) / thrs[j])
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
                lmt = lmw * lb(a, y) if (not tonly or istone[y]) else 0.0
                v = sc + lng + lp[y] - lp[cand[0]] + lmt
                if y not in nb or v > nb[y][0]:
                    nb[y] = (v, sq + [mod.sym[y]])
        beams = nb
    best = None
    for a, (sc, sq) in beams.items():
        v = sc + (lmw * lb(a, V) if not tonly else 0.0)
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
    cc = col_ctx_aln(A, mod.K)
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
        m = fit_family(langs, tr, dict(cfg, stack=0, boot=cfg.get("pool_boot", cfg.get("boot", 1))))
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
    bounds = [(0.0, 5.0)] * nE + ([(0.0, 0.0)] if cfg.get("pool_nob", 0) else [(-10.0, 10.0)])
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
        cf = dict(cfg)
        cf.update(cfg.get("fam_cfg", {}).get(fam, {}))
        m = fit_family(langs, data, cf)
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
    _TCTX[0], _TCTX[1] = int(cfg.get("tctx", 0)), int(cfg.get("sskip", 0))
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
