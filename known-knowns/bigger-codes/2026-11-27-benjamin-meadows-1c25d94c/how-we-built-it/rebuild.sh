#!/bin/sh
# Rebuild the object from the published seed code. Run from the package folder:
#   sh how-we-built-it/rebuild.sh
# Needs curl, a C++17 compiler and Python 3. Downloads one file, converts it to 0/1 rows, compiles the search and
# replays the runs listed in how-we-built-it/chain.tsv (one core), then compares the output with the object.
# Last line: PASS or FAIL.
set -u
H=how-we-built-it
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
SEED_URL=https://aeb.win.tue.nl/codes/cwc/d6/a29.6.6.1205H
SEED_SHA=898cb1edd43ef9ebacc3abc6bca16eeb95e04ecdef4ac3c72f7a301d5d589c8f
curl -sS -o "$T/a29.6.6.1205H" "$SEED_URL" || { echo "download failed"; echo FAIL; exit 1; }
got=$(python3 -c 'import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],"rb").read()).hexdigest())' "$T/a29.6.6.1205H")
echo "seed sha256 $got"
[ "$got" = "$SEED_SHA" ] || { echo "seed file differs from the one used ($SEED_SHA)"; echo FAIL; exit 1; }
python3 $H/seed_to_rows.py "$T/a29.6.6.1205H" 29 > "$T/start.txt" || { echo "seed conversion failed"; echo FAIL; exit 1; }
echo "seed words: $(wc -l < "$T/start.txt" | tr -d ' ')"
CXX=${CXX:-c++}
# -mpopcnt only makes the program faster on x86-64 (a hardware popcount); the results do not depend on it.
case "$(uname -m)" in x86_64|amd64) ARCH=-mpopcnt ;; *) ARCH= ;; esac
$CXX -O2 $ARCH -std=c++17 -o "$T/cwbst" $H/cwbst.cpp || { echo "compile failed"; echo FAIL; exit 1; }
prev="$T/start.txt"
ok=1
while IFS='	' read -r step size rseed tmin tmax rst steps0; do
  [ "$step" = step ] && continue
  # arguments: n w d size seed cpu_seconds outfile seedfile tabu_min tabu_max restart_after
  "$T/cwbst" 29 6 6 "$size" "$rseed" 3600 "$T/out-$size.txt" "$prev" "$tmin" "$tmax" "$rst" > "$T/run-$size.log" 2>&1
  res=$(grep '^RESULT' "$T/run-$size.log" | tail -n 1)
  echo "step $step: size $size, random seed $rseed: $res"
  case "$res" in
    "RESULT FOUND pen 0 steps $steps0 "*) prev="$T/out-$size.txt" ;;
    *) echo "step $step did not end as recorded (FOUND after $steps0 steps)"; ok=0; break ;;
  esac
done < $H/chain.tsv
if [ "$ok" = 1 ] && grep -v '^#' object/A-29-6-6-1207words.txt | cmp -s - "$prev"; then
  echo "search output equals the object (without its first line), byte for byte"
  echo PASS
else
  echo "search output differs from the object"
  echo FAIL
  exit 1
fi
