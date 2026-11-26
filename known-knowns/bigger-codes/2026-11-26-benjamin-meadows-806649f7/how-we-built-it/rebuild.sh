#!/bin/sh
# Rebuild the object from the published seed code. Run from the package folder:
#   sh how-we-built-it/rebuild.sh
# Needs curl, a C++17 compiler and Python 3. Downloads one file, compiles the search and runs it once
# (one core, about 1-2 minutes), then compares the output with the object. Last line: PASS or FAIL.
set -u
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
SEED_URL=https://aeb.win.tue.nl/codes/cwc/d12/a30.12.9.44
SEED_SHA=56d5cb3304998a0322d495e97dbb128b8c3710a8201bcdd080d75c0d72d2f4cd
curl -sS -o "$T/a30.12.9.44" "$SEED_URL" || { echo "download failed"; echo FAIL; exit 1; }
got=$(python3 -c 'import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],"rb").read()).hexdigest())' "$T/a30.12.9.44")
echo "seed sha256 $got"
[ "$got" = "$SEED_SHA" ] || { echo "seed file differs from the one used ($SEED_SHA)"; echo FAIL; exit 1; }
CXX=${CXX:-c++}
# bststate.cpp includes <bits/stdc++.h>, which GCC provides and clang on macOS does not; a stand-in header
# with the standard headers it uses is put on the include path (GCC finds its own first).
mkdir -p "$T/inc/bits"
printf '#include <algorithm>\n#include <chrono>\n#include <climits>\n#include <cstdint>\n#include <cstdlib>\n#include <fstream>\n#include <iostream>\n#include <random>\n#include <string>\n#include <unordered_set>\n#include <vector>\n' > "$T/inc/bits/stdc++.h"
$CXX -O2 -std=c++17 -idirafter "$T/inc" -o "$T/bststate" how-we-built-it/bststate.cpp || { echo "compile failed"; echo FAIL; exit 1; }
# arguments: n w d size seed seconds outfile seedfile tabu_min tabu_max restart_after
"$T/bststate" 30 9 12 45 1008 600 "$T/out.txt" "$T/a30.12.9.44" 1 5 1000000000 2> "$T/run.log"
tail -n 1 "$T/run.log"
grep -v '^#' object/A-30-12-9-45words.txt > "$T/object-body.txt"
if cmp -s "$T/out.txt" "$T/object-body.txt"; then
  echo "search output equals the object (without its first line), byte for byte"
  echo PASS
else
  echo "search output differs from the object"
  echo FAIL
  exit 1
fi
