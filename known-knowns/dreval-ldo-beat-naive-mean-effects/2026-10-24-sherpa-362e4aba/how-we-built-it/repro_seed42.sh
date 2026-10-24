#!/bin/bash
# Reproduction of record: published LDO leaders + baseline, drevalpy 1.3.5, CTRPv2, 10 splits,
# split seed 42 (hard-coded in 1.3.5 experiment.py), RMSE tuning, no response transformation.
cd ${RESULTS:-./results}
${ENV:-./env}/bin/drevalpy \
  --run_id repro_seed42 \
  --path_data ${DATA:-./data} \
  --dataset_name CTRPv2 \
  --test_mode LDO \
  --n_cv_splits 10 \
  --optim_metric RMSE \
  --response_transformation None \
  --models MultiOmicsNeuralNetwork GradientBoosting SimpleNeuralNetwork \
  --baselines NaiveMeanEffectsPredictor \
  --path_out ${RESULTS:-./results}
