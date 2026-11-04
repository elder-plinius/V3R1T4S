# Run it yourself

All commands run from this folder in a fresh shell. Needed: python3 (3.8 or later, standard library), sh, xz, tar
with xz support, and curl for the automatic download.

## 1. Get the certificates

The five files are over 1 MB each, so they live on Zenodo; names, sizes, sha256 and URLs are in
`object/CERTIFICATES.md` (`archive_url` for orders 18 to 20, `n21_url` and `n22_url`). Either let `run_checks.sh`
fetch them (step 2), or by hand:

    mkdir -p certificates
    curl -fL -o certificates/archive.tar.xz "$(sed -n 's/^archive_url: *//p' object/CERTIFICATES.md)"
    tar -xJf certificates/archive.tar.xz -C certificates
    for n in 21 22; do curl -fL -o certificates/cert_n$n.txt.xz "$(sed -n "s/^n${n}_url: *//p" object/CERTIFICATES.md)"; done
    python3 verify-it-yourself/sha256check.py object/certificates.sha256 certificates

## 2. Check

    sh verify-it-yourself/run_checks.sh

Expected output (one real run is in `verify-it-yourself/RECEIPTS.md`): the hash checks, then for each n in 18..22 one
`-> PASS` line from each checker, and last line `PASS`. To use certificates kept elsewhere:
`CERT_DIR=/path/to/dir sh verify-it-yourself/run_checks.sh`.

- `indep_check.py CERT n --regen`: each line is a tree (union-find), labels are exactly {1..n}, the n-1 edge sums
  are distinct and span n-2; trees are keyed by a canonical level sequence (centre found by double BFS, bicentral
  trees rooted on the central edge, exact keys); A000055(n) is computed from Otter's formula; then every free tree on
  n vertices is regenerated (Wright-Richmond-Odlyzko-McKay 1986) and matched to exactly one line (missing = extra = 0).
- `verify_sem_coverage.py`: the run's pre-registered statistic. AHU canonical codes rooted at the centre, pairwise
  distinct, as many as A000055(n) from the OEIS b-file, each labeling checked by `check_sem.py`.

## 3. Rebuild the object (optional)

See `how-we-built-it/README.md`. The searches are randomised, so a rebuild gives different, equally valid
labelings, which the same checkers accept; the hashes then differ.
