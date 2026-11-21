"""Run one or more drevalpy models through the package pipeline (CTRPv2 LCO 10-fold).

Usage: python run_model.py <measure> <run_id> <model_names...>
Example: python run_model.py LN_IC50 rf_lco_v1 RandomForest
"""
import os
import sys
import time

import numpy as np  # noqa: F401  (kept for debugging sessions)

from drevalpy.datasets.loader import load_ctrpv2
from drevalpy.experiment import drug_response_experiment
from drevalpy.models import MODEL_FACTORY

# custom attacker models live in this directory; import them so the
# registration side effects in custom_models.py run before the factory is read
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import custom_models  # noqa: F401,E402  (registers attacker classes in MODEL_FACTORY)
import custom_models_v131  # noqa: F401,E402  (registers v1.3.1-ruler attacker classes)
import ensemble_model  # noqa: F401,E402  (registers EnsembleResidualOmics)


def main() -> None:
    measure = sys.argv[1]
    run_id = sys.argv[2]
    model_names = sys.argv[3:]
    t0 = time.time()
    print(f"[run_model] measure={measure} run_id={run_id} models={model_names}", flush=True)
    response = load_ctrpv2(path_data="data", measure=measure)
    print(f"[run_model] response dataset: {len(response.cell_line_ids)} rows, "
          f"{len(set(response.cell_line_ids))} cell lines, {len(set(response.drug_ids))} drugs", flush=True)
    models = []
    for name in model_names:
        if name not in MODEL_FACTORY:
            raise SystemExit(f"unknown model {name}; factory keys: {sorted(MODEL_FACTORY)[:20]}...")
        models.append(MODEL_FACTORY[name])
    drug_response_experiment(
        models=models,
        response_data=response,
        run_id=run_id,
        test_mode="LCO",
        n_cv_splits=10,
        path_out="results",
        path_data="data",
        hyperparameter_tuning=True,
    )
    print(f"[run_model] DONE in {time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
