#!/bin/sh
DIR="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
OBJ="$DIR/object/p2_240_planes_order5.txt"
VIY="$DIR/verify-it-yourself"

fail_out() {
    echo "FAIL"
    exit 1
}

if [ ! -f "$OBJ" ]; then
    echo "Missing object file"
    fail_out
fi

TMP_DIR=$(mktemp -d "${TMPDIR:-.}/v3_qfano.XXXXXX") || fail_out
cleanup() {
    rm -rf "$TMP_DIR"
}
trap cleanup EXIT INT TERM

CC_BIN="${CC:-cc}"
"$CC_BIN" -std=c99 -O2 -Wall -Wextra -Werror "$VIY/verify_p2_c.c" -o "$TMP_DIR/verify_p2_c" || fail_out

python3 "$VIY/verify_p2_py.py" "$OBJ" || fail_out
"$TMP_DIR/verify_p2_c" "$OBJ" || fail_out

python3 - "$OBJ" "$TMP_DIR" <<'PYEOF' || fail_out
import sys
obj_path, tdir = sys.argv[1], sys.argv[2]
base = open(obj_path).read().splitlines()

n1 = [" ".join("1" if r == c else "0" for c in range(7)) for r in range(7)] + base[7:]
open(f"{tdir}/neg1.txt", "w").write("\n".join(n1) + "\n")

n2 = base[:11] + base[8:11] + base[14:]
open(f"{tdir}/neg2.txt", "w").write("\n".join(n2) + "\n")

r0 = [int(x) for x in base[8].split()]
r1 = [int(x) for x in base[9].split()]
n3 = base[:10] + [" ".join(str(r0[c] ^ r1[c]) for c in range(7))] + base[11:]
open(f"{tdir}/neg3.txt", "w").write("\n".join(n3) + "\n")

f_rows = ["0 0 0 0 1 0 0", "0 0 0 0 0 1 0", "0 0 0 0 0 0 1"]
n4 = base[:8] + f_rows + base[11:]
open(f"{tdir}/neg4.txt", "w").write("\n".join(n4) + "\n")

disj_rows = ["1 0 0 0 0 0 0", "0 1 0 0 0 0 0", "0 0 1 0 0 0 0"]
n5 = base[:8] + disj_rows + base[11:]
open(f"{tdir}/neg5.txt", "w").write("\n".join(n5) + "\n")
PYEOF

for k in 1 2 3 4 5; do
    if python3 "$VIY/verify_p2_py.py" "$TMP_DIR/neg${k}.txt" >/dev/null 2>&1; then
        echo "Python verifier accepted negative control neg${k}"
        fail_out
    fi
    if "$TMP_DIR/verify_p2_c" "$TMP_DIR/neg${k}.txt" >/dev/null 2>&1; then
        echo "C99 verifier accepted negative control neg${k}"
        fail_out
    fi
done

echo "PASS"
exit 0
