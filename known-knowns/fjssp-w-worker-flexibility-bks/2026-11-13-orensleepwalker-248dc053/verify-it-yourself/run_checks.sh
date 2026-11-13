#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (needs python3, curl and sha256sum; about 15 MB of downloads)
# For every row of expected.txt: checks the schedule file's sha256, downloads the instance at the pinned commit and checks its sha256,
# validates the schedule (verify-it-yourself/check_schedule.py) and requires makespan = expected and makespan <= UB - 1. Last line: PASS or FAIL.
set -u
B=https://raw.githubusercontent.com/jrc-rodec/FJSSP-W-Benchmarking/eb1d28381c34525b58736965cddbeb89e095f88a/instances/Example_Instances_FJSSP-WF
T=$(mktemp -d) || { echo FAIL; exit 1; }
trap 'rm -rf "$T"' EXIT
bad=0; n=0
while read f osha isha mk ub; do
  n=$((n+1))
  [ "$(sha256sum "object/$f.json" | cut -d' ' -f1)" = "$osha" ] || { echo "$f: object sha256 mismatch"; bad=$((bad+1)); continue; }
  curl -sS -A 'V3R1T4S-checker (+https://github.com/elder-plinius/V3R1T4S)' -o "$T/$f.fjs" "$B/$f.fjs" || { echo "$f: download failed"; bad=$((bad+1)); continue; }
  [ "$(sha256sum "$T/$f.fjs" | cut -d' ' -f1)" = "$isha" ] || { echo "$f: instance sha256 mismatch"; bad=$((bad+1)); continue; }
  out=$(python3 verify-it-yourself/check_schedule.py "$T/$f.fjs" "object/$f.json")
  echo "$f: $out (listed UB $ub)"
  [ "$out" = "VALID makespan=$mk" ] && [ "$mk" -le $((ub-1)) ] || bad=$((bad+1))
done < verify-it-yourself/expected.txt
echo "checked $n, failed $bad"
if [ "$bad" -eq 0 ] && [ "$n" -eq 65 ]; then echo PASS; else echo FAIL; exit 1; fi
