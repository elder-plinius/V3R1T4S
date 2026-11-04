# Reproduce

All commands run from this folder (`claim/`) in a fresh shell. Only `python3` (standard library) is needed for the
checks.

## 1. Check the object

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output (about 7 seconds on a laptop):

```
== exact Brent-equation check (check_scheme.py)
format <12,13,13>, 1270 terms, every term with three nonzero factors, common denominator 59904, 4112784 Brent equations checked, 0 wrong
rank 1270 scheme for <12,13,13> over Q verified exactly
PASS
== random exact evaluation against AB (check_random_eval.py)
trial 1: 0 of 156 entries of C differ from AB
trial 2: 0 of 156 entries of C differ from AB
trial 3: 0 of 156 entries of C differ from AB
PASS
PASS
```

File format (`object/u.txt`, `v.txt`, `w.txt`): header lines `# format 12 13 13` and `# rank 1270`, then one line
per term k = 0..1269 with the nonzero entries `index:coefficient` of that term's factor. Convention:
m_k = (sum u_k[i*13+j] A[i][j]) * (sum v_k[j*13+l] B[j][l]) for A 12x13, B 13x13, and C[i][l] = sum_k w_k[i*13+l] m_k.

sha256 of the object files:

```
d08b64bbd70b1059b87528ba8e988f57a7f20293d181168a2083380b810d4690  object/u.txt
a1c142447b30847fe70f7f0dc7aa638665c313efdab236f9ede41b10c04eadaf  object/v.txt
8180074e608df407ce136e21ed42797fb7071b28691182e034dab6bb84feaf58  object/w.txt
```

## 2. Rebuild the object (optional; needs numpy and python-flint 0.9.0)

Here `python3` means a Python that has numpy and python-flint 0.9.0 installed (for example a virtual environment);
section 1 needs only the standard library.

The input is LITA's published scheme, copied here as `rebuild/13x13x13_r1379.npz` (from
https://raw.githubusercontent.com/khoruzhii/lita/HEAD/schemes/13x13x13_r1379.npz; sha256
9df0b464793e3c9584c9e95e48dc748a4774afa07bd1b7aa7e6d4421570b40eb, git blob sha1
bc0840bbda26c63915d242360fcc56a7c0e4047b as listed in the LITA repository tree).

```sh
shasum -a 256 rebuild/13x13x13_r1379.npz
python3 rebuild/convert.py rebuild/13x13x13_r1379.npz lita_13.json
python3 rebuild/rebuild_12x13x13.py lita_13.json rebuilt.json 1,1,1,1,1,1,-4,1,1,1,1,1,1 -1,1,1,1,1,1,1,1,1,1,1,1,1 5001 6
python3 rebuild/export_txt.py rebuilt.json rebuilt/
cmp rebuilt/u.txt object/u.txt && cmp rebuilt/v.txt object/v.txt && cmp rebuilt/w.txt object/w.txt && echo SAME
```

`rebuild_12x13x13.py` prints `slice axis 0 with e=1,1,1,1,1,1,-4,1,1,1,1,1,1 f=-1,1,1,1,1,1,1,1,1,1,1,1,1 -> (12, 13, 13)
rank 1295` and `flat absorption removed 25 -> rank 1270` (about 8 seconds), and the comparison prints SAME.
The slice (axis 0, the row index i shared by A and C) maps every term's A factor through E^T and its C factor
through F^T, where the columns of E span the vectors orthogonal to e, the columns of F span the vectors orthogonal
to f, and E^T F = I; terms whose A factor is e x^T or whose C factor is f y^T vanish. The absorption step finds exact
linear dependencies among the terms (kernel vectors of a pairing of two factor types, verified exactly over Q) and
removes terms by shifting the third factor; it is seeded (seed 5001), so the result is deterministic.
