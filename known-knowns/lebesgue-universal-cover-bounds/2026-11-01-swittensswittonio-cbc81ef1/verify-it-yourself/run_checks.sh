#!/bin/sh
# Run from the package folder:  sh verify-it-yourself/run_checks.sh   (last output line: PASS or FAIL)
# Needs: python 3.9+ with mpmath, the .NET SDK 8 or newer (10 used), about 4 GB free disk, network the FIRST time
# (Zenodo, 765 MB, cached afterwards in V3R1T4S_CACHE or <temp>/v3r1t4s_zeng_cache after md5+sha256 verification).
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
stamp() { printf "[%s] " "$(date -u +%H:%M:%S)"; }
stamp; echo "step 1: sha256 of every file in object/"
"$PY" -B verify-it-yourself/check_hashes.py || finish 1
TMP=$(mktemp -d) || finish 1
W="$TMP/w"
mkdir -p "$W/work" "$W/out/controls" || finish 1
stamp; echo "step 2: fetch the pinned public certificate (md5 + sha256 checked) and unpack it"
"$PY" -B verify-it-yourself/fetch_inputs.py "$TMP/in" || finish 1
"$PY" -B -c "import zipfile,sys;zipfile.ZipFile(sys.argv[1]).extractall(sys.argv[2])" "$TMP/in/certificate.zip" "$W/work" || finish 1
rm -f "$TMP/in/certificate.zip"
cp -r object/ZengCheck object/tables object/scripts "$W/" || finish 1
cd "$W" || finish 1
stamp; echo "step 3: sample-point tables: independent 90-digit membership re-check; far-field constants with exact radii"
"$PY" -B scripts/table_check.py tables/tables_b.txt | tee out/table_check.txt || finish 1
grep -q "enclosure violations 0" out/table_check.txt || finish 1
"$PY" -B scripts/reduction_check.py | tee out/reduction_check.txt || finish 1
stamp; echo "step 4: build the checker"
(cd ZengCheck && dotnet build -c Release -o ../dbin >"$TMP/build.log" 2>&1) || { tail -20 "$TMP/build.log"; finish 1; }
stamp; echo "step 5: interval type self-test (random operations against exact Fractions / mpmath)"
dotnet dbin/ZengCheck.dll selftest out/iv_selftest.txt 20000 >/dev/null || finish 1
"$PY" -B scripts/iv_selftest.py out/iv_selftest.txt | tee out/iv_selftest.result.txt || finish 1
grep -q "violations 0" out/iv_selftest.result.txt || finish 1
THREADS=$("$PY" -B -c "import os;print(max(1,min(16,(os.cpu_count() or 4)-2)))")
stamp; echo "step 6: replay ALL leaves of the certificate (2,374 + 1,029 collar leaves, 6,742,989 core leaves) on $THREADS threads"
dotnet dbin/ZengCheck.dll --cert work/certificate --tables tables/tables_b.txt --excl tables/author_exclusions.json --parts r3_collar,r5_collar,core5d --threads "$THREADS" --out out/final2.jsonl >out/final2.log 2>&1 || { tail -20 out/final2.log; finish 1; }
dotnet dbin/ZengCheck.dll verdict --cert work/certificate --out out/final2.jsonl --verdict out/final2_verdict.txt >out/verdict.log 2>&1
RC=$?
cat out/final2_verdict.txt
[ "$RC" -eq 0 ] || finish 1
grep -q "TOTAL leaves=6746392 failing=0" out/final2_verdict.txt || finish 1
grep -q "VERDICT: ACCEPT" out/final2_verdict.txt || finish 1
stamp; echo "step 7: negative controls (tampered one-frontier mini certificates; each must be rejected)"
"$PY" -B scripts/make_tamper.py >/dev/null || finish 1
"$PY" -B scripts/run_controls.py dbin/ZengCheck.dll tables/tables_b.txt --excl tables/author_exclusions.json | tee out/controls.log || finish 1
"$PY" -B "$PKG/verify-it-yourself/check_controls.py" out/controls/summary.json || finish 1
trap - EXIT
finish 0
