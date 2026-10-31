#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Downloads each instance file from the organisers' repository at the pinned commit (not redistributed here),
# checks every schedule in object/ and compares the makespan with expected.txt (file, makespan, table UB). Last line: PASS or FAIL.
set -u
B=https://raw.githubusercontent.com/jrc-rodec/FJSSP-W-Benchmarking/eb1d28381c34525b58736965cddbeb89e095f88a/instances/Example_Instances_FJSSP-WF
T=$(mktemp -d) || { echo FAIL; exit 1; }
trap 'rm -rf "$T"' EXIT
bad=0; n=0
while read f mk ub; do
  n=$((n+1))
  curl -sS -A 'V3R1T4S-checker (+https://github.com/elder-plinius/V3R1T4S)' -o "$T/$f" "$B/$f" || { echo "download failed: $f"; bad=$((bad+1)); continue; }
  out=$(python3 verify-it-yourself/fjsspw_check.py "$T/$f" "object/${f%.fjs}.json")
  echo "$f: $out (table UB $ub)"
  [ "$out" = "VALID makespan=$mk" ] && [ "$mk" -lt "$ub" ] || bad=$((bad+1))
done < verify-it-yourself/expected.txt
echo "checked $n, failed $bad"
[ "$bad" -eq 0 ] && [ "$n" -gt 0 ] && echo PASS || echo FAIL
