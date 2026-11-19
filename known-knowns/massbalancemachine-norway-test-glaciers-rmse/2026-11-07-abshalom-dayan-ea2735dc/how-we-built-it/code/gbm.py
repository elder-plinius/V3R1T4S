"""Histogram gradient boosting in numpy with MBM's aggregated objective.

Each row is one month; a group (point balance) is the set of rows sharing an id. Loss = 0.5 * sum_g (sum_{i in g} f_i - y_g)^2,
so the gradient of row i is (S_g - y_g) and, as in MBM's custom objective, the hessian is 1 per row.
Trees are XGBoost-style: leaf weight -G/(H+lambda), split gain G_L^2/(H_L+l) + G_R^2/(H_R+l) - G^2/(H+l), depth-wise growth.
Optional monotone constraints (+1/-1 per feature) are enforced by bounding child weights, as XGBoost does.
"""
import numpy as np

NB = 128


def make_bins(X, nb=NB):
    edges = []
    for j in range(X.shape[1]):
        q = np.unique(np.quantile(X[:, j], np.linspace(0, 1, nb + 1)[1:-1]))
        edges.append(q)
    return edges


def apply_bins(X, edges):
    B = np.empty(X.shape, dtype=np.int32)
    for j, e in enumerate(edges):
        B[:, j] = np.searchsorted(e, X[:, j], side="right")  # bin b means e[b-1] <= x < e[b]
    return B


