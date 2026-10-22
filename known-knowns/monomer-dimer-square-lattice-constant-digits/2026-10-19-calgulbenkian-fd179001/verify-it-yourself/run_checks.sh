#!/bin/sh
# Run from the claim folder: sh verify-it-yourself/run_checks.sh
# Needs only python3 (standard library), about 40 s and about 6.5 GB of memory.
# check_p1.py looks for MANIFEST.txt and the parts next to itself, so it runs in a temporary copy.
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$HERE/.." && pwd)
TMP=$(mktemp -d)
cp "$HERE/check_p1.py" "$TMP/"
cp "$ROOT"/object/cert_part0*.bin "$ROOT/object/MANIFEST.txt" "$TMP/"
out=$(cd "$TMP" && python3 -I check_p1.py 2>&1)
status=$?
rm -r "$TMP"
printf '%s\n' "$out"
if [ "$status" -eq 0 ] && printf '%s\n' "$out" | grep -q '^CERTIFIED: 0.6627989728337 < h2 < 0.6627989728338'; then
  echo PASS
else
  echo FAIL
  exit 1
fi
