# How the certificates were built

Exact commands, from this folder, in a shell that has python3, networkx, gcc, and a C11 compiler
invoked as cc. The searches are randomised in the restart phase, so a rebuild gives different,
equally valid labelings.

## Checker calibration

    python3 code/checker/test_checker.py

Must pass before any search result is trusted. The labeling predicate is in
`code/checker/check_odd_graceful.py`. Coverage (count, distinct AHU forms, A000055) is
`code/checker/verify_count_distinct.py`. The package's own standalone checker, written from the
definition and used to confirm the object, is `verify-it-yourself/check_og.c` and
`verify-it-yourself/check_og.py`, not these files.

## Orders 10..22

    cd code/small-data-direct
    cc -O2 -o og_direct og_direct.c
    cc -O2 -o og_restart og_restart.c
    sh run_hybrid_order.sh 10 1
    # ... similarly for each n in 11..22; use more shards (the second argument) as n grows

`dump_trees.py` writes every unlabeled tree on n vertices (networkx.nonisomorphic_trees).
`og_direct` tries a deterministic backtracker with a 1e5-node cap; `og_restart` retries the leftovers;
`merge_hybrid.py` writes `cert_nN.txt`. Pre-registration: `PREREG_n10_22.md`.

## Order 23

The same binaries, with the tree dump streamed into 1,000,000-tree chunks and five low-priority
workers. A sketch is in `code/n23-stream/stream_n23.sh`. Pre-registration: `PREREG_n23.md`.
The first pass left 208 trees unlabeled; the restart search labelled all 208. The resulting file
was gzip-compressed for storage; the Zenodo archive holds the plain-text `cert_n23.txt`.

Networkx is the only non-stdlib Python dependency, and only for rebuilding the object, not for
checking it.
