# RECEIPTS — real output of: sh verify-it-yourself/run_checks.sh
# (captured 2026-10-17T13:31:32Z on a 10-core laptop)

A. ground-truth brute force (all 2^(2n^2) orientations), n=1..3:
   n=1: 4
   n=2: 18
   n=3: 148
B. independent sector transfer matrix (pure python), reproduce n=1..10:
   n= 1: 4  OK
   n= 2: 18  OK
   n= 3: 148  OK
   n= 4: 2970  OK
   n= 5: 143224  OK
   n= 6: 16448400  OK
   n= 7: 4484823396  OK
   n= 8: 2901094068042  OK
   n= 9: 4448410550095612  OK
   n=10: 16178049740086515288  OK
C. n=15 object vs saved residues (independent CRT + bound):
   RUN_A: 11 primes, CRT==object? True, modulus bits=220, residue mismatches=0
   RUN_B: 12 primes, CRT==object? True, modulus bits=228, residue mismatches=0
   prime-set intersection across runs: empty
D. optional numpy recomputation of RUN_A residue mod 1048387 (n=15):
   recomputed=576767  stored=576767  value%p=576767  match=True

PASS
