# Run it yourself
From this folder in a fresh shell:
```sh
sh verify-it-yourself/run_checks.sh
# optional, skip the 137 MB download: SSP_TARBALL=/path/to/ssp_coords.tar.gz sh verify-it-yourself/run_checks.sh
```
Expected output: one line per N ending in OK, then `# rows 90 failed 0` and `PASS` (see verify-it-yourself/RECEIPTS.md).
Rebuild the object: `python3 how-we-built-it/repro_ssp_radiustxt.py` (stdlib + mpmath) prints the same 90 rows and PASS; captured output in how-we-built-it/repro_local_output.txt.
