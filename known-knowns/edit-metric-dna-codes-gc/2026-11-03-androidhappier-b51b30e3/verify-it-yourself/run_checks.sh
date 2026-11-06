#!/bin/sh
# Run from the package folder:  sh verify-it-yourself/run_checks.sh
# Checks that object/code_n9_d3_k1042.txt is the claimed file and is a (9,3,4)_4 DNA code in Sun's sense:
# 1042 distinct words over ACGT of length 9, GC weight exactly floor(9/2) = 4, pairwise Levenshtein distance >= 3,
# and Levenshtein distance >= 3 between every codeword and the reverse complement of every codeword (itself included).
# Needs python3 (standard library only). It uses verify_dna_edit_code_fast.py (same definition and the same two
# methods as the family checker verify_dna_edit_code.py, made fast enough for 1042 words); each checker call runs
# once (output kept in a temporary folder). About 1-2 minutes on a laptop. The last output line is PASS or FAIL.
OBJ=object/code_n9_d3_k1042.txt
WANT=b51b30e3082648bc6cb0511bd156b71ae51c967f7281a83010d2c0e844e4a93a
CHK=verify-it-yourself/verify_dna_edit_code_fast.py
ok=1
M=$(mktemp -d)

echo "== 1. sha256 of $OBJ"
GOT=$(python3 -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" "$OBJ")
echo "got  $GOT"
echo "want $WANT"
if [ "$GOT" = "$WANT" ]; then echo "sha256: match"; else echo "sha256: MISMATCH"; ok=0; fi

echo "== 2. 1042 words, n=9, d=3, GC=4, edit distance and reverse-complement constraint (exhaustive, two methods)"
python3 "$CHK" "$OBJ" 9 3 --expect-size 1042
[ $? -eq 0 ] || ok=0

echo "== 3. control: the same object read with d=4 must FAIL (minimum distance is exactly 3; method A only, to keep it fast)"
if python3 "$CHK" "$OBJ" 9 4 --expect-size 1042 --method-a-only > "$M/d4.out" 2>&1; then r=0; else r=1; fi
grep -E "^(method A|first violation|NOT|FAIL|PASS)" "$M/d4.out"
if [ $r -eq 0 ]; then echo "control: unexpected PASS at d=4"; ok=0; else echo "control: FAIL at d=4 as expected"; fi

python3 - "$OBJ" "$M" <<'PY'
import sys
w = open(sys.argv[1]).read().split()
d = sys.argv[2]
comp = {"A": "T", "T": "A", "C": "G", "G": "C"}
def put(name, words):
    open(d + "/" + name, "w").write("\n".join(words) + "\n")
# one A<->T substitution in a copy of the first word (GC weight unchanged, edit distance 1 to the first word)
x = w[0]; i = next(k for k, c in enumerate(x) if c in "AT")
put("near.txt", w[:-1] + [x[:i] + comp[x[i]] + x[i + 1:]])
put("dup.txt", w[:-1] + [w[0]])
# the reverse complement of the first word (GC weight 4; violates d(x, rc(y)) >= 3 with distance 0)
put("rc.txt", w[:-1] + ["".join(comp[c] for c in reversed(w[0]))])
# one letter changed so that the word has GC weight 5 (needs 4)
y = w[-1]; j = next(k for k, c in enumerate(y) if c in "AT")
put("gc.txt", w[:-1] + [y[:j] + "C" + y[j + 1:]])
# a single word whose own reverse complement is at edit distance 2 (ACGTACGTA vs TACGTACGT): tests the x = y case
put("self.txt", ["ACGTACGTA"])
PY
n=4
for t in near dup rc gc self; do
  case $t in
    near) what="last word replaced by the first word with one A<->T substitution";;
    dup)  what="last word replaced by a copy of the first word";;
    rc)   what="last word replaced by the reverse complement of the first word (tests the RC constraint)";;
    gc)   what="one letter of the last word changed so its GC weight is 5";;
    self) what="the one-word code ACGTACGTA (d(x, rc(x)) = 2 < 3; the RC rule includes x = y)";;
  esac
  echo "== $n. control: $what must FAIL"
  if python3 "$CHK" "$M/$t.txt" 9 3 > "$M/$t.out" 2>&1; then r=0; else r=1; fi
  grep -E "^(GC weight|distinct|first violation|NOT|FAIL|PASS)" "$M/$t.out"
  if [ $r -eq 0 ]; then echo "$t control: unexpected PASS"; ok=0; else echo "$t control: FAIL as expected"; fi
  n=$((n+1))
done
rm -rf "$M"

if [ $ok -eq 1 ]; then echo PASS; exit 0; else echo FAIL; exit 1; fi
