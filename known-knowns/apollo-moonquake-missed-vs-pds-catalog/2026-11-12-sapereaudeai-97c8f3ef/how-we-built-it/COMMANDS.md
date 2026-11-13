# REPRODUCE (p2 claim)

All commands run from the claim/ folder (create an out/ folder there first) with Python 3 + numpy, scipy, pandas (no other packages; no programs are
downloaded). The waveform files are in waveforms/s12/ (sha256 list waveforms/SHA256SUMS_waveforms.txt) and can be
re-fetched one by one from the URLs in data/urls_s12_1971.txt and data/urls_s12_dev1972.txt (NASA PDS Geosciences
Node, bundle urn:nasa:pds:apollo_pse). EarthScope FDSN was not reachable from the claimant's network, so PDS file
URLs replace FDSN request URLs.

1. Check the waveform copies:
   `cd waveforms && sha256sum -c SHA256SUMS_waveforms.txt && cd ..`
2. (Optional) decoder check against the PDS GeoCSV twin of one file (needs xa.s12.00.mhz.1973.001.0.mseed and its
   .a.csv from the PDS; output in data/validation/):
   `python -I code/tools/validate_vs_geocsv.py <mseed> <a.csv> code/tools`
3. (Optional) rebuild the frozen templates and threshold from the 1972 dev days (about 1 min):
   `python -I code/scripts/dev_eval.py 0.25 1.0 450 0.1 s12 out/dev_check`
   and compare out/dev_check.npz (tm, theta) with frozen/A1_s12_dev1972_templates.npz.
4. Scan 1971 with the frozen templates (forward data, time-reversed data and 400 phase-randomised template
   controls; about 15-20 s per day, resumable; give 0 instead of 400 to skip the controls, p2 does not need them):
   `python -I code/scripts/score_scan.py frozen/A1_s12_dev1972_templates.npz 1971 1 365 out/scan.jsonl 400 20261112`
   The result should equal results/scan_s12_A1_1971.jsonl (deterministic; floating-point last digits may differ
   on other machines).
5. Score p2 (recovery at the frozen theta, false alarms on time-reversed data, chance recovery, curve):
   `python -I code/scripts/score_p2.py frozen/A1_s12_dev1972_templates.npz results/scan_s12_A1_1971.jsonl data/catalog/levent.1008weber.csv 71 out/p2`
6. Null test (400 shifted catalogues):
   `python -I code/scripts/p2_null.py frozen/A1_s12_dev1972_templates.npz results/scan_s12_A1_1971.jsonl data/catalog/levent.1008weber.csv 71 out/null_test.md`

Set APOLLO_WF to another waveform folder (with an s12/ subfolder) if the files are elsewhere.
