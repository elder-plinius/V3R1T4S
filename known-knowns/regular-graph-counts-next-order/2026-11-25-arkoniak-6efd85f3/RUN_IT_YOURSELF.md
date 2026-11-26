# Run it yourself

From this folder, in a fresh shell (Python 3, gcc):

    sh verify-it-yourself/run_checks.sh

Expected output: five lines (1) to (5), each ending True or with empty mismatch lists [], then `PASS` (verify-it-yourself/RECEIPTS.md has the real output).

Rebuild the object: method D over every cycle type of N (two lanes), then the sum against method A:

    mkdir SCRATCH && cp how-we-built-it/methodD/* how-we-built-it/methodA/engine.py how-we-built-it/methodA/A_terms_d4.txt SCRATCH/ && cd SCRATCH && gcc -O2 -o svdp svdp.c
    python3 -I runDd.py --d 4 --N 29 --tcap 3600 --symL 1 --noA --out Dd4_N29_lane0.txt --lane 0 --lanes 2
    python3 -I runDd.py --d 4 --N 29 --tcap 3600 --symL 1 --noA --out Dd4_N29_lane1.txt --lane 1 --lanes 2
    python3 -I dsumcheck.py 29 A_terms_d4.txt Dd4_N29_lane0.txt Dd4_N29_lane1.txt

Larger N the same way (N=50: about 8 h on 2 cores). Method A: `gcc -O2 -o cubic cubic.c && python3 -I driver.py --bin ./cubic --deg 4 --nmax 50 --nprimes 8 --pivot max --dumpU` in how-we-built-it/methodA.
