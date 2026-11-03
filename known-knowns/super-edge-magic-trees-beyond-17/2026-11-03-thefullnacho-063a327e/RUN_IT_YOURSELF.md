# Run it yourself

All commands run from this folder in a fresh shell. Only python3 (3.8 or later, standard library), sh, tar with xz
support and, for the automatic download, curl are needed.

## 1. Get the certificates

The three certificate files are over 1 MB each, so they live in one archive outside this folder. Its name, size,
sha256 and public URL are in `object/CERTIFICATES.md` (lines `archive_name`, `archive_bytes`, `archive_sha256`,
`archive_url`); the archive is on Zenodo, DOI 10.5281/zenodo.23918679. Either let `run_checks.sh` fetch it (step 2), or by hand:

    mkdir -p certificates
    curl -fL -o certificates/archive.tar.xz "$(sed -n 's/^archive_url: *//p' object/CERTIFICATES.md)"
    python3 -c "import hashlib; print(hashlib.sha256(open('certificates/archive.tar.xz','rb').read()).hexdigest())"
    # must print 390d1698ff6e9563ed2e41a645cff865a05ab6b5427ece910e5bdda6ed82cc8b
    tar -xJf certificates/archive.tar.xz -C certificates

## 2. Check

    sh verify-it-yourself/run_checks.sh

Expected output (the full text of one real run is in `verify-it-yourself/RECEIPTS.md`): five sections, every
`-> PASS`, the line `OVERALL: PASS`, and last line `PASS`. It checks, in order: the object/ files against
SHA256SUMS; the five hardest labelings; the certificate hashes; for each n, that every line is a tree on n vertices
with a valid labeling, that the trees are pairwise non-isomorphic and that there are A000055(n) of them; and,
independently, that regenerating every tree on n vertices from K2 gives exactly the certificate's trees.

To use certificates kept elsewhere: `CERT_DIR=/path/to/dir sh verify-it-yourself/run_checks.sh`.

## 3. Rebuild the object (optional)

See `how-we-built-it/README.md`. The searches are randomised, so a rebuild gives different, equally valid
labelings, which the same checker accepts; the hashes in `object/` then differ.

## 4. Cross-check against nauty gentreeg (optional)

The package checkers do not call gentreeg (gap G2 in `panel/criterion.md`). The CRITERION panelist closed that gap
with its own code: `panel/criterion-work/gentreeg_xcheck.py` reads `gentreeg -p n` parent arrays (nauty 2.8.9) and
the three certificate files, and matches the trees one-to-one by canonical form. Its output,
`panel/criterion-work/gentreeg_xcheck_output.txt`, shows for n = 18, 19, 20: gentreeg = A000055 = certificate lines
(123867, 317955, 823065), bad=0, dup=0, missing=0, extra=0. To repeat it, build gentreeg from the nauty source
and run `python3 panel/criterion-work/gentreeg_xcheck.py /path/to/gentreeg certificates`.
