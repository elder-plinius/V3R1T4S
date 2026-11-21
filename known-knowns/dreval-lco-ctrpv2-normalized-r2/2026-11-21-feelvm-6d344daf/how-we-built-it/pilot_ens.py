import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drevalpy.datasets.loader import load_ctrpv2
from drevalpy.experiment import drug_response_experiment
from drevalpy.models import MODEL_FACTORY
import custom_models  # noqa: F401
import custom_models_v131  # noqa: F401
import ensemble_model  # noqa: F401

resp = load_ctrpv2(path_data="data", measure="LN_IC50_curvecurator")
resp.remove_nan_responses()
rng = np.random.default_rng(7)
sub = resp.copy()
mask = np.zeros(len(sub), dtype=bool)
idx = rng.choice(len(sub), size=40000, replace=False)
mask[idx] = True
sub.mask(mask)
print("pilot rows:", len(sub), flush=True)
t0 = time.time()
drug_response_experiment(
    models=[MODEL_FACTORY["EnsembleResidualOmics"]],
    response_data=sub,
    run_id="pilot",
    test_mode="LCO",
    n_cv_splits=2,
    path_out="results_pilot",
    path_data="data",
    hyperparameter_tuning=True,
)
print(f"PILOT DONE in {time.time()-t0:.0f}s", flush=True)
