"""Exact-equivalent fast version of PotencyCore (verified against potency_core.py in
output/fast_equivalence.txt). Two changes, neither touching the mathematics:
  1. Tanimoto and pathway-Jaccard similarities are fixed functions of structure / annotations (no
     fitting, no responses), so they are computed once for all drugs and indexed.
  2. For each kernel combination and inner fold, one eigendecomposition serves every ridge strength.
"""
import numpy as np, pandas as pd
from potency_core import ALPHAS, BETAS, TAUS, INNER_FOLDS, INNER_SEED, tanimoto, jaccard


class GlobalKernels:
    def __init__(self, FP, PW, drug_universe):
        self.ids = np.array(sorted(drug_universe)); self.pos = {d: i for i, d in enumerate(self.ids)}
        X = np.stack([FP[d] for d in self.ids]); self.KF = tanimoto(X, X).astype(np.float64)
        self.KP = jaccard(self.ids, self.ids, PW).astype(np.float64)

    def idx(self, drugs):
        return np.array([self.pos[d] for d in drugs])


class PotencyCoreFast:
    def __init__(self, GK, TEACHER, alphas=ALPHAS, betas=BETAS, taus=TAUS, calibrate=True, perm=None,
                 gammas=(0.0,), DESC=None):
        """perm: optional array permuting the drug universe -- used ONLY by the null test, to break the
        link between each drug and its own structure/annotation features."""
        self.GK, self.T, self.alphas, self.betas, self.taus, self.calibrate = GK, TEACHER, alphas, betas, taus, calibrate
        self.perm = perm; self.gammas = gammas; self.DESC = DESC or {}

    def _desc(self, drugs):
        """physicochemical descriptors, standardized with the scaler fitted on TRAINING drugs; drugs
        without a structure get the training mean (zeros after standardization)."""
        fi = self._feat_idx(drugs); out = []
        for j in fi:
            v = self.DESC.get(self.GK.ids[j])
            out.append((v - self.dmu) / self.dsd if v is not None else np.zeros(len(self.dmu)))
        return np.stack(out)

    def _feat_idx(self, drugs):
        i = self.GK.idx(drugs)
        return i if self.perm is None else self.perm[i]

    def _teacher(self, drugs):
        fi = self._feat_idx(drugs); return np.array([self.T[self.GK.ids[j]] for j in fi])

    def fit(self, cell_ids, drug_ids, y):
        drug_ids = np.asarray(drug_ids).astype(str)
        df = pd.DataFrame({"c": np.asarray(cell_ids), "d": drug_ids, "y": np.asarray(y, float)})
        self.cm = df.groupby("c")["y"].mean(); self.global_mean = float(df["y"].mean())
        df["r"] = df["y"] - df["c"].map(self.cm)
        g = df.groupby("d")["r"]; dmean = g.mean(); dn = g.size()
        self.drugs = np.array(dmean.index); y_ = dmean.to_numpy(); w = dn.to_numpy().astype(float)
        fi = self._feat_idx(self.drugs)
        Kf = self.GK.KF[np.ix_(fi, fi)]; Kp = self.GK.KP[np.ix_(fi, fi)]
        zt = self._teacher(self.drugs); self.zm, self.zs = zt.mean(), zt.std() + 1e-9
        self.z = (zt - self.zm) / self.zs; Kt = np.outer(self.z, self.z)
        if self.gammas != (0.0,):
            have = [self.DESC[self.GK.ids[j]] for j in fi if self.GK.ids[j] in self.DESC]
            D0 = np.stack(have); self.dmu, self.dsd = D0.mean(0), D0.std(0) + 1e-9
            self.Z = self._desc(self.drugs)
            Kd = np.exp(-((self.Z[:, None, :] - self.Z[None, :, :]) ** 2).sum(-1) / (2 * self.Z.shape[1]))
        else:
            Kd = np.zeros_like(Kf)
        rng = np.random.default_rng(INNER_SEED); folds = rng.permutation(len(self.drugs)) % INNER_FOLDS
        self.ybar = float(np.average(y_, weights=w)); best = None
        for beta in self.betas:
          for gamma in self.gammas:
            for tau in self.taus:
                K = Kf + beta * Kp + tau * Kt + gamma * Kd
                oofs = {a: np.empty(len(self.drugs)) for a in self.alphas}
                for f in range(INNER_FOLDS):
                    a_, b_ = folds != f, folds == f
                    Kaa = K[np.ix_(a_, a_)]; Kba = K[np.ix_(b_, a_)]
                    mu = np.average(y_[a_], weights=w[a_]); ev, V = np.linalg.eigh(Kaa)
                    proj = V.T @ (y_[a_] - mu); KbV = Kba @ V
                    for alpha in self.alphas:
                        oofs[alpha][b_] = KbV @ (proj / (ev + alpha)) + mu
                for alpha in self.alphas:
                    # Pair-level least squares with a drug-constant regressor equals pair-count-weighted
                    # least squares on drug means (the within-drug sum of squares is a constant), so it
                    # is computed at drug level: same argmin, same coefficients, ~400x fewer rows.
                    xd = oofs[alpha] - self.ybar; sw = np.sqrt(w)
                    if self.calibrate:
                        c0, k = np.linalg.lstsq(np.c_[sw, sw * xd], sw * y_, rcond=None)[0]
                        k = float(np.clip(k, 0.0, 1.5)); mse = float(np.sum(w * (y_ - c0 - k * xd) ** 2))
                    else:
                        c0, k = 0.0, 1.0; mse = float(np.sum(w * (y_ - xd - self.ybar) ** 2))
                    if best is None or mse < best[0]:
                        best = (mse, beta, tau, alpha, float(c0), k, gamma)
        _, self.beta, self.tau, self.alpha, self.c0, self.kappa, self.gamma = best
        self.fi = fi; K = Kf + self.beta * Kp + self.tau * Kt + self.gamma * Kd
        self.mu = float(np.average(y_, weights=w))
        self.coef = np.linalg.solve(K + self.alpha * np.eye(len(y_)), y_ - self.mu)
        return self

    def drug_effect(self, drugs):
        drugs = np.asarray(drugs).astype(str); fj = self._feat_idx(drugs)
        zte = (self._teacher(drugs) - self.zm) / self.zs
        Kte = self.GK.KF[np.ix_(fj, self.fi)] + self.beta * self.GK.KP[np.ix_(fj, self.fi)] + self.tau * np.outer(zte, self.z)
        if self.gamma:
            Zt = self._desc(drugs)
            Kte = Kte + self.gamma * np.exp(-((Zt[:, None, :] - self.Z[None, :, :]) ** 2).sum(-1) / (2 * self.Z.shape[1]))
        dhat = Kte @ self.coef + self.mu
        return self.c0 + self.kappa * (dhat - self.ybar) if self.calibrate else dhat

    def predict(self, cell_ids, drug_ids):
        drug_ids = np.asarray(drug_ids).astype(str); ud = np.unique(drug_ids)
        eff = dict(zip(ud, self.drug_effect(ud)))
        base = pd.Series(cell_ids).map(self.cm).fillna(self.global_mean).to_numpy()
        return base + pd.Series(drug_ids).map(eff).to_numpy()

    def params(self):
        return dict(alpha=self.alpha, beta=self.beta, tau=self.tau, gamma=self.gamma, b=self.c0, kappa=self.kappa)
