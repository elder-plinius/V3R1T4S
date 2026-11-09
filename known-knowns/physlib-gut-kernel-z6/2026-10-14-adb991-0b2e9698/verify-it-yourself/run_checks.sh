#!/bin/sh
# Check this package's proof. Run from the package folder:  sh verify-it-yourself/run_checks.sh
# Needs: Python 3 (standard library), git, Lean 4 v4.34.1 with `lake` on PATH (elan picks it from Physlib's
# lean-toolchain), and Physlib built at commit be0f21e5002d6d73b87f2055530c1e8bf7151546 in $PHYSLIB (default: $HOME/physlib):
#   git clone https://github.com/leanprover-community/physlib "$HOME/physlib"
#   git -C "$HOME/physlib" checkout be0f21e5002d6d73b87f2055530c1e8bf7151546
#   cd "$HOME/physlib" && lake exe get_cache && lake build
# The checker compiles the frozen statement (verify-it-yourself/spec_inclSM_ker.lean) as its own module, then the object
# (object/InclSMKer.lean), then `theorem V3R1T4S_check : V3R1T4S.spec := V3R1T4S.claim` with `#print axioms`.
# It needs about 6 GB of memory and writes scratch files in a folder `tmp` next to the Physlib checkout
# (its own subfolder is deleted afterwards). Last line of output: PASS or FAIL.
PHYSLIB=${PHYSLIB:-$HOME/physlib}
PIN=be0f21e5002d6d73b87f2055530c1e8bf7151546
cd "$(dirname "$0")/.." || { echo "cannot enter the package folder"; echo FAIL; exit 1; }
if [ ! -d "$PHYSLIB" ]; then echo "no Physlib checkout at $PHYSLIB (set PHYSLIB)"; echo FAIL; exit 1; fi
HEAD=$(git -C "$PHYSLIB" rev-parse HEAD 2>/dev/null || echo unknown)
echo "physlib commit: $HEAD"
if [ "$HEAD" != "$PIN" ] && [ -z "${V3R1T4S_ANY_PHYSLIB:-}" ]; then
  echo "the claim is about Physlib $PIN; set V3R1T4S_ANY_PHYSLIB=1 to check against another commit"
  echo FAIL; exit 1
fi
echo "object sha256: $(sha256sum object/InclSMKer.lean 2>/dev/null | cut -c1-64)"
python3 -I verify-it-yourself/lean_claim_check.py --physlib "$PHYSLIB" \
  --spec verify-it-yourself/spec_inclSM_ker.lean --candidate object/InclSMKer.lean
