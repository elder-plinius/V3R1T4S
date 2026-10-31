#!/bin/sh
# Run from the package folder:  sh verify-it-yourself/run_checks.sh   (last output line: PASS or FAIL)
# Needs: python (3.9+), the .NET SDK (8 or newer), network access to github.com (pinned archive download).
cd "$(dirname "$0")/.." || { echo FAIL; exit 1; }
PKG=$(pwd)
PY=python
command -v "$PY" >/dev/null 2>&1 || PY=python3
TMP=
finish() {
  rc=$1
  [ -n "$TMP" ] && rm -rf "$TMP" 2>/dev/null || true
  if [ "$rc" -eq 0 ]; then echo PASS; exit 0; else echo FAIL; exit 1; fi
}
trap 'finish 1' EXIT INT TERM HUP
set -u
echo "step 1: sha256 of every file in object/"
"$PY" -I -B verify-it-yourself/check_hashes.py || finish 1
TMP=$(mktemp -d) || finish 1
W="$TMP/workdir"
V="$W/attempts/csharp-verifier/code"
mkdir -p "$V" "$W/attempts/csharp-verifier/result" "$W/data/hervay_inputs" || finish 1
cp -r object/RidVerify "$V/" || finish 1
echo "step 2: fetch the pinned public inputs and check their sha256"
"$PY" -I -B verify-it-yourself/fetch_inputs.py "$W/data/hervay_inputs" || finish 1
echo "step 3: build the verifier"
cd "$V/RidVerify" || finish 1
dotnet build -c Release -o ../build >"$TMP/build.log" 2>&1 || { tail -20 "$TMP/build.log"; finish 1; }
echo "step 4: run the full verification (about 5 minutes on 4 threads)"
dotnet ../build/RidVerify.dll all >"$TMP/run.log" 2>&1
RC=$?
grep -E 'accepted|CONTROLS total|OVERALL|coverage|zoom' "$TMP/run.log" | tail -40
[ "$RC" -eq 0 ] || finish 1
grep -q 'OVERALL: ALL CHECKS PASSED' "$TMP/run.log" || finish 1
trap - EXIT
finish 0
