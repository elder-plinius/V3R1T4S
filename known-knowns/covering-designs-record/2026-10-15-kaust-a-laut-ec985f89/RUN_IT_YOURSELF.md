# Run it yourself

## Verify the object (Python 3, standard library only)
From this folder:

    sh verify-it-yourself/run_checks.sh

Expected output (the same as verify-it-yourself/RECEIPTS.md):

    sha256 ec985f89dd793006ccf15346b6937419e1ce4e922034d73b18e769fb958778aa matches
    blocks 2207 expected 2207 distinct 2207
    t-subsets 749398 uncovered 0
    Schonheim bound 1070 blocks >= bound True
    PASS

Without sh: `python verify-it-yourself/check_covering.py 41 12 5 object/C41_12_5_2207blocks.txt 2207 ec985f89dd793006ccf15346b6937419e1ce4e922034d73b18e769fb958778aa`.

## Rebuild the object
In any (v,k,t) covering design, the blocks containing a fixed point p, with p deleted and the remaining points
relabelled to 1..v-1, form a (v-1,k-1,t-1) covering design of size deg(p).

1. Extract the 8735-block `C(42,13,6)` design from the LJCR Zenodo v1.2 `covers.json` file (record 19735294,
   https://doi.org/10.5281/zenodo.19735294) as one block per line (`zenodo_C42_13_6.txt`).
2. Run `how-we-built-it/derive_at_point.py`:

       python -I how-we-built-it/derive_at_point.py zenodo_C42_13_6.txt 42 C41_12_5_derived.txt

   It finds that point `16` has minimum degree `2207` (degree range `2207..3091`, average `2703.7`) and writes the
   2207 derived blocks to `C41_12_5_derived.txt`, matching `object/C41_12_5_2207blocks.txt` (`sha256 ec985f89dd793006ccf15346b6937419e1ce4e922034d73b18e769fb958778aa`) byte for byte.
