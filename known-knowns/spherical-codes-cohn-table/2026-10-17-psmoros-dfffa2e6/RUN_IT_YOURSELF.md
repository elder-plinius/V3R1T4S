# Run it yourself

## Verify (fresh shell, from this folder)

    shasum -a 256 -c SHA256SUMS            # or: sha256sum -c SHA256SUMS
    sh verify-it-yourself/run_checks.sh

Expected output of the second command (verify-it-yourself/RECEIPTS.md has the real one):

    object object/d6_N526.txt sha256 dfffa2e676f24cbecc11657a119d33fd2169f06963446dbde15c10e6455c8eb8
    points 526 dimension 6 minimum significant digits 26
    pairs checked 138075
    c* = 0.786427532330074152872057367155 at points (202, 395)
    table cosine 0.786636400242 (https://spherical-codes.org/plain, fetched 2026-10-16T05:12:04Z)
    gain = table - c* = 0.00020886791192584713
    PASS

The live table now lists this code (our c* rounded up at the 12th decimal: 0.786427532331), so a comparison with
the live value cannot pass the 1e-10 margin by design; the claim compares with the pre-upload value recorded in
the-record-we-beat/ (see README).

## Rebuild the object (how it was found)

how-we-built-it/code/ holds the search code (Python 3 with numpy and scipy; C files compiled with
`cc -O3 -shared -fPIC -o liblse2.so lse2.c -framework Accelerate` on macOS, or against a BLAS elsewhere; paths that
pointed into the original workspace are written WORKDIR, see code_hashes.json). The object came from the posted
(6,527) code of the table (https://spherical-codes.org/data/6/527) with one point deleted and the remaining 526 points
polished: LogSumExp smooth-max surrogate with L-BFGS at increasing sharpness (lse2.c), then a penalty-threshold polish
(lse3.c, bsprec.py), driven by h3sweep.py; exact commands in how-we-built-it/LENS_REPRODUCE.md. Then, in run 2026-10-16-0758, that code was re-polished in place
(how-we-built-it/repolish-run0758/: repolish_rows.py driving lse3.c/lse4.c and the sequential-LP polish nm_slp.py;
PREREG in how-we-built-it/PREREG_run0758.md), giving this object. The search is
randomised; a rerun gives a code of similar quality, not this file byte for byte.
