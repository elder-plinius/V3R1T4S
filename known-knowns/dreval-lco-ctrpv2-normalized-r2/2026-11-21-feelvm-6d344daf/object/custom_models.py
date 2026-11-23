"""Attacker model classes for the dreval-lco-ctrpv2-normalized-r2 hunt (2026-11-21).

Core idea: the normalized metric subtracts NaiveMeanEffectsPredictor predictions from true and
predicted values. In LCO, that predictor falls back to overall+tissue+drug effects for unseen
cell lines, so the *normalized target* is the cell-line-specific deviation. We therefore model
the residual r = y - NaiveMeanEffectsPredictor(x) directly from gene expression, with every
preprocessing step (scaler, PCA, completion) fitted on training cell lines only (LCO-leakage safe).

The naive half is computed by an internal NaiveMeanEffectsPredictor instance trained on the same
training fold, so residual definitions match the pipeline's normalization ruler exactly.

Missing drug response entries (not every drug screened on every line) are handled exactly:
per-drug ridge solves on observed entries with a shared (X'X + alpha*I)^-1 factor. The
reduced-rank path completes the training residual matrix with soft-impute-lite (col-mean fill ->
SVD reconstruct -> refill, a few iterations) before the omics->factor ridge.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from drevalpy.datasets.dataset import DrugResponseDataset, FeatureDataset
from drevalpy.models import MODEL_FACTORY, MULTI_DRUG_MODEL_FACTORY
from drevalpy.models.baselines.naive_pred import NaiveMeanEffectsPredictor
from drevalpy.models.drp_model import DRPModel
from drevalpy.models.utils import (
    get_multiomics_feature_dataset,
    load_cl_ids_and_tissues_from_csv,
    load_drug_ids_from_csv,
    scale_gene_expression,
)


def _view_to_frame(feature_dataset: FeatureDataset, view: str, cl_ids: np.ndarray) -> pd.DataFrame:
    """Extract one view of a FeatureDataset as a DataFrame indexed by cell line id."""
    rows = {}
    for cl in cl_ids:
        feats = feature_dataset.features[cl]
        rows[cl] = np.asarray(feats[view], dtype=float)
    return pd.DataFrame.from_dict(rows, orient="index")


def _soft_impute(R: np.ndarray, k: int, n_iter: int = 3) -> np.ndarray:
    """Soft-impute-lite: fill missing with current estimate, SVD-reconstruct, refill missing."""
    R = R.copy()
    col_mean = np.nanmean(R, axis=0)
    nan_mask = np.isnan(R)
    R[nan_mask] = np.take(col_mean, np.where(nan_mask)[1])
    for _ in range(n_iter):
        u, s, vt = np.linalg.svd(R - R.mean(axis=0, keepdims=True), full_matrices=False)
        kk = min(k, min(R.shape) - 1)
        recon = (u[:, :kk] * s[:kk]) @ vt[:kk, :] + R.mean(axis=0, keepdims=True)
        R[nan_mask] = recon[nan_mask]
    return R


_FEATURE_CACHE: dict = {}
"""Cache of loaded FeatureDatasets (immutable here; the pipeline copies before handing to models)."""

_FOLD_CACHE: dict = {}
"""Cache of fold-level preprocessing shared across hyperparameter trials.

