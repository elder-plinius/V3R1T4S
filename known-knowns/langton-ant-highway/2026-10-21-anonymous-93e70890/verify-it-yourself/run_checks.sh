#!/bin/sh
# Standalone check of the 6x6 Langton's-ant p1 package. Run from the package folder: sh verify-it-yourself/run_checks.sh
# Needs: sh, gcc, python3, awk, zcat, sha256sum. About 2 min single-threaded. Last output line: PASS or FAIL.
# 1. object/ integrity and every number of object/RESULT.txt recomputed (verify-it-yourself/code/check_object.py).
# 2. Reassemble the split data into a scratch tree and run the claim checks (verify-it-yourself/code/scripts/run_all.sh):
#    build lantx2 (independent simulator, written from the definition) and lant4/lant_ref (the exhaustive engine, from
#    how-we-built-it/lant4pkg); all 4x4 masks and a 5x5 slice vs saved lant output; the 4096 hard cases vs the chunk
#    summaries; lant4 vs lantx2 per mask; 4 sample units recomputed; the sample summary with a pure-Python recount of
#    the hash selection; 8 tamper tests that must be detected.
PKG=$(pwd)
WD=$(mktemp -d 2>/dev/null || echo "$PKG/.work_$$")
mkdir -p "$WD"
fail() { echo "check failed: $1"; rm -rf "$WD"; echo FAIL; exit 1; }
python3 verify-it-yourself/code/check_object.py || fail "object integrity / RESULT.txt"
mkdir -p "$WD/code" "$WD/data/user-chunk-sums" "$WD/data/validation" "$WD/data/sample" "$WD/data/hard-cases"
cp -r verify-it-yourself/code/lantx2 verify-it-yourself/code/scripts "$WD/code/" || fail "copy code"
cp -r how-we-built-it/lant4pkg "$WD/code/lant4pkg" || fail "copy lant4pkg"
cat object/chunk_sums/chunks_0000-2047.txt object/chunk_sums/chunks_2048-4095.txt | \
  awk -v d="$WD/data/user-chunk-sums" '{for(i=1;i<NF;i++) if($i=="chunk"){c=$(i+1); break} f=d "/chunk_" c ".sum"; print > f; close(f)}'
cat object/validation/enum4_lant2.part0.txt object/validation/enum4_lant2.part1.txt > "$WD/data/validation/enum4_lant2.txt"
cat object/validation/enum5_chunk07_parts/enum5_chunk07_lantc.gz.part* > "$WD/data/validation/enum5_chunk07_lantc.gz"
cat object/sample/sample_units.part0.txt object/sample/sample_units.part1.txt object/sample/sample_units.part2.txt > "$WD/data/sample/sample_units.txt"
[ "$(ls "$WD/data/user-chunk-sums" | wc -l)" = 4096 ] || fail "reassembled chunk summaries are not 4096 files"
( cd "$WD" && sh code/scripts/run_all.sh ) > "$WD/run_all.txt" 2>&1
cat "$WD/run_all.txt"
grep -q "^RUN_ALL: PASS" "$WD/run_all.txt" || fail "claim checks (run_all.sh)"
rm -rf "$WD"
echo PASS
