"""v1.3.1-ruler attacker models (Track B, report-faithful protocol).

Base predictor = the REPORT's (drevalpy v1.3.1) NaiveMeanEffectsPredictor semantics:
prediction = overall_mean + cell_line_effect[train only] + drug_effect; unseen cell lines
contribute 0 (no tissue fallback). Under the report's ruler the tissue variance stays in the
normalized target, so the omics model explains it. All fits are train-fold only (LCO-safe).
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from drevalpy.datasets.dataset import DrugResponseDataset
from drevalpy.models import MODEL_FACTORY, MULTI_DRUG_MODEL_FACTORY

from custom_models import _FOLD_CACHE, ResidualOmics, _fold_cache_key, _view_to_frame
from drevalpy.models.utils import scale_gene_expression


class _NaiveV131:
    """The v1.3.1 NaiveMeanEffectsPredictor semantics (train-fold fitted)."""

    def __init__(self):
        self.overall = 0.0
        self.cl_effect = None
        self.drug_effect = None

    def fit(self, df: pd.DataFrame) -> None:
        self.overall = float(df["response"].mean())
        self.cl_effect = df.groupby("cl")["response"].mean() - self.overall
        self.drug_effect = df.groupby("drug")["response"].mean() - self.overall

    def predict(self, cls, drugs) -> np.ndarray:
        cl = pd.Series(cls).map(self.cl_effect).fillna(0.0).to_numpy()
        dr = pd.Series(drugs).map(self.drug_effect).fillna(0.0).to_numpy()
        return self.overall + cl + dr


def _fold_precompute_v131(output: DrugResponseDataset, cell_line_input, gene_list: str):
    """Naive ruler (v1.3.1) + residual matrix + scaled omics for one training fold."""
    df = pd.DataFrame({"cl": output.cell_line_ids, "drug": output.drug_ids, "response": output.response})
    naive = _NaiveV131()
    naive.fit(df)
    resid = df["response"].to_numpy() - naive.predict(df["cl"], df["drug"])
    R = pd.DataFrame({"cl": df["cl"], "drug": df["drug"], "r": resid}).pivot_table(
        index="cl", columns="drug", values="r", aggfunc="mean"
    )
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
    return naive, R.to_numpy(dtype=float), cl_ids, drug_names, scaler, X


class ResidualOmics131(ResidualOmics):
    """Residual omics model against the REPORT's (v1.3.1) naive ruler."""

    @classmethod
    def get_model_name(cls) -> str:
        return "ResidualOmics131"

    @classmethod
    def get_hyperparameter_set(cls) -> list[dict]:
        hpams = []
        for alpha in [30.0, 100.0, 300.0, 1000.0]:
            for n_pcs in [0, 100]:
                for n_factors in [0, 5, 10]:
                    hpams.append({"alpha": alpha, "n_pcs": n_pcs, "n_factors": n_factors})
        return hpams

    def train(self, output, cell_line_input, drug_input=None, output_earlystopping=None,
              model_checkpoint_dir="checkpoints") -> None:
        if len(output) == 0:
            return
        key = _fold_cache_key(output, "v131-" + self.gene_list)
        cached = _FOLD_CACHE.get(key)
        if cached is None:
            cached = _fold_precompute_v131(output, cell_line_input, self.gene_list)
            _FOLD_CACHE.clear()
            _FOLD_CACHE[key] = cached
        self.naive, R_np, cl_ids, drug_names, self.gene_expression_scaler, X = cached

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

    def predict(self, cell_line_ids, drug_ids, cell_line_input, drug_input=None) -> np.ndarray:
        if self.W is None:
            return np.full(len(cell_line_ids), np.nan)
        base = self.naive.predict(cell_line_ids, drug_ids)  # v1.3.1 ruler: unseen cl -> 0
        pred_map = self._residual_pred_matrix(cell_line_ids, cell_line_input)
        out = []
        for cl, dr in zip(cell_line_ids, drug_ids, strict=True):
            dr = str(dr)
            out.append(pred_map.at[cl, dr] if dr in pred_map.columns else 0.0)
        return base + np.asarray(out, dtype=float)


