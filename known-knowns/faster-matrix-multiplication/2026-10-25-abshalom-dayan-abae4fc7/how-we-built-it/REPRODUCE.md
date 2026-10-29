# Reproduce

All commands run from this folder (`claim/`) in a fresh shell. Only `python3` (standard library) is needed for the
checks.

## 1. Check the object

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output (about 4 minutes on a laptop; the exact Brent-equation check is the slow part):

```
== exact Brent-equation check (check_scheme.py)
format <14,14,15>, 1709 terms, every term with three nonzero factors, common denominator 2121600, 8643600 Brent equations checked, 0 wrong
rank 1709 scheme for <14,14,15> over Q verified exactly
PASS
== random exact evaluation against AB (check_random_eval.py)
trial 1: 0 of 210 entries of C differ from AB
trial 2: 0 of 210 entries of C differ from AB
trial 3: 0 of 210 entries of C differ from AB
PASS
PASS
```

File format (`object/u.txt`, `v.txt`, `w.txt`): header lines `# format 14 14 15` and `# rank 1709`, then one line
per term k = 0..1708 with the nonzero entries `index:coefficient` of that term's factor. Convention:
m_k = (sum u_k[i*14+j] A[i][j]) * (sum v_k[j*15+l] B[j][l]) for A 14x14, B 14x15, and C[i][l] = sum_k w_k[i*15+l] m_k.

sha256 of the object files:

```
abae4fc7429a9c3b715405717c52e2dfcd36ab0f41cd137f3e1327252b1ff56e  object/u.txt
a05bcf35e2018bde9600457e4776483969b8b6c0de6c3a1463847f8ca3ae08bb  object/v.txt
041992e80c316daa766acecffae71c0c7839fa5f189c77365109f2e63fe7c32d  object/w.txt
```

## 2. Rebuild the object (optional; needs numpy and python-flint 0.9.0)

The input is LITA's published scheme, copied here as `rebuild/15x15x15_r1977.npz` (from
https://raw.githubusercontent.com/khoruzhii/lita/HEAD/schemes/15x15x15_r1977.npz; sha256
94515288f3079546e2c9f552bd246742ac45b2bc62b5aa908a9f491c44102a33, git blob sha1
65821484d954b4aade06cbda624932ba2a481f7b as listed in the LITA repository tree).

```sh
shasum -a 256 rebuild/15x15x15_r1977.npz
python3 rebuild/convert.py rebuild/15x15x15_r1977.npz lita_15.json
python3 rebuild/rebuild_chain.py lita_15.json rebuilt.json \
  0/1,1,1,1,1,1,1,-5,1,1,1,1,1,1,1/-1,1,1,1,1,1,1,1,1,1,1,1,1,1,1/5001/6 \
  1/1,1,1,1,1,1,1,-5,1,1,1,1,1,1,1/1,1,1,1,1,1,1,-5,1,1,1,1,1,1,1/1030/6
python3 rebuild/export_txt.py rebuilt.json rebuilt/
cmp rebuilt/u.txt object/u.txt && cmp rebuilt/v.txt object/v.txt && cmp rebuilt/w.txt object/w.txt && echo SAME
```

`rebuild_chain.py` prints (about 1 minute):

```
parent <15,15,15> rank 1977
step 1: slice axis 0 with e=1,1,1,1,1,1,1,-5,1,1,1,1,1,1,1 f=-1,1,1,1,1,1,1,1,1,1,1,1,1,1,1 -> (14, 15, 15) rank 1865
step 1: flat absorption (seed 5001, restarts 6) removed 29 -> rank 1836
step 2: slice axis 1 with e=1,1,1,1,1,1,1,-5,1,1,1,1,1,1,1 f=1,1,1,1,1,1,1,-5,1,1,1,1,1,1,1 -> (14, 14, 15) rank 1731
step 2: flat absorption (seed 1030, restarts 6) removed 22 -> rank 1709
```

and the comparison prints SAME.

What the steps do. A slice on axis 0 (the row index i shared by A and C) maps every term's A factor through E^T and
its C factor through F^T; a slice on axis 1 (the inner index j shared by A and B) maps every term's A factor through
E on the right and its B factor through F^T on the left. Here the columns of E span the vectors orthogonal to e, the
columns of F span the vectors orthogonal to f, and E^T F = I, so the restricted scheme computes the smaller product
exactly; terms whose e-side factor has the form e x^T (or x e^T) or whose f-side factor has the form f y^T vanish.
The absorption step finds exact linear dependencies among the terms (kernel vectors of a pairing of two factor
types, verified exactly over Q) and removes terms by shifting the third factor. It is seeded (seeds 5001 and 1030),
so the result is deterministic.
