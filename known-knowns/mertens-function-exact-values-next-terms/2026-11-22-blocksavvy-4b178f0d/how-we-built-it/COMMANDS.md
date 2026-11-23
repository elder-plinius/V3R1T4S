# How the object was built (exact commands; run from this folder in a fresh shell)

Needs gcc with OpenMP and python3 (sympy only for check_windows.py). No other dependencies.

```sh
gcc -O2 -fopenmp -o msieve msieve.c -lm
gcc -O2 -fopenmp -o msieve2 msieve2.c -lm

# Run 1: product-check segmented Mobius sieve, blocks of 1e8, k = 1 .. 3.4e11 (about 10 min on 8 cores)
nice -n 19 ./msieve blocks 100000000 0 3400 > my_blocks.txt
python3 combine.py my_blocks.txt          # compare with logs/msieve_out_combine.txt
./msieve scan 330000000001 330100000000 -257128 262144   # expect: first k=330055906058 M=-262144

# Run 2: different code (log-sum mu test, segment 2^15), blocks of 1.25e8, k = 1 .. 3.30125e11 (about 15 min on 6 cores)
nice -n 19 ./msieve2 blocks 125000000 0 2641 > my_blocks2.txt
python3 combine2.py my_blocks2.txt 125000000   # compare with logs/msieve2_out_combine.txt
./msieve2 scan 330000000001 330125000000 -257128 262144   # expect: first k=330055906058 M=-262144

# Spot checker (sympy trial factorisation of random 1000-wide windows against run 1)
MSIEVE=./msieve python3 check_windows.py      # expect ALL_AGREE (logs/check_windows_out.txt)
```

- Block line format: "b sum maxprefix minprefix", prefixes relative to the block start; lines may be out of order
  (OpenMP). Run 1 counts the empty prefix 0 in max/min; the checker in verify-it-yourself/ normalises for that.
- The combiners print the scan arguments (M before the first block reaching 2^n) and check the anchors
  M(10^8..10^11) against OEIS A084237 and a(14..17) against OEIS A084235.
- logs/grid_compare.txt: run 1 and run 2 cumulative M agree at all 660 common grid points (multiples of 5e8) up to
  3.3e11; M(3.3e11) = -257128 in both.
- PREREG.md is the run's frozen pre-registration (null test not needed: deterministic exact value).
- verify-it-yourself/certificate_blocks.txt is logs/msieve_out_blocks.txt sorted by block index.
