# Run it yourself

In a fresh shell, from this package folder:

```sh
sh verify-it-yourself/run_checks.sh
```

Requirements: python3 3.8 or later (standard library only) and a C compiler named cc (the program verify-it-yourself/mdlayer.c applies the full matrix and is compiled by the checker). No network. About 1 GB of memory.

Time: about 20 seconds on a laptop, so no special timeout is needed.

Expected last line: `ALL CHECKS PASS`. Real output of an earlier run is in verify-it-yourself/RECEIPTS.md.

What it does, in order: first it checks that every file in object/ matches SHA256SUMS; then it reproduces the earlier (3,3) claim exactly (ratio 731051554747087/618837374495, 0.7860441) as a known-answer test; then it reassembles the (5,4) certificate from its two parts (checking the sha256 of each part and of the whole), applies the full 1048576 x 1048576 monomer-dimer matrix to the vector expanded from the 52488 orbit values, takes max (T x)_U / x_U over every state by exact cross multiplication (expected 1891821269973664/281869529) and rounds the logarithm divided by 20 up to seven decimals (expected 0.7859681).

## Rebuilding the object

The object was produced by the contributor's C program cubic_md_h3.c in how-we-built-it/ (its main function calls solve_md(5, 4, 50, ...) for this certificate). No command lines were recorded in the snapshot (see how-we-built-it/README.md). The derivation of why the ratio bounds the constant is in object/DERIVATION.md.
