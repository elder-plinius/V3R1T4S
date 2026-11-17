# Run it yourself

All commands run from this folder in a fresh shell. python3 (3.8 or later, standard library), sh, and
optionally gcc (or another C11 compiler invoked as cc), tar with xz support, and curl are enough.

## 1. Check the bundled object (always)

Orders 10..15 and a mixed-order sample are in `object/`. From this folder:

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS`. The script compiles `verify-it-yourself/check_og.c` if cc is available,
runs self-tests, checks `object/` against SHA256SUMS, checks the sample, then checks each bundled
certificate (labels, tree property, pairwise non-isomorphism under the AHU form, count = A000055(n))
and regenerates every tree on 10..15 vertices in Python to match the files one-to-one.

To point the script at certificates kept elsewhere: `CERT_DIR=/path/to/dir sh verify-it-yourself/run_checks.sh`.

## 2. Get the full certificates (orders 16..23, optional)

The files cert_n16.txt through cert_n23.txt are over 1 MB each, so they live in one archive outside
this folder. Its name, size, sha256, public URL and DOI are in `object/CERTIFICATES.md`
(lines `archive_name`, `archive_bytes`, `archive_sha256`, `archive_url`, `archive_doi`).
Either let `run_checks.sh` fetch it from Zenodo, or by hand:

    mkdir -p certificates
    curl -fL -o certificates/archive.tar.xz "$(sed -n 's/^archive_url: *//p' object/CERTIFICATES.md)"
    python3 -c "import hashlib; print(hashlib.sha256(open('certificates/archive.tar.xz','rb').read()).hexdigest())"
    # must print f89ddd847de5ea066c05730800a17ac01f9ee694c346638d40d1b1b0dc526713
    tar -xJf certificates/archive.tar.xz -C certificates
    CERT_DIR=certificates sh verify-it-yourself/run_checks.sh

Alternatively, copy the fourteen plain-text files into `certificates/` (or set
CERT_DIR) and run the same command. Expected last line: `PASS`. With the C checker this is a few
minutes on one core; in Python only it would be much slower.

## 3. Rebuild the object (optional)

See `how-we-built-it/README.md`. The restart phase is randomised, so a rebuild gives different,
equally valid labelings, which the same checker accepts; the hashes in `object/` then differ.
