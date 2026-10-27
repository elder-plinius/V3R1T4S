# How we built it

- **code/:** the claim's scripts, as the panel saw them.
  - null_full.py: the detector, the full null and the per-control maxima.
  - early_null.py: the early-hours sensitivity.
  - locate.py, mag_check.py, mc_table.py, checks.py and blast_table.py: the other numbers.
  - checker_cc.py: the from-definition check of the detector's correlation. Its output is checker_v2_out.txt.
- **claim/:** claim.md and REPRODUCE.md as the panel saw them. REPRODUCE.md gives a command for every number.
- **PREREG.md and PREREG.v2.md:** the run's frozen rules.
- **null_test.md:** the null result.
- **data/:**
  - Control job lists and summaries.
  - The real detections.
  - The Mc gate.
  - Every request log (URL, UTC time, HTTP status, bytes, sha256).
- **claim_data_manifest.json:** the size and sha256 of every input file the claim used. That includes the large or
  third-party files that are not copied in (templates.json, waveforms, StationXML, ComCat CSVs, the Zenodo catalogue).
- **Python:** 3.13 with requirements.txt.
