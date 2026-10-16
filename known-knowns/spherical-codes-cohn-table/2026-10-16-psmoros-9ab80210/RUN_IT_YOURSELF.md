# Run it yourself

## Verify (fresh shell, from this folder)

    shasum -a 256 -c SHA256SUMS            # or: sha256sum -c SHA256SUMS
    sh verify-it-yourself/run_checks.sh

Expected output of the second command (verify-it-yourself/RECEIPTS.md has the real one):

    object object/d6_N526.txt sha256 9ab8021055cf16bc37eafb5ff62c65ce9a9660c1c907fca8e202f9def2d5b83a
    points 526 dimension 6 minimum significant digits 26
    pairs checked 138075
    c* = 0.786430618544579725385299139732 at points (168, 416)
    table cosine 0.786636400242 (https://spherical-codes.org/plain, fetched 2026-10-16T05:12:04Z)
    gain = table - c* = 0.00020578169742027461
    PASS

To compare with the live table: download https://spherical-codes.org/plain once, find the line starting "6,526,",
put its cosine into the-record-we-beat/cell.json ("table_cosine"), and rerun; check the (6,526) row of
https://spherical-codes.org/ for a star or the text "needs more optimization".

## Rebuild the object (how it was found)

how-we-built-it/code/ holds the search code (Python 3 with numpy and scipy; C files compiled with
`cc -O3 -shared -fPIC -o liblse2.so lse2.c -framework Accelerate` on macOS, or against a BLAS elsewhere; paths that
pointed into the original workspace are written WORKDIR, see code_hashes.json). The object came from the posted
(6,527) code of the table (https://spherical-codes.org/data/6/527) with one point deleted and the remaining 526 points
polished: LogSumExp smooth-max surrogate with L-BFGS at increasing sharpness (lse2.c), then a penalty-threshold polish
(lse3.c, bsprec.py), driven by h3sweep.py; exact commands in how-we-built-it/LENS_REPRODUCE.md. The search is
randomised; a rerun gives a code of similar quality, not this file byte for byte.
