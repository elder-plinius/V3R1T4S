# How the value was computed (commands, run from how-we-built-it/)

Needs gcc with OpenMP and python3 (standard library). Program B at n = 25 needs about 1 GiB of RAM. Under 2 minutes on 8 cores.

```sh
W=$(mktemp -d)
gcc -O3 -march=native -fopenmp -o "$W/tsA" code/tsasm_rowmajor.c
for p in 4611686018427387847 4611686018427387817 4611686018427387787 4611686018427387761; do "$W/tsA" $p 0 26 > "$W/A_p$p.txt"; done
python3 code/crt.py "$W"/A_p*.txt > "$W/A_crt.txt"     # CRT on 3 primes, the 4th is a check; marks OEIS matches

gcc -O3 -march=native -fopenmp -o "$W/tsB" code/tsasm_colmajor.c
gcc -O3 -march=native -fopenmp -DSTORE64 -o "$W/tsB64" code/tsasm_colmajor.c
"$W/tsB" exact 0 25 > "$W/B_wrap128.txt"                # exact modulo 2^128 (additions only)
for p in 2305843009213693951 2305843009213693921 2305843009213693907 2305843009213693723; do "$W/tsB64" $p 0 26 > "$W/B_p$p.txt"; done
python3 code/crt.py "$W"/B_p*.txt > "$W/B_crt.txt"
python3 code/compare.py "$W/A_crt.txt" "$W/B_crt.txt" "$W/B_wrap128.txt"   # expect ALL_AGREE over n=0..26

python3 code/tsasm_check.py 7     # brute force from the definition: fixtures, then a(0..7)
python3 code/primes.py            # prints the prime sets (deterministic Miller-Rabin)
```

- Program A (code/tsasm_rowmajor.c): a row-major transfer matrix on the reduced quadrant (a symmetric n x n
  {-1,0,1} matrix with row prefix sums in {0,1}), counting modulo P_A (4 primes below 2^62).
- Program B (code/tsasm_colmajor.c): a column-major sweep with a different state encoding, counting modulo P_B
  (4 primes below 2^61) and exactly modulo 2^128. a(25) < 2^115, so the mod-2^128 value is a(25) itself.
- result/a005164_0_26.txt and result/residues.txt are the outputs of the run (a(26) is a by-product, not claimed).
- PREREG.md is the run's pre-registration (frozen 2026-11-01T02:09:55Z). No null test was required (exact count; see
  its null_test line).
