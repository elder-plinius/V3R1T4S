"""Run the published leader (MultiOmicsNeuralNetwork) on ONE LDO fold, using drevalpy 1.3.5's own
hyperparameter tuning and training calls, exactly as experiment.py does for the FIRST model in a run:

    best = hpam_tune(train, validation, hpam_set=model.get_hyperparameter_set(), metric="RMSE")
    train.add_rows(validation); train.shuffle(42)
    train_and_predict(model, best, train, test)

Folds are independent, so this lets the 10 folds run concurrently instead of sequentially. Writes the
prediction CSV in the pipeline's own format and layout.
usage: leader_fold.py <splits_dir> <out_dir> <fold>
"""
import os
import sys, os, json, pathlib
os.environ.setdefault("OMP_NUM_THREADS", "2"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")
import pandas as pd
from drevalpy.datasets.loader import load_ctrpv2
from drevalpy.models import MODEL_FACTORY
from drevalpy.experiment import hpam_tune, train_and_predict
DATA = os.environ.get("DATA", "./data")
splits_dir, out_dir, fold = sys.argv[1], sys.argv[2], int(sys.argv[3])
ds = load_ctrpv2(path_data=DATA); ds.remove_nan_responses(); ds.load_splits(path=splits_dir)
s = ds.cv_splits[fold]
cls = MODEL_FACTORY["MultiOmicsNeuralNetwork"]
model = cls(); model.build_model(cls.get_hyperparameter_set()[0])
best = hpam_tune(model=model, train_dataset=s["train"], validation_dataset=s["validation"],
                 early_stopping_dataset=(s["early_stopping"] if model.early_stopping else None),
                 hpam_set=cls.get_hyperparameter_set(), response_transformation=None, metric="RMSE",
                 path_data=DATA, model_checkpoint_dir="TEMPORARY")
tr = s["train"]; tr.add_rows(s["validation"]); tr.shuffle(random_state=42)
out = train_and_predict(model=model, hpams=best, path_data=DATA, train_dataset=tr,
                        prediction_dataset=s["test"],
                        early_stopping_dataset=(s["early_stopping"] if model.early_stopping else None),
                        response_transformation=None, model_checkpoint_dir="TEMPORARY")
p = pathlib.Path(out_dir) / "MultiOmicsNeuralNetwork" / "predictions"; p.mkdir(parents=True, exist_ok=True)
pd.DataFrame({"cell_line_name": out.cell_line_ids, "pubchem_id": out.drug_ids,
              "response": out.response, "predictions": out.predictions}
             ).to_csv(p / f"predictions_split_{fold}.csv", index=False)
hp = pathlib.Path(out_dir) / "MultiOmicsNeuralNetwork" / "best_hpams"; hp.mkdir(parents=True, exist_ok=True)
json.dump(best, open(hp / f"best_hpams_split_{fold}.json", "w"))
print(f"fold {fold} done: {len(out.predictions)} predictions, hpams {best}", flush=True)
