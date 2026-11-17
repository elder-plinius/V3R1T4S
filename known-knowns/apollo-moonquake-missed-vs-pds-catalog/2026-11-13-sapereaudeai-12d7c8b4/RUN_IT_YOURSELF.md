# Run it yourself

## Quick check
From this folder: `sh verify-it-yourself/run_checks.sh` -> last line `PASS` (verify-it-yourself/RECEIPTS.md).

## Full re-run (about 2 hours, mostly download and the null)
Python 3 with numpy, scipy and pandas. In a working folder holding code/ (from how-we-built-it/code), frozen/ (the two
npz files), data/catalog/ (the PDS catalogue CSVs), data/pse/collection_data_seed_inventory.csv, data/lit/ (Onodera
CSVs, Zenodo 8373651; the Liu et al. 2025 S14 ACC-Spike CSVs, Zenodo 15715187) and waveforms/ (every URL in
how-we-built-it/waveforms_manifest.csv, fetched one at a time and checked against its sha256), follow
how-we-built-it/COMMANDS.md. Expected: D 0.6439 at 1971-09-05 01:25:44.150 UTC for nest A39 (MH1 0.5952, MH2 0.6925);
null over 1971 days 36-365: time-reversed maximum 0.2205, best of 400 phase-randomised controls 0.3180.
