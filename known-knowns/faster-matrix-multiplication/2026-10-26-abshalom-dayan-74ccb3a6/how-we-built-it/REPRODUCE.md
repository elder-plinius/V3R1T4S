# Reproduce

All commands run from this folder (`claim/`) in a fresh shell. Only `python3` (standard library) is needed for the
checks.

## 1. Check the object

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output (seconds to a few minutes on a laptop):

```
== exact Brent-equation check (check_scheme.py)
format <14,15,15>, 1836 terms, every term with three nonzero factors, common denominator 54400, 9922500 Brent equations checked, 0 wrong
rank 1836 scheme for <14,15,15> over Q verified exactly
PASS
== random exact evaluation against AB (check_random_eval.py)
trial 1: 0 of 210 entries of C differ from AB
trial 2: 0 of 210 entries of C differ from AB
trial 3: 0 of 210 entries of C differ from AB
PASS
PASS
```

File format (`object/u.txt`, `v.txt`, `w.txt`): header lines `# format 14 15 15` and `# rank 1836`, then one line
per term k = 0..1835 with the nonzero entries `index:coefficient` (integer or p/q) of that term's factor. Convention:
m_k = (sum u_k[i*15+j] A[i][j]) * (sum v_k[j*15+l] B[j][l]) for A 14x15, B 15x15, and C[i][l] = sum_k w_k[i*15+l] m_k.

sha256 of the object files:

```
74ccb3a6e497169b251b66cdfa494fd9b9c953105339c8e76b50f36f88c54a09  object/u.txt
0f86e47a9d787227caa9dbdfcdf5acd1f8694ab0d770fc9206f3df36658471ae  object/v.txt
cac452b54850e243944c0b26e24ea5c41b170e25976d418d2578941e506224b8  object/w.txt
```

## 2. Rebuild the object (optional; needs numpy and python-flint 0.9.0)

The input is LITA's published scheme, copied here as `rebuild/15x15x15_r1977.npz` (from
https://raw.githubusercontent.com/khoruzhii/lita/HEAD/schemes/15x15x15_r1977.npz; sha256
94515288f3079546e2c9f552bd246742ac45b2bc62b5aa908a9f491c44102a33, git blob sha1
65821484d954b4aade06cbda624932ba2a481f7b as listed in the LITA repository tree).

```sh
shasum -a 256 rebuild/15x15x15_r1977.npz
python3 rebuild/convert.py rebuild/15x15x15_r1977.npz lita_15.json
python3 rebuild/rebuild_slice.py lita_15.json rebuilt.json 1,1,1,1,1,1,1,-5,1,1,1,1,1,1,1 -1,1,1,1,1,1,1,1,1,1,1,1,1,1,1 5001 6
python3 rebuild/export_txt.py rebuilt.json rebuilt_txt
cmp rebuilt_txt/u.txt object/u.txt && cmp rebuilt_txt/v.txt object/v.txt && cmp rebuilt_txt/w.txt object/w.txt && echo identical
```

Expected: "parent <15,15,15> rank 1977", "slice axis 0 ... -> (14, 15, 15) rank 1865", "flat absorption removed 29 ->
rank 1836", "wrote 1836 terms", then `identical` (about 15 s).