class BaggedResidualOmics131(ResidualOmics131):
    """Bagged variant of ResidualOmics131 (variance reduction)."""

    @classmethod
    def get_model_name(cls) -> str:
        return "BaggedResidualOmics131"

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

    def train(self, output, cell_line_input, drug_input=None, output_earlystopping=None,
              model_checkpoint_dir="checkpoints") -> None:
        if len(output) == 0:
            return
        key = _fold_cache_key(output, "v131-" + self.gene_list)
        cached = _FOLD_CACHE.get(key)
        if cached is None:
            cached = _fold_precompute_v131(output, cell_line_input, self.gene_list)
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
            idx = rng.integers(0, n_cl, size=n_cl)
            sub = ResidualOmics131()
            sub.hyperparameters = {
                "alpha": self.hyperparameters["alpha"],
                "n_pcs": 0,
                "n_factors": int(self.hyperparameters.get("n_factors", 0)),
            }
            sub._fit_residual(X[idx], R_np[idx], drug_names)
            self.bag_W.append(sub.W)
            self.bag_intercept.append(sub.intercept)
        self.W = np.mean(np.stack(self.bag_W), axis=0)
        self.intercept = np.mean(np.stack(self.bag_intercept), axis=0)
        self.pca = None

    def predict(self, cell_line_ids, drug_ids, cell_line_input, drug_input=None) -> np.ndarray:
        if self.W is None or not self.bag_W:
            return np.full(len(cell_line_ids), np.nan)
        base = self.naive.predict(cell_line_ids, drug_ids)
        uniq = np.unique(cell_line_ids)
        X = self._omics_matrix(cell_line_input, uniq, training=False)
        resid_pred = np.mean(
            np.stack([X @ w + b for w, b in zip(self.bag_W, self.bag_intercept)]), axis=0
        )
        pred_map = pd.DataFrame(resid_pred, index=uniq, columns=self.drug_columns)
        out = []
        for cl, dr in zip(cell_line_ids, drug_ids, strict=True):
            dr = str(dr)
            out.append(pred_map.at[cl, dr] if dr in pred_map.columns else 0.0)
        return base + np.asarray(out, dtype=float)


def register() -> None:
    for cls in (ResidualOmics131, BaggedResidualOmics131):
        name = cls.get_model_name()
        MULTI_DRUG_MODEL_FACTORY[name] = cls
        MODEL_FACTORY[name] = cls


register()


