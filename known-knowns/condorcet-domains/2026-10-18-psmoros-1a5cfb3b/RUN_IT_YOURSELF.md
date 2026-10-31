# Run it yourself

From this package folder, in a fresh shell (cc, python3 with its standard library, xz or python3's lzma):

    sh verify-it-yourself/run_checks.sh

Expected output (verify-it-yourself/RECEIPTS.md holds the real one):

    joined xz sha256 1a5cfb3b80fe8600bee47668e068a0fcf8923f87f895da9e23a1efe07f02b75d
    n 21 lines 7467760 malformed 0 distinct 7467760 duplicates 0 triples 1330 violations 0
    assignment lines 1330 bad_or_missing 0 orders_disobeying 0
    size 7467760, required more than 6674931
    PASS

The same by hand:

    cat object/n21_orders.txt.xz.part_aa object/n21_orders.txt.xz.part_ab object/n21_orders.txt.xz.part_ac > n21.xz
    xz -dc n21.xz | shasum -a 256          # 0cb0dd880cc7a0ad640634f505b7520bd2a5c0bb95fd7a2ce4d56fbeb8578e27
    xz -dc n21.xz | wc -l                  # 7467760
    xz -dc n21.xz | LC_ALL=C sort -u | wc -l   # 7467760

What the checker tests, from the definition (arXiv:2601.07336v1, Section 2, after Sen): every line must be a linear order of 1..21, all lines distinct, and for every one of the C(21,3) = 1330 triples some alternative of the triple must be never first, never second or never last within the triple over all orders.

## Rebuild the object (optional; hours of CPU)

how-we-built-it/ holds the search code and the lenses' exact commands (BUILD.md):
- code/lsearch_wave1.c: the exact subset-DP counter, the enumerator and pair-LNS.
- code/lsx.c: adds restriction, extension and sequenced LNS.
- code/multistart.py, topdown.py, dchain.py and vcycle.py: the drivers.

The final assignment came from this sequence:
1. A chain of the record paper's one-alternative extension step, from rebuilt record domains (n = 17).
2. Pair-LNS polish (all triples through a pair of alternatives re-optimised exactly by branch and bound).
3. Restriction of a polished n = 22 domain to 21 alternatives (deleting alternative 11, 0-based), then one more pair-LNS pass.

The list is the lexicographic enumeration of all orders that obey object/n21_assignment.txt:

    cc -O3 -o lsx how-we-built-it/code/lsx.c -lm
    # convert object/n21_assignment.txt to the .npy encoding with how-we-built-it/code/txt2npy.py (needs numpy), then
    ./lsx enum 21 n21_assignment.npy | xz -9e > n21_orders.txt.xz

A time-limited search may end at a different local optimum on another machine; the object itself is fixed by its sha256.
