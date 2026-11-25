# Reproduce from a fresh shell

All paths relative to this package folder. Needs python3 (3.8+, stdlib only) and a C compiler (`cc`) to build drat-trim.

## Fastest path (recommended)

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. This independently re-derives the grid-line enumeration from the bare definition (not from the claimant's code), checks the shipped CNF matches that encoding clause-for-clause, and re-verifies the shipped DRAT proof.

## Rebuilding the object from scratch

```sh
python3 how-we-built-it/make_cnf.py          # writes how-we-built-it/ceiling98.cnf (343 vars, 17456 clauses)
cadical how-we-built-it/ceiling98.cnf myproof.drat ; echo $?  # expect exit code 20 (UNSAT); any DRAT-producing solver works
cc -O2 -o drat-trim verify-it-yourself/drat-trim.c
./drat-trim how-we-built-it/ceiling98.cnf myproof.drat  # expect final line "s VERIFIED"
```

The rebuilt CNF should match `object/ceiling98.cnf` clause-for-clause (write it to a scratch directory and diff there) (the independent panel reviewer confirmed this with their own, separately-written encoder too — see `panel/reproduce.md`).

## If a solver disagrees (reports SAT)

Extract the witness and check it directly against the definition: every grid line of 3+ points must contain at most 2 witness points, AND every axis-parallel line must contain exactly 2 (the counting identity in `README.md` / `how-we-built-it/PREREG.md` forces this for any 98-point set). If such a witness exists, this claim is refuted and a(7) = 98.

## The counting step (check by hand)

Any 98-point admissible set in the 7-cube: each of its points lies on exactly 3 axis-parallel lines (147 total), so summing incidences over axis lines gives 3*98 = 294 = 2*147. Since no axis line may hold more than 2 selected points (no-three-collinear), equality forces exactly 2 on every one of the 147 axis-parallel lines. That is exactly the "ceiling model" solved above; its UNSAT result rules out all 98-point admissible sets.
