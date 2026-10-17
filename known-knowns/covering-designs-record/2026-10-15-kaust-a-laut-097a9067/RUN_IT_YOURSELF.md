# Run it yourself

## Verify the object (Python 3, standard library only)
From this folder:

    sh verify-it-yourself/run_checks.sh

Expected output (the same as verify-it-yourself/RECEIPTS.md):

    sha256 097a9067d0628e1d3ba01f6230bafbcab3573b78f4d0c9913b8759676e00a18e matches
    blocks 27 expected 27 distinct 27
    t-subsets 35990 uncovered 0
    Schonheim bound 20 blocks >= bound True
    PASS

Without sh: `python verify-it-yourself/check_covering.py 61 25 3 object/C61_25_3_27blocks.txt 27 097a9067d0628e1d3ba01f6230bafbcab3573b78f4d0c9913b8759676e00a18e`.

## Rebuild the object
how-we-built-it/covsearch3.c is the search. Build it with any C99 compiler, for example

    python -m pip install ziglang
    python -m ziglang cc -O2 -o covsearch3 how-we-built-it/covsearch3.c

then run it cold (random start) at 27 blocks with seed 1, tenure 10, maxw 1000000, maxcand 0:

    ./covsearch3 61 25 3 27 900 1 found.txt - 10 1000000 PNOISE 0

With `PNOISE = 0.2`, `covsearch3` is deterministic in steps and finishes at step `487885` (~193 s on a single core), writing a file whose sha256 (`097a9067d0628e1d3ba01f6230bafbcab3573b78f4d0c9913b8759676e00a18e`) matches `object/C61_25_3_27blocks.txt` byte for byte (verified in `runs/2026-10-15-2309/attempts/evaluator-first/rebuild_C61/` and `package_code/rebuild/fresh_build_run.log`).

The object is the 1-based block file the program writes when it prints "FOUND covering with 27 blocks". Other seeds
and pnoise values also find 27-block designs (different ones); any of them can be checked with the checker above.
