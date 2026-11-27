#!/bin/sh
# Fetch the three files of github.com/khsjursen/ML_MB_Norway that the code reads (about 22 MB) into data/
# (not shipped: third-party data, MIT license; stake data NVE, doi:10.58059/sjse-6w92) and check their sha256.
# Run from how-we-built-it/:  sh get_data.sh
set -e
cd "$(dirname "$0")"
mkdir -p data
B=https://raw.githubusercontent.com/khsjursen/ML_MB_Norway/main/src
for p in Data/2023-08-28_stake_mb_norway_cleaned_ids_latlon_wattributes_climate_svf_monthly.csv \
         Data/2023-08-28_stake_mb_norway_cleaned_ids_latlon_wattributes_climate_test_svf.csv \
         Training_cluster/2024-10-24_10-30-28/custom_loss_best_model.json; do
  f=data/src_$(echo "$p" | tr / _)
  [ -f "$f" ] || curl -sSfL -o "$f" "$B/$p"
done
shasum -a 256 -c <<'EOF'
19e10b018db4e291f4e9e99dcc908ca08a82ef25817b633a3b809b3b30200e94  data/src_Data_2023-08-28_stake_mb_norway_cleaned_ids_latlon_wattributes_climate_svf_monthly.csv
d1d34e0821a9147a3a166b6dc4ee8cee8abed8a288e2ab89cdd107273f100f1c  data/src_Data_2023-08-28_stake_mb_norway_cleaned_ids_latlon_wattributes_climate_test_svf.csv
a7ddf96b2f11a51dd8415fbe6190f95671c23123526e200533fb09aae74e1d0d  data/src_Training_cluster_2024-10-24_10-30-28_custom_loss_best_model.json
EOF
