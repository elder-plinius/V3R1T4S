# Run it yourself

All commands from THIS folder, fresh shell, Python 3 standard library only.

## Verify the object (seconds)

```sh
sh verify-it-yourself/run_checks.sh      # expected last line: PASS
python3 verify-it-yourself/checker.py    # same checks, verbose
```

The checker verifies: both CRT residue sets (28 residues over 28 distinct primes 1 mod 15, disjoint
between the two runs) reconstruct object/a15.txt exactly; each modulus exceeds the rigorous bound
2^15 * 1220^15 (||T||_inf = 1220 is the exact max row sum of the transfer matrix); both programs'
ladder evidence (how-we-built-it/ladder.json, ladder2.json) matches every published term a(1)..a(14);
the growth/finiteness consistency facts. The corruption self-test inside run_checks.sh flips one digit
of the object and expects FAIL.

## Rebuild the object from scratch (~30 min, numpy required)

```sh
python3 how-we-built-it/iso_row.py --mode ladder      # run-1 code reproduces a(1)..a(14), ~4 min
python3 how-we-built-it/iso_ht.py  --mode ladder      # run-2 code reproduces a(1)..a(14), ~1 min
python3 how-we-built-it/iso_row.py --mode n15         # run-1: 14 residues + CRT, ~5 min
python3 how-we-built-it/iso_ht.py  --mode n15 --exclude-primes 32611,32491,32401,32371,32341,32251,32191,31981,31891,31771,31741,31531,31321,31231
                                                      # run-2: disjoint primes, ~20 min
python3 how-we-built-it/growth_check.py               # growth analysis (needs both result JSONs)
```

Expected: both n15 modes reconstruct 4310182149988584261406143524214457416387448. The ladder modes
read the published terms from the run's data file (path ../../data/A054759_b054759.txt.raw relative
to the program file; alternatively point the program at any copy of the OEIS b-file); the n15 mode
needs only the prime lists. Primes are chosen largest-first (P = 1 mod 15, P < 2^15 for float64-exact
arithmetic; the code asserts every intermediate stays below 2^53).

## Skeptic spot-check (the bank's verification method, ~1-4 min)

```sh
python3 how-we-built-it/iso_row.py --mode prime --prime P    # fresh prime P = 1 (mod 15), P < 2^15
python3 how-we-built-it/iso_ht.py  --mode prime --prime P
```

Both print the same residue; compare with a15.txt mod P. (Several such residues, CRT-combined, cover
any larger modulus.)
