#!/bin/sh
# Check this package: Erdos Problem 677 (Justin Sun Prize JSP-000550), no counterexample with 0 <= n <= 5871 k.
# Run from the package folder:
#   sh verify-it-yourself/run_checks.sh
# Needs: python3 (standard library only), sha256sum or shasum, cmp, mktemp; nice is used when present.
# About 0.2 GB of memory, one core, a few minutes (the recomputation in step 3 dominates).
# What it does, in order (it stops at the first problem):
#   1. the three object files are the ones the panel read: their sha256 must equal the values recorded in
#      the claim (how-we-built-it/claim/CLAIM.md, "Object files").
#   2. the saved output object/out/range_nCk_C5871.txt reports no counterexample and ends with the RESULT line.
#   3. reruns `python3 -I object/range_nCk.py 5871` (at nice -n 10) and compares its output byte for byte with
#      object/out/range_nCk_C5871.txt; the fresh output must end with the same RESULT line.
#   4. sanity check of the exact judge verify-it-yourself/check677.py (same bytes as the claim's checker):
#      the two known near-misses (k, n, m) = (3, 4, 13) and (4, 18, 53) must be rejected with "lcms differ",
#      and Erdos's different-length coincidence M(4,3) = M(13,2) = 210 must be accepted (so the judge can say PASS).
# Last line of output: PASS or FAIL (exit status 0 or 1).
# The mathematical argument that makes the enumeration complete (no cap on m) is object/PROOF.md; it relies on
# Rosser-Schoenfeld (1962) and Schoenfeld (1976), which this script does not and cannot check.

SHA_PROOF=a6c79becb3858a3d64648aa138040aa7f8411f1c98af00787e85c5b8f2312210
SHA_PROG=b83f0f45f0324da37bbe56575555560cdc7317fc04df92253a74c80a9a291824
SHA_OUT=84b1d82fb5d2474686c60663817c5fb49709d7372987c4e044157aac61008d14
RESULT_LINE="RESULT: no counterexample with n <= 5871 k"

say() { printf '%s\n' "$*"; }
WORK=""
cleanup() { if [ -n "$WORK" ]; then rm -rf "$WORK"; fi; }
fail() { say "problem: $*"; cleanup; say FAIL; exit 1; }
trap 'cleanup' EXIT
trap 'say "interrupted"; cleanup; say FAIL; exit 1' INT TERM

cd "$(dirname "$0")/.." || { say "cannot enter the package folder"; say FAIL; exit 1; }

case "${1:-}" in
  -h|--help) sed -n '2,19p' "$0"; exit 0 ;;
  "") ;;
  *) fail "unknown option $1 (no options; see --help)" ;;
esac

for t in python3 cmp mktemp tail date; do
  command -v "$t" >/dev/null 2>&1 || fail "needs $t on PATH"
done
if command -v sha256sum >/dev/null 2>&1; then SHA="sha256sum"
elif command -v shasum >/dev/null 2>&1; then SHA="shasum -a 256"
else fail "needs sha256sum or shasum"; fi
NICE=""; if command -v nice >/dev/null 2>&1; then NICE="nice -n 10"; fi
WORK=$(mktemp -d 2>/dev/null || mktemp -d -t v3r1t4s) || fail "cannot create a scratch folder"
hash_of() { $SHA < "$1" | awk '{print $1}'; }

say "package check: erdos-677-lcm-blocks (Erdos 677 = JSP-000550), no counterexample with 0 <= n <= 5871 k"
say "python3: $(python3 -c 'import sys; print(sys.version.split()[0])')"

# 1. object integrity
for pair in "object/PROOF.md $SHA_PROOF" "object/range_nCk.py $SHA_PROG" "object/out/range_nCk_C5871.txt $SHA_OUT"; do
  f=${pair% *}; want=${pair#* }
  [ -f "$f" ] || fail "$f is missing"
  got=$(hash_of "$f")
  [ "$got" = "$want" ] || fail "$f has sha256 $got, the claim records $want (the file is not the one the panel read)"
  say "  $got  $f"
done
say "step 1 object files: sha256 equal to the claim's record: ok"

# 2. the saved output
grep -qx 'counterexamples found (n, m, k): \[\]' object/out/range_nCk_C5871.txt \
  || fail "object/out/range_nCk_C5871.txt does not report an empty counterexample list"
last=$(tail -n 1 object/out/range_nCk_C5871.txt)
[ "$last" = "$RESULT_LINE" ] || fail "object/out/range_nCk_C5871.txt ends with '$last', expected '$RESULT_LINE'"
say "step 2 saved output: counterexamples found (n, m, k): [], last line '$last': ok"

# 3. recompute
t0=$(date +%s)
$NICE python3 -I object/range_nCk.py 5871 > "$WORK/range_nCk_C5871.txt" 2> "$WORK/err.txt"
rc=$?
t1=$(date +%s)
[ "$rc" = 0 ] || { cat "$WORK/err.txt"; fail "object/range_nCk.py 5871 exited with status $rc"; }
say "  fresh run of object/range_nCk.py 5871: exit 0, $((t1 - t0)) s, sha256 $(hash_of "$WORK/range_nCk_C5871.txt")"
cmp - object/out/range_nCk_C5871.txt < "$WORK/range_nCk_C5871.txt" > "$WORK/cmp.txt" 2>&1 \
  || { cat "$WORK/cmp.txt"; fail "the fresh output differs from object/out/range_nCk_C5871.txt"; }
flast=$(tail -n 1 "$WORK/range_nCk_C5871.txt")
[ "$flast" = "$RESULT_LINE" ] || fail "the fresh output ends with '$flast'"
say "step 3 recomputation: byte-identical to object/out/range_nCk_C5871.txt, last line '$flast': ok"

# 4. the exact judge on the two known near-misses (must be rejected) and on a known equality (must be accepted)
for t in "4 13 3" "18 53 4"; do
  # shellcheck disable=SC2086
  python3 -I verify-it-yourself/check677.py $t > "$WORK/j.txt" 2>&1
  jrc=$?
  jl=$(tail -n 1 "$WORK/j.txt")
  if [ "$jrc" = 1 ] && [ "$jl" = FAIL ] && grep -qx 'problem: lcms differ' "$WORK/j.txt"; then
    say "  near-miss check677.py $t (n m k): $(sed -n 1p "$WORK/j.txt"), $(sed -n 2p "$WORK/j.txt"), lcms differ: rejected as expected"
  else
    cat "$WORK/j.txt"; fail "check677.py $t should print 'problem: lcms differ' and FAIL"
  fi
done
python3 -I verify-it-yourself/check677.py 4 13 3 --allow-different-length 2 > "$WORK/j.txt" 2>&1
jrc=$?
[ "$jrc" = 0 ] && [ "$(tail -n 1 "$WORK/j.txt")" = PASS ] \
  || { cat "$WORK/j.txt"; fail "check677.py should accept Erdos's coincidence M(4,3) = M(13,2)"; }
say "  positive control check677.py 4 13 3 --allow-different-length 2: $(sed -n 1p "$WORK/j.txt"): accepted as expected"
say "step 4 exact judge: ok"

say PASS
exit 0
