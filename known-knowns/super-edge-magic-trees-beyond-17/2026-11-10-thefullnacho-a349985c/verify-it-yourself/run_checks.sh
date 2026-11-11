#!/bin/sh
# Run from the package folder:  sh verify-it-yourself/run_checks.sh
# Needs python3 (standard library only), xz, and curl for the automatic download. The eight certificates (about 4.9 GB
# compressed) are not in this folder; put them in ./certificates/ (or set CERT_DIR), or let this script fetch them
# from the URLs in object/CERTIFICATES.md. Both checkers read every line of every order, one after the other.
# Resources: about 3 hours on one core in total, and about 12 GB of memory at n = 25 (3.5 GB at n = 24).
# ORDERS="18 19 20" (any subset of 18..25) limits the run, e.g. on a smaller machine. Last output line: PASS or FAIL.
set -u
export PYTHONDONTWRITEBYTECODE=1
V=verify-it-yourself
CERTS="${CERT_DIR:-certificates}"
ORDERS="${ORDERS:-18 19 20 21 22 23 24 25}"
fail() { echo "$1"; echo "FAIL"; exit 1; }
field() { sed -n "s/^$1: *//p" object/CERTIFICATES.md | head -n 1; }
fetch() {
  case "$1" in https://*) ;; *) fail "object/CERTIFICATES.md has no usable URL for $2" ;; esac
  command -v curl >/dev/null 2>&1 || fail "curl not found; download $1 by hand into $CERTS/"
  curl -fsSL -o "$CERTS/$2" "$1" || fail "could not fetch $1"
}
file_for() { if [ "$1" -le 20 ]; then echo "cert_n$1.txt"; else echo "cert_n$1.txt.xz"; fi; }

echo "== 1. object/ files match SHA256SUMS"
python3 "$V/sha256check.py" SHA256SUMS . object/ || fail "object/ does not match SHA256SUMS"

echo "== 2. certificates present and matching object/certificates.sha256"
mkdir -p "$CERTS"
need_archive=0
for n in $ORDERS; do [ "$n" -le 20 ] && [ ! -f "$CERTS/cert_n$n.txt" ] && need_archive=1; done
if [ "$need_archive" = 1 ]; then
  fetch "$(field archive_url)" archive.tar.xz
  got=$(python3 -c "import hashlib,sys; h=hashlib.sha256(); f=open(sys.argv[1],'rb'); [h.update(b) for b in iter(lambda: f.read(1<<20), b'')]; print(h.hexdigest())" "$CERTS/archive.tar.xz")
  [ "$got" = "$(field archive_sha256)" ] || fail "archive sha256 $got does not match"
  tar -xJf "$CERTS/archive.tar.xz" -C "$CERTS" || fail "could not unpack the archive"
fi
for n in $ORDERS; do [ "$n" -ge 21 ] && [ ! -f "$CERTS/cert_n$n.txt.xz" ] && fetch "$(field n${n}_url)" "cert_n$n.txt.xz"; done
grep -E "  ($(for n in $ORDERS; do printf 'cert_n%s\\.txt(\\.xz)?|' $n; done)NONE)\$" object/certificates.sha256 > "$CERTS/.selected.sha256"
python3 "$V/sha256check.py" "$CERTS/.selected.sha256" "$CERTS" || fail "certificate files do not match object/certificates.sha256"

echo "== 3. indep_check.py --regen: every tree regenerated (WROM) and matched 1:1, A000055 by Otter's formula"
a=0
for n in $ORDERS; do
  out=$(python3 "$V/indep_check.py" "$CERTS/$(file_for $n)" $n --regen 2>&1); echo "$out"
  echo "$out" | grep -q -- '-> PASS$' && a=$((a+1))
done
echo "== 4. verify_sem_coverage.py: distinct AHU canonical codes, count = A000055 (b-file), every labeling checked"
b=0
for n in $ORDERS; do
  if [ "$n" -le 20 ]; then out=$(python3 "$V/verify_sem_coverage.py" "$V/A000055_18_25.txt" "$CERTS/cert_n$n.txt" 2>&1)
  else out=$(xz -dc "$CERTS/cert_n$n.txt.xz" | python3 "$V/verify_sem_coverage.py" "$V/A000055_18_25.txt" /dev/stdin 2>&1); fi
  echo "$out"; echo "$out" | grep -q -- '-> PASS$' && b=$((b+1))
done
k=$(echo $ORDERS | wc -w)
[ "$a" -eq "$k" ] && [ "$b" -eq "$k" ] || fail "not every order passed both checkers ($a/$k and $b/$k)"
echo "PASS"
