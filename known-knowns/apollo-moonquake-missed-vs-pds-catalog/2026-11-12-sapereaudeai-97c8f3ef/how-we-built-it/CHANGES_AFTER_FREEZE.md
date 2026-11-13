# Changes after the freeze and implementation notes (disclosed; no scored number changes)

- The code here is a copy of the frozen run code with machine-specific absolute paths rewritten to package-relative
  ones (the run's tools/sanitize_paths.py); four files therefore differ from the sha256 values listed in PREREG.v2.md
  (apollo_lib.py, score_scan.py, score_p2.py, candidates.py). The REPRODUCE and CRITERION skeptics showed the copies
  reproduce the saved scan (all 365 days), p2.json, null_test.md and the frozen templates bit for bit.
- Preprocessing marks samples within 20 s of a gap (-1 sample or missing record) as invalid (pad_s = 20 in
  apollo_lib.preprocess); PREREG.md does not spell this out. It costs one catalogued event (1971-08-06 07:20, a 45 s
  telemetry gap 535-582 s after the catalogued start) and about 11 scanned day-equivalents (REPRODUCE).
- apollo_lib.decluster keeps the largest sample greedily within +/- 5 min rather than first restricting to local
  maxima as PREREG.md words it; REPRODUCE recounted with local maxima: 400 reversed and 444 forward detections, same.
- PREREG.md says "52 days" of dev data: 52 day files were fetched (event windows can cross midnight); 49 days hold
  the 54 dev events.
- null_test.md's command line uses run-folder paths; in this package the same script is
  how-we-built-it/code/scripts/p2_null.py.
