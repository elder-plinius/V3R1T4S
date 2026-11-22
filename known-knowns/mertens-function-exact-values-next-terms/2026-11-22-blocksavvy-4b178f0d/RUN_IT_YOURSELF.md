# Run it yourself

Fresh shell, from this package folder. Needs python3 (standard library) and a C compiler (cc, gcc or clang;
OpenMP is used if available).

```sh
sh verify-it-yourself/run_checks.sh            # quick tier, about 40 s; last line: PASS
FULL=1 sh verify-it-yourself/run_checks.sh     # full tier from k = 1, about 2 CPU-hours (about 20 min on 6 cores); last line: PASS
```

What the quick tier does (expected output in verify-it-yourself/RECEIPTS.md):
1. Compiles verify-it-yourself/mu_check.c (a residual-division Mobius sieve written from the definition, separate
   from the contributor's two sieves) and checks it against Python trial division on mu(1..20000) and on the 200
   integers ending at k = 330055906058.
2. Reproduces a(0..9) with a pure-Python sieve.
3. Chains verify-it-yourself/certificate_blocks.txt (block sums of 1e8-wide blocks from k = 1, with max/min prefix)
   to M(10^8), M(10^9), M(10^10), M(10^11) (OEIS A084237) and finds the first block reaching |M| = 2^n for n = 14..18.
4. Recomputes 22 blocks from the definition (12 of them chosen at random each time) and compares them with the
   certificate exactly, then scans the first-hit blocks exactly: a(14..17) as published, and a(18) = 330055906058
   with M = -262144 as in object/a18.txt.

The full tier recomputes all 3301 blocks covering k = 1 .. 330100000000 and rebuilds the chain without the
certificate, so "least" is checked completely.

To rebuild the object with the contributor's own code, see how-we-built-it/COMMANDS.md.
