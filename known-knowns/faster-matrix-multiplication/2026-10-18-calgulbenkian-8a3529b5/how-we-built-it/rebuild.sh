#!/bin/sh
# Rebuild object/11x14x16_m1547_ZT.json from the rank-1540 integer scheme of #410 (how-we-built-it/start/), in the two
# steps the agent ran after the block substitution: the ternary split (rank 1548), then the ternary flip reduction
# tools/zt_flip_reduce.c with 100000 steps, seed 1337 and maximum coefficient 1 (rank 1547). Needs python3 and a C compiler.
# Run from the package folder: sh how-we-built-it/rebuild.sh [OUTDIR]   (default OUTDIR: ./rebuild-out; nothing is deleted)
set -eu
HERE=$(cd "$(dirname "$0")/.." && pwd)
OUT=${1:-./rebuild-out}
mkdir -p "$OUT"
B="$HERE/how-we-built-it"
CHK="$HERE/verify-it-yourself/check_fmm_fast.py"
echo "== step 2: ternary split of the rank-1540 integer scheme"
python3 -I "$B/rebuild_split.py" "$B/start/11x14x16_m1540_Z.json" "$OUT/split_m1548_ZT.json"
python3 -I "$CHK" "$OUT/split_m1548_ZT.json" --expect-rank 1548 --expect-class ZT | tail -n 1
echo "== step 3: ternary flip reduction (100000 steps, seed 1337, maximum coefficient 1)"
${CC:-cc} -O2 -o "$OUT/zt_flip_reduce" "$B/tools/zt_flip_reduce.c"
python3 -I "$B/flip_io.py" to-text "$OUT/split_m1548_ZT.json" "$OUT/flip_in.txt"
"$OUT/zt_flip_reduce" 100000 1337 1 < "$OUT/flip_in.txt" > "$OUT/flip_out.txt"
python3 -I "$B/flip_io.py" from-text "$OUT/flip_out.txt" "$OUT/rebuilt_m1547_ZT.json"
python3 -I "$CHK" "$OUT/rebuilt_m1547_ZT.json" --expect-rank 1547 --expect-class ZT | tail -n 1
echo "== compare the rebuilt scheme with the shipped object"
python3 -I "$HERE/verify-it-yourself/convert_sparse.py" compare "$OUT/rebuilt_m1547_ZT.json" "$HERE/object/11x14x16_m1547_ZT.json"
