#!/bin/sh
# Run every release checker on the shipped degree-diameter graphs.
#   sh verify-it-yourself/run_checks.sh            five small graphs (C + numpy checkers), about a minute
#   BIG=1 THREADS=8 sh verify-it-yourself/run_checks.sh   also the two large graphs with the C checker (minutes to tens of minutes)
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd)
SECTION=known-knowns/biggest-graphs
CONTRACT="$HERE/../check_harness_contract.py"
[ -f "$CONTRACT" ] || { echo "missing known-knowns/check_harness_contract.py (keep the shared helper with this family)"; exit 2; }
require() {  # input files must be present
  for o in "$@"; do
    [ -f "$HERE/$o" ] || { echo "missing $SECTION/$o"; exit 2; }
  done
}
require graphs/G_15_4_n13365.edges
[ "${BIG:-0}" = "1" ] && require graphs/G_13_6_n535495.edges.gz graphs/G_15_6_n1424896.edges.gz
THREADS=${THREADS:-4}
TMP=${TMPDIR:-/tmp}/v3r1t4s-dd.$$
mkdir -p "$TMP"
if command -v sha256sum >/dev/null 2>&1; then SHA="sha256sum"; else SHA="shasum -a 256"; fi
fail=0
echo "== compile"; cc -O3 -o "$TMP/ddcheck" "$HERE/verify-it-yourself/ddcheck.c" -lpthread || exit 2
check_control() {  # file delta D [exact-far-pairs]
  ctrl_file=$1; ctrl_delta=$2; ctrl_D=$3; ctrl_far=${4:-}
  ctrl_rc=0
  "$TMP/ddcheck" "$ctrl_file" "$ctrl_delta" "$ctrl_D" "$THREADS" > "$TMP/control.out" 2> "$TMP/control.err" || ctrl_rc=$?
  tail -2 "$TMP/control.out"
  set -- "$CONTRACT" graph --stdout "$TMP/control.out" --stderr "$TMP/control.err" --exit-code "$ctrl_rc" \
    --file "$ctrl_file" --delta "$ctrl_delta" --diameter "$ctrl_D"
  [ -z "$ctrl_far" ] || set -- "$@" --far "$ctrl_far"
  python3 "$@" || fail=1
}
check_small() {  # file delta D expected_sha
  f="$HERE/graphs/$1"; echo "== $1 (Delta=$2, D=$3)"
  got=$($SHA "$f" | cut -d' ' -f1); [ "$got" = "$4" ] && echo "sha256 ok" || { echo "sha256 MISMATCH $got"; fail=1; }
  "$TMP/ddcheck" "$f" "$2" "$3" "$THREADS" || fail=1
  python3 "$HERE/verify-it-yourself/ddcheck.py" "$f" "$2" "$3" || fail=1
  echo "-- control at D-1 (must be INVALID):"; check_control "$f" "$2" $(( $3 - 1 ))
}
check_small G_9_4_n1700.edges       9 4 d271a1e84aa9539ba47f8d036cd15e4a5a9ccc5a4752d0dacc94a9d35f17eebd
check_small G_15_3_n1620.edges.txt 15 3 da9faa8c8a875ac789506ca3f91a45db37b3f1f3952b729c88199557caa792ce
check_small G_14_4_n8424.edges.txt 14 4 71ef820b5804f77c626209fbcda3a8bd50c546a5fb70175cbe36a9f98f22f281
check_small G_15_4_n13365.edges    15 4 2d36814028c63e32e527fc0f88ac08cbc70be134f8786de4867c58d748dae52f
check_small G_13_4_n6630.edges     13 4 7c44e128901d6dd6b64e0574b90ff8aa21872462338fd267bab466cb268e10a4
echo "-- control: the (13,4) near-miss parent (how-we-built-it/13_4) must be INVALID with exactly 4 far ordered pairs:"
check_control "$HERE/how-we-built-it/13_4/near_miss_N6630_cost2.edges" 13 4 4
if [ "${BIG:-0}" = "1" ]; then
  check_big() {  # gz delta D expected_sha
    echo "== $1 (Delta=$2, D=$3), $THREADS threads"
    gzip -dc "$HERE/graphs/$1" > "$TMP/big.edges"
    got=$($SHA "$TMP/big.edges" | cut -d' ' -f1); [ "$got" = "$4" ] && echo "sha256 (decompressed) ok" || { echo "sha256 MISMATCH $got"; fail=1; }
    "$TMP/ddcheck" "$TMP/big.edges" "$2" "$3" "$THREADS" || fail=1
    rm -f "$TMP/big.edges"
  }
  check_big G_13_6_n535495.edges.gz  13 6 4ed4fc62000b3cbc6c23b08d9db4af383aa28b01e69fc802b5b1bbdbab170e94
  check_big G_15_6_n1424896.edges.gz 15 6 554149b59ffe151197dff3ae48ae315596d9c618924d25db4775b1315ab47a75
else
  echo "== large graphs skipped (set BIG=1)"
fi
rm -rf "$TMP"
[ $fail = 0 ] && echo "ALL CHECKS PASSED" || echo "SOME CHECK FAILED"
exit $fail
