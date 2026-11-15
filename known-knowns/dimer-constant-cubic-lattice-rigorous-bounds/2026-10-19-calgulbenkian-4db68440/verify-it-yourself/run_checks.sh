#!/bin/sh
_PKG=$(cd "$(dirname "$0")/.." && pwd)
if command -v shasum >/dev/null 2>&1; then _S="shasum -a 256"; else _S="sha256sum"; fi
( cd "$_PKG" && grep "  object/" SHA256SUMS > "${TMPDIR:-/tmp}/objsums.$$" && $_S -c "${TMPDIR:-/tmp}/objsums.$$" >/dev/null 2>&1 ) || { echo "object file sha256 MISMATCH against SHA256SUMS"; echo "FAIL"; exit 1; }
echo "all object/ files match SHA256SUMS"
# Monomer-dimer h3 bound at (m,n) = (5,4).  Python 3.8+ standard library plus a C compiler (cc); about 20 seconds, about 1 GB of memory.
# Step 1 is a sanity run on the (3,3) vector of the earlier claim (expected 0.786044083039..., bound 0.7860441).
cd "$(dirname "$0")" || exit 1
echo "== sanity: (3,3) =="
python3 -I check_h3.py 3 3 cert_md_h3_33_sibling.txt 731051554747087 618837374495 0.7860441 || { echo SOME CHECK FAILED; exit 1; }
echo "== claim: (5,4) =="
mkdir -p _asm || exit 1
python3 -I assemble.py _asm/cert_md_h3_54.txt || { echo SOME CHECK FAILED; exit 1; }
python3 -I check_h3.py 5 4 _asm/cert_md_h3_54.txt 1891821269973664 281869529 0.7859681
rc=$?
rm -f _asm/cert_md_h3_54.txt; rmdir _asm 2>/dev/null
exit $rc
