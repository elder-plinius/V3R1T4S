#!/bin/sh
# Self-contained verification runner for the perfect-cuboid p1 exclusion package (v2).
# Run from the package root: sh verify-it-yourself/run_checks.sh
set -u

fail() {
  if [ -n "${TMP_BUILD:-}" ] && [ -d "$TMP_BUILD" ]; then
    rm -rf "$TMP_BUILD"
  fi
  echo "FAIL"
  exit 1
}

trap 'if [ -n "${TMP_BUILD:-}" ] && [ -d "$TMP_BUILD" ]; then rm -rf "$TMP_BUILD"; fi' EXIT

if [ ! -f "object/certificate.json" ] || [ ! -f "object/dgh_internal_edge_cuboids_proof.lean" ]; then
  echo "Missing required object files in object/" >&2
  fail
fi

sha256_file() {
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$1" | awk '{print $1}'
  elif command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$1" | awk '{print $1}'
  elif command -v openssl >/dev/null 2>&1; then
    openssl dgst -sha256 "$1" | awk '{print $NF}'
  else
    return 1
  fi
}

LEAN_SHA=$(sha256_file "object/dgh_internal_edge_cuboids_proof.lean") || fail

# 1. Independent Verifier 1: Strict ISO C99 (-std=c99 -O2 -Wall -Wextra -Werror -Wpedantic)
CC_BIN=""
for cand in cc clang gcc; do
  if command -v "$cand" >/dev/null 2>&1; then
    CC_BIN="$cand"
    break
  fi
done
[ -n "$CC_BIN" ] || { echo "No C compiler found" >&2; fail; }

TMP_BUILD=$(mktemp -d) || fail
"$CC_BIN" -std=c99 -O2 -Wall -Wextra -Werror -Wpedantic \
  "verify-it-yourself/verify_c99.c" -o "$TMP_BUILD/verify_c99" || fail

"$TMP_BUILD/verify_c99" \
  "object/certificate.json" \
  "object/dgh_internal_edge_cuboids_proof.lean" \
  "$LEAN_SHA" || fail

# 2. Independent Verifier 2: Pure-stdlib Python 3 first-principles verifier
PY_BIN=""
for cand in python3 python; do
  if command -v "$cand" >/dev/null 2>&1; then
    PY_BIN="$cand"
    break
  fi
done
[ -n "$PY_BIN" ] || { echo "No python3 found" >&2; fail; }

"$PY_BIN" "verify-it-yourself/verify_py.py" "object" || fail

# 3. Core Lean 4 kernel typecheck + strict #print axioms allowlist audit (exactly 12 blocks, three standard axioms only)
LEAN_BIN=""
if command -v lean >/dev/null 2>&1 && lean --version >/dev/null 2>&1; then
  LEAN_BIN=$(command -v lean)
elif [ -n "${HOME:-}" ] && [ -d "$HOME/.elan/toolchains" ]; then
  for d in "$HOME"/.elan/toolchains/*/bin/lean; do
    if [ -x "$d" ] && "$d" --version >/dev/null 2>&1; then
      case "$d" in
        *-rc*) [ -z "$LEAN_BIN" ] && LEAN_BIN="$d" ;;
        *) LEAN_BIN="$d" ;;
      esac
    fi
  done
fi
[ -n "$LEAN_BIN" ] || { echo "Lean 4 binary not found in PATH or ~/.elan/toolchains" >&2; fail; }

LEAN_OUT=$("$LEAN_BIN" -j 2 "object/dgh_internal_edge_cuboids_proof.lean" 2>&1) || {
  printf "%s\n" "$LEAN_OUT" >&2
  fail
}
printf "%s\n" "$LEAN_OUT"

"$PY_BIN" -c '
import re, sys
out = sys.stdin.read()
allowed = {"propext", "Classical.choice", "Quot.sound"}
blocks = re.findall(r"\x27([^\x27]+)\x27\s+depends on axioms:\s*\[([^\]]*)\]", out, flags=re.S)
if len(blocks) != 12 or len({name for name, _ in blocks}) != 12:
    sys.stderr.write(f"AXIOM_AUDIT_REJECT: expected 12 distinct theorem axiom blocks, got {len(blocks)}\n")
    sys.exit(1)
stripped = re.sub(r"\x27[^\x27]+\x27\s+depends on axioms:\s*\[[^\]]*\]", "", out, flags=re.S).strip()
if stripped:
    sys.stderr.write(f"AXIOM_AUDIT_REJECT: unexpected Lean output: {stripped[:120]}\n")
    sys.exit(1)
for name, ax_str in blocks:
    axioms = [a.strip() for a in ax_str.replace("\n", " ").split(",") if a.strip()]
    bad = [a for a in axioms if a not in allowed]
    if bad:
        sys.stderr.write(f"AXIOM_AUDIT_REJECT: {name} uses disallowed axioms {bad}\n")
        sys.exit(1)
' << EOF_LEAN_AUDIT || fail
$LEAN_OUT
EOF_LEAN_AUDIT

rm -rf "$TMP_BUILD"
TMP_BUILD=""
echo "PASS"
exit 0
