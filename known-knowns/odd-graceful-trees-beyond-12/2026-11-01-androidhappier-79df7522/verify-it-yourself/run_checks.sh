#!/bin/sh
# Run from the package folder:  sh verify-it-yourself/run_checks.sh
# Verifies the odd-graceful certificates in object/ (orders 2..20 ship in this package; orders 21 and 22 are
# checked too if their files are placed in large-files/, see RUN_IT_YOURSELF.md).
# Needs python3 (standard library only). If a C compiler (cc) is present, a second checker (ogcheck.c), which
# regenerates every tree by leaf addition, is also run. The last output line is PASS or FAIL.
MANIFEST=object/CERTIFICATES.txt
WANT=79df75225a75f48b971b2e7ea2a91e325a129d836720df7542d056dfed2971af
ok=1
W=$(mktemp -d)
trap 'rm -rf "$W"' EXIT

echo "== 1. sha256 of $MANIFEST"
GOT=$(python3 -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" "$MANIFEST")
echo "got  $GOT"; echo "want $WANT"
if [ "$GOT" = "$WANT" ]; then echo "manifest sha256: match"; else echo "manifest sha256: MISMATCH"; ok=0; fi

echo "== 2. reassemble the certificates and check each sha256 and size against $MANIFEST"
python3 - "$MANIFEST" "$W" <<'PY' > "$W/orders.txt"
import glob, hashlib, os, sys
man, out = sys.argv[1], sys.argv[2]
bad = 0
for line in open(man):
    if line.startswith('#') or not line.strip():
        continue
    h, size, name, where = line.split()
    n = int(name.split('_')[1].split('.')[0])
    if where == 'in-package':
        parts = [os.path.join('object', 'certs', name)] if os.path.isfile(os.path.join('object', 'certs', name)) \
            else sorted(glob.glob(os.path.join('object', 'certs', name + '.part*')))
    else:
        parts = [os.path.join('large-files', name)] if os.path.isfile(os.path.join('large-files', name)) else []
    if not parts:
        if where == 'in-package':
            sys.stderr.write('%s: MISSING from the package\n' % name); bad += 1
        else:
            sys.stderr.write('%s: not present (external file, order %d not checked here)\n' % (name, n))
        continue
    data = b''.join(open(p, 'rb').read() for p in parts)
    got = hashlib.sha256(data).hexdigest()
    if got != h or len(data) != int(size):
        sys.stderr.write('%s: sha256/size MISMATCH (got %s, %d bytes)\n' % (name, got, len(data))); bad += 1
        continue
    open(os.path.join(out, name), 'wb').write(data)
    sys.stderr.write('%s: sha256 match (%d part(s), %d bytes)\n' % (name, len(parts), len(data)))
    print(n)
sys.exit(1 if bad else 0)
PY
[ $? -eq 0 ] || ok=0
ORDERS=$(tr -d '\r' < "$W/orders.txt" | tr '\n' ' ')
echo "orders available: $ORDERS"
[ -n "$ORDERS" ] || ok=0

echo "== 3. Python checker (check_odd_graceful.py, standard library): every line of every available certificate"
for n in $ORDERS; do
  python3 verify-it-yourself/check_odd_graceful.py $n "$W/cert_$n.txt.gz" || ok=0
done

echo "== 4. controls: damaged copies of the order-13 certificate must FAIL"
python3 - "$W/cert_13.txt.gz" "$W" <<'PY'
import gzip, os, sys
lines = gzip.open(sys.argv[1], 'rt').read().splitlines(True)
out = sys.argv[2]
a, b = lines[0].split('|'); lab = b.split(); lab[0], lab[-1] = lab[-1], lab[0]
bad1 = lines[:]; bad1[0] = a + '| ' + ' '.join(lab) + '\n'          # two labels swapped
bad2 = lines[:-1]                                                   # one tree missing
bad3 = lines[:-1] + [lines[0]]                                      # one tree missing, one duplicated
for i, L in enumerate((bad1, bad2, bad3), 1):
    open(os.path.join(out, 'control%d.txt' % i), 'w').write(''.join(L))
PY
for i in 1 2 3; do
  if python3 verify-it-yourself/check_odd_graceful.py 13 "$W/control$i.txt"; then echo "control $i: unexpected PASS"; ok=0; else echo "control $i: FAIL as expected"; fi
done

echo "== 5. second checker (ogcheck.c, C): regenerates all trees of order n by leaf addition and matches the certificate"
# A000055(n), n = 2..22 (OEIS A000055); the regenerated count must equal it.
T="2:1 3:1 4:2 5:3 6:6 7:11 8:23 9:47 10:106 11:235 12:551 13:1301 14:3159 15:7741 16:19320 17:48629 18:123867 19:317955 20:823065 21:2144505 22:5623756"
if command -v cc >/dev/null 2>&1; then
  if cc -O2 -fopenmp -o "$W/ogcheck" verify-it-yourself/ogcheck.c 2>/dev/null || cc -O2 -o "$W/ogcheck" verify-it-yourself/ogcheck.c; then
    for n in $ORDERS; do
      want=$(echo "$T" | tr ' ' '\n' | grep "^$n:" | cut -d: -f2)
      python3 -c "import gzip,sys,shutil;shutil.copyfileobj(gzip.open(sys.argv[1]),sys.stdout.buffer)" "$W/cert_$n.txt.gz" > "$W/c.txt"
      "$W/ogcheck" $n "$W/c.txt" 2>/dev/null > "$W/og.raw"; rc=$?
      tr -d '\r' < "$W/og.raw" > "$W/og.out"
      cat "$W/og.out"
      reg=$(sed -n 's/^order [0-9]*: regenerated \([0-9]*\) trees$/\1/p' "$W/og.out")
      if [ $rc -ne 0 ] || ! grep -q "^PASS order $n$" "$W/og.out" || [ "$reg" != "$want" ]; then echo "ogcheck order $n: FAIL (regenerated $reg, A000055 $want)"; ok=0; else echo "ogcheck order $n: regenerated $reg = A000055($n)"; fi
      rm -f "$W/c.txt"
    done
    if "$W/ogcheck" 13 "$W/control1.txt" >/dev/null 2>&1; then echo "ogcheck control: unexpected PASS"; ok=0; else echo "ogcheck control (swapped labels): FAIL as expected"; fi
  else
    echo "compile failed"; ok=0
  fi
else
  echo "no C compiler found; second checker skipped (the Python checker alone decides)"
fi

echo "== summary: orders checked: $ORDERS"
if [ $ok -eq 1 ]; then echo PASS; exit 0; else echo FAIL; exit 1; fi
