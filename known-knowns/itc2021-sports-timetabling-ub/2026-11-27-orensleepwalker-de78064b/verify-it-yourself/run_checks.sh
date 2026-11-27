#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (POSIX shell, curl, sha256sum, Python 3 standard library)
# Re-derives every bound from the downloaded instance with the standard-library certificate scripts. If OR-Tools is installed it also replays
# each saved model (object/<instance>/bound.pbtxt, one worker, the recorded seed); without OR-Tools that step is skipped and reported.
set -u
failure() { printf '%s\n' FAIL; exit 1; }
sha256sum --check --quiet SHA256SUMS || failure
tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
UA='V3R1T4S-checker (+https://github.com/elder-plinius/V3R1T4S)'; bad=0; n=0
while read inst isha script lb seed; do
  n=$((n+1))
  curl -fsSL --max-time 60 -A "$UA" -o "$tmp/$inst.xml" "https://robinxval.ugent.be/validator/Repository/ITC2021/Instances/$inst.xml" || { echo "$inst: download failed"; bad=$((bad+1)); continue; }
  [ "$(sha256sum "$tmp/$inst.xml" | cut -d' ' -f1)" = "$isha" ] || { echo "$inst: instance sha256 mismatch"; bad=$((bad+1)); continue; }
  o=$(python3 -I "$script" "$tmp/$inst.xml" | grep -E '^# Lower bound on|penalty lower bound from BR2')
  got=$(printf '%s' "$o" | grep -oE '[0-9]+$')
  echo "$inst: $o (claimed $lb)"; [ "$got" = "$lb" ] || bad=$((bad+1))
  printf '%s object/%s/bound.pbtxt %s\n' "$inst" "$inst" "$seed" >> "$tmp/models.txt"
  sleep 1
done < verify-it-yourself/expected.txt
if python3 -c 'import ortools' 2>/dev/null; then echo 'solver replay:'; python3 verify-it-yourself/replay.py "$tmp/models.txt" || bad=$((bad+1)); else echo 'solver replay skipped (OR-Tools not installed)'; fi
echo "checked $n, failed $bad"
if [ "$bad" -eq 0 ] && [ "$n" -eq 5 ]; then printf '%s\n' PASS; else failure; fi