class ResidualOmics131T(ResidualOmics131):
    """ResidualOmics131 with a tissue-x-drug mean base (train-fold statistic).

    Base: for each (tissue, drug) pair present in training, the mean response of that
    tissue's training cell lines for that drug (fallback: drug mean -> overall mean).
    Tissue labels come from the cell line feature metadata (available for test lines);
    the means are train-fold statistics only (LCO-safe). The omics ridge then models
    what the tissue-drug base leaves unexplained.
    """

    @classmethod
    def get_model_name(cls) -> str:
        return "ResidualOmics131T"

    @classmethod
    def get_hyperparameter_set(cls) -> list[dict]:
        hpams = []
        for alpha in [100.0, 300.0, 1000.0]:
            for n_pcs in [0, 100]:
                for n_factors in [0, 5]:
                    hpams.append({"alpha": alpha, "n_pcs": n_pcs, "n_factors": n_factors})
        return hpams

    def _tissue_drug_base(self, df: pd.DataFrame, tissue_lookup: pd.Series):
        """Fit tissue x drug mean table from training rows (df has tissue column)."""
        self.tissue_map = tissue_lookup  # cl -> tissue (train lines)
        self.td_mean = df.groupby(["tissue", "drug"])["response"].mean()
        self.drug_mean = df.groupby("drug")["response"].mean()

    def _base_predict(self, cls, drugs, tissue_lookup: pd.Series) -> np.ndarray:
        t = pd.Series(cls).map(tissue_lookup)
        key = pd.MultiIndex.from_arrays([t.to_numpy(), pd.Series(drugs).to_numpy()])
        base = self.td_mean.reindex(key).to_numpy()
        # fallbacks: drug mean -> overall mean
        dm = pd.Series(drugs).map(self.drug_mean).to_numpy()
        base = np.where(np.isnan(base), dm, base)
        base = np.where(np.isnan(base), self.naive.overall, base)
        return base

    def train(self, output, cell_line_input, drug_input=None, output_earlystopping=None,
              model_checkpoint_dir="checkpoints") -> None:
        if len(output) == 0:
            return
        # tissue lookup for every cell line in the feature dataset (metadata view)
        tissue_of = {}
        for cl, feats in cell_line_input.features.items():
            if "tissue" in feats:
                tissue_of[cl] = str(np.asarray(feats["tissue"]).ravel()[0])
        tissue_lookup = pd.Series(tissue_of)

        key = _fold_cache_key(output, "v131T-" + self.gene_list)
        cached = _FOLD_CACHE.get(key)
        if cached is None:
            df = pd.DataFrame(
                {
                    "cl": output.cell_line_ids,
                    "drug": output.drug_ids,
                    "response": output.response,
                }
            )
            df["tissue"] = df["cl"].map(tissue_lookup)
            naive = _NaiveV131()
            naive.fit(df)
            self.naive = naive  # needed by _base_predict fallback in the cache-miss branch
            self._tissue_drug_base(df, tissue_lookup)
            base = self._base_predict(df["cl"].to_numpy(), df["drug"].to_numpy(), tissue_lookup)
            resid = df["response"].to_numpy() - base
            R = pd.DataFrame({"cl": df["cl"], "drug": df["drug"], "r": resid}).pivot_table(
                index="cl", columns="drug", values="r", aggfunc="mean"
            )
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
            cached = (naive, R.to_numpy(dtype=float), cl_ids, drug_names, scaler, X, tissue_lookup)
            _FOLD_CACHE.clear()
            _FOLD_CACHE[key] = cached
        self.naive, R_np, cl_ids, drug_names, self.gene_expression_scaler, X, tissue_lookup = cached
        self.tissue_map = tissue_lookup
        # re-derive the tissue x drug table (cheap) so predict uses this fold's table
        dfb = pd.DataFrame(
            {
                "cl": output.cell_line_ids,
                "drug": output.drug_ids,
                "response": output.response,
                "tissue": output.cell_line_ids.map(tissue_lookup) if hasattr(output.cell_line_ids, "map") else [tissue_lookup.get(c) for c in output.cell_line_ids],
            }
        )
        self.td_mean = dfb.groupby(["tissue", "drug"])["response"].mean()
        self.drug_mean = dfb.groupby("drug")["response"].mean()

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

    def predict(self, cell_line_ids, drug_ids, cell_line_input, drug_input=None) -> np.ndarray:
        if self.W is None:
            return np.full(len(cell_line_ids), np.nan)
        tissue_of = {}
        for cl, feats in cell_line_input.features.items():
            if "tissue" in feats:
                tissue_of[cl] = str(np.asarray(feats["tissue"]).ravel()[0])
        tissue_lookup = pd.Series(tissue_of)
        base = self._base_predict(cell_line_ids, drug_ids, tissue_lookup)
        pred_map = self._residual_pred_matrix(cell_line_ids, cell_line_input)
        out = []
        for cl, dr in zip(cell_line_ids, drug_ids, strict=True):
            dr = str(dr)
            out.append(pred_map.at[cl, dr] if dr in pred_map.columns else 0.0)
        return base + np.asarray(out, dtype=float)


def register_all() -> None:
    for cls in (ResidualOmics131T,):
        name = cls.get_model_name()
        MULTI_DRUG_MODEL_FACTORY[name] = cls
        MODEL_FACTORY[name] = cls


register_all()
