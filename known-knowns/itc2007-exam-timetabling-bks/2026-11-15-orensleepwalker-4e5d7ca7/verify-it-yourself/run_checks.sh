#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh   (needs python3, curl and sha256sum; about 0.5 MB of downloads, seconds)
# Downloads the set5 instance and OptHub's posted best from OptHub storage, checks their sha256, requires the checker to
# reproduce 2327 for the posted best, then requires the object to be hard-feasible with total 2305 (< 2327). Last line: PASS or FAIL.
set -u
T=$(mktemp -d) || { echo FAIL; exit 1; }
trap 'rm -rf "$T"' EXIT
bad=0
[ "$(sha256sum object/set5.sol | cut -d' ' -f1)" = "4e5d7ca7deef7801e267778b211a7dd96c20dcea9b4a42b260a72669d7204964" ] || { echo "object sha256 mismatch"; bad=1; }
curl -sS -A 'V3R1T4S-checker (+https://github.com/elder-plinius/V3R1T4S)' -o "$T/set5.exam" "https://opthubstorage.blob.core.windows.net/opthub-data/timetabling/edutt/ett/itc-2007-ett/instances/exam/set5.exam" || bad=1
curl -sS -A 'V3R1T4S-checker (+https://github.com/elder-plinius/V3R1T4S)' -o "$T/posted.sol" "https://opthubstorage.blob.core.windows.net/opthub-data/timetabling/edutt/ett/itc-2007-ett/solutions/set5/set5.sol" || bad=1
[ "$(sha256sum "$T/set5.exam" | cut -d' ' -f1)" = "32729acc5a05156cb43309f50a99c1b9f093970ca9bafefb32d03c1b93bb0553" ] || { echo "instance sha256 mismatch"; bad=1; }
[ "$(sha256sum "$T/posted.sol" | cut -d' ' -f1)" = "b83fcb6a83b95961b08e58fac2a1c9cd547d2024ad3d3553469615869062ee00" ] || { echo "posted best sha256 mismatch"; bad=1; }
a=$(PYTHONDONTWRITEBYTECODE=1 python3 -I verify-it-yourself/check.py "$T/set5.exam" "$T/posted.sol")
b=$(PYTHONDONTWRITEBYTECODE=1 python3 -I verify-it-yourself/check.py "$T/set5.exam" object/set5.sol)
echo "posted best: $a"
echo "object:      $b"
echo "$a" | grep -q '"feasible": true, "hard": {}, "total": 2327,' || { echo "posted best not reproduced as 2327"; bad=1; }
echo "$b" | grep -q '"feasible": true, "hard": {}, "total": 2305,' || { echo "object is not feasible with total 2305"; bad=1; }
if [ "$bad" -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
