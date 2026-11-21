"""EnsembleResidualOmics — the claim-vehicle model class (Track A protocol).

Averages two complementary residual families, both train-fold-only (LCO-safe):
  member A: NaiveMeanEffectsPredictor (v1.6.0 semantics, the pinned package's own ruler base)
            + multi-output ridge on gene-expression residuals;
  member B: tissue-x-drug mean base (train-fold statistic; tissue labels from feature metadata)
            + multi-output ridge on what that base leaves unexplained.
Both members share the fold-level preprocessing cache. The pipeline's hpam_tune drives a small
honest grid over the joint ridge strengths/ranks via validation partitions only.

Registered as "EnsembleResidualOmics".
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from drevalpy.models import MODEL_FACTORY, MULTI_DRUG_MODEL_FACTORY
from drevalpy.models.utils import scale_gene_expression
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from custom_models import ResidualOmics, _FOLD_CACHE, _fold_cache_key, _view_to_frame
from custom_models_v131 import _NaiveV131


class EnsembleResidualOmics(ResidualOmics):
    """Mean of (v16-ruler residual ridge) and (tissue-drug-mean base + residual ridge)."""

    @classmethod
    def get_model_name(cls) -> str:
        return "EnsembleResidualOmics"

    @classmethod
    def get_hyperparameter_set(cls) -> list[dict]:
        hpams = []
        for alpha_b in [100.0, 300.0, 1000.0]:
            for nf_b in [0, 5]:
                for w in [0.4, 0.5, 0.6]:
                    hpams.append(
                        {"alpha_a": 300.0, "alpha_b": alpha_b, "n_factors_b": nf_b, "w": w,
                         "n_pcs": 0, "n_factors_a": 0}
                    )
        return hpams

    def load_cell_line_features(self, data_path: str, dataset_name: str):
        # member A needs identifier+tissue views (its internal naive ruler); member B needs
        # the tissue view. Same loading as the parents.
        return super().load_cell_line_features(data_path, dataset_name)

    def build_model(self, hyperparameters: dict) -> None:
        super().build_model(hyperparameters)
        self.gene_expression_scaler_b = StandardScaler()
        self.W_b = None
        self.intercept_b = None
        self.td_mean = None
        self.drug_mean = None
        self.tissue_lookup = None

    def _fit_ridge(self, X, R, alpha, n_factors):
        sub = ResidualOmics()
        sub.hyperparameters = {"alpha": alpha, "n_pcs": 0, "n_factors": n_factors}
        sub._fit_residual(X, R, self.drug_columns)
        return sub.W, sub.intercept

    def train(self, output, cell_line_input, drug_input=None, output_earlystopping=None,
              model_checkpoint_dir="checkpoints") -> None:
        if len(output) == 0:
            return
        # ---------- fold preprocessing (shared across hpam trials via cache) ----------
        key = _fold_cache_key(output, "ens-" + self.gene_list)
        cached = _FOLD_CACHE.get(key)
        if cached is None:
            # member A: v1.6.0 ruler base (the package's own NaiveMeanEffectsPredictor)
            from drevalpy.models.baselines.naive_pred import NaiveMeanEffectsPredictor

            naive_a_pkg = NaiveMeanEffectsPredictor()
            naive_a_pkg.train(
                output=output.copy(), cell_line_input=cell_line_input, drug_input=drug_input
            )
            pred_a = naive_a_pkg.predict(
                cell_line_ids=output.cell_line_ids,
                drug_ids=output.drug_ids,
                cell_line_input=cell_line_input,
                drug_input=drug_input,
            )
            resid_a = output.response - pred_a

            # member B: tissue-x-drug mean base
            tissue_of = {}
            for cl, feats in cell_line_input.features.items():
                if "tissue" in feats:
                    tissue_of[cl] = str(np.asarray(feats["tissue"]).ravel()[0])
            tissue_lookup = pd.Series(tissue_of)
            dfb = pd.DataFrame(
                {
                    "cl": output.cell_line_ids,
                    "drug": output.drug_ids,
                    "response": output.response,
                }
            )
            dfb["tissue"] = [tissue_lookup.get(c) for c in dfb["cl"]]
            self.td_mean = dfb.groupby(["tissue", "drug"])["response"].mean()
            self.drug_mean = dfb.groupby("drug")["response"].mean()
            t_key = pd.MultiIndex.from_arrays([dfb["tissue"].to_numpy(), dfb["drug"].to_numpy()])
            base_b = self.td_mean.reindex(t_key).to_numpy()
            dm = dfb["drug"].map(self.drug_mean).to_numpy()
            base_b = np.where(np.isnan(base_b), dm, base_b)
            self.overall_b = float(dfb["response"].mean())
            base_b = np.where(np.isnan(base_b), self.overall_b, base_b)
            resid_b = dfb["response"].to_numpy() - base_b

            # shared omics matrix (scaled once on train fold)
            df_all = pd.DataFrame({"cl": output.cell_line_ids, "drug": output.drug_ids})
            R_a = pd.DataFrame({"cl": df_all["cl"], "drug": df_all["drug"], "r": resid_a}).pivot_table(
                index="cl", columns="drug", values="r", aggfunc="mean"
            )
            R_b = pd.DataFrame({"cl": df_all["cl"], "drug": df_all["drug"], "r": resid_b}).pivot_table(
                index="cl", columns="drug", values="r", aggfunc="mean"
            )
            cl_ids = R_a.index.to_numpy()
            drug_names = [str(c) for c in R_a.columns]
            scaler = StandardScaler()
            scaled = scale_gene_expression(
                cell_line_input=cell_line_input.copy(),
                cell_line_ids=cl_ids,
                training=True,
                gene_expression_scaler=scaler,
            )
            X_df = _view_to_frame(scaled, "gene_expression", cl_ids).reindex(cl_ids)
            X = np.nan_to_num(X_df.to_numpy(dtype=float), nan=0.0)
            cached = (naive_a_pkg, R_a.to_numpy(dtype=float), R_b.to_numpy(dtype=float),
                      cl_ids, drug_names, scaler, X, tissue_lookup,
                      self.td_mean, self.drug_mean, self.overall_b)
            _FOLD_CACHE.clear()
            _FOLD_CACHE[key] = cached
        (self.naive, R_a_np, R_b_np, cl_ids, drug_names, self.gene_expression_scaler, X,
         self.tissue_lookup, self.td_mean, self.drug_mean, self.overall_b) = cached
        self.drug_columns = drug_names
        self.cl_index = cl_ids

        # ---------- members (per hpam trial) ----------
        self.W, self.intercept = self._fit_ridge(
            X, R_a_np, float(self.hyperparameters["alpha_a"]), int(self.hyperparameters.get("n_factors_a", 0))
        )
        self.W_b, self.intercept_b = self._fit_ridge(
            X, R_b_np, float(self.hyperparameters["alpha_b"]), int(self.hyperparameters.get("n_factors_b", 0))
        )
        self.pca = None
        self.pca_b = None

    def _tissue_base_predict(self, cls, drugs) -> np.ndarray:
        t = pd.Series(cls).map(self.tissue_lookup)
        key = pd.MultiIndex.from_arrays([t.to_numpy(), pd.Series(drugs).to_numpy()])
        base = self.td_mean.reindex(key).to_numpy()
        dm = pd.Series(drugs).map(self.drug_mean).to_numpy()
        base = np.where(np.isnan(base), dm, base)
        return np.where(np.isnan(base), getattr(self, "overall_b", 0.0), base)

    def predict(self, cell_line_ids, drug_ids, cell_line_input, drug_input=None) -> np.ndarray:
        if self.W is None or self.W_b is None:
            return np.full(len(cell_line_ids), np.nan)
        # member A prediction
        pred_a = super().predict(cell_line_ids, drug_ids, cell_line_input, drug_input)
        # member B prediction
        uniq = np.unique(cell_line_ids)
        X = self._omics_matrix(cell_line_input, uniq, training=False)
        resid_b = X @ self.W_b + self.intercept_b
        map_b = pd.DataFrame(resid_b, index=uniq, columns=self.drug_columns)
        base_b = self._tissue_base_predict(cell_line_ids, drug_ids)
        out_b = []
        for cl, dr in zip(cell_line_ids, drug_ids, strict=True):
            dr = str(dr)
            out_b.append(map_b.at[cl, dr] if dr in map_b.columns else 0.0)
        pred_b = base_b + np.asarray(out_b, dtype=float)
        w = float(self.hyperparameters.get("w", 0.5))
        return w * pred_a + (1.0 - w) * pred_b


def register() -> None:
    name = EnsembleResidualOmics.get_model_name()
    MULTI_DRUG_MODEL_FACTORY[name] = EnsembleResidualOmics
    MODEL_FACTORY[name] = EnsembleResidualOmics


register()
