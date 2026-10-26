"""PotencyTransfer core: shared by the development harness and the drevalpy model class, so both run
literally the same code.

Prediction for (cell line c, drug d):
    cell_line_mean(c)                       # exactly what NaiveMeanEffects predicts for an unseen drug
  + b + kappa * (delta_hat(d) - mean_training_delta)

delta_hat is kernel ridge regression of each TRAINING drug's mean residual (response minus cell-line
mean) on a sum of drug-drug kernels computed from structure and target annotations only:
    K = Tanimoto(Morgan fingerprints) + beta * Jaccard(target pathways) + tau * z z^T (+ gamma * physchem)
z is a structure-only potency prior (an NCI-60-trained teacher; every CTRPv2 compound and near-twin was
excluded from its training). Every weight, the ridge strength, the intercept b and the shrinkage kappa
are chosen by 5-fold drug-grouped cross-validation INSIDE the training drugs. Nothing about the drugs
being predicted -- other than their structure-derived features -- is used.
"""
import numpy as np, pandas as pd

ALPHAS = (0.03, 0.1, 0.3, 1.0, 3.0)
BETAS = (0.0, 0.5, 1.0, 2.0)
TAUS = (0.0, 0.5, 1.0, 2.0, 4.0)
GAMMAS = (0.0,)
INNER_FOLDS = 5
INNER_SEED = 12345


def tanimoto(A, B):
    A = A.astype(np.float32); B = B.astype(np.float32); inter = A @ B.T
    return inter / (A.sum(1)[:, None] + B.sum(1)[None, :] - inter + 1e-9)


def jaccard(A, B, PW):
    M = np.zeros((len(A), len(B)), np.float32)
    for i, a in enumerate(A):
        sa = PW.get(a)
        if not sa: continue
        for j, b in enumerate(B):
            sb = PW.get(b)
            if sb: M[i, j] = len(sa & sb) / len(sa | sb)
    return M


def krr(Ktr, ytr, w, Kte, alpha):
    mu = np.average(ytr, weights=w)
    return Kte @ np.linalg.solve(Ktr + alpha * np.eye(len(ytr)), ytr - mu) + mu


class PotencyCore:
    def __init__(self, FP, PW, TEACHER, alphas=ALPHAS, betas=BETAS, taus=TAUS, calibrate=True):
        self.FP, self.PW, self.T = FP, PW, TEACHER
        self.alphas, self.betas, self.taus, self.calibrate = alphas, betas, taus, calibrate

    def fit(self, cell_ids, drug_ids, y):
        drug_ids = np.asarray(drug_ids).astype(str); cell_ids = np.asarray(cell_ids)
        df = pd.DataFrame({"c": cell_ids, "d": drug_ids, "y": np.asarray(y, float)})
        self.cm = df.groupby("c")["y"].mean(); self.global_mean = float(df["y"].mean())
        df["r"] = df["y"] - df["c"].map(self.cm)
        g = df.groupby("d")["r"]; dmean = g.mean(); dn = g.size()
        self.drugs = np.array(dmean.index); self.y = dmean.to_numpy(); self.w = dn.to_numpy().astype(float)
        self.X = np.stack([self.FP[d] for d in self.drugs])
        Kf = tanimoto(self.X, self.X); Kp = jaccard(self.drugs, self.drugs, self.PW)
        zt = np.array([self.T[d] for d in self.drugs]); self.zm, self.zs = zt.mean(), zt.std() + 1e-9
        self.z = (zt - self.zm) / self.zs; Kt = np.outer(self.z, self.z)
        rng = np.random.default_rng(INNER_SEED); folds = rng.permutation(len(self.drugs)) % INNER_FOLDS
        self.ybar = float(np.average(self.y, weights=self.w)); best = None
        t = df["r"].to_numpy(); dcode = pd.Categorical(df["d"], categories=self.drugs).codes
        for beta in self.betas:
            for tau in self.taus:
                K = Kf + beta * Kp + tau * Kt
                for alpha in self.alphas:
                    oof = np.empty(len(self.drugs))
                    for f in range(INNER_FOLDS):
                        a, b = folds != f, folds == f
                        oof[b] = krr(K[np.ix_(a, a)], self.y[a], self.w[a], K[np.ix_(b, a)], alpha)
                    x = oof[dcode] - self.ybar
                    if self.calibrate:
                        c0, k = np.linalg.lstsq(np.c_[np.ones_like(x), x], t, rcond=None)[0]
                        k = float(np.clip(k, 0.0, 1.5)); mse = float(np.mean((t - c0 - k * x) ** 2))
                    else:
                        c0, k = 0.0, 1.0; mse = float(np.mean((t - x - self.ybar) ** 2))
                    if best is None or mse < best[0]:
                        best = (mse, beta, tau, alpha, float(c0), k)
        _, self.beta, self.tau, self.alpha, self.c0, self.kappa = best
        self.K = Kf + self.beta * Kp + self.tau * Kt
        self.coef = np.linalg.solve(self.K + self.alpha * np.eye(len(self.y)), self.y - np.average(self.y, weights=self.w))
        self.mu = float(np.average(self.y, weights=self.w))
        return self

    def drug_effect(self, drugs):
        drugs = np.asarray(drugs).astype(str)
        Xte = np.stack([self.FP[d] for d in drugs]); zte = (np.array([self.T[d] for d in drugs]) - self.zm) / self.zs
        Kte = tanimoto(Xte, self.X) + self.beta * jaccard(drugs, self.drugs, self.PW) + self.tau * np.outer(zte, self.z)
        dhat = Kte @ self.coef + self.mu
        if self.calibrate:
            return self.c0 + self.kappa * (dhat - self.ybar)
        return dhat

    def predict(self, cell_ids, drug_ids):
        drug_ids = np.asarray(drug_ids).astype(str); ud = np.unique(drug_ids)
        eff = dict(zip(ud, self.drug_effect(ud)))
        base = pd.Series(cell_ids).map(self.cm).fillna(self.global_mean).to_numpy()
        return base + pd.Series(drug_ids).map(eff).to_numpy()

    def params(self):
        return dict(alpha=self.alpha, beta=self.beta, tau=self.tau, b=self.c0, kappa=self.kappa)
