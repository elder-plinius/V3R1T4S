#!/bin/sh
# Run from the package folder:  sh verify-it-yourself/run_checks.sh   (last output line: PASS or FAIL)
# Needs: python 3.9+ with mpmath, the .NET SDK 8 or newer (10 used), network access to raw.githubusercontent.com (pinned commit).
# What this script runs: hashes, build, interval-type containment test, negative controls (valid author certificate verifies; 10 tampered copies and a raised-tau copy of the real certificate are refused),
# and a deterministic 1% slice (43 of 3,596 jobs, 2,897,141 leaves) of the real certificate. The FULL replay (245,496,952 leaves)
# takes about 2.5 hours on 5-6 threads and is a separate documented command (RUN_IT_YOURSELF.md, step 7); its log is in object/records/.
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
mkdir -p "$W/work" "$W/outputs/controls" || finish 1
stamp; echo "step 2: fetch the pinned public inputs and check their sha256"
"$PY" -B verify-it-yourself/fetch_inputs.py "$W/work" || finish 1
cp -r object/LebVerifyI object/tools "$W/" || finish 1
cd "$W" || finish 1
stamp; echo "step 3: build the verifier"
(cd LebVerifyI && dotnet build -c Release -o ../dbin >"$TMP/build.log" 2>&1) || { tail -20 "$TMP/build.log"; finish 1; }
stamp; echo "step 4: Iv containment test (random operations against exact Fractions / mpmath.iv)"
dotnet dbin/LebVerify.dll ivtest 20000 outputs/ivtest_records.txt 7 >/dev/null || finish 1
"$PY" -B tools/ivtest_check.py outputs/ivtest_records.txt | tee outputs/ivtest_check.txt || finish 1
grep -q "violations: 0" outputs/ivtest_check.txt || finish 1
stamp; echo "step 5: negative controls (valid author control must verify; header, bit-stream and threshold tampers must be refused)"
"$PY" -B tools/make_tampers.py work/certB_test.bin >/dev/null || finish 1
THREADS=$("$PY" -B -c "import os;print(max(1,min(16,(os.cpu_count() or 4)-2)))")
ctl() { n=$1; f=$2; dotnet dbin/LebVerify.dll verify "$f" --threads 1 --claim none > "outputs/controls/$n.txt" 2>&1; echo $? > "outputs/controls/$n.rc"; }
ctl certB_test work/certB_test.bin &
for n in bad_magic trailing_byte truncated_file inflate_negative inflate_zero tmax_0.60 tmax_0.65 flip_first_bit flip_mid_bit truncated_block; do ctl "$n" "work/tamper/$n.bin" &
  while [ "$(jobs -r | wc -l)" -ge 6 ]; do sleep 1; done
done
wait
# threshold control on the REAL certificate: raising the header tau to 0.83442 must make job 3431 (which holds the worst leaves) fail, while the unpatched job passes
"$PY" -B -c "
import struct,sys
b=bytearray(open('work/cert_B_08344.bin','rb').read()); struct.pack_into('<d',b,8,0.83442); open('work/cert_tau83442.bin','wb').write(b)" || finish 1
dotnet dbin/LebVerify.dll verify work/cert_B_08344.bin --threads "$THREADS" --claim none --jobs 3431-3432 > outputs/controls/real_job3431_unpatched.txt 2>&1; echo $? > outputs/controls/real_job3431_unpatched.rc
dotnet dbin/LebVerify.dll verify work/cert_tau83442.bin --threads "$THREADS" --claim none --jobs 3431-3432 > outputs/controls/real_job3431_tau83442.txt 2>&1; echo $? > outputs/controls/real_job3431_tau83442.rc
"$PY" -B - <<'PYEOF' || finish 1
import glob, os, sys
bad = []; n_run = 0
for rc in sorted(glob.glob("outputs/controls/*.rc")):
    n = os.path.basename(rc)[:-3]; code = int(open(rc).read().strip()); txt = open("outputs/controls/%s.txt" % n, errors="replace").read(); n_run += 1
    if n == "certB_test":
        ok = code == 0 and "RESULT VERIFIED" in txt
    elif n == "real_job3431_unpatched":
        ok = code == 0 and "RESULT: SLICE OK" in txt
    else:
        ok = code != 0 and "RESULT VERIFIED" not in txt and "SLICE OK" not in txt
    print("%-24s exit=%d %s" % (n, code, "as expected" if ok else "UNEXPECTED"))
    if not ok: bad.append(n)
print("controls: %d run, unexpected %s" % (n_run, bad))
sys.exit(1 if bad or n_run != 13 else 0)
PYEOF
stamp; echo "step 6: deterministic 1% slice of the real certificate on $THREADS threads (interval mode)"
dotnet dbin/LebVerify.dll verify work/cert_B_08344.bin --threads "$THREADS" --claim 8344/10000 --sample 0.01 --sseed 3 > outputs/slice.log 2>&1 || { tail -20 outputs/slice.log; finish 1; }
grep -E "jobs covered|failing leaves|RESULT|covers|child-covers" outputs/slice.log
grep -q "RESULT: SLICE OK" outputs/slice.log || finish 1
grep -q "failing leaves 0 " outputs/slice.log || finish 1
grep -q "leaves 2,897,141" outputs/slice.log || finish 1
trap - EXIT
finish 0
