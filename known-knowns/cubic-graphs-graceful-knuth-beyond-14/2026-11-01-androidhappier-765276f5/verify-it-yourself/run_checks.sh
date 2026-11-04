#!/bin/sh
# Run from the package folder:  sh verify-it-yourself/run_checks.sh
# Verifies the graceful-labeling certificates of connected cubic graphs pinned in object/CERTIFICATES.txt.
# Orders 4..20 ship in this package; order 22 is checked too if large-files/cert_22.txt.gz (or the uncompressed
# large-files/cert_22.txt) is present, see RUN_IT_YOURSELF.md.
# Needs python3 (standard library only). Optional extras: a C compiler (cc) runs the C per-line checker checkK.c;
# NAUTY_BIN=folder-with-geng-and-labelg additionally regenerates each order with geng and matches canonical forms.
# The last output line is PASS or FAIL.
MANIFEST=object/CERTIFICATES.txt
WANT=765276f52743141c9fa508cbe9558c8cd2814e5a7e4711e8992fd5f57d985ffc
ok=1
W=$(mktemp -d)
trap 'rm -rf "$W"' EXIT

echo "== 1. sha256 of $MANIFEST"
GOT=$(python3 -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" "$MANIFEST")
echo "got  $GOT"; echo "want $WANT"
if [ "$GOT" = "$WANT" ]; then echo "manifest sha256: match"; else echo "manifest sha256: MISMATCH"; ok=0; fi

echo "== 2. reassemble the certificates; check sha256 and size of the .gz and of the uncompressed text"
python3 - "$MANIFEST" "$W" <<'PY' > "$W/orders.txt"
import glob, gzip, hashlib, os, shutil, sys
man, out = sys.argv[1], sys.argv[2]
bad = 0
def digest(path, gz=False):
    h, size = hashlib.sha256(), 0
    with (gzip.open(path, 'rb') if gz else open(path, 'rb')) as f:
        while True:
            b = f.read(1 << 20)
            if not b:
                return h.hexdigest(), size
            h.update(b); size += len(b)
for line in open(man):
    if line.startswith('#') or not line.strip():
        continue
    gh, gsize, name, where, th, tsize = line.split()
    n = int(name.split('_')[1].split('.')[0])
    dst = os.path.join(out, name)
    if where == 'in-package':
        single = os.path.join('object', 'certs', name)
        parts = [single] if os.path.isfile(single) else sorted(glob.glob(single + '.part*'))
        if not parts:
            sys.stderr.write('%s: MISSING from the package\n' % name); bad += 1; continue
        with open(dst, 'wb') as o:
            for p in parts:
                o.write(open(p, 'rb').read())
        src, gz, label = dst, True, '%d part(s)' % len(parts)
    else:
        gzp, txt = os.path.join('large-files', name), os.path.join('large-files', name[:-3])
        if os.path.isfile(gzp):
            src, gz, label, parts = gzp, True, 'large-files', [gzp]
        elif os.path.isfile(txt):
            src, gz, label, parts = txt, False, 'large-files, uncompressed', None
        else:
            sys.stderr.write('%s: not present (external file, order %d not checked here)\n' % (name, n)); continue
    if parts is not None:
        h, s = digest(src)
        if h != gh or s != int(gsize):
            sys.stderr.write('%s: gzip sha256/size MISMATCH (got %s, %d bytes)\n' % (name, h, s)); bad += 1; continue
    h, s = digest(src, gz)
    if h != th or s != int(tsize):
        sys.stderr.write('%s: uncompressed sha256/size MISMATCH (got %s, %d bytes)\n' % (name, h, s)); bad += 1; continue
    if src != dst:
        os.symlink(os.path.abspath(src), os.path.join(out, 'cert_%d.src' % n))
    else:
        os.rename(dst, os.path.join(out, 'cert_%d.src' % n))
    sys.stderr.write('%s: sha256 match (%s; text %d bytes, sha256 %s...)\n' % (name, label, s, th[:16]))
    print('%d %s' % (n, 'gz' if gz else 'txt'))
sys.exit(1 if bad else 0)
PY
[ $? -eq 0 ] || ok=0
ORDERS=$(cut -d' ' -f1 "$W/orders.txt" | tr '\n' ' ')
echo "orders available: $ORDERS"
[ -n "$ORDERS" ] || ok=0
# give every available certificate a name the checker understands (.gz or plain)
while read n kind; do
  if [ "$kind" = gz ]; then ln -s "$W/cert_$n.src" "$W/cert_$n.txt.gz"; echo "$W/cert_$n.txt.gz"; else ln -s "$W/cert_$n.src" "$W/cert_$n.txt"; echo "$W/cert_$n.txt"; fi > "$W/path_$n"
done < "$W/orders.txt"

echo "== 3. Python checker (check_graceful_cubic.py, standard library): every line, exact canonical forms, A002851"
for n in $ORDERS; do
  python3 verify-it-yourself/check_graceful_cubic.py $n "$(cat "$W/path_$n")" || ok=0
done

echo "== 4. controls: damaged copies of the order-10 certificate must FAIL"
if [ -f "$W/path_10" ]; then
python3 - "$(cat "$W/path_10")" "$W" <<'PY'
import gzip, os, random, sys
lines = gzip.open(sys.argv[1], 'rt').read().splitlines(True)
out, n = sys.argv[2], 10
p = lines[0].split()
s = p[0]; bits = []
for ch in s[1:]:
    bits += [((ord(ch) - 63) >> b) & 1 for b in range(5, -1, -1)]
pairs = [(i, j) for j in range(1, n) for i in range(j)]
edges = [pairs[k] for k in range(len(pairs)) if bits[k]]
# two labels swapped: the first pair (i, j) whose swap breaks the difference set
for i, j in pairs:
    lab = [int(x) for x in p[1:]]; lab[i], lab[j] = lab[j], lab[i]
    if set(abs(lab[a] - lab[b]) for a, b in edges) != set(range(1, 16)):
        break
bad1 = lines[:]; bad1[0] = ' '.join([p[0]] + [str(x) for x in lab]) + '\n'
bad2 = lines[:-1]                                                 # one graph missing
bad3 = lines[:-1] + [lines[0]]                                    # one graph missing, one repeated verbatim
# one graph missing, replaced by a relabelled (isomorphic, still gracefully labelled) copy of another
perm = list(range(n)); random.Random(7).shuffle(perm)
new = set((min(perm[a], perm[b]), max(perm[a], perm[b])) for a, b in edges)
nb = [1 if pr in new else 0 for pr in pairs]; nb += [0] * (-len(nb) % 6)
g6 = chr(63 + n) + ''.join(chr(63 + int(''.join(map(str, nb[i:i + 6])), 2)) for i in range(0, len(nb), 6))
f = [0] * n
for v in range(n):
    f[perm[v]] = p[1 + v]
bad4 = lines[:-1] + [' '.join([g6] + f) + '\n']
for i, L in enumerate((bad1, bad2, bad3, bad4), 1):
    open(os.path.join(out, 'control%d.txt' % i), 'w').write(''.join(L))
PY
for i in 1 2 3 4; do
  if python3 verify-it-yourself/check_graceful_cubic.py 10 "$W/control$i.txt"; then echo "control $i: unexpected PASS"; ok=0; else echo "control $i: FAIL as expected"; fi
done
else
  echo "order-10 certificate not available"; ok=0
fi

echo "== 5. optional second checker (checkK.c, C, per-line) and nauty coverage (NAUTY_BIN)"
if command -v cc >/dev/null 2>&1 && cc -O2 -o "$W/checkK" verify-it-yourself/checkK.c 2>/dev/null; then
  for n in $ORDERS; do
    python3 -c "import gzip,sys,shutil;f=sys.argv[1];shutil.copyfileobj(gzip.open(f) if f.endswith('.gz') else open(f,'rb'),sys.stdout.buffer)" "$(cat "$W/path_$n")" \
      | "$W/checkK" $n > "$W/g6_$n.txt" 2> "$W/k.err"; rc=$?
    cat "$W/k.err"; [ $rc -eq 0 ] || ok=0
  done
  if "$W/checkK" 10 < "$W/control1.txt" > /dev/null 2>&1; then echo "checkK control (swapped labels): unexpected PASS"; ok=0; else echo "checkK control (swapped labels): FAIL as expected"; fi
  if [ -n "$NAUTY_BIN" ] && [ -x "$NAUTY_BIN/geng" ] && [ -x "$NAUTY_BIN/labelg" ]; then
    for n in $ORDERS; do
      "$NAUTY_BIN/labelg" -q "$W/g6_$n.txt" | LC_ALL=C sort > "$W/c.can"
      seq 0 15 | xargs -P ${PAR:-4} -I{} sh -c "\"$NAUTY_BIN/geng\" -cq -d3 -D3 $n {}/16 | \"$NAUTY_BIN/labelg\" -q > \"$W/gen_{}.can\""
      cat "$W"/gen_*.can | LC_ALL=C sort > "$W/g.can"; rm -f "$W"/gen_*.can
      if cmp -s "$W/c.can" "$W/g.can" && [ -z "$(uniq -d "$W/c.can")" ]; then echo "nauty coverage order $n: $(wc -l < "$W/g.can") geng graphs = certificate graphs, no duplicates"; else echo "nauty coverage order $n: MISMATCH"; ok=0; fi
    done
  else
    echo "NAUTY_BIN not set: nauty coverage skipped (the Python checker's canonical forms decide completeness)"
  fi
else
  echo "no C compiler found; checkK skipped (the Python checker alone decides)"
fi

echo "== summary: orders checked: $ORDERS"
if [ $ok -eq 1 ]; then echo PASS; exit 0; else echo FAIL; exit 1; fi
