# Run It Yourself (`2026-10-20-mizopl-56ac1336`)

1. Ensure `python3` (`>= 3.9`) and `numpy` are installed.
2. From the root of this package directory, execute:
   ```sh
   sh verify-it-yourself/run_checks.sh
   ```
3. The script parses all `2,192` rows of `object/streamfulldata2026.txt.gz` and the verbatim GMN trajectory lines in `object/new_shower_gmn_lines.txt`, `object/m1_cepheus_core_gmn_lines.txt`, `object/m1_cepheus_mc_gmn_lines.txt`, `object/m3_camelopardalis_gmn_lines.txt`, `object/p1_outburst_gmn_lines.txt`, and `object/p2_recurrence_gmn_lines.txt`, verifies every orbital compactness ($D_{\text{SH}}$), MDC isolation, station/country diversity, and 400-control null test metric, and prints `PASS` on the final line.
