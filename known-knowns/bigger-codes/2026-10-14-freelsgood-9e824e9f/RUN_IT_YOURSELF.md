# Reproduce the certificate

Requires Python 3.10 or newer and a POSIX shell. No external Python packages or network access are needed for the certificate checks. Run from this package directory:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. This checks every unordered pair, reconstructs the certificate twice and compares exact bytes, checks its published hash, and verifies the hex encoding. The independent all-pairs review took about 13 seconds in the review environment; laptop time varies.

An alternative exhaustive check uses all eight-element support subsets:

```sh
python3 -I -B verify-it-yourself/check_subsets.py object/A27_6_10_13026.txt
```

Export the deterministic reconstruction to a separate file:

```sh
python3 -I -B how-we-built-it/export_code.py rebuilt.txt
cmp rebuilt.txt object/A27_6_10_13026.txt
rm rebuilt.txt
```

`cmp` exits zero for exact byte equality. The wrapper never overwrites the submitted witness.

Check all packaged bytes:

```sh
sha256sum -c SHA256SUMS
```

The original search source is supplied for provenance. To reconstruct its decimal seed and compile it, if separately desired:

```sh
python3 -I -B how-we-built-it/export_code.py --seed seed_27_6_10.txt
g++ -O3 -std=c++17 how-we-built-it/find_orbits_and_polish.cpp -o find_orbits_and_polish
```

The historical C++ search is not needed for verification and was not rerun in this review. It includes a wall-clock-dependent search phase; its narrative is unverified. Do not interpret these commands as a receipt of its execution.

The panel reports are unchanged records with paths relative to their original claim workspace. Their checker scripts and receipts are included in verify-it-yourself/ under the names documented above. Current commands in this file are the package-relative replay interface.
