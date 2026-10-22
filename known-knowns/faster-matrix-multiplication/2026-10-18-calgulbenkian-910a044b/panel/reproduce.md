context: Claude Code subagent, fresh context

# Reproduce report: ring-9x12x16-Z-r1065

Role: reproduce. All paths below are relative to the package folder.

## Claim under test (quoted from the claim record, not shipped; the package README.md states the same values)
object/9x12x16_m1065_Z.json is an explicit bilinear scheme of rank 1065 for the matrix multiplication format 9 x 12 x 16 in which every coefficient is an integer (class Z, not ternary; the largest absolute coefficient is in the checker output in verify-it-yourself/RECEIPTS.md), and it satisfies the Brent equations exactly over Z; its rank 1065 is below the Z rank 1074 listed for 9x12x16 in Perminov's live README table.

## Definition (quoted from the claim record, not shipped; RUN_IT_YOURSELF.md states the same index convention)
For a format n1 x n2 x n3 the scheme holds lists u, v, w of equal length (one entry per rank-one term). The checker
reads u[i*n2+j] as the coefficient of A[i][j], v[j*n3+l] as the coefficient of B[j][l], and w[l*n1+i] as the
coefficient of C[i][l], and tests, for all i, i2, j, j2, l, l2,
sum over terms t of u_t[i*n2+j] * v_t[j2*n3+l] * w_t[l2*n1+i2] = [j == j2] * [l == l2] * [i == i2].
Here n1 x n2 x n3 = 9 x 12 x 16, as in the object's "n" field.

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
object/9x12x16_m1065_Z.json: OK
verify-it-yourself/check_fmm_fast.py: OK
verify-it-yourself/RECEIPTS.md: OK
verify-it-yourself/run_checks.sh: OK
```

## Step 2: my checker on the object, then on the corrupted copy
Full output:
```
$ (own checker, run on object/9x12x16_m1065_Z.json)
n field: [9, 12, 16] m field: 1065 keys: ['m', 'n', 'u', 'v', 'w']
terms: u 1065 v 1065 w 1065
max abs coeff: 3 coeffs outside {-1,0,1}: 2860
terms with an all-zero factor: 0
per-entry sum bound: 9585 < 2^63: True
entries of tensor checked: 2985984 mismatching: 0
RESULT: EXACT BRENT OK rank 1065 class Z
(exit 0)

$ (own checker, run on a corrupted copy: first nonzero w coefficient of term 0 negated)
n field: [9, 12, 16] m field: 1065 keys: ['m', 'n', 'u', 'v', 'w']
terms: u 1065 v 1065 w 1065
max abs coeff: 3 coeffs outside {-1,0,1}: 2860
terms with an all-zero factor: 0
per-entry sum bound: 9585 < 2^63: True
entries of tensor checked: 2985984 mismatching: 135
RESULT: BRENT FAIL rank 1065 class Z
(exit 1)
```

## Step 3: the author's run_checks.sh (run only after step 2), from a private copy of the package
Command: sh verify-it-yourself/run_checks.sh
```
sha256 matches INDEX.csv (910a044b4fccb5ea250be0894c8e4a40947f31989b04c39e1cb34d31bbbc9e6a)
== check_fmm_fast.py: exact Brent equations over Z, rank 1065, coefficient class Z
coefficient class: Z (max |coefficient| = 3; ZT means all coefficients in {-1, 0, 1})
exact integer check: D=1 (DU=1, DV=1, DW=1), coefficient bound 11 bits, slot width 13 bits, 20736 blocks of 144 slots compared
PASS format=9x12x16 rank=1065
== negative control: a copy with the first nonzero coefficient of u[0] negated must FAIL
FAIL format=9x12x16 rank=1065: 5 of 20736 (a, b) blocks differ; first at A[1][3] x B[0][6]
negative control rejected as expected
ALL CHECKS PASS
```
(exit 0)

## Comparison
My checker and the author's checker agree: both report the exact Brent equations hold over Z, with the same rank and coefficient class. The author's checker uses a different method (packed big-integer slots), mine uses sparse-free int64 matrix products with a proven overflow bound, so the agreement is between independent implementations. Both reject a corrupted copy. Mismatches: none.

Scope: this report covers only reproduction of the saved object (validity, rank, coefficient class). It does not judge the table value or novelty.

pass: true
