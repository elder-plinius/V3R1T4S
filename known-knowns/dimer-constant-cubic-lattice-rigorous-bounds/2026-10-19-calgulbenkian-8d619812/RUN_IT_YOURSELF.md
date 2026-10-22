# Run it yourself

In a fresh shell, from this package folder:

```sh
sh verify-it-yourself/run_checks.sh
```

Requirements: python3 3.8 or later, standard library only for the default sector-12 check; a C compiler (cc, libc and pthreads only) for the check of all 13 sectors. Without a C compiler only sector 12 is checked and the script says so.

Time: about 8 minutes (8 min 23 s measured by the contributor on a loaded 28-core Mac; about 2 minutes of the checker is the Python check of sector 12, the rest is the C check of all 13 sectors).

Expected last line: `ALL CHECKS PASS`. Real output of an earlier run is in verify-it-yourself/RECEIPTS.md.

The certificate vector for sector 12 is stored as three parts (a 1 MB file limit); the checker reassembles it as part1, part2, part3 and checks the sha256 of each part and of the whole (object/PARTS.sha256). To reassemble by hand: `cat object/cert_he_55_converged_sector12.txt.part1 object/cert_he_55_converged_sector12.txt.part2 object/cert_he_55_converged_sector12.txt.part3 > cert12.txt`.

To check all 13 sectors in Python without a C compiler: `CW_SMALL=1 sh verify-it-yourself/run_checks.sh` (slow, tens of minutes). `CW_PROCS=n` sets the number of Python worker processes.

## Rebuilding the object

The object was produced by the contributor's C programs in how-we-built-it/. No command lines were recorded in the snapshot (see how-we-built-it/README.md). The derivation of why the ratio bounds the constant is in object/DERIVATION.md.
