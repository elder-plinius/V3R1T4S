"""drevalpy 1.3.5 model class wrapping PotencyCore, so the confirmatory runs go through drevalpy's own
pipeline, splits, tuning loop and evaluation code -- as the success criterion requires.

Views are identifiers only, so drevalpy keeps every drug and every cell line in the evaluation: the
model is scored on the full benchmark, with no feature-availability subsetting.

Structure/annotation lookups, read from <data_path>/<dataset>/potency_transfer/ and the dataset's own
fingerprint file:
  * drug_fingerprints/pubchem_id_to_demorgan_2048_map.csv   (shipped with the dataset)
  * potency_transfer/drug_pathways.csv.gz                    (drevalpy meta, target-derived pathways)
  * potency_transfer/teacher_pred.csv                        (NCI-60 teacher, structure only)
"""
import os, sys, numpy as np, pandas as pd
from drevalpy.models.drp_model import DRPModel
from drevalpy.datasets.dataset import FeatureDataset
from drevalpy.datasets.utils import CELL_LINE_IDENTIFIER, DRUG_IDENTIFIER
from drevalpy.models.utils import load_cl_ids_from_csv, load_drug_ids_from_csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from potency_core import PotencyCore

_LOOKUPS = {}


def _lookups(data_path, dataset_name):
    key = (os.path.abspath(data_path), dataset_name)
    if key not in _LOOKUPS:
        base = os.path.join(data_path, dataset_name)
        fp = pd.read_csv(os.path.join(base, "drug_fingerprints", "pubchem_id_to_demorgan_2048_map.csv"), dtype=str)
        FP = {c: fp[c].astype(np.uint8).to_numpy() for c in fp.columns}
        pw = pd.read_csv(os.path.join(base, "potency_transfer", "drug_pathways.csv.gz"), dtype=str)
        PW = {d: set(g.pathway) for d, g in pw.groupby("pubchem_id")}
        t = pd.read_csv(os.path.join(base, "potency_transfer", "teacher_pred.csv"), dtype={0: str})
        T = dict(zip(t.iloc[:, 0].astype(str), t.iloc[:, 1].astype(float)))
        _LOOKUPS[key] = (FP, PW, T)
    return _LOOKUPS[key]


class PotencyTransfer(DRPModel):
    cell_line_views = [CELL_LINE_IDENTIFIER]
    drug_views = [DRUG_IDENTIFIER]
    early_stopping = False
    is_single_drug_model = False

    def __init__(self):
        super().__init__()
        self.core = None; self._lk = None

    @classmethod
    def get_model_name(cls) -> str:
        return "PotencyTransfer"

    @classmethod
    def get_hyperparameter_set(cls):
        return [{}]          # every hyperparameter is chosen by drug-grouped CV inside train()

    def build_model(self, hyperparameters):
        self.hyperparameters = hyperparameters

    def train(self, output, cell_line_input, drug_input=None, output_earlystopping=None, model_checkpoint_dir="checkpoints"):
        FP, PW, T = self._lk
        self.core = PotencyCore(FP, PW, T).fit(output.cell_line_ids, output.drug_ids, output.response)

    def predict(self, cell_line_ids, drug_ids, cell_line_input, drug_input=None):
        return self.core.predict(cell_line_ids, drug_ids)

    def load_cell_line_features(self, data_path, dataset_name) -> FeatureDataset:
        return load_cl_ids_from_csv(data_path, dataset_name)

    def load_drug_features(self, data_path, dataset_name) -> FeatureDataset:
        self._lk = _lookups(data_path, dataset_name)
        return load_drug_ids_from_csv(data_path, dataset_name)
