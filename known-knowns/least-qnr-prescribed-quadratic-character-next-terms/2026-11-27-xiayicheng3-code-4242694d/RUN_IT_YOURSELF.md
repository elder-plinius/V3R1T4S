# Run it yourself

From this folder, in a fresh shell (needs python3 and gcc or clang; OpenMP optional):

```sh
python3 verify-it-yourself/check.py object object/a002224_42.json
sh verify-it-yourself/run_checks.sh
```

Expected output of the first command (last line `OK`):
```
object: q = 6072205049848081, q mod 8 = 1, first 44 primes are QRs (needs 42), least QNR 197, Lucas certificate valid, Miller-Rabin agrees
OK
```
Expected last line of the second: `PASS` (see verify-it-yourself/RECEIPTS.md for a full real run).

What run_checks.sh does: (1) checks the value's property and primality certificate; (2) compiles
verify-it-yourself/enum.c and enumerates every q = 1 (mod 8) in [1, 6072205049848081] whose residue modulo each odd
prime <= 113 is a nonzero square (for a prime q = 1 mod 8 this is equivalent, by quadratic reciprocity, to those
primes being QRs mod q, so no candidate prime is skipped), keeping those with 2^(q-1) = 1 mod q; (3) re-tests every
survivor in Python (deterministic Miller-Rabin, Euler's criterion), checks that the least primes for n = 30..41 are
the OEIS b-file values, and that the least for n = 42 is the claimed value.

Rebuilding the object: see how-we-built-it/README.md (two independent enumerators over [1, 10^16]).
