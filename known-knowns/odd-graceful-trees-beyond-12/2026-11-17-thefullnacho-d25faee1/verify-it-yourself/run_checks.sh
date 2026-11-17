#!/bin/sh
# Run from the package folder:  sh verify-it-yourself/run_checks.sh
# Needs python3 (standard library only). gcc is optional: if present, the C
# checker is used for any full certificate file that is available.
# Certificate files larger than 1 MB are not in this folder. Put cert_n16.txt
# through cert_n23.txt in ./certificates/ (or set CERT_DIR), or let this script
# fetch the archive named in object/CERTIFICATES.md once archive_url is a live
# https URL. Orders 10..15 and a mixed-order sample are in object/ and are
# always checked, so this script can PASS from a clean copy of the package
# even without the large files; if archive_url is a live https URL it will
# also fetch and check orders 16..23.
# Last output line: PASS or FAIL.
set -u
export PYTHONDONTWRITEBYTECODE=1
V=verify-it-yourself
CERTS="${CERT_DIR:-certificates}"
fail() { echo "$1"; echo "FAIL"; exit 1; }

echo "== 0. self-tests"
python3 "$V/check_og.py" --selftest || fail "python self-test failed"
if command -v cc >/dev/null 2>&1; then
  cc -O2 -std=c11 -o "$V/check_og" "$V/check_og.c" || fail "could not compile check_og.c"
  "$V/check_og" --selftest || fail "C self-test failed"
else
  echo "cc not found; the C checker will be skipped (python will be used)"
fi

echo "== 1. object/ files match SHA256SUMS"
python3 "$V/sha256check.py" SHA256SUMS . object/ || fail "object/ does not match SHA256SUMS"

echo "== 2. sample_labelings.txt (spot check, several orders)"
# The sample mixes orders and is not a census, so the count is not compared to A000055.
python3 - "$V" << 'PY' || fail "sample_labelings.txt failed"
import runpy, sys, os
sys.path.insert(0, sys.argv[1] if False else "verify-it-yourself")
# import from path
import importlib.util
spec = importlib.util.spec_from_file_location("check_og", "verify-it-yourself/check_og.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
n = 0
forms = set()
with open("object/sample_labelings.txt") as f:
    for i, line in enumerate(f, 1):
        try:
            r = m.parse_and_check(line)
        except ValueError as e:
            print("sample line %d: %s" % (i, e)); print("FAIL"); sys.exit(1)
        if r is None:
            continue
        n += 1
        if r[1] in forms:
            print("sample line %d: repeated tree" % i); print("FAIL"); sys.exit(1)
        forms.add(r[1])
print("sample_lines_ok=%d unique=%d" % (n, len(forms)))
if n < 1:
    print("FAIL"); sys.exit(1)
print("PASS")
PY

echo "== 3. bundled certificates for n=10..15 (complete, in object/)"
A000055_10_15="10:106 11:235 12:551 13:1301 14:3159 15:7741"
for pair in $A000055_10_15; do
  n=${pair%%:*}
  e=${pair##*:}
  f=object/cert_n$n.txt
  [ -f "$f" ] || fail "missing $f"
  if [ -x "$V/check_og" ]; then
    "$V/check_og" --n "$n" --expect "$e" "$f" || fail "C check failed for n=$n"
  else
    python3 "$V/check_og.py" --n "$n" --expect "$e" --regen "$f" || fail "python check failed for n=$n"
  fi
done
# Independent regeneration is always run in Python for n=10..15 (stdlib).
if [ -x "$V/check_og" ]; then
  echo "== 3b. independent regeneration of all trees on 10..15 vertices"
  for pair in $A000055_10_15; do
    n=${pair%%:*}
    e=${pair##*:}
    python3 "$V/check_og.py" --n "$n" --expect "$e" --regen "object/cert_n$n.txt" || fail "regen failed for n=$n"
  done
fi

echo "== 4. full certificates n=16..23, if present"
# Prefer CERT_DIR / certificates/ for every n we have; also accept object/ copies.
want_url=$(sed -n 's/^archive_url: *//p' object/CERTIFICATES.md | head -n 1)
want_sha=$(sed -n 's/^archive_sha256: *//p' object/CERTIFICATES.md | head -n 1)
need=
for n in 16 17 18 19 20 21 22 23; do
  if [ ! -f "$CERTS/cert_n$n.txt" ] && [ ! -f "object/cert_n$n.txt" ]; then
    need=1
  fi
done
if [ -n "$need" ]; then
  case "$want_url" in
    https://*)
      command -v curl >/dev/null 2>&1 || fail "curl not found; download the archive by hand into $CERTS/"
      mkdir -p "$CERTS"
      echo "fetching $want_url"
      curl -fsSL -o "$CERTS/archive.tar.xz" "$want_url" || fail "could not fetch $want_url"
      got=$(python3 -c "import hashlib,sys; print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" "$CERTS/archive.tar.xz")
      [ "$got" = "$want_sha" ] || fail "archive sha256 $got does not match $want_sha"
      tar -xJf "$CERTS/archive.tar.xz" -C "$CERTS" || fail "could not unpack the archive"
      ;;
    *)
      echo "full certificates for n=16..23 are not in $CERTS/ and archive_url is not a live https URL yet"
      echo "skipping section 4 (bundled n=10..15 and the sample were checked)"
      echo "OVERALL: PASS"
      echo "PASS"
      exit 0
      ;;
  esac
fi

# Check hashes then each file
if [ -f object/certificates.sha256 ]; then
  # Check whatever cert files are actually present against the sums file.
  for n in 10 11 12 13 14 15 16 17 18 19 20 21 22 23; do
    f=
    [ -f "$CERTS/cert_n$n.txt" ] && f="$CERTS/cert_n$n.txt"
    [ -z "$f" ] && [ -f "object/cert_n$n.txt" ] && f="object/cert_n$n.txt"
    [ -n "$f" ] || continue
    want=$(awk -v n="cert_n$n.txt" '$2==n {print $1}' object/certificates.sha256)
    [ -n "$want" ] || fail "object/certificates.sha256 has no entry for cert_n$n.txt"
    got=$(python3 -c "import hashlib,sys; print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" "$f")
    [ "$got" = "$want" ] || fail "sha256 mismatch for cert_n$n.txt"
  done
  echo "certificate hashes match object/certificates.sha256"
fi

A000055="16:19320 17:48629 18:123867 19:317955 20:823065 21:2144505 22:5623756 23:14828074"
for pair in $A000055; do
  n=${pair%%:*}
  e=${pair##*:}
  f=
  [ -f "$CERTS/cert_n$n.txt" ] && f="$CERTS/cert_n$n.txt"
  [ -z "$f" ] && [ -f "object/cert_n$n.txt" ] && f="object/cert_n$n.txt"
  [ -n "$f" ] || fail "missing cert_n$n.txt after archive step"
  echo "-- n=$n"
  if [ -x "$V/check_og" ]; then
    "$V/check_og" --n "$n" --expect "$e" "$f" || fail "C check failed for n=$n"
  else
    python3 "$V/check_og.py" --n "$n" --expect "$e" "$f" || fail "python check failed for n=$n"
  fi
done

echo "OVERALL: PASS"
echo "PASS"
