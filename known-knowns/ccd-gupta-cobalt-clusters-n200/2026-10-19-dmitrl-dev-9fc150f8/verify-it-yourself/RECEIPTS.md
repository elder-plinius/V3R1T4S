# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this folder on 2026-10-19 (Python 3.11.17, numpy
2.4.6, scipy 1.17.1), with CCD_DATA_DIR set to the folder holding the three CCD files as
downloaded on 2026-10-19 (their sha256 match the pins; the download mode was also run once and printed PASS). Wall time
about 36 s; exit status 0.

```text
rows checked: 199; Co.zip rows: 10
as posted, energy off by more than 1e-5 eV at N = 163, 175, 179, 183, 185, 188, 189, 190
after polishing, every posted energy reproduced within 1e-5 eV: True
posted structures that polish lower by more than 1e-4 eV: none
rows whose best known energy is the Co.zip one: 84, 95, 101, 113, 121, 122, 196, 197, 198, 200
PASS
```
