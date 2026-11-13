# Run it yourself

## Quick check
From this folder: `sh verify-it-yourself/run_checks.sh` -> last line `PASS` (verify-it-yourself/RECEIPTS.md). Python 3
standard library only; it recomputes the detection, the null comparison and the glitch-catalogue gates G1 and G2 from
object/.

## Regenerate the glitch-catalogue extracts (standard library, about a minute plus the download)
1. Download the archive of https://doi.org/10.5281/zenodo.15715187 (lunar_ACC-v1.0.1.zip, 109655361 bytes, md5
   38e162c8e4407e750de3c5cb126fdcfd, the checksum the Zenodo record lists; sha256
   7278ac65c926e88d14748ee6a2ff32c17fb6fde84b3ecf20fbec5a6fcd12566d).
2. `python3 how-we-built-it/code/scripts/extract_spike_subset.py lunar_ACC-v1.0.1.zip regenerated/ window`
   (a folder holding S14_ACC-Spike_MH1_all.csv and S14_ACC-Spike_MH2_all.csv also works as the source). It refuses a
   source whose sha256 differs from 78e91b83...0a1 (MH1) / 1219c0fa...9f9 (MH2). Expected output: 48 MH1 rows, sha256
   1790975279fd0548ed0b0864685b76f400382a19e290698e53e02555dc63129f, and 65 MH2 rows, sha256
   6609a7ebc72c65c48c82e038be7868add87aae16bac367647db49f9c52ab2708. Both files must equal the
   object/glitch_catalogue_*_onset_pm24h.csv files byte for byte. With `year` instead of `window` it writes the full
   scanned-span extract that the package does not ship (1971 days 36-365: 9361 MH1 rows, sha256
   7ceff7e10c0f28d83a2dd1f84ba56ced5538533d4c66d146549f98e321ac6fa4; 11394 MH2 rows, sha256
   f3b6fb225730fd614ab9fc1de4e2592f874027d1e90b17520345fb005aa1f4ce).
3. Descriptive survey of all nine S14 files of the archive (not a gate):
   `python3 how-we-built-it/code/scripts/survey_nine_files.py lunar_ACC-v1.0.1.zip survey.json` (equals
   how-we-built-it/glitch_catalogue_survey.json), `python3 how-we-built-it/code/scripts/day133_hourly.py
   lunar_ACC-v1.0.1.zip hourly.csv` (equals how-we-built-it/glitch_catalogue_hourly_1971-05-12_to_14.csv) and
   `python3 how-we-built-it/code/scripts/coverage_boundaries.py lunar_ACC-v1.0.1.zip bounds.txt` (equals
   how-we-built-it/glitch_catalogue_coverage_boundaries.txt).
4. Our per-day interval counts and gap summary over 1971 days 36-365 (derived statistics, not gates):
   `python3 how-we-built-it/code/scripts/daily_counts.py lunar_ACC-v1.0.1.zip daily.csv gaps.txt` (equal to
   how-we-built-it/glitch_catalogue_daily_counts_1971d036-365.csv and glitch_catalogue_gap_summary.txt; about a minute).
5. G3 base rates (numpy and pandas; needs levent.1008weber.csv from
   https://pds-geosciences.wustl.edu/lunar/urn-nasa-pds-apollo_seismic_event_catalog/data/):
   `python3 how-we-built-it/code/scripts/g3_base_rates.py levent.1008weber.csv lunar_ACC-v1.0.1.zip g3.json`
   (same G3 counts as how-we-built-it/glitch_gates_A38.json: 3327 of 20000 random times, 898 of 6607 type-A events).

## Full re-run (about 2 hours, mostly download and the null)
Python 3 with numpy, scipy and pandas. In a working folder holding code/ (from how-we-built-it/code), frozen/ (the two
npz files), data/catalog/ (the PDS catalogue CSVs), data/pse/collection_data_seed_inventory.csv, data/lit/ (Onodera
CSVs, Zenodo 8373651; the two S14 ACC-Spike CSVs above) and waveforms/ (every URL in how-we-built-it/waveforms_manifest.csv,
fetched one at a time and checked against its sha256), follow how-we-built-it/COMMANDS.md. Expected: D 0.7417 at
1971-05-13 18:39:33.7 UTC for nest A38 (MH1 0.7268, MH2 0.7567); null over 1971 days 36-365: time-reversed maximum
0.2124, best of 400 phase-randomised controls 0.2868; glitch gates (COMMANDS.md step 7): output equal to
how-we-built-it/glitch_gates_A38.json; the object extracts (step 8) equal to object/ byte for byte.
