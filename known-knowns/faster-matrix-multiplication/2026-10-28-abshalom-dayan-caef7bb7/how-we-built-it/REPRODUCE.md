# Reproduce

All commands run from this folder (`claim/`) in a fresh shell. Only `python3` (standard library) is needed for the
checks.

## 1. Check the object

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output (about 10 s on a laptop):

```
== exact Brent-equation check (check_scheme.py)
format <14,15,13>, 1644 terms, every term with three nonzero factors, common denominator 54400, 7452900 Brent equations checked, 0 wrong
rank 1644 scheme for <14,15,13> over Q verified exactly
PASS
== random exact evaluation against AB (check_random_eval.py)
trial 1: 0 of 182 entries of C differ from AB
trial 2: 0 of 182 entries of C differ from AB
trial 3: 0 of 182 entries of C differ from AB
PASS
PASS
```

File format (`object/u.txt`, `v.txt`, `w.txt`): header lines `# format 14 15 13` and `# rank 1644`, then one line
per term k = 0..1643 with the nonzero entries `index:coefficient` (integer or p/q) of that term's factor. Convention:
m_k = (sum u_k[i*15+j] A[i][j]) * (sum v_k[j*13+l] B[j][l]) for A 14x15, B 15x13, and C[i][l] = sum_k w_k[i*13+l] m_k.

sha256 of the object files:

```
caef7bb7a2974dc44dee7feb61779a52d00b0473b7b416069c7f0e0d11d7e8cd  object/u.txt
b31e5e77899a5ec44a8922eb49963ccc8babf8e84368a47b2c92d89dd9aa6616  object/v.txt
79b90daf911f392ccde5cf5abed5400b207ed04980ad392d7c4c9028d20a7da1  object/w.txt
```

## 2. Rebuild the object (optional; needs numpy and python-flint 0.9.0)

The input is LITA's published scheme, copied here as `rebuild/15x15x15_r1977.npz` (from
https://raw.githubusercontent.com/khoruzhii/lita/HEAD/schemes/15x15x15_r1977.npz; sha256
94515288f3079546e2c9f552bd246742ac45b2bc62b5aa908a9f491c44102a33, git blob sha1
65821484d954b4aade06cbda624932ba2a481f7b as listed in the LITA repository tree).

```sh
PY=<python with numpy and flint> sh rebuild/run_rebuild.sh
```

Expected (about 35 s):

```
94515288f3079546e2c9f552bd246742ac45b2bc62b5aa908a9f491c44102a33  ../../data/lita/15x15x15_r1977.npz
parent <15,15,15> rank 1977
axis 0 e=1,1,1,1,1,1,1,-5,1,1,1,1,1,1,1 f=-1,1,1,1,1,1,1,1,1,1,1,1,1,1,1: slice -> (14, 15, 15) rank 1865; flat absorption seed 5001 removed 29 -> rank 1836
axis 2 e=1,0,0,0,0,0,0,0,0,0,0,0,0,0,0 f=1,1,1,1,1,1,1,-5,1,1,1,1,1,1,1: slice -> (14, 15, 14) rank 1709; flat absorption seed 1000 removed 0 -> rank 1709
axis 2 e=0,0,1,0,0,0,0,-1,0,0,0,0,0,0 f=0,0,1,0,0,0,0,0,0,0,1,0,0,0: slice -> (14, 15, 13) rank 1677; flat absorption seed 1008 removed 33 -> rank 1644
wrote 1644 terms to ...
u.txt identical
v.txt identical
w.txt identical
```

## 3. Known positive (optional)

`the-record-we-beat/13x14x15_r1645_Q.json` is the merged 1645 scheme (pull request #166) in this repository's
known-knowns encoding (vocab_rle_v1: comma-separated indices into "vocab", "i*k" = index i repeated k times; w index
l*n1+i). Decoding it to the text format above and running the same checkers gives PASS with 1645 terms.
