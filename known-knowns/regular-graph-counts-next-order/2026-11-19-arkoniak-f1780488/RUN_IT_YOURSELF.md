# Run it yourself (from this folder, fresh shell, Python 3)

1. Check: `sh verify-it-yourself/run_checks.sh` -> last line `PASS` (about 20 s).
2. Rebuild method A's per-type values: `python3 -I how-we-built-it/methodA/dump42.py py42.csv` (about 15 s; 53174 rows 'partition;F_A').
3. Rebuild method D's per-type values (about 1.1 h on 2 cores), one command per lane:
   `python3 -I how-we-built-it/methodD/runD.py --csv py42.csv --symL 7 --tcap 600 --lane 0 --lanes 2 --out D_lane0.txt`
   `python3 -I how-we-built-it/methodD/runD.py --csv py42.csv --symL 7 --tcap 600 --lane 1 --lanes 2 --out D_lane1.txt`
   Every line ends `;ok;` when F_D equals F_A. `--pmod 607` repeats it modulo 2^607-1 instead of 2^521-1.
4. U(42) and the comparison with method A's C engine terms: `python3 -I how-we-built-it/methodD/dsumcheck.py 42 how-we-built-it/methodA/A_terms_d3.txt D_lane0.txt D_lane1.txt`
   -> `N=42 types=53174 U_D=264928974203634896907 U_A=264928974203634896907 AGREE`.
5. The object: `object/A002851_21.txt` (the term); `object/F_N42_part*.txt` ('partition;F_D' for every cycle type of 42).