Key: hash of (response bytes, cell_line_ids bytes, drug_ids bytes, class gene_list).
The cached pieces (naive ruler, residual matrix, scaled omics) depend ONLY on the training
fold content, never on hyperparameters, so reusing them across trials is exact and keeps the
per-trial fit honest (each trial still fits its own scaler-free map, PCA and ridge).
"""


def _fold_cache_key(output: DrugResponseDataset, gene_list: str) -> bytes:
    h = __import__("hashlib").sha256()
    h.update(output.response.tobytes())
    h.update(output.cell_line_ids.tobytes())
    h.update(output.drug_ids.tobytes())
    h.update(gene_list.encode())
    return h.digest()


class ResidualOmics(DRPModel):
    """NaiveMeanEffects predictor + rank-controlled multi-output ridge on the omics.

    Hyperparameters:
      alpha: ridge strength for the omics->residual map.
      n_pcs: train-fold PCA components of the omics (0 = off).
      n_factors: reduced-rank truncation of the residual matrix (0 = per-drug full ridge).
    """

    early_stopping = False
    cell_line_views = ["gene_expression"]
    drug_views = ["pubchem_id"]
    gene_list = "landmark_genes"

    @classmethod
    def get_model_name(cls) -> str:
        return "ResidualOmics"

    @classmethod
    def get_hyperparameter_set(cls) -> list[dict]:
        hpams = []
        for alpha in [30.0, 100.0, 300.0, 1000.0]:
            for n_pcs in [0, 100]:
                for n_factors in [0, 5, 10]:
                    hpams.append({"alpha": alpha, "n_pcs": n_pcs, "n_factors": n_factors})
        return hpams

    def load_cell_line_features(self, data_path: str, dataset_name: str) -> FeatureDataset:
        cache_key = ("cl", data_path, dataset_name, self.gene_list)
        cached = _FEATURE_CACHE.get(cache_key)
        if cached is None:
            feats = get_multiomics_feature_dataset(
                data_path=data_path,
                dataset_name=dataset_name,
                gene_lists={"gene_expression": self.gene_list},
                omics=["gene_expression"],
            )
            # the internal naive ruler needs the identifier + tissue views
            feats.add_features(load_cl_ids_and_tissues_from_csv(path=data_path, dataset_name=dataset_name))
            _FEATURE_CACHE[cache_key] = feats
            cached = feats
        return cached

    def load_drug_features(self, data_path: str, dataset_name: str) -> FeatureDataset:
        cache_key = ("drugs", data_path, dataset_name)
        cached = _FEATURE_CACHE.get(cache_key)
        if cached is None:
            cached = load_drug_ids_from_csv(data_path=data_path, dataset_name=dataset_name)
            _FEATURE_CACHE[cache_key] = cached
        return cached

    def build_model(self, hyperparameters: dict) -> None:
        self.hyperparameters = dict(hyperparameters)
        self.gene_expression_scaler = StandardScaler()
        self.naive = None
        self.pca = None
        self.W = None  # (n_features, n_drugs) regression weights
        self.intercept = None
        self.drug_columns = None
        self.cl_index = None  # training cell line order used to fit

    def _omics_matrix(self, cell_line_input: FeatureDataset, cl_ids: np.ndarray, training: bool) -> np.ndarray:
        """Scale (fit on train only when training=True) and return the omics matrix for cl_ids."""
        scaled = scale_gene_expression(
            cell_line_input=cell_line_input.copy(),
            cell_line_ids=cl_ids,
            training=training,
            gene_expression_scaler=self.gene_expression_scaler,
        )
        X_df = _view_to_frame(scaled, "gene_expression", cl_ids).reindex(cl_ids)
        X = np.nan_to_num(X_df.to_numpy(dtype=float), nan=0.0)
        return X

    def _fit_residual(self, X: np.ndarray, R: np.ndarray, drug_names: list[str]) -> None:
        """Fit the omics->residual map. X: (n_cl, p) already scaled; R: (n_cl, m) with NaN = unobserved."""
        alpha = float(self.hyperparameters["alpha"])
        n_factors = int(self.hyperparameters.get("n_factors", 0))
        n_cl, p = X.shape
        m = len(drug_names)
        # shared per-drug ridge factor: (X'X + aI)^-1 X'
        XtX = X.T @ X + alpha * np.eye(p)
        XtX_inv_Xt = np.linalg.solve(XtX, X.T)  # (p, n_cl)
        W = np.zeros((p, m))
        intercept = np.zeros(m)
        for j in range(m):
            y = R[:, j]
            obs = ~np.isnan(y)
            if obs.sum() >= 10:
                W[:, j] = XtX_inv_Xt[:, obs] @ y[obs]
                intercept[j] = y[obs].mean() - X[obs].mean(axis=0) @ W[:, j]
        if n_factors > 0:
            try:
                # reduced-rank path: complete the residual matrix (train only), factorize,
                # then map omics -> factor scores with a ridge on the completed scores.
                R_filled = _soft_impute(R.copy(), k=n_factors)
                R_centered = R_filled - R_filled.mean(axis=0, keepdims=True)
                u, s_svd, vt = np.linalg.svd(R_centered, full_matrices=False)
                k = min(n_factors, min(R_filled.shape) - 1)
                scores = u[:, :k] * s_svd[:k]  # (n_cl, k)
                XtX_s = X.T @ X + alpha * np.eye(p)
                B = np.linalg.solve(XtX_s, X.T @ scores)  # (p, k)
                W_rr = B @ vt[:k, :]  # (p, m)
                intercept_rr = R_filled.mean(axis=0) - X.mean(axis=0) @ W_rr
                W, intercept = W_rr, intercept_rr
            except np.linalg.LinAlgError:
                pass  # degenerate bootstrap column: keep the per-drug ridge computed above
        self.W = W
        self.intercept = intercept
        self.drug_columns = list(drug_names)

    def train(
        self,
        output: DrugResponseDataset,
        cell_line_input: FeatureDataset,
        drug_input: FeatureDataset | None = None,
        output_earlystopping: DrugResponseDataset | None = None,
        model_checkpoint_dir: str = "checkpoints",
    ) -> None:
        if len(output) == 0:
            return
        key = _fold_cache_key(output, self.gene_list)
        cached = _FOLD_CACHE.get(key)
        if cached is None:
            # 1) naive ruler on the SAME training fold (fresh instance; tuning-safe)
            naive = NaiveMeanEffectsPredictor()
            naive.train(output=output.copy(), cell_line_input=cell_line_input, drug_input=drug_input)
            naive_pred = naive.predict(
                cell_line_ids=output.cell_line_ids,
                drug_ids=output.drug_ids,
                cell_line_input=cell_line_input,
                drug_input=drug_input,
            )
            resid = output.response - naive_pred
            # 2) aggregate replicate pairs to a cell-line x drug residual matrix (NaN = unobserved)
            df = pd.DataFrame({"cl": output.cell_line_ids, "drug": output.drug_ids, "r": resid})
            R = df.pivot_table(index="cl", columns="drug", values="r", aggfunc="mean")
            cl_ids = R.index.to_numpy()
            drug_names = [str(c) for c in R.columns]
            # 3) gene expression for exactly these training cell lines; scaler fit here (train only)
            scaler = StandardScaler()
            scaled = scale_gene_expression(
                cell_line_input=cell_line_input.copy(),
                cell_line_ids=cl_ids,
                training=True,
                gene_expression_scaler=scaler,
            )
            X_df = _view_to_frame(scaled, "gene_expression", cl_ids).reindex(cl_ids)
            X = np.nan_to_num(X_df.to_numpy(dtype=float), nan=0.0)
            cached = (naive, R.to_numpy(dtype=float), cl_ids, drug_names, scaler, X)
            _FOLD_CACHE.clear()  # one fold at a time is enough; keep memory bounded
            _FOLD_CACHE[key] = cached
        self.naive, R_np, cl_ids, drug_names, self.gene_expression_scaler, X = cached

        # 4) optional train-fold PCA denoising of the omics (per trial: depends on n_pcs)
        n_pcs = int(self.hyperparameters.get("n_pcs", 0))
        if n_pcs > 0:
            k = min(n_pcs, min(X.shape) - 1)
            self.pca = PCA(n_components=k, random_state=42).fit(X)
            Xr = self.pca.transform(X)
        else:
            self.pca = None
            Xr = X

        self.cl_index = cl_ids
        self._fit_residual(Xr, R_np, drug_names)

    def _residual_pred_matrix(self, cell_line_ids: np.ndarray, cell_line_input: FeatureDataset) -> pd.DataFrame:
        uniq = np.unique(cell_line_ids)
        X = self._omics_matrix(cell_line_input, uniq, training=False)
        if self.pca is not None:
            X = self.pca.transform(X)
        resid_pred = X @ self.W + self.intercept  # (n_cl, m)
        return pd.DataFrame(resid_pred, index=uniq, columns=self.drug_columns)

    def predict(
        self,
        cell_line_ids: np.ndarray,
        drug_ids: np.ndarray,
        cell_line_input: FeatureDataset,
        drug_input: FeatureDataset | None = None,
    ) -> np.ndarray:
        if self.W is None:
            return np.full(len(cell_line_ids), np.nan)
        naive_pred = self.naive.predict(
            cell_line_ids=cell_line_ids,
            drug_ids=drug_ids,
            cell_line_input=cell_line_input,
            drug_input=drug_input,
        )
        pred_map = self._residual_pred_matrix(cell_line_ids, cell_line_input)
        out = []
        for cl, dr in zip(cell_line_ids, drug_ids, strict=True):
            dr = str(dr)
            out.append(pred_map.at[cl, dr] if dr in pred_map.columns else 0.0)
        return naive_pred + np.asarray(out, dtype=float)


class BaggedResidualOmics(ResidualOmics):
    """Bagged ResidualOmics: bootstrap training cell lines, average the residual maps.

    Variance reduction for the LCO bar (criterion demands >= 0.02 = ~11% relative over RF).
    """

    @classmethod
    def get_model_name(cls) -> str:
        return "BaggedResidualOmics"

    @classmethod
    def get_hyperparameter_set(cls) -> list[dict]:
        hpams = []
        for alpha in [100.0, 300.0, 1000.0]:
            for n_factors in [0, 5]:
                for n_bags in [15, 30]:
                    hpams.append(
                        {"alpha": alpha, "n_pcs": 0, "n_factors": n_factors, "n_bags": n_bags, "seed": 42}
                    )
        return hpams

    def build_model(self, hyperparameters: dict) -> None:
        super().build_model(hyperparameters)
        self.bag_W = []
        self.bag_intercept = []

    def train(
        self,
        output: DrugResponseDataset,
        cell_line_input: FeatureDataset,
        drug_input: FeatureDataset | None = None,
        output_earlystopping: DrugResponseDataset | None = None,
        model_checkpoint_dir: str = "checkpoints",
    ) -> None:
        if len(output) == 0:
            return
        key = _fold_cache_key(output, self.gene_list)
        cached = _FOLD_CACHE.get(key)
        if cached is None:
            naive = NaiveMeanEffectsPredictor()
            naive.train(output=output.copy(), cell_line_input=cell_line_input, drug_input=drug_input)
            naive_pred = naive.predict(
                cell_line_ids=output.cell_line_ids,
                drug_ids=output.drug_ids,
                cell_line_input=cell_line_input,
                drug_input=drug_input,
            )
            resid = output.response - naive_pred
            df = pd.DataFrame({"cl": output.cell_line_ids, "drug": output.drug_ids, "r": resid})
            R = df.pivot_table(index="cl", columns="drug", values="r", aggfunc="mean")
            cl_ids = R.index.to_numpy()
            drug_names = [str(c) for c in R.columns]
            scaler = StandardScaler()
            scaled = scale_gene_expression(
                cell_line_input=cell_line_input.copy(),
                cell_line_ids=cl_ids,
                training=True,
                gene_expression_scaler=scaler,
            )
            X_df = _view_to_frame(scaled, "gene_expression", cl_ids).reindex(cl_ids)
            X = np.nan_to_num(X_df.to_numpy(dtype=float), nan=0.0)
            cached = (naive, R.to_numpy(dtype=float), cl_ids, drug_names, scaler, X)
            _FOLD_CACHE.clear()
            _FOLD_CACHE[key] = cached
        self.naive, R_np, cl_ids, drug_names, self.gene_expression_scaler, X = cached
        self.cl_index = cl_ids
        self.drug_columns = drug_names

        n_bags = int(self.hyperparameters.get("n_bags", 20))
        seed = int(self.hyperparameters.get("seed", 42))
        rng = np.random.default_rng(seed)
        n_cl = len(cl_ids)
        self.bag_W = []
        self.bag_intercept = []
        for _ in range(n_bags):
            idx = rng.integers(0, n_cl, size=n_cl)  # bootstrap over training cell lines
            sub = ResidualOmics()
            sub.hyperparameters = {
                "alpha": self.hyperparameters["alpha"],
                "n_pcs": 0,
                "n_factors": int(self.hyperparameters.get("n_factors", 0)),
            }
            sub._fit_residual(X[idx], R_np[idx], drug_names)
            self.bag_W.append(sub.W)
            self.bag_intercept.append(sub.intercept)
        # canonical state = average of bags
        self.W = np.mean(np.stack(self.bag_W), axis=0)
        self.intercept = np.mean(np.stack(self.bag_intercept), axis=0)
        self.pca = None

    def predict(
        self,
        cell_line_ids: np.ndarray,
        drug_ids: np.ndarray,
        cell_line_input: FeatureDataset,
        drug_input: FeatureDataset | None = None,
    ) -> np.ndarray:
        if self.W is None or not self.bag_W:
            return np.full(len(cell_line_ids), np.nan)
        naive_pred = self.naive.predict(
            cell_line_ids=cell_line_ids,
            drug_ids=drug_ids,
            cell_line_input=cell_line_input,
            drug_input=drug_input,
        )
        uniq = np.unique(cell_line_ids)
        X = self._omics_matrix(cell_line_input, uniq, training=False)
        # average residual prediction across bags (all bags share the drug column order)
        resid_pred = np.mean(
            np.stack([X @ w + b for w, b in zip(self.bag_W, self.bag_intercept)]), axis=0
        )
        pred_map = pd.DataFrame(resid_pred, index=uniq, columns=self.drug_columns)
        out = []
        for cl, dr in zip(cell_line_ids, drug_ids, strict=True):
            dr = str(dr)
            out.append(pred_map.at[cl, dr] if dr in pred_map.columns else 0.0)
        return naive_pred + np.asarray(out, dtype=float)


def register() -> None:
    for cls in (ResidualOmics, BaggedResidualOmics):
        name = cls.get_model_name()
        MULTI_DRUG_MODEL_FACTORY[name] = cls
        MODEL_FACTORY[name] = cls


register()
