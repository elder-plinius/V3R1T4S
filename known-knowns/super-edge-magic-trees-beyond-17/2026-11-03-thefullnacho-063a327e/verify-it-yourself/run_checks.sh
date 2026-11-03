#!/bin/sh
# Run from the package folder:  sh verify-it-yourself/run_checks.sh
# Needs python3 (standard library only). The three full certificates (about 192 MB of text) are not in this folder
# (each is over 1 MB); they come from the archive named in object/CERTIFICATES.md. Put cert_n18.txt, cert_n19.txt and
# cert_n20.txt in ./certificates/ (or set CERT_DIR), or let this script fetch the archive once from archive_url.
# Last output line: PASS or FAIL.
set -u
export PYTHONDONTWRITEBYTECODE=1
V=verify-it-yourself
CERTS="${CERT_DIR:-certificates}"
fail() { echo "$1"; echo "FAIL"; exit 1; }

echo "== 1. object/ files match SHA256SUMS"
python3 "$V/sha256check.py" SHA256SUMS . object/ | tail -n 4
python3 "$V/sha256check.py" SHA256SUMS . object/ >/dev/null || fail "object/ does not match SHA256SUMS"

echo "== 2. the five hardest trees (object/hardest_trees_n19_n20.txt): labelings"
python3 "$V/check_sem.py" object/hardest_trees_n19_n20.txt
python3 "$V/check_sem.py" object/hardest_trees_n19_n20.txt | tail -n 1 | grep -qx PASS || fail "hardest-tree labelings fail"

echo "== 3. full certificates"
if [ ! -f "$CERTS/cert_n18.txt" ] || [ ! -f "$CERTS/cert_n19.txt" ] || [ ! -f "$CERTS/cert_n20.txt" ]; then
  url=$(sed -n 's/^archive_url: *//p' object/CERTIFICATES.md | head -n 1)
  want=$(sed -n 's/^archive_sha256: *//p' object/CERTIFICATES.md | head -n 1)
  case "$url" in
    https://*) ;;
    *) fail "certificates not found in $CERTS/ and object/CERTIFICATES.md has no archive_url yet" ;;
  esac
  command -v curl >/dev/null 2>&1 || fail "curl not found; download $url by hand into $CERTS/"
  mkdir -p "$CERTS"
  curl -fsSL -o "$CERTS/archive.tar.xz" "$url" || fail "could not fetch $url"
  got=$(python3 -c "import hashlib,sys; print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" "$CERTS/archive.tar.xz")
  [ "$got" = "$want" ] || fail "archive sha256 $got does not match $want"
  tar -xJf "$CERTS/archive.tar.xz" -C "$CERTS" || fail "could not unpack the archive"
fi
python3 "$V/sha256check.py" object/certificates.sha256 "$CERTS" || fail "certificate files do not match object/certificates.sha256"

echo "== 4. coverage: trees on n vertices, distinct canonical forms, count = A000055(n), every labeling valid"
for n in 18 19 20; do
  python3 "$V/verify_sem_coverage.py" "$V/A000055_18_20.txt" "$CERTS/cert_n$n.txt" || fail "coverage check failed for n=$n"
done

echo "== 5. independent regeneration of all trees on 18..20 vertices and one-to-one matching"
python3 "$V/verify_cert.py" "$V/A000055_18_20.txt" "$CERTS/cert_n18.txt" "$CERTS/cert_n19.txt" "$CERTS/cert_n20.txt" \
  || fail "regeneration check failed"
echo "PASS"
