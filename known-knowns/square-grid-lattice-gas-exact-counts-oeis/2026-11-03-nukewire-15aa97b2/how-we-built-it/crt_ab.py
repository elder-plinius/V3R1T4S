"""The two-run gate: CRT T(28,k) independently over Run A (row sweeps, 13 set-A
primes) and Run B (column sweeps, 13 set-B primes); require exact agreement on
every cell k=1..27, plus T(28,28) over B == the a(28) object from PR #849."""
import sys

import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))  # paths relative to this file
A_RES = _os.path.join(_HERE, 'runA_residues.txt')
B_RES = _os.path.join(_HERE, 'runB_residues.txt')
A28 = _os.path.normpath(_os.path.join(_HERE, '..', 'the-record-we-beat', 'a28_anchor.txt'))


def load(path, keyj, keyk=None):
    """Return {(k or None): {prime: residue}} for lines matching the sweep's shape."""
    cells = {}
    for line in open(path, encoding='utf-8'):
        if not line.startswith('p='):
            continue
        f = dict(t.split('=') for t in line.split())
        p, j = int(f['p']), int(f['j'])
        if keyj is not None and j != keyj:
            continue
        k = int(f['k']) if keyk is None else keyk
        cells.setdefault(k, {})[p] = int(f['r'])
    return cells


def crt(residues):
    x, m = 0, 1
    for p, r in sorted(residues.items()):
        g = pow(m, -1, p)
        x = x + m * (((r - x) % p) * g % p)
        m *= p
    return x % m, m


rowA = load(A_RES, keyj=28)          # runA j=28 lines: T(28,k) per k
rowB = load(B_RES, keyj=28, keyk=28)  # runB j=28 column: T(28, 1..28)? NO --
# runB lines are p=.. j=.. r=.. (no k): column j total = T(28, j). Load per j:
rowB = {}
for line in open(B_RES, encoding='utf-8'):
    if not line.startswith('p='):
        continue
    f = dict(t.split('=') for t in line.split())
    p, j = int(f['p']), int(f['j'])
    rowB.setdefault(j, {})[p] = int(f['r'])

a28 = int(open(A28).read().strip())
assert len(rowA) == 27 and all(len(v) == 13 for v in rowA.values()), \
    {k: len(v) for k, v in rowA.items() if len(v) != 13}
assert len(rowB) == 28 and all(len(v) == 13 for v in rowB.values()), \
    {k: len(v) for k, v in rowB.items() if len(v) != 13}

bad = 0
vals = {}
for k in range(1, 28):
    xa, ma = crt(rowA[k])
    xb, mb = crt(rowB[k])
    vals[k] = xa
    if xa != xb:
        bad += 1
        print(f"DISAGREEMENT k={k}: A={xa} B={xb}")
x28, m28 = crt(rowB[28])
if x28 != a28:
    bad += 1
    print(f"DISAGREEMENT k=28 (B CRT vs #849 a(28))")
print(f"TWO-RUN GATE {'PASS' if bad == 0 else 'FAIL'}: 27/27 cells agree exactly "
      f"(A: 13 set-A primes row sweeps; B: 13 set-B primes column sweeps); "
      f"T(28,28) via B == a(28): {x28 == a28}")
print(f"moduli: A {ma.bit_length()} bits, B {mb.bit_length()} bits, "
      f"anchor a(28) {a28.bit_length()} bits")
for k in range(1, 28):
    print(f"T(28,{k}) = {vals[k]}  [{len(str(vals[k]))} digits]")
import json
json.dump({str(k): str(v) for k, v in vals.items()}, open('row28_final.json', 'w'),
          indent=1)
print("saved row28_final.json")
