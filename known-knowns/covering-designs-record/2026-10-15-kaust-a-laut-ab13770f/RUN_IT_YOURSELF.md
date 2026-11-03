# Run it yourself

## Verify the object (Python 3, standard library only)
From this folder:

    sh verify-it-yourself/run_checks.sh

Expected output (the same as verify-it-yourself/RECEIPTS.md):

    sha256 ab13770f500eb1e64f71e63b1cd61f98500ddb58e0f22f985cef400861950a5e matches
    blocks 34 expected 34 distinct 34
    t-subsets 23426 uncovered 0
    Schonheim bound 24 blocks >= bound True
    PASS

Without sh: `python verify-it-yourself/check_covering.py 53 20 3 object/C53_20_3_34blocks.txt 34 ab13770f500eb1e64f71e63b1cd61f98500ddb58e0f22f985cef400861950a5e`.

## Rebuild the object
how-we-built-it/covsearch3.c is the search. Build it with any C99 compiler, for example

    python -m pip install ziglang
    python -m ziglang cc -O2 -o covsearch3 how-we-built-it/covsearch3.c

then run it cold (random start) at 34 blocks with seed 1, tenure 10, maxw 1000000, pnoise 0.25, maxcand 0:

    ./covsearch3 53 20 3 34 180 1 found.txt - 10 1000000 0.25 0

`covsearch3` is deterministic in steps and finishes at step `142760` (~33.3 s on a single core), writing a file whose
sha256 (`ab13770f500eb1e64f71e63b1cd61f98500ddb58e0f22f985cef400861950a5e`) matches `object/C53_20_3_34blocks.txt` byte for byte (`how-we-built-it/search_b34.log`).
