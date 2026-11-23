import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drevalpy.datasets.loader import load_ctrpv2
from drevalpy.experiment import drug_response_experiment
from drevalpy.models import MODEL_FACTORY
import custom_models, custom_models_v131, ensemble_model  # noqa: F401

resp = load_ctrpv2(path_data="data", measure="LN_IC50_curvecurator")
print("rows loaded", len(resp), flush=True)
t0 = time.time()
drug_response_experiment(
    models=[MODEL_FACTORY["EnsembleResidualOmics"]],
    response_data=resp,
    run_id="att_v1ens_v2",
    test_mode="LCO",
    n_cv_splits=10,
    path_out="results",
    path_data="data",
    hyperparameter_tuning=True,
    hpam_optimization_metric="Pearson",  # validation-only model selection (disclosed in PREREG.v5)
)
print(f"ENS2 DONE in {time.time()-t0:.0f}s", flush=True)
