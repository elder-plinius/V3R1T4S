# Run it yourself (from this folder, fresh shell, Python 3, gcc)

1. Check: `sh verify-it-yourself/run_checks.sh` -> last line `PASS` (about 10 minutes).
2. Method A terms (C engine): `mkdir -p build && gcc -O2 -o build/cubic how-we-built-it/methodA/cubic.c && python3 -I how-we-built-it/methodA/driver.py --bin build/cubic --deg 6 --nmax 25 --nprimes 8 --pivot max --dumpU`
   -> line `25 1058090189356373578845816711343 1058090189356372623457538781723` (N, U, C), as in how-we-built-it/methodA/A_terms_d6.txt.
3. Method D per-type values: copy how-we-built-it/methodD/ and how-we-built-it/methodA/engine.py into one scratch folder, `gcc -O2 -o svdp svdp.c` there, then per lane L in 0 1:
   `python3 -I runDd.py --d 6 --N 25 --tcap 7200 --symL 1 --noA --vdp --cvdp --out Dd6_N25_laneL.txt --lane L --lanes 2`
   (rows 'partition;F_D;-1;Donly;seconds'; a row marked ERR is retried by rerunning the same command).
4. U_D(25) vs method A: `python3 -I dsumcheck.py 25 A_terms_d6.txt Dd6_N25_lane0.txt Dd6_N25_lane1.txt`
   -> `N=25 types=1958 U_D=1058090189356373578845816711343 U_A=1058090189356373578845816711343 AGREE`.
5. The object: `object/A006822_25.txt` (the term); `object/F_N25.txt` ('partition;F_D' for every cycle type of 25).
