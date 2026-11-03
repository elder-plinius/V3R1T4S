# Run it yourself

## Verify the object (Python 3, standard library only)
From this folder:

    sh verify-it-yourself/run_checks.sh

Expected output (the same as verify-it-yourself/RECEIPTS.md):

    sha256 d111b0feb0cd74f5af84f8bbf660d65979caca2eb05885191dbd3fb63c14ea53 matches
    blocks 76 expected 76 distinct 76
    t-subsets 98770 uncovered 0
    Schonheim bound 54 blocks >= bound True
    PASS

Without sh: `python verify-it-yourself/check_covering.py 85 24 3 object/C85_24_3_76blocks.txt 76 d111b0feb0cd74f5af84f8bbf660d65979caca2eb05885191dbd3fb63c14ea53`.

## Rebuild the object
how-we-built-it/covsearch3.c is the search. Build it with any C99 compiler, for example

    python -m pip install ziglang
    python -m ziglang cc -O2 -o covsearch3 how-we-built-it/covsearch3.c

then run it cold (random start) at 76 blocks with seed 11, tenure 10, maxw 1000000, pnoise 0.2, maxcand 0:

    ./covsearch3 85 24 3 76 1500 11 found.txt - 10 1000000 0.2 0

`covsearch3` is deterministic in steps and finishes at step `701893` (~302 s on a single core), writing a file whose
sha256 (`d111b0feb0cd74f5af84f8bbf660d65979caca2eb05885191dbd3fb63c14ea53`) matches `object/C85_24_3_76blocks.txt` byte for byte (`how-we-built-it/C85_24_3_b76_s11_pn0.2.log`).
