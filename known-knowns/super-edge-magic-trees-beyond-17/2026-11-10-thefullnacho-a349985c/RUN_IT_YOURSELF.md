# Run it yourself

All commands run from this folder in a fresh shell. Needed: python3 (3.8 or later, standard library), sh, xz, tar with
xz support, and curl for the automatic download.

## 1. Get the certificates

The eight files are on Zenodo; names, sizes, sha256 and URLs are in `object/CERTIFICATES.md` (`archive_url` for
orders 18 to 20, `n21_url` to `n25_url`). Either let `run_checks.sh` fetch them, or by hand:

    mkdir -p certificates
    curl -fL -o certificates/archive.tar.xz "$(sed -n 's/^archive_url: *//p' object/CERTIFICATES.md)"
    tar -xJf certificates/archive.tar.xz -C certificates
    for n in 21 22 23 24 25; do curl -fL -o certificates/cert_n$n.txt.xz "$(sed -n "s/^n${n}_url: *//p" object/CERTIFICATES.md)"; done
    python3 verify-it-yourself/sha256check.py object/certificates.sha256 certificates

## 2. Check

    sh verify-it-yourself/run_checks.sh                        # all of 18..25: about 3 h, about 12 GB at n = 25
    ORDERS="18 19 20 21 22" sh verify-it-yourself/run_checks.sh   # a laptop-sized subset, minutes

Expected: for each order, one `-> PASS` line from each checker, and last line `PASS` (one real run is in
`verify-it-yourself/RECEIPTS.md`). `CERT_DIR=/path` uses certificates kept elsewhere.

- `indep_check.py CERT n --regen`: each line is a tree (union-find), labels exactly {1..n}, n-1 distinct edge sums
  spanning n-2; canonical level sequences (centre by double BFS, bicentral trees rooted on the central edge, exact keys);
  A000055(n) from Otter's formula; then every free tree on n vertices is regenerated (Wright-Richmond-Odlyzko-McKay
  1986) and matched to exactly one line (missing = extra = 0).
- `verify_sem_coverage.py`: the run's pre-registered statistic: AHU canonical codes rooted at the centre, pairwise
  distinct, as many as A000055(n) from the OEIS b-file, each labeling checked by `check_sem.py`.

## 3. Rebuild the object (optional)

See `how-we-built-it/README.md`. The searches are randomised; a rebuild gives different, equally valid labelings.
