# Run it yourself

## Quick check (seconds)

From this folder: `sh verify-it-yourself/run_checks.sh` -> last line `PASS` (see verify-it-yourself/RECEIPTS.md).

## Full re-run from the waveforms (hours, mostly download)

Python 3 with numpy, scipy and pandas. From how-we-built-it/:
1. Download every URL in waveforms_manifest.csv into waveforms/s12/ (one request at a time, a few seconds apart;
   check each file against its sha256). Download levent.1008weber.csv (URL in the-record-we-beat/RECORD.md) into
   data/catalog/ and collection_data_seed_inventory.csv
   (https://pds-geosciences.wustl.edu/lunar/urn-nasa-pds-apollo_pse/data/collection_data_seed_inventory.csv) into
   data/pse/.
2. Follow COMMANDS.md (its paths are relative to a folder holding code/, data/, frozen/ and waveforms/; copy
   A1_s12_dev1972_templates.npz into frozen/): rebuild the frozen templates from 1972 (step 3), scan 1971 (step 4),
   score (step 5) and run the null test (step 6). Expected: recovered 63 of 67, 400 time-reversed detections >= theta
   over 334.54 scanned day-equivalents (1.196 per day), null test best control 0.0484 against real 0.9403.
