# Run it yourself

## Quick check
From this folder: `sh verify-it-yourself/run_checks.sh` -> last line `PASS` (verify-it-yourself/RECEIPTS.md). Python 3
standard library only; set PYTHON if `python3` is not on PATH. Under a second. From the saved preprocessed S14 and S16
windows and the saved A100 stack (object/window_and_template.csv) it recomputes every channel's NCC at each lag within
+/- 7 samples, each station's best lag, Dt, R7, the null (Dt above all 401 controls' full-span maxima,
object/null_full_span_maxima.csv), R8 (ATT-corrected S16 - S14 against the saved reference values), R9 (anomalistic
phase in the 95% interval of the 62 catalogued A100 events), the thermal check and the saved catalogue distances.

## Full re-run (about 2 hours, mostly download, the null and the reverse search)
Python 3 with numpy, scipy and pandas. Build a working folder holding code/ (how-we-built-it/code: tools/, scripts/,
fullwin/, c1030/), frozen/ (how-we-built-it/frozen), results/ (how-we-built-it/results, for comparison), and data/:
data/catalog/ (the PDS catalogue CSVs from https://pds-geosciences.wustl.edu/lunar/urn-nasa-pds-apollo_seismic_event_catalog/data/),
data/pse/collection_data_seed_inventory.csv (PDS apollo_pse bundle), data/lit/ (Onodera CSVs, Zenodo 8373651;
Knapmeyer-Endrun and Hammer 2015 supporting tables, doi:10.1002/2015JE004862; Bulow et al. 2005 PDF), data/lit_acc/
(the Liu, Xiao and Li 2025 S14 and S16 catalogue CSVs from the lunar_ACC v1.0.1 release, Zenodo 15715187; check them
against how-we-built-it/glitch_catalogue_SHA256SUMS.txt), data/urls_s14_s16_1973_mh12.txt and data/urls_att_and_s12.txt
(both are in how-we-built-it/waveforms_urls.txt), and waveforms/ (every URL in how-we-built-it/waveforms_urls.txt,
fetched one at a time and checked against how-we-built-it/waveforms_SHA256SUMS.txt, in subfolders s14/, s16/, s12/
and att/). Step 2's determinism check and step 12's S12 comparison read two files from the earlier lenses
(data/lens_scan_1973.jsonl, data/lens_s12s14_candidates_stdout.txt); without them, skip the determinism line and pass
any file holding the line "A100: null C0 0.118, best shift 0.203, best control 0.203". Then follow
how-we-built-it/COMMANDS.md steps 1-13.

Expected: Dt 0.2981 at window start 1973-10-30 02:25:21.509 UTC for nest A100 (S14 MH1 0.4936, MH2 0.6211 at
-1.509 s; S16 MH1 0.6196, MH2 -0.0235 at -0.906 s); null over all of 1973: time-reversed maximum 0.1574, best of 400
S16-shifted controls 0.1906; ATT-corrected S16 - S14 0.71 s against the nest's 0.82 s; anomalistic phase 161.5 deg in
[46.7, 318.3]; attribution, glitch-gate and multiplicity outputs as in how-we-built-it/results/.

## Rebuild the object files
After steps 2-3, copy out/scan12_1973.jsonl and out/cand12.json into results/, then from the working folder:
`python -I -B code/c1030/build_object_1030.py . out/object` (frozen pipeline; writes candidate.json,
window_and_template.csv, null_full_span_maxima.csv, null_daily_maxima.csv, a100_catalogue_times.csv and
r8_reference.csv) and compare with object/.
