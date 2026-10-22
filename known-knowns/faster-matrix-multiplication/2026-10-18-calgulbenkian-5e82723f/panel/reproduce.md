context: Claude Code subagent, fresh context

# Reproduce report: ring-12x14x14-ZT-r1472

Role: reproduce. All paths below are relative to the package folder.

## Claim under test (quoted from the claim record, not shipped; the package README.md states the same values)
object/12x14x14_m1472_ZT.json is an explicit bilinear scheme of rank 1472 for the matrix multiplication format 12 x 14 x 14 in which every coefficient lies in {-1, 0, 1} (class ZT, "ternary"), and it satisfies the Brent equations exactly over Z; its rank 1472 is below the ZT rank 1484 listed for 12x14x14 in Perminov's live README table.

## Definition (quoted from the claim record, not shipped; RUN_IT_YOURSELF.md states the same index convention)
For a format n1 x n2 x n3 the scheme holds lists u, v, w of equal length (one entry per rank-one term). The checker
reads u[i*n2+j] as the coefficient of A[i][j], v[j*n3+l] as the coefficient of B[j][l], and w[l*n1+i] as the
coefficient of C[i][l], and tests, for all i, i2, j, j2, l, l2,
sum over terms t of u_t[i*n2+j] * v_t[j2*n3+l] * w_t[l2*n1+i2] = [j == j2] * [l == l2] * [i == i2].
Here n1 x n2 x n3 = 12 x 14 x 14, as in the object's "n" field.

I wrote my own checker (written from scratch, not shipped in this package) from this definition before opening verify-it-yourself/. It checks:
1. Integrity: every file against the contributor's hash list.
2. Format: the n field equals the format in the folder name, the m field and the lengths of u, v, w all equal the claimed rank, every row has length n1*n2 (u), n2*n3 (v), n3*n1 (w), every coefficient is a Python int (no float, no bool).
3. Coefficient class: maximum absolute coefficient and the number of coefficients outside {-1,0,1}; for a ZT claim every coefficient must be in {-1,0,1}.
4. Brent equations: for every (a,b,c), sum over terms of u[t][a]*v[t][b]*w[t][c] equals the identity tensor entry (1 exactly at a=(i,j), b=(j,l), c=(l,i), else 0). Computed for the full tensor (no sampling) with exact int64 matrix products; the checker first proves the bound rank*max|u|*max|v|*max|w| is below 2^63, so no overflow and no modular reduction or floating point is involved.
5. Calibration: the first nonzero w coefficient of term 0 was negated in a copy; the checker must reject it.

## Step 1: hash check (run in the package folder)
Command: shasum -a 256 -c on the contributor's hash list
Result: all files OK
```
INDEX.csv: OK
object/12x14x14_m1472_ZT.json: OK
verify-it-yourself/check_fmm_fast.py: OK
verify-it-yourself/RECEIPTS.md: OK
verify-it-yourself/run_checks.sh: OK
```

## Step 2: my checker on the object, then on the corrupted copy
Full output:
```
$ (own checker, run on object/12x14x14_m1472_ZT.json)
n field: [12, 14, 14] m field: 1472 keys: ['m', 'n', 'u', 'v', 'w']
terms: u 1472 v 1472 w 1472
max abs coeff: 1 coeffs outside {-1,0,1}: 0
terms with an all-zero factor: 0
per-entry sum bound: 1472 < 2^63: True
entries of tensor checked: 5531904 mismatching: 0
RESULT: EXACT BRENT OK rank 1472 class ZT
(exit 0)

$ (own checker, run on a corrupted copy: first nonzero w coefficient of term 0 negated)
n field: [12, 14, 14] m field: 1472 keys: ['m', 'n', 'u', 'v', 'w']
terms: u 1472 v 1472 w 1472
max abs coeff: 1 coeffs outside {-1,0,1}: 0
terms with an all-zero factor: 0
per-entry sum bound: 1472 < 2^63: True
entries of tensor checked: 5531904 mismatching: 36
RESULT: BRENT FAIL rank 1472 class ZT
(exit 1)
```

## Step 3: the author's run_checks.sh (run only after step 2), from a private copy of the package
Command: sh verify-it-yourself/run_checks.sh
```
sha256 matches INDEX.csv (0cebed78a0b198d25f02ba2e7b6960bb4b83cc57c41f4f35e6501d8f731cd006)
== check_fmm_fast.py: exact Brent equations over Z, rank 1472, coefficient class ZT
coefficient class: ZT (max |coefficient| = 1; ZT means all coefficients in {-1, 0, 1})
exact integer check: D=1 (DU=1, DV=1, DW=1), coefficient bound 11 bits, slot width 13 bits, 32928 blocks of 168 slots compared
PASS format=12x14x14 rank=1472
== negative control: a copy with the first nonzero coefficient of u[0] negated must FAIL
FAIL format=12x14x14 rank=1472: 12 of 32928 (a, b) blocks differ; first at A[6][3] x B[0][0]
negative control rejected as expected
ALL CHECKS PASS
```
(exit 0)

## Comparison
My checker and the author's checker agree: both report the exact Brent equations hold over Z, with the same rank and coefficient class. The author's checker uses a different method (packed big-integer slots), mine uses sparse-free int64 matrix products with a proven overflow bound, so the agreement is between independent implementations. Both reject a corrupted copy. Mismatches: none.

Scope: this report covers only reproduction of the saved object (validity, rank, coefficient class). It does not judge the table value or novelty.

pass: true
