#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Rebuilds the input files, compiles the interval checker, replays all seven pieces and their cover checks.
# If FLINT_PY names a Python with python-flint, also replays Arb covers and positivity at 128 bits.
P=$(pwd); W="$P/.work"; rm -rf "$W"; mkdir -p "$W/away-primal/code" "$W/near-lift/certs" || { echo FAIL; exit 1; }
fail(){ echo "$1"; rm -rf "$W"; echo FAIL; exit 1; }
# Every shipped file must match SHA256SUMS. This ties the library inputs to the package; it does not rederive them.
python3 -I - "$P" <<'S' || fail "SHA256SUMS mismatch"
import sys,hashlib,os
p=sys.argv[1]; bad=0
for l in open(p+"/SHA256SUMS"):
    sha,name=l.split(None,1); name=name.strip()
    if hashlib.sha256(open(os.path.join(p,name),"rb").read()).hexdigest()!=sha: print("mismatch",name); bad=1
sys.exit(bad)
S
# The written proof is not machine-checked; this only pins its text.
[ "$(python3 -I -c 'import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],"rb").read()).hexdigest())' "$P/object/PROOF.md")" = "45fa6fa4cedfe7c3fa0ac217e874ea3afeee0876c7804a1e99eaa6308c7b6f56" ] || fail "object/PROOF.md differs from the pinned text"
python3 -I - "$P/object/parts" "$W" <<'E' || fail "parts rebuild failed"
import sys,glob,gzip,hashlib,shutil
pp,w=sys.argv[1:]
for l in open(pp+"/MANIFEST.txt"):
    sha,name=l.split()
    data=b"".join(open(f,"rb").read() for f in sorted(glob.glob(pp+"/"+name+("" if name.endswith(".bin") else ".gz")+".part*")))
    if not name.endswith(".bin"): data=gzip.decompress(data)
    if hashlib.sha256(data).hexdigest()!=sha: sys.exit("hash mismatch "+name)
    open((w+"/trig.bin") if name=="trig.bin" else (w+"/near-lift/certs/"+name),"wb").write(data)
E
cp "$P"/verify-it-yourself/*.py "$P"/verify-it-yourself/check.c "$W/away-primal/code/"; cp -R "$P/object/lib" "$P/object/cover" "$P/object/strips" "$W/away-primal/"
for d in "$W"/away-primal/lib "$W"/away-primal/strips/*/lib; do cp "$W/trig.bin" "$d/trig.bin"; done
cd "$W/away-primal" || fail "cd"
TMPDIR="$W" clang -O2 -ffp-contract=off -frounding-math -o code/check code/check.c -lm || fail "compile failed (clang needed)"
ARB=""; if [ -n "$FLINT_PY" ] && "$FLINT_PY" -c "import flint" 2>/dev/null; then ARB=1; fi
one(){ # lib prefix T eta
  code/check "$1" "$2" "$3" "$4" | tail -1 | cut -c1-170; code/check "$1" "$2" "$3" "$4" >/dev/null || fail "check failed $2"
  python3 -I code/cover_check.py "$2" | tail -1 | cut -c1-110; python3 -I code/cover_check.py "$2" >/dev/null || fail "cover failed $2"
  if [ -n "$ARB" ]; then "$FLINT_PY" -I code/check_arb.py "$1" "$2" "$3" "$4" 2>&1 | tail -1 | cut -c1-150; "$FLINT_PY" -I code/check_arb.py "$1" "$2" "$3" "$4" >/dev/null 2>&1 || fail "arb failed $2"; fi
}
for s in "0 0.2" "0.2 0.3" "0.3 0.4" "0.4 0.5" "0.5 0.6" "0.6 0.7"; do set -- $s; one strips/s$1_$2/lib strips/s$1_$2/c_t0155 0.0155 $1; done
one lib cover/t0156 0.0156 0.7
if [ -n "$ARB" ]; then for e in 0.2 0.3 0.4 0.5 0.6 0.7; do "$FLINT_PY" -I code/check_pts.py $e | tail -1 | cut -c1-130; "$FLINT_PY" -I code/check_pts.py $e >/dev/null || fail "pts $e"; done; else echo "note: FLINT_PY not set: Arb replays and positivity skipped (see RUN_IT_YOURSELF.md)"; fi
cd "$P"; [ -n "$KEEP_WORK" ] || rm -rf "$W"; echo PASS
