#!/bin/sh
# Run from the package folder:  sh verify-it-yourself/run_checks.sh
# Needs python3 (standard library only), xz, and curl for the automatic download. The five certificates are not in
# this folder (each is over 1 MB); put cert_n18.txt, cert_n19.txt, cert_n20.txt, cert_n21.txt.xz and cert_n22.txt.xz
# in ./certificates/ (or set CERT_DIR), or let this script fetch them once from the URLs in object/CERTIFICATES.md.
# Two checkers run side by side (about 7 minutes and under 1 GB each on a current core). Last output line: PASS or FAIL.
set -u
export PYTHONDONTWRITEBYTECODE=1
V=verify-it-yourself
CERTS="${CERT_DIR:-certificates}"
fail() { echo "$1"; echo "FAIL"; exit 1; }
field() { sed -n "s/^$1: *//p" object/CERTIFICATES.md | head -n 1; }
fetch() {  # url target
  case "$1" in https://*) ;; *) fail "object/CERTIFICATES.md has no usable URL for $2 yet" ;; esac
  command -v curl >/dev/null 2>&1 || fail "curl not found; download $1 by hand into $CERTS/"
  curl -fsSL -o "$CERTS/$2" "$1" || fail "could not fetch $1"
}

echo "== 1. object/ files match SHA256SUMS"
python3 "$V/sha256check.py" SHA256SUMS . object/ || fail "object/ does not match SHA256SUMS"

echo "== 2. certificates present and matching object/certificates.sha256"
mkdir -p "$CERTS"
if [ ! -f "$CERTS/cert_n18.txt" ] || [ ! -f "$CERTS/cert_n19.txt" ] || [ ! -f "$CERTS/cert_n20.txt" ]; then
  fetch "$(field archive_url)" archive.tar.xz
  got=$(python3 -c "import hashlib,sys; print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" "$CERTS/archive.tar.xz")
  [ "$got" = "$(field archive_sha256)" ] || fail "archive sha256 $got does not match"
  tar -xJf "$CERTS/archive.tar.xz" -C "$CERTS" || fail "could not unpack the archive"
fi
for n in 21 22; do [ -f "$CERTS/cert_n$n.txt.xz" ] || fetch "$(field n${n}_url)" "cert_n$n.txt.xz"; done
python3 "$V/sha256check.py" object/certificates.sha256 "$CERTS" || fail "certificate files do not match object/certificates.sha256"

echo "== 3. two independent checkers over every line of n = 18..22"
L=$(mktemp -d)
( for n in 18 19 20; do python3 "$V/indep_check.py" "$CERTS/cert_n$n.txt" $n --regen; done
  for n in 21 22; do python3 "$V/indep_check.py" "$CERTS/cert_n$n.txt.xz" $n --regen; done ) > "$L/indep.txt" 2>&1 &
( for n in 18 19 20; do python3 "$V/verify_sem_coverage.py" "$V/A000055_18_22.txt" "$CERTS/cert_n$n.txt"; done
  for n in 21 22; do xz -dc "$CERTS/cert_n$n.txt.xz" | python3 "$V/verify_sem_coverage.py" "$V/A000055_18_22.txt" /dev/stdin; done ) > "$L/cov.txt" 2>&1 &
wait
echo "-- indep_check.py --regen (WROM regeneration, 1:1 canonical match, A000055 by Otter's formula)"
cat "$L/indep.txt"
echo "-- verify_sem_coverage.py (AHU canonical codes, distinct count = A000055 from the b-file)"
cat "$L/cov.txt"
a=$(grep -c -- '-> PASS$' "$L/indep.txt"); b=$(grep -c -- '-> PASS$' "$L/cov.txt"); rm -rf "$L"
[ "$a" -eq 5 ] && [ "$b" -eq 5 ] || fail "not every order passed both checkers ($a/5 and $b/5)"
echo "PASS"
