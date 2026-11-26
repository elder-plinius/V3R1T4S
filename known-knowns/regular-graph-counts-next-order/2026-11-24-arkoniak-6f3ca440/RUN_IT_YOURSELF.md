# Run it yourself (from this folder, fresh shell, Python 3, gcc)

1. Check: `sh verify-it-yourself/run_checks.sh` -> last line `PASS` (about 5 minutes).
2. Method A terms (C engine): `mkdir -p build && gcc -O2 -o build/cubic how-we-built-it/methodA/cubic.c && python3 -I how-we-built-it/methodA/driver.py --bin build/cubic --deg 5 --nmax 30 --nprimes 8 --pivot max --dumpU`
   -> line `30 1690586697369281612308192667831589 1690586697346784893842479211750187` (N, U, C), as in how-we-built-it/methodA/A_terms_d5.txt.
3. Method D per-type values: copy how-we-built-it/methodD/ and how-we-built-it/methodA/engine.py into one scratch folder, `gcc -O2 -o svdp svdp.c` there, then per lane L in 0 1:
   `python3 -I runDd.py --d 5 --N 30 --tcap 7200 --symL 1 --noA --vdp --cvdp --out Dd5_N30_laneL.txt --lane L --lanes 2`
   (rows 'partition;F_D;-1;Donly;seconds'; a row marked ERR is retried by rerunning the same command).
4. U_D(30) vs method A: `python3 -I dsumcheck.py 30 A_terms_d5.txt Dd5_N30_lane0.txt Dd5_N30_lane1.txt` -> `... AGREE`.
5. The object: `object/A006821_15.txt` (the term); `object/F_N30.txt` ('partition;F_D' for every cycle type of 30).
