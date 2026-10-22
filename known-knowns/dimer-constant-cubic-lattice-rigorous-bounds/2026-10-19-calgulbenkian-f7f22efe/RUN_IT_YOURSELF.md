# Run it yourself

In a fresh shell, from this package folder:

```sh
sh verify-it-yourself/run_checks.sh
```

Requirements: python3 3.8 or later, standard library only. No network.

Time: about 6 minutes (about 5 minutes alone and 11 min 5 s on a loaded machine, as measured by the contributor; CW_QUICK=1 skips the all-sector iteration and takes about 40 seconds).

Expected last line: `ALL CHECKS PASS`. Real output of an earlier run is in verify-it-yourself/RECEIPTS.md.

`CW_QUICK=1 sh verify-it-yourself/run_checks.sh` skips the all-sector iteration (about 40 seconds). Note: the shipped object's header and the older output in RECEIPTS.md show the author's rounded-down 0.5840147693; the claim is 0.5840147694 (see README.md, section Not claimed).

## Rebuilding the object

The object was produced by the contributor's C programs in how-we-built-it/. No command lines were recorded in the snapshot (see how-we-built-it/README.md). The derivation of why the ratio bounds the constant is in object/DERIVATION.md.
