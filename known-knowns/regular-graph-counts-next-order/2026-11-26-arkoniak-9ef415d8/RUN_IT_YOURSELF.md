# Run it yourself

From this folder, in a fresh shell (Python 3, gcc):

    sh verify-it-yourself/run_checks.sh

Expected output: six lines (1) to (6), each ending True or with empty mismatch lists [], then `PASS` (verify-it-yourself/RECEIPTS.md has the real output).

Rebuild the object: method D over every cycle type of N (two lanes), then the sum against method A:

    mkdir SCRATCH && cp how-we-built-it/methodD/* how-we-built-it/methodA/engine.py how-we-built-it/methodA/A_terms_d4.txt SCRATCH/ && cd SCRATCH && gcc -O2 -o svdp svdp.c
    python3 -I runDd.py --d 4 --N 29 --tcap 3600 --symL 1 --noA --out Dd4_N29_lane0.txt --lane 0 --lanes 2
    python3 -I runDd.py --d 4 --N 29 --tcap 3600 --symL 1 --noA --out Dd4_N29_lane1.txt --lane 1 --lanes 2
    python3 -I dsumcheck.py 29 A_terms_d4.txt Dd4_N29_lane0.txt Dd4_N29_lane1.txt

Larger N the same way (N=51, the claimed order: about 10 h on 2 cores, 239943 cycle types; `dsumcheck.py 51` must print AGREE with U_D = U_A = 152556963477307480948188554287675435592122034073857046). Method A: `gcc -O2 -o cubic cubic.c && python3 -I driver.py --bin ./cubic --deg 4 --nmax 51 --nprimes 8 --pivot max --dumpU` in how-we-built-it/methodA.