class GBM:
    def __init__(self, n_trees=300, lr=0.05, depth=5, lam=1.0, min_child=0.0, gamma=0.0, subsample=1.0,
                 colsample=1.0, monotone=None, seed=0, base=0.0):
        self.__dict__.update(dict(n_trees=n_trees, lr=lr, depth=depth, lam=lam, min_child=min_child, gamma=gamma,
                                  subsample=subsample, colsample=colsample, monotone=monotone, seed=seed, base=base))

    def fit(self, X, gid, y_group_row, edges=None, init=None):
        rng = np.random.default_rng(self.seed)
        self.edges = edges if edges is not None else make_bins(X)
        B = apply_bins(X, self.edges)
        n, p = B.shape
        uid, inv = np.unique(gid, return_inverse=True)
        G = len(uid)
        yg = np.bincount(inv, weights=y_group_row, minlength=G) / np.bincount(inv, minlength=G)
        f = np.full(n, self.base) if init is None else self.base + np.asarray(init, float).copy()
        mono = np.zeros(p, int) if self.monotone is None else np.asarray(self.monotone)
        self.trees = []
        for t in range(self.n_trees):
            S = np.bincount(inv, weights=f, minlength=G)
            g = (S - yg)[inv]
            h = np.ones(n)
            if self.subsample < 1:
                keep_g = rng.random(G) < self.subsample
                w = keep_g[inv].astype(float)
                g = g * w; h = h * w
            cols = np.arange(p) if self.colsample >= 1 else np.sort(rng.choice(p, max(1, int(round(self.colsample * p))), replace=False))
            tree = self._grow(B, g, h, cols, mono)
            self.trees.append(tree)
            f += self._predict_tree(tree, B)
        return self

    def _grow(self, B, g, h, cols, mono):
        n = len(g); lam = self.lam
        # node arrays: feature, bin threshold (go left if bin <= thr), left, right, value
        feat = [-1]; thr = [0]; left = [-1]; right = [-1]; val = [0.0]; lo = [-np.inf]; hi = [np.inf]
        node = np.zeros(n, dtype=np.int64)
        frontier = [0]
        Gs = [g.sum()]; Hs = [h.sum()]
        for d in range(self.depth):
            if not frontier:
                break
            fr = np.array(frontier)
            pos = -np.ones(len(feat), dtype=np.int64); pos[fr] = np.arange(len(fr))
            active = pos[node] >= 0
            ra = np.nonzero(active)[0]; pn = pos[node[ra]]
            best = [(0.0, -1, -1)] * len(fr)
            bestgain = np.full(len(fr), self.gamma + 1e-12); bestf = -np.ones(len(fr), int); bestb = -np.ones(len(fr), int)
            bestw = [None] * len(fr)
            for j in cols:
                key = pn * (NB + 1) + B[ra, j]
                gh = np.bincount(key, weights=g[ra], minlength=len(fr) * (NB + 1)).reshape(len(fr), NB + 1)
                hh = np.bincount(key, weights=h[ra], minlength=len(fr) * (NB + 1)).reshape(len(fr), NB + 1)
                GL = np.cumsum(gh, 1)[:, :-1]; HL = np.cumsum(hh, 1)[:, :-1]
                Gt = gh.sum(1)[:, None]; Ht = hh.sum(1)[:, None]
                GR = Gt - GL; HR = Ht - HL
                ok = (HL > max(self.min_child, 1e-9)) & (HR > max(self.min_child, 1e-9))
                wl = -GL / (HL + lam); wr = -GR / (HR + lam)
                if mono[j] != 0:
                    ok &= (wr - wl) * mono[j] >= 0
                gain = np.where(ok, GL ** 2 / (HL + lam) + GR ** 2 / (HR + lam) - Gt ** 2 / (Ht + lam), -np.inf)
                bi = np.argmax(gain, 1); bg = gain[np.arange(len(fr)), bi]
                better = bg > bestgain
                bestgain[better] = bg[better]; bestf[better] = j; bestb[better] = bi[better]
            new_frontier = []
            for k, nd in enumerate(fr):
                if bestf[k] < 0:
                    continue
                feat[nd] = int(bestf[k]); thr[nd] = int(bestb[k])
                for side in (0, 1):
                    feat.append(-1); thr.append(0); left.append(-1); right.append(-1); val.append(0.0)
                    lo.append(lo[nd]); hi.append(hi[nd])
                left[nd] = len(feat) - 2; right[nd] = len(feat) - 1
                new_frontier += [left[nd], right[nd]]
            if not new_frontier:
                break
            # route rows of split nodes
            sp = np.array([nd for nd in fr if feat[nd] >= 0])
            isp = np.zeros(len(feat), bool); isp[sp] = True
            r = np.nonzero(isp[node])[0]
            fa = np.array(feat); ta = np.array(thr); la = np.array(left); rr = np.array(right)
            nn = node[r]
            goL = B[r, fa[nn]] <= ta[nn]
            node[r] = np.where(goL, la[nn], rr[nn])
            # monotone bounds for children
            for nd in sp:
                j = feat[nd]
                if mono[j] != 0:
                    m = node == left[nd]; wl = -g[m].sum() / (h[m].sum() + lam)
                    m2 = node == right[nd]; wr = -g[m2].sum() / (h[m2].sum() + lam)
                    mid = 0.5 * (wl + wr)
                    if mono[j] > 0:
                        hi[left[nd]] = min(hi[nd], mid); lo[right[nd]] = max(lo[nd], mid)
                    else:
                        lo[left[nd]] = max(lo[nd], mid); hi[right[nd]] = min(hi[nd], mid)
            frontier = new_frontier
        # leaf values
        Gl = np.bincount(node, weights=g, minlength=len(feat)); Hl = np.bincount(node, weights=h, minlength=len(feat))
        for nd in range(len(feat)):
            if feat[nd] < 0:
                w = -Gl[nd] / (Hl[nd] + lam)
                val[nd] = self.lr * float(np.clip(w, lo[nd], hi[nd]))
        return (np.array(feat), np.array(thr), np.array(left), np.array(right), np.array(val))

    @staticmethod
    def _predict_tree(tree, B):
        feat, thr, left, right, val = tree
        node = np.zeros(len(B), dtype=np.int64)
        for _ in range(64):
            internal = feat[node] >= 0
            if not internal.any():
                break
            r = np.nonzero(internal)[0]; nn = node[r]
            node[r] = np.where(B[r, feat[nn]] <= thr[nn], left[nn], right[nn])
        return val[node]

    def predict(self, X, init=None):
        B = apply_bins(X, self.edges)
        out = np.full(len(B), self.base) if init is None else self.base + np.asarray(init, float).copy()
        for t in self.trees:
            out += self._predict_tree(t, B)
        return out
