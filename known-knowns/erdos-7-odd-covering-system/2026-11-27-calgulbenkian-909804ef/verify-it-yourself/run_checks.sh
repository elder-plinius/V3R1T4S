#!/bin/sh
# Runs both checkers on object/ and prints PASS as the last line only if both pass.
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Needs python3 (3.9 or later, standard library only) and a C++17 compiler (c++, or set CXX).
set -u

DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PKG=$(CDPATH= cd -- "$DIR/.." && pwd)
OBJ="$PKG/object"
PY_BIN=${PYTHON:-python3}
CXX_BIN=${CXX:-c++}
export PYTHONDONTWRITEBYTECODE=1

WORK=$(mktemp -d) || {
    echo "FAIL"
    exit 1
}
cleanup() {
    for f in c1.log c1.rc c2.log c2.rc finite_geometry.so; do
        rm -f "$WORK/$f"
    done
    rmdir "$WORK" 2>/dev/null
}
trap cleanup EXIT
trap 'cleanup; echo "FAIL"; exit 1' INT TERM

fail_out() {
    echo "FAIL"
    exit 1
}

# The manifest lists every certificate file with its sha256, and INDEX.csv records the sha256 of the manifest.
# So one comparison here ties every byte of object/MANIFEST.json and object/certs/ to the package's index row.
WANT=$(awk -F, 'NR==2{print $NF}' "$PKG/INDEX.csv" | tr -d '\r\n ')
GOT=$("$PY_BIN" -B -c 'import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],"rb").read()).hexdigest())' "$OBJ/MANIFEST.json") || fail_out
echo "== object/MANIFEST.json sha256: $GOT"
if [ -z "$WANT" ] || [ "$GOT" != "$WANT" ]; then
    echo "object/MANIFEST.json does not match the sha256 recorded in INDEX.csv"
    fail_out
fi

# Use up to 4 processes for the first checker, fewer if the machine has fewer.
NCPU=$(getconf _NPROCESSORS_ONLN 2>/dev/null || echo 1)
case "$NCPU" in
    ''|*[!0-9]*) NCPU=1 ;;
esac
PROCS=$NCPU
if [ "$PROCS" -gt 4 ]; then PROCS=4; fi
if [ "$PROCS" -lt 1 ]; then PROCS=1; fi

echo "== Checker 1: verify-it-yourself/check.py (Python standard library, $PROCS processes)"
T0=$(date +%s)
( "$PY_BIN" -B "$DIR/check.py" --dir "$OBJ" --procs "$PROCS"; echo "$?" > "$WORK/c1.rc" ) 2>&1 | tee "$WORK/c1.log"
T1=$(date +%s)
RC1=$(cat "$WORK/c1.rc" 2>/dev/null || echo 1)
LAST1=$(grep -v '^[[:space:]]*$' "$WORK/c1.log" | tail -n 1)
echo "== Checker 1 finished in $((T1 - T0)) s, exit code $RC1"
if [ "$RC1" != "0" ] || [ "$LAST1" != "PASS" ]; then
    echo "Checker 1 did not pass"
    fail_out
fi

echo "== Checker 2: verify-it-yourself/alternate/ (Python standard library and a C++17 kernel)"
T2=$(date +%s)
"$CXX_BIN" -O3 -std=c++17 -fPIC -shared "$DIR/alternate/finite_geometry.cpp" -o "$WORK/finite_geometry.so" || {
    echo "Could not build the C++17 kernel"
    fail_out
}
( "$PY_BIN" -B "$DIR/alternate/check_alternate.py" "$OBJ" "$WORK/finite_geometry.so"; echo "$?" > "$WORK/c2.rc" ) 2>&1 | tee "$WORK/c2.log"
T3=$(date +%s)
RC2=$(cat "$WORK/c2.rc" 2>/dev/null || echo 1)
LAST2=$(grep -v '^[[:space:]]*$' "$WORK/c2.log" | tail -n 1)
echo "== Checker 2 finished in $((T3 - T2)) s including the build, exit code $RC2"
if [ "$RC2" != "0" ] || [ "$LAST2" != "PASS" ]; then
    echo "Checker 2 did not pass"
    fail_out
fi

echo "== Both checkers passed"
echo "PASS"
exit 0
