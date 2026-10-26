"""Confirmatory run of the frozen PotencyTransfer (PREREG.v4) through drevalpy 1.3.5's own CLI entry
point. The only addition to the stock pipeline is registering the model class in MODEL_FACTORY.
usage: run_confirmatory.py <run_id>    (reuses the splits already saved in that result directory)"""
import os
import sys, os
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "4"
sys.path.insert(0, os.environ.get("PKG", ".") + "/how-we-built-it")
from potency_transfer_model import PotencyTransfer
from drevalpy.models import MODEL_FACTORY, MULTI_DRUG_MODEL_FACTORY
MODEL_FACTORY["PotencyTransfer"] = PotencyTransfer
MULTI_DRUG_MODEL_FACTORY["PotencyTransfer"] = PotencyTransfer   # experiment.get_model_name_and_drug_id checks this dict
from drevalpy.utils import get_parser, main
args = get_parser().parse_args([
    "--run_id", sys.argv[1], "--path_data", os.environ.get("DATA", "./data"), "--dataset_name", "CTRPv2",
    "--test_mode", "LDO", "--n_cv_splits", "10", "--optim_metric", "RMSE", "--response_transformation", "None",
    "--models", "PotencyTransfer", "--baselines", "NaiveMeanEffectsPredictor", "--path_out", os.environ.get("RESULTS", "./results")])
print("drevalpy args:", vars(args), flush=True)
main(args)
print("CONFIRMATORY RUN COMPLETE", flush=True)
