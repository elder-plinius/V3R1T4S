#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (POSIX shell, curl, sha256sum, Python 3 standard library)
set -u
failure() { printf '%s\n' FAIL; exit 1; }
sha256sum --check --quiet SHA256SUMS || failure
tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
UA='V3R1T4S-checker (+https://github.com/elder-plinius/V3R1T4S)'; bad=0; n=0
while read inst obj osha url isha ov pg; do
  n=$((n+1))
  [ "$(sha256sum "$obj" | cut -d' ' -f1)" = "$osha" ] || { echo "$inst: solution sha256 mismatch"; bad=$((bad+1)); continue; }
  curl -fsSL --max-time 120 -A "$UA" -o "$tmp/$inst.xml" "$url" || { echo "$inst: download failed"; bad=$((bad+1)); continue; }
  [ "$(sha256sum "$tmp/$inst.xml" | cut -d' ' -f1)" = "$isha" ] || { echo "$inst: instance sha256 mismatch"; bad=$((bad+1)); continue; }
  echo "$inst:"; python3 -I verify-it-yourself/verify.py "$tmp/$inst.xml" "$obj" "$ov" "$pg" || bad=$((bad+1))
  sleep 2
done < verify-it-yourself/expected.txt
echo "checked $n, failed $bad"
if [ "$bad" -eq 0 ] && [ "$n" -eq 1 ]; then printf '%s\n' PASS; else failure; fi
