context: Claude Code subagent, fresh context [Sonnet 5.5]

# Reproduce report: object/bb504_logical_wt28.txt (p1 of bivariate-bicycle-exact-distance-360-756)

## Definition checked against
"Build H_X and H_Z from (l, m, A, B) as 0/1 block-circulant matrices. Check H_X H_Z^T = 0 mod 2 and k = n - rank H_X - rank H_Z (12 or 16). For a witness u, check H_X u = 0, check that u is not in the row space of H_Z (rank test), and count its weight."
Also: "x and y, the commuting cyclic shifts on Z_l x Z_m; A = A1+A2+A3 and B = B1+B2+B3; H_X = [A|B] and H_Z = [B^T|A^T]." Claim parameters: l=42, m=6, A = x^27+y+y^2, B = y^3+x^37+x^38, n=504, k=12, weight 28.

## My checker
Written before opening the author's code. Pure-Python GF(2) with bit-integers, run with python -I. Qubit (i,j) is x^i y^j, i in Z_42, j in Z_6; each block has 252 qubits. The witness holds 28 distinct indices in 0..503 (min 7, max 489); its sha256 matches the claim (2894986d...0f878). 12 indices fall in the first block, 16 in the second.

Exact output, four conventions tried:
```
idx=i*m+j orth True n 504 rkHX 246 rkHZ 246 k 12
  H_X u=0: False  in rowspace(H_Z): False  weight 28
idx=j*l+i orth True n 504 rkHX 246 rkHZ 246 k 12
  H_X u=0: False  in rowspace(H_Z): False  weight 28
idx=i*m+j, inverse shifts orth True n 504 rkHX 246 rkHZ 246 k 12
  H_X u=0: True  in rowspace(H_Z): False  weight 28
idx=j*l+i, inverse shifts orth True n 504 rkHX 246 rkHZ 246 k 12
  H_X u=0: False  in rowspace(H_Z): False  weight 28
```

## Findings
- Code parameters: in every convention H_X H_Z^T = 0, n = 504, rank H_X = rank H_Z = 246, k = 12. Matches the claim.
- First convention failed: my first convention (matrix of x^a sends qubit p to p+a in row p) did not satisfy H_X u = 0, nor did the swapped indexing (j*l+i).
- Convention that passes: qubit index i*m+j (shift acts on the l-index) with the inverse shift direction. There H_X u = 0, u is not in the row space of H_Z, weight 28.
- Why the relabelling is harmless: the inverse-shift matrix of x^a is the transpose of my first one. Let P be the qubit permutation (i,j) -> (-i,-j) on both blocks; P S_a P^-1 = S_-a, so it maps one convention's H_X and H_Z onto the other's. The codes are identical up to a qubit permutation; weights, n, k, ranks are preserved and logicals map to logicals of equal weight. So the witness, read in the correct convention, is a genuine weight-28 Z-logical of the stated code.
- Dual X-type operator: the witness itself is not an X-logical (H_Z u != 0). Derived by hand: v = (P u2, P u1), halves swapped and P applied. Since B^T P = P B and A^T P = P A, H_Z v = P(H_X u) = 0. Checker confirmed:
```
v weight 28 H_Z v=0 True in rowspace(H_X) False
```
  The X-type claim holds, but the package ships only the Z-type vector; the X vector comes from this symmetry.
- Scope: only the upper bound (30 to 28) is demonstrated, which is all the claim and p1 ask for.
- Not checked: novelty against the upstream status source (no network, outside this role).

## Cross-check
I did not run the author's script. I only read verify-it-yourself/RECEIPTS.md, which reports the same numbers (rank 246/246, k 12, weight 28, left 12, right 16), agreeing with my independent results.

## Verdict
Every property the verification method asks for is confirmed by my own checker, in the convention that passes (shown above).

pass: true
