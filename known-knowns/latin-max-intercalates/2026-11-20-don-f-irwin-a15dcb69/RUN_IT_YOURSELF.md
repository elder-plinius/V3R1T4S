# Run it yourself

From this folder, in a fresh shell:

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS`.

Full expected output:

    order: 28
    latin: True
    intercalates (2x2-block method): 3324
    intercalates (permutation-cycle method): 3324
    bar: 2940 | proven bound: 5292
    PASS

## Rebuild the object from its published factors

The object is the direct product of the unique order-2 Latin square with the order-14 Latin square published in
A092237's proving list (a092237_2.txt, header `n=14, a(14)>=391`). To rebuild it:

    python3 how-we-built-it/rebuild_object.py

That writes a rebuilt square and checks it equals object/square_n28_3324.txt exactly.
