# Run it yourself

All commands run from this package folder in a fresh shell.

## Check the certificate

```sh
sh verify-it-yourself/run_checks.sh
```

Needs python3 3.9 or later, standard library only. **It needs about 6.5 GB of memory (measured peak 6,451,609,600 bytes) and about 40 seconds**; a machine with less than about 8 GB free may fail.

Expected output (times differ from run to run):

```
sha256 of 5 parts and of the concatenation (4496070 bytes) verified
m=22: 96909 orbits, ...
m=24: 352698 orbits, ...
ENCLOSURE  0.6627989728337138109756 <= h2 <= 0.6627989728337490653104   (width 3.525433E-14)
common decimals of the two bounds: 13  -> h2 = 0.6627989728337...  certified
CERTIFIED: 0.6627989728337 < h2 < 0.6627989728338  (13 decimals)
PASS
```

`run_checks.sh` copies the checker, `object/MANIFEST.txt` and the five certificate parts into a temporary folder, runs `python3 -I check_p1.py` there, deletes the folder and prints `PASS` or `FAIL` last. A real run is recorded in `verify-it-yourself/RECEIPTS.md`.

## What the checker does

1. Verifies the sha256 of the five parts and of their concatenation against `object/MANIFEST.txt`.
2. Rebuilds the transfer matrix from its definition for widths 3 to 8 and compares it with the fast sweep used for the large widths.
3. For widths 22 and 24: enumerates the dihedral orbits, expands the stored vector, computes y = P x in exact integers, checks that every entry of x is positive, and takes the exact minimum and maximum of y_i / x_i (Collatz-Wielandt).
4. Computes the two bounds with outward-rounded 70-digit decimal arithmetic and asserts that the enclosure lies strictly between 0.6627989728337 and 0.6627989728338.

The proofs of the two inequalities are in `object/PROOF.md`.

## Rebuild the object (optional, not needed to check it)

`how-we-built-it/make_cert.py` is the producer. It needs the contributor's C tools built from `how-we-built-it/mdtm.c` (see `how-we-built-it/README.md`), about 12 threads and tens of gigabytes of memory for width 24. The checker does not use any of it.
