#!/bin/sh
# Run from the package folder: sh verify-it-yourself/run_checks.sh
# Needs: a C compiler (cc), python3 (standard library), and xz (or python3's lzma module). About 1-2 minutes, ~600 MB of temp disk.
set -eu
T=$(mktemp -d 2>/dev/null || mktemp -d -t v3check)
trap 'rm -rf "$T"' EXIT
cat object/n21_orders.txt.xz.part_aa object/n21_orders.txt.xz.part_ab object/n21_orders.txt.xz.part_ac > "$T/n21_orders.txt.xz"
python3 -I -B -c 'import hashlib,sys; h=hashlib.sha256(open(sys.argv[1],"rb").read()).hexdigest(); print("joined xz sha256", h); sys.exit(0 if h==sys.argv[2] else 1)' "$T/n21_orders.txt.xz" 1a5cfb3b80fe8600bee47668e068a0fcf8923f87f895da9e23a1efe07f02b75d || { echo "joined file does not match"; echo FAIL; exit 1; }
if command -v xz >/dev/null 2>&1; then xz -dc "$T/n21_orders.txt.xz" > "$T/n21_orders.txt"
else python3 -I -B -c 'import lzma,shutil,sys; shutil.copyfileobj(lzma.open(sys.argv[1]), open(sys.argv[2],"wb"))' "$T/n21_orders.txt.xz" "$T/n21_orders.txt"; fi
cc -O2 -o "$T/check_condorcet" verify-it-yourself/check_condorcet.c || { echo "no C compiler"; echo FAIL; exit 1; }
"$T/check_condorcet" 21 6674932 object/n21_assignment.txt < "$T/n21_orders.txt"
