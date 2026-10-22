# Run it yourself

In a fresh shell, from this package folder:

```sh
sh verify-it-yourself/run_checks.sh
```

Requirements: python3 3.8 or later, standard library only for the 11 Python entries; a C compiler (cc, libc and pthreads only) for the (5,5) entry at p = 2. Without a C compiler only the 11 Python entries are checked and the script says so. CW_QUICK=1 skips the slowest entry, (5,4).

Time: about 14 minutes (13 min 36 s measured by the contributor on a loaded 28-core Mac; the Python entries alone took about 8 minutes when the machine was unloaded, (5,4) being about 7.5 minutes of that; the C check of the (5,5) entry takes about 75 seconds).

Expected last line: `ALL CHECKS PASS`. Real output of an earlier run is in verify-it-yourself/RECEIPTS.md.

`CW_QUICK=1 sh verify-it-yourself/run_checks.sh` skips the slowest entry, (5,4).

## Rebuilding the object

The object was produced by the contributor's C programs in how-we-built-it/. No command lines were recorded in the snapshot (see how-we-built-it/README.md). The derivation of why the ratio bounds the constant is in object/DERIVATION.md (and object/RESULTS.md holds the author's notes).
