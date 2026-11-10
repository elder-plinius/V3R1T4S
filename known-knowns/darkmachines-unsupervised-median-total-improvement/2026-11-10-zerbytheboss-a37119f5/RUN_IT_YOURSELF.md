# Run It Yourself

## 1. Standalone Verification & Live Channel `2a` Retraining (`~3` seconds)

From this package folder in a fresh shell (requires Python 3.8+ with `numpy`):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:

```text
Negative control rejected perturbed CSV cell.
Verified all 136 signal-channel rows and live Channel 2a retraining (max float32 diff = 0.0000).
BSPOT_MaxSec     : cha300 TI = 6.0000 (> 1.10), cha400 TI = 7.0000 (> 1.00), Median_TI = 5.3759.
BSPOT_Union_OR   : cha300 TI = 3.0000 (> 1.10), cha400 TI = 5.0000 (> 1.00), Median_TI = 5.0000, Min_TI = 0.8000 (>= 0.80).
BSPOT_FloorGuard : cha300 TI = 1.8000 (> 1.10), cha400 TI = 2.2136 (> 1.00), Median_TI = 3.1000, Min_TI = 0.9000 (>= 0.90).
PASS
```

## 2. Full 4-Channel Rebuild From Raw Zenodo `3961917` CSVs (`~2` minutes featurization + `~30` seconds BS-POT evaluation)

Download `Unsupervised_Hackathon_files.tar.gz` (`2.1 GB`, Zenodo `3961917`), extract `chan1/`, `chan2a/`, `chan2b/`, `chan3/` into `./training_files`, and compile the deterministic C99 featurizer and BS-POT evaluator:

```sh
cc -O3 -std=c99 -Wall -Wextra how-we-built-it/dm_featurize.c -lm -o dm_featurize
cc -O3 -std=c99 -Wall -Wextra how-we-built-it/dm_bsp_eval.c -lm -o dm_bsp_eval
for ch in chan1 chan2a chan2b chan3; do
  mkdir -p "./cache/$ch"
  for csv_file in "./training_files/$ch"/*.csv; do
    ./dm_featurize "$csv_file" "./cache/$ch/$(basename "$csv_file" .csv).bin"
  done
done
./dm_bsp_eval ./cache ./bspot_raw_counts.csv
python3 how-we-built-it/export_bspot_objects.py ./bspot_raw_counts.csv verify-it-yourself/data/bspot_eval_ref.json.gz ./darkmachines_bspot_results.csv ./darkmachines_19signals_bspot_summary.tsv
```

`dm_bsp_eval` trains strictly on odd-`event_ID` SM background events per channel and evaluates exact tie-aware thresholds across `100%` of even-`event_ID` SM background events (including all `4,261,244` even background events in Channel `3`) in `~30` seconds, and `how-we-built-it/export_bspot_objects.py` applies deterministic row ordering and IEEE-754 2-decimal `eps_S` rounding (`notebooks/04-SignificanceImprovement.ipynb`) to reproduce `object/darkmachines_bspot_results.csv` and `object/darkmachines_19signals_bspot_summary.tsv` byte-for-byte.
