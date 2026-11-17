#!/bin/sh
# Fetch the three shipped inputs from khsjursen/ML_MB_Norway at the pinned commit into ./data and check their sha256.
# One plain request per file; do not retry on 401/403/429/503.
set -e
C=32d8175adab27963c6ca2766f2420f24cdb72a6b
B=https://raw.githubusercontent.com/khsjursen/ML_MB_Norway/$C/src
mkdir -p data
for f in Data/2023-08-28_stake_mb_norway_cleaned_ids_latlon_wattributes_climate_svf.csv \
         Data/2023-08-28_stake_mb_norway_cleaned_ids_latlon_wattributes_climate_test_svf.csv \
         Training_cluster/2024-10-24_10-30-28/custom_loss_best_model.json; do
  curl -sS --fail -A "V3R1T4S reproduction" --max-time 120 -o "data/$(basename "$f")" "$B/$f"
done
cd data && sha256sum -c ../expected_data_sha256.txt
