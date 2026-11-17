# Run it yourself

## Quick check
From this folder: `sh verify-it-yourself/run_checks.sh` -> last line `PASS` (verify-it-yourself/RECEIPTS.md).

## Full re-run (about 2 hours, mostly download and the null)
Python 3 with numpy, scipy and pandas. Build a working folder holding code/ (how-we-built-it/code: tools/, scripts/,
fullwin/), frozen/ (how-we-built-it/frozen), results/ (how-we-built-it/results), data/catalog/ (the PDS catalogue CSVs
from https://pds-geosciences.wustl.edu/lunar/urn-nasa-pds-apollo_seismic_event_catalog/data/),
data/pse/collection_data_seed_inventory.csv (PDS apollo_pse bundle), data/lit/ (Onodera CSVs, Zenodo 8373651),
data/lit_acc/ (the Liu, Xiao and Li 2025 S14 and S16 catalogue CSVs from the lunar_ACC v1.0.1 release, Zenodo
15715187; check them against how-we-built-it/glitch_catalogue_SHA256SUMS.txt) and waveforms/ (every URL in
how-we-built-it/waveforms_urls.txt plus the ATT files listed there (S14 and S16, 1973 days 3, 139, 194, 221, 248, 303, 330, 357; S14 also day 10),
fetched one at a time and checked against how-we-built-it/waveforms_SHA256SUMS.txt). Then follow
how-we-built-it/COMMANDS.md steps 1-13 from that folder.

Expected: Dt 0.3433 at window start 1973-11-26 07:45:58.641 UTC for nest A100 (S14 MH1 0.4264, MH2 0.5621 at +1.509 s;
S16 MH1 0.6994, MH2 -0.0128 at +2.113 s); null over all of 1973: time-reversed maximum 0.1574, best of 400
S16-shifted controls 0.1906; ATT-corrected S16 - S14 0.93 s against the nest's 0.82 s; anomalistic phase 157.2 deg in
[46.7, 318.3]; attribution and glitch-gate outputs as in how-we-built-it/results/.
